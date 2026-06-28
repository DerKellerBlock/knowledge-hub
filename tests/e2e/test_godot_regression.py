"""E2E regression tests against the prebuilt Godot index.

These tests require chromadb_data/godot/ to exist (prebuilt via
embed_index.py --domain godot). They verify that the real index returns
content-relevant results, not just any results.

Run: pytest tests/e2e/test_godot_regression.py -v -m e2e
"""

import pytest

from pathlib import Path

HUB_ROOT = Path(__file__).resolve().parent.parent.parent
GODOT_INDEX = HUB_ROOT / "chromadb_data" / "godot" / "chroma"

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.skipif(
        not GODOT_INDEX.exists(),
        reason="Godot index not built. Run: python scripts/embed_index.py --domain godot",
    ),
]


def test_godot_node3d_search_finds_relevant_results():
    """Search for 'Node3D rotate' should return results mentioning Node3D/Spatial/rotate."""
    from hybrid_search import search

    result = search("godot", "Node3D rotate", mode="hybrid", top_k=10)
    assert result["total_found"] >= 1
    # Content relevance: top 3 results should mention the topic
    top3_text = " ".join(r.get("text", "") for r in result["results"][:3]).lower()
    assert any(kw in top3_text for kw in ["node3d", "spatial", "rotate", "rotation"])


def test_godot_search_returns_metadata():
    """First result should have source_file and non-empty text."""
    from hybrid_search import search

    result = search("godot", "Node3D", top_k=5)
    assert result["total_found"] >= 1
    r = result["results"][0]
    assert r.get("source_file")
    assert r.get("text")
    assert r["chunk_id"].startswith("godot::")


def test_godot_all_search_modes_work():
    """exact, semantic, and hybrid modes should all return results."""
    from hybrid_search import search

    for mode in ["exact", "semantic", "hybrid"]:
        result = search("godot", "Node3D rotate", mode=mode, top_k=5)
        assert result["total_found"] >= 1, f"mode={mode} returned no results"


def test_godot_hybrid_under_10_seconds():
    """Hybrid search should complete in under 10 seconds."""
    from hybrid_search import search

    result = search("godot", "Node3D rotate", mode="hybrid", top_k=10)
    assert result["query_time_ms"] <= 10000


def test_godot_search_result_structure():
    """Result dict should have all required keys."""
    from hybrid_search import search

    result = search("godot", "camera", top_k=3)
    assert "results" in result
    assert "total_found" in result
    assert "mode" in result
    assert "query_time_ms" in result
    assert isinstance(result["results"], list)