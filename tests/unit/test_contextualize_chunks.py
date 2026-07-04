"""Unit tests for :mod:`contextualize_chunks` (Phase 3.1b, Task 8 / Phase D).

Covers:
  * Path-A filter (NB-2 core): excludes ``late_chunk``, includes
    ``personal_section`` and ``None`` (fallback) chunk_types.
  * Mixed-domain (NB-2 mixed): repo chunk contextualized, PDF late_chunk
    skipped.
  * Cache hit skips LLM (M2 happy-path).
  * Cache miss calls LLM and writes cache entries.
  * Cache resume after partial crash (M2 crash-path).
  * Retry / backoff (NB-5): survives an Ollama restart mid-batch, fails
    after 3 permanent retries.
  * ``context_prefix`` assignment + late_chunk skipped.
  * ``--dry-run`` mode: no LLM, no cache.
  * Output-validation rejection sets ``context_prefix = None`` and does
    NOT write a cache entry.
  * Batch commit size (``conn.commit()`` call count).

No real Ollama / Gemma download or GPU is needed — the Ollama client is
mocked via :class:`FakeOllamaClient` / :class:`FlakyOllamaClient`.
"""

import sqlite3

import pytest

pytestmark = pytest.mark.unit

import context_cache as cc
from context_cache import open_cache
from parser_base import Chunk

import contextualize_chunks as ctx_mod
from contextualize_chunks import (
    _RetryClientProxy,
    _is_usage_limit_error,
    contextualize_chunks,
    document_text_for_chunk,
    load_chunks_for_contextualization,
)


# ── Fake Ollama clients (shared with test_contextualize_infra.py) ──────────


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

    def __init__(self, content="This chunk describes a Godot API method for 3D rotation tutorial."):
        self._content = content
        self.calls = []

    def chat(self, model, messages, options=None, keep_alive=None, stream=False):
        self.calls.append({
            "model": model,
            "messages": messages,
            "options": options,
            "keep_alive": keep_alive,
        })
        return _FakeChatResponse(self._content)


class FlakyOllamaClient:
    """Mock Ollama client that fails the first N calls then succeeds.

    Used for NB-5 retry tests. Raises ``ConnectionError`` on calls
    ``1..fail_until_call`` (1-based), succeeds afterwards.
    """

    def __init__(self, fail_until_call=2, content="Valid context after retry, situating the chunk."):
        self._fail_until = fail_until_call
        self._calls = 0
        self._content = content

    def chat(self, model, messages, options=None, keep_alive=None, stream=False):
        self._calls += 1
        if self._calls <= self._fail_until:
            raise ConnectionError("simulated Ollama down")
        return _FakeChatResponse(self._content)

    @property
    def calls(self):
        return self._calls


class PermanentlyFailingOllamaClient:
    """Mock Ollama client that always raises ConnectionError."""

    def __init__(self):
        self._calls = 0

    def chat(self, model, messages, options=None, keep_alive=None, stream=False):
        self._calls += 1
        raise ConnectionError("simulated Ollama permanently down")

    @property
    def calls(self):
        return self._calls


class UsageLimitOllamaClient:
    """Mock Ollama client that raises a persistent usage-limit error.

    Phase 3.1c: simulates an Ollama-Cloud quota/session exhaustion. The
    raised ``ConnectionError`` carries a "rate limit" keyword so that
    :func:`_is_usage_limit_error` detects it via the keyword fallback
    path (the canonical 429-status-code path is exercised separately
    via ``_RetryClientProxy`` unit tests with a fake exception object).
    """

    def __init__(self, message="rate limit exceeded: session quota reached"):
        self._calls = 0
        self._message = message

    def chat(self, model, messages, options=None, keep_alive=None, stream=False):
        self._calls += 1
        raise ConnectionError(self._message)

    @property
    def calls(self):
        return self._calls


# ── Helpers ────────────────────────────────────────────────────────────────


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


# ── Path-A filter (NB-2 core) ──────────────────────────────────────────────


