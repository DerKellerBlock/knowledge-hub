"""Unit tests for config.py path helpers."""

import importlib
from pathlib import Path

from mcp_servers.knowledge_hub.config import (
    HUB_ROOT,
    DOMAINS_DIR,
    SCRIPTS_DIR,
    CHROMA_DIR,
    PERSONAL_DIR,
    domain_chroma_path,
    domain_bm25_path,
    legacy_bm25_path,
    legacy_collection_path,
    DEFAULT_MODEL_NAME,
    EMBEDDING_MODEL_ENV_VAR,
    CROSS_ENCODER_MODEL,
    BM25_CACHE_MAX,
    CHROMA_MEMORY_LIMIT_BYTES,
)


def test_hub_root_is_absolute():
    assert HUB_ROOT.is_absolute()
    assert HUB_ROOT.name == "knowledge-hub"


def test_domains_dir_under_hub_root():
    assert DOMAINS_DIR == HUB_ROOT / "domains"


def test_scripts_dir_under_hub_root():
    assert SCRIPTS_DIR == HUB_ROOT / "scripts"


def test_chroma_dir_under_hub_root():
    assert CHROMA_DIR == HUB_ROOT / "chromadb_data"


def test_domain_chroma_path_godot():
    p = domain_chroma_path("godot")
    assert p == CHROMA_DIR / "godot" / "chroma"


def test_domain_chroma_path_davinci_resolve():
    p = domain_chroma_path("davinci_resolve")
    assert p == CHROMA_DIR / "davinci_resolve" / "chroma"


def test_domain_chroma_path_arbitrary():
    p = domain_chroma_path("my_domain")
    assert p == CHROMA_DIR / "my_domain" / "chroma"


def test_domain_bm25_path_godot():
    p = domain_bm25_path("godot")
    assert p == CHROMA_DIR / "godot" / "godot_bm25.pkl"


def test_domain_bm25_path_davinci_resolve():
    p = domain_bm25_path("davinci_resolve")
    assert p == CHROMA_DIR / "davinci_resolve" / "davinci_resolve_bm25.pkl"


def test_legacy_bm25_path():
    assert legacy_bm25_path("godot") == CHROMA_DIR / "godot_bm25.pkl"


def test_legacy_collection_path():
    assert legacy_collection_path("godot") == CHROMA_DIR / "godot_knowledge"


def test_default_model_name_is_string():
    assert isinstance(DEFAULT_MODEL_NAME, str)
    assert len(DEFAULT_MODEL_NAME) > 0


def test_embedding_model_env_var_name_is_string():
    """KH_EMBEDDING_MODEL env-var name is exposed as a constant (Phase 2a)."""
    assert isinstance(EMBEDDING_MODEL_ENV_VAR, str)
    assert EMBEDDING_MODEL_ENV_VAR == "KH_EMBEDDING_MODEL"
    assert len(EMBEDDING_MODEL_ENV_VAR) > 0


def test_default_model_name_is_all_mpnet_fallback():
    """DEFAULT_MODEL_NAME stays the all-mpnet fallback (Decision 2.2).

    The live model is resolved in model_manager.get_embedder() via the
    KH_EMBEDDING_MODEL env var / domain.md; this constant is the final
    fallback only.
    """
    assert DEFAULT_MODEL_NAME == "all-mpnet-base-v2"


def test_cross_encoder_model_is_string():
    assert isinstance(CROSS_ENCODER_MODEL, str)


def test_bm25_cache_max_is_positive_int():
    assert isinstance(BM25_CACHE_MAX, int)
    assert BM25_CACHE_MAX > 0


def test_chroma_memory_limit_is_bytes():
    assert isinstance(CHROMA_MEMORY_LIMIT_BYTES, int)
    assert CHROMA_MEMORY_LIMIT_BYTES > 0


# ── CROSS_ENCODER_MODEL / KH_RERANKER_MODEL env override (Phase 1, 1.2) ──


def test_reranker_model_default(monkeypatch):
    """Without KH_RERANKER_MODEL set, default is the legacy ms-marco MiniLM."""
    monkeypatch.delenv("KH_RERANKER_MODEL", raising=False)
    from mcp_servers.knowledge_hub import config as cfg

    importlib.reload(cfg)
    try:
        assert cfg.CROSS_ENCODER_MODEL == "cross-encoder/ms-marco-MiniLM-L-12-v2"
    finally:
        # Reload once more so the module-level constant is the import-time
        # value (the real env, not a test artifact) for subsequent tests.
        importlib.reload(cfg)


def test_reranker_model_env_var_override(monkeypatch):
    """KH_RERANKER_MODEL env var overrides the default reranker at import time."""
    monkeypatch.setenv("KH_RERANKER_MODEL", "jinaai/jina-reranker-v2-base-multilingual")
    from mcp_servers.knowledge_hub import config as cfg

    importlib.reload(cfg)
    try:
        assert cfg.CROSS_ENCODER_MODEL == "jinaai/jina-reranker-v2-base-multilingual"
    finally:
        monkeypatch.delenv("KH_RERANKER_MODEL", raising=False)
        importlib.reload(cfg)