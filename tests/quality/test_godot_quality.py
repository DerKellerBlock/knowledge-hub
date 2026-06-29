"""E2E quality test for the Godot domain.

This test runs the Golden Dataset evaluation against the live Godot
index. It is skipped automatically when the index has not been built
(``chromadb_data/godot/chroma`` does not exist).

Run: pytest tests/quality/test_godot_quality.py -v -m quality
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest


HUB_ROOT = Path(__file__).resolve().parent.parent.parent
GODOT_INDEX = HUB_ROOT / "chromadb_data" / "godot" / "chroma"
GOLDEN = HUB_ROOT / "quality" / "golden" / "godot.yaml"

pytestmark = [
    pytest.mark.quality,
    pytest.mark.skipif(
        not GODOT_INDEX.exists(),
        reason="Godot index not built. Run: python scripts/embed_index.py --domain godot",
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

    return run_evaluation("godot")


def test_godot_quality_has_results():
    """All Godot Golden Dataset questions should return at least one result."""
    result = _run_evaluation()
    evals = result["evaluations"]
    assert len(evals) >= 1, "No evaluations were run"
    for e in evals:
        assert e["total_results"] >= 1, (
            f"{e['id']}: no results returned (composite={e['composite_score']})"
        )


def test_godot_quality_not_all_fail():
    """At least one question must not be a fail — sanity check on coverage."""
    result = _run_evaluation()
    evals = result["evaluations"]
    assert len(evals) >= 1
    fail_count = sum(1 for e in evals if e["label"] == "fail")
    assert fail_count < len(evals), (
        f"All {len(evals)} questions failed: "
        f"{[(e['id'], e['composite_score']) for e in evals]}"
    )


def test_godot_quality_evaluations_have_expected_fields():
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
