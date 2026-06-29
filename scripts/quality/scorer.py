"""Core scoring and dataset loading logic for the Quality Evaluation Platform.

Pure functions — no side effects, no index access, no hybrid_search calls.
Scorer functions take search results as arguments (mockable in tests).
The CLI wrapper ``run_evaluation.py`` is the only module that calls
``hybrid_search.search()`` directly.

Design spec:
    docs/superpowers/specs/2026-06-29-knowledge-hub-quality-evaluation-platform-design.md
"""

from __future__ import annotations

import json
from pathlib import Path
from statistics import mean
from typing import Any

import yaml


# ── Dataset Loader constants ──────────────────────────────────────────────

VALID_DIFFICULTIES = {"easy", "medium", "hard"}
DEFAULT_TOP_K = 10


# ── Scoring constants ────────────────────────────────────────────────────

# Heuristic — `text` is truncated to 5000 chars in hybrid_search (LIM-003).
# False positives possible for naturally 5000-char chunks. Used only to flag
# a warning in the report, not to penalize the score.
TRUNCATION_HEURISTIC_CHARS = 5000

# Default metric weights (sum = 1.00)
W_SR = 0.35
W_PMA = 0.20
W_TKR = 0.25
W_EQ = 0.20

# Thresholds for classify_score
PASS_THRESHOLD = 0.7
WEAK_THRESHOLD = 0.4


# ── Dataset Loader ────────────────────────────────────────────────────────


def load_golden_dataset(path: Path) -> dict[str, Any]:
    """Load and validate a Golden Dataset YAML file.

    Args:
        path: Path to the .yaml file.

    Returns:
        Dict with keys: domain, version, description, last_updated, questions.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the YAML is invalid or required fields are missing.
    """
    if not path.exists():
        raise FileNotFoundError(f"Golden Dataset not found: {path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in {path}: {e}") from e

    if data is None:
        raise ValueError(f"Empty YAML file: {path}")

    if "domain" not in data:
        raise ValueError(f"Missing required field 'domain' in {path}")

    if "questions" not in data:
        data["questions"] = []

    for q in data["questions"]:
        q.setdefault("min_top_k", DEFAULT_TOP_K)
        q.setdefault("expected_page_ranges", [])
        q.setdefault("real_world_source_url", None)
        q.setdefault("real_world_source_date", None)
        q.setdefault("tags", [])
        q.setdefault("notes", None)

    return data


def validate_question(question: dict, domain: str) -> list[str]:
    """Validate a single Golden Dataset question entry.

    Args:
        question: The question dict from the YAML.
        domain: Expected domain name (for ID prefix check).

    Returns:
        List of error strings. Empty list means valid.
    """
    errors = []

    if not question.get("id"):
        errors.append("Missing required field: id")
    else:
        expected_prefix = f"{domain}-"
        if not question["id"].startswith(expected_prefix):
            errors.append(
                f"Question id '{question['id']}' must start with '{expected_prefix}'"
            )

    if not question.get("question"):
        errors.append("Missing required field: question")

    if "expected_source_files" not in question:
        errors.append("Missing required field: expected_source_files")

    if "difficulty" not in question:
        errors.append("Missing required field: difficulty")
    elif question["difficulty"] not in VALID_DIFFICULTIES:
        errors.append(
            f"Invalid difficulty '{question['difficulty']}'. "
            f"Must be one of: {', '.join(sorted(VALID_DIFFICULTIES))}"
        )

    if "created_date" not in question:
        errors.append("Missing required field: created_date")

    if "last_verified" not in question:
        errors.append("Missing required field: last_verified")

    return errors


# ── Scoring Functions ────────────────────────────────────────────────────


def score_source_recall(
    results: list[dict], expected_source_files: list[str]
) -> float | None:
    """Fraction of expected source files found in results.

    Returns:
        - None (N/A) if ``expected_source_files`` is empty (no source
          expectation → no penalty, no division-by-zero).
        - 0.0 if expected sources but no results returned.
        - Otherwise the recall in [0, 1].
    """
    if not expected_source_files:
        return None  # N/A — no source expectation

    if not results:
        return 0.0

    found = {r.get("source_file", "") for r in results if r.get("source_file")}
    expected = set(expected_source_files)
    return round(len(expected & found) / len(expected), 4)


def score_page_metadata_accuracy(
    results: list[dict],
    is_pdf_domain: bool = False,
    expected_ranges: list[dict] | None = None,
) -> float | None:
    """Fraction of results with valid page metadata.

    Returns:
        - None (N/A) for non-PDF domains (no page_start expected) or empty
          results.
        - Otherwise: if ``expected_ranges`` is provided, the fraction of
          results whose ``page_start`` falls inside one of the ranges.
          Otherwise the fraction of results with a non-None ``page_start``.
    """
    if not is_pdf_domain:
        return None  # N/A — no page metadata expected

    if not results:
        return None  # N/A — no results to check

    if expected_ranges:
        in_range_count = 0
        for r in results:
            ps = r.get("page_start")
            if ps is not None:
                for er in expected_ranges:
                    if er["start"] <= ps <= er["end"]:
                        in_range_count += 1
                        break
        return round(in_range_count / len(results), 4)
    else:
        with_page = sum(1 for r in results if r.get("page_start") is not None)
        return round(with_page / len(results), 4)


