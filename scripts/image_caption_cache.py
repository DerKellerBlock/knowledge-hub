"""SQLite cache for Vision-LLM-generated image captions.

Vision Retrieval Feature (Task 3). Stores context-aware captions produced
by :func:`caption_images.caption_image` so a crashed or partial caption run
can resume without re-paying the ~2.5 s/image Cloud cost, and so a domain
promote step (e.g. eval → live) can copy the cache file and reuse captions.

Design mirrors :mod:`context_cache` (Phase 3.1b):

* **Per-domain database file, domain-independent cache key.** Each domain
  gets its own ``chromadb_data/<domain>/image_caption_cache.db``
  (gitignored — ``chromadb_data/`` is already in ``.gitignore``). The cache
  key omits the domain entirely (content-hash of the image bytes + model),
  so a caption cached for an eval domain is reused when the image is
  promoted to the live domain — the promote step just copies the DB file.

* **WAL mode.** ``PRAGMA journal_mode=WAL`` + ``PRAGMA synchronous=NORMAL``
  give good bulk-insert throughput while keeping crash safety for the
  resume-after-crash scenario.

* **``INSERT OR REPLACE`` idempotency.** Re-running the caption script on the
  same image overwrites stale entries atomically.

* **``check_same_thread=False`` + ``busy_timeout=5000``** for
  ``ThreadPoolExecutor`` worker sharing (analog :func:`context_cache.open_cache`
  Phase 3.3a concurrency hardening).

No real Ollama / GPU / embedding model is needed here — this module is pure
SQLite. Importing it does NOT import ``ollama`` or ``transformers``, so it is
safe to use in unit tests.
"""

from __future__ import annotations

import hashlib
import sqlite3
from pathlib import Path

# Live-lookup of the config module so tests can monkeypatch
# ``config.CHROMA_DIR`` (see tests/conftest.py ``tmp_hub`` fixture) and have
# the change take effect here. Mirrors the pattern in :mod:`context_cache`.
import sys as _sys

_pkg_root = Path(__file__).resolve().parent.parent
if str(_pkg_root) not in _sys.path:
    _sys.path.insert(0, str(_pkg_root))

from mcp_servers.knowledge_hub.config import CHROMA_DIR

_SCHEMA = """
CREATE TABLE IF NOT EXISTS image_caption_cache (
    cache_key           TEXT PRIMARY KEY,
    image_id            TEXT NOT NULL,
    image_hash          TEXT NOT NULL,
    model               TEXT NOT NULL,
    caption             TEXT NOT NULL,
    created_at          TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_image_caption_cache_image_id
    ON image_caption_cache(image_id);
"""


# ── Path helper ────────────────────────────────────────────────────────────


def cache_db_path(domain: str) -> Path:
    """Return the SQLite cache DB path for a domain.

    Resolves ``config.CHROMA_DIR`` live (so test monkeypatching works).
    The directory is created on demand.
    """
    _config_mod = (
        _sys.modules.get("mcp_servers.knowledge_hub.config")
        or _sys.modules.get("config")
    )
    chroma_dir = getattr(_config_mod, "CHROMA_DIR", CHROMA_DIR)
    domain_dir = Path(chroma_dir) / domain
    domain_dir.mkdir(parents=True, exist_ok=True)
    return domain_dir / "image_caption_cache.db"


# ── Schema ────────────────────────────────────────────────────────────────


def init_schema(conn: sqlite3.Connection) -> None:
    """Create the ``image_caption_cache`` table + image_id index if absent.

    Idempotent — safe to call on every ``open_cache()``.
    """
    conn.executescript(_SCHEMA)
    conn.commit()


def open_cache(domain: str) -> sqlite3.Connection:
    """Open (or create) the per-domain image-caption cache DB.

    Enables WAL journal mode and ``synchronous=NORMAL`` for good bulk-insert
    throughput while remaining crash-safe (resume).

    Phase 3.3a concurrency hardening (analog :func:`context_cache.open_cache`):

    * ``check_same_thread=False`` allows the connection to be shared across
      ``ThreadPoolExecutor`` workers.
    * ``PRAGMA busy_timeout=5000`` makes SQLite wait up to 5 s on a locked DB.
    """
    db_path = cache_db_path(domain)
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA busy_timeout=5000")
    init_schema(conn)
    return conn


# ── Cache key ──────────────────────────────────────────────────────────────


def image_hash(image_path: Path) -> str:
    """SHA-256 of the image file bytes. Used as a content-addressed key.

    Re-packing a PDF (even by a single byte) changes the extracted PNG
    bytes → cache miss → re-caption. This makes the cache robust against
    silent source-file edits.
    """
    h = hashlib.sha256()
    with open(image_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def cache_key(image_id: str, img_hash: str, model: str) -> str:
    """Domain-independent cache key.

    The domain is intentionally NOT part of the key, so a caption cached
    for an eval domain is reused when the image is promoted to the live
    domain. The promote step merely copies ``image_caption_cache.db``.

    Args:
        image_id: Stable image identifier (``<domain>::img::<stem>::<page>::<idx>``).
        img_hash: :func:`image_hash` of the image file bytes.
        model: Vision-LLM model name (e.g. ``"gemma4:cloud"``). A model
            switch invalidates all entries.

    Returns:
        Hex SHA-256 digest as the PRIMARY KEY for the row.
    """
    raw = f"{image_id}|{img_hash}|{model}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


# ── CRUD ───────────────────────────────────────────────────────────────────


def get_cached(
    conn: sqlite3.Connection,
    image_id: str,
    img_hash: str,
    model: str,
) -> str | None:
    """Look up a cached caption. Returns ``None`` on miss."""
    row = conn.execute(
        "SELECT caption FROM image_caption_cache WHERE cache_key = ?",
        (cache_key(image_id, img_hash, model),),
    ).fetchone()
    return row[0] if row is not None else None


def put_cached(
    conn: sqlite3.Connection,
    image_id: str,
    img_hash: str,
    model: str,
    caption: str,
) -> None:
    """Insert or replace a cached caption atomically.

    ``INSERT OR REPLACE`` makes the operation idempotent.
    """
    conn.execute(
        """INSERT OR REPLACE INTO image_caption_cache
               (cache_key, image_id, image_hash, model, caption)
           VALUES (?, ?, ?, ?, ?)""",
        (
            cache_key(image_id, img_hash, model),
            image_id,
            img_hash,
            model,
            caption,
        ),
    )
    conn.commit()


def count_entries(
    conn: sqlite3.Connection,
    model: str | None = None,
) -> int:
    """Count cached entries, optionally filtered by model."""
    if model is None:
        row = conn.execute("SELECT COUNT(*) FROM image_caption_cache").fetchone()
    else:
        row = conn.execute(
            "SELECT COUNT(*) FROM image_caption_cache WHERE model = ?",
            (model,),
        ).fetchone()
    return int(row[0]) if row else 0


def bulk_invalidate_by_image_id(
    conn: sqlite3.Connection,
    image_id_prefix: str,
) -> int:
    """Delete all cache entries whose ``image_id`` starts with the prefix.

    Used when a source PDF is re-packed and every image in it has
    potentially shifted. Returns the number of deleted rows.
    """
    cur = conn.execute(
        "DELETE FROM image_caption_cache WHERE image_id LIKE ?",
        (image_id_prefix + "%",),
    )
    conn.commit()
    return cur.rowcount
