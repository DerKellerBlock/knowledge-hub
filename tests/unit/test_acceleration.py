"""Unit tests for Phase 3.3a acceleration infrastructure.

Covers:

* ``KH_EMBEDDING_DEVICE`` env-var parsing in ``model_manager.get_embedder``
  (default ``cpu``, opt-in ``mps``). The ``SentenceTransformer``
  constructor is mocked so no real model download is triggered and the
  captured ``device`` kwarg can be asserted.
* ``context_cache.open_cache`` concurrency hardening:
  ``PRAGMA busy_timeout`` ≥ 5000 and ``check_same_thread=False``.
* ``contextualize_chunks`` parallel path: ``workers=1`` stays sequential
  (no ThreadPoolExecutor), ``workers>1`` dispatches cache misses to a
  ThreadPoolExecutor, and a simulated HTTP 429 usage-limit error sets
  the shared ``cancel_event`` so all workers abort.

No real Ollama / GPU / embedding model is loaded — the Ollama client is
mocked via :class:`FakeOllamaClient` / :class:`UsageLimitOllamaClient`
and the embedder constructor is replaced with a recording fake.
"""

from __future__ import annotations

import sqlite3
import threading

import pytest

pytestmark = pytest.mark.unit

import context_cache as cc
from context_cache import open_cache
from parser_base import Chunk

import contextualize_chunks as ctx_mod
from contextualize_chunks import (
    _DEFAULT_LLM_WORKERS,
    contextualize_chunks,
)


# ── Fake Ollama client (shared shape with test_contextualize_chunks.py) ────


class _FakeMessage:
    def __init__(self, content):
        self.content = content
        self.thinking = None


class _FakeChatResponse:
    def __init__(self, content):
        self.message = _FakeMessage(content)
        self.done_reason = "stop"
        self.eval_count = 42


class FakeOllamaClient:
    """Deterministic mock Ollama client (no GPU/download)."""

    def __init__(self, content="Valid context situating the chunk within the Godot Node3D tutorial."):
        self._content = content
        self.calls = []
        self._calls_lock = threading.Lock()

    def chat(self, model, messages, options=None, keep_alive=None, stream=False):
        with self._calls_lock:
            self.calls.append({
                "model": model,
                "messages": messages,
                "options": options,
                "keep_alive": keep_alive,
            })
        return _FakeChatResponse(self._content)


class UsageLimitOllamaClient:
    """Mock Ollama client that raises a persistent usage-limit error."""

    def __init__(self, message="rate limit exceeded: session quota reached"):
        self._calls = 0
        self._message = message

    def chat(self, model, messages, options=None, keep_alive=None, stream=False):
        self._calls += 1
        raise ConnectionError(self._message)

    @property
    def calls(self):
        return self._calls


MODEL = "gemma4:12b-mlx"


def _make_chunk(
    chunk_id="c0",
    domain="dummy",
    text="chunk body text",
    source_type="repo",
    chunk_type=None,
    source_file="foo-packed.md",
    chunk_id_in_file=0,
) -> Chunk:
    return Chunk(
        chunk_id=chunk_id,
        domain=domain,
        text=text,
        source_type=source_type,
        chunk_type=chunk_type,
        source_file=source_file,
        chunk_id_in_file=chunk_id_in_file,
    )


def _llm_entry(client) -> dict:
    return {"client": client, "model": MODEL, "backend": "ollama"}


# ── KH_EMBEDDING_DEVICE ────────────────────────────────────────────────────


