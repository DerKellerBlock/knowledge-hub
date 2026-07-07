"""SQLite cache for multimodal image embeddings.

Vision Retrieval Feature (Task 4). Stores the SigLIP-2 / jina-clip-v2
embeddings (image and caption) so a crashed or partial embedding run can
resume without re-paying the MPS/CPU encode cost, and so a domain promote
step can copy the cache file and reuse embeddings.

Design mirrors :mod:`image_caption_cache`:

* **Per-domain database file, domain-independent cache key.** Each domain
  gets its own ``chromadb_data/<domain>/image_embedding_cache.db``. The
  cache key omits the domain (content-hash of image bytes + model +
  modality), so an embedding cached for an eval domain is reused when the
  image is promoted to the live domain.

* **WAL mode + ``INSERT OR REPLACE`` + ``check_same_thread=False`` +
  ``busy_timeout=5000``** — same concurrency hardening as the other
  caches.

Embeddings are stored as base64-encoded float32 byte strings so they can
round-trip through SQLite TEXT columns without loss. The dim is stored
alongside to validate on read.
"""

from __future__ import annotations

import base64
import hashlib
import sqlite3
from pathlib import Path

import sys as _sys

_pkg_root = Path(__file__).resolve().parent.parent
if str(_pkg_root) not in _sys.path:
    _sys.path.insert(0, str(_pkg_root))

from mcp_servers.knowledge_hub.config import CHROMA_DIR

_SCHEMA = """
CREATE TABLE IF NOT EXISTS image_embedding_cache (
    cache_key           TEXT PRIMARY KEY,
    image_id            TEXT NOT NULL,
    image_hash          TEXT NOT NULL,
    model               TEXT NOT NULL,
    modality            TEXT NOT NULL,
    dim                 INTEGER NOT NULL,
    embedding_b64       TEXT NOT NULL,
    created_at          TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_image_embedding_cache_image_id
    ON image_embedding_cache(image_id);
"""


# ── Path helper ────────────────────────────────────────────────────────────


def cache_db_path(domain: str) -> Path:
    """Return the SQLite cache DB path for a domain."""
    _config_mod = (
        _sys.modules.get("mcp_servers.knowledge_hub.config")
        or _sys.modules.get("config")
    )
    chroma_dir = getattr(_config_mod, "CHROMA_DIR", CHROMA_DIR)
    domain_dir = Path(chroma_dir) / domain
    domain_dir.mkdir(parents=True, exist_ok=True)
    return domain_dir / "image_embedding_cache.db"


def init_schema(conn: sqlite3.Connection) -> None:
    """Create the ``image_embedding_cache`` table if absent. Idempotent."""
    conn.executescript(_SCHEMA)
    conn.commit()


def open_cache(domain: str) -> sqlite3.Connection:
    """Open (or create) the per-domain image-embedding cache DB.

    Enables WAL journal mode + ``synchronous=NORMAL`` + ``busy_timeout=5000``
    + ``check_same_thread=False`` for ThreadPoolExecutor worker sharing.
    """
    db_path = cache_db_path(domain)
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA busy_timeout=5000")
    init_schema(conn)
    return conn


# ── Encoding helpers ────────────────────────────────────────────────────────


def image_hash(image_path: Path) -> str:
    """SHA-256 of the image file bytes."""
    h = hashlib.sha256()
    with open(image_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def caption_hash(caption: str) -> str:
    """SHA-256 of the caption text. Used when modality == 'caption'."""
    return hashlib.sha256(caption.encode("utf-8")).hexdigest()


def cache_key(image_id: str, content_hash: str, model: str, modality: str) -> str:
    """Domain-independent cache key.

    Args:
        image_id: Stable image identifier.
        content_hash: :func:`image_hash` (for ``modality=="image"``) or
            :func:`caption_hash` (for ``modality=="caption"``).
        model: Multimodal model name (e.g. ``"google/siglip2-so400m-patch16-512"``).
        modality: ``"image"`` or ``"caption"``.
    """
    raw = f"{image_id}|{content_hash}|{model}|{modality}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _encode_embedding(vec) -> str:
    """Encode a numpy array as base64 float32 bytes."""
    import numpy as _np
    arr = _np.asarray(vec, dtype=_np.float32)
    return base64.b64encode(arr.tobytes()).decode("ascii")


def _decode_embedding(b64: str, dim: int):
    """Decode base64 float32 bytes back to a numpy array."""
    import numpy as _np
    raw = base64.b64decode(b64)
    arr = _np.frombuffer(raw, dtype=_np.float32)
    if len(arr) != dim:
        raise ValueError(
            f"Embedding dim mismatch: expected {dim}, got {len(arr)}"
        )
    return arr


# ── CRUD ───────────────────────────────────────────────────────────────────


def get_cached(
    conn: sqlite3.Connection,
    image_id: str,
    content_hash: str,
    model: str,
    modality: str,
):
    """Look up a cached embedding. Returns the numpy array or ``None``."""
    row = conn.execute(
        "SELECT dim, embedding_b64 FROM image_embedding_cache WHERE cache_key = ?",
        (cache_key(image_id, content_hash, model, modality),),
    ).fetchone()
    if row is None:
        return None
    dim, b64 = row
    return _decode_embedding(b64, dim)


def put_cached(
    conn: sqlite3.Connection,
    image_id: str,
    content_hash: str,
    model: str,
    modality: str,
    embedding,
) -> None:
    """Insert or replace a cached embedding atomically."""
    import numpy as _np
    arr = _np.asarray(embedding, dtype=_np.float32)
    dim = arr.shape[-1]
    b64 = _encode_embedding(arr)
    conn.execute(
        """INSERT OR REPLACE INTO image_embedding_cache
               (cache_key, image_id, image_hash, model, modality, dim, embedding_b64)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (
            cache_key(image_id, content_hash, model, modality),
            image_id,
            content_hash,
            model,
            modality,
            dim,
            b64,
        ),
    )
    conn.commit()


def count_entries(
    conn: sqlite3.Connection,
    model: str | None = None,
    modality: str | None = None,
) -> int:
    """Count cached entries, optionally filtered by model and/or modality."""
    sql = "SELECT COUNT(*) FROM image_embedding_cache"
    clauses = []
    params = []
    if model is not None:
        clauses.append("model = ?")
        params.append(model)
    if modality is not None:
        clauses.append("modality = ?")
        params.append(modality)
    if clauses:
        sql += " WHERE " + " AND ".join(clauses)
    row = conn.execute(sql, params).fetchone()
    return int(row[0]) if row else 0
