"""E2E integration test for jina-reranker-v2-base-multilingual (LIM-007 regression guard).

Verifies that the jina reranker loads via ``KH_RERANKER_MODEL`` and produces
scores in the sigmoid range [0, 1] (not the ms-marco logit range -10..+10),
and that ``trust_remote_code=True`` is passed through to CrossEncoder.

This test loads the real ~560 MB jina model. It is skipped automatically when
the model is not present in the local HuggingFace cache, so the standard
``pytest -m e2e`` suite does not require a network download. To run it
explicitly, first trigger the download via::

    KH_RERANKER_MODEL=jinaai/jina-reranker-v2-base-multilingual \\
        python -c "import model_manager; model_manager.get_reranker()"

Run: pytest tests/e2e/test_jina_reranker_integration.py -v -m e2e
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

HUB_ROOT = Path(__file__).resolve().parent.parent.parent
# HuggingFace hub cache layout: models--<org>--<model>/snapshots/<hash>/
HF_HUB_CACHE = Path(os.environ.get("HF_HOME", str(Path.home() / ".cache" / "huggingface"))) / "hub"
JINA_CACHE_DIR = HF_HUB_CACHE / "models--jinaai--jina-reranker-v2-base-multilingual"

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.skipif(
        not JINA_CACHE_DIR.exists(),
        reason=(
            "jina reranker not cached locally. Trigger a download first: "
            "KH_RERANKER_MODEL=jinaai/jina-reranker-v2-base-multilingual "
            "python -c \"import model_manager; model_manager.get_reranker()\""
        ),
    ),
]


def _clear_reranker_cache() -> None:
    """Drop the reranker entry from model_manager's cache (if loaded)."""
    import model_manager

    model_manager._model_cache.pop("reranker", None)


def test_jina_reranker_loads_and_predicts_sigmoid_scores(monkeypatch):
    """jina loaded via KH_RERANKER_MODEL must produce scores in [0, 1]."""
    import model_manager

    _clear_reranker_cache()
    monkeypatch.setenv("KH_RERANKER_MODEL", "jinaai/jina-reranker-v2-base-multilingual")

    try:
        model = model_manager.get_reranker()
        scores = model.predict([("test query", "test document")])
        score = float(scores[0])
    finally:
        _clear_reranker_cache()
        monkeypatch.delenv("KH_RERANKER_MODEL", raising=False)

    # jina uses a sigmoid head: scores are in [0, 1].
    # ms-marco logits would be roughly in [-10, 10] and fail this assertion.
    assert 0.0 <= score <= 1.0, f"jina score {score} outside sigmoid range [0, 1]"


def test_jina_reranker_passes_trust_remote_code(monkeypatch):
    """get_reranker() must pass trust_remote_code=True for jina models.

    Regression guard for LIM-007: jina ships custom code (auto_map) that
    HuggingFace refuses to load without explicit trust. We capture the
    constructor kwargs via a patched CrossEncoder and assert the flag is set.
    The real jina model is not loaded in this test path.
    """
    import model_manager

    _clear_reranker_cache()

    captured: dict = {}

    class _FakeCrossEncoder:
        def __init__(self, model_name, **kwargs):
            captured["model_name"] = model_name
            captured["trust_remote_code"] = kwargs.get("trust_remote_code")
            self.predict = lambda pairs: [0.5 for _ in pairs]

    monkeypatch.setattr(model_manager, "CrossEncoder", _FakeCrossEncoder)
    monkeypatch.setenv("KH_RERANKER_MODEL", "jinaai/jina-reranker-v2-base-multilingual")

    try:
        model_manager.get_reranker()
    finally:
        _clear_reranker_cache()
        monkeypatch.delenv("KH_RERANKER_MODEL", raising=False)

    assert captured["model_name"] == "jinaai/jina-reranker-v2-base-multilingual"
    assert captured["trust_remote_code"] is True