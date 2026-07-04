#!/usr/bin/env python3
"""Contextualize chunks for a domain (Phase 3.1b, Task 7 / Phase D).

CLI script that loads the chunks of a domain, generates an LLM-based
``context_prefix`` for every Path-A chunk (``chunk_type != "late_chunk"``
— Spec N1, pure chunk_type-based, NO domain / source_types check),
persists the contexts in the per-domain SQLite cache
(:mod:`context_cache`) and sets ``chunk.context_prefix`` on the returned
``Chunk`` objects.

The script is **resume-friendly**: on a re-run, cached chunks are read
back from the SQLite DB and the LLM is only called for misses. The
script does NOT persist anything to ChromaDB — that remains the job of
``embed_index.py`` (run separately after contextualization).

Retry / backoff (NB-7): transient Ollama connection errors are retried
with exponential backoff (30 s / 60 s / 120 s). After 3 consecutive
failures the run aborts with ``RuntimeError`` — the cache keeps all
already-written entries, so a later re-run resumes from where it died.

Usage::

    python scripts/contextualize_chunks.py --domain godot
    python scripts/contextualize_chunks.py --domain godot --limit 50 --dry-run
    python scripts/contextualize_chunks.py --domain godot --source-file foo-packed.md
    python scripts/contextualize_chunks.py --domain godot --batch-size 100
    python scripts/contextualize_chunks.py --domain godot --workers 3  # Phase 3.3a

Phase 3.3a parallelism: ``--workers N`` (or ``KH_LLM_WORKERS`` env var)
dispatches cache misses to a ``ThreadPoolExecutor`` so multiple LLM
calls run concurrently. Default ``1`` preserves the original sequential
loop (backward-compat). SQLite writes are serialised via a
``threading.Lock``; a shared ``cancel_event`` propagates HTTP 429
usage-limit aborts to every in-flight worker.

No real Ollama / GPU / embedding model is loaded by this module on
import — ``get_llm()`` and ``load_domain_sources()`` are called lazily
inside functions, so the module is safe to import in unit tests (tests
inject a fake ``llm_entry`` and a tmp-path ``conn``).
"""

from __future__ import annotations

import argparse
import os
import re
import sqlite3
import sys
import threading
import time
import concurrent.futures
from pathlib import Path

# Make the repo root importable when run as a script.
_PKG_ROOT = Path(__file__).resolve().parent.parent
if str(_PKG_ROOT) not in sys.path:
    sys.path.insert(0, str(_PKG_ROOT))

from context_cache import (
    chunk_text_hash,
    get_cached,
    open_cache,
    put_cached,
)
from model_manager import DEFAULT_LLM_MODEL, generate_context, get_llm
from parser_base import Chunk

# ── Constants ──────────────────────────────────────────────────────────────

# Exponential backoff schedule (NB-7): 30 s, 60 s, 120 s between retries.
_RETRY_BACKOFF_SECONDS = (30, 60, 120)
_MAX_RETRIES = 3

# Phase 3.3a: default number of parallel LLM workers. ``1`` preserves the
# original sequential behaviour (backward-compat). Override via the
# ``--workers`` CLI flag or the ``KH_LLM_WORKERS`` env var (e.g. 3 for
# Ollama-Cloud Pro concurrency).
_DEFAULT_LLM_WORKERS = 1

# Domain name validation (must match `^[a-z0-9_]+$`).
_DOMAIN_NAME_RE = re.compile(r"^[a-z0-9_]+$")

# Keywords that indicate a persistent Ollama-Cloud usage-limit error (Phase
# 3.1c). Such errors are NOT transient — retrying with backoff wastes 30+60+120s
# for zero benefit. Matched case-insensitively against the exception message.
_USAGE_LIMIT_KEYWORDS = ("rate limit", "quota exceeded", "usage limit")
# HTTP 429 Too Many Requests — the canonical usage-limit status code.
_USAGE_LIMIT_STATUS_CODE = 429


# ── Helpers ────────────────────────────────────────────────────────────────