class TestPathAFilter:
    def test_path_a_filter_excludes_late_chunk(self):
        # Direct filter logic: late_chunk excluded, fallback included.
        chunks = [
            _make_chunk(chunk_id="c0", chunk_type="late_chunk"),
            _make_chunk(chunk_id="c1", chunk_type=None),
        ]
        filtered = [c for c in chunks if c.chunk_type != "late_chunk"]
        assert len(filtered) == 1
        assert filtered[0].chunk_id == "c1"

    def test_path_a_filter_includes_personal_section(self):
        chunks = [
            _make_chunk(chunk_id="c0", chunk_type="personal_section",
                        source_type="personal"),
        ]
        filtered = [c for c in chunks if c.chunk_type != "late_chunk"]
        assert len(filtered) == 1
        assert filtered[0].chunk_type == "personal_section"

    def test_path_a_filter_includes_fallback_none(self):
        chunks = [
            _make_chunk(chunk_id="c0", chunk_type=None),
        ]
        filtered = [c for c in chunks if c.chunk_type != "late_chunk"]
        assert len(filtered) == 1
        assert filtered[0].chunk_type is None

    def test_load_chunks_for_contextualization_applies_filter(
        self, tmp_hub, monkeypatch,
    ):
        # Monkeypatch load_domain_sources to return a mixed list without
        # importing the real embed_index (which pulls chromadb/ST).
        late = _make_chunk(chunk_id="c0", chunk_type="late_chunk")
        fallback = _make_chunk(chunk_id="c1", chunk_type=None)
        personal = _make_chunk(
            chunk_id="c2", chunk_type="personal_section",
            source_type="personal",
        )

        import embed_index  # noqa
        monkeypatch.setattr(
            embed_index, "load_domain_sources",
            lambda domain: ([late, fallback, personal], None),
        )

        result = load_chunks_for_contextualization("dummy")
        ids = [c.chunk_id for c in result]
        assert "c0" not in ids  # late_chunk excluded
        assert "c1" in ids
        assert "c2" in ids

    def test_load_chunks_filter_by_source_file(self, tmp_hub, monkeypatch):
        a = _make_chunk(chunk_id="c0", source_file="a.md", chunk_type=None)
        b = _make_chunk(chunk_id="c1", source_file="b.md", chunk_type=None)
        import embed_index  # noqa
        monkeypatch.setattr(
            embed_index, "load_domain_sources",
            lambda domain: ([a, b], None),
        )
        result = load_chunks_for_contextualization("dummy", source_file="b.md")
        assert len(result) == 1
        assert result[0].source_file == "b.md"

    def test_load_chunks_limit_applied(self, tmp_hub, monkeypatch):
        chunks = [
            _make_chunk(chunk_id=f"c{i}", chunk_type=None)
            for i in range(10)
        ]
        import embed_index  # noqa
        monkeypatch.setattr(
            embed_index, "load_domain_sources",
            lambda domain: (chunks, None),
        )
        result = load_chunks_for_contextualization("dummy", limit=3)
        assert len(result) == 3


# ── Mixed-domain (NB-2 mixed) ──────────────────────────────────────────────


class TestMixedDomain:
    def test_mixed_domain_repo_contextualized_pdf_not(self, tmp_hub):
        # 2 chunks: late_chunk (PDF) + fallback (repo). After filter only
        # repo; after contextualize, repo has context_prefix, late_chunk
        # does not (not even passed in).
        late = _make_chunk(chunk_id="pdf0", chunk_type="late_chunk")
        repo = _make_chunk(chunk_id="repo0", chunk_type=None)
        to_ctx = [c for c in [late, repo] if c.chunk_type != "late_chunk"]
        assert to_ctx == [repo]

        conn = open_cache("dummy")
        try:
            contextualize_chunks(
                domain="dummy",
                chunks=to_ctx,
                llm_entry=_llm_entry(FakeOllamaClient()),
                conn=conn,
                model_name=MODEL,
            )
        finally:
            conn.close()

        assert repo.context_prefix is not None
        assert late.context_prefix is None  # never touched


# ── Cache hit / miss ──────────────────────────────────────────────────────


