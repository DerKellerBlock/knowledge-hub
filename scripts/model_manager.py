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
import os
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

# Import config via the fully-qualified module name so that there is
# exactly ONE config module object in sys.modules. The previous
# `from config import ...` style created a *second* module object
# (sys.modules['config']) distinct from the one imported by tests
# and the rest of the codebase via `mcp_servers.knowledge_hub.config`.
# That made monkeypatched values (DOMAINS_DIR, CHROMA_DIR) invisible
# to get_domain_config(), breaking integration tests for synthetic
# domains (Phase 2.2 late-chunking tests).
import sys as _sys
_pkg_root = Path(__file__).resolve().parent.parent
if str(_pkg_root) not in _sys.path:
    _sys.path.insert(0, str(_pkg_root))

from mcp_servers.knowledge_hub.config import (
    CHROMA_DIR,
    DOMAINS_DIR,
    domain_chroma_path,
    domain_bm25_path,
    DEFAULT_MODEL_NAME,
    CHROMA_MEMORY_LIMIT_BYTES,
    BM25_CACHE_MAX,
)

# Default cross-encoder model name. Read LIVE from KH_RERANKER_MODEL in
# get_reranker() so runtime env-var overrides take effect after import.
# Kept here as a fallback constant for documentation/other modules.
DEFAULT_RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-12-v2"

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
_SOURCE_TYPES_RE = re.compile(
    r"- Source-Types:\s*(.+?)\s*$",
    re.MULTILINE,
)

DEFAULT_SOURCE_TYPES = ["repo"]


def get_domain_config(domain: str) -> dict:
    """Read domain.md Metadaten block and return a config dict.

    The ``domain.md`` path is resolved via the live ``config`` module
    (looked up via ``sys.modules``) so tests can monkeypatch
    ``config.DOMAINS_DIR`` and have the change take effect. The
    previous hardcoded ``Path(__file__).resolve().parent.parent /
    "domains" / ...`` ignored the patchable constant, breaking
    integration tests for synthetic domains.

    Returns:
        {
            "embedding_model": "all-mpnet-base-v2",
            "collection": "<domain>_knowledge",
            "chroma_path": Path,
            "bm25_path": Path,
            "source_types": list[str]   (e.g. ["pdf"], ["repo"], or
                ["pdf", "repo"]; default ["repo"] when field missing),
        }
    """
    # Live lookup of config.DOMAINS_DIR so monkeypatch in tests works.
    # Prefer the fully-qualified mcp_servers.knowledge_hub.config module
    # (the one tests patch via conftest) over the bare 'config' alias that
    # earlier `from config import ...` statements used to create. Falls
    # back to the bare alias for backwards-compat with callers that may
    # have imported the module under either name.
    import sys as _sys
    _config_mod = _sys.modules.get("mcp_servers.knowledge_hub.config")
    if _config_mod is None:
        _config_mod = _sys.modules.get("config")
    if _config_mod is None:
        # Last-resort: import directly (shouldn't normally happen).
        from mcp_servers.knowledge_hub import config as _config_mod  # noqa
    domain_md = _config_mod.DOMAINS_DIR / domain / "domain.md"
    if not domain_md.exists():
        # Fallback to defaults
        return {
            "embedding_model": DEFAULT_MODEL_NAME,
            "collection": f"{domain}_knowledge",
            "chroma_path": domain_chroma_path(domain),
            "bm25_path": domain_bm25_path(domain),
            "source_types": list(DEFAULT_SOURCE_TYPES),
        }

    text = domain_md.read_text(encoding="utf-8")
    meta_block = _DOMAIN_META_RE.search(text)
    model_name = DEFAULT_MODEL_NAME
    source_types: list[str] = list(DEFAULT_SOURCE_TYPES)
    if meta_block:
        block = meta_block.group(1)
        m = _EMBEDDING_MODEL_RE.search(block)
        if m:
            model_name = m.group(1).strip()

        sm = _SOURCE_TYPES_RE.search(block)
        if sm:
            raw = sm.group(1).strip()
            parsed = [t.strip() for t in raw.split(",") if t.strip()]
            if parsed:
                source_types = parsed

    return {
        "embedding_model": model_name,
        "collection": f"{domain}_knowledge",
        "chroma_path": domain_chroma_path(domain),
        "bm25_path": domain_bm25_path(domain),
        "source_types": source_types,
    }


def get_embedder(domain: str) -> SentenceTransformer:
    """Lazy-load embedding model for a domain. Cached per model_name.

    Resolution order (Decision 2.7):

    1. ``KH_EMBEDDING_MODEL`` environment variable (read LIVE on every
       cache-miss, analog to :func:`get_reranker`).
    2. ``domain.md`` ``Metadaten → Embedding-Model`` entry.
    3. :data:`config.DEFAULT_MODEL_NAME` (``all-mpnet-base-v2``) fallback.

    The cache key is ``embedder:<model_name>``. Switching the env var at
    runtime therefore loads a new model into the cache on the next
    cache-miss; the previously loaded model stays resident until the
    process exits (Phase 2a limitation, see LIM-008). Loading both
    BGE-M3 (~2.2 GB) and all-mpnet-base-v2 (~420 MB) simultaneously
    costs ~2.6 GB of RAM. An LRU-bounded ``_model_cache`` is deferred to
    Phase 2b (B4).
    """
    cfg = get_domain_config(domain)
    model_name = os.environ.get("KH_EMBEDDING_MODEL", cfg["embedding_model"])
    key = f"embedder:{model_name}"
    if key not in _model_cache:
        _model_cache[key] = SentenceTransformer(model_name)
    return _model_cache[key]


def get_reranker() -> CrossEncoder:
    """Lazy-load cross-encoder. Only loads on first hybrid search.

    The model name is read LIVE from the ``KH_RERANKER_MODEL`` environment
    variable on every cache-miss (not bound at import time), so runtime
    overrides take effect without reloading the module.

    ``trust_remote_code=True`` is required for jina-reranker-v2-base-multilingual
    because that model ships custom code (``auto_map`` in config.json) which
    HuggingFace refuses to load without explicit trust. The legacy
    ms-marco MiniLM has no ``auto_map`` and ignores this flag, so the same
    call works for both models.
    """
    if "reranker" not in _model_cache:
        model_name = os.environ.get(
            "KH_RERANKER_MODEL",
            DEFAULT_RERANKER_MODEL,
        )
        _model_cache["reranker"] = CrossEncoder(
            model_name,
            trust_remote_code=True,  # required for jina-reranker-v2 custom code
        )
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
