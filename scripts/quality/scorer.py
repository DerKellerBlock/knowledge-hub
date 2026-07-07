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

from quality.config import DEFAULT_WEIGHTS, DEFAULT_THRESHOLDS, load_config


# ── Dataset Loader constants ──────────────────────────────────────────────

VALID_DIFFICULTIES = {"easy", "medium", "hard"}
DEFAULT_TOP_K = 10

# Valid ``type`` values for entries inside ``real_world_sources``.
# Kept as a module-level constant so both ``scorer.py`` and
# ``validate_dataset.py`` import the same source of truth.
VALID_RWS_TYPES = frozenset({
    "official-docs",
    "github-issue",
    "github-pr",
    "forum",
    "reddit",
    "youtube",
    "blog",
    "stack-exchange",
    "other",
})

# Length of the top-snippet preview included in the Markdown report and the
# evaluation result. Keeps the report compact while showing enough context
# to manually judge solution alignment with online sources.
TOP_SNIPPET_CHARS = 200


# ── Scoring constants ────────────────────────────────────────────────────

# Heuristic — `text` is truncated to 5000 chars in hybrid_search (LIM-003).
# False positives possible for naturally 5000-char chunks. Used only to flag
# a warning in the report, not to penalize the score.
TRUNCATION_HEURISTIC_CHARS = 5000

# Default metric weights (sum = 1.00). Kept as module-level constants for
# backwards compatibility — the canonical source of truth is now
# ``quality.config.DEFAULT_WEIGHTS``. Scoring functions prefer an explicit
# ``weights=`` argument, falling back to these constants (which mirror
# ``DEFAULT_WEIGHTS``).
W_SR = DEFAULT_WEIGHTS["source_recall"]
W_PMA = DEFAULT_WEIGHTS["page_metadata_accuracy"]
W_TKR = DEFAULT_WEIGHTS["top_k_relevance"]
W_EQ = DEFAULT_WEIGHTS["evidence_quality"]
W_IP = DEFAULT_WEIGHTS["image_presence"]

# Thresholds for classify_score (fallbacks when no override given).
PASS_THRESHOLD = DEFAULT_THRESHOLDS["pass"]
WEAK_THRESHOLD = DEFAULT_THRESHOLDS["weak"]


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

        # Real-world sources backward-compat normalization.
        # ``real_world_source_url`` (string) is the deprecated legacy field.
        # ``real_world_sources`` (list of dicts) is the new structured field.
        # We only migrate the old field when the new field is *absent*
        # (``is None``), so a deliberate empty list stays empty — see
        # blind-spot #2.
        if q.get("real_world_sources") is None:
            old_url = q.get("real_world_source_url")
            if old_url:
                q["real_world_sources"] = [{
                    "url": old_url,
                    "date": q.get("real_world_source_date"),
                    "type": "other",
                    "solution_summary": None,
                    "has_solution": False,
                }]
            else:
                q["real_world_sources"] = []
        q.setdefault("real_world_sources", [])

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


def score_image_presence(
    results: list[dict], question: dict | None = None
) -> float | None:
    """Vision Retrieval Feature: image/caption presence in top-k results.

    Returns the fraction of results with ``modality`` in
    ``{"image", "caption"}``. Returns ``None`` (N/A) when:

    - Results are empty
    - No results have a non-text modality (domain without Vision Retrieval)
    - The question is NOT an image-related question (no ``screenshot`` or
      ``image`` tag). This prevents text questions (e.g. "How do I set up
      a Planar Tracker?") from being penalised by irrelevant image
      results that the 1/3 interleave budget injects into every query.

    A score of 0.0 means "no image results in top-k" (valid score, not
    N/A). A score of 0.3 means "30% of top-k are image/caption results".

    The 1/3 interleave budget in ``hybrid_search.py`` targets ~0.33
    for image-centric queries on image-enabled domains.
    """
    if not results:
        return None

    # Only score image-related questions (tagged with 'screenshot' or 'image')
    if question is not None:
        tags = question.get("tags", []) or []
        if not any(t in ("screenshot", "image") for t in tags):
            return None

    modalities = [r.get("modality", "text") for r in results]
    if not any(m in ("image", "caption") for m in modalities):
        return None
    image_count = sum(1 for m in modalities if m in ("image", "caption"))
    return round(image_count / len(results), 4)