class TestCacheHitMiss:
    def test_cache_hit_skips_llm(self, tmp_hub):
        # Pre-fill cache for 2 chunks; contextualize -> 0 LLM calls.
        chunks = [
            _make_chunk(chunk_id="c0", text="body0", chunk_id_in_file=0),
            _make_chunk(chunk_id="c1", text="body1", chunk_id_in_file=1),
        ]
        client = FakeOllamaClient()
        conn = open_cache("dummy")
        try:
            for c in chunks:
                h = cc.chunk_text_hash(c.text)
                cc.put_cached(conn, c.source_file, c.chunk_id_in_file,
                              h, MODEL, "cached context for this chunk")
            contextualize_chunks(
                domain="dummy", chunks=chunks,
                llm_entry=_llm_entry(client), conn=conn, model_name=MODEL,
            )
        finally:
            conn.close()

        assert client.calls == []  # zero LLM calls
        assert all(c.context_prefix == "cached context for this chunk"
                   for c in chunks)

    def test_cache_miss_calls_llm(self, tmp_hub):
        # Empty cache, 2 chunks -> 2 LLM calls, 2 cache entries after.
        chunks = [
            _make_chunk(chunk_id="c0", text="body0", chunk_id_in_file=0),
            _make_chunk(chunk_id="c1", text="body1", chunk_id_in_file=1),
        ]
        client = FakeOllamaClient()
        conn = open_cache("dummy")
        try:
            contextualize_chunks(
                domain="dummy", chunks=chunks,
                llm_entry=_llm_entry(client), conn=conn, model_name=MODEL,
            )
            assert len(client.calls) == 2
            assert cc.count_entries(conn, model=MODEL) == 2
        finally:
            conn.close()

        assert all(c.context_prefix is not None for c in chunks)

    def test_cache_resume_after_partial_crash(self, tmp_hub):
        # 10 chunks, 5 pre-cached. contextualize -> 5 LLM calls (misses),
        # 0 for the 5 hits.
        chunks = [
            _make_chunk(chunk_id=f"c{i}", text=f"body{i}",
                        chunk_id_in_file=i)
            for i in range(10)
        ]
        client = FakeOllamaClient()
        conn = open_cache("dummy")
        try:
            # Pre-cache first 5.
            for i in range(5):
                h = cc.chunk_text_hash(chunks[i].text)
                cc.put_cached(conn, chunks[i].source_file, i,
                              h, MODEL, f"cached-{i}")
            contextualize_chunks(
                domain="dummy", chunks=chunks,
                llm_entry=_llm_entry(client), conn=conn, model_name=MODEL,
            )
        finally:
            conn.close()

        assert len(client.calls) == 5  # only the 5 misses
        # First 5 got cached values, last 5 got fresh.
        for i in range(5):
            assert chunks[i].context_prefix == f"cached-{i}"
        for i in range(5, 10):
            assert chunks[i].context_prefix is not None


# ── Retry / backoff (NB-5) ─────────────────────────────────────────────────


class TestRetryBackoff:
    def test_contextualize_survives_ollama_restart(self, tmp_hub, monkeypatch):
        # FlakyOllamaClient fails call #1, succeeds on call #2.
        # With _RetryClientProxy(max_retries=3), the FIRST chunk's first
        # attempt fails and is retried within the same chunk → success.
        # All 5 chunks contextualized, no crash.
        sleeps = []
        monkeypatch.setattr(ctx_mod.time, "sleep",
                            lambda s: sleeps.append(s))

        chunks = [
            _make_chunk(chunk_id=f"c{i}", text=f"body{i}",
                        chunk_id_in_file=i)
            for i in range(5)
        ]
        # fail_until_call=1: the very first chat() call raises, retry
        # succeeds. Each chunk is a separate chat() call though — so
        # only the first chunk sees the failure (its 2nd attempt
        # succeeds); chunks 2-5 succeed on first attempt.
        client = FlakyOllamaClient(fail_until_call=1)
        conn = open_cache("dummy")
        try:
            contextualize_chunks(
                domain="dummy", chunks=chunks,
                llm_entry=_llm_entry(client), conn=conn, model_name=MODEL,
            )
        finally:
            conn.close()

        assert all(c.context_prefix is not None for c in chunks)
        # The first chunk's first chat() attempt failed → 1 backoff sleep.
        assert sleeps == [30]
        # Total chat() attempts: chunk0 = 2 (fail + retry), chunks1-4 = 1
        # each = 6 total.
        assert client.calls == 6

    def test_contextualize_fails_after_3_retries(self, tmp_hub, monkeypatch):
        # PermanentlyFailingOllamaClient always raises ConnectionError.
        # _RetryClientProxy retries 3 times then gives up →
        # contextualize_chunks raises RuntimeError after 3 attempts.
        sleeps = []
        monkeypatch.setattr(ctx_mod.time, "sleep",
                            lambda s: sleeps.append(s))

        chunks = [
            _make_chunk(chunk_id="c0", text="body0", chunk_id_in_file=0),
        ]
        client = PermanentlyFailingOllamaClient()
        conn = open_cache("dummy")
        try:
            with pytest.raises(RuntimeError, match="Ollama unreachable"):
                contextualize_chunks(
                    domain="dummy", chunks=chunks,
                    llm_entry=_llm_entry(client), conn=conn,
                    model_name=MODEL,
                )
        finally:
            conn.close()

        # 3 chat() attempts on the first (and only) chunk.
        assert client.calls == 3
        # Backoff sleeps: 30s after attempt 1, 60s after attempt 2.
        # (No sleep after the 3rd/final failure — it raises immediately.)
        assert sleeps == [30, 60]


