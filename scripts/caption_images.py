#!/usr/bin/env python3
"""Caption images for a domain (Vision Retrieval Feature, Task 3).

CLI script that reads ``chromadb_data/<domain>/image_manifest.json``, asks
a Vision-LLM (Gemma 4 via Ollama Cloud) to describe each ``good`` /
``unchecked`` image in the context of the surrounding handbook text, and
persists the context-aware captions in the per-domain SQLite cache
(:mod:`image_caption_cache`).

Context-aware captions (TowardsDataScience best-practice):

.. code-block:: text

   caption = context_before + Vision-LLM description + context_after

The Vision-LLM description is generated from the image + a prompt that
includes the surrounding text context, so similar-looking screenshots
(different Color Page dialogs) get distinguishing captions.

The script is **resume-friendly**: on a re-run, cached images are read
back from the SQLite DB and the LLM is only called for misses. The script
does NOT persist anything to ChromaDB — that remains the job of
``embed_images.py`` (Task 4, run separately after captioning).

Phase 3.3a parallelism: ``--workers N`` (or ``KH_VISION_LLM_WORKERS`` env
var) dispatches cache misses to a ``ThreadPoolExecutor`` so multiple LLM
calls run concurrently. Default ``1`` preserves the original sequential
loop (backward-compat). SQLite writes are serialised via a
``threading.Lock``; a shared ``cancel_event`` propagates a usage-limit
(HTTP 429) abort to every in-flight worker (analog
:func:`contextualize_chunks.contextualize_chunks`).

Usage::

    python scripts/caption_images.py --domain davinci_resolve
    python scripts/caption_images.py --domain davinci_resolve --limit 10
    python scripts/caption_images.py --domain davinci_resolve --workers 3
    KH_LLM_MODEL=gemma4:cloud KH_OLLAMA_HOST=http://localhost:11434 \\
        KH_VISION_LLM_WORKERS=3 python scripts/caption_images.py --domain davinci_resolve

No real Ollama / GPU / embedding model is loaded by this module on import —
``get_llm()`` is called lazily inside ``main()``, so the module is safe to
import in unit tests (tests inject a fake ``llm_entry``).
"""

from __future__ import annotations

import argparse
import base64
import concurrent.futures
import json
import os
import re
import sys as _sys
import threading
import time
from pathlib import Path

# Make the repo root importable when run as a script.
_PKG_ROOT = Path(__file__).resolve().parent.parent
if str(_PKG_ROOT) not in _sys.path:
    _sys.path.insert(0, str(_PKG_ROOT))

from image_caption_cache import (
    get_cached,
    image_hash,
    open_cache,
    put_cached,
    count_entries,
)
from caption_cleaning import clean_caption
from mcp_servers.knowledge_hub import config as _config
from mcp_servers.knowledge_hub.config import domain_image_manifest_path

# ── Constants ──────────────────────────────────────────────────────────────

# Domain name validation (must match `^[a-z0-9_]+$`).
_DOMAIN_NAME_RE = re.compile(r"^[a-z0-9_]+$")

# Default number of parallel Vision-LLM workers. ``1`` preserves the
# original sequential behaviour (backward-compat). Override via the
# ``--workers`` CLI flag or the ``KH_VISION_LLM_WORKERS`` env var (e.g. 3
# for Ollama-Cloud Pro concurrency).
_DEFAULT_VISION_LLM_WORKERS = 1

# Exponential backoff schedule: 30 s, 60 s, 120 s between retries.
_RETRY_BACKOFF_SECONDS = (30, 60, 120)
_MAX_RETRIES = 3

# Keywords that indicate a persistent Ollama-Cloud usage-limit error.
_USAGE_LIMIT_KEYWORDS = ("rate limit", "quota exceeded", "usage limit")
_USAGE_LIMIT_STATUS_CODE = 429

# Max image bytes to base64-encode for the Vision-LLM prompt. 10 MB is a
# safe upper bound for a single PNG screenshot; larger images are likely
# not UI screenshots and would blow up the prompt.
_MAX_IMAGE_BYTES = 10 * 1024 * 1024

# Truncation limits for the context window embedded in the prompt.
_MAX_CONTEXT_CHARS = 500


