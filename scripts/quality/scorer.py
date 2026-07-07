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
import math as _math
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


def score_ndcg(
    results: list[dict],
    question: dict | None = None,
    expected_source_files: list[str] | None = None,
    expected_page_ranges: list[dict] | None = None,
    query_tokens: set[str] | None = None,
) -> float | None:
    """NDCG@10 — Normalized Discounted Cumulative Gain with 4-level relevance.

    Replaces the constant ``score_top_k_relevance`` (which always returns
    ~0.55 for 10 results) with a discriminative rank-aware metric.

    Relevance levels (heuristic, no manual judgment needed):
        3 = chunk is from an expected_source_file AND page_start is in
            an expected_page_range (±2 tolerance for chunking variance)
        2 = chunk is from an expected_source_file (without page match)
        1 = chunk text has keyword overlap with the query (BM25 tokens)
        0 = no match at all

    Formula:
        DCG@K  = Σ(i=1..K) (2^rel_i - 1) / log2(i + 1)
        IDCG@K = DCG of ideal ranking (descending by rel)
        NDCG@K = DCG@K / IDCG@K  (0.0 if IDCG=0, i.e. no relevant results)

    Args:
        results: Search results (must have ``rank`` or be in rank order).
        question: Optional Golden Dataset question (for extracting
            expected sources/ranges if not passed explicitly).
        expected_source_files: Override for expected sources.
        expected_page_ranges: Override for expected page ranges.
        query_tokens: Optional set of query keywords for rel=1 heuristic.
            If None, rel=1 is skipped (only rel=0/2/3 used).

    Returns:
        NDCG@10 in [0, 1], or None (N/A) for empty results.
    """
    if not results:
        return None

    # Extract expected sources/ranges from question if not explicit
    if expected_source_files is None and question:
        expected_source_files = question.get("expected_source_files", []) or []
    if expected_page_ranges is None and question:
        expected_page_ranges = question.get("expected_page_ranges") or []
    if query_tokens is None:
        # Simple keyword extraction from question text
        q_text = (question.get("question", "") if question else "").lower()
        # Use same CamelCase + Unicode tokenization as BM25 (simplified)
        import re as _re
        tokens = _re.findall(r'[a-z0-9]+', q_text)
        # Filter very short tokens
        query_tokens = {t for t in tokens if len(t) >= 3}

    expected_sources_set = set(expected_source_files or [])
    expected_ranges = expected_page_ranges or []

    def _relevance(result: dict) -> int:
        """Determine 4-level relevance for a single result."""
        sf = result.get("source_file", "")
        ps = result.get("page_start")

        # rel=3: source match + page match
        if sf in expected_sources_set and ps is not None and expected_ranges:
            for er in expected_ranges:
                if er["start"] - 2 <= ps <= er["end"] + 2:
                    return 3
            # Source match but no page match → rel=2
            return 2

        # rel=2: source match without page
        if sf in expected_sources_set:
            return 2

        # rel=1: keyword overlap
        if query_tokens:
            text = (result.get("text", "") or "").lower()
            result_tokens = set(_re.findall(r'[a-z0-9]+', text))
            overlap = query_tokens & result_tokens
            if len(overlap) >= 2:  # at least 2 query keywords in text
                return 1

        # rel=0: no match
        return 0

    # Compute relevance for top-10
    top_k = results[:10]
    rels = [_relevance(r) for r in top_k]

    # DCG
    dcg = sum(
        (2 ** rel - 1) / _math.log2(i + 2)  # i+2 because log2(1+1)=1 for i=0
        for i, rel in enumerate(rels)
    )

    # IDCG (ideal: sort descending by rel)
    ideal_rels = sorted(rels, reverse=True)
    idcg = sum(
        (2 ** rel - 1) / _math.log2(i + 2)
        for i, rel in enumerate(ideal_rels)
    )

    if idcg == 0:
        # No relevant results at all → NDCG=0 (not None — it's a valid 0)
        return 0.0

    return round(dcg / idcg, 4)


