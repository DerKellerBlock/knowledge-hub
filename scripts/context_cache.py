#!/usr/bin/env python3
"""SQLite cache for LLM-generated Contextual-Retrieval context prefixes.

Phase 3.1b Task 5. Stores the 50–100 token ``context_prefix`` strings
that :func:`model_manager.generate_context` produces for each chunk, so
that a crashed or partial contextualize run can resume without paying
the ~16.6 s/chunk LLM cost again, and so that promoting an eval domain
(e.g. ``godot_eval_a``) to the live domain (``godot``) reuses cached
contexts.

Design decisions (see Phase 3.1b plan):

* **Per-domain database file, domain-independent cache key (OQ-3 Option
  b).** Each domain gets its own ``chromadb_data/<domain>/context_cache.db``
  (gitignored — ``chromadb_data/`` is already in ``.gitignore``), so eval
  runs cannot pollute the live domain's cache. But the *cache key*
  omits the domain entirely
  (``sha256(source_file | chunk_id_in_file | chunk_text_hash | model)``),
  so a context cached for ``godot_eval_a/sources/foo-packed.md`` is
  found again when ``godot/sources/foo-packed.md`` is promoted — the
  promote step just copies the DB file.

* **WAL mode.** ``PRAGMA journal_mode=WAL`` + ``PRAGMA synchronous=NORMAL``
  give good bulk-insert throughput while keeping crash safety for the
  resume-after-crash scenario (M2).

* **``INSERT OR REPLACE`` idempotency.** Re-running the contextualize
  script on the same chunks overwrites stale entries atomically, so the
  cache never accumulates duplicate rows for the same key.

No real Ollama / GPU / embedding model is needed here — this module is
pure SQLite. Importing it does NOT import ``sentence_transformers`` or
``chromadb``, so it is safe to use in unit tests.
"""

from __future__ import annotations

import hashlib
import sqlite3
from pathlib import Path

# Live-lookup of the config module so tests can monkeypatch
# ``config.CHROMA_DIR`` (see tests/conftest.py ``tmp_hub`` fixture) and
# have the change take effect here. Mirrors the pattern used in
# ``model_manager.get_domain_config()``.
import sys as _sys

_pkg_root = Path(__file__).resolve().parent.parent
if str(_pkg_root) not in _sys.path:
    _sys.path.insert(0, str(_pkg_root))

from mcp_servers.knowledge_hub.config import CHROMA_DIR

_SCHEMA = """
CREATE TABLE IF NOT EXISTS context_cache (
    cache_key           TEXT PRIMARY KEY,
    source_file         TEXT NOT NULL,
    chunk_id_in_file    INTEGER NOT NULL,
    chunk_text_hash     TEXT NOT NULL,
    model               TEXT NOT NULL,
    context             TEXT NOT NULL,
    created_at          TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_context_cache_source_file
    ON context_cache(source_file);
"""


# ── Path helper ────────────────────────────────────────────────────────────


def cache_db_path(domain: str) -> Path:
    """Return the SQLite cache DB path for a domain.

    Resolves ``config.CHROMA_DIR`` live (so test monkeypatching of
    ``CHROMA_DIR`` via the ``tmp_hub`` fixture works). The directory is
    created on demand.
    """
    _config_mod = (
        _sys.modules.get("mcp_servers.knowledge_hub.config")
        or _sys.modules.get("config")
    )
    chroma_dir = getattr(_config_mod, "CHROMA_DIR", CHROMA_DIR)
    domain_dir = Path(chroma_dir) / domain
    domain_dir.mkdir(parents=True, exist_ok=True)
    return domain_dir / "context_cache.db"


# ── Schema ────────────────────────────────────────────────────────────────


def init_schema(conn: sqlite3.Connection) -> None:
    """Create the ``context_cache`` table + source-file index if absent.

    Idempotent — safe to call on every ``open_cache()``.
    """
    conn.executescript(_SCHEMA)
    conn.commit()


def open_cache(domain: str) -> sqlite3.Connection:
    """Open (or create) the per-domain context cache DB.

    Enables WAL journal mode and ``synchronous=NORMAL`` for good
    bulk-insert throughput while remaining crash-safe (M2 resume).

    Phase 3.3a concurrency hardening:

    * ``check_same_thread=False`` allows the connection to be shared
      across ``ThreadPoolExecutor`` workers (needed for parallel LLM
      calls in :func:`contextualize_chunks.contextualize_chunks`).
      Sharing the connection does NOT make concurrent writes safe —
      callers MUST serialise writes via a ``threading.Lock`` and rely on
      ``busy_timeout`` for the remaining races.
    * ``PRAGMA busy_timeout=5000`` makes SQLite wait up to 5 s on a
      locked DB instead of raising ``OperationalError: database is
      locked`` immediately. This absorbs the residual write/write races
      that the caller-side lock does not cover (e.g. WAL checkpoint
      contention).

    Args:
        domain: Domain name (e.g. ``"godot"``). Maps to
            ``chromadb_data/<domain>/context_cache.db``.

    Returns:
        An open :class:`sqlite3.Connection` with the schema initialised.
        Caller is responsible for closing it (``with``/``.close()``).
    """
    db_path = cache_db_path(domain)
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA busy_timeout=5000")
    init_schema(conn)
    return conn


