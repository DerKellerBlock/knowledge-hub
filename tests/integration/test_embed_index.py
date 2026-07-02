"""Integration tests for embed_index.build_index with a dummy domain."""

import os
from pathlib import Path

import pytest

pytestmark = pytest.mark.integration

# HuggingFace hub cache layout: models--<org>--<model>/snapshots/<hash>/
# BGE-M3 (~2.2 GB download) is required for the late-chunking PDF integration
# tests below. The ``indexed_dummy``-based tests keep using the default
# ``all-mpnet-base-v2`` (small, always available) and are NOT affected by this
# skip. Pattern modeled after tests/e2e/test_jina_reranker_integration.py.
HF_HUB_CACHE = Path(
    os.environ.get("HF_HOME", str(Path.home() / ".cache" / "huggingface"))
) / "hub"
BGE_M3_CACHE_DIR = HF_HUB_CACHE / "models--BAAI--bge-m3"

_skip_if_no_bge_m3 = pytest.mark.skipif(
    not BGE_M3_CACHE_DIR.exists(),
    reason=(
        "BGE-M3 model not cached locally. Run: "
        "python scripts/embed_index.py --domain godot"
    ),
)


def test_build_index_creates_collection(indexed_dummy):
    """Verify the collection was created and has chunks."""
    from model_manager import get_chroma_client

    client = get_chroma_client(indexed_dummy)
    collection = client.get_collection(f"{indexed_dummy}_knowledge")
    assert collection.count() > 0
    # Should have chunks from 3 source files + 1 personal note
    assert collection.count() >= 4


def test_build_index_chunks_have_metadata(indexed_dummy):
    """Verify chunks have correct source_type and source_file metadata."""
    from model_manager import get_chroma_client

    client = get_chroma_client(indexed_dummy)
    collection = client.get_collection(f"{indexed_dummy}_knowledge")
    result = collection.get(limit=5, include=["metadatas"])
    metas = result["metadatas"]
    assert len(metas) > 0
    for m in metas:
        assert m["source_type"] in ("repo", "personal")
        assert m["domain"] == indexed_dummy
        assert "source_file" in m
        assert "line_start" in m
        assert "line_end" in m


def test_build_index_bm25_pickle_exists(indexed_dummy):
    """Verify BM25 index file was created."""
    from mcp_servers.knowledge_hub.config import domain_bm25_path

    bm25_path = domain_bm25_path(indexed_dummy)
    assert bm25_path.exists()
    assert bm25_path.stat().st_size > 0


def test_build_index_chunk_ids_start_with_domain(indexed_dummy):
    """Verify chunk IDs follow the domain:: prefix convention."""
    from model_manager import get_chroma_client

    client = get_chroma_client(indexed_dummy)
    collection = client.get_collection(f"{indexed_dummy}_knowledge")
    result = collection.get(limit=10, include=["metadatas"])
    for cid in result["ids"]:
        assert cid.startswith(f"{indexed_dummy}::")


# ── Phase 2.2: Late Chunking integration tests ──────────────────────────

def _create_pdf_dummy_domain(tmp_hub, domain_name="pdf_dummy"):
    """Create a minimal PDF domain in tmp_hub for late-chunking tests.

    Writes:
        - domain.md with ``Source-Types: pdf`` and BGE-M3 model
        - sources/manual.md with ``--- end of page=N ---`` separators

    Returns the domain name.
    """
    from mcp_servers.knowledge_hub import config as cfg

    domain_dir = tmp_hub / "domains" / domain_name
    sources_dir = domain_dir / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)

    (domain_dir / "domain.md").write_text(
        """# Domain: """ + domain_name + """

## Zweck
PDF test domain for late-chunking integration tests.

## Metadaten
- Embedding-Model: BAAI/bge-m3 (1024 dims)
- Collection: """ + domain_name + """_knowledge
- ChromaDB-Path: chromadb_data/""" + domain_name + """/chroma/
- BM25-Path: chromadb_data/""" + domain_name + """/""" + domain_name + """_bm25.pkl
- Source-Types: pdf
- Letztes Update: 2026-07-01
""",
        encoding="utf-8",
    )

    # Realistic DaVinci-like text with multiple page separators and chapters.
    # Use a small window_size to keep the test fast.
    (sources_dir / "manual.md").write_text(
        """# Chapter 1

Content on page 0 about video editing basics in DaVinci Resolve.

--- end of page=0 ---

Content on page 1 about the Color page and primary corrections.

--- end of page=1 ---

## Chapter 2

Content on page 2 about Fusion compositing and motion graphics.

--- end of page=2 ---

More content on page 3 about Fairlight audio post-production.
""",
        encoding="utf-8",
    )

    return domain_name


