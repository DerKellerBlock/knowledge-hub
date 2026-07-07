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
from model_manager import get_embedder, get_chroma_client, get_domain_config
# Live-lookup import for path constants so monkeypatching in tests works.
# `from X import Y` binds the value at import time; for immutable values
# like Path, the test fixture's ``monkeypatch.setattr(cfg, "DOMAINS_DIR", ...)``
# would not be visible here. We look up ``_config.DOMAINS_DIR`` at call time
# (mirroring the pattern in ``model_manager.get_domain_config``).
from mcp_servers.knowledge_hub import config as _config
from mcp_servers.knowledge_hub.config import (
    domain_chroma_path,
    domain_bm25_path,
)
from parser_base import Chunk, DomainParser, fallback_chunk, markdown_section_chunk, late_chunk
from bm25_search import build_bm25_index as build_bm25, get_bm25_index_size_mb
from migration import migrate_legacy_layout


def get_parser(domain: str) -> DomainParser | None:
    """Discover and load a domain-specific parser, if one exists."""
    parser_path = _config.DOMAINS_DIR / domain / "parser.py"
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


def load_domain_sources(
    domain: str,
) -> tuple[list[Chunk], dict | None]:
    """Load all source files for a domain.

    Returns:
        ``(chunks, precomputed_embeddings)`` where ``chunks`` is the
        full list of Chunks for the domain and ``precomputed_embeddings``
        is a ``dict[chunk_id, np.ndarray]`` for chunks whose embeddings
        were computed during chunking (Phase 2.2 late chunking only).

        For non-PDF domains (or PDF domains with a domain-specific
        parser) ``precomputed_embeddings`` is ``None`` — the caller
        must embed the chunks via ``_encode_robust`` instead.

    Late chunking (Phase 2.2) is only enabled for PDF domains WITHOUT
    a domain-specific parser, where ``late_chunk`` produces
    token-level-aware embeddings at chunking time. The embedder
    model is loaded on demand (cached by ``model_manager``).
    """
    import numpy as np

    domain_dir = _config.DOMAINS_DIR / domain
    parser = get_parser(domain)
    chunks: list[Chunk] = []
    precomputed: dict[str, "np.ndarray"] = {}

    # PDF domain detection: source_types contains "pdf" in domain.md.
    is_pdf_domain = "pdf" in get_domain_config(domain).get(
        "source_types", ["repo"]
    )
    use_late_chunk = is_pdf_domain and parser is None

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

            # Late chunking path (Phase 2.2): PDF domains without a
            # domain-specific parser use chapter-wise late chunking,
            # producing precomputed token-level embeddings that span
            # chapter boundaries (no arbitrary character splits).
            if use_late_chunk:
                try:
                    model = get_embedder(domain)
                    late_chunks, late_precomputed = late_chunk(
                        content,
                        domain=domain,
                        source_file=file.name,
                        model=model,
                    )
                    if late_chunks:
                        print(f"[INFO]  Late chunking: {len(late_chunks)} "
                              f"chunks from {file.name} "
                              f"(chapter-wise BGE-M3 token pooling)")
                        chunks.extend(late_chunks)
                        precomputed.update(late_precomputed)
                        continue
                    else:
                        print(f"[INFO]  Late chunking: 0 chunks from "
                              f"{file.name} — falling back to fallback_chunk")
                except Exception as e:
                    print(f"[WARN]  Late chunking failed for {file.name}: "
                          f"{type(e).__name__}: {e} — falling back")

            # Default fallback (Godot RST, non-PDF repos, late_chunk
            # disabled or failed).
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

    precomputed_or_none = precomputed if precomputed else None
    return chunks, precomputed_or_none


