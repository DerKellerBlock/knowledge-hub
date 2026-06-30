#!/usr/bin/env python3
"""
Cross-Encoder reranking for Knowledge Hub (Stage 2 retrieval).

Model: configurable via CROSS_ENCODER_MODEL (see config.py). Default
``cross-encoder/ms-marco-MiniLM-L-12-v2`` (~130 MB). Set
``KH_RERANKER_MODEL=jinaai/jina-reranker-v2-base-multilingual`` to use the
multilingual reranker (~1.1 GB, CC-BY-NC-4.0).

Loaded lazily via model_manager.get_reranker().

Note on score scale: ``ms-marco-MiniLM-L-12-v2`` returns raw logits
(typically in the range −10 to +10). ``jina-reranker-v2-base-multilingual``
returns sigmoid scores in the range 0 to 1. We sort descending in both
cases (higher = more relevant). Downstream consumers (RRF fusion, hybrid
search) only use the score as a sort key — there is no threshold on the
absolute score, so the two score scales are drop-in compatible.
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
