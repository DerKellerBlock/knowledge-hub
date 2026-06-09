#!/usr/bin/env python3
"""
Cross-Encoder reranking for Knowledge Hub (Stage 2 retrieval).

Model: cross-encoder/ms-marco-MiniLM-L-12-v2 (~130 MB, auto-downloaded by
sentence-transformers on first use).

Usage:
  from reranker import rerank, is_reranker_available
"""

import logging
from sentence_transformers import CrossEncoder

logger = logging.getLogger(__name__)

CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L-12-v2"

# ── Singleton ──────────────────────────────────────────────────────────────
_model: CrossEncoder | None = None
_load_error: str | None = None


def get_reranker() -> CrossEncoder:
    """Load or return cached CrossEncoder model."""
    global _model, _load_error
    if _model is None and _load_error is None:
        try:
            _model = CrossEncoder(CROSS_ENCODER_MODEL)
        except Exception as e:
            _load_error = str(e)
            raise
    if _load_error:
        raise RuntimeError(f"Cross-encoder unavailable: {_load_error}")
    return _model


def is_reranker_available() -> bool:
    """Check if cross-encoder loaded successfully. Does NOT trigger download."""
    global _load_error
    if _model is not None:
        return True
    if _load_error is not None:
        return False
    try:
        get_reranker()
        return True
    except Exception:
        return False


def rerank(
    query: str,
    candidates: list[dict],
    top_k: int = 10,
) -> list[dict]:
    """Cross-Encoder re-ranks Stage-1 candidates.

    Each candidate dict must have a "text" key (the chunk text).
    Adds "rerank_score" and "stage1_score" fields, updates "score" to
    the cross-encoder score.

    Args:
        query: The search query string.
        candidates: List of candidate dicts with "text" and "score" keys.
        top_k: Number of results to return.

    Returns:
        Re-ranked and truncated list of candidates.
    """
    if not candidates:
        return []

    model = get_reranker()
    pairs = [(query, c["text"]) for c in candidates]
    scores = model.predict(pairs)
    # scores is numpy array or list[float]; higher = more relevant

    for c, score in zip(candidates, scores):
        c["rerank_score"] = float(score)
        c["stage1_score"] = c.get("score")
        c["score"] = float(score)

    candidates.sort(key=lambda c: c["score"], reverse=True)
    return candidates[:top_k]
