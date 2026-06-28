#!/usr/bin/env python3
"""
Central model cache for Knowledge Hub.

Lazy-loads embedding models and cross-encoders, caches them per model_name.
Provides per-domain ChromaDB PersistentClient cache with LRU eviction.
Provides unload_domain() for explicit resource cleanup.

License: MIT (no PyMuPDF imports here).
"""

import gc
import json
import logging
import re
from collections import OrderedDict
from pathlib import Path

import chromadb
from chromadb.config import Settings
from sentence_transformers import CrossEncoder, SentenceTransformer

# Silence ChromaDB telemetry warnings. chromadb 1.5.x ships with an
# incompatible posthog client signature (capture() arity mismatch), which
# produces a noisy "Failed to send telemetry event" ERROR log on every
# operation. The telemetry is non-essential and anonymized_telemetry=False
# does not suppress these logs because the failure happens before the
# telemetry-disabled guard is consulted. This filter drops messages from
# the posthog telemetry logger specifically.
class _ChromaTelemetryFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return "Failed to send telemetry event" not in record.getMessage()


logging.getLogger("chromadb.telemetry.product.posthog").addFilter(
    _ChromaTelemetryFilter()
)

# Import config (add scripts/ + mcp_servers/knowledge_hub/ to path for standalone use)
import sys as _sys
_pkg_root = Path(__file__).resolve().parent.parent
_mcp_config = _pkg_root / "mcp_servers" / "knowledge_hub"
if str(_pkg_root) not in _sys.path:
    _sys.path.insert(0, str(_pkg_root))
if str(_mcp_config) not in _sys.path:
    _sys.path.insert(0, str(_mcp_config))

from config import (
    CHROMA_DIR,
    domain_chroma_path,
    domain_bm25_path,
    DEFAULT_MODEL_NAME,
    CROSS_ENCODER_MODEL,
    CHROMA_MEMORY_LIMIT_BYTES,
    BM25_CACHE_MAX,
)

# ── Model cache ────────────────────────────────────────────────────────────
_model_cache: dict[str, object] = {}
_chroma_clients: dict[str, chromadb.PersistentClient] = {}
_bm25_cache: OrderedDict[str, dict] = OrderedDict()

# ── Domain config reader (parses Metadaten block in domain.md) ───────────
_DOMAIN_META_RE = re.compile(
    r"## Metadaten\s*\n(.*?)(?=\n## |\Z)",
    re.DOTALL,
)
_EMBEDDING_MODEL_RE = re.compile(
    r"- Embedding-Model:\s*(.+?)(?:\s*\(.*\))?\s*$",
    re.MULTILINE,
)


def get_domain_config(domain: str) -> dict:
    """Read domain.md Metadaten block and return a config dict.

    Returns:
        {
            "embedding_model": "all-mpnet-base-v2",
            "collection": "<domain>_knowledge",
            "chroma_path": Path,
            "bm25_path": Path,
        }
    """
    domain_md = Path(__file__).resolve().parent.parent / "domains" / domain / "domain.md"
    if not domain_md.exists():
        # Fallback to defaults
        return {
            "embedding_model": DEFAULT_MODEL_NAME,
            "collection": f"{domain}_knowledge",
            "chroma_path": domain_chroma_path(domain),
            "bm25_path": domain_bm25_path(domain),
        }

    text = domain_md.read_text(encoding="utf-8")
    meta_block = _DOMAIN_META_RE.search(text)
    model_name = DEFAULT_MODEL_NAME
    if meta_block:
        m = _EMBEDDING_MODEL_RE.search(meta_block.group(1))
        if m:
            model_name = m.group(1).strip()

    return {
        "embedding_model": model_name,
        "collection": f"{domain}_knowledge",
        "chroma_path": domain_chroma_path(domain),
        "bm25_path": domain_bm25_path(domain),
    }


def get_embedder(domain: str) -> SentenceTransformer:
    """Lazy-load embedding model for a domain. Cached per model_name."""
    cfg = get_domain_config(domain)
    model_name = cfg["embedding_model"]
    key = f"embedder:{model_name}"
    if key not in _model_cache:
        _model_cache[key] = SentenceTransformer(model_name)
    return _model_cache[key]


def get_reranker() -> CrossEncoder:
    """Lazy-load cross-encoder. Only loads on first hybrid search."""
    if "reranker" not in _model_cache:
        _model_cache["reranker"] = CrossEncoder(CROSS_ENCODER_MODEL)
    return _model_cache["reranker"]


def get_chroma_client(domain: str) -> chromadb.PersistentClient:
    """Get cached PersistentClient for a domain's isolated ChromaDB."""
    if domain not in _chroma_clients:
        db_path = domain_chroma_path(domain)
        db_path.mkdir(parents=True, exist_ok=True)
        _chroma_clients[domain] = chromadb.PersistentClient(
            path=str(db_path),
            settings=Settings(
                chroma_segment_cache_policy="LRU",
                chroma_memory_limit_bytes=CHROMA_MEMORY_LIMIT_BYTES,
                anonymized_telemetry=False,
            ),
        )
    return _chroma_clients[domain]


def bm25_cache_get(domain: str) -> dict | None:
    """Get BM25 index from cache, updating LRU order."""
    if domain in _bm25_cache:
        _bm25_cache.move_to_end(domain)
        return _bm25_cache[domain]
    return None


def bm25_cache_set(domain: str, data: dict) -> None:
    """Store BM25 index in cache with LRU eviction."""
    _bm25_cache[domain] = data
    _bm25_cache.move_to_end(domain)
    while len(_bm25_cache) > BM25_CACHE_MAX:
        _bm25_cache.popitem(last=False)


def bm25_cache_invalidate(domain: str) -> None:
    """Remove a domain's BM25 index from cache (e.g., after rebuild)."""
    _bm25_cache.pop(domain, None)


def unload_domain(domain: str) -> None:
    """Unload all resources tied to a domain: BM25 index, ChromaDB client."""
    _bm25_cache.pop(domain, None)
    _chroma_clients.pop(domain, None)
    gc.collect()


def is_reranker_available() -> bool:
    """Check if cross-encoder can be loaded. Does NOT trigger download."""
    if "reranker" in _model_cache:
        return True
    try:
        get_reranker()
        return True
    except Exception:
        return False