# ── Helpers ────────────────────────────────────────────────────────────────


def _resolve_image_path(entry: dict) -> Path:
    """Resolve the absolute path of a manifest entry's image."""
    return _config.HUB_ROOT / entry["image_path"]


def _encode_image_b64(image_path: Path) -> str | None:
    """Base64-encode an image for the Ollama vision API.

    Returns ``None`` and logs a warning if the image is too large or
    unreadable.
    """
    try:
        size = image_path.stat().st_size
    except OSError as e:
        print(f"[WARN]  stat failed for {image_path.name}: {e}")
        return None
    if size > _MAX_IMAGE_BYTES:
        print(f"[WARN]  {image_path.name} too large ({size/1024/1024:.1f} MB > "
              f"{_MAX_IMAGE_BYTES/1024/1024:.0f} MB) — skipping")
        return None
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except OSError as e:
        print(f"[WARN]  read failed for {image_path.name}: {e}")
        return None


_IMAGE_REF_RE = re.compile(r"!\[\]\([^)]+\.png\)")


def _clean_context(text: str) -> str:
    """Strip image references and collapse whitespace from context text."""
    if not text:
        return ""
    cleaned = _IMAGE_REF_RE.sub("", text)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def _build_caption_prompt(context_before: str, context_after: str) -> str:
    """Build the Vision-LLM prompt for captioning a DaVinci image.

    The prompt is context-aware (TowardsDataScience best-practice): it
    includes the surrounding handbook text so the LLM can disambiguate
    similar-looking screenshots. Image references (![](path.png)) are
    stripped from the context so they do not leak file paths into the
    prompt.
    """
    cb = _clean_context(context_before)[:_MAX_CONTEXT_CHARS]
    ca = _clean_context(context_after)[:_MAX_CONTEXT_CHARS]
    return (
        "You are a captioning assistant for screenshots from a DaVinci "
        "Resolve handbook. Look at the image and describe what it shows in "
        "1-3 sentences. Focus on: which UI page/panel is visible, which "
        "dialog or tool is open, and what the screenshot illustrates.\n\n"
        f"Surrounding handbook text (for disambiguation):\n"
        f"BEFORE: {cb}\n"
        f"AFTER:  {ca}\n\n"
        "Reply with ONLY the description (no preamble, no 'The image shows'). "
        "Keep it factual and specific so a reader can find this screenshot "
        "by searching for the described UI elements."
    )


def _transient_error_types() -> tuple[type[BaseException], ...]:
    """Return the tuple of transient connection-error types we retry on."""
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
    """Detect a persistent Ollama-Cloud usage-limit error (analog
    :func:`contextualize_chunks._is_usage_limit_error`).
    """
    status_code = getattr(exc, "status_code", None)
    if status_code == _USAGE_LIMIT_STATUS_CODE:
        return True
    msg = str(exc).lower()
    return any(kw in msg for kw in _USAGE_LIMIT_KEYWORDS)


class _UsageLimitError(RuntimeError):
    """Raised when Ollama-Cloud returns a persistent usage-limit error."""


