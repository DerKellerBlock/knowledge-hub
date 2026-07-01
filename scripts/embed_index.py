#!/usr/bin/env python3
"""
Build ChromaDB + BM25 index from all domain sources.

Per-Domain isolated: each domain gets its own ChromaDB at
chromadb_data/<domain>/chroma/ and BM25 at chromadb_data/<domain>/<domain>_bm25.pkl.

Usage:
  python scripts/embed_index.py --domain godot
  python scripts/embed_index.py --all
"""

import argparse
import importlib.util
import os
import sys
from pathlib import Path

import sys as _sys
_pkg_root = Path(__file__).resolve().parent.parent
if str(_pkg_root) not in _sys.path:
    _sys.path.insert(0, str(_pkg_root))
from model_manager import get_embedder, get_chroma_client
from mcp_servers.knowledge_hub.config import (
    DOMAINS_DIR,
    domain_chroma_path,
    domain_bm25_path,
)
from parser_base import Chunk, DomainParser, fallback_chunk, markdown_section_chunk
from bm25_search import build_bm25_index as build_bm25, get_bm25_index_size_mb
from migration import migrate_legacy_layout


def get_parser(domain: str) -> DomainParser | None:
    """Discover and load a domain-specific parser, if one exists."""
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


def _encode_robust(model, texts: list[str]) -> "list":
    """Embed texts with memory-robust batching.

    Long-context embedding models (e.g. BGE-M3, 8192 token context) can
    exhaust accelerator memory when a batch mixes very long and short
    texts: the attention buffer is sized to the longest sequence in the
    batch, so a single 58k-char chunk next to 31 short chunks tries to
    allocate a multi-GiB attention matrix and aborts with
    ``RuntimeError: Invalid buffer size``.

    Strategy (Phase 2a, addresses MPS/SDPA OOM with BGE-M3):

    1. Sort chunks by length so each batch contains similarly-sized texts
       (avoids one outlier inflating the whole batch's attention buffer).
    2. Use a large batch (32) for short texts and ``batch_size=1`` for the
       long tail (>= 4000 chars), which keeps throughput high for the bulk
       of short Godot/RST chunks while preventing OOM on the few very long
       ones.
    3. Concatenate the partial embeddings back into the original chunk
       order so ChromaDB metadata alignment is preserved.

    This is a build-time helper only; ``hybrid_search`` still calls
    ``model.encode`` directly on a single query (no batching issue there).
    """
    import numpy as np

    if not texts:
        return []

    # Indices sorted by text length ascending; we encode in three buckets
    # so the long tail gets batch_size=1 and the bulk gets batch_size=32.
    order = sorted(range(len(texts)), key=lambda i: len(texts[i]))

    LONG_THRESHOLD = 4000  # chars; ~1000 tokens, safe for bs=1 long-context
    short_idx = [i for i in order if len(texts[i]) < LONG_THRESHOLD]
    long_idx = [i for i in order if len(texts[i]) >= LONG_THRESHOLD]
    print(
        f"[INFO]  Embedding batches: {len(short_idx)} short (<{LONG_THRESHOLD}c, bs=32) "
        f"+ {len(long_idx)} long (bs=1)"
    )

    out = [None] * len(texts)

    # Short bucket — high throughput.
    if short_idx:
        short_texts = [texts[i] for i in short_idx]
        short_emb = model.encode(
            short_texts, batch_size=32, show_progress_bar=True,
            convert_to_numpy=True,
        )
        for j, idx in enumerate(short_idx):
            out[idx] = short_emb[j]

    # Long bucket — bs=1 to keep the attention buffer bounded.
    if long_idx:
        print(f"[INFO]  Encoding {len(long_idx)} long chunks (bs=1)...")
        for k, idx in enumerate(long_idx):
            if k % 50 == 0:
                print(f"[INFO]   long chunk {k}/{len(long_idx)} "
                      f"({len(texts[idx])} chars)")
            emb = model.encode(
                [texts[idx]], batch_size=1, show_progress_bar=False,
                convert_to_numpy=True,
            )
            out[idx] = emb[0]

    result = np.stack(out)
    print(f"[INFO]  Stacked embeddings: {result.shape}")
    return result


