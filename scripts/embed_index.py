#!/usr/bin/env python3
"""
Build ChromaDB index from all domain sources.

Usage:
  python scripts/embed_index.py --domain godot
  python scripts/embed_index.py --all

Workflow:
  1. Scan domains/<domain>/sources/*.md + personal/*.md
  2. Chunking: ~500 tokens per chunk, ~100 token overlap
  3. Embedding: all-mpnet-base-v2 (768-dim) via sentence-transformers
  4. Store in ChromaDB collection "<domain>_knowledge"
  5. Delete old collection, create new (complete rebuild)

Requirements:
  pip install chromadb sentence-transformers
  # First run downloads ~420 MB model (one-time)
"""

import argparse
import os
import sys
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

# ── Config ──────────────────────────────────────────────────────────────────
HUB_ROOT = Path(__file__).resolve().parent.parent
DOMAINS_DIR = HUB_ROOT / "domains"
CHROMA_DIR = HUB_ROOT / "chromadb_data"
MODEL_NAME = "all-mpnet-base-v2"

CHUNK_SIZE = 500       # approximate tokens per chunk
CHUNK_OVERLAP = 100    # token overlap between consecutive chunks

# Estimated: 1 token ≈ 4 chars (English text). Adjust for code/markdown.
CHARS_PER_TOKEN = 4
CHUNK_CHARS = CHUNK_SIZE * CHARS_PER_TOKEN      # 2000 chars
OVERLAP_CHARS = CHUNK_OVERLAP * CHARS_PER_TOKEN # 400 chars


def chunk_text(text: str, chunk_size: int = CHUNK_CHARS, overlap: int = OVERLAP_CHARS) -> list[dict]:
    """Split text into overlapping chunks with metadata."""
    chunks = []
    start = 0
    chunk_id = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end]

        # Find approximate line number for metadata
        line_offset = text[:start].count('\n') + 1

        chunks.append({
            "text": chunk,
            "chunk_id": chunk_id,
            "line_offset": line_offset,
        })

        chunk_id += 1
        start += (chunk_size - overlap)

    return chunks


def load_domain_sources(domain: str) -> list[dict]:
    """Load all source files for a domain. Returns list of {text, metadata}."""
    domain_dir = DOMAINS_DIR / domain
    documents = []

    # Load repo sources
    sources_dir = domain_dir / "sources"
    if sources_dir.is_dir():
        for file in sources_dir.glob("*.md"):
            text = file.read_text(encoding="utf-8")
            source_name = file.stem.replace("-packed", "")

            for chunk in chunk_text(text):
                documents.append({
                    "text": chunk["text"],
                    "metadata": {
                        "source_type": "repo",
                        "domain": domain,
                        "source": source_name,
                        "filename": file.name,
                        "chunk_id_in_file": chunk["chunk_id"],
                        "line_offset": chunk["line_offset"],
                    },
                })

    # Load personal knowledge
    personal_dir = domain_dir / "personal"
    if personal_dir.is_dir():
        for file in sorted(personal_dir.glob("*.md")):
            text = file.read_text(encoding="utf-8")
            category = file.stem

            for chunk in chunk_text(text):
                documents.append({
                    "text": chunk["text"],
                    "metadata": {
                        "source_type": "personal",
                        "domain": domain,
                        "source": category,
                        "filename": file.name,
                        "chunk_id_in_file": chunk["chunk_id"],
                        "line_offset": chunk["line_offset"],
                    },
                })

    return documents


def build_index(domain: str, model: SentenceTransformer) -> None:
    """Build ChromaDB index for a single domain."""
    collection_name = f"{domain}_knowledge"

    print(f"[INFO]  Loading domain: {domain}")
    documents = load_domain_sources(domain)

    if not documents:
        print(f"[WARN]  No documents found for domain '{domain}'")
        return

    print(f"[INFO]  Chunked into {len(documents)} chunks from "
          f"{len(set(d['metadata']['source'] for d in documents))} sources")

    # Embed
    print(f"[INFO]  Embedding with {MODEL_NAME} (768 dims)...")
    texts = [d["text"] for d in documents]
    embeddings = model.encode(texts, show_progress_bar=True)

    # Connect to ChromaDB
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    # Delete existing collection, create new
    try:
        client.delete_collection(collection_name)
        print(f"[INFO]  Deleted existing collection '{collection_name}'")
    except Exception:
        pass

    collection = client.create_collection(
        name=collection_name,
        metadata={"domain": domain, "model": MODEL_NAME, "dimensions": 768},
    )

    # Insert in batches
    batch_size = 500
    for i in range(0, len(documents), batch_size):
        batch = documents[i : i + batch_size]
        batch_embeddings = embeddings[i : i + batch_size]

        collection.add(
            ids=[f"{domain}_chunk_{j}" for j in range(i, i + len(batch))],
            embeddings=batch_embeddings.tolist(),
            documents=[d["text"] for d in batch],
            metadatas=[d["metadata"] for d in batch],
        )
        print(f"[INFO]  Inserted batch {i // batch_size + 1}: {len(batch)} chunks")

    index_size = sum(
        os.path.getsize(os.path.join(r, f))
        for r, _, fs in os.walk(str(CHROMA_DIR / collection_name))
        for f in fs
    )
    print(f"[INFO]  ✓ Collection '{collection_name}' built: "
          f"{len(documents)} chunks, {index_size / 1024 / 1024:.0f} MB")


def main():
    parser = argparse.ArgumentParser(
        description="Build ChromaDB index from domain sources"
    )
    parser.add_argument(
        "--domain",
        type=str,
        help="Single domain to index (e.g., 'godot')",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Index all available domains",
    )

    args = parser.parse_args()

    if not args.domain and not args.all:
        parser.print_help()
        sys.exit(1)

    # Load model (once)
    print(f"[INFO]  Loading embedding model: {MODEL_NAME}")
    print(f"[INFO]  (first run downloads ~420 MB — please wait)")
    model = SentenceTransformer(MODEL_NAME)

    # Determine domains
    if args.all:
        domains = [
            d.name
            for d in DOMAINS_DIR.iterdir()
            if d.is_dir() and (d / "domain.md").exists()
        ]
        if not domains:
            print("[ERROR] No domains found with domain.md")
            sys.exit(1)
        print(f"[INFO]  Found {len(domains)} domain(s): {', '.join(domains)}")
    else:
        domains = [args.domain]

    # Build index per domain
    for domain in domains:
        print(f"\n{'=' * 60}")
        print(f"  Building index for: {domain}")
        print(f"{'=' * 60}")
        build_index(domain, model)

    print(f"\n[INFO]  Done. Index stored at: {CHROMA_DIR}")


if __name__ == "__main__":
    main()
