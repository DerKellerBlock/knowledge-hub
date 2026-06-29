"""E2E regression tests against the prebuilt DaVinci Resolve index.

These tests require chromadb_data/davinci_resolve/ to exist (prebuilt via
embed_index.py --domain davinci_resolve). They verify that the real index
returns content-relevant results from the 10 Blackmagic PDFs.

Run: pytest tests/e2e/test_davinci_regression.py -v -m e2e
"""

import pytest
from pathlib import Path

HUB_ROOT = Path(__file__).resolve().parent.parent.parent
DAVINCI_INDEX = HUB_ROOT / "chromadb_data" / "davinci_resolve" / "chroma"

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.skipif(
        not DAVINCI_INDEX.exists(),
        reason="DaVinci index not built. Run: python scripts/embed_index.py --domain davinci_resolve",
    ),
]


def test_davinci_trim_clip_search_finds_relevant_results():
    """Search for 'trim clip edit' should return results about trimming/editing."""
    from hybrid_search import search

    result = search("davinci_resolve", "trim clip edit", mode="hybrid", top_k=10)
    assert result["total_found"] >= 1
    top3_text = " ".join(r.get("text", "") for r in result["results"][:3]).lower()
    assert any(kw in top3_text for kw in ["trim", "edit", "clip"])


def test_davinci_color_grading_search():
    """Search for 'color grading primary correction' should find color-related content."""
    from hybrid_search import search

    result = search("davinci_resolve", "color grading primary correction", mode="hybrid", top_k=10)
    assert result["total_found"] >= 1
    top3_text = " ".join(r.get("text", "") for r in result["results"][:3]).lower()
    assert any(kw in top3_text for kw in ["color", "primary", "correction", "grade"])


def test_davinci_render_deliver_search():
    """Search for 'render deliver settings' should find deliver-related content."""
    from hybrid_search import search

    result = search("davinci_resolve", "render deliver settings", mode="hybrid", top_k=10)
    assert result["total_found"] >= 1
    top3_text = " ".join(r.get("text", "") for r in result["results"][:3]).lower()
    assert any(kw in top3_text for kw in ["deliver", "render", "export", "settings"])


def test_davinci_search_returns_pdf_metadata():
    """At least one result should have page_start set (PDF page number)."""
    from hybrid_search import search

    result = search("davinci_resolve", "trim clip", top_k=10)
    has_page = any(r.get("page_start") is not None for r in result["results"])
    assert has_page, "No result had page_start metadata (expected from PDF source)"


def test_davinci_hybrid_under_10_seconds():
    """Hybrid search should complete in under 10 seconds."""
    from hybrid_search import search

    result = search("davinci_resolve", "trim clip edit", mode="hybrid", top_k=10)
    assert result["query_time_ms"] <= 10000


def test_davinci_all_search_modes_work():
    """exact, semantic, and hybrid modes should all return results."""
    from hybrid_search import search

    for mode in ["exact", "semantic", "hybrid"]:
        result = search("davinci_resolve", "color grading", mode=mode, top_k=5)
        assert result["total_found"] >= 1, f"mode={mode} returned no results"


def test_davinci_result_structure():
    """Result dict should have all required keys."""
    from hybrid_search import search

    result = search("davinci_resolve", "fairlight audio", top_k=3)
    assert "results" in result
    assert "total_found" in result
    assert "mode" in result
    assert "query_time_ms" in result