class _RetryClientProxy:
    """Wrap an Ollama client and retry ``chat()`` on transient errors.

    Analog :class:`contextualize_chunks._RetryClientProxy`. The proxy also
    detects persistent usage-limit errors and aborts immediately so the
    cache stays intact for resume.
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

    def chat(self, *args, **kwargs):
        last_exc: BaseException | None = None
        for attempt in range(self._max_retries):
            try:
                return self._real.chat(*args, **kwargs)
            except self._transient as e:
                if _is_usage_limit_error(e):
                    print(
                        f"[ERROR] Ollama usage limit reached "
                        f"(attempt {attempt + 1}): {type(e).__name__}: {e} "
                        f"— stopping immediately. Run `ollama signin` with a "
                        f"different account, then restart. Cache preserved."
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
                        f"{self._max_retries} attempts: {type(e).__name__}: {e}"
                    )
        self.connection_failed = True
        assert last_exc is not None
        raise last_exc

    def __getattr__(self, name):
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)
        return getattr(self._real, name)


# ── Caption generation ────────────────────────────────────────────────────


def _format_eta(seconds: float) -> str:
    """Format seconds as a human-readable duration string.

    ``90`` -> ``"1m 30s"``; ``3700`` -> ``"1h 1m"``.
    """
    if seconds < 0 or not (seconds == seconds):  # NaN check
        return "?"
    s = int(seconds)
    if s < 60:
        return f"{s}s"
    m, s = divmod(s, 60)
    if m < 60:
        return f"{m}m {s}s"
    h, m = divmod(m, 60)
    return f"{h}h {m}m"


def caption_image(
    llm_entry: dict,
    image_path: Path,
    context_before: str,
    context_after: str,
) -> str:
    """Generate a context-aware caption for a single image.

    Returns the Vision-LLM description, or ``""`` on error / invalid output.
    The caller wraps the final caption as
    ``context_before + description + context_after`` (TowardsDataScience
    context-aware best-practice) when persisting to the cache.
    """
    b64 = _encode_image_b64(image_path)
    if b64 is None:
        return ""

    prompt = _build_caption_prompt(context_before, context_after)

    try:
        response = llm_entry["client"].chat(
            model=llm_entry["model"],
            messages=[{
                "role": "user",
                "content": prompt,
                "images": [b64],
            }],
            options={"temperature": 0, "num_predict": 200},
            keep_alive="24h",
            stream=False,
        )
        try:
            raw = response.message.content.strip()
        except AttributeError:
            raw = response["message"]["content"].strip()
    except Exception as e:
        print(f"[WARN]  caption failed for {image_path.name}: "
              f"{type(e).__name__}: {e}")
        return ""

    if not raw:
        return ""
    # Truncate extremely long descriptions to keep captions usable.
    if len(raw) > 1000:
        raw = raw[:1000]
    return raw


def _caption_with_retry(
    llm_entry: dict,
    image_path: Path,
    context_before: str,
    context_after: str,
) -> str:
    """Call :func:`caption_image` with exponential-backoff retries.

    Wraps ``llm_entry["client"]`` in a :class:`_RetryClientProxy` so the
    retry happens at the ``chat()`` level. Raises :class:`RuntimeError` on
    permanent connection failure (caller aborts the batch).
    """
    proxy = _RetryClientProxy(llm_entry["client"])
    proxy_entry = dict(llm_entry)
    proxy_entry["client"] = proxy
    caption = caption_image(proxy_entry, image_path, context_before, context_after)
    if proxy.connection_failed:
        if proxy.usage_limit_reached:
            err = RuntimeError(
                "Usage limit reached — run `ollama signin` with a "
                "different account, then restart. Cache is preserved "
                "for resume."
            )
            err._is_usage_limit = True  # type: ignore[attr-defined]
            raise err
        raise RuntimeError(f"Ollama unreachable after {_MAX_RETRIES} retries")
    return caption


def _caption_with_retry_cancelable(
    llm_entry: dict,
    image_path: Path,
    context_before: str,
    context_after: str,
    cancel_event: threading.Event,
) -> str:
    """Worker-side wrapper that aborts early when ``cancel_event`` is set."""
    if cancel_event.is_set():
        raise RuntimeError("Usage limit reached — worker cancelled")
    return _caption_with_retry(llm_entry, image_path, context_before, context_after)


# ── Core loop ─────────────────────────────────────────────────────────────


def caption_manifest(
    domain: str,
    manifest_entries: list[dict],
    llm_entry: dict,
    conn,
    model_name: str,
    batch_size: int = 50,
    dry_run: bool = False,
    workers: int = 1,
) -> list[dict]:
    """Caption a list of manifest entries.

    For each entry whose ``quality`` is ``"good"`` or ``"unchecked"``, look
    up the SQLite cache; on hit, set ``entry["caption"]`` from the cache; on
    miss, call the Vision-LLM, persist the caption and set ``entry["caption"]``.

    Entries with ``quality == "poor"`` get ``caption = ""`` and are skipped
    (TowardsDataScience: filter logos/illegible early).

    Phase 3.3a parallelism: when ``workers > 1`` the LLM calls for cache
    misses are dispatched to a ``ThreadPoolExecutor``. SQLite writes are
    serialised via a ``threading.Lock``; a shared ``cancel_event`` propagates
    a usage-limit (HTTP 429) abort to every in-flight worker.

    Returns:
        The same list of entries (mutated in place) with a ``"caption"`` key
        set on each captioned entry.
    """
    stats = {"hits": 0, "misses": 0, "skipped_poor": 0, "errors": 0, "missing_file": 0}
    stats_lock = threading.Lock()
    write_lock = threading.Lock()
    cancel_event = threading.Event()

    if workers < 1:
        workers = 1

    # Filter: only caption good + unchecked images. Poor images skip.
    to_caption = []
    for entry in manifest_entries:
        if entry.get("quality") == "poor":
            entry["caption"] = ""
            stats["skipped_poor"] += 1
        else:
            entry["caption"] = ""
            to_caption.append(entry)

    if dry_run:
        print(f"[INFO] Dry-run: would caption {len(to_caption)} images "
              f"({stats['skipped_poor']} poor skipped)")
        return manifest_entries

    print(f"[INFO] Captioning {len(to_caption)} images "
          f"({stats['skipped_poor']} poor skipped), {workers} worker(s)")

    if workers == 1:
        return _caption_sequential(
            domain, to_caption, llm_entry, conn, model_name,
            batch_size, stats,
        )

    # ── Parallel path (workers > 1) ───────────────────────────────────
    t_loop_start = time.time()
    processed = 0
    pending_since_last_commit = 0
    pending_writes: list[tuple[dict, str, str]] = []  # (entry, img_hash, caption)

    # First pass: sequential cache lookup. Collect misses for the pool.
    misses: list[tuple[int, dict, str]] = []  # (idx, entry, img_hash)
    for idx, entry in enumerate(to_caption):
        image_path = _resolve_image_path(entry)
        if not image_path.exists():
            print(f"[WARN]  Image file missing: {entry['image_path']} — skipping")
            stats["missing_file"] += 1
            continue
        try:
            img_hash = image_hash(image_path)
        except OSError as e:
            print(f"[WARN]  hash failed for {image_path.name}: {e} — skipping")
            stats["errors"] += 1
            continue
        cached = get_cached(conn, entry["image_id"], img_hash, model_name)
        if cached is not None:
            entry["caption"] = cached
            with stats_lock:
                stats["hits"] += 1
        else:
            misses.append((idx, entry, img_hash))

    print(f"[INFO] Parallel caption: {len(misses)} LLM misses / "
          f"{len(to_caption)} images, {workers} workers")

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        future_to_entry: dict = {}
        for idx, entry, img_hash in misses:
            if cancel_event.is_set():
                break
            image_path = _resolve_image_path(entry)
            fut = pool.submit(
                _caption_with_retry_cancelable,
                llm_entry, image_path,
                entry.get("context_before", ""),
                entry.get("context_after", ""),
                cancel_event,
            )
            future_to_entry[fut] = (entry, img_hash)

        for fut in concurrent.futures.as_completed(future_to_entry):
            if cancel_event.is_set():
                for f in future_to_entry:
                    f.cancel()
                break
            entry, img_hash = future_to_entry[fut]
            processed += 1
            try:
                description = fut.result()
            except RuntimeError as e:
                is_usage_limit = getattr(e, "_is_usage_limit", False)
                if not is_usage_limit and "Usage limit" in str(e):
                    is_usage_limit = True
                if is_usage_limit:
                    cancel_event.set()
                    print(f"[ERROR] Usage limit reached — cancelling workers. "
                          f"Cache preserved for resume.")
                    for f in future_to_entry:
                        f.cancel()
                    if pending_writes:
                        with write_lock:
                            for ent, ih, cap in pending_writes:
                                put_cached(conn, ent["image_id"], ih, model_name, cap)
                            conn.commit()
                        pending_writes.clear()
                    break
                if cancel_event.is_set():
                    continue
                raise
            if description == "":
                entry["caption"] = ""
                with stats_lock:
                    stats["errors"] += 1
            else:
                # Context-aware caption: context_before + description + context_after.
                cb = _clean_context(entry.get("context_before", ""))
                ca = _clean_context(entry.get("context_after", ""))
                full_caption = clean_caption(f"{cb} [IMAGE: {description}] {ca}".strip())
                entry["caption"] = full_caption
                pending_writes.append((entry, img_hash, full_caption))
                with stats_lock:
                    stats["misses"] += 1
                    pending_since_last_commit += 1

            if pending_writes:
                with write_lock:
                    for ent, ih, cap in pending_writes:
                        put_cached(conn, ent["image_id"], ih, model_name, cap)
                    pending_writes.clear()

            if pending_since_last_commit >= batch_size:
                with write_lock:
                    conn.commit()
                pending_since_last_commit = 0

            if processed % 25 == 0 or processed == len(misses):
                elapsed = time.time() - t_loop_start
                rate = processed / elapsed if elapsed > 0 else 0
                remaining = len(misses) - processed
                eta_sec = remaining / rate if rate > 0 else 0
                eta_str = _format_eta(eta_sec)
                elapsed_str = _format_eta(elapsed)
                with stats_lock:
                    print(f"[INFO] [{elapsed_str} elapsed, ETA {eta_str}] "
                          f"Captioned {processed}/{len(misses)} misses "
                          f"({stats['hits']} hits, {stats['misses']} misses, "
                          f"{stats['errors']} errors, {rate:.1f} img/s)")

    # Final flush.
    if pending_writes:
        with write_lock:
            for ent, ih, cap in pending_writes:
                put_cached(conn, ent["image_id"], ih, model_name, cap)
            conn.commit()

    elapsed = time.time() - t_loop_start
    elapsed_str = _format_eta(elapsed)
    print(f"[INFO] Done in {elapsed_str}: {stats['hits']} hits, "
          f"{stats['misses']} misses, {stats['errors']} errors, "
          f"{stats['skipped_poor']} poor skipped, "
          f"{stats['missing_file']} missing files")
    return manifest_entries


def _caption_sequential(
    domain: str,
    to_caption: list[dict],
    llm_entry: dict,
    conn,
    model_name: str,
    batch_size: int,
    stats: dict,
) -> list[dict]:
    """Sequential caption loop (workers == 1, backward-compat)."""
    processed = 0
    pending_since_last_commit = 0

    t_loop_start = time.time()
    for entry in to_caption:
        processed += 1
        image_path = _resolve_image_path(entry)
        if not image_path.exists():
            print(f"[WARN]  Image file missing: {entry['image_path']} — skipping")
            stats["missing_file"] += 1
            continue
        try:
            img_hash = image_hash(image_path)
        except OSError as e:
            print(f"[WARN]  hash failed for {image_path.name}: {e} — skipping")
            stats["errors"] += 1
            continue

        cached = get_cached(conn, entry["image_id"], img_hash, model_name)
        if cached is not None:
            entry["caption"] = cached
            stats["hits"] += 1
        else:
            try:
                description = _caption_with_retry(
                    llm_entry, image_path,
                    entry.get("context_before", ""),
                    entry.get("context_after", ""),
                )
            except RuntimeError:
                raise
            if description == "":
                entry["caption"] = ""
                stats["errors"] += 1
            else:
                cb = _clean_context(entry.get("context_before", ""))
                ca = _clean_context(entry.get("context_after", ""))
                full_caption = clean_caption(f"{cb} [IMAGE: {description}] {ca}".strip())
                entry["caption"] = full_caption
                put_cached(conn, entry["image_id"], img_hash, model_name, full_caption)
                stats["misses"] += 1
                pending_since_last_commit += 1

        if pending_since_last_commit >= batch_size:
            conn.commit()
            pending_since_last_commit = 0

        if processed % 10 == 0 or processed == len(to_caption):
            elapsed = time.time() - t_loop_start
            rate = processed / elapsed if elapsed > 0 else 0
            remaining = len(to_caption) - processed
            eta_sec = remaining / rate if rate > 0 else 0
            eta_str = _format_eta(eta_sec)
            elapsed_str = _format_eta(elapsed)
            print(f"[INFO] [{elapsed_str} elapsed, ETA {eta_str}] "
                  f"Captioned {processed}/{len(to_caption)} images "
                  f"({stats['hits']} hits, {stats['misses']} misses, "
                  f"{stats['errors']} errors, {rate:.1f} img/s)")

    if pending_since_last_commit > 0:
        conn.commit()

    elapsed = time.time() - t_loop_start
    elapsed_str = _format_eta(elapsed)
    print(f"[INFO] Done in {elapsed_str}: {stats['hits']} hits, "
          f"{stats['misses']} misses, {stats['errors']} errors, "
          f"{stats['skipped_poor']} poor skipped, "
          f"{stats['missing_file']} missing files")
    return to_caption


# ── Manifest I/O ───────────────────────────────────────────────────────────


def load_manifest(domain: str) -> list[dict]:
    """Load ``image_manifest.json`` for a domain.

    Raises :class:`FileNotFoundError` if the manifest does not exist
    (caller should run ``extract_pdf_images.py`` first).
    """
    path = domain_image_manifest_path(domain)
    if not path.exists():
        raise FileNotFoundError(
            f"Image manifest not found for domain '{domain}': {path}. "
            f"Run: python scripts/extract_pdf_images.py --domain {domain}"
        )
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("images", [])


# ── CLI ────────────────────────────────────────────────────────────────────


def _build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="caption_images",
        description=(
            "Caption images for a domain via Vision-LLM (Vision Retrieval "
            "Feature, Task 3). Persists to SQLite cache; does NOT touch ChromaDB."
        ),
    )
    p.add_argument(
        "--domain", required=True,
        help="Domain name (must match ^[a-z0-9_]+$).",
    )
    p.add_argument(
        "--limit", type=int, default=None,
        help="Only process the first N images (after quality filter).",
    )
    p.add_argument(
        "--dry-run", action="store_true",
        help="No LLM calls, no cache writes; only log what would happen.",
    )
    p.add_argument(
        "--batch-size", type=int, default=50,
        help="Batch commit size for SQLite (default 50).",
    )
    p.add_argument(
        "--workers", type=int,
        default=int(os.environ.get("KH_VISION_LLM_WORKERS", _DEFAULT_VISION_LLM_WORKERS)),
        help=(
            "Number of parallel Vision-LLM workers. Default 1 = sequential. "
            "Override via KH_VISION_LLM_WORKERS env var. >1 dispatches cache "
            "misses to a ThreadPoolExecutor."
        ),
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_arg_parser().parse_args(argv)

    if not _DOMAIN_NAME_RE.match(args.domain):
        print(f"[ERROR] Invalid domain name '{args.domain}' — "
              "must match ^[a-z0-9_]+$")
        return 1
    if args.batch_size < 1:
        print("[ERROR] --batch-size must be >= 1")
        return 1
    if args.workers < 1:
        print("[ERROR] --workers must be >= 1")
        return 1

    # Load manifest.
    try:
        manifest_entries = load_manifest(args.domain)
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        return 1

    if args.limit is not None:
        manifest_entries = manifest_entries[:args.limit]

    if not manifest_entries:
        print("[INFO] No images in manifest. Done.")
        return 0

    # Startup check: Ollama available?
    if not args.dry_run:
        try:
            from model_manager import get_llm, DEFAULT_LLM_MODEL
            from contextualize_chunks import check_ollama_available
            llm_entry = get_llm()
            check_ollama_available(llm_entry)
        except RuntimeError as e:
            print(f"[ERROR] {e}")
            return 1
        except Exception as e:
            print(f"[ERROR] Failed to load LLM: {type(e).__name__}: {e}")
            return 1
        model_name = os.environ.get("KH_LLM_MODEL", DEFAULT_LLM_MODEL)
    else:
        from model_manager import DEFAULT_LLM_MODEL
        llm_entry = {"client": None, "model": "(dry-run)", "backend": "ollama"}
        model_name = os.environ.get("KH_LLM_MODEL", DEFAULT_LLM_MODEL)

    # Open cache.
    conn = open_cache(args.domain)
    try:
        cached_count = count_entries(conn, model=model_name)
        print(f"[INFO] Cache: {cached_count} existing entries for model "
              f"'{model_name}'")

        caption_manifest(
            domain=args.domain,
            manifest_entries=manifest_entries,
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


if __name__ == "__main__":
    _sys.exit(main())