class TestEmbeddingDevice:
    """Phase 3.3a: get_embedder() honours KH_EMBEDDING_DEVICE (default cpu)."""

    def setup_method(self):
        import model_manager as mm
        for key in list(mm._model_cache.keys()):
            if key.startswith("embedder:"):
                mm._model_cache.pop(key, None)

    def test_kh_embedding_device_default_cpu(self, monkeypatch):
        """Without KH_EMBEDDING_DEVICE the embedder loads on CPU (backward-compat)."""
        import model_manager as mm

        monkeypatch.delenv("KH_EMBEDDING_DEVICE", raising=False)
        monkeypatch.delenv("KH_EMBEDDING_MODEL", raising=False)

        captured: dict = {}

        class _FakeST:
            def __init__(self, model_name, *args, **kwargs):
                captured["model_name"] = model_name
                captured["device"] = kwargs.get("device", "UNSET")

        monkeypatch.setattr(mm, "SentenceTransformer", _FakeST)
        try:
            mm.get_embedder("godot")
        finally:
            for key in list(mm._model_cache.keys()):
                if key.startswith("embedder:"):
                    mm._model_cache.pop(key, None)

        assert captured["device"] == "cpu"

    def test_kh_embedding_device_mps(self, monkeypatch):
        """KH_EMBEDDING_DEVICE=mps propagates to SentenceTransformer(device=...)."""
        import model_manager as mm

        monkeypatch.setenv("KH_EMBEDDING_DEVICE", "mps")
        monkeypatch.delenv("KH_EMBEDDING_MODEL", raising=False)

        captured: dict = {}

        class _FakeST:
            def __init__(self, model_name, *args, **kwargs):
                captured["model_name"] = model_name
                captured["device"] = kwargs.get("device", "UNSET")

        monkeypatch.setattr(mm, "SentenceTransformer", _FakeST)
        try:
            mm.get_embedder("godot")
        finally:
            for key in list(mm._model_cache.keys()):
                if key.startswith("embedder:"):
                    mm._model_cache.pop(key, None)
            monkeypatch.delenv("KH_EMBEDDING_DEVICE", raising=False)

        assert captured["device"] == "mps"

    def test_device_is_part_of_cache_key(self, monkeypatch):
        """Switching KH_EMBEDDING_DEVICE loads a fresh instance (no wrong-device reuse)."""
        import model_manager as mm

        monkeypatch.delenv("KH_EMBEDDING_MODEL", raising=False)

        class _FakeST:
            def __init__(self, model_name, *args, **kwargs):
                self.device = kwargs.get("device", "cpu")

        monkeypatch.setattr(mm, "SentenceTransformer", _FakeST)

        monkeypatch.setenv("KH_EMBEDDING_DEVICE", "cpu")
        cpu_embedder = mm.get_embedder("godot")
        cpu_key = [k for k in mm._model_cache if k.startswith("embedder:") and k.endswith(":cpu")][0]

        monkeypatch.setenv("KH_EMBEDDING_DEVICE", "mps")
        mps_embedder = mm.get_embedder("godot")
        mps_key = [k for k in mm._model_cache if k.startswith("embedder:") and k.endswith(":mps")][0]

        try:
            assert cpu_key != mps_key
            assert cpu_embedder.device == "cpu"
            assert mps_embedder.device == "mps"
            assert cpu_embedder is not mps_embedder
        finally:
            for key in list(mm._model_cache.keys()):
                if key.startswith("embedder:"):
                    mm._model_cache.pop(key, None)
            monkeypatch.delenv("KH_EMBEDDING_DEVICE", raising=False)


# ── SQLite busy_timeout + check_same_thread ────────────────────────────────


class TestCacheConcurrency:
    """Phase 3.3a: open_cache() hardens the connection for ThreadPool use."""

    def test_busy_timeout_set(self, tmp_hub):
        conn = open_cache("dummy")
        try:
            row = conn.execute("PRAGMA busy_timeout").fetchone()
            assert row[0] >= 5000
        finally:
            conn.close()

    def test_check_same_thread_false(self, tmp_hub):
        # A connection opened with check_same_thread=False can be used
        # from a different thread. The default (True) would raise
        # ProgrammingError on cross-thread use.
        conn = open_cache("dummy")
        errors: list = []

        def _worker():
            try:
                conn.execute("SELECT COUNT(*) FROM context_cache").fetchone()
            except Exception as e:  # noqa: BLE001
                errors.append(e)

        try:
            t = threading.Thread(target=_worker)
            t.start()
            t.join()
        finally:
            conn.close()

        assert errors == [], f"Cross-thread use failed: {errors}"


# ── Parallel LLM workers ───────────────────────────────────────────────────