def compute_composite_score(
    source_recall: float | None,
    page_metadata_accuracy: float | None,
    top_k_relevance: float | None,
    evidence_quality: float | None,
    image_presence: float | None = None,
    weights: dict[str, float] | None = None,
) -> float:
    """Weighted composite score with N/A redistribution.

    When a metric is None (N/A), its weight is redistributed proportionally
    across the remaining metrics. This prevents domains without page
    metadata (e.g. Godot) from being artificially lowered.

    Args:
        weights: Optional override mapping (e.g.
            ``{"source_recall": 0.35, "page_metadata_accuracy": 0.20, ...}``).
            ``None`` falls back to :data:`quality.config.DEFAULT_WEIGHTS`.
            Unknown keys are ignored; missing keys fall back to defaults.
    """
    w = {**DEFAULT_WEIGHTS, **(weights or {})}
    parts = [
        (source_recall, w["source_recall"]),
        (page_metadata_accuracy, w["page_metadata_accuracy"]),
        (top_k_relevance, w["top_k_relevance"]),
        (evidence_quality, w["evidence_quality"]),
        (image_presence, w.get("image_presence", 0.0)),
    ]
    active = [(v, wt) for v, wt in parts if v is not None]

    if not active:
        return 0.0

    total_weight = sum(wt for _, wt in active)
    if total_weight == 0:
        return 0.0

    weighted_sum = sum(v * wt for v, wt in active)
    return round(weighted_sum / total_weight, 4)


def classify_score(
    composite: float, thresholds: dict[str, float] | None = None
) -> str:
    """Classify composite as ``pass``, ``weak`` or ``fail``.

    Args:
        composite: The composite score in [0, 1].
        thresholds: Optional override mapping with ``"pass"`` and ``"weak"``
            keys. ``None`` falls back to
            :data:`quality.config.DEFAULT_THRESHOLDS`. ``composite >= pass``
            is ``pass``; ``composite >= weak`` is ``weak``; otherwise
            ``fail``.
    """
    t = {**DEFAULT_THRESHOLDS, **(thresholds or {})}
    if composite >= t["pass"]:
        return "pass"
    elif composite >= t["weak"]:
        return "weak"
    else:
        return "fail"


