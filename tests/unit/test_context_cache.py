"""Unit tests for :mod:`context_cache` (Phase 3.1b Task 5).

Pure SQLite tests — no real Ollama/Gemma call, no embedding model, no
ChromaDB. Uses the ``tmp_hub`` fixture from ``tests/conftest.py`` so
each test gets an isolated ``chromadb_data/<domain>/context_cache.db``
under a temporary directory (``config.CHROMA_DIR`` is monkeypatched).
"""

import pytest

pytestmark = pytest.mark.unit

import context_cache as cc
from context_cache import (
    cache_key,
    chunk_text_hash,
    count_entries,
    get_cached,
    put_cached,
    bulk_invalidate_by_source_file,
    open_cache,
)


# ── Schema / open_cache ────────────────────────────────────────────────────


class TestSchema:
    def test_init_schema_creates_table(self, tmp_hub):
        # tmp_hub monkeypatches config.CHROMA_DIR to a temp dir, so
        # open_cache() builds the DB there and never touches the real
        # chromadb_data/.
        conn = open_cache("godot")
        try:
            # Table exists.
            row = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' "
                "AND name='context_cache'"
            ).fetchone()
            assert row is not None
            assert row[0] == "context_cache"
            # WAL journal mode active.
            mode = conn.execute("PRAGMA journal_mode").fetchone()
            assert mode[0].lower() == "wal"
            # Index exists.
            idx = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='index' "
                "AND name='idx_context_cache_source_file'"
            ).fetchone()
            assert idx is not None
        finally:
            conn.close()


# ── Round-trip CRUD ─────────────────────────────────────────────────────────


class TestCacheRoundTrip:
    def test_cache_round_trip(self, tmp_hub):
        conn = open_cache("godot")
        try:
            h = chunk_text_hash("chunk body text")
            put_cached(conn, "foo-packed.md", 3, h, "gemma4:12b-mlx",
                       "A Node3D rotation tutorial context.")
            got = get_cached(conn, "foo-packed.md", 3, h, "gemma4:12b-mlx")
            assert got == "A Node3D rotation tutorial context."
        finally:
            conn.close()

    def test_get_returns_none_on_miss(self, tmp_hub):
        conn = open_cache("godot")
        try:
            assert get_cached(conn, "missing.md", 0, "deadbeef",
                              "gemma4:12b-mlx") is None
        finally:
            conn.close()


# ── Cache key semantics (M1: model invalidation, domain independence) ──────


class TestCacheKey:
    def test_cache_key_changes_on_model_change(self):
        # M1: a model switch must invalidate the cache.
        k1 = cache_key("f.md", 0, "h", "gemma4:12b-mlx")
        k2 = cache_key("f.md", 0, "h", "llama3.2:3b")
        assert k1 != k2

    def test_cache_key_changes_on_text_change(self):
        # Changing the chunk text changes chunk_text_hash -> different
        # cache key -> cache miss (invalidation on source edit).
        h1 = chunk_text_hash("original chunk text")
        h2 = chunk_text_hash("edited chunk text")
        k1 = cache_key("f.md", 0, h1, "gemma4:12b-mlx")
        k2 = cache_key("f.md", 0, h2, "gemma4:12b-mlx")
        assert k1 != k2

    def test_cache_key_changes_on_chunk_id_change(self):
        k1 = cache_key("f.md", 0, "h", "gemma4:12b-mlx")
        k2 = cache_key("f.md", 1, "h", "gemma4:12b-mlx")
        assert k1 != k2

    def test_cache_key_changes_on_source_file_change(self):
        k1 = cache_key("a.md", 0, "h", "gemma4:12b-mlx")
        k2 = cache_key("b.md", 0, "h", "gemma4:12b-mlx")
        assert k1 != k2

    def test_cache_key_deterministic_for_same_inputs(self):
        # Same inputs -> same key (idempotent, reusable).
        assert cache_key("f.md", 0, "h", "gemma4:12b-mlx") == \
               cache_key("f.md", 0, "h", "gemma4:12b-mlx")