def _domain_dir(domain: str) -> Path:
    """Resolve the domain directory via the live config module.

    Uses ``sys.modules`` lookup so tests that monkeypatch
    ``config.DOMAINS_DIR`` (via the ``tmp_hub`` fixture) get the patched
    value, mirroring the pattern in :mod:`context_cache` /
    :mod:`model_manager`.
    """
    import sys as _sys

    _config_mod = (
        _sys.modules.get("mcp_servers.knowledge_hub.config")
        or _sys.modules.get("config")
    )
    if _config_mod is None:
        from mcp_servers.knowledge_hub import config as _config_mod  # noqa
    return Path(_config_mod.DOMAINS_DIR) / domain


def document_text_for_chunk(chunk: Chunk, domain: str) -> str:
    """Load the original source document text for a chunk.

    Repo chunks resolve to ``domains/<domain>/sources/<source_file>``,
    personal chunks to ``domains/<domain>/personal/<source_file>``. If
    the file cannot be read, an empty string is returned (the LLM will
    still be called but with no document context — better than crashing
    the whole batch).

    Args:
        chunk: The chunk to load the document for.
        domain: Domain name (used to resolve the directory).

    Returns:
        The full source document text, or ``""`` on read failure.
    """
    base = _domain_dir(domain)
    if chunk.source_type == "personal":
        path = base / "personal" / chunk.source_file
    else:
        path = base / "sources" / chunk.source_file
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, FileNotFoundError) as e:
        print(
            f"[WARN]  Could not read source document {path}: "
            f"{type(e).__name__}: {e} — using empty document_text"
        )
        return ""


def load_chunks_for_contextualization(
    domain: str,
    limit: int | None = None,
    source_file: str | None = None,
) -> list[Chunk]:
    """Load and filter the chunks of a domain for Path-A contextualization.

    Lazy-imports :func:`embed_index.load_domain_sources` *inside* the
    function body so that unit tests can monkeypatch the import without
    triggering a real ``embed_index`` import (which pulls in
    ``sentence_transformers`` / ``chromadb``).

    Path-A filter (Spec N1): ``chunk_type != "late_chunk"`` — pure
    chunk_type-based, no domain / source_types check. This means a
    mixed PDF+repo domain contextualizes its repo chunks while leaving
    the PDF late-chunks untouched (NB-2 mixed-domain support).

    Args:
        domain: Domain name (``^[a-z0-9_]+$``).
        limit: Optional cap on the number of chunks returned (after
            filtering). Useful for spot-checks / tests.
        source_file: Optional filter — only chunks whose ``source_file``
            matches are returned.

    Returns:
        Filtered list of chunks (Path-A only). The original
        ``precomputed_embeddings`` from ``load_domain_sources`` is
        discarded — this script does not need it.
    """
    # Lazy import so tests can monkeypatch `embed_index.load_domain_sources`.
    import embed_index  # noqa: WPS433 (intentional lazy import)

    chunks, _precomputed = embed_index.load_domain_sources(domain)

    # Path-A filter (Spec N1): exclude late_chunk only.
    filtered = [c for c in chunks if c.chunk_type != "late_chunk"]

    if source_file is not None:
        filtered = [c for c in filtered if c.source_file == source_file]

    if limit is not None:
        filtered = filtered[:limit]

    return filtered


def check_ollama_available(llm_entry: dict) -> None:
    """Verify that the Ollama service is reachable and the model is loaded.

    Calls ``client.list()`` (Ollama 0.x) and checks that the configured
    model is present. Raises :class:`RuntimeError` with a clear,
    actionable message if the service is down or the model is missing.

    Args:
        llm_entry: Entry returned by :func:`model_manager.get_llm`
            (``{"client", "model", "backend"}`` for the ollama backend).

    Raises:
        RuntimeError: If the Ollama service is unreachable or the
            configured model is not available.
    """
    if llm_entry.get("backend") != "ollama":
        # Non-ollama backends (e.g. llama-cpp) are not ping-checked here
        # — they load the model lazily on the first call. Skip.
        return
    client = llm_entry["client"]
    model = llm_entry["model"]
    try:
        info = client.list()
    except Exception as e:
        raise RuntimeError(
            "Ollama not running or model not available. "
            f"Start: brew services start ollama && ollama pull {model}. "
            f"Error: {type(e).__name__}: {e}"
        ) from e

    # Ollama 0.6+ returns a ListResponse with .models; older versions
    # return a dict {"models": [...]}. Tolerate both.
    models = []
    try:
        models = [m.model for m in info.models] if info.models else []
    except AttributeError:
        try:
            models = [m.get("name") or m.get("model")
                      for m in info.get("models", [])]
        except Exception:
            models = []

    if model not in models:
        # Some Ollama versions report model names with a :latest suffix.
        # Accept a suffix match as a fallback so we don't false-negative.
        if not any(m == model or m.startswith(model + ":") for m in models):
            raise RuntimeError(
                f"Model '{model}' not available in Ollama. "
                f"Pull it: ollama pull {model}. "
                f"Available models: {models}"
            )


