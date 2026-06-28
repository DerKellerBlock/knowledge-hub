"""Integration tests for embed_index.build_index with a dummy domain."""

import pytest

pytestmark = pytest.mark.integration


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