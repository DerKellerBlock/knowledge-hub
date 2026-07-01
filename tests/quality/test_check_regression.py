"""Unit tests for run_evaluation.check_regression() Spec thresholds (B8/B9).

Phase-2a spec (Decision 2.4):

    1. avg_composite < baseline.avg_composite - 0.1  -> regression
    2. per-question pass -> weak|fail                  -> regression
    3. per-question weak -> fail                       -> regression
    4. weak->weak OK, fail->fail OK, fail->weak OK

These tests construct synthetic current/baseline dicts and call
:func:`run_evaluation.check_regression` directly — no live index, no
file IO. They lock in the Spec semantics so a future refactor cannot
silently loosen the gate.
"""

from __future__ import annotations

import pytest

from scripts.quality.run_evaluation import check_regression


pytestmark = pytest.mark.quality


def _eval(qid: str, label: str, composite: float) -> dict:
    return {
        "id": qid,
        "label": label,
        "composite_score": composite,
        "source_recall": 1.0,
        "page_metadata_accuracy": None,
        "top_k_relevance": 1.0,
        "evidence_quality": 1.0,
    }


def _result(evals, avg_composite):
    return {
        "domain": "godot",
        "date": "2026-06-30",
        "evaluations": evals,
        "summary": {"avg_composite": avg_composite},
    }


# ── (a) avg_composite drop > 0.1 -> fail ──────────────────────────────────


def test_avg_composite_drop_greater_than_0_1_is_regression():
    baseline = _result([_eval("godot-001", "pass", 0.9)], 0.8351)
    current = _result([_eval("godot-001", "pass", 0.9)], 0.7250)  # drop 0.1101
    warnings = check_regression(current, baseline)
    assert any("Domain average composite regression" in w for w in warnings)


def test_avg_composite_drop_exactly_0_1_is_not_regression():
    """A drop of exactly 0.1 is the boundary; spec uses strict ``< - 0.1``."""
    baseline = _result([_eval("godot-001", "pass", 0.9)], 0.8351)
    # 0.8351 - 0.1 = 0.7351 exactly — must NOT warn (strict inequality).
    current = _result([_eval("godot-001", "pass", 0.9)], 0.7351)
    warnings = check_regression(current, baseline)
    assert not any("Domain average composite regression" in w for w in warnings)


# ── (b) pass -> weak -> fail ──────────────────────────────────────────────


def test_pass_to_weak_is_regression():
    baseline = _result([_eval("godot-001", "pass", 0.9)], 0.9)
    current = _result([_eval("godot-001", "weak", 0.6)], 0.6)
    warnings = check_regression(current, baseline)
    assert any("pass -> weak" in w for w in warnings)


def test_pass_to_fail_is_regression():
    baseline = _result([_eval("godot-001", "pass", 0.9)], 0.9)
    current = _result([_eval("godot-001", "fail", 0.1)], 0.1)
    warnings = check_regression(current, baseline)
    assert any("pass -> fail" in w for w in warnings)


# ── (c) weak -> weak OK ────────────────────────────────────────────────────


def test_weak_to_weak_is_not_regression():
    baseline = _result([_eval("godot-001", "weak", 0.6)], 0.6)
    current = _result([_eval("godot-001", "weak", 0.55)], 0.55)
    warnings = check_regression(current, baseline)
    # No avg drop (0.05 < 0.1), no label regression.
    assert warnings == []


# ── (d) no regression OK ──────────────────────────────────────────────────


def test_no_regression_returns_empty():
    baseline = _result([_eval("godot-001", "pass", 0.9)], 0.9)
    current = _result([_eval("godot-001", "pass", 0.95)], 0.95)
    warnings = check_regression(current, baseline)
    assert warnings == []


def test_fail_to_weak_is_improvement_not_regression():
    baseline = _result([_eval("godot-001", "fail", 0.1)], 0.1)
    current = _result([_eval("godot-001", "weak", 0.6)], 0.6)
    warnings = check_regression(current, baseline)
    assert warnings == []


def test_weak_to_fail_is_regression():
    """Spec is silent on weak->fail; we warn for safety (B9)."""
    baseline = _result([_eval("godot-001", "weak", 0.6)], 0.6)
    current = _result([_eval("godot-001", "fail", 0.05)], 0.05)
    warnings = check_regression(current, baseline)
    assert any("weak -> fail" in w for w in warnings)


def test_missing_question_in_current_is_regression():
    baseline = _result([_eval("godot-001", "pass", 0.9)], 0.9)
    current = _result([], 0.0)
    warnings = check_regression(current, baseline)
    assert any("missing in current run" in w for w in warnings)