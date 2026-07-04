"""Integration tests for Phase 3.3a acceleration infrastructure.

Two flaky-risk areas that unit tests cannot exercise realistically:

* ``test_parallel_cache_write_no_lock`` — 3 threads call ``put_cached``
  concurrently through a :class:`ThreadPoolExecutor` against a real
  SQLite file opened with ``check_same_thread=False`` +
  ``busy_timeout=5000``. The hardening (Fix 2 + Fix 3) must prevent
  ``OperationalError: database is locked``. We use a ``threading.Lock``
  around the writes to mirror the caller pattern in
  :func:`contextualize_chunks.contextualize_chunks`.

* ``test_mps_encode_pre_flight`` — guards against a BGE-M3 MPS
  regression. The test is skipped automatically when
  ``sentence_transformers`` is missing OR when MPS is unavailable (CI /
  non-Apple-Silicon hosts). On Apple Silicon it loads BGE-M3 on MPS and
  encodes 10 short texts, asserting the call returns within 30 s and
  without hanging. This is the Pre-Flight Mitigation referenced in
  R1.1: a green test means an MPS build is safe to start.
"""

from __future__ import annotations

import threading
import time

import pytest

pytestmark = pytest.mark.integration

import context_cache as cc
from context_cache import open_cache


def test_parallel_cache_write_no_lock(tmp_hub):
    """3 concurrent put_cached calls via ThreadPoolExecutor do not raise.

    Phase 3.3a Fix 2 + Fix 3: ``open_cache()`` now sets
    ``check_same_thread=False`` and ``PRAGMA busy_timeout=5000``. The
    caller pattern in ``contextualize_chunks`` wraps writes in a
    ``threading.Lock`` (serialisation) and lets ``busy_timeout`` absorb
    residual races (WAL checkpoint contention). This test reproduces the
    caller pattern end-to-end against a real SQLite file.
    """
    conn = open_cache("dummy")
    write_lock = threading.Lock()
    errors: list = []

    def _write(i):
        try:
            with write_lock:
                cc.put_cached(
                    conn, "foo-packed.md", i,
                    cc.chunk_text_hash(f"body{i}"),
                    "gemma4:12b-mlx", f"context-{i}",
                )
        except Exception as e:  # noqa: BLE001
            errors.append(e)

    from concurrent.futures import ThreadPoolExecutor

    try:
        with ThreadPoolExecutor(max_workers=3) as pool:
            list(pool.map(_write, range(9)))
    finally:
        conn.close()

    assert errors == [], f"Concurrent cache writes failed: {errors}"

    # All 9 entries survived (idempotent key per (file, id, hash, model)).
    conn2 = open_cache("dummy")
    try:
        assert cc.count_entries(conn2, model="gemma4:12b-mlx") == 9
    finally:
        conn2.close()


def test_mps_encode_pre_flight(tmp_hub, monkeypatch):
    """BGE-M3 on MPS encodes 10 texts within 30 s without hanging.

    Pre-Flight Mitigation (R1.1): a green test means an MPS build is
    safe to start. Skipped when ``sentence_transformers`` is missing or
    MPS is unavailable (CI / non-Apple-Silicon).

    This test deliberately loads the real BGE-M3 model — it is NOT a
    mock. It is therefore slow (~10–20 s on first download, ~2 s once
    cached) and gated behind the integration marker so it only runs
    when an operator explicitly selects ``-m integration``.
    """
    st = pytest.importorskip("sentence_transformers")
    torch = pytest.importorskip("torch")
    if not torch.backends.mps.is_available():
        pytest.skip("MPS unavailable on this host")

    monkeypatch.setenv("KH_EMBEDDING_DEVICE", "mps")
    monkeypatch.setenv("KH_EMBEDDING_MODEL", "BAAI/bge-m3")

    import model_manager as mm
    # Clear any cached embedder so the MPS instance is built fresh.
    for key in list(mm._model_cache.keys()):
        if key.startswith("embedder:"):
            mm._model_cache.pop(key, None)

    try:
        start = time.time()
        embedder = mm.get_embedder("godot")
        vecs = embedder.encode(
            [f"This is test sentence number {i} for MPS pre-flight." for i in range(10)],
            show_progress_bar=False,
        )
        elapsed = time.time() - start
    finally:
        for key in list(mm._model_cache.keys()):
            if key.startswith("embedder:"):
                mm._model_cache.pop(key, None)

    assert vecs.shape[0] == 10
    assert elapsed < 30.0, (
        f"MPS encode took {elapsed:.1f}s (>30s) — possible hang, "
        f"fall back to KH_EMBEDDING_DEVICE=cpu"
    )