"""Unit tests for the rubric scoring functions in scorer.py.

Uses mock search-result dicts — no real index, no hybrid_search call.
Covers Source Recall, Page Metadata Accuracy, Top-K Relevance,
Evidence Quality, Composite (with N/A weight redistribution) and the
full ``evaluate_question`` entry point.
"""

from __future__ import annotations

from quality.scorer import (
    classify_score,
    compute_composite_score,
    evaluate_question,
    score_evidence_quality,
    score_page_metadata_accuracy,
    score_source_recall,
    score_top_k_relevance,
    TRUNCATION_HEURISTIC_CHARS,
)


# ── Helpers ───────────────────────────────────────────────────────────────


def _r(source_file: str = "src.md", text: str = "body", page_start=None, page_end=None):
    return {
        "source_file": source_file,
        "text": text,
        "page_start": page_start,
        "page_end": page_end,
    }


# ── score_source_recall ───────────────────────────────────────────────────


def test_sr_all_expected_found():
    results = [_r("a.md"), _r("b.md"), _r("c.md")]
    assert score_source_recall(results, ["a.md", "b.md"]) == 1.0


def test_sr_partial():
    results = [_r("a.md"), _r("c.md"), _r("d.md")]
    assert score_source_recall(results, ["a.md", "b.md"]) == 0.5


def test_sr_none_found():
    results = [_r("c.md"), _r("d.md")]
    assert score_source_recall(results, ["a.md", "b.md"]) == 0.0


def test_sr_empty_expected_is_na_not_one():
    """Blind-Spot-Fix: empty expected_source_files -> N/A, not 1.0."""
    assert score_source_recall([_r("a.md")], []) is None
    assert score_source_recall([_r("a.md")], None) is None


def test_sr_both_empty_is_na():
    assert score_source_recall([], []) is None


def test_sr_empty_results_with_expected_is_zero():
    assert score_source_recall([], ["a.md"]) == 0.0


# ── score_page_metadata_accuracy ──────────────────────────────────────────


def test_pma_all_pages_present_pdf():
    results = [_r(page_start=1), _r(page_start=2), _r(page_start=3)]
    assert score_page_metadata_accuracy(results, is_pdf_domain=True) == 1.0


def test_pma_some_pages_present_pdf():
    results = [_r(page_start=1), _r(page_start=None), _r(page_start=3)]
    # 2/3 results have page_start
    assert score_page_metadata_accuracy(results, is_pdf_domain=True) == 0.6667


def test_pma_no_pages_pdf():
    results = [_r(page_start=None), _r(page_start=None)]
    assert score_page_metadata_accuracy(results, is_pdf_domain=True) == 0.0


def test_pma_non_pdf_is_na():
    """Blind-Spot-Fix: non-PDF domain -> N/A, not 1.0."""
    results = [_r(page_start=None), _r(page_start=None)]
    assert score_page_metadata_accuracy(results, is_pdf_domain=False) is None


def test_pma_empty_results_is_na():
    assert score_page_metadata_accuracy([], is_pdf_domain=True) is None


def test_pma_with_expected_ranges_in_range():
    results = [_r(page_start=5), _r(page_start=10)]
    ranges = [{"start": 1, "end": 10}, {"start": 20, "end": 30}]
    assert score_page_metadata_accuracy(
        results, is_pdf_domain=True, expected_ranges=ranges
    ) == 1.0


def test_pma_with_expected_ranges_out_of_range():
    results = [_r(page_start=100), _r(page_start=200)]
    ranges = [{"start": 1, "end": 10}]
    assert score_page_metadata_accuracy(
        results, is_pdf_domain=True, expected_ranges=ranges
    ) == 0.0


# ── score_top_k_relevance (rank-based) ───────────────────────────────────


def test_tkr_rank_based_normalization():
    """4 results -> normalized = [1.0, 0.75, 0.5, 0.25], mean = 0.625."""
    results = [_r("a.md"), _r("b.md"), _r("c.md"), _r("d.md")]
    assert score_top_k_relevance(results) == 0.625


def test_tkr_single_result_is_one():
    assert score_top_k_relevance([_r("a.md")]) == 1.0


def test_tkr_empty_results_is_zero():
    assert score_top_k_relevance([]) == 0.0


def test_tkr_two_results():
    # normalized = [1.0, 0.5], mean = 0.75
    assert score_top_k_relevance([_r(), _r()]) == 0.75


# ── score_evidence_quality ────────────────────────────────────────────────


def test_eq_all_have_text():
    results = [_r(text="x"), _r(text="y"), _r(text="z")]
    assert score_evidence_quality(results) == 1.0


def test_eq_some_have_text():
    results = [_r(text="x"), _r(text=""), _r(text="z")]
    # 2/3 have non-empty text
    assert score_evidence_quality(results) == 0.6667


def test_eq_no_text():
    results = [_r(text=""), _r(text="")]
    assert score_evidence_quality(results) == 0.0