def score_top_k_relevance(results: list[dict]) -> float:
    """Rank-based normalized relevance score.

    RRF/Cross-Encoder scores from ``hybrid_search`` are not in [0, 1]
    (~0.017), so we normalize by rank position instead. Rank 1 → index 0
    → highest normalized score.

    ``normalized_score_i = 1.0 - (rank_index_i / total_results)``

    Returns 0.0 for empty results.
    """
    if not results:
        return 0.0

    total = len(results)
    normalized = [1.0 - (i / total) for i in range(total)]
    return round(sum(normalized) / total, 4)


def score_evidence_quality(results: list[dict]) -> float | None:
    """Fraction of results with non-empty ``text`` field.

    Returns None (N/A) for empty results (cannot evaluate).
    """
    if not results:
        return None

    with_text = sum(1 for r in results if r.get("text"))
    return round(with_text / len(results), 4)


def compute_composite_score(
    source_recall: float | None,
    page_metadata_accuracy: float | None,
    top_k_relevance: float | None,
    evidence_quality: float | None,
) -> float:
    """Weighted composite score with N/A redistribution.

    When a metric is None (N/A), its weight is redistributed proportionally
    across the remaining metrics. This prevents domains without page
    metadata (e.g. Godot) from being artificially lowered.
    """
    parts = [
        (source_recall, W_SR),
        (page_metadata_accuracy, W_PMA),
        (top_k_relevance, W_TKR),
        (evidence_quality, W_EQ),
    ]
    active = [(v, w) for v, w in parts if v is not None]

    if not active:
        return 0.0

    total_weight = sum(w for _, w in active)
    if total_weight == 0:
        return 0.0

    weighted_sum = sum(v * w for v, w in active)
    return round(weighted_sum / total_weight, 4)


def classify_score(composite: float) -> str:
    """Classify composite as ``pass`` (>=0.7), ``weak`` (0.4-0.7), ``fail`` (<0.4)."""
    if composite >= PASS_THRESHOLD:
        return "pass"
    elif composite >= WEAK_THRESHOLD:
        return "weak"
    else:
        return "fail"


def evaluate_question(
    question: dict,
    results: list[dict],
    is_pdf_domain: bool = False,
) -> dict:
    """Evaluate a single Golden Dataset question against search results.

    Pure function — does not call ``hybrid_search``. Takes results as
    argument so it is fully testable with mock data.

    Returns a dict with the 4 metric scores, the composite, the label,
    truncation warning count, the found source files and the total result
    count.
    """
    expected_sources = question.get("expected_source_files", []) or []
    expected_ranges = question.get("expected_page_ranges") or None

    sr = score_source_recall(results, expected_sources)
    pma = score_page_metadata_accuracy(
        results, is_pdf_domain=is_pdf_domain, expected_ranges=expected_ranges
    )
    tkr = score_top_k_relevance(results)
    eq_ = score_evidence_quality(results)
    composite = compute_composite_score(sr, pma, tkr, eq_)
    label = classify_score(composite)

    # Truncation heuristic (LIM-003) — False positives possible.
    # Score is not reduced; the warning is shown in the report.
    truncation_warnings = sum(
        1 for r in results if len(r.get("text", "")) >= TRUNCATION_HEURISTIC_CHARS
    )

    found_sources = list(
        {r.get("source_file", "") for r in results if r.get("source_file")}
    )

    return {
        "id": question["id"],
        "question": question["question"],
        "source_recall": sr,
        "page_metadata_accuracy": pma,
        "top_k_relevance": tkr,
        "evidence_quality": eq_,
        "composite_score": composite,
        "label": label,
        "truncation_warnings": truncation_warnings,
        "found_source_files": found_sources,
        "total_results": len(results),
    }


# ── Aggregation & Report Generation ──────────────────────────────────────


