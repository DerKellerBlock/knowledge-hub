#!/usr/bin/env python3
"""
Semantic query against ChromaDB index (per-domain isolated).

Usage:
  python scripts/embed_search.py --domain godot --query "How to add gravity?" --top 5
"""

import argparse
import json
import sys
from pathlib import Path

import sys as _sys
_pkg_root = Path(__file__).resolve().parent.parent
if str(_pkg_root) not in _sys.path:
    _sys.path.insert(0, str(_pkg_root))
from model_manager import get_embedder, get_chroma_client
from mcp_servers.knowledge_hub.config import DEFAULT_MODEL_NAME


def semantic_search(
    domain: str, query: str, top_k: int = 5, model=None
) -> list[dict]:
    """Semantic search in a domain's knowledge index."""
    collection_name = f"{domain}_knowledge"

    if model is None:
        model = get_embedder(domain)

    client = get_chroma_client(domain)

    try:
        collection = client.get_collection(collection_name)
    except Exception:
        print(f"[ERROR] Collection '{collection_name}' not found. Run embed_index.py first.")
        if __name__ != "__main__":
            raise
        sys.exit(1)

    query_embedding = model.encode([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    formatted = []
    for i in range(len(results["ids"][0])):
        meta = results["metadatas"][0][i]
        distance = results["distances"][0][i]
        if distance > 2.0:
            score = round(1.0 / (1.0 + distance), 4)
        else:
            score = round(1.0 - distance, 4)

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
            "text": results["documents"][0][i][:5000],
            "match_type": "semantic",
            "source_type": meta.get("source_type", "unknown"),
            "domain": meta.get("domain", domain),
            "source_file": meta.get("source_file", ""),
            "line_start": meta.get("line_start", 0),
            "line_end": meta.get("line_end", 0),
            "chunk_type": meta.get("chunk_type"),
            "class_name": meta.get("class_name"),
            "name": meta.get("name"),
            "signature": meta.get("signature"),
            "inherits_from": inherits,
            "page_start": meta.get("page_start"),
            "page_end": meta.get("page_end"),
            "section_path": meta.get("section_path"),
        }
        formatted.append(entry)

    return formatted


def main():
    parser = argparse.ArgumentParser(description="Semantic search in Knowledge Hub")
    parser.add_argument("--domain", type=str, required=True)
    parser.add_argument("--query", type=str, required=True)
    parser.add_argument("--top", type=int, default=5)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    print(f"[INFO]  Semantic search in '{args.domain}_knowledge': {args.query}")
    results = semantic_search(args.domain, args.query, args.top)

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