# ── Core loop ──────────────────────────────────────────────────────────────


def _transient_error_types() -> tuple[type[BaseException], ...]:
    """Return the tuple of transient connection-error types we retry on.

    Lazily imports ``httpx.ConnectError`` and ``ollama.ResponseError`` so
    a missing optional dependency does not break module import.
    """
    types: tuple[type[BaseException], ...] = (ConnectionError,)
    try:
        import httpx as _httpx  # type: ignore
        types = types + (_httpx.ConnectError,)
    except ImportError:
        pass
    try:
        import ollama as _ollama  # type: ignore
        types = types + (_ollama.ResponseError,)
    except (ImportError, AttributeError):
        pass
    return types


def _is_usage_limit_error(exc: BaseException) -> bool:
    """Detect a persistent Ollama-Cloud usage-limit error (Phase 3.1c).

    Ollama-Cloud returns a persistent usage-limit error when the session
    or weekly quota is exhausted. Such errors are NOT transient — retrying
    with exponential backoff only wastes 30+60+120s for zero benefit. This
    helper distinguishes usage-limit errors from transient connection
    errors so the retry loop can stop immediately and preserve the cache
    for a later resume (after `ollama signin` with a fresh account or
    after the quota reset window).

    Detection logic (any one match → True):

    1. ``ollama.ResponseError`` with ``status_code == 429`` (canonical HTTP
       "Too Many Requests"). The ``ollama`` package exposes ``status_code``
       on ``ResponseError``; if the attribute is missing we fall back to (2).
    2. The exception's string representation (``str(exc)``) contains any of
       the keywords in :data:`_USAGE_LIMIT_KEYWORDS` (case-insensitive).

    Args:
        exc: The exception to inspect.

    Returns:
        ``True`` if the exception looks like a persistent usage-limit
        error, ``False`` otherwise (treat as transient / retry).
    """
    # (1) HTTP status code 429 on ollama.ResponseError (if available).
    status_code = getattr(exc, "status_code", None)
    if status_code == _USAGE_LIMIT_STATUS_CODE:
        return True

    # (2) Keyword match on the exception message (case-insensitive). This
    # catches plain ConnectionError / httpx errors that carry a usage-limit
    # message body, as well as ollama.ResponseError without status_code.
    msg = str(exc).lower()
    if any(kw in msg for kw in _USAGE_LIMIT_KEYWORDS):
        return True

    return False


class _UsageLimitError(RuntimeError):
    """Raised when Ollama-Cloud returns a persistent usage-limit error.

    Phase 3.1c: distinguishes a usage-limit error (session/weekly quota
    exhausted) from a transient connection error. The proxy raises this
    *instead* of retrying, so the caller can surface a clear
    "run ``ollama signin``" message and the cache stays intact for resume.
    """


