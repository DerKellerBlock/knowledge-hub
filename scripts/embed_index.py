#!/usr/bin/env python3
"""
Build ChromaDB + BM25 index from all domain sources.

Usage:
  python scripts/embed_index.py --domain godot
  python scripts/embed_index.py --all

Workflow:
  1. Scan domains/<domain>/sources/*.md + personal/*.md
  2. If domain has parser.py: use structured parsing
     Else: fallback to sliding-window chunking (500 tokens, 100 overlap)
  3. Embedding: all-mpnet-base-v2 (768-dim) via sentence-transformers
  4. Store in ChromaDB collection "<domain>_knowledge" + build BM25 index
  5. Delete old collection + BM25 index, create new (complete rebuild)

Requirements:
  pip install chromadb sentence-transformers rank-bm25
  # First run downloads ~420 MB embedding model + ~130 MB cross-encoder (one-time)
"""

import argparse
import importlib.util
import os
import sys
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from parser_base import Chunk, DomainParser, fallback_chunk
from bm25_search import build_bm25_index as build_bm25

# ── Config ──────────────────────────────────────────────────────────────────
HUB_ROOT = Path(__file__).resolve().parent.parent
DOMAINS_DIR = HUB_ROOT / "domains"
CHROMA_DIR = HUB_ROOT / "chromadb_data"
MODEL_NAME = "all-mpnet-base-v2"


def get_parser(domain: str) -> DomainParser | None:
    """Discover and load a domain-specific parser, if one exists.

    Looks for domains/<domain>/parser.py. The file must contain a class
    named 'Parser' that subclasses DomainParser.
    """
    parser_path = DOMAINS_DIR / domain / "parser.py"
    if not parser_path.exists():
        return None

    try:
        module_name = f"{domain}_parser"
        spec = importlib.util.spec_from_file_location(module_name, parser_path)
        if spec is None or spec.loader is None:
            return None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        parser = module.Parser()
        if not isinstance(parser, DomainParser):
            print(f"[WARN]  Parser for '{domain}' is not a DomainParser — ignoring")
            return None
        return parser
    except Exception as e:
        print(f"[WARN]  Failed to load parser for '{domain}': {e}")
        return None


def load_domain_sources(domain: str) -> list[Chunk]:
    """Load all source files for a domain. Returns list[Chunk].

    - If a parser.py exists, uses it for structured chunks.
    - Otherwise falls back to sliding-window chunking.
    - Personal notes always use fallback chunking.
    """
    domain_dir = DOMAINS_DIR / domain
    parser = get_parser(domain)
    chunks: list[Chunk] = []

    # Load repo sources
    sources_dir = domain_dir / "sources"
    if sources_dir.is_dir():
        for file in sorted(sources_dir.glob("*.md")):
            content = file.read_text(encoding="utf-8")

            if parser:
                # Use domain-specific structured parser
                try:
                    parsed = parser.parse(str(file), content)
                    for c in parsed:
                        c.source_file = file.name
                        if not c.chunk_id.startswith(f"{domain}::"):
                            c.chunk_id = f"{domain}::{c.chunk_id}"
                    chunks.extend(parsed)
                    print(f"[INFO]  Parser '{parser.source_type_name}': "
                          f"{len(parsed)} structured chunks from {file.name}")
                    continue
                except Exception as e:
                    print(f"[WARN]  Parser failed for {file.name}: {e} — falling back")

            # Fallback chunking
            fallback = fallback_chunk(
                content, domain=domain, source_type="repo", source_file=file.name
            )
            # Update chunk_ids to be unique across files
            for i, c in enumerate(fallback):
                c.chunk_id = f"{domain}::fallback::repo::{file.stem}::{i}"
                c.chunk_id_in_file = i
            chunks.extend(fallback)

    # Load personal knowledge (always fallback chunking)
    personal_dir = domain_dir / "personal"
    if personal_dir.is_dir():
        for file in sorted(personal_dir.glob("*.md")):
            content = file.read_text(encoding="utf-8")
            category = file.stem
            fallback = fallback_chunk(
                content, domain=domain, source_type="personal", source_file=file.name
            )
            for i, c in enumerate(fallback):
                c.chunk_id = f"{domain}::personal::{category}::{i}"
                c.chunk_id_in_file = i
                c.name = category  # tag with category for BM25 boosting
            chunks.extend(fallback)

    return chunks


def build_index(domain: str, model: SentenceTransformer) -> None:
    """Build ChromaDB + BM25 index for a single domain."""
    collection_name = f"{domain}_knowledge"

    print(f"[INFO]  Loading domain: {domain}")
    chunks = load_domain_sources(domain)

    if not chunks:
        print(f"[WARN]  No chunks found for domain '{domain}'")
        return

    repo_count = sum(1 for c in chunks if c.source_type == "repo")
    personal_count = sum(1 for c in chunks if c.source_type == "personal")
    print(f"[INFO]  Parsed into {len(chunks)} chunks "
          f"(repo: {repo_count}, personal: {personal_count})")

    # Embed
    print(f"[INFO]  Embedding with {MODEL_NAME} (768 dims)...")
    texts = [c.text for c in chunks]
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
        metadata={
            "domain": domain,
            "model": MODEL_NAME,
            "dimensions": 768,
            "hnsw:space": "cosine",
        },
    )

    # Insert in batches
    batch_size = 500
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        batch_embeddings = embeddings[i : i + batch_size]

        collection.add(
            ids=[c.chunk_id for c in batch],
            embeddings=batch_embeddings.tolist(),
            documents=[c.text for c in batch],
            metadatas=[c.to_chromadb_metadata() for c in batch],
        )
        print(f"[INFO]  Inserted batch {i // batch_size + 1}: {len(batch)} chunks")

    # Build BM25 index
    print(f"[INFO]  Building BM25 index...")
    build_bm25(domain, chunks)
    from bm25_search import get_bm25_index_size_mb
    bm25_mb = get_bm25_index_size_mb(domain)
    print(f"[INFO]  BM25 index built: {bm25_mb} MB")

    # Summary
    chroma_size = sum(
        os.path.getsize(os.path.join(r, f))
        for r, _, fs in os.walk(str(CHROMA_DIR))
        for f in fs
        if os.path.exists(os.path.join(r, f))
    )
    print(f"[INFO]  ✓ Collection '{collection_name}' built: "
          f"{len(chunks)} chunks, ChromaDB ~{chroma_size / 1024 / 1024:.0f} MB, "
          f"BM25 {bm25_mb} MB")


def main():
    parser = argparse.ArgumentParser(
        description="Build ChromaDB + BM25 index from domain sources"
    )
    parser.add_argument(
        "--domain", type=str, help="Single domain to index (e.g., 'godot')"
    )
    parser.add_argument(
        "--all", action="store_true", help="Index all available domains"
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
        parser_info = get_parser(domain)
        if parser_info:
            print(f"  Parser: {parser_info.source_type_name}")
        else:
            print(f"  Parser: none (fallback chunking)")
        print(f"{'=' * 60}")
        build_index(domain, model)

    print(f"\n[INFO]  Done. Index stored at: {CHROMA_DIR}")


if __name__ == "__main__":
    main()