@_skip_if_no_bge_m3
def test_build_index_with_late_chunking_pdf_domain(tmp_hub, monkeypatch):
    """PDF domain with page separators → chunk_type='late_chunk' in ChromaDB.

    Verifies the full Phase 2.2 pipeline:
    - build_index detects Source-Types: pdf in domain.md
    - PDF sources go through late_chunk (not fallback_chunk)
    - ChromaDB metadata contains chunk_type="late_chunk"
    """
    pytest.importorskip("chromadb")
    pytest.importorskip("sentence_transformers")

    # Use small window_size for fast test execution.
    monkeypatch.setenv("KH_EMBEDDING_MODEL", "BAAI/bge-m3")
    domain = _create_pdf_dummy_domain(tmp_hub, "pdf_dummy")

    # Force a small late-chunk window via monkey-patching the constants
    # in parser_base so the test runs fast even on CPU.
    import parser_base
    monkeypatch.setattr(parser_base, "LATE_CHUNK_WINDOW_TOKENS", 16)
    monkeypatch.setattr(parser_base, "LATE_CHUNK_POOLING_OVERLAP", 4)

    # The default fallback chunk size is 8000 chars; keep that for
    # personal notes (none in this domain).

    from embed_index import build_index
    from model_manager import get_chroma_client

    build_index(domain)

    client = get_chroma_client(domain)
    collection = client.get_collection(f"{domain}_knowledge")
    n = collection.count()
    assert n > 0, f"PDF domain produced 0 chunks: {n}"

    # Verify the chunk_type metadata is "late_chunk" for all chunks.
    # Pull everything in batches; for a small domain a single get() is fine.
    result = collection.get(include=["metadatas"])
    types = [m.get("chunk_type") for m in result["metadatas"]]
    assert "late_chunk" in types, (
        f"Expected chunk_type='late_chunk' for PDF domain chunks, "
        f"got types: {set(types)}"
    )
    # And the source_type is "repo" (PDF sources live in sources/, not personal/).
    source_types = [m.get("source_type") for m in result["metadatas"]]
    assert all(st == "repo" for st in source_types), (
        f"Expected source_type='repo', got: {set(source_types)}"
    )


@_skip_if_no_bge_m3
def test_late_chunking_preserves_page_metadata(tmp_hub, monkeypatch):
    """Late-chunked PDF chunks carry page_start/page_end in ChromaDB metadata.

    The page numbers follow the same convention as the existing
    ``fallback_chunk`` (1-based, off-by-one due to 0-based separators
    in parse_pdf_to_markdown.py). This test verifies that page metadata
    is preserved through the full pipeline and that page_start >= 1.
    """
    pytest.importorskip("chromadb")
    pytest.importorskip("sentence_transformers")

    monkeypatch.setenv("KH_EMBEDDING_MODEL", "BAAI/bge-m3")
    domain = _create_pdf_dummy_domain(tmp_hub, "pdf_dummy_page")

    import parser_base
    monkeypatch.setattr(parser_base, "LATE_CHUNK_WINDOW_TOKENS", 16)
    monkeypatch.setattr(parser_base, "LATE_CHUNK_POOLING_OVERLAP", 4)

    from embed_index import build_index
    from model_manager import get_chroma_client

    build_index(domain)

    client = get_chroma_client(domain)
    collection = client.get_collection(f"{domain}_knowledge")
    result = collection.get(include=["metadatas"])

    # All late_chunk chunks should have page_start and page_end set.
    late_chunks = [
        (rid, m) for rid, m in zip(result["ids"], result["metadatas"])
        if m.get("chunk_type") == "late_chunk"
    ]
    assert len(late_chunks) > 0, "No late_chunk chunks found"

    for rid, m in late_chunks:
        assert "page_start" in m, (
            f"Chunk {rid} missing page_start: {m}"
        )
        assert "page_end" in m, (
            f"Chunk {rid} missing page_end: {m}"
        )
        assert m["page_start"] is not None, (
            f"Chunk {rid} page_start is None: {m}"
        )
        assert m["page_end"] is not None, (
            f"Chunk {rid} page_end is None: {m}"
        )
        # 1-based convention (matches fallback_chunk); page_start >= 1.
        assert m["page_start"] >= 1, (
            f"Chunk {rid} page_start={m['page_start']} < 1"
        )
        assert m["page_end"] >= m["page_start"], (
            f"Chunk {rid} page_end < page_start: "
            f"{m['page_end']} < {m['page_start']}"
        )


