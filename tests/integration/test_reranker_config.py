"""Integration tests for model_manager.get_reranker() live env-var resolution.

Verifies the Phase-1 fix for finding C2: ``get_reranker()`` must read the
``KH_RERANKER_MODEL`` environment variable LIVE on every cache-miss, not a
stale import-time copy of ``config.CROSS_ENCODER_MODEL``.

The ``CrossEncoder`` constructor is mocked so no real model download is
triggered.
"""

import pytest

pytestmark = pytest.mark.integration


def _clear_reranker_cache():
    """Clear the reranker entry from model_manager's cache (if loaded)."""
    import model_manager

    model_manager._model_cache.pop("reranker", None)


def test_get_reranker_reads_env_var_live(monkeypatch):
    """KH_RERANKER_MODEL set AFTER import must still reach get_reranker()."""
    import model_manager

    _clear_reranker_cache()

    captured: dict = {}

    class _FakeCrossEncoder:
        def __init__(self, model_name, **kwargs):
            captured["model_name"] = model_name
            captured["trust_remote_code"] = kwargs.get("trust_remote_code")

    monkeypatch.setattr(model_manager, "CrossEncoder", _FakeCrossEncoder)
    monkeypatch.setenv("KH_RERANKER_MODEL", "jinaai/jina-reranker-v2-base-multilingual")

    try:
        model_manager.get_reranker()
    finally:
        _clear_reranker_cache()
        monkeypatch.delenv("KH_RERANKER_MODEL", raising=False)

    assert captured["model_name"] == "jinaai/jina-reranker-v2-base-multilingual"
    assert captured["trust_remote_code"] is True


def test_get_reranker_defaults_without_env_var(monkeypatch):
    """Without KH_RERANKER_MODEL, the default ms-marco MiniLM is used."""
    import model_manager

    _clear_reranker_cache()

    captured: dict = {}

    class _FakeCrossEncoder:
        def __init__(self, model_name, **kwargs):
            captured["model_name"] = model_name

    monkeypatch.setattr(model_manager, "CrossEncoder", _FakeCrossEncoder)
    monkeypatch.delenv("KH_RERANKER_MODEL", raising=False)

    try:
        model_manager.get_reranker()
    finally:
        _clear_reranker_cache()

    assert captured["model_name"] == "cross-encoder/ms-marco-MiniLM-L-12-v2"


def test_get_reranker_uses_cached_after_first_load(monkeypatch):
    """After the first load, subsequent calls return the cached instance
    without re-instantiating CrossEncoder (env-var is only read on miss)."""
    import model_manager

    _clear_reranker_cache()

    call_count = {"n": 0}

    class _FakeCrossEncoder:
        def __init__(self, model_name, **kwargs):
            call_count["n"] += 1

    monkeypatch.setattr(model_manager, "CrossEncoder", _FakeCrossEncoder)
    monkeypatch.setenv("KH_RERANKER_MODEL", "cross-encoder/ms-marco-MiniLM-L-12-v2")

    try:
        model_manager.get_reranker()
        model_manager.get_reranker()
        assert call_count["n"] == 1
    finally:
        _clear_reranker_cache()
        monkeypatch.delenv("KH_RERANKER_MODEL", raising=False)