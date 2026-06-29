"""E2E quality test for the DaVinci Resolve domain.

This test runs the Golden Dataset evaluation against the live DaVinci
Resolve index. It is skipped automatically when the index has not been
built (``chromadb_data/davinci_resolve/chroma`` does not exist).

In addition to the generic "has results" and "not all fail" checks,
this test verifies that page-metadata-aware scoring is producing
non-zero values (since DaVinci Resolve ingests PDFs and should have
``page_start`` metadata in its chunks).

Run: pytest tests/quality/test_davinci_quality.py -v -m quality
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest


HUB_ROOT = Path(__file__).resolve().parent.parent.parent
DAVINCI_INDEX = HUB_ROOT / "chromadb_data" / "davinci_resolve" / "chroma"
GOLDEN = HUB_ROOT / "quality" / "golden" / "davinci_resolve.yaml"

pytestmark = [
    pytest.mark.quality,
    pytest.mark.skipif(
        not DAVINCI_INDEX.exists(),
        reason=(
            "DaVinci Resolve index not built. "
            "Run: python scripts/embed_index.py --domain davinci_resolve"
        ),
    ),
    pytest.mark.skipif(
        not GOLDEN.exists(),
        reason="Golden dataset not created. Run: see quality/golden/ for spec",
    ),
]


def _run_evaluation():
    """Import and call run_evaluation, with proper sys.path setup."""
    sys.path.insert(0, str(HUB_ROOT / "scripts"))
    from quality.run_evaluation import run_evaluation

    return run_evaluation("davinci_resolve")


def test_davinci_quality_has_results():
    """All DaVinci Resolve Golden Dataset questions should return at least one result."""
    result = _run_evaluation()
    evals = result["evaluations"]
    assert len(evals) >= 1, "No evaluations were run"
    for e in evals:
        assert e["total_results"] >= 1, (
            f"{e['id']}: no results returned (composite={e['composite_score']})"
        )


def test_davinci_quality_not_all_fail():
    """At least one question must not be a fail — sanity check on coverage."""
    result = _run_evaluation()
    evals = result["evaluations"]
    assert len(evals) >= 1
    fail_count = sum(1 for e in evals if e["label"] == "fail")
    assert fail_count < len(evals), (
        f"All {len(evals)} questions failed: "
        f"{[(e['id'], e['composite_score']) for e in evals]}"
    )


def test_davinci_quality_page_metadata_present():
    """PDF-derived domain must have non-zero page_metadata_accuracy for at
    least one question. If all PMA values are 0, page metadata is being
    lost somewhere in the index/retrieval pipeline.
    """
    result = _run_evaluation()
    pma_values = [
        e["page_metadata_accuracy"]
        for e in result["evaluations"]
        if e["page_metadata_accuracy"] is not None
    ]
    assert len(pma_values) >= 1, (
        "No evaluations had page_metadata_accuracy (all N/A). "
        "PDF-derived DaVinci Resolve domain should have non-N/A PMA."
    )
    assert any(v > 0 for v in pma_values), (
        f"All PMA values are 0.0: {pma_values}. "
        "Page metadata is being lost in the index/retrieval pipeline."
    )


def test_davinci_quality_evaluations_have_expected_fields():
    """Each evaluation result must contain the standard metric fields."""
    result = _run_evaluation()
    required_fields = {
        "id",
        "question",
        "source_recall",
        "page_metadata_accuracy",
        "top_k_relevance",
        "evidence_quality",
        "composite_score",
        "label",
        "truncation_warnings",
        "found_source_files",
        "total_results",
    }
    for e in result["evaluations"]:
        missing = required_fields - set(e.keys())
        assert not missing, f"{e.get('id', '<no-id>')} missing fields: {missing}"