def score_jaccard_page_overlap(
    results: list[dict],
    is_pdf_domain: bool = False,
    expected_ranges: list[dict] | None = None,
) -> float | None:
    """Jaccard Page Overlap — naturally continuous page accuracy metric.

    Replaces ``score_page_metadata_accuracy`` which used a rigid ±2
    tolerance (binary in/out per range). Jaccard is naturally continuous
    and handles Late Chunking variance better.

    For each result with page_start/page_end, computes the Jaccard index
    against each expected_page_range and takes the maximum. The overall
    score is the average of per-result best-Jaccard values.

    Formula (per result):
        expected_pages = {start, start+1, ..., end}  (from expected range)
        actual_pages   = {page_start, ..., page_end}
        Jaccard = |expected ∩ actual| / |expected ∪ actual|

    Args:
        results: Search results with optional page_start/page_end.
        is_pdf_domain: Whether the domain uses PDF sources.
        expected_ranges: List of ``{"start": N, "end": M}`` dicts.

    Returns:
        Average best-Jaccard in [0, 1], or None (N/A) for non-PDF domains
        or empty results or no expected_ranges.
    """
    if not is_pdf_domain or not results or not expected_ranges:
        return None

    jaccards = []
    for r in results:
        ps = r.get("page_start")
        pe = r.get("page_end")
        if ps is None or pe is None:
            jaccards.append(0.0)
            continue

        actual_pages = set(range(int(ps), int(pe) + 1))
        best_j = 0.0

        for er in expected_ranges:
            exp_pages = set(range(er["start"], er["end"] + 1))
            union = actual_pages | exp_pages
            if not union:
                continue
            intersection = actual_pages & exp_pages
            j = len(intersection) / len(union)
            best_j = max(best_j, j)

        jaccards.append(best_j)

    if not jaccards:
        return None
    return round(sum(jaccards) / len(jaccards), 4)


def score_weighted_source_recall(
    results: list[dict],
    expected_source_files: list,
) -> float | None:
    """Weighted Source Recall — continuous, with optional per-source weights.

    Replaces ``score_source_recall`` which was binary (found/not-found).
    Supports optional ``weight`` per source via dict entries in the
    Golden Dataset:

    .. code-block:: yaml

        expected_source_files:
          - file: "reference-manual.md"
            weight: 2.0
          - file: "colorist-guide.md"
            weight: 1.0

    Backward-compatible: plain string entries get default weight 1.0,
    producing identical results to the old ``score_source_recall``.

    Formula:
        WSR = Σ(w_s × found_s) / Σ(w_s)  for s ∈ expected_sources

    Args:
        results: Search results with ``source_file`` field.
        expected_source_files: List of filenames (str) or dicts with
            ``file`` and optional ``weight`` keys.

    Returns:
        Weighted recall in [0, 1], or None (N/A) if no expected sources.
    """
    if not expected_source_files:
        return None

    if not results:
        return 0.0

    found_sources = {r.get("source_file", "") for r in results if r.get("source_file")}

    # Parse expected sources with weights
    total_weight = 0.0
    found_weight = 0.0
    for entry in expected_source_files:
        if isinstance(entry, dict):
            fname = entry.get("file", "")
            weight = entry.get("weight", 1.0)
        else:
            fname = str(entry)
            weight = 1.0
        total_weight += weight
        if fname in found_sources:
            found_weight += weight

    if total_weight == 0:
        return None
    return round(found_weight / total_weight, 4)


