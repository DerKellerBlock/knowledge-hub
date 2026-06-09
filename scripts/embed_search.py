#!/usr/bin/env python3
"""
Semantic query against ChromaDB index.

Usage:
  python scripts/embed_search.py --domain godot --query "How to add gravity?" --top 5
  python scripts/embed_search.py --domain godot --query "CharacterBody3D" --json

Returns JSON (with --json) or pretty-printed to stdout.
"""

import argparse
import json
import sys
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

HUB_ROOT = Path(__file__).resolve().parent.parent
CHROMA_DIR = HUB_ROOT / "chromadb_data"
MODEL_NAME = "all-mpnet-base-v2"


def semantic_search(
    domain: str, query: str, top_k: int = 5, model: SentenceTransformer | None = None
) -> list[dict]:
    """Semantic search in a domain's knowledge index."""
    collection_name = f"{domain}_knowledge"

    # Load model if not provided
    if model is None:
        model = SentenceTransformer(MODEL_NAME)

    # Connect and query
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    try:
        collection = client.get_collection(collection_name)
    except Exception:
        print(f"[ERROR] Collection '{collection_name}' not found. Run embed_index.py first.")
        sys.exit(1)

    query_embedding = model.encode([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    # Format results with full Chunk metadata
    formatted = []
    for i in range(len(results["ids"][0])):
        meta = results["metadatas"][0][i]
        distance = results["distances"][0][i]
        # Normalize distance to similarity score
        if distance > 2.0:
            score = round(1.0 / (1.0 + distance), 4)   # L2 fallback
        else:
            score = round(1.0 - distance, 4)            # Cosine

        # Parse inherits_from from JSON (stored as json.dumps in parser_base)
        inherits = None
        if meta.get("inherits_from"):
            try:
                inherits = json.loads(meta["inherits_from"])
            except (json.JSONDecodeError, TypeError):
                pass

        entry = {
            "rank": i + 1,
            "score": score,
            "chunk_id": results["ids"][0][i],
            "text": results["documents"][0][i][:500],
            "match_type": "semantic",
            "source_type": meta.get("source_type", "unknown"),
            "domain": meta.get("domain", domain),
            "source_file": meta.get("source_file", ""),
            "line_start": meta.get("line_start", 0),
            "line_end": meta.get("line_end", 0),
            # Structured fields (None if not present)
            "chunk_type": meta.get("chunk_type"),
            "class_name": meta.get("class_name"),
            "name": meta.get("name"),
            "signature": meta.get("signature"),
            "inherits_from": inherits,
        }

        formatted.append(entry)

    return formatted


def main():
    parser = argparse.ArgumentParser(
        description="Semantic search in Knowledge Hub"
    )
    parser.add_argument("--domain", type=str, required=True, help="Domain to search")
    parser.add_argument("--query", type=str, required=True, help="Search query")
    parser.add_argument("--top", type=int, default=5, help="Number of results")
    parser.add_argument(
        "--json", action="store_true", help="Output as JSON"
    )

    args = parser.parse_args()

    print(f"[INFO]  Semantic search in '{args.domain}_knowledge': {args.query}")
    print(f"[INFO]  Loading model {MODEL_NAME}...")

    model = SentenceTransformer(MODEL_NAME)
    results = semantic_search(args.domain, args.query, args.top, model)

    if args.json:
        print(json.dumps({"results": results, "total_found": len(results)}, indent=2))
    else:
        for r in results:
            source_label = f"[{r['source_type']}:{r['source_file']}]"
            print(f"\n  #{r['rank']} {source_label} (score: {r['score']})")
            print(f"  {r['text'][:200]}...")

    print(f"\n[INFO]  Found {len(results)} results")


if __name__ == "__main__":
    main()