def evaluate_question(
    question: dict,
    results: list[dict],
    is_pdf_domain: bool = False,
    config: dict[str, Any] | None = None,
) -> dict:
    """Evaluate a single Golden Dataset question against search results.

    Pure function — does not call ``hybrid_search``. Takes results as
    argument so it is fully testable with mock data.

    Args:
        question: The Golden Dataset question entry.
        results: List of search-result dicts.
        is_pdf_domain: Whether the domain uses PDF sources (enables page
            metadata scoring).
        config: Optional override for ``weights`` and ``thresholds``
            (see :func:`quality.config.load_config`). ``None`` falls back
            to :func:`quality.config.load_config` defaults.

    Returns a dict with the 4 metric scores, the composite, the label,
    truncation warning count, the found source files, the total result
    count, the question's ``real_world_sources`` list, and a preview of
    the top-3 snippets (``top_snippets``, each up to ``TOP_SNIPPET_CHARS``
    characters).
    """
    cfg = config if config is not None else load_config()
    weights = cfg.get("weights")
    thresholds = cfg.get("thresholds")

    expected_sources = question.get("expected_source_files", []) or []
    expected_ranges = question.get("expected_page_ranges") or None

    sr = score_source_recall(results, expected_sources)
    pma = score_page_metadata_accuracy(
        results, is_pdf_domain=is_pdf_domain, expected_ranges=expected_ranges
    )
    tkr = score_top_k_relevance(results)
    eq_ = score_evidence_quality(results)
    ip = score_image_presence(results, question=question)
    composite = compute_composite_score(sr, pma, tkr, eq_, ip, weights=weights)
    label = classify_score(composite, thresholds=thresholds)

    # Truncation heuristic (LIM-003) — False positives possible.
    # Score is not reduced; the warning is shown in the report.
    # ``text`` may be ``None`` (not just missing) so we coerce via ``or``.
    truncation_warnings = sum(
        1
        for r in results
        if len(r.get("text") or "") >= TRUNCATION_HEURISTIC_CHARS
    )

    found_sources = list(
        {r.get("source_file", "") for r in results if r.get("source_file")}
    )

    # Real-world sources — pass through verbatim for the report's
    # "Real-World Source Comparison" section. Defaults to ``[]`` if the
    # loader did not run yet (defensive — pure unit tests on
    # ``evaluate_question`` may construct questions without the loader).
    real_world_sources = question.get("real_world_sources") or []

    # Top-3 snippets — first ``TOP_SNIPPET_CHARS`` chars of each top
    # result's ``text``. Used for manual "solution alignment" review
    # against the online sources. Empty/None text becomes ``""``.
    top_snippets = [
        (r.get("text") or "")[:TOP_SNIPPET_CHARS] for r in results[:3]
    ]

    return {
        "id": question["id"],
        "question": question["question"],
        "source_recall": sr,
        "page_metadata_accuracy": pma,
        "top_k_relevance": tkr,
        "evidence_quality": eq_,
        "image_presence": ip,
        "composite_score": composite,
        "label": label,
        "truncation_warnings": truncation_warnings,
        "found_source_files": found_sources,
        "total_results": len(results),
        "real_world_sources": real_world_sources,
        "top_snippets": top_snippets,
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
        "avg_image_presence": avg("image_presence"),
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
    ip = summary.get('avg_image_presence')
    if ip is not None:
        lines.append(f"| Image Presence | {ip} |")
    lines.append("")
    lines.append("## Per-Question Results")
    has_ip = any(e.get("image_presence") is not None for e in evaluations)
    if has_ip:
        lines.append("| ID | Question | Score | Label | SR | PMA | TKR | EQ | IP |")
        lines.append("|----|----------|-------|-------|----|----|----|----|----|")
    else:
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
        ip_val = e.get("image_presence")
        ip_str = ip_val if ip_val is not None else "N/A"
        if has_ip:
            lines.append(
                f"| {e['id']} | {q_short} | {e['composite_score']} | {e['label']} | "
                f"{sr} | {pma} | {e['top_k_relevance']} | {eq} | {ip_str} |"
            )
        else:
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

    # Real-world source comparison — only show the section if at least one
    # evaluation has a non-empty ``real_world_sources`` list. Otherwise
    # we skip the section entirely so domains without curated online
    # sources stay clean.
    rws_evals = [e for e in evaluations if e.get("real_world_sources")]
    if rws_evals:
        lines.append("## Real-World Source Comparison")
        lines.append("")
        lines.append(
            "Online source coverage and Hub top-3 snippets for manual "
            "solution-alignment review."
        )
        lines.append("")
        for e in rws_evals:
            lines.append(f"### {e['id']}: {e['question']}")
            lines.append("")
            lines.append("**Online Sources:**")
            lines.append("")
            lines.append("| URL | Type | Has Solution | Date |")
            lines.append("|-----|------|--------------|------|")
            for rws in e["real_world_sources"]:
                url = rws.get("url", "")
                rws_type = rws.get("type", "other")
                has_sol = "yes" if rws.get("has_solution") else "no"
                date_val = rws.get("date") or "—"
                # Truncate long URLs in the table cell to keep it readable
                url_display = url if len(url) <= 80 else url[:77] + "…"
                lines.append(
                    f"| {url_display} | {rws_type} | {has_sol} | {date_val} |"
                )
            lines.append("")
            lines.append("**Hub Top Snippets:**")
            lines.append("")
            top_snippets = e.get("top_snippets") or []
            if top_snippets:
                for i, snippet in enumerate(top_snippets, 1):
                    # Replace newlines with spaces so the table-style
                    # bullets render as one logical line each.
                    flat = snippet.replace("\n", " ").strip()
                    if not flat:
                        flat = "[empty]"
                    lines.append(f"{i}. {flat}")
            else:
                lines.append("- [no results returned]")
            lines.append("")
            lines.append("**Manual Evaluation:**")
            lines.append("")
            # GFM checkboxes (blind-spot #9) — render in Markdown issue
            # trackers such as GitHub. Plain `- [ ]` (with space) is the
            # canonical GFM form, not the bullet-with-tick we had before.
            lines.append("- [ ] Source Coverage: Hub findet thematisch passende Quellen?")
            lines.append("- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?")
            lines.append("- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?")
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