class _RetryClientProxy:
    """Wrap an Ollama client and retry ``chat()`` on transient errors.

    ``generate_context()`` in :mod:`model_manager` catches *all*
    ``Exception`` subclasses and returns ``""`` — so a transient
    ``ConnectionError`` raised inside ``client.chat()`` would be
    silently swallowed and never reach a retry loop. To work around
    that without modifying ``model_manager`` (forbidden in Phase D),
    we wrap the client in this proxy: the proxy retries ``chat()``
    itself, and on permanent failure sets ``connection_failed`` and
    re-raises. ``generate_context`` then catches the re-raised error
    and returns ``""``, and :func:`_generate_with_retry` inspects
    ``connection_failed`` to distinguish a connection failure (→
    ``RuntimeError``, abort the batch) from an output-validation
    rejection (→ ``""``, skip this chunk).

    The proxy also proxies any other attribute access (e.g.
    ``client.list()`` for the startup ping) to the wrapped client.
    """

    def __init__(
        self,
        real_client: object,
        max_retries: int = _MAX_RETRIES,
        backoff: tuple[int, ...] = _RETRY_BACKOFF_SECONDS,
        transient_errors: tuple[type[BaseException], ...] | None = None,
    ) -> None:
        self._real = real_client
        self._max_retries = max_retries
        self._backoff = backoff
        self._transient = transient_errors or _transient_error_types()
        self.connection_failed = False
        self.usage_limit_reached = False
        self.chat_attempts = 0

    def chat(self, *args, **kwargs):
        """Retry ``chat()`` on transient errors with exponential backoff.

        Usage-limit errors (Phase 3.1c) are detected *before* any backoff
        and abort immediately: they are persistent (not transient), so
        retrying would waste 30+60+120s for zero benefit. The proxy sets
        ``connection_failed = True`` and raises a
        :class:`_UsageLimitError` so the caller can surface a clear
        "run ``ollama signin``" message and the cache stays intact for
        resume.
        """
        last_exc: BaseException | None = None
        for attempt in range(self._max_retries):
            self.chat_attempts += 1
            try:
                return self._real.chat(*args, **kwargs)
            except self._transient as e:
                # Phase 3.1c: detect persistent usage-limit errors BEFORE
                # backoff. Stop immediately — no retry, no sleep.
                if _is_usage_limit_error(e):
                    print(
                        f"[ERROR] Ollama usage limit reached "
                        f"(attempt {attempt + 1}): {type(e).__name__}: "
                        f"{e} — stopping immediately (not transient). "
                        f"Run `ollama signin` with a different account, "
                        f"then restart. Cache is preserved for resume."
                    )
                    self.connection_failed = True
                    self.usage_limit_reached = True
                    raise _UsageLimitError(str(e)) from e
                last_exc = e
                if attempt < self._max_retries - 1:
                    delay = self._backoff[attempt]
                    print(
                        f"[WARN]  Ollama chat() failed (attempt "
                        f"{attempt + 1}/{self._max_retries}): "
                        f"{type(e).__name__}: {e} — retrying in {delay}s"
                    )
                    time.sleep(delay)
                else:
                    print(
                        f"[ERROR] Ollama chat() failed after "
                        f"{self._max_retries} attempts: "
                        f"{type(e).__name__}: {e}"
                    )
        self.connection_failed = True
        # Re-raise the last transient error so generate_context()'s
        # ``except Exception`` catches it and returns "" — we then
        # detect via ``connection_failed`` and raise RuntimeError.
        assert last_exc is not None
        raise last_exc

    def __getattr__(self, name):
        # Guard dunder attributes (e.g. ``__getstate__``, ``__setstate__``,
        # ``__deepcopy__``, ``__init_subclass__``) so pickle/copy/doctest
        # probing does not silently forward to the wrapped client and
        # trigger surprising behaviour (Phase 3.1b diff-review Finding M-2).
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)
        return getattr(self._real, name)


def _generate_with_retry(
    llm_entry: dict,
    document_text: str,
    chunk_text: str,
) -> str:
    """Call :func:`generate_context` with exponential-backoff retries.

    Wraps ``llm_entry["client"]`` in a :class:`_RetryClientProxy` so the
    retry happens at the ``chat()`` level (because ``generate_context``
    swallows all exceptions and returns ``""``). After
    :data:`_MAX_RETRIES` consecutive transient failures, raises
    :class:`RuntimeError` so the batch aborts and the cache keeps
    already-written entries for resume.

    Args:
        llm_entry: LLM cache entry from :func:`get_llm`.
        document_text: Full source document text.
        chunk_text: The chunk text to situate.

    Returns:
        The generated (and validated) context string, or ``""`` if the
        LLM returned an invalid / empty response (output-validation
        rejection — caller should set ``context_prefix = None``).

    Raises:
        RuntimeError: After ``_MAX_RETRIES`` consecutive connection
            failures.
    """
    proxy = _RetryClientProxy(llm_entry["client"])
    proxy_entry = dict(llm_entry)
    proxy_entry["client"] = proxy
    ctx = generate_context(proxy_entry, document_text, chunk_text)
    if proxy.connection_failed:
        if proxy.usage_limit_reached:
            raise RuntimeError(
                "Usage limit reached — run `ollama signin` with a "
                "different account, then restart. Cache is preserved "
                "for resume."
            )
        raise RuntimeError(
            f"Ollama unreachable after {_MAX_RETRIES} retries"
        )
    return ctx


