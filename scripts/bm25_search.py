#!/usr/bin/env python3
"""
BM25 sparse retrieval for Knowledge Hub.

Usage:
  from bm25_search import build_bm25_index, bm25_search, tokenize

The BM25 index is built during embed_index.py and persisted via pickle to
chromadb_data/<domain>_bm25.pkl. Each query loads the index (cached in memory)
and returns scored chunk_ids.
"""

import pickle
import re
from pathlib import Path

import numpy as np
from rank_bm25 import BM25Okapi

HUB_ROOT = Path(__file__).resolve().parent.parent
CHROMA_DIR = HUB_ROOT / "chromadb_data"

# ── Caching ────────────────────────────────────────────────────────────────
_bm25_cache: dict[str, dict] = {}


def tokenize(text: str) -> list[str]:
    """Simple tokenizer: lowercase, split on non-alphanumeric."""
    return re.findall(r"\w+", text.lower())


def build_bm25_index(domain: str, chunks: list) -> None:
    """Build and persist a BM25 index from a list of Chunk objects.

    Args:
        domain: Domain name (e.g. 'godot')
        chunks: List of Chunk objects (from parser_base)

    Field-boosting: chunk.name (2x), chunk.signature (3x) tokens appended
    to increase their weight in the BM25 index.
    """
    corpus = []
    chunk_ids = []

    for chunk in chunks:
        tokens = tokenize(chunk.text)
        if chunk.name:
            tokens.extend(tokenize(chunk.name) * 2)
        if chunk.signature:
            tokens.extend(tokenize(chunk.signature) * 3)
        corpus.append(tokens)
        chunk_ids.append(chunk.chunk_id)

    if not corpus:
        return

    bm25 = BM25Okapi(corpus)
    index_path = CHROMA_DIR / f"{domain}_bm25.pkl"
    with open(index_path, "wb") as f:
        pickle.dump({"index": bm25, "chunk_ids": chunk_ids}, f)

    # Invalidate cache for this domain
    _bm25_cache.pop(domain, None)


def _load_index(domain: str) -> dict:
    """Load BM25 index from pickle, with in-memory caching."""
    if domain in _bm25_cache:
        return _bm25_cache[domain]

    index_path = CHROMA_DIR / f"{domain}_bm25.pkl"
    if not index_path.exists():
        raise FileNotFoundError(
            f"BM25 index not found for domain '{domain}'. "
            f"Run embed_index.py --domain {domain} first."
        )

    with open(index_path, "rb") as f:
        data = pickle.load(f)

    _bm25_cache[domain] = data
    return data


def bm25_search(domain: str, query: str, top_k: int = 100) -> list[dict]:
    """BM25 sparse retrieval with field boosting.

    Returns:
        [
            {"chunk_id": "godot::Node3D::method::rotate_y",
             "score": 12.45,
             "match_type": "bm25"},
            ...
        ]
    """
    data = _load_index(domain)
    bm25: BM25Okapi = data["index"]
    chunk_ids: list[str] = data["chunk_ids"]

    tokens = tokenize(query)
    scores = bm25.get_scores(tokens)

    # Get top-k indices by score
    if len(scores) == 0:
        return []

    top_indices = np.argsort(scores)[::-1][:top_k]

    return [
        {
            "chunk_id": chunk_ids[i],
            "score": float(scores[i]),
            "match_type": "bm25",
        }
        for i in top_indices
        if scores[i] > 0
    ]


def get_bm25_index_size_mb(domain: str) -> float:
    """Get BM25 index file size in MB."""
    index_path = CHROMA_DIR / f"{domain}_bm25.pkl"
    if index_path.exists():
        return round(index_path.stat().st_size / 1024 / 1024, 2)
    return 0.0