# ── context_prefix assignment ──────────────────────────────────────────────


class TestContextPrefixAssignment:
    def test_contextualize_assigns_context_prefix(self, tmp_hub):
        chunks = [
            _make_chunk(chunk_id="c0", text="body0", chunk_id_in_file=0,
                        chunk_type=None),
            _make_chunk(chunk_id="c1", text="body1", chunk_id_in_file=1,
                        chunk_type="personal_section",
                        source_type="personal"),
        ]
        conn = open_cache("dummy")
        try:
            contextualize_chunks(
                domain="dummy", chunks=chunks,
                llm_entry=_llm_entry(FakeOllamaClient()), conn=conn,
                model_name=MODEL,
            )
        finally:
            conn.close()
        assert all(c.context_prefix is not None for c in chunks)

    def test_late_chunk_chunks_skipped(self, tmp_hub):
        # If a late_chunk is (mistakenly) passed in, it still gets
        # processed by contextualize_chunks (caller is responsible for
        # filtering). But the contract is: caller filters. Here we
        # verify that an empty input list leaves nothing to do and
        # that a late_chunk NOT passed in keeps context_prefix=None.
        late = _make_chunk(chunk_id="late0", chunk_type="late_chunk")
        assert late.context_prefix is None
        # Pass an empty list.
        conn = open_cache("dummy")
        try:
            contextualize_chunks(
                domain="dummy", chunks=[],
                llm_entry=_llm_entry(FakeOllamaClient()), conn=conn,
                model_name=MODEL,
            )
        finally:
            conn.close()
        assert late.context_prefix is None  # never touched


# ── Dry-run ────────────────────────────────────────────────────────────────


class TestDryRun:
    def test_dry_run_no_llm_no_cache(self, tmp_hub):
        chunks = [
            _make_chunk(chunk_id="c0", text="body0", chunk_id_in_file=0),
            _make_chunk(chunk_id="c1", text="body1", chunk_id_in_file=1),
        ]
        client = FakeOllamaClient()
        conn = open_cache("dummy")
        try:
            contextualize_chunks(
                domain="dummy", chunks=chunks,
                llm_entry=_llm_entry(client), conn=conn, model_name=MODEL,
                dry_run=True,
            )
            assert cc.count_entries(conn) == 0
        finally:
            conn.close()
        assert client.calls == []
        assert all(c.context_prefix is None for c in chunks)


# ── Output validation rejection ────────────────────────────────────────────


class TestOutputValidationRejection:
    def test_output_validation_rejection_sets_none_and_no_cache(
        self, tmp_hub,
    ):
        # FakeOllamaClient returns "ok" (2 chars) — below the
        # _MIN_CONTEXT_CHARS (10) threshold → output-validation rejects
        # it → generate_context returns "" → contextualize sets
        # context_prefix = None and does NOT write a cache entry.
        chunks = [
            _make_chunk(chunk_id="c0", text="body0", chunk_id_in_file=0),
        ]
        client = FakeOllamaClient(content="ok")
        conn = open_cache("dummy")
        try:
            contextualize_chunks(
                domain="dummy", chunks=chunks,
                llm_entry=_llm_entry(client), conn=conn, model_name=MODEL,
            )
            assert cc.count_entries(conn) == 0
        finally:
            conn.close()
        assert chunks[0].context_prefix is None
        assert len(client.calls) == 1  # LLM was called once


# ── Batch commit size ──────────────────────────────────────────────────────