def load_domain_sources(domain: str) -> list[Chunk]:
    """Load all source files for a domain. Returns list[Chunk]."""
    domain_dir = DOMAINS_DIR / domain
    parser = get_parser(domain)
    chunks: list[Chunk] = []

    sources_dir = domain_dir / "sources"
    if sources_dir.is_dir():
        for file in sorted(sources_dir.glob("*.md")):
            content = file.read_text(encoding="utf-8")

            if parser:
                try:
                    parsed = parser.parse(str(file), content)
                    for c in parsed:
                        c.source_file = file.name
                        if not c.chunk_id.startswith(f"{domain}::"):
                            c.chunk_id = f"{domain}::{c.chunk_id}"
                    chunks.extend(parsed)
                    if parsed:
                        print(f"[INFO]  Parser '{parser.source_type_name}': "
                              f"{len(parsed)} structured chunks from {file.name}")
                        continue
                    else:
                        print(f"[INFO]  Parser '{parser.source_type_name}': "
                              f"0 structured chunks from {file.name} — falling back")
                except Exception as e:
                    print(f"[WARN]  Parser failed for {file.name}: {e} — falling back")

            fallback = fallback_chunk(
                content, domain=domain, source_type="repo", source_file=file.name
            )
            for i, c in enumerate(fallback):
                c.chunk_id = f"{domain}::fallback::repo::{file.stem}::{i}"
                c.chunk_id_in_file = i
            chunks.extend(fallback)

    personal_dir = domain_dir / "personal"
    if personal_dir.is_dir():
        for file in sorted(personal_dir.glob("*.md")):
            content = file.read_text(encoding="utf-8")
            category = file.stem
            # Markdown section chunking: each `## ` section becomes its own
            # chunk (with `name` set to the section heading) so cross-encoder
            # semantics aren't diluted by long single-chunk files like
            # gotchas.md. Falls back to fallback_chunk for files without
            # `## ` headers.
            chunks.extend(
                markdown_section_chunk(
                    content,
                    domain=domain,
                    source_type="personal",
                    source_file=file.name,
                    category=category,
                )
            )

    return chunks


def build_index(domain: str) -> None:
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

    model = get_embedder(domain)
    print(f"[INFO]  Embedding with {model.__class__.__name__}...")
    texts = [c.text for c in chunks]
    embeddings = _encode_robust(model, texts)

    # B7: log the embedding dimension after the first encode so a
    # silent model swap (e.g. 768d → 1024d) is visible in the build log.
    # We don't assert against an expected value because it is
    # model-dependent; the log line is a diagnostic, not a gate.
    if embeddings is not None and len(embeddings) > 0:
        dim = len(embeddings[0])
        print(f"[INFO]  Embedding dimension: {dim}")

    client = get_chroma_client(domain)

    try:
        client.delete_collection(collection_name)
        print(f"[INFO]  Deleted existing collection '{collection_name}'")
    except Exception:
        pass

    collection = client.create_collection(
        name=collection_name,
        metadata={
            "domain": domain,
            "hnsw:space": "cosine",
        },
    )

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

    print(f"[INFO]  Building BM25 index...")
    build_bm25(domain, chunks)
    bm25_mb = get_bm25_index_size_mb(domain)

    chroma_path = domain_chroma_path(domain)
    chroma_size = sum(
        os.path.getsize(os.path.join(r, f))
        for r, _, fs in os.walk(str(chroma_path))
        for f in fs
        if os.path.exists(os.path.join(r, f))
    )
    print(f"[INFO]  ✓ Collection '{collection_name}' built: "
          f"{len(chunks)} chunks, ChromaDB ~{chroma_size / 1024 / 1024:.0f} MB, "
          f"BM25 {bm25_mb} MB")


def main():
    parser = argparse.ArgumentParser(description="Build ChromaDB + BM25 index")
    parser.add_argument("--domain", type=str, help="Single domain to index")
    parser.add_argument("--all", action="store_true", help="Index all domains")
    args = parser.parse_args()

    if not args.domain and not args.all:
        parser.print_help()
        sys.exit(1)

    # Run migration if needed
    print("[INFO]  Checking for legacy layout migration...")
    migrate_legacy_layout()

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

    for domain in domains:
        print(f"\n{'=' * 60}")
        print(f"  Building index for: {domain}")
        parser_info = get_parser(domain)
        if parser_info:
            print(f"  Parser: {parser_info.source_type_name}")
        else:
            print(f"  Parser: none (fallback chunking)")
        print(f"{'=' * 60}")
        build_index(domain)

    print(f"\n[INFO]  Done.")


if __name__ == "__main__":
    main()