def build_index(domain: str, contextualize: bool = False,
                contextualize_bm25: bool = False,
                embed_images: bool = False) -> None:
    """Build ChromaDB + BM25 index for a single domain.

    Phase 2.2: For PDF domains (e.g. DaVinci Resolve), if
    ``load_domain_sources`` returns precomputed embeddings (from
    ``late_chunk``), those are used directly for the late_chunk
    chunks. Other chunks (e.g. personal notes, or fallback_chunks
    in mixed domains) are still embedded via ``_encode_robust``.

    Phase 3.1: When ``contextualize=True``, an LLM-generated
    ``context_prefix`` is prepended to the chunk text for embedding
    input only (``context_prefix + "\\n" + text``). ChromaDB documents
    and BM25 continue to see clean ``text`` (D1). Contextualization is
    opt-in via the ``--contextualize`` CLI flag (default off →
    backward-compatible).
    """
    import numpy as np

    collection_name = f"{domain}_knowledge"

    print(f"[INFO]  Loading domain: {domain}")
    chunks, precomputed_embeddings = load_domain_sources(domain)

    if not chunks:
        print(f"[WARN]  No chunks found for domain '{domain}'")
        return

    repo_count = sum(1 for c in chunks if c.source_type == "repo")
    personal_count = sum(1 for c in chunks if c.source_type == "personal")
    late_count = sum(1 for c in chunks if c.chunk_type == "late_chunk")
    print(f"[INFO]  Parsed into {len(chunks)} chunks "
          f"(repo: {repo_count}, personal: {personal_count}, "
          f"late_chunk: {late_count})")

    # Phase 3.1: Contextualize chunks (opt-in via --contextualize).
    # Generates an LLM ``context_prefix`` for each Path-A chunk
    # (chunk_type != "late_chunk") and persists it in the per-domain
    # SQLite cache. The prefix is prepended to the chunk text for
    # embedding input only (D1); ChromaDB documents and BM25 keep
    # clean ``text``.
    if contextualize and chunks:
        if contextualize_bm25:
            print("[INFO]  Contextual BM25 enabled — BM25 corpus includes "
                  "context_prefix")
        print(f"[INFO]  Contextualizing chunks (Phase 3.1)...")
        from contextualize_chunks import (
            contextualize_chunks as _contextualize,
            check_ollama_available,
        )
        from context_cache import open_cache
        from model_manager import DEFAULT_LLM_MODEL, get_llm
        llm_entry = get_llm()
        check_ollama_available(llm_entry)
        model_name = os.environ.get("KH_LLM_MODEL", DEFAULT_LLM_MODEL)
        conn = open_cache(domain)
        try:
            # Path-A filter (Spec N1): exclude late_chunk chunks. The
            # ``contextualize_chunks`` function does not re-filter (its
            # contract expects a pre-filtered list), so filter here.
            path_a_chunks = [c for c in chunks if c.chunk_type != "late_chunk"]
            _contextualize(domain, path_a_chunks, llm_entry, conn, model_name)
            contextualized_count = sum(1 for c in chunks if c.context_prefix)
            print(f"[INFO]  Contextualized {contextualized_count}/{len(chunks)} "
                  f"chunks")
        finally:
            conn.close()

    # Build the per-chunk embedding array aligned with `chunks`. If
    # precomputed_embeddings is present (PDF domain with late_chunk),
    # use those for the late_chunk chunks; embed everything else via
    # _encode_robust. This keeps Godot's RST parser path and personal
    # notes' markdown_section_chunk path unchanged.
    if precomputed_embeddings:
        # Determine which chunk indices have precomputed embeddings.
        precomputed_indices = [
            i for i, c in enumerate(chunks) if c.chunk_id in precomputed_embeddings
        ]
        fallback_indices = [
            i for i, c in enumerate(chunks) if c.chunk_id not in precomputed_embeddings
        ]
        print(
            f"[INFO]  Precomputed embeddings: {len(precomputed_indices)} "
            f"(from late_chunk); to-embed: {len(fallback_indices)}"
        )

        # Embed fallback chunks via _encode_robust.
        if fallback_indices:
            model = get_embedder(domain)
            print(f"[INFO]  Embedding {len(fallback_indices)} fallback "
                  f"chunks with {model.__class__.__name__}...")
            if contextualize:
                fallback_texts = [
                    (chunks[i].context_prefix + "\n" + chunks[i].text)
                    if chunks[i].context_prefix else chunks[i].text
                    for i in fallback_indices
                ]
            else:
                fallback_texts = [chunks[i].text for i in fallback_indices]
            fallback_emb = _encode_robust(model, fallback_texts)
        else:
            fallback_emb = None

        # Assemble the full aligned embedding array. We need
        # ``len(chunks)`` rows, in chunk order.
        n_chunks = len(chunks)
        dim = None
        if precomputed_indices:
            dim = precomputed_embeddings[chunks[precomputed_indices[0]].chunk_id].shape[-1]
        elif fallback_emb is not None and len(fallback_emb) > 0:
            dim = len(fallback_emb[0])
        if dim is None:
            # Nothing to embed (no chunks have embeddings) — defensive
            dim = 0

        embeddings = np.zeros((n_chunks, dim), dtype=np.float32)
        for i in precomputed_indices:
            cid = chunks[i].chunk_id
            embeddings[i] = precomputed_embeddings[cid]
        if fallback_indices and fallback_emb is not None:
            for j, idx in enumerate(fallback_indices):
                embeddings[idx] = fallback_emb[j]
    else:
        # Default path: encode all chunks via _encode_robust.
        model = get_embedder(domain)
        print(f"[INFO]  Embedding with {model.__class__.__name__}...")
        if contextualize:
            texts = [
                (c.context_prefix + "\n" + c.text) if c.context_prefix else c.text
                for c in chunks
            ]
        else:
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
    build_bm25(domain, chunks, use_context_prefix=contextualize_bm25)
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

    # Vision Retrieval Feature: build image BM25 index from cached captions.
    # This is additive — it does NOT touch the text index. Requires
    # image_manifest.json + image_caption_cache.db to exist (built by
    # extract_pdf_images.py + caption_images.py).
    if embed_images:
        print("[INFO]  Building image BM25 index (Vision Retrieval Feature)...")
        from bm25_search import build_image_bm25_index, get_image_bm25_index_size_mb
        from mcp_servers.knowledge_hub.config import domain_image_manifest_path
        from image_caption_cache import open_cache as open_caption_cache
        import json as _json
        import os as _os

        manifest_path = domain_image_manifest_path(domain)
        if not manifest_path.exists():
            print(f"[WARN]  No image_manifest.json for '{domain}' — "
                  f"run extract_pdf_images.py first. Skipping image BM25.")
        else:
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = _json.load(f)
            image_entries = manifest.get("images", [])

            # Inject cached captions into entries.
            llm_model = _os.environ.get("KH_LLM_MODEL", "gemma4:cloud")
            cap_conn = open_caption_cache(domain)
            try:
                rows = cap_conn.execute(
                    "SELECT image_id, caption FROM image_caption_cache "
                    "WHERE model = ?",
                    (llm_model,),
                ).fetchall()
                cap_map = {row[0]: row[1] for row in rows}
            finally:
                cap_conn.close()

            for entry in image_entries:
                entry["caption"] = cap_map.get(entry["image_id"], "")

            cap_count = sum(1 for e in image_entries if e["caption"])
            print(f"[INFO]  Image manifest: {len(image_entries)} images, "
                  f"{cap_count} with captions (model={llm_model})")

            built = build_image_bm25_index(domain, image_entries)
            img_bm25_mb = get_image_bm25_index_size_mb(domain)
            if built:
                print(f"[INFO]  ✓ Image BM25 built: {img_bm25_mb} MB")
            else:
                print(f"[WARN]  Image BM25 not built (no captions or empty)")