def score_source_diversity(results: list[dict]) -> float | None:
    """Source Diversity — normalized Shannon entropy of source distribution.

    Measures how well the top-k results spread across multiple source
    files. A single-source result set gets 0.0; an evenly spread multi-
    source set gets ~1.0.

    Formula:
        p_i = count(source_i) / total_results
        Diversity = -Σ(p_i × log2(p_i)) / log2(num_unique_sources)

    The normalization by ``log2(num_unique_sources)`` ensures the score
    is in [0, 1] regardless of how many sources are in the top-k.

    Returns None (N/A) for empty results or results without source_file.
    """
    if not results:
        return None

    # Count sources
    source_counts: dict[str, int] = {}
    for r in results:
        sf = r.get("source_file", "")
        if sf:
            source_counts[sf] = source_counts.get(sf, 0) + 1

    if not source_counts:
        return None

    total = sum(source_counts.values())
    num_unique = len(source_counts)

    if num_unique == 1:
        return 0.0  # All from one source → zero diversity

    # Shannon entropy
    entropy = 0.0
    for count in source_counts.values():
        p = count / total
        if p > 0:
            entropy -= p * _math.log2(p)

    # Normalize by max possible entropy (log2(num_unique))
    max_entropy = _math.log2(num_unique)
    return round(entropy / max_entropy, 4)


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
    source_diversity: float | None = None,
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
        (source_diversity, w.get("source_diversity", 0.0)),
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

    # Quality Metrics v2: use new discriminative metrics when available.
    # Fall back to legacy metrics for backward-compat (tests may pass
    # plain-string expected_source_files without weight dicts).
    sr = score_weighted_source_recall(results, expected_sources)
    pma = score_jaccard_page_overlap(
        results, is_pdf_domain=is_pdf_domain, expected_ranges=expected_ranges
    )
    tkr = score_ndcg(
        results, question=question,
        expected_source_files=expected_sources,
        expected_page_ranges=expected_ranges,
    )
    eq_ = score_evidence_quality(results)
    ip = score_image_presence(results, question=question)
    div = score_source_diversity(results)
    composite = compute_composite_score(sr, pma, tkr, eq_, ip, div, weights=weights)
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
        "source_diversity": div,
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
        "avg_source_diversity": avg("source_diversity"),
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
    if ip is not None and ip > 0:
        lines.append(f"| Image Presence | {ip} |")
    div = summary.get('avg_source_diversity')
    if div is not None and div > 0:
        lines.append(f"| Source Diversity | {div} |")
    lines.append("")
    lines.append("## Per-Question Results")
    has_ip = any(e.get("image_presence") is not None for e in evaluations)
    has_div = any(e.get("source_diversity") is not None for e in evaluations)
    if has_ip and has_div:
        lines.append("| ID | Question | Score | Label | SR | PMA | NDCG | EQ | IP | Div |")
        lines.append("|----|----------|-------|-------|----|----|------|----|----|-----|")
    elif has_ip:
        lines.append("| ID | Question | Score | Label | SR | PMA | NDCG | EQ | IP |")
        lines.append("|----|----------|-------|-------|----|----|------|----|----|")
    else:
        lines.append("| ID | Question | Score | Label | SR | PMA | NDCG | EQ |")
        lines.append("|----|----------|-------|-------|----|----|------|----|")
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
        div_val = e.get("source_diversity")
        div_str = div_val if div_val is not None else "N/A"
        tkr = e["top_k_relevance"] if e["top_k_relevance"] is not None else "N/A"
        if has_ip and has_div:
            lines.append(
                f"| {e['id']} | {q_short} | {e['composite_score']} | {e['label']} | "
                f"{sr} | {pma} | {tkr} | {eq} | {ip_str} | {div_str} |"
            )
        elif has_ip:
            lines.append(
                f"| {e['id']} | {q_short} | {e['composite_score']} | {e['label']} | "
                f"{sr} | {pma} | {tkr} | {eq} | {ip_str} |"
            )
        else:
            lines.append(
                f"| {e['id']} | {q_short} | {e['composite_score']} | {e['label']} | "
                f"{sr} | {pma} | {tkr} | {eq} |"
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
