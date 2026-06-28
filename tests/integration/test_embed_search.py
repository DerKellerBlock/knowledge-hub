"""Integration tests for embed_search.semantic_search with a real (small) index."""

import pytest

pytestmark = pytest.mark.integration


def test_semantic_search_returns_results(indexed_dummy):
    """Semantic search should return results for a relevant query."""
    from embed_search import semantic_search

    results = semantic_search(indexed_dummy, "How to rotate a 3D node", top_k=5)
    assert len(results) >= 1
    r = results[0]
    assert r["score"] > 0
    assert r["text"]  # non-empty
    assert r["source_file"]  # has source metadata


def test_semantic_search_has_correct_match_type(indexed_dummy):
    """All results should have match_type='semantic'."""
    from embed_search import semantic_search

    results = semantic_search(indexed_dummy, "camera", top_k=3)
    for r in results:
        assert r["match_type"] == "semantic"


def test_semantic_search_ranks_assigned(indexed_dummy):
    """Results should have incremental rank numbers."""
    from embed_search import semantic_search

    results = semantic_search(indexed_dummy, "audio", top_k=5)
    for i, r in enumerate(results):
        assert r["rank"] == i + 1


def test_semantic_search_chunk_ids(indexed_dummy):
    """All chunk IDs should start with the domain prefix."""
    from embed_search import semantic_search

    results = semantic_search(indexed_dummy, "Node3D", top_k=3)
    for r in results:
        assert r["chunk_id"].startswith(f"{indexed_dummy}::")