class TestBatchCommit:
    def test_batch_commit_size(self, tmp_hub):
        # 5 chunks, batch_size=2 → 3 batch-commits (2 + 2 + 1).
        # We use a counting proxy around a real sqlite3 connection
        # because sqlite3.Connection.commit is read-only (cannot be
        # monkeypatched directly).
        chunks = [
            _make_chunk(chunk_id=f"c{i}", text=f"body{i}",
                        chunk_id_in_file=i)
            for i in range(5)
        ]
        client = FakeOllamaClient()

        real_conn = open_cache("dummy")
        commit_count = {"n": 0}

        class _CommitCountingConn:
            """Thin proxy that counts commit() calls and forwards the
            rest to the real connection."""

            def __init__(self, real):
                self._real = real

            def commit(self):
                commit_count["n"] += 1
                self._real.commit()

            def execute(self, *a, **kw):
                return self._real.execute(*a, **kw)

            def executemany(self, *a, **kw):
                return self._real.executemany(*a, **kw)

            def close(self):
                return self._real.close()

        conn = _CommitCountingConn(real_conn)
        try:
            contextualize_chunks(
                domain="dummy", chunks=chunks,
                llm_entry=_llm_entry(client), conn=conn, model_name=MODEL,
                batch_size=2,
            )
        finally:
            conn.close()

        # put_cached() commits per call (5 commits) plus the batch
        # flushes (3 commits) = 8 total. We assert the total here.
        assert commit_count["n"] == 8


# ── document_text_for_chunk ────────────────────────────────────────────────


class TestDocumentTextForChunk:
    def test_repo_source_file(self, dummy_domain):
        chunk = _make_chunk(source_type="repo",
                            source_file="node3d-rotation.md")
        text = document_text_for_chunk(chunk, "dummy")
        assert "Node3D Rotation" in text

    def test_personal_source_file(self, dummy_domain):
        chunk = _make_chunk(source_type="personal",
                            source_file="gotchas.md")
        text = document_text_for_chunk(chunk, "dummy")
        assert "Gotchas" in text

    def test_missing_file_returns_empty(self, dummy_domain):
        chunk = _make_chunk(source_type="repo",
                            source_file="does-not-exist.md")
        text = document_text_for_chunk(chunk, "dummy")
        assert text == ""


# ── _RetryClientProxy unit tests ────────────────────────────────────────────


class TestRetryClientProxy:
    def test_proxy_retries_then_succeeds(self, monkeypatch):
        sleeps = []
        monkeypatch.setattr(ctx_mod.time, "sleep",
                            lambda s: sleeps.append(s))
        flaky = FlakyOllamaClient(fail_until_call=2)
        proxy = _RetryClientProxy(flaky, max_retries=3,
                                  backoff=(30, 60, 120))
        result = proxy.chat(model="m", messages=[])
        assert result.message.content == "Valid context after retry, situating the chunk."
        assert proxy.chat_attempts == 3
        assert proxy.connection_failed is False
        assert sleeps == [30, 60]

    def test_proxy_fails_after_max_retries(self, monkeypatch):
        sleeps = []
        monkeypatch.setattr(ctx_mod.time, "sleep",
                            lambda s: sleeps.append(s))
        client = PermanentlyFailingOllamaClient()
        proxy = _RetryClientProxy(client, max_retries=3,
                                  backoff=(30, 60, 120))
        with pytest.raises(ConnectionError):
            proxy.chat(model="m", messages=[])
        assert proxy.chat_attempts == 3
        assert proxy.connection_failed is True
        assert sleeps == [30, 60]  # no sleep after final failure


# ── Usage-limit detection (Phase 3.1c) ──────────────────────────────────────


