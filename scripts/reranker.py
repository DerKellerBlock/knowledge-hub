#!/usr/bin/env python3
"""
Cross-Encoder reranking for Knowledge Hub (Stage 2 retrieval).

Model: cross-encoder/ms-marco-MiniLM-L-12-v2 (~130 MB).
Loaded lazily via model_manager.get_reranker().
"""

import logging
from pathlib import Path

import sys as _sys
_pkg_root = Path(__file__).resolve().parent.parent
if str(_pkg_root) not in _sys.path:
    _sys.path.insert(0, str(_pkg_root))
from model_manager import get_reranker, is_reranker_available

logger = logging.getLogger(__name__)


def rerank(
    query: str,
    candidates: list[dict],
    top_k: int = 10,
) -> list[dict]:
    """Cross-Encoder re-ranks Stage-1 candidates."""
    if not candidates:
        return []

    model = get_reranker()
    pairs = [(query, c["text"]) for c in candidates]
    scores = model.predict(pairs)

    for c, score in zip(candidates, scores):
        c["rerank_score"] = float(score)
        c["stage1_score"] = c.get("score")
        c["score"] = float(score)

    candidates.sort(key=lambda c: c["score"], reverse=True)
    return candidates[:top_k]