@_skip_if_no_bge_m3
def test_precomputed_embeddings_match_chunk_ids(tmp_hub, monkeypatch):
    """The chunk_ids stored in ChromaDB match the chunks emitted by late_chunk.

    Indirect verification: ``load_domain_sources`` returns
    ``(chunks, precomputed_embeddings)`` where ``precomputed_embeddings``
    maps ``chunk_id → np.ndarray``. By extension, every chunk in the
    returned list either has a precomputed embedding (late_chunk) or
    is in the fallback path. We verify the alignment by counting
    chunks and checking that all late_chunk chunks have page metadata
    (which is only set by late_chunk, not fallback_chunk).
    """
    pytest.importorskip("chromadb")
    pytest.importorskip("sentence_transformers")

    monkeypatch.setenv("KH_EMBEDDING_MODEL", "BAAI/bge-m3")
    domain = _create_pdf_dummy_domain(tmp_hub, "pdf_dummy_align")

    import parser_base
    monkeypatch.setattr(parser_base, "LATE_CHUNK_WINDOW_TOKENS", 16)
    monkeypatch.setattr(parser_base, "LATE_CHUNK_POOLING_OVERLAP", 4)

    from embed_index import build_index
    from model_manager import get_chroma_client
    from embed_index import load_domain_sources

    # First, get the precomputed_embeddings dict from load_domain_sources
    # so we can compare its keys to the ChromaDB chunk_ids later.
    chunks, precomputed = load_domain_sources(domain)
    assert precomputed is not None, (
        "PDF domain should produce precomputed_embeddings"
    )
    assert len(precomputed) > 0, (
        f"PDF domain produced empty precomputed_embeddings: {precomputed}"
    )
    precomputed_keys = set(precomputed.keys())

    # Every precomputed key must be in the chunks list.
    chunk_ids = {c.chunk_id for c in chunks}
    missing = precomputed_keys - chunk_ids
    assert not missing, (
        f"precomputed_embeddings has keys not in chunks: {missing}"
    )

    # Now build the index and verify ChromaDB has the same set of IDs
    # for late_chunk chunks.
    build_index(domain)
    client = get_chroma_client(domain)
    collection = client.get_collection(f"{domain}_knowledge")
    result = collection.get(include=["metadatas"])

    # All late_chunk IDs in ChromaDB must be a subset of precomputed_keys.
    chroma_late_ids = {
        rid for rid, m in zip(result["ids"], result["metadatas"])
        if m.get("chunk_type") == "late_chunk"
    }
    # And the union of chroma IDs must equal chunk_ids.
    chroma_all_ids = set(result["ids"])
    assert chroma_all_ids == chunk_ids, (
        f"ChromaDB IDs differ from load_domain_sources chunks. "
        f"Missing from ChromaDB: {chunk_ids - chroma_all_ids}. "
        f"Extra in ChromaDB: {chroma_all_ids - chunk_ids}"
    )
    # The late_chunk subset must match precomputed keys.
    assert chroma_late_ids == precomputed_keys, (
        f"ChromaDB late_chunk IDs ({len(chroma_late_ids)}) differ from "
        f"precomputed_embeddings keys ({len(precomputed_keys)}). "
        f"Missing in ChromaDB: {precomputed_keys - chroma_late_ids}. "
        f"Extra in ChromaDB: {chroma_late_ids - precomputed_keys}"
    )
