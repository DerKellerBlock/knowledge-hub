#!/usr/bin/env python3
"""
BM25 sparse retrieval for Knowledge Hub.

Per-Domain isolated BM25 index at chromadb_data/<domain>/<domain>_bm25.pkl.
LRU-cached in memory (max BM25_CACHE_MAX domains held simultaneously).

Usage:
  from bm25_search import build_bm25_index, bm25_search, tokenize
"""

import pickle
import re
from pathlib import Path

import numpy as np
from rank_bm25 import BM25Okapi

import sys as _sys
_pkg_root = Path(__file__).resolve().parent.parent
if str(_pkg_root) not in _sys.path:
    _sys.path.insert(0, str(_pkg_root))
from mcp_servers.knowledge_hub.config import domain_bm25_path
from model_manager import bm25_cache_get, bm25_cache_set, bm25_cache_invalidate


def tokenize(text: str) -> list[str]:
    """Simple tokenizer: lowercase, split on non-alphanumeric."""
    return re.findall(r"\w+", text.lower())


def build_bm25_index(domain: str, chunks: list) -> bool:
    """Build and persist a BM25 index from a list of Chunk objects."""
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
        return False

    bm25 = BM25Okapi(corpus)
    bm25_path = domain_bm25_path(domain)
    bm25_path.parent.mkdir(parents=True, exist_ok=True)
    with open(bm25_path, "wb") as f:
        pickle.dump({"index": bm25, "chunk_ids": chunk_ids}, f)

    bm25_cache_invalidate(domain)
    return True


def _load_index(domain: str) -> dict:
    """Load BM25 index from pickle, with LRU in-memory caching."""
    cached = bm25_cache_get(domain)
    if cached is not None:
        return cached

    index_path = domain_bm25_path(domain)
    if not index_path.exists():
        raise FileNotFoundError(
            f"BM25 index not found for domain '{domain}' at {index_path}. "
            f"Run embed_index.py --domain {domain} first."
        )

    with open(index_path, "rb") as f:
        data = pickle.load(f)

    bm25_cache_set(domain, data)
    return data


def bm25_search(domain: str, query: str, top_k: int = 100) -> list[dict]:
    """BM25 sparse retrieval with field boosting."""
    data = _load_index(domain)
    bm25: BM25Okapi = data["index"]
    chunk_ids: list[str] = data["chunk_ids"]

    tokens = tokenize(query)
    scores = bm25.get_scores(tokens)

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
    index_path = domain_bm25_path(domain)
    if index_path.exists():
        return round(index_path.stat().st_size / 1024 / 1024, 2)
    return 0.0
