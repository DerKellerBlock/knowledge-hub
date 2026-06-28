"""Integration tests for hybrid_search.search with all three modes."""

import pytest

pytestmark = pytest.mark.integration


def test_hybrid_search_returns_results(indexed_dummy):
    """Hybrid search should return results for a relevant query."""
    from hybrid_search import search

    result = search(indexed_dummy, "Node3D rotate", mode="hybrid", top_k=10)
    assert result["total_found"] >= 1
    assert "results" in result
    assert "query_time_ms" in result
    assert result["mode"] == "hybrid"


def test_exact_mode_returns_bm25_results(indexed_dummy):
    """Exact mode should return results with match_type='bm25'."""
    from hybrid_search import search

    result = search(indexed_dummy, "Node3D rotate", mode="exact", top_k=10)
    assert result["mode"] == "exact"
    if result["results"]:
        assert result["results"][0]["match_type"] == "bm25"


def test_semantic_mode_returns_semantic_results(indexed_dummy):
    """Semantic mode should return results with match_type='semantic'."""
    from hybrid_search import search

    result = search(indexed_dummy, "Node3D rotate", mode="semantic", top_k=10)
    assert result["mode"] == "semantic"
    if result["results"]:
        assert result["results"][0]["match_type"] == "semantic"


def test_hybrid_mode_returns_hybrid_results(indexed_dummy):
    """Hybrid mode should return results with match_type='hybrid'."""
    from hybrid_search import search

    result = search(indexed_dummy, "Node3D rotate", mode="hybrid", top_k=10)
    assert result["mode"] == "hybrid"
    if result["results"]:
        assert result["results"][0]["match_type"] == "hybrid"


def test_source_filter_repo_only(indexed_dummy):
    """source_filter=['repo'] should only return repo-sourced results."""
    from hybrid_search import search

    result = search(indexed_dummy, "Node3D", mode="hybrid", top_k=10, source_filter=["repo"])
    for r in result["results"]:
        assert r.get("source_type") == "repo"


def test_source_filter_personal_only(indexed_dummy):
    """source_filter=['personal'] should only return personal-sourced results."""
    from hybrid_search import search

    result = search(indexed_dummy, "Node3D", mode="hybrid", top_k=10, source_filter=["personal"])
    for r in result["results"]:
        assert r.get("source_type") == "personal"


def test_result_dict_structure(indexed_dummy):
    """Result dict should contain required keys."""
    from hybrid_search import search

    result = search(indexed_dummy, "camera", top_k=5)
    assert "results" in result
    assert "total_found" in result
    assert "mode" in result
    assert "query_time_ms" in result
    assert isinstance(result["total_found"], int)
    assert isinstance(result["query_time_ms"], int)


def test_results_have_text(indexed_dummy):
    """Each result should have non-empty text."""
    from hybrid_search import search

    result = search(indexed_dummy, "Node3D rotate", top_k=5)
    for r in result["results"]:
        assert r.get("text")  # non-empty string