def contextualize_chunks(
    domain: str,
    chunks: list[Chunk],
    llm_entry: dict,
    conn: sqlite3.Connection,
    model_name: str,
    batch_size: int = 50,
    dry_run: bool = False,
    workers: int = 1,
) -> list[Chunk]:
    """Contextualize a list of chunks (Path-A filter applied by caller).

    Main loop: for each chunk, look up the SQLite cache; on hit, set
    ``context_prefix`` from the cache; on miss, call the LLM (with
    retry / backoff), validate the output, persist to the cache and set
    ``context_prefix`` on the chunk.

    Phase 3.3a parallelism: when ``workers > 1`` the LLM calls for
    cache misses are dispatched to a :class:`ThreadPoolExecutor` so
    multiple chunks are contextualized concurrently. The cache lookup
    stays sequential (cheap), only the expensive LLM call is
    parallelised. SQLite writes are serialised in the main thread via a
    ``threading.Lock`` and a single ``cancel_event`` propagates a
    usage-limit (HTTP 429) abort to every in-flight worker.

    The function is **dependency-injected** — ``llm_entry`` and ``conn``
    are passed in so unit tests can supply a :class:`FakeOllamaClient`
    and a tmp-path SQLite connection without touching real Ollama or
    ChromaDB.

    Args:
        domain: Domain name (used for ``document_text_for_chunk``).
        chunks: Chunks to contextualize. Caller is expected to have
            already applied the Path-A filter (``chunk_type !=
            "late_chunk"``); this function does not re-filter so it can
            be unit-tested in isolation.
        llm_entry: LLM cache entry from :func:`get_llm` (or a fake entry
            for tests).
        conn: Open SQLite connection from :func:`open_cache`. Must be
            opened with ``check_same_thread=False`` when ``workers > 1``
            (Phase 3.3a — :func:`context_cache.open_cache` does this by
            default now).
        model_name: LLM model name (must match the cache key used in
            ``get_cached`` / ``put_cached``).
        batch_size: Number of chunks after which a ``conn.commit()`` is
            issued. ``put_cached`` already commits per call (for
            atomicity), so the batch commit here is an extra safety
            flush for resilience against long-running batches.
        dry_run: If True, do not call the LLM and do not write to the
            cache. Only log what would happen and leave
            ``context_prefix`` untouched (``None``).
        workers: Number of parallel LLM workers. ``1`` (default) runs
            the original sequential loop (backward-compat). ``> 1``
            dispatches cache misses to a ThreadPoolExecutor.

    Returns:
        The same list of chunks (mutated in place) with
        ``context_prefix`` set on each contextualized chunk. Chunks for
        which the LLM returned an invalid / empty response keep
        ``context_prefix = None`` (no cache entry is written for them).
    """
    stats = {"hits": 0, "misses": 0, "rejected": 0, "errors": 0}
    stats_lock = threading.Lock()
    write_lock = threading.Lock()
    cancel_event = threading.Event()

    if workers < 1:
        workers = 1

    if workers == 1:
        return _contextualize_sequential(
            domain, chunks, llm_entry, conn, model_name,
            batch_size, dry_run, stats,
        )

    # ── Parallel path (workers > 1) ───────────────────────────────────
    processed = 0
    pending_since_last_commit = 0

    # Pre-load document_text per source_file (KV-cache reuse). Loaded
    # lazily on first miss for each file; the lookup itself is
    # best-effort — concurrent reads of ``doc_text_cache`` are safe
    # because Python's GIL serialises dict operations on distinct keys
    # and we only ever insert new keys (no deletion / overwrite).
    doc_text_cache: dict[str, str] = {}

    # Phase 3.3a B2: pre-warm get_llm() so the _model_cache dict is
    # populated before any worker starts. Workers reuse the cached
    # entry (no writes to _model_cache during the pool run → no race).
    # The caller has already called get_llm() in main(); we touch it
    # again here defensively so the function is safe when called
    # directly from tests without the CLI startup path.
    if not dry_run:
        try:
            get_llm()
        except Exception:
            # Tests inject a fake llm_entry; ignore pre-warm failures.
            pass

    # First pass: sequential cache lookup. Collect misses for the pool.
    misses: list[tuple[int, Chunk, str]] = []  # (index, chunk, text_hash)
    for idx, chunk in enumerate(chunks):
        if dry_run:
            continue
        text_hash = chunk_text_hash(chunk.text)
        cached = get_cached(
            conn, chunk.source_file, chunk.chunk_id_in_file,
            text_hash, model_name,
        )
        if cached is not None:
            chunk.context_prefix = cached
            with stats_lock:
                stats["hits"] += 1
        else:
            misses.append((idx, chunk, text_hash))

    if dry_run:
        print(f"[INFO] Dry-run: would contextualize {len(chunks)} chunks")
        return chunks

    print(
        f"[INFO] Parallel contextualize: {len(misses)} LLM misses / "
        f"{len(chunks)} chunks, {workers} workers"
    )

    # Dispatch misses to the pool. Results are collected and written
    # back sequentially after the batch to serialise SQLite writes.
    pending_writes: list[tuple[Chunk, str, str]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        future_to_chunk: dict = {}
        for idx, chunk, text_hash in misses:
            if cancel_event.is_set():
                break
            doc_text = doc_text_cache.get(chunk.source_file)
            if doc_text is None:
                doc_text = document_text_for_chunk(chunk, domain)
                doc_text_cache[chunk.source_file] = doc_text
            fut = pool.submit(
                _generate_with_retry_cancelable,
                llm_entry, doc_text, chunk.text, cancel_event,
            )
            future_to_chunk[fut] = (chunk, text_hash)

        for fut in concurrent.futures.as_completed(future_to_chunk):
            if cancel_event.is_set():
                # Cancel any not-yet-started futures and stop draining.
                for f in future_to_chunk:
                    f.cancel()
                break
            chunk, text_hash = future_to_chunk[fut]
            processed += 1
            try:
                ctx = fut.result()
            except RuntimeError as e:
                if "Usage limit" in str(e):
                    cancel_event.set()
                    print(
                        f"[ERROR] Usage limit reached — cancelling "
                        f"remaining workers. Cache preserved for resume."
                    )
                    # Cancel not-yet-started futures and stop draining.
                    for f in future_to_chunk:
                        f.cancel()
                    break
                # A worker aborted because the cancel_event was set by a
                # sibling that hit the usage limit first. Swallow the
                # cancellation and keep draining (or stop if every
                # remaining future is already cancelled).
                if cancel_event.is_set():
                    continue
                raise
            if ctx == "":
                chunk.context_prefix = None
                with stats_lock:
                    stats["rejected"] += 1
            else:
                chunk.context_prefix = ctx
                pending_writes.append((chunk, text_hash, ctx))
                with stats_lock:
                    stats["misses"] += 1
                    pending_since_last_commit += 1

            # Sequential SQLite writes (serialised by write_lock too).
            if pending_writes:
                with write_lock:
                    for c, th, cv in pending_writes:
                        put_cached(
                            conn, c.source_file, c.chunk_id_in_file,
                            th, model_name, cv,
                        )
                    pending_writes.clear()

            if pending_since_last_commit >= batch_size:
                with write_lock:
                    conn.commit()
                pending_since_last_commit = 0

            if processed % 100 == 0:
                with stats_lock:
                    print(
                        f"[INFO] Contextualized {processed}/{len(misses)} "
                        f"misses ({stats['hits']} cache hits, "
                        f"{stats['misses']} misses, "
                        f"{stats['rejected']} rejected)"
                    )

    # Final flush of any remaining writes.
    if pending_writes:
        with write_lock:
            for c, th, cv in pending_writes:
                put_cached(
                    conn, c.source_file, c.chunk_id_in_file,
                    th, model_name, cv,
                )
            conn.commit()

    print(
        f"[INFO] Done: {len(chunks)} chunks ({stats['hits']} hits, "
        f"{stats['misses']} misses, {stats['rejected']} rejected)"
    )
    return chunks


def _generate_with_retry_cancelable(
    llm_entry: dict,
    document_text: str,
    chunk_text: str,
    cancel_event: threading.Event,
) -> str:
    """Worker-side wrapper that aborts early when ``cancel_event`` is set.

    Phase 3.3a: a usage-limit (HTTP 429) raised by any worker sets the
    shared ``cancel_event``. In-flight workers check the event before
    issuing their LLM call and raise ``RuntimeError`` so the future
    completes and the main thread can observe the cancellation. This
    avoids wasting the full ``_RETRY_BACKOFF_SECONDS`` schedule on
    workers that would also hit the usage limit.
    """
    if cancel_event.is_set():
        raise RuntimeError("Usage limit reached — worker cancelled")
    return _generate_with_retry(llm_entry, document_text, chunk_text)


def _contextualize_sequential(
    domain: str,
    chunks: list[Chunk],
    llm_entry: dict,
    conn: sqlite3.Connection,
    model_name: str,
    batch_size: int,
    dry_run: bool,
    stats: dict,
) -> list[Chunk]:
    """Sequential contextualize loop (workers == 1, backward-compat).

    Factored out of :func:`contextualize_chunks` so the parallel path
    can diverge without touching the well-tested sequential behaviour.
    """
    processed = 0
    commits = 0
    pending_since_last_commit = 0

    # Pre-load document_text per source_file (KV-cache reuse via
    # keep_alive=24h in generate_context).
    doc_text_cache: dict[str, str] = {}

    for chunk in chunks:
        processed += 1

        if dry_run:
            # In dry-run mode: no LLM call, no cache write, just log.
            if processed % 100 == 0 or processed == len(chunks):
                print(
                    f"[INFO] Dry-run: would contextualize {processed}/"
                    f"{len(chunks)} chunks"
                )
            continue

        # Cache lookup.
        text_hash = chunk_text_hash(chunk.text)
        cached = get_cached(
            conn, chunk.source_file, chunk.chunk_id_in_file,
            text_hash, model_name,
        )
        if cached is not None:
            chunk.context_prefix = cached
            stats["hits"] += 1
        else:
            # Cache miss -> call LLM.
            doc_text = doc_text_cache.get(chunk.source_file)
            if doc_text is None:
                doc_text = document_text_for_chunk(chunk, domain)
                doc_text_cache[chunk.source_file] = doc_text

            try:
                ctx = _generate_with_retry(llm_entry, doc_text, chunk.text)
            except RuntimeError:
                # Unreachable after retries — abort the batch, keep
                # already-written cache entries for resume.
                raise

            if ctx == "":
                # Output-validation rejection or LLM error — do NOT
                # cache (so a future re-run can retry) and leave
                # context_prefix = None.
                chunk.context_prefix = None
                stats["rejected"] += 1
            else:
                chunk.context_prefix = ctx
                put_cached(
                    conn, chunk.source_file, chunk.chunk_id_in_file,
                    text_hash, model_name, ctx,
                )
                stats["misses"] += 1
                pending_since_last_commit += 1

        # Batch commit (extra safety flush; put_cached already commits).
        if pending_since_last_commit >= batch_size:
            conn.commit()
            commits += 1
            pending_since_last_commit = 0

        # Progress log every 100 chunks.
        if processed % 100 == 0:
            print(
                f"[INFO] Contextualized {processed}/{len(chunks)} chunks "
                f"({stats['hits']} cache hits, {stats['misses']} misses, "
                f"{stats['rejected']} rejected)"
            )

    # Final flush.
    if pending_since_last_commit > 0 and not dry_run:
        conn.commit()
        commits += 1

    print(
        f"[INFO] Done: {processed}/{len(chunks)} contextualized "
        f"({stats['hits']} hits, {stats['misses']} misses, "
        f"{stats['rejected']} rejected)"
    )
    return chunks


# ── CLI ────────────────────────────────────────────────────────────────────


def _build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="contextualize_chunks",
        description=(
            "Generate LLM context_prefix for Path-A chunks of a domain "
            "(Phase 3.1b). Persists to SQLite cache; does NOT touch ChromaDB."
        ),
    )
    p.add_argument(
        "--domain", required=True,
        help="Domain name (must match ^[a-z0-9_]+$).",
    )
    p.add_argument(
        "--limit", type=int, default=None,
        help="Only process the first N chunks (after filtering).",
    )
    p.add_argument(
        "--dry-run", action="store_true",
        help="No LLM calls, no cache writes; only log what would happen.",
    )
    p.add_argument(
        "--source-file", default=None,
        help="Only process chunks from this source file.",
    )
    p.add_argument(
        "--batch-size", type=int, default=50,
        help="Batch commit size for SQLite (default 50).",
    )
    p.add_argument(
        "--workers", type=int,
        default=int(os.environ.get("KH_LLM_WORKERS", _DEFAULT_LLM_WORKERS)),
        help=(
            "Number of parallel LLM workers (Phase 3.3a). Default 1 = "
            "sequential (backward-compat). Override via KH_LLM_WORKERS env "
            "var. >1 dispatches cache misses to a ThreadPoolExecutor."
        ),
    )
    return p


