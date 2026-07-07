"""Quality Evaluation Platform configuration.

Default weights and thresholds for the scoring rubric. Can be overridden
per-domain via the Golden Dataset YAML header (``weights`` and
``thresholds`` sections under the top-level keys). Overrides are merged
on top of these defaults by :func:`load_config`.

Design spec:
    docs/superpowers/specs/2026-06-29-knowledge-hub-quality-evaluation-platform-design.md
"""

from __future__ import annotations

from typing import Any


# ── Defaults ───────────────────────────────────────────────────────────────

# Metric weights (sum = 1.00). Used by ``compute_composite_score`` when no
# override is provided. Keys map directly to the four metric names so that
# a Golden Dataset can override individual metrics without redefining
# every weight.
DEFAULT_WEIGHTS: dict[str, float] = {
    # Quality Metrics v2 (2026-07-07): discriminative metrics replace
    # constant TKR (was always 0.55) and near-constant EQ (was always 1.0).
    # New: source_diversity (Shannon entropy) rewards multi-source spread.
    # 70% of weight is now on discriminative metrics (was 60%).
    "source_recall": 0.30,          # Weighted Source Recall (continuous)
    "page_metadata_accuracy": 0.15, # Jaccard Page Overlap (continuous)
    "top_k_relevance": 0.20,        # NDCG@10 (4-level relevance)
    "evidence_quality": 0.10,       # EQ (reduced from 0.20 — near-constant)
    "image_presence": 0.0,          # Vision Retrieval (default off)
    "source_diversity": 0.05,       # NEW: Shannon entropy of source spread
}

# Composite-score classification thresholds. ``composite >= pass`` is
# classified as ``pass``; ``composite >= weak`` as ``weak``; otherwise
# ``fail``. Both are also overridable per-domain.
DEFAULT_THRESHOLDS: dict[str, float] = {
    "pass": 0.7,
    "weak": 0.4,
}


# ── Loader ────────────────────────────────────────────────────────────────


def load_config(dataset: dict[str, Any] | None = None) -> dict[str, Any]:
    """Load quality config, optionally overriding defaults from a Golden Dataset.

    Args:
        dataset: The loaded Golden Dataset dict (may contain ``weights``
            and ``thresholds`` keys at its top level). ``None`` means
            "use defaults only".

    Returns:
        ``{"weights": {...}, "thresholds": {...}}`` with defaults merged
        over any overrides found in the dataset. Non-dict overrides or
        non-numeric values are silently ignored — invalid YAML should not
        crash the evaluation pipeline.
    """
    weights = dict(DEFAULT_WEIGHTS)
    thresholds = dict(DEFAULT_THRESHOLDS)

    if dataset:
        ds_weights = dataset.get("weights")
        if isinstance(ds_weights, dict):
            for k, v in ds_weights.items():
                if isinstance(v, (int, float)) and not isinstance(v, bool):
                    weights[k] = float(v)

        ds_thresholds = dataset.get("thresholds")
        if isinstance(ds_thresholds, dict):
            for k, v in ds_thresholds.items():
                if isinstance(v, (int, float)) and not isinstance(v, bool):
                    thresholds[k] = float(v)

    return {"weights": weights, "thresholds": thresholds}