def test_eq_empty_results_is_na():
    assert score_evidence_quality([]) is None


# ── compute_composite_score (weight redistribution) ───────────────────────


def test_composite_all_one():
    assert compute_composite_score(1.0, 1.0, 1.0, 1.0) == 1.0


def test_composite_all_zero():
    assert compute_composite_score(0.0, 0.0, 0.0, 0.0) == 0.0


def test_composite_sr_na_redistributes():
    # SR=N/A, rest 1.0 -> (0.20*1 + 0.25*1 + 0.20*1) / 0.65 = 1.0
    assert compute_composite_score(None, 1.0, 1.0, 1.0) == 1.0


def test_composite_pma_na_redistributes():
    # PMA=N/A, rest 1.0 -> (0.35*1 + 0.25*1 + 0.20*1) / 0.80 = 1.0
    assert compute_composite_score(1.0, None, 1.0, 1.0) == 1.0


def test_composite_both_sr_and_pma_na():
    # Both N/A, rest 1.0 -> (0.25*1 + 0.20*1) / 0.45 = 1.0
    assert compute_composite_score(None, None, 1.0, 1.0) == 1.0


def test_composite_sr_pma_na_with_partials():
    """Real-world case: Godot (PMA=N/A) with SR=1.0, TKR=0.625, EQ=1.0.
    Expected: (0.35*1 + 0.25*0.625 + 0.20*1) / 0.80 = 0.70625/0.80 = 0.8828.
    """
    val = compute_composite_score(1.0, None, 0.625, 1.0)
    assert abs(val - 0.8828) < 1e-4


def test_composite_eq_na_redistributes():
    # EQ=N/A, rest 1.0 -> (0.35*1 + 0.20*1 + 0.25*1) / 0.80 = 1.0
    assert compute_composite_score(1.0, 1.0, 1.0, None) == 1.0


def test_composite_all_na_is_zero():
    assert compute_composite_score(None, None, None, None) == 0.0


# ── classify_score ────────────────────────────────────────────────────────


def test_classify_pass_high():
    assert classify_score(0.9) == "pass"
    assert classify_score(0.7) == "pass"


def test_classify_weak_mid():
    assert classify_score(0.5) == "weak"
    assert classify_score(0.4) == "weak"


def test_classify_fail_low():
    assert classify_score(0.3) == "fail"
    assert classify_score(0.0) == "fail"


# ── evaluate_question (integration of all scorers) ───────────────────────


def _q(**overrides):
    base = {
        "id": "godot-001",
        "question": "How do I rotate a Node3D?",
        "expected_source_files": ["godot-docs.md"],
        "difficulty": "easy",
    }
    base.update(overrides)
    return base


def test_evaluate_question_pdf_domain_full_match():
    q = _q()
    results = [
        _r("godot-docs.md", text="rotate_y", page_start=5),
        _r("other.md", text="x", page_start=10),
    ]
    out = evaluate_question(q, results, is_pdf_domain=True)
    assert out["id"] == "godot-001"
    assert out["source_recall"] == 1.0
    assert out["page_metadata_accuracy"] == 1.0
    assert out["top_k_relevance"] == 0.75  # 2 results: [1.0, 0.5] / 2
    assert out["evidence_quality"] == 1.0
    assert out["label"] in ("pass", "weak", "fail")
    assert out["truncation_warnings"] == 0
    assert "godot-docs.md" in out["found_source_files"]


def test_evaluate_question_non_pdf_domain_pma_is_na():
    q = _q()
    results = [_r("godot-docs.md", text="x"), _r("other.md", text="y")]
    out = evaluate_question(q, results, is_pdf_domain=False)
    assert out["page_metadata_accuracy"] is None
    # composite is still defined, just not artificially low
    assert isinstance(out["composite_score"], float)


def test_evaluate_question_empty_expected_sources_sr_is_na():
    q = _q(expected_source_files=[])
    results = [_r("a.md", text="x"), _r("b.md", text="y")]
    out = evaluate_question(q, results, is_pdf_domain=True)
    assert out["source_recall"] is None


def test_evaluate_question_truncation_warning():
    q = _q()
    big_text = "x" * TRUNCATION_HEURISTIC_CHARS
    results = [_r("godot-docs.md", text=big_text)]
    out = evaluate_question(q, results, is_pdf_domain=False)
    assert out["truncation_warnings"] == 1


def test_evaluate_question_no_results():
    q = _q()
    out = evaluate_question(q, [], is_pdf_domain=False)
    assert out["source_recall"] == 0.0
    assert out["page_metadata_accuracy"] is None
    assert out["top_k_relevance"] == 0.0
    assert out["evidence_quality"] is None
    assert out["total_results"] == 0
    assert out["found_source_files"] == []


def test_evaluate_question_returns_all_required_keys():
    q = _q()
    out = evaluate_question(q, [_r("godot-docs.md", text="x")], is_pdf_domain=False)
    for k in (
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
    ):
        assert k in out, f"Missing key: {k}"