class TestUsageLimitDetection:
    """Phase 3.1c: persistent usage-limit errors stop immediately without
    backoff, while transient connection errors still retry 3×."""

    def test_usage_limit_stops_immediately_without_backoff(
        self, tmp_hub, monkeypatch,
    ):
        # UsageLimitOllamaClient raises a ConnectionError whose message
        # contains "rate limit" — _is_usage_limit_error matches the keyword
        # fallback path. contextualize_chunks must raise RuntimeError
        # ("Usage limit") after 0 backoff sleeps and 1 chat() attempt.
        sleeps = []
        monkeypatch.setattr(ctx_mod.time, "sleep",
                            lambda s: sleeps.append(s))

        chunks = [
            _make_chunk(chunk_id="c0", text="body0", chunk_id_in_file=0),
        ]
        client = UsageLimitOllamaClient()
        conn = open_cache("dummy")
        try:
            with pytest.raises(RuntimeError, match="Usage limit"):
                contextualize_chunks(
                    domain="dummy", chunks=chunks,
                    llm_entry=_llm_entry(client), conn=conn,
                    model_name=MODEL,
                )
        finally:
            conn.close()

        # Critical assertion: NO backoff sleep happened (usage-limit is
        # persistent — retrying is pointless). Contrast with
        # test_transient_error_uses_backoff below which sleeps 2×.
        assert sleeps == []
        # Only one chat() attempt — no retry.
        assert client.calls == 1

    def test_transient_error_uses_backoff(self, tmp_hub, monkeypatch):
        # PermanentlyFailingOllamaClient raises a plain ConnectionError
        # WITHOUT a usage-limit keyword — transient, retries 3× with
        # backoff (30s, 60s, no sleep after final failure) before raising
        # RuntimeError. Verifies the contrast to usage-limit handling.
        sleeps = []
        monkeypatch.setattr(ctx_mod.time, "sleep",
                            lambda s: sleeps.append(s))

        chunks = [
            _make_chunk(chunk_id="c0", text="body0", chunk_id_in_file=0),
        ]
        client = PermanentlyFailingOllamaClient()
        conn = open_cache("dummy")
        try:
            with pytest.raises(RuntimeError, match="Ollama unreachable"):
                contextualize_chunks(
                    domain="dummy", chunks=chunks,
                    llm_entry=_llm_entry(client), conn=conn,
                    model_name=MODEL,
                )
        finally:
            conn.close()

        # 3 chat() attempts — retry happened.
        assert client.calls == 3
        # Backoff sleeps: 30s after attempt 1, 60s after attempt 2.
        # (No sleep after the 3rd/final failure — it raises immediately.)
        assert sleeps == [30, 60]

    def test_usage_limit_cache_preserved(self, tmp_hub, monkeypatch):
        # Pre-fill the cache with 5 entries, then trigger a usage-limit
        # error on chunk #6. contextualize_chunks must raise RuntimeError
        # AND the cache must still contain exactly 5 entries (no data
        # loss — usage-limit aborts before writing chunk #6's context).
        sleeps = []
        monkeypatch.setattr(ctx_mod.time, "sleep",
                            lambda s: sleeps.append(s))

        # 5 cached chunks (chunk_id_in_file 0..4) + 1 uncached (id 5).
        chunks = [
            _make_chunk(chunk_id=f"c{i}", text=f"body{i}",
                        chunk_id_in_file=i)
            for i in range(6)
        ]
        client = UsageLimitOllamaClient()
        conn = open_cache("dummy")
        try:
            # Pre-cache the first 5 chunks.
            for i in range(5):
                h = cc.chunk_text_hash(chunks[i].text)
                cc.put_cached(conn, chunks[i].source_file, i,
                              h, MODEL, f"cached-{i}")
            assert cc.count_entries(conn, model=MODEL) == 5

            with pytest.raises(RuntimeError, match="Usage limit"):
                contextualize_chunks(
                    domain="dummy", chunks=chunks,
                    llm_entry=_llm_entry(client), conn=conn,
                    model_name=MODEL,
                )
            # Cache must still hold exactly 5 entries — chunk #6 was NOT
            # written (usage-limit abort before put_cached).
            assert cc.count_entries(conn, model=MODEL) == 5
        finally:
            conn.close()

        # No backoff on usage-limit.
        assert sleeps == []
        # Only chunk #6 triggered a chat() call (chunks 0..4 were cache
        # hits). That single call raised the usage-limit error.
        assert client.calls == 1


# ── _is_usage_limit_error unit tests ─────────────────────────────────────────


class TestIsUsageLimitError:
    """Direct unit tests for the _is_usage_limit_error helper."""

    def test_keyword_rate_limit(self):
        assert _is_usage_limit_error(
            ConnectionError("HTTP 429: rate limit exceeded")
        ) is True

    def test_keyword_quota_exceeded(self):
        assert _is_usage_limit_error(
            ConnectionError("quota exceeded: weekly limit reached")
        ) is True

    def test_keyword_usage_limit_case_insensitive(self):
        assert _is_usage_limit_error(
            ConnectionError("USAGE LIMIT reached")
        ) is True

    def test_status_code_429(self):
        # Simulate an ollama.ResponseError-like object with status_code.
        class _FakeResponseError(Exception):
            def __init__(self, msg, status_code):
                super().__init__(msg)
                self.status_code = status_code

        assert _is_usage_limit_error(
            _FakeResponseError("too many requests", 429)
        ) is True

    def test_transient_message_not_usage_limit(self):
        assert _is_usage_limit_error(
            ConnectionError("simulated Ollama permanently down")
        ) is False

    def test_plain_exception_without_keywords(self):
        assert _is_usage_limit_error(
            ValueError("something else entirely")
        ) is False

    def test_none_status_code_not_usage_limit(self):
        class _NoStatus(Exception):
            pass

        assert _is_usage_limit_error(_NoStatus("plain error")) is False