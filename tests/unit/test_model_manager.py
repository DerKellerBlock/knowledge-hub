"""Unit tests for model_manager — regex parsing, domain config, BM25 LRU cache.

These tests do NOT load any models (SentenceTransformer / CrossEncoder).
They test only the pure-logic parts: regex matching, config parsing, LRU cache.
"""

from pathlib import Path

import pytest

import model_manager as mm
from model_manager import (
    _DOMAIN_META_RE,
    _EMBEDDING_MODEL_RE,
    get_domain_config,
    bm25_cache_get,
    bm25_cache_set,
    bm25_cache_invalidate,
)


# ── _DOMAIN_META_RE ────────────────────────────────────────────────────────

class TestDomainMetaRegex:
    def test_matches_standard_metadaten_block(self):
        text = """# Domain: godot

## Metadaten
- Embedding-Model: all-mpnet-base-v2 (768 dims)
- Collection: godot_knowledge

## Lizenz-Hinweis
Some text.
"""
        m = _DOMAIN_META_RE.search(text)
        assert m is not None
        block = m.group(1)
        assert "Embedding-Model: all-mpnet-base-v2" in block
        assert "Collection: godot_knowledge" in block

    def test_matches_metadaten_at_end_of_file(self):
        text = """# Domain: test

## Metadaten
- Embedding-Model: all-MiniLM-L6-v2
"""
        m = _DOMAIN_META_RE.search(text)
        assert m is not None
        assert "all-MiniLM-L6-v2" in m.group(1)

    def test_no_metadaten_section(self):
        text = """# Domain: test

## Quellen
Some content.
"""
        m = _DOMAIN_META_RE.search(text)
        assert m is None

    def test_empty_metadaten_block(self):
        text = """# Domain: test

## Metadaten

## Other
"""
        m = _DOMAIN_META_RE.search(text)
        # empty block should still match (greedy .*? with DOTALL)
        assert m is not None

    def test_davinci_resolve_domain_md_matches(self):
        # read the actual davinci_resolve domain.md
        davinci_md = (
            Path(__file__).resolve().parent.parent.parent
            / "domains"
            / "davinci_resolve"
            / "domain.md"
        )
        if not davinci_md.exists():
            pytest.skip("davinci_resolve domain.md not found")
        text = davinci_md.read_text(encoding="utf-8")
        m = _DOMAIN_META_RE.search(text)
        assert m is not None
        assert "Embedding-Model" in m.group(1)

    def test_godot_domain_md_matches(self):
        godot_md = (
            Path(__file__).resolve().parent.parent.parent
            / "domains"
            / "godot"
            / "domain.md"
        )
        if not godot_md.exists():
            pytest.skip("godot domain.md not found")
        text = godot_md.read_text(encoding="utf-8")
        m = _DOMAIN_META_RE.search(text)
        assert m is not None


# ── _EMBEDDING_MODEL_RE ────────────────────────────────────────────────────

class TestEmbeddingModelRegex:
    def test_extracts_with_dims_annotation(self):
        block = "- Embedding-Model: all-mpnet-base-v2 (768 dims)\n"
        m = _EMBEDDING_MODEL_RE.search(block)
        assert m is not None
        assert m.group(1).strip() == "all-mpnet-base-v2"

    def test_extracts_without_dims(self):
        block = "- Embedding-Model: all-MiniLM-L6-v2\n"
        m = _EMBEDDING_MODEL_RE.search(block)
        assert m is not None
        assert m.group(1).strip() == "all-MiniLM-L6-v2"

    def test_no_match_if_wrong_key(self):
        block = "- Model: something\n"
        m = _EMBEDDING_MODEL_RE.search(block)
        assert m is None


# ── get_domain_config ──────────────────────────────────────────────────────

class TestGetDomainConfig:
    def test_nonexistent_domain_returns_defaults(self):
        cfg = get_domain_config("totally_nonexistent_domain_xyz")
        assert cfg["embedding_model"] == mm.DEFAULT_MODEL_NAME
        assert cfg["collection"] == "totally_nonexistent_domain_xyz_knowledge"
        assert "chroma_path" in cfg
        assert "bm25_path" in cfg

    def test_godot_config_if_domain_md_exists(self):
        godot_md = (
            Path(__file__).resolve().parent.parent.parent
            / "domains"
            / "godot"
            / "domain.md"
        )
        if not godot_md.exists():
            pytest.skip("godot domain.md not found")
        cfg = get_domain_config("godot")
        assert cfg["collection"] == "godot_knowledge"
        assert cfg["embedding_model"]  # non-empty
        assert cfg["chroma_path"].name == "chroma"
        assert cfg["bm25_path"].name == "godot_bm25.pkl"

    def test_davinci_config_if_domain_md_exists(self):
        davinci_md = (
            Path(__file__).resolve().parent.parent.parent
            / "domains"
            / "davinci_resolve"
            / "domain.md"
        )
        if not davinci_md.exists():
            pytest.skip("davinci_resolve domain.md not found")
        cfg = get_domain_config("davinci_resolve")
        assert cfg["collection"] == "davinci_resolve_knowledge"
        assert cfg["bm25_path"].name == "davinci_resolve_bm25.pkl"


# ── BM25 LRU Cache ──────────────────────────────────────────────────────────

class TestBM25CacheLRU:
    def setup_method(self):
        # Clear cache before each test
        mm._bm25_cache.clear()

    def test_set_and_get(self):
        bm25_cache_set("d1", {"index": "fake"})
        assert bm25_cache_get("d1") == {"index": "fake"}

    def test_get_nonexistent_returns_none(self):
        assert bm25_cache_get("nonexistent") is None

    def test_invalidate_removes_entry(self):
        bm25_cache_set("d1", {"index": "fake"})
        bm25_cache_invalidate("d1")
        assert bm25_cache_get("d1") is None

    def test_invalidate_nonexistent_does_not_raise(self):
        bm25_cache_invalidate("never_set")

    def test_lru_eviction_at_max_plus_one(self):
        # BM25_CACHE_MAX is 3 (from config)
        for i in range(mm.BM25_CACHE_MAX + 1):
            bm25_cache_set(f"d{i}", {"index": f"idx{i}"})
        # d0 should be evicted
        assert bm25_cache_get("d0") is None
        # d1, d2, d3 should still be there
        assert bm25_cache_get("d1") is not None
        assert bm25_cache_get("d2") is not None
        assert bm25_cache_get("d3") is not None

    def test_lru_order_updates_on_get(self):
        bm25_cache_set("d1", {})
        bm25_cache_set("d2", {})
        bm25_cache_set("d3", {})
        # Access d1 → moves to end (most recently used)
        bm25_cache_get("d1")
        # Add d4 → evicts least recently used (d2, not d1)
        bm25_cache_set("d4", {})
        assert bm25_cache_get("d1") is not None
        assert bm25_cache_get("d2") is None
        assert bm25_cache_get("d3") is not None
        assert bm25_cache_get("d4") is not None

    def test_lru_order_updates_on_set_existing(self):
        bm25_cache_set("d1", {})
        bm25_cache_set("d2", {})
        bm25_cache_set("d3", {})
        # Re-set d1 → moves to end
        bm25_cache_set("d1", {"updated": True})
        # Add d4 → evicts d2
        bm25_cache_set("d4", {})
        assert bm25_cache_get("d1") == {"updated": True}
        assert bm25_cache_get("d2") is None