def main():
    parser = argparse.ArgumentParser(description="Build ChromaDB + BM25 index")
    parser.add_argument("--domain", type=str, help="Single domain to index")
    parser.add_argument("--all", action="store_true", help="Index all domains")
    parser.add_argument(
        "--contextualize",
        action="store_true",
        help="Generate LLM context prefix for chunks (Phase 3.1). "
             "Default: off (no context prefix).",
    )
    parser.add_argument(
        "--contextualize-bm25",
        action="store_true",
        help="Also use context_prefix in BM25 (Contextual BM25, "
             "experimental). Implies --contextualize.",
    )
    parser.add_argument(
        "--embed-images",
        action="store_true",
        help="Build image BM25 index from cached captions (Vision Retrieval "
             "Feature). Requires image_manifest.json + image_caption_cache.db "
             "(run extract_pdf_images.py + caption_images.py first). Does NOT "
             "re-embed images — use embed_images.py for that.",
    )
    args = parser.parse_args()

    if not args.domain and not args.all:
        parser.print_help()
        sys.exit(1)

    contextualize = args.contextualize or args.contextualize_bm25
    contextualize_bm25 = args.contextualize_bm25

    # Run migration if needed
    print("[INFO]  Checking for legacy layout migration...")
    migrate_legacy_layout()

    if args.all:
        domains = [
            d.name
            for d in _config.DOMAINS_DIR.iterdir()
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
        build_index(domain, contextualize=contextualize,
                    contextualize_bm25=contextualize_bm25,
                    embed_images=args.embed_images)

    print(f"\n[INFO]  Done.")


if __name__ == "__main__":
    main()