class TestModelInvalidation:
    def test_cache_miss_on_model_change(self, tmp_hub):
        # Cache with model A, look up with model B -> None (M1).
        conn = open_cache("godot")
        try:
            h = chunk_text_hash("body")
            put_cached(conn, "f.md", 0, h, "model-a", "ctx A")
            assert get_cached(conn, "f.md", 0, h, "model-a") == "ctx A"
            assert get_cached(conn, "f.md", 0, h, "model-b") is None
        finally:
            conn.close()


# ── Resume after partial crash (M2) ────────────────────────────────────────


class TestResumeAfterCrash:
    def test_cache_resume_after_partial_crash(self, tmp_hub):
        # Simulate a crash midway: half the chunks are cached, the
        # other half are not. Resume must find the cached half and miss
        # the rest (so the script only sends the rest to the LLM).
        conn = open_cache("godot")
        try:
            h = chunk_text_hash("body")
            # Cache entries for chunk_id 0..4 (the "first half").
            for i in range(5):
                put_cached(conn, "f.md", i, h, "gemma4:12b-mlx", f"ctx {i}")
            # Resume: look up all 10; first 5 hit, last 5 miss.
            hits, misses = 0, 0
            for i in range(10):
                got = get_cached(conn, "f.md", i, h, "gemma4:12b-mlx")
                if got is None:
                    misses += 1
                else:
                    hits += 1
            assert hits == 5
            assert misses == 5
        finally:
            conn.close()


# ── Idempotency ────────────────────────────────────────────────────────────


class TestIdempotency:
    def test_insert_or_replace_idempotent(self, tmp_hub):
        conn = open_cache("godot")
        try:
            h = chunk_text_hash("body")
            put_cached(conn, "f.md", 0, h, "gemma4:12b-mlx", "first context")
            put_cached(conn, "f.md", 0, h, "gemma4:12b-mlx", "second context")
            # Only one row for this key.
            assert count_entries(conn) == 1
            # And get returns the latest (replaced) value.
            assert get_cached(conn, "f.md", 0, h, "gemma4:12b-mlx") == \
                "second context"
        finally:
            conn.close()


# ── Bulk invalidation ──────────────────────────────────────────────────────


class TestBulkInvalidate:
    def test_bulk_invalidate_by_source_file(self, tmp_hub):
        conn = open_cache("godot")
        try:
            h = chunk_text_hash("body")
            put_cached(conn, "a.md", 0, h, "gemma4:12b-mlx", "ctx a0")
            put_cached(conn, "a.md", 1, h, "gemma4:12b-mlx", "ctx a1")
            put_cached(conn, "b.md", 0, h, "gemma4:12b-mlx", "ctx b0")
            deleted = bulk_invalidate_by_source_file(conn, "a.md")
            assert deleted == 2
            assert count_entries(conn) == 1
            assert get_cached(conn, "a.md", 0, h, "gemma4:12b-mlx") is None
            assert get_cached(conn, "a.md", 1, h, "gemma4:12b-mlx") is None
            assert get_cached(conn, "b.md", 0, h, "gemma4:12b-mlx") == "ctx b0"
        finally:
            conn.close()


# ── count_entries ──────────────────────────────────────────────────────────


class TestCountEntries:
    def test_count_entries(self, tmp_hub):
        conn = open_cache("godot")
        try:
            h = chunk_text_hash("body")
            put_cached(conn, "a.md", 0, h, "gemma4:12b-mlx", "ctx 1")
            put_cached(conn, "a.md", 1, h, "gemma4:12b-mlx", "ctx 2")
            put_cached(conn, "b.md", 0, h, "gemma4:12b-mlx", "ctx 3")
            assert count_entries(conn) == 3
            assert count_entries(conn, model="gemma4:12b-mlx") == 3
            assert count_entries(conn, model="llama3.2:3b") == 0
        finally:
            conn.close()