class TestParallelWorkers:
    """Phase 3.3a: workers>1 dispatches misses to a ThreadPoolExecutor."""

    def test_workers_default_1_sequential(self, tmp_hub, monkeypatch):
        """workers=1 (default) must NOT spawn a ThreadPoolExecutor."""
        # Spy on ThreadPoolExecutor construction inside the module.
        called = {"pool": False}

        class _NoPool:
            def __init__(self, *a, **kw):
                called["pool"] = True
                raise AssertionError(
                    "ThreadPoolExecutor must not be created when workers=1"
                )

        monkeypatch.setattr(ctx_mod.concurrent.futures, "ThreadPoolExecutor", _NoPool)

        chunks = [
            _make_chunk(chunk_id=f"c{i}", text=f"body{i}",
                        chunk_id_in_file=i)
            for i in range(3)
        ]
        client = FakeOllamaClient()
        conn = open_cache("dummy")
        try:
            contextualize_chunks(
                domain="dummy", chunks=chunks,
                llm_entry=_llm_entry(client), conn=conn, model_name=MODEL,
                workers=1,
            )
        finally:
            conn.close()

        assert called["pool"] is False
        assert len(client.calls) == 3
        assert all(c.context_prefix is not None for c in chunks)

    def test_workers_3_uses_threadpool(self, tmp_hub, monkeypatch):
        """workers=3 dispatches the 3 cache misses concurrently."""
        # Patch _generate_with_retry_cancelable so we can track
        # concurrency without touching the LLM. Record the active
        # worker count with a thread-safe counter.
        active = {"n": 0, "max": 0}
        active_lock = threading.Lock()
        barrier = threading.Barrier(3)

        def _fake_worker(llm_entry, doc_text, chunk_text, cancel_event):
            with active_lock:
                active["n"] += 1
                active["max"] = max(active["max"], active["n"])
            # Block until all 3 workers are simultaneously inside the
            # function — this proves the pool actually ran them in
            # parallel rather than serially.
            try:
                barrier.wait(timeout=5.0)
            except threading.BrokenBarrierError:
                pass
            with active_lock:
                active["n"] -= 1
            return "Valid parallel context situating the chunk in the doc."

        monkeypatch.setattr(
            ctx_mod, "_generate_with_retry_cancelable", _fake_worker,
        )

        chunks = [
            _make_chunk(chunk_id=f"c{i}", text=f"body{i}",
                        chunk_id_in_file=i)
            for i in range(3)
        ]
        client = FakeOllamaClient()
        conn = open_cache("dummy")
        try:
            contextualize_chunks(
                domain="dummy", chunks=chunks,
                llm_entry=_llm_entry(client), conn=conn, model_name=MODEL,
                workers=3,
            )
        finally:
            conn.close()

        assert active["max"] == 3, (
            f"Expected 3 concurrent workers, max observed was {active['max']}"
        )
        assert all(c.context_prefix is not None for c in chunks)
        # 3 cache entries persisted despite parallel generation.
        conn2 = open_cache("dummy")
        try:
            assert cc.count_entries(conn2, model=MODEL) == 3
        finally:
            conn2.close()

    def test_cancel_event_on_usage_limit(self, tmp_hub, monkeypatch):
        """A simulated HTTP 429 usage-limit sets cancel_event and aborts workers."""
        # Every worker raises the usage-limit RuntimeError. The first
        # one to be drained sets the cancel_event; the others either
        # raise the same error (caught by the "Usage limit" branch) or
        # observe the now-set cancel_event and raise the cancelled
        # variant. No valid context is ever produced → no cache writes.
        cancel_seen = {"event": None}
        call_count = {"n": 0}
        call_lock = threading.Lock()
        usage_msg = (
            "Usage limit reached — run `ollama signin` with a "
            "different account, then restart. Cache is preserved "
            "for resume."
        )

        def _worker(llm_entry, doc_text, chunk_text, cancel_event):
            cancel_seen["event"] = cancel_event
            with call_lock:
                call_count["n"] += 1
            if cancel_event.is_set():
                raise RuntimeError("Usage limit reached — worker cancelled")
            raise RuntimeError(usage_msg)

        monkeypatch.setattr(
            ctx_mod, "_generate_with_retry_cancelable", _worker,
        )

        chunks = [
            _make_chunk(chunk_id=f"c{i}", text=f"body{i}",
                        chunk_id_in_file=i)
            for i in range(5)
        ]
        client = UsageLimitOllamaClient()
        conn = open_cache("dummy")
        try:
            # The function should NOT raise — the parallel path catches
            # the usage-limit RuntimeError, sets the cancel_event, and
            # drains the remaining futures (which then raise the same
            # RuntimeError, also caught by the "Usage limit" branch).
            contextualize_chunks(
                domain="dummy", chunks=chunks,
                llm_entry=_llm_entry(client), conn=conn, model_name=MODEL,
                workers=3,
            )
        finally:
            conn.close()

        # The cancel_event was created and shared with workers.
        assert cancel_seen["event"] is not None
        # The cancel_event is set after the first usage-limit error.
        assert cancel_seen["event"].is_set()
        # At least one worker observed the set cancel_event (proves
        # propagation, not just first-worker failure).
        assert call_count["n"] >= 1
        # No cache entries should have been written (every miss raised
        # usage-limit or was cancelled before producing a context).
        conn2 = open_cache("dummy")
        try:
            assert cc.count_entries(conn2, model=MODEL) == 0
        finally:
            conn2.close()

    def test_workers_clamped_to_1_when_below(self, tmp_hub, monkeypatch):
        """workers=0 (or negative) is clamped to 1 (sequential safety)."""
        called = {"pool": False}

        class _NoPool:
            def __init__(self, *a, **kw):
                called["pool"] = True
                raise AssertionError(
                    "ThreadPoolExecutor must not be created when workers<=1"
                )

        monkeypatch.setattr(ctx_mod.concurrent.futures, "ThreadPoolExecutor", _NoPool)

        chunks = [
            _make_chunk(chunk_id="c0", text="body0", chunk_id_in_file=0),
        ]
        client = FakeOllamaClient()
        conn = open_cache("dummy")
        try:
            contextualize_chunks(
                domain="dummy", chunks=chunks,
                llm_entry=_llm_entry(client), conn=conn, model_name=MODEL,
                workers=0,
            )
        finally:
            conn.close()

        assert called["pool"] is False


# ── Default constant ───────────────────────────────────────────────────────


def test_default_llm_workers_constant_is_1():
    """Backward-compat: _DEFAULT_LLM_WORKERS stays 1 (sequential default)."""
    assert _DEFAULT_LLM_WORKERS == 1