def main(argv: list[str] | None = None) -> int:
    """CLI entry point.

    Returns the process exit code (0 on success, 1 on startup failure).
    """
    args = _build_arg_parser().parse_args(argv)

    if not _DOMAIN_NAME_RE.match(args.domain):
        print(
            f"[ERROR] Invalid domain name '{args.domain}' — "
            "must match ^[a-z0-9_]+$"
        )
        return 1

    if args.batch_size < 1:
        print("[ERROR] --batch-size must be >= 1")
        return 1

    if args.workers < 1:
        print("[ERROR] --workers must be >= 1")
        return 1

    # ── 0. Phase 3.3a B-R2-3: ensure context_cache.db has a valid schema.
    # Opening the cache (even when dry-run) calls init_schema(), so an
    # empty/stale DB file becomes a valid cache before any promote step.
    try:
        _schema_conn = open_cache(args.domain)
        _schema_conn.close()
    except sqlite3.Error as e:
        print(f"[ERROR] Cache schema init failed: {type(e).__name__}: {e}")
        return 1

    # ── 1. Startup check: Ollama available? ──────────────────────────────
    if not args.dry_run:
        try:
            llm_entry = get_llm()
            check_ollama_available(llm_entry)
        except RuntimeError as e:
            print(f"[ERROR] {e}")
            return 1
        except Exception as e:
            print(
                f"[ERROR] Failed to load LLM: {type(e).__name__}: {e}"
            )
            return 1
        model_name = os.environ.get("KH_LLM_MODEL", DEFAULT_LLM_MODEL)
    else:
        llm_entry = {"client": None, "model": "(dry-run)", "backend": "ollama"}
        model_name = os.environ.get("KH_LLM_MODEL", DEFAULT_LLM_MODEL)

    # ── 2. Load + filter chunks ──────────────────────────────────────────
    chunks = load_chunks_for_contextualization(
        args.domain,
        limit=args.limit,
        source_file=args.source_file,
    )
    late_chunk_count = _count_late_chunks_skipped(args.domain)
    print(
        f"[INFO] Loaded {len(chunks)} Path-A chunks for domain "
        f"'{args.domain}'"
        + (f" (--limit {args.limit})" if args.limit else "")
        + (f" (--source-file {args.source_file})"
           if args.source_file else "")
    )
    if late_chunk_count:
        print(
            f"[INFO] {late_chunk_count} late_chunk chunks skipped "
            "(PDF late-chunking, Spec N1)"
        )

    if not chunks:
        print("[INFO] No chunks to contextualize. Done.")
        return 0

    # ── 3. Open cache ────────────────────────────────────────────────────
    conn = open_cache(args.domain)
    try:
        cached_count = _cached_count_for_model(conn, model_name)
        print(
            f"[INFO] Cache: {cached_count} existing entries for model "
            f"'{model_name}'"
        )

        # ── 4. Contextualize ──────────────────────────────────────────
        contextualize_chunks(
            domain=args.domain,
            chunks=chunks,
            llm_entry=llm_entry,
            conn=conn,
            model_name=model_name,
            batch_size=args.batch_size,
            dry_run=args.dry_run,
            workers=args.workers,
        )
    finally:
        conn.close()

    return 0


def _count_late_chunks_skipped(domain: str) -> int:
    """Count late_chunk chunks for a domain (for the startup log line).

    Best-effort: if ``load_domain_sources`` cannot be called (e.g.
    missing model), returns 0. We re-load the full chunk list here only
    for the informational log; the actual processing list is built
    separately by :func:`load_chunks_for_contextualization`.
    """
    try:
        import embed_index  # noqa
        all_chunks, _ = embed_index.load_domain_sources(domain)
        return sum(1 for c in all_chunks if c.chunk_type == "late_chunk")
    except Exception:
        return 0


def _cached_count_for_model(conn: sqlite3.Connection, model: str) -> int:
    """Count existing cache entries for the active model (startup log)."""
    try:
        from context_cache import count_entries
        return count_entries(conn, model=model)
    except Exception:
        return 0


if __name__ == "__main__":
    sys.exit(main())