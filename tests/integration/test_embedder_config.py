"""Integration tests for model_manager.get_embedder() live env-var resolution.

Verifies the Phase-2a fix for blind-spot B1: ``get_embedder()`` must read
the ``KH_EMBEDDING_MODEL`` environment variable LIVE on every cache-miss,
not only from ``domain.md``. Resolution precedence (Decision 2.7):

    KH_EMBEDDING_MODEL env var  >  domain.md  >  DEFAULT_MODEL_NAME

The ``SentenceTransformer`` constructor is mocked so no real model
download is triggered.
"""

import pytest

pytestmark = pytest.mark.integration


def _clear_embedder_cache():
    """Clear all embedder entries from model_manager's cache (if loaded).

    Embedder cache keys are ``embedder:<model_name>``, so we drop every
    key that starts with the embedder prefix. This is more robust than
    hard-coding a single model name.
    """
    import model_manager

    for key in list(model_manager._model_cache.keys()):
        if key.startswith("embedder:"):
            model_manager._model_cache.pop(key, None)


def test_get_embedder_reads_env_var_live(monkeypatch):
    """KH_EMBEDDING_MODEL set AFTER import must reach get_embedder()."""
    import model_manager

    _clear_embedder_cache()

    captured: dict = {}

    class _FakeSentenceTransformer:
        def __init__(self, model_name, *args, **kwargs):
            captured["model_name"] = model_name

    monkeypatch.setattr(model_manager, "SentenceTransformer", _FakeSentenceTransformer)
    monkeypatch.setenv("KH_EMBEDDING_MODEL", "BAAI/bge-m3")

    try:
        model_manager.get_embedder("godot")
    finally:
        _clear_embedder_cache()
        monkeypatch.delenv("KH_EMBEDDING_MODEL", raising=False)

    assert captured["model_name"] == "BAAI/bge-m3"


def test_get_embedder_defaults_to_domain_md_without_env_var(monkeypatch):
    """Without KH_EMBEDDING_MODEL, the model from domain.md is used.

    The godot domain.md currently lists ``all-mpnet-base-v2`` (Phase-2a
    pre-rebuild state), so the fallback chain resolves to that name. We
    read the expected name dynamically from get_domain_config so the test
    stays correct if domain.md is updated in a later phase.
    """
    import model_manager

    _clear_embedder_cache()

    captured: dict = {}

    class _FakeSentenceTransformer:
        def __init__(self, model_name, *args, **kwargs):
            captured["model_name"] = model_name

    monkeypatch.setattr(model_manager, "SentenceTransformer", _FakeSentenceTransformer)
    monkeypatch.delenv("KH_EMBEDDING_MODEL", raising=False)

    expected = model_manager.get_domain_config("godot")["embedding_model"]

    try:
        model_manager.get_embedder("godot")
    finally:
        _clear_embedder_cache()

    assert captured["model_name"] == expected


def test_get_embedder_uses_cached_after_first_load(monkeypatch):
    """After the first load, subsequent calls return the cached instance
    without re-instantiating SentenceTransformer (env-var is only read on
    cache-miss, analog to the reranker test)."""
    import model_manager

    _clear_embedder_cache()

    call_count = {"n": 0}

    class _FakeSentenceTransformer:
        def __init__(self, model_name, *args, **kwargs):
            call_count["n"] += 1

    monkeypatch.setattr(model_manager, "SentenceTransformer", _FakeSentenceTransformer)
    monkeypatch.setenv("KH_EMBEDDING_MODEL", "BAAI/bge-m3")

    try:
        model_manager.get_embedder("godot")
        model_manager.get_embedder("godot")
        assert call_count["n"] == 1
    finally:
        _clear_embedder_cache()
        monkeypatch.delenv("KH_EMBEDDING_MODEL", raising=False)