"""Unit tests for the report generation functions in scorer.py.

Covers aggregate_domain_scores, generate_markdown_report and
generate_json_report. Tests use mock evaluation dicts.
"""

from __future__ import annotations

import json

from quality.scorer import (
    aggregate_domain_scores,
    generate_json_report,
    generate_markdown_report,
)


def _e(id, label, score, sr=None, pma=None, tkr=0.0, eq=None, trunc=0, found=None):
    return {
        "id": id,
        "question": f"Question {id}",
        "source_recall": sr,
        "page_metadata_accuracy": pma,
        "top_k_relevance": tkr,
        "evidence_quality": eq,
        "composite_score": score,
        "label": label,
        "truncation_warnings": trunc,
        "found_source_files": found or [],
        "total_results": 5,
    }


# ── aggregate_domain_scores ───────────────────────────────────────────────


def test_aggregate_counts_labels():
    evals = [
        _e("godot-001", "pass", 0.85),
        _e("godot-002", "pass", 0.75),
        _e("godot-003", "weak", 0.55),
        _e("godot-004", "fail", 0.30),
    ]
    summary = aggregate_domain_scores("godot", evals)
    assert summary["domain"] == "godot"
    assert summary["total_questions"] == 4
    assert summary["pass_count"] == 2
    assert summary["weak_count"] == 1
    assert summary["fail_count"] == 1


def test_aggregate_averages_skip_na():
    """N/A metric values (None) must be skipped in the average, not counted as 0."""
    evals = [
        _e("godot-001", "pass", 0.85, sr=1.0, pma=None, tkr=0.5, eq=1.0),
        _e("godot-002", "pass", 0.75, sr=0.5, pma=None, tkr=0.7, eq=0.5),
    ]
    summary = aggregate_domain_scores("godot", evals)
    # avg SR = (1.0 + 0.5) / 2 = 0.75
    assert summary["avg_source_recall"] == 0.75
    # avg PMA — both None -> no values, default 0.0
    assert summary["avg_page_metadata_accuracy"] == 0.0
    # avg TKR = (0.5 + 0.7) / 2 = 0.6
    assert summary["avg_top_k_relevance"] == 0.6
    # avg EQ = (1.0 + 0.5) / 2 = 0.75
    assert summary["avg_evidence_quality"] == 0.75


def test_aggregate_pma_includes_only_non_na():
    evals = [
        _e("godot-001", "pass", 0.85, pma=1.0),
        _e("godot-002", "pass", 0.75, pma=None),  # N/A for non-PDF
    ]
    summary = aggregate_domain_scores("godot", evals)
    # Only one valid PMA value
    assert summary["avg_page_metadata_accuracy"] == 1.0


def test_aggregate_empty_evaluations():
    summary = aggregate_domain_scores("godot", [])
    assert summary["total_questions"] == 0
    assert summary["pass_count"] == 0
    assert summary["weak_count"] == 0
    assert summary["fail_count"] == 0
    assert summary["avg_composite"] == 0.0


def test_aggregate_all_keys_present():
    summary = aggregate_domain_scores("godot", [_e("godot-001", "pass", 0.8)])
    for k in (
        "domain",
        "total_questions",
        "pass_count",
        "weak_count",
        "fail_count",
        "avg_composite",
        "avg_source_recall",
        "avg_page_metadata_accuracy",
        "avg_top_k_relevance",
        "avg_evidence_quality",
    ):
        assert k in summary, f"Missing key: {k}"


# ── generate_markdown_report ──────────────────────────────────────────────


def test_markdown_report_contains_required_sections():
    evals = [_e("godot-001", "pass", 0.85, sr=1.0, pma=1.0, tkr=0.7, eq=1.0)]
    summary = aggregate_domain_scores("godot", evals)
    md = generate_markdown_report("godot", "2026-06-29", summary, evals)
    assert "# Quality Report: godot — 2026-06-29" in md
    assert "## Summary" in md
    assert "## Metric Averages" in md
    assert "## Per-Question Results" in md
    assert "godot-001" in md


def test_markdown_report_weak_fail_section_present():
    evals = [_e("godot-001", "fail", 0.30, found=["foo.md"])]
    summary = aggregate_domain_scores("godot", evals)
    md = generate_markdown_report("godot", "2026-06-29", summary, evals)
    assert "## Weak / Fail Details" in md
    assert "godot-001" in md
    assert "Review index coverage" in md


def test_markdown_report_no_weak_fail_shows_empty_message():
    evals = [_e("godot-001", "pass", 0.85)]
    summary = aggregate_domain_scores("godot", evals)
    md = generate_markdown_report("godot", "2026-06-29", summary, evals)
    assert "## Weak / Fail Details" in md
    assert "No weak or fail questions" in md


def test_markdown_report_truncation_warnings_section():
    evals = [_e("godot-001", "pass", 0.85, trunc=3)]
    summary = aggregate_domain_scores("godot", evals)
    md = generate_markdown_report("godot", "2026-06-29", summary, evals)
    assert "## Truncation Warnings" in md
    assert "godot-001" in md
    assert "3 result(s)" in md


def test_markdown_report_no_truncation_omits_section():
    evals = [_e("godot-001", "pass", 0.85, trunc=0)]
    summary = aggregate_domain_scores("godot", evals)
    md = generate_markdown_report("godot", "2026-06-29", summary, evals)
    assert "## Truncation Warnings" not in md


def test_markdown_report_gaps_section_health_message():
    evals = [_e("godot-001", "pass", 0.85)]
    summary = aggregate_domain_scores("godot", evals)
    md = generate_markdown_report("godot", "2026-06-29", summary, evals)
    assert "## Gaps & Recommendations" in md
    assert "No weak/fail questions" in md


# ── generate_json_report ──────────────────────────────────────────────────


def test_json_report_is_valid_json():
    evals = [_e("godot-001", "pass", 0.85, sr=1.0)]
    summary = aggregate_domain_scores("godot", evals)
    raw = generate_json_report("godot", "2026-06-29", summary, evals)
    parsed = json.loads(raw)
    assert isinstance(parsed, dict)


def test_json_report_contains_expected_keys():
    evals = [_e("godot-001", "pass", 0.85, sr=1.0)]
    summary = aggregate_domain_scores("godot", evals)
    raw = generate_json_report("godot", "2026-06-29", summary, evals)
    parsed = json.loads(raw)
    assert parsed["domain"] == "godot"
    assert parsed["date"] == "2026-06-29"
    assert "summary" in parsed
    assert "evaluations" in parsed
    assert len(parsed["evaluations"]) == 1


def test_json_report_na_values_serialize_as_null():
    evals = [_e("godot-001", "pass", 0.85, sr=None, pma=None, eq=None)]
    summary = aggregate_domain_scores("godot", evals)
    raw = generate_json_report("godot", "2026-06-29", summary, evals)
    parsed = json.loads(raw)
    eval0 = parsed["evaluations"][0]
    assert eval0["source_recall"] is None
    assert eval0["page_metadata_accuracy"] is None
    assert eval0["evidence_quality"] is None
