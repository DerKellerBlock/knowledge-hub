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

# Phase 3.1 Contextual Retrieval — local LLM defaults.
# Read LIVE from KH_LLM_MODEL / KH_LLM_BACKEND in get_llm() on every
# cache-miss, analog to get_embedder()/get_reranker().
DEFAULT_LLM_MODEL = "gemma4:12b-mlx"
DEFAULT_LLM_BACKEND = "ollama"  # "ollama" | "llama-cpp"

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

    Device selection: ``device='cpu'`` is forced. ``BAAI/bge-m3`` ships
    custom code via ``trust_remote_code`` which deadlocks on Apple
    Silicon MPS with ``transformers`` 4.57.6 — ``encode()`` never returns,
    no error, no progress. CPU is sufficient for batch embedding
    (bs=32 short / bs=1 long via ``_encode_robust``). Fixed 2026-07-02.
    """
    cfg = get_domain_config(domain)
    model_name = os.environ.get("KH_EMBEDDING_MODEL", cfg["embedding_model"])
    key = f"embedder:{model_name}"
    if key not in _model_cache:
        # Force CPU: BGE-M3 + transformers 4.57.6 deadlocks on MPS.
        _model_cache[key] = SentenceTransformer(model_name, device="cpu")
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


# ── LLM (Phase 3.1 Contextual Retrieval) ──────────────────────────────────

# Phase 3.1b output-validation constants for generate_context().
_MAX_CONTEXT_CHARS = 500      # upper bound for a valid context prefix
_MIN_CONTEXT_CHARS = 10       # lower bound (below -> reject as too short)
_MAX_DOCUMENT_CHARS = 50_000  # truncation limit for document_text input
_MAX_CHUNK_CHARS = 30_000      # truncation limit for chunk_text input

# MEHRZEILIGE Instruktionssprache-Heuristik (M6 from blind-spot review):
# matcht nur Instruktionen, deren Schlüsselwort auf einer eigenen Zeile
# steht UND denen auf der FOLGEZEILE mindestens 20 Zeichen Text
# folgen. Legitime einzeilige Godot-Kontexte wie
# "please refer to the Node3D documentation for rotation methods" werden
# NICHT gematcht (kein Zeilenumbruch → `\n.{20,}` greift nicht). Das
# `(?m)`-Flag aktiviert `^`-Matching am Zeilenanfang; `.` matcht ohne
# `(?s)`-Flag KEINE Newlines, wodurch der 20+-Zeichen-Body auf einer
# separaten Zeile liegen muss (wirklich MEHRZEILIG, wie M6 verlangt).
_INSTRUCTION_MULTILINE_RE = re.compile(
    r"(?m)^\s*(please|do not|don't|you must|you should|now|next|step\s+\d+)\b[^\n]*\n.{20,}"
)
# Instruktionen am Zeilenanfang, die immer verworfen werden (Prompt-Injection
# Indikator — "ignore previous instructions", "system:", "assistant:"). Das
# ``(?m)``-Flag aktiviert ``^``-Matching am Zeilenanfang JEDER Zeile (nicht
# nur der ersten), sodass eine Injection in Zeile 2+ (z.B.
# "Valid context.\nsystem: ignore rules") ebenfalls erkannt wird (Finding L-5
# aus dem Phase-3.1b diff-review). Führende Whitespaces werden toleriert.
_INSTRUCTION_PREFIX_RE = re.compile(
    r"(?m)^\s*(ignore|forget|system:|assistant:)\s", re.IGNORECASE
)


def _truncate(text: str, limit: int, label: str) -> str:
    """Truncate ``text`` to ``limit`` chars, warning if truncation occurs.

    Args:
        text: Input text to truncate.
        limit: Maximum number of characters to keep.
        label: Human-readable label used in the warning message
            (e.g. ``"document_text"``).

    Returns:
        ``text`` unchanged if ``len(text) <= limit``; otherwise the first
        ``limit`` characters. A ``UserWarning`` is emitted on truncation
        so operators can spot oversized inputs (Phase 3.1a akzeptiertes
        Risiko MEDIUM "Unbounded Prompt-Input" — hiermit adressiert).
    """
    if len(text) <= limit:
        return text
    import warnings as _warnings
    _warnings.warn(
        f"{label} truncated to {limit} chars (was {len(text)} chars)",
        RuntimeWarning,
        stacklevel=2,
    )
    return text[:limit]


def _validate_context(ctx: str) -> str | None:
    """Validate an LLM-generated context prefix.

    Phase 3.1b output validation (NB-6 / M6 from blind-spot review):
    guards against prompt-injection leakage, over-long reasoning output
    and degenerate empty responses. Only MEHRZEILIGE instruction
    language is rejected — legitimate Godot contexts that happen to
    contain words like "please" on a single line pass through.

    Args:
        ctx: Stripped LLM output to validate.

    Returns:
        The validated (and possibly truncated) context string, or
        ``None`` if the context is rejected (caller should fall back to
        ``context_prefix=None``).
    """
    import warnings as _warnings

    n = len(ctx)
    # 1. Length: too short -> reject (degenerate / empty reasoning).
    if n < _MIN_CONTEXT_CHARS:
        _warnings.warn(
            f"context too short ({n} chars) — rejected", RuntimeWarning,
            stacklevel=2,
        )
        return None
    # 1b. Length: too long -> truncate (safe; short contexts are OK).
    if n > _MAX_CONTEXT_CHARS:
        _warnings.warn(
            f"context truncated to 500 chars (was {n} chars)",
            RuntimeWarning,
            stacklevel=2,
        )
        ctx = ctx[:_MAX_CONTEXT_CHARS]
    # 2. Instruction-language heuristic (MEHRZEILIG, M6): reject only
    #    instructions spanning their own line with 20+ chars of body.
    if _INSTRUCTION_MULTILINE_RE.search(ctx):
        _warnings.warn(
            "context rejected: instruction language detected",
            RuntimeWarning,
            stacklevel=2,
        )
        return None
    # 3. Instruction-prefix check: "ignore", "forget", "system:",
    #    "assistant:" at the start of ANY line -> prompt injection.
    #    ``.search`` (not ``.match``) so the ``(?m)``-flag in
    #    ``_INSTRUCTION_PREFIX_RE`` can match injection on lines 2+
    #    (Phase 3.1b diff-review Finding L-5).
    if _INSTRUCTION_PREFIX_RE.search(ctx):
        _warnings.warn(
            "context rejected: instruction prefix detected",
            RuntimeWarning,
            stacklevel=2,
        )
        return None
    return ctx


def get_llm():
    """Lazy-load LLM for contextual retrieval. Cached per (backend, model_name).

    Resolution order:
    1. ``KH_LLM_MODEL`` environment variable (read LIVE on every cache-miss)
    2. :data:`DEFAULT_LLM_MODEL` (``gemma4:12b-mlx``)

    Backend selection via ``KH_LLM_BACKEND`` (default ``"ollama"``):
    - ``"ollama"``: Ollama HTTP-API, MLX-native on Apple Silicon.
      Requires the ``ollama`` system service (``brew install ollama``)
      and the model pulled (``ollama pull gemma4:12b-mlx``). The
      ``ollama`` Python package is only a lightweight HTTP client — no
      transformers conflict.

      Security (Phase 3.1a hardening): the client is pinned to
      ``http://localhost:11434`` by default to prevent accidental
      exfiltration of local repo/personal-notes content to a remote
      Ollama host. A non-loopback host is accepted ONLY via an
      explicit ``KH_OLLAMA_HOST`` environment variable (opt-in).
      ``OLLAMA_HOST`` (the ollama client default) is intentionally NOT
      honoured unless it resolves to a loopback address.
    - ``"llama-cpp"``: Cross-Platform fallback via ``llama-cpp-python``.

    Cache key: ``llm:<backend>:<model_name>``. Switching either env var
    at runtime loads a new model on the next cache-miss.

    Note:
        Gemma 4 12B MLX uses ~7.7 GB RAM on Metal GPU. Combined with
        BGE-M3 (~2.2 GB CPU) + ChromaDB + BM25 = ~10.5 GB total. BGE-M3
        is the required embedding model for Contextual Retrieval
        (8192-token context fits ``context_prefix + "\n" + text``);
        the legacy all-mpnet (384-token) would truncate the prefix.
    """
    import urllib.parse as _urlparse

    model_name = os.environ.get("KH_LLM_MODEL", DEFAULT_LLM_MODEL)
    backend = os.environ.get("KH_LLM_BACKEND", DEFAULT_LLM_BACKEND)
    key = f"llm:{backend}:{model_name}"
    if key not in _model_cache:
        if backend == "ollama":
            import ollama as _ollama

            # Loopback guard: pin to localhost:11434 by default. A
            # remote host is accepted ONLY via explicit KH_OLLAMA_HOST
            # opt-in (never via the implicit OLLAMA_HOST default).
            host = os.environ.get("KH_OLLAMA_HOST", "http://localhost:11434")
            parsed = _urlparse.urlparse(host)
            resolved_host = (parsed.hostname or "").lower()
            is_loopback = resolved_host in ("localhost", "127.0.0.1", "::1", "")
            if not is_loopback:
                # Non-loopback hosts require the explicit opt-in env var
                # (already read above). We log a warning so the operator
                # is aware that chunk/document content leaves the machine.
                import logging as _logging
                _logging.getLogger(__name__).warning(
                    "KH_OLLAMA_HOST points to a non-loopback host "
                    "(%s). Local repo/personal-notes content WILL be "
                    "sent to that remote Ollama service. Set KH_OLLAMA_HOST "
                    "only if you trust the remote host.",
                    host,
                )
            _model_cache[key] = {
                "client": _ollama.Client(host=host),
                "model": model_name,
                "backend": "ollama",
            }
        elif backend == "llama-cpp":
            from llama_cpp import Llama
            _model_cache[key] = {
                "model": Llama(model_path=model_name),
                "backend": "llama-cpp",
            }
        else:
            raise ValueError(f"Unknown KH_LLM_BACKEND: {backend}")
    return _model_cache[key]


def generate_context(llm_cache_entry, document_text, chunk_text, max_tokens=None):
    """Generate a 50-100 token context prefix for a chunk via the LLM.

    Uses the Anthropic Contextual Retrieval prompt template
    (https://www.anthropic.com/news/contextual-retrieval). The returned
    context situates the chunk within the overall document for the
    purposes of improving search retrieval.

    Args:
        llm_cache_entry: Entry returned by :func:`get_llm`
            (``{"client", "model", "backend"}`` for ollama, or
            ``{"model", "backend"}`` for llama-cpp).
        document_text: Whole source document text the chunk belongs to.
        chunk_text: The chunk text to situate.
        max_tokens: Maximum tokens for the LLM response. ``None`` (default)
            auto-resolves based on the model: reasoning models (Gemma 4)
            get 800 tokens (the thinking phase consumes tokens before the
            final answer; with 100 tokens ``done_reason='length'`` and
            ``content=''``; empirically ~256 eval tokens are needed),
            non-reasoning models (Llama, Qwen, glm, gpt, claude) get 200.
            An explicit value overrides the auto-resolution.

    Returns:
        The validated context string, or an empty string on error or
        invalid output (a warning is emitted via :mod:`warnings`; the
        function never raises — callers can fall back to
        ``context_prefix=None``). Phase 3.1b added output validation
        (length bounds + instruction-language rejection) and input
        truncation (document_text → 50k chars, chunk_text → 30k chars).
    """
    # Phase 3.1b: bound prompt inputs to avoid unbounded LLM runs
    # (security risk MEDIUM "Unbounded Prompt-Input" from 3.1a review).
    document_text = _truncate(document_text, _MAX_DOCUMENT_CHARS, "document_text")
    chunk_text = _truncate(chunk_text, _MAX_CHUNK_CHARS, "chunk_text")

    # L5: auto-resolve max_tokens based on the model when not explicit.
    # Gemma 4 is a reasoning model — the thinking phase needs token budget
    # (LIM-012). Non-reasoning models (Llama, Qwen, glm, gpt, claude, gemma3)
    # only need ~200 tokens for a 50-100 token context output.
    if max_tokens is None:
        model_name = llm_cache_entry.get("model", "")
        if "gemma4" in model_name.lower() or "gemma-4" in model_name.lower():
            max_tokens = 800
        else:
            max_tokens = 200

    prompt = (
        f"<document>\n{document_text}\n</document>\n"
        f"Here is the chunk we want to situate within the whole document:\n"
        f"<chunk>\n{chunk_text}\n</chunk>\n"
        f"Please give a short succinct context to situate this chunk "
        f"within the overall document for the purposes of improving "
        f"search retrieval of the chunk. Answer only with the succinct "
        f"context and nothing else."
    )

    if llm_cache_entry["backend"] == "ollama":
        try:
            response = llm_cache_entry["client"].chat(
                model=llm_cache_entry["model"],
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0, "num_predict": max_tokens},
                keep_alive="24h",  # keep model + KV-cache in RAM for batch
                stream=False,
            )
            # ollama 0.6.x returns a ChatResponse pydantic model, NOT a
            # dict. Use attribute access; fall back to dict access for
            # older ollama versions / other clients.
            try:
                raw = response.message.content.strip()
            except AttributeError:
                raw = response["message"]["content"].strip()
        except Exception as e:
            import warnings
            warnings.warn(f"LLM context generation failed: {e}", RuntimeWarning,
                          stacklevel=2)
            return ""
    elif llm_cache_entry["backend"] == "llama-cpp":
        try:
            response = llm_cache_entry["model"](
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=0,
            )
            raw = response["choices"][0]["text"].strip()
        except Exception as e:
            import warnings
            warnings.warn(f"LLM context generation failed: {e}", RuntimeWarning,
                          stacklevel=2)
            return ""
    else:
        return ""

    # Phase 3.1b: output validation (additive after strip()). On reject
    # we return "" — callers set context_prefix=None (NOT "").
    validated = _validate_context(raw)
    return validated if validated is not None else ""
