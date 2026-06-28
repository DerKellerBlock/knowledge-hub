"""Integration tests for bm25_search with a real (small) index."""

import pytest

pytestmark = pytest.mark.integration


def test_bm25_finds_node3d_results(indexed_dummy):
    """BM25 should find results for 'Node3D rotate'."""
    from bm25_search import bm25_search

    results = bm25_search(indexed_dummy, "Node3D rotate", top_k=10)
    assert len(results) >= 1
    assert results[0]["score"] > 0
    assert results[0]["match_type"] == "bm25"


def test_bm25_no_results_for_gibberish(indexed_dummy):
    """BM25 should return empty list for non-matching query."""
    from bm25_search import bm25_search

    results = bm25_search(indexed_dummy, "zzznonexistentword12345", top_k=10)
    assert results == []


def test_bm25_top_k_limits_results(indexed_dummy):
    """top_k should limit the number of results."""
    from bm25_search import bm25_search

    results = bm25_search(indexed_dummy, "Node3D", top_k=1)
    assert len(results) <= 1


def test_bm25_score_positive(indexed_dummy):
    """All returned results should have positive scores."""
    from bm25_search import bm25_search

    results = bm25_search(indexed_dummy, "camera follow", top_k=10)
    for r in results:
        assert r["score"] > 0


def test_bm25_tokenized_query(indexed_dummy):
    """BM25 should handle multi-word queries."""
    from bm25_search import bm25_search

    results = bm25_search(indexed_dummy, "audio bus volume", top_k=10)
    assert len(results) >= 1