# ── Cache key ──────────────────────────────────────────────────────────────


def chunk_text_hash(text: str) -> str:
    """SHA-256 of the chunk text. Used as a content-addressed invalidator.

    Changing the source document (even by a single character) changes
    the hash → cache miss → re-generation. This makes the cache robust
    against silent source-file edits without needing an explicit
    invalidation step.
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def cache_key(
    source_file: str,
    chunk_id_in_file: int,
    chunk_text_hash: str,
    model: str,
) -> str:
    """Domain-independent cache key (OQ-3 Option b).

    The domain is intentionally NOT part of the key, so that a cache
    entry produced for ``godot_eval_a/sources/foo-packed.md`` is reused
    when the same file is promoted to ``godot/sources/foo-packed.md``.
    The promote step merely copies ``context_cache.db`` across.

    Args:
        source_file: Source filename (e.g. ``"foo-packed.md"``). Must be
            stable across promote/copy steps for reuse to work.
        chunk_id_in_file: 0-based ordinal of the chunk within the file.
        chunk_text_hash: :func:`chunk_text_hash` of the chunk text.
        model: LLM model name (e.g. ``"gemma4:12b-mlx"``). A model
            switch invalidates all entries (M1).

    Returns:
        Hex SHA-256 digest as the PRIMARY KEY for the row.
    """
    raw = f"{source_file}|{chunk_id_in_file}|{chunk_text_hash}|{model}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


# ── CRUD ───────────────────────────────────────────────────────────────────


def get_cached(
    conn: sqlite3.Connection,
    source_file: str,
    chunk_id_in_file: int,
    chunk_text_hash: str,
    model: str,
) -> str | None:
    """Look up a cached context. Returns ``None`` on miss."""
    row = conn.execute(
        "SELECT context FROM context_cache WHERE cache_key = ?",
        (cache_key(source_file, chunk_id_in_file, chunk_text_hash, model),),
    ).fetchone()
    return row[0] if row is not None else None


def put_cached(
    conn: sqlite3.Connection,
    source_file: str,
    chunk_id_in_file: int,
    chunk_text_hash: str,
    model: str,
    context: str,
) -> None:
    """Insert or replace a cached context atomically.

    ``INSERT OR REPLACE`` makes the operation idempotent: re-running the
    contextualize script on the same chunks overwrites stale rows rather
    than accumulating duplicates.

    Args:
        conn: Open DB connection from :func:`open_cache`.
        source_file: Source filename.
        chunk_id_in_file: 0-based chunk ordinal within the file.
        chunk_text_hash: :func:`chunk_text_hash` of the chunk text.
        model: LLM model name.
        context: The validated context prefix string to cache.
    """
    # NOTE: a ``document_truncated`` column was originally specced to
    # record whether ``_truncate()`` truncated ``document_text`` during
    # generation, but no caller populated it (the field would always be
    # 0). Removed in the Phase 3.1b diff-review (Finding L-3) to avoid
    # a misleading always-zero column. If needed later, re-add it via a
    # schema migration and have ``generate_context``/``_truncate`` return
    # the truncation status.
    conn.execute(
        """INSERT OR REPLACE INTO context_cache
               (cache_key, source_file, chunk_id_in_file, chunk_text_hash,
                model, context)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (
            cache_key(source_file, chunk_id_in_file, chunk_text_hash, model),
            source_file,
            chunk_id_in_file,
            chunk_text_hash,
            model,
            context,
        ),
    )
    conn.commit()


def bulk_invalidate_by_source_file(
    conn: sqlite3.Connection,
    source_file: str,
) -> int:
    """Delete all cache entries for a given source file.

    Used when a source file is re-packed (repomix) and every chunk in it
    has potentially shifted. Returns the number of deleted rows.
    """
    cur = conn.execute(
        "DELETE FROM context_cache WHERE source_file = ?",
        (source_file,),
    )
    conn.commit()
    return cur.rowcount


def count_entries(
    conn: sqlite3.Connection,
    model: str | None = None,
) -> int:
    """Count cached entries, optionally filtered by model.

    Used by the contextualize script to report resume progress
    (``"N/M chunks cached"``).
    """
    if model is None:
        row = conn.execute("SELECT COUNT(*) FROM context_cache").fetchone()
    else:
        row = conn.execute(
            "SELECT COUNT(*) FROM context_cache WHERE model = ?",
            (model,),
        ).fetchone()
    return int(row[0]) if row else 0