def aggregate_domain_scores(domain: str, evaluations: list[dict]) -> dict:
    """Aggregate per-question scores into a domain-level summary.

    N/A metric values (None) are skipped when computing per-metric averages.
    """
    total = len(evaluations)
    pass_count = sum(1 for e in evaluations if e.get("label") == "pass")
    weak_count = sum(1 for e in evaluations if e.get("label") == "weak")
    fail_count = sum(1 for e in evaluations if e.get("label") == "fail")

    def avg(key: str) -> float:
        vals = [e[key] for e in evaluations if e.get(key) is not None]
        return round(mean(vals), 4) if vals else 0.0

    avg_composite = (
        round(mean([e["composite_score"] for e in evaluations]), 4)
        if evaluations
        else 0.0
    )

    return {
        "domain": domain,
        "total_questions": total,
        "pass_count": pass_count,
        "weak_count": weak_count,
        "fail_count": fail_count,
        "avg_composite": avg_composite,
        "avg_source_recall": avg("source_recall"),
        "avg_page_metadata_accuracy": avg("page_metadata_accuracy"),
        "avg_top_k_relevance": avg("top_k_relevance"),
        "avg_evidence_quality": avg("evidence_quality"),
    }


def generate_markdown_report(
    domain: str, date_str: str, summary: dict, evaluations: list[dict]
) -> str:
    """Generate a human-readable Markdown quality report."""
    lines: list[str] = []
    lines.append(f"# Quality Report: {domain} — {date_str}")
    lines.append("")
    lines.append("## Summary")
    lines.append(f"- **Domain:** {domain}")
    lines.append(f"- **Date:** {date_str}")
    lines.append(f"- **Questions evaluated:** {summary['total_questions']}")
    lines.append(f"- **Composite Score:** {summary['avg_composite']}")

    def _pct(n: int) -> str:
        if not summary["total_questions"]:
            return "0 (0%)"
        return f"{n} ({round(100 * n / summary['total_questions'], 1)}%)"

    lines.append(
        f"- **Pass:** {_pct(summary['pass_count'])} | "
        f"**Weak:** {_pct(summary['weak_count'])} | "
        f"**Fail:** {_pct(summary['fail_count'])}"
    )
    lines.append("")
    lines.append("## Metric Averages")
    lines.append("| Metric | Average |")
    lines.append("|--------|---------|")
    lines.append(f"| Source Recall | {summary['avg_source_recall']} |")
    lines.append(f"| Page Metadata Accuracy | {summary['avg_page_metadata_accuracy']} |")
    lines.append(f"| Top-K Relevance | {summary['avg_top_k_relevance']} |")
    lines.append(f"| Evidence Quality | {summary['avg_evidence_quality']} |")
    lines.append("")
    lines.append("## Per-Question Results")
    lines.append("| ID | Question | Score | Label | SR | PMA | TKR | EQ |")
    lines.append("|----|----------|-------|-------|----|----|----|----|")
    for e in evaluations:
        q_short = e["question"][:40] + ("..." if len(e["question"]) > 40 else "")
        sr = e["source_recall"] if e["source_recall"] is not None else "N/A"
        pma = (
            e["page_metadata_accuracy"]
            if e["page_metadata_accuracy"] is not None
            else "N/A"
        )
        eq = e["evidence_quality"] if e["evidence_quality"] is not None else "N/A"
        lines.append(
            f"| {e['id']} | {q_short} | {e['composite_score']} | {e['label']} | "
            f"{sr} | {pma} | {e['top_k_relevance']} | {eq} |"
        )
    lines.append("")
    weak_fail = [e for e in evaluations if e["label"] in ("weak", "fail")]
    if weak_fail:
        lines.append("## Weak / Fail Details")
        for e in weak_fail:
            lines.append(f"### {e['id']} ({e['label']}, {e['composite_score']})")
            lines.append(f"- **Question:** {e['question']}")
            lines.append(
                f"- **Found sources:** {e['found_source_files'] or '[none]'}"
            )
            lines.append(
                "- **Recommendation:** Review index coverage for this question."
            )
            lines.append("")
    else:
        lines.append("## Weak / Fail Details")
        lines.append("- No weak or fail questions.")
        lines.append("")
    trunc = [e for e in evaluations if e.get("truncation_warnings", 0) > 0]
    if trunc:
        lines.append("## Truncation Warnings")
        for e in trunc:
            lines.append(
                f"- {e['id']}: {e['truncation_warnings']} result(s) with "
                f"text >= {TRUNCATION_HEURISTIC_CHARS} chars (heuristic, see LIM-003)."
            )
        lines.append("")
    lines.append("## Gaps & Recommendations")
    if weak_fail:
        lines.append(
            f"- {len(weak_fail)} question(s) scored weak/fail. "
            "Review index coverage and source availability."
        )
    else:
        lines.append("- No weak/fail questions. Domain coverage looks healthy.")
    lines.append("")
    return "\n".join(lines)


def generate_json_report(
    domain: str, date_str: str, summary: dict, evaluations: list[dict]
) -> str:
    """Generate a machine-readable JSON quality report.

    N/A metric values are serialized as ``null``.
    """
    report = {
        "domain": domain,
        "date": date_str,
        "summary": summary,
        "evaluations": evaluations,
    }
    return json.dumps(report, indent=2, ensure_ascii=False)
