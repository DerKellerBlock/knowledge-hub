# Knowledge Hub — Test Suite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a four-layer automated test suite (unit / integration / e2e / MCP-contract) that verifies Knowledge Hub information retrieval actually works — content relevance, not just structure.

**Architecture:** pytest with marker-based layer separation. Unit tests run in seconds with no models loaded. Integration tests use a temporary ChromaDB with 3 dummy markdown sources. E2E tests run against the prebuilt godot/davinci_resolve indexes. MCP-contract tests call the actual tool functions with pytest-asyncio.

**Tech Stack:** Python 3.13, pytest 8.x, pytest-asyncio 0.23+, pytest-cov, chromadb, sentence-transformers, rank-bm25, mcp.

---

## File Structure

```
knowledge-hub/
├── pyproject.toml                       # pytest config (NEW)
├── requirements-dev.txt                  # dev dependencies (NEW)
├── tests/
│   ├── __init__.py                       # package marker (NEW)
│   ├── conftest.py                        # shared fixtures: tmp_hub, dummy_domain, indexed_dummy, skip markers (NEW)
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_config.py
│   │   ├── test_model_manager.py
│   │   ├── test_tools.py
│   │   ├── test_bm25_tokenizer.py
│   │   ├── test_rrf_fusion.py
│   │   └── test_parser_base.py
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_embed_index.py
│   │   ├── test_bm25_search.py
│   │   ├── test_embed_search.py
│   │   ├── test_hybrid_search.py
│   │   ├── test_migration.py
│   │   └── test_personal_notes.py
│   ├── e2e/
│   │   ├── __init__.py
│   │   ├── test_godot_regression.py
│   │   └── test_davinci_regression.py
│   └── mcp/
│       ├── __init__.py
│       └── test_mcp_contract.py
```

---

## Task 1: pytest Infrastructure (pyproject.toml, requirements-dev.txt, tests package)

**Files:**
- Create: `pyproject.toml`
- Create: `requirements-dev.txt`
- Create: `tests/__init__.py`
- Create: `tests/unit/__init__.py`
- Create: `tests/integration/__init__.py`
- Create: `tests/e2e/__init__.py`
- Create: `tests/mcp/__init__.py`

- [ ] **Step 1: Write pyproject.toml**

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
markers = [
    "unit: fast isolated tests, no models/DB loaded (< 10s)",
    "integration: tests with a temporary ChromaDB and dummy data (~60s)",
    "e2e: regression tests against the prebuilt real index (~30s)",
    "mcp: MCP contract tests calling actual tool functions (~30s)",
]
addopts = "--strict-markers"
```

- [ ] **Step 2: Write requirements-dev.txt**

```text
# Knowledge Hub — Development/Test Dependencies
#
# Installation:
#   pip install -r requirements-dev.txt
#
# This installs runtime deps (requirements.txt) + test deps.

-r requirements.txt

pytest>=8.0.0,<9.0.0
pytest-asyncio>=0.23.0,<1.0.0
pytest-cov>=4.0.0,<6.0.0
```

- [ ] **Step 3: Create package marker files**

Create 5 empty `__init__.py` files:

```bash
mkdir -p tests/unit tests/integration tests/e2e tests/mcp
touch tests/__init__.py tests/unit/__init__.py tests/integration/__init__.py tests/e2e/__init__.py tests/mcp/__init__.py
```

- [ ] **Step 4: Install dev dependencies**

```bash
cd /Users/noahk/Documents/work/knowledge-hub
.venv/bin/pip install -r requirements-dev.txt
```

Expected: pytest, pytest-asyncio, pytest-cov install successfully.

- [ ] **Step 5: Verify pytest discovers nothing yet**

```bash
.venv/bin/pytest --collect-only
```

Expected: `no tests ran` or `collected 0 items` (no errors, config loads).

- [ ] **Step 6: Commit**

```bash
git add pyproject.toml requirements-dev.txt tests/
git commit -m "test: add pytest infrastructure (pyproject.toml, requirements-dev, test packages)"
```

---

## Task 2: Unit Tests — config.py and bm25 tokenizer

**Files:**
- Create: `tests/unit/test_config.py`
- Create: `tests/unit/test_bm25_tokenizer.py`

- [ ] **Step 1: Write tests/unit/test_config.py**

```python
"""Unit tests for config.py path helpers."""

from pathlib import Path

from mcp_servers.knowledge_hub.config import (
    HUB_ROOT,
    DOMAINS_DIR,
    SCRIPTS_DIR,
    CHROMA_DIR,
    PERSONAL_DIR,
    domain_chroma_path,
    domain_bm25_path,
    legacy_bm25_path,
    legacy_collection_path,
    DEFAULT_MODEL_NAME,
    CROSS_ENCODER_MODEL,
    BM25_CACHE_MAX,
    CHROMA_MEMORY_LIMIT_BYTES,
)


def test_hub_root_is_absolute():
    assert HUB_ROOT.is_absolute()
    assert HUB_ROOT.name == "knowledge-hub"


def test_domains_dir_under_hub_root():
    assert DOMAINS_DIR == HUB_ROOT / "domains"


def test_scripts_dir_under_hub_root():
    assert SCRIPTS_DIR == HUB_ROOT / "scripts"


def test_chroma_dir_under_hub_root():
    assert CHROMA_DIR == HUB_ROOT / "chromadb_data"


def test_domain_chroma_path_godot():
    p = domain_chroma_path("godot")
    assert p == CHROMA_DIR / "godot" / "chroma"


def test_domain_chroma_path_davinci_resolve():
    p = domain_chroma_path("davinci_resolve")
    assert p == CHROMA_DIR / "davinci_resolve" / "chroma"


def test_domain_chroma_path_arbitrary():
    p = domain_chroma_path("my_domain")
    assert p == CHROMA_DIR / "my_domain" / "chroma"


def test_domain_bm25_path_godot():
    p = domain_bm25_path("godot")
    assert p == CHROMA_DIR / "godot" / "godot_bm25.pkl"


def test_domain_bm25_path_davinci_resolve():
    p = domain_bm25_path("davinci_resolve")
    assert p == CHROMA_DIR / "davinci_resolve" / "davinci_resolve_bm25.pkl"


def test_legacy_bm25_path():
    assert legacy_bm25_path("godot") == CHROMA_DIR / "godot_bm25.pkl"


def test_legacy_collection_path():
    assert legacy_collection_path("godot") == CHROMA_DIR / "godot_knowledge"


def test_default_model_name_is_string():
    assert isinstance(DEFAULT_MODEL_NAME, str)
    assert len(DEFAULT_MODEL_NAME) > 0


def test_cross_encoder_model_is_string():
    assert isinstance(CROSS_ENCODER_MODEL, str)


def test_bm25_cache_max_is_positive_int():
    assert isinstance(BM25_CACHE_MAX, int)
    assert BM25_CACHE_MAX > 0


def test_chroma_memory_limit_is_bytes():
    assert isinstance(CHROMA_MEMORY_LIMIT_BYTES, int)
    assert CHROMA_MEMORY_LIMIT_BYTES > 0
```

- [ ] **Step 2: Write tests/unit/test_bm25_tokenizer.py**

```python
"""Unit tests for bm25_search.tokenize (pure function, no DB needed)."""

from bm25_search import tokenize


def test_tokenize_simple_two_words():
    assert tokenize("Node3D rotate") == ["node3d", "rotate"]


def test_tokenize_preserves_underscores():
    assert tokenize("rotate_y") == ["rotate_y"]


def test_tokenize_multiple_spaces():
    assert tokenize("  multiple   spaces  ") == ["multiple", "spaces"]


def test_tokenize_empty_string():
    assert tokenize("") == []


def test_tokenize_only_punctuation():
    assert tokenize("!@#$%^&*()") == []


def test_tokenize_camelcase_lowercased():
    # tokenizer lowercases everything; CamelCase is not split
    assert tokenize("CamelCaseString") == ["camelcasestring"]


def test_tokenize_mixed_alphanumeric():
    assert tokenize("Vector3 1.5 2.0") == ["vector3", "1", "5", "2", "0"]


def test_tokenize_newlines_and_tabs():
    assert tokenize("line1\nline2\ttab") == ["line1", "line2", "tab"]


def test_tokenize_german_umlaute():
    # \w in Python regex includes unicode word chars by default
    tokens = tokenize("übermäßige Größe")
    assert "übermäßige" in tokens
    assert "größe" in tokens


def test_tokenize_hyphen_separated():
    assert tokenize("all-mpnet-base-v2") == ["all", "mpnet", "base", "v2"]


def test_tokenize_numbers_only():
    assert tokenize("123 456") == ["123", "456"]
```

- [ ] **Step 3: Run unit tests for config + tokenizer**

```bash
cd /Users/noahk/Documents/work/knowledge-hub
.venv/bin/pytest tests/unit/test_config.py tests/unit/test_bm25_tokenizer.py -v -m unit
```

Expected: all tests PASS.

- [ ] **Step 4: Commit**

```bash
git add tests/unit/test_config.py tests/unit/test_bm25_tokenizer.py
git commit -m "test(unit): add config path helper tests and bm25 tokenizer tests"
```

---

## Task 3: Unit Tests — model_manager regex and BM25 LRU cache

**Files:**
- Create: `tests/unit/test_model_manager.py`

- [ ] **Step 1: Write tests/unit/test_model_manager.py**

```python
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
```

- [ ] **Step 2: Run unit tests for model_manager**

```bash
cd /Users/noahk/Documents/work/knowledge-hub
.venv/bin/pytest tests/unit/test_model_manager.py -v -m unit
```

Expected: all tests PASS. The `test_godot_domain_md_matches` / `test_davinci_config_if_domain_md_exists` tests will be skipped if those domain.md files don't exist (they do in this repo).

- [ ] **Step 3: Commit**

```bash
git add tests/unit/test_model_manager.py
git commit -m "test(unit): add model_manager regex parsing and BM25 LRU cache tests"
```

---

## Task 4: Unit Tests — tools.py domain scoping and parser_base

**Files:**
- Create: `tests/unit/test_tools.py`
- Create: `tests/unit/test_parser_base.py`

- [ ] **Step 1: Write tests/unit/test_tools.py**

```python
"""Unit tests for tools.py — domain scoping and category validation.

Does NOT call search_knowledge (which requires a loaded index).
Tests only the pure-logic helpers: set_domain_scope, _check_domain_scope,
list_scoped_domains, and regex validation.
"""

import pytest

from mcp_servers.knowledge_hub import tools
from mcp_servers.knowledge_hub.tools import (
    set_domain_scope,
    _check_domain_scope,
    list_domains,
    list_scoped_domains,
    _CATEGORY_RE,
)


@pytest.fixture(autouse=True)
def reset_scope():
    """Reset domain scope before and after each test."""
    set_domain_scope(None)
    yield
    set_domain_scope(None)


class TestDomainScoping:
    def test_no_scope_all_visible(self):
        set_domain_scope(None)
        assert _check_domain_scope("godot") is None
        assert _check_domain_scope("davinci_resolve") is None
        assert _check_domain_scope("anything") is None

    def test_empty_list_all_visible(self):
        set_domain_scope([])
        assert _check_domain_scope("anything") is None

    def test_single_domain_scope(self):
        # Use a domain that actually exists for the scope to be accepted
        available = list_domains()
        if not available:
            pytest.skip("no domains available")
        target = available[0]
        set_domain_scope([target])
        assert _check_domain_scope(target) is None
        # Any other domain → error
        for other in available:
            if other != target:
                result = _check_domain_scope(other)
                assert result is not None
                assert "error" in result
                assert target in result["error"]

    def test_scope_with_nonexistent_domain_raises(self):
        with pytest.raises(ValueError, match="Domain\\(s\\) not found"):
            set_domain_scope(["totally_nonexistent_xyz"])

    def test_scope_restricts_list_scoped_domains(self):
        available = list_domains()
        if len(available) < 2:
            pytest.skip("need at least 2 domains")
        target = available[0]
        set_domain_scope([target])
        scoped = list_scoped_domains()
        assert scoped == [target]

    def test_no_scope_list_scoped_equals_list_domains(self):
        set_domain_scope(None)
        assert list_scoped_domains() == list_domains()


class TestCategoryRegex:
    def test_valid_lowercase(self):
        assert _CATEGORY_RE.match("gotchas")
        assert _CATEGORY_RE.match("tips")
        assert _CATEGORY_RE.match("best-practices")
        assert _CATEGORY_RE.match("faq")
        assert _CATEGORY_RE.match("my_category")

    def test_uppercase_rejected(self):
        assert not _CATEGORY_RE.match("Gotchas")
        assert not _CATEGORY_RE.match("TIPS")

    def test_slash_rejected(self):
        assert not _CATEGORY_RE.match("bad/cat")

    def test_empty_rejected(self):
        assert not _CATEGORY_RE.match("")

    def test_space_rejected(self):
        assert not _CATEGORY_RE.match("two words")

    def test_dot_rejected(self):
        assert not _CATEGORY_RE.match("file.txt")
```

- [ ] **Step 2: Write tests/unit/test_parser_base.py**

```python
"""Unit tests for parser_base — Chunk dataclass and fallback_chunk."""

import json

from parser_base import Chunk, fallback_chunk, FALLBACK_CHUNK_CHARS, FALLBACK_OVERLAP_CHARS


class TestChunkToMetadata:
    def test_basic_fields_present(self):
        c = Chunk(
            chunk_id="test::1",
            domain="test",
            text="hello",
            source_type="repo",
            source_file="file.md",
            line_start=10,
            line_end=20,
        )
        meta = c.to_chromadb_metadata()
        assert meta["source_type"] == "repo"
        assert meta["domain"] == "test"
        assert meta["source_file"] == "file.md"
        assert meta["line_start"] == 10
        assert meta["line_end"] == 20
        assert meta["chunk_id_in_file"] == 0

    def test_none_fields_omitted(self):
        c = Chunk(
            chunk_id="test::1",
            domain="test",
            text="hello",
            source_type="repo",
        )
        meta = c.to_chromadb_metadata()
        assert "chunk_type" not in meta
        assert "class_name" not in meta
        assert "name" not in meta
        assert "signature" not in meta
        assert "inherits_from" not in meta
        assert "docstring" not in meta

    def test_inherits_from_serialized_as_json(self):
        c = Chunk(
            chunk_id="test::1",
            domain="test",
            text="hello",
            source_type="repo",
            inherits_from=["Node", "Node3D"],
        )
        meta = c.to_chromadb_metadata()
        assert meta["inherits_from"] == '["Node", "Node3D"]'
        assert isinstance(meta["inherits_from"], str)

    def test_docstring_truncated(self):
        long_doc = "x" * 1000
        c = Chunk(
            chunk_id="test::1",
            domain="test",
            text="hello",
            source_type="repo",
            docstring=long_doc,
        )
        meta = c.to_chromadb_metadata()
        assert len(meta["docstring"]) == 500


class TestChunkFromMetadata:
    def test_round_trip(self):
        c = Chunk(
            chunk_id="test::1",
            domain="test",
            text="hello world",
            source_type="repo",
            source_file="file.md",
            line_start=5,
            line_end=15,
            chunk_type="method",
            class_name="Node3D",
            name="rotate_y",
            signature="void rotate_y(angle: float)",
            inherits_from=["Node"],
            docstring="Rotates on Y axis",
        )
        meta = c.to_chromadb_metadata()
        restored = Chunk.from_chromadb_metadata("test::1", "hello world", meta)
        assert restored.chunk_id == "test::1"
        assert restored.text == "hello world"
        assert restored.source_type == "repo"
        assert restored.source_file == "file.md"
        assert restored.line_start == 5
        assert restored.line_end == 15
        assert restored.chunk_type == "method"
        assert restored.class_name == "Node3D"
        assert restored.name == "rotate_y"
        assert restored.signature == "void rotate_y(angle: float)"
        assert restored.inherits_from == ["Node"]
        assert restored.docstring == "Rotates on Y axis"

    def test_from_metadata_no_optional_fields(self):
        meta = {
            "source_type": "repo",
            "domain": "test",
            "source_file": "f.md",
            "line_start": 0,
            "line_end": 0,
            "chunk_id_in_file": 0,
        }
        c = Chunk.from_chromadb_metadata("id", "text", meta)
        assert c.chunk_type is None
        assert c.class_name is None
        assert c.name is None
        assert c.inherits_from is None


class TestFallbackChunk:
    def test_empty_text_returns_empty_list(self):
        result = fallback_chunk("", domain="test", source_type="repo", source_file="f.md")
        assert result == []

    def test_short_text_single_chunk(self):
        text = "short text"
        result = fallback_chunk(text, domain="test", source_type="repo", source_file="f.md")
        assert len(result) == 1
        assert result[0].text == text
        assert result[0].domain == "test"
        assert result[0].source_file == "f.md"
        assert result[0].chunk_id == "test::fallback::0"

    def test_long_text_multiple_chunks(self):
        # Use small chunk_size to produce multiple chunks without huge text
        text = "A" * 250
        result = fallback_chunk(
            text, domain="test", source_type="repo", source_file="f.md",
            chunk_size=100, overlap=20,
        )
        # Chunks: [0:100], [80:180], [160:250] → 3 chunks
        assert len(result) == 3
        assert result[0].chunk_id == "test::fallback::0"
        assert result[1].chunk_id == "test::fallback::1"
        assert result[2].chunk_id == "test::fallback::2"

    def test_chunk_line_numbers_increment(self):
        text = "line1\nline2\nline3\nline4\nline5"
        result = fallback_chunk(
            text, domain="test", source_type="repo", source_file="f.md",
            chunk_size=100, overlap=20,
        )
        # each chunk should have line_start <= line_end
        for c in result:
            assert c.line_start >= 1
            assert c.line_end >= c.line_start

    def test_chunk_id_in_file_increments(self):
        text = "A" * 250
        result = fallback_chunk(
            text, domain="test", source_type="repo", source_file="f.md",
            chunk_size=100, overlap=20,
        )
        for i, c in enumerate(result):
            assert c.chunk_id_in_file == i

    def test_default_chunk_and_overlap_constants(self):
        assert FALLBACK_CHUNK_CHARS == 8000
        assert FALLBACK_OVERLAP_CHARS == 800
```

- [ ] **Step 3: Run all unit tests so far**

```bash
cd /Users/noahk/Documents/work/knowledge-hub
.venv/bin/pytest tests/unit/ -v -m unit
```

Expected: all tests PASS.

- [ ] **Step 4: Commit**

```bash
git add tests/unit/test_tools.py tests/unit/test_parser_base.py
git commit -m "test(unit): add domain scoping, category validation, and parser_base tests"
```

---

## Task 5: Unit Tests — RRF fusion

**Files:**
- Create: `tests/unit/test_rrf_fusion.py`

- [ ] **Step 1: Write tests/unit/test_rrf_fusion.py**

```python
"""Unit tests for hybrid_search.rrf_fusion — pure function, no models needed."""

from hybrid_search import rrf_fusion


def test_empty_inputs_returns_empty():
    assert rrf_fusion([], []) == []


def test_only_sparse_results():
    sparse = [{"chunk_id": "A", "score": 5.0}]
    results = rrf_fusion(sparse, [])
    assert len(results) == 1
    assert results[0]["chunk_id"] == "A"
    assert results[0]["score"] > 0
    assert "bm25" in results[0]["stage1_sources"]


def test_only_dense_results():
    dense = [{"chunk_id": "B", "score": 0.9, "text": "hello"}]
    results = rrf_fusion([], dense)
    assert len(results) == 1
    assert results[0]["chunk_id"] == "B"
    assert "semantic" in results[0]["stage1_sources"]
    assert results[0]["text"] == "hello"


def test_same_chunk_in_both_sources():
    sparse = [{"chunk_id": "A", "score": 5.0}]
    dense = [{"chunk_id": "A", "score": 0.9, "text": "hello"}]
    results = rrf_fusion(sparse, dense)
    assert len(results) == 1
    assert results[0]["chunk_id"] == "A"
    assert "bm25" in results[0]["stage1_sources"]
    assert "semantic" in results[0]["stage1_sources"]


def test_different_chunks_in_sources():
    sparse = [{"chunk_id": "A", "score": 5.0}]
    dense = [{"chunk_id": "B", "score": 0.9, "text": "hello"}]
    results = rrf_fusion(sparse, dense)
    assert len(results) == 2
    # Both should have positive scores
    assert results[0]["score"] > 0
    assert results[1]["score"] > 0
    # Ranks assigned
    assert results[0]["rank"] == 1
    assert results[1]["rank"] == 2


def test_top_n_limits_results():
    sparse = [{"chunk_id": f"s{i}", "score": 10.0 - i} for i in range(10)]
    dense = [{"chunk_id": f"d{i}", "score": 0.9 - i * 0.05} for i in range(10)]
    results = rrf_fusion(sparse, dense, top_n=5)
    assert len(results) == 5


def test_score_is_rounded():
    sparse = [{"chunk_id": "A", "score": 5.0}]
    results = rrf_fusion(sparse, [])
    # score is rounded to 4 decimal places
    assert results[0]["score"] == round(results[0]["score"], 4)


def test_match_type_is_hybrid():
    sparse = [{"chunk_id": "A", "score": 5.0}]
    dense = [{"chunk_id": "A", "score": 0.9, "text": "hello"}]
    results = rrf_fusion(sparse, dense)
    assert results[0]["match_type"] == "hybrid"


def test_dense_metadata_propagated():
    dense = [{
        "chunk_id": "B", "score": 0.9, "text": "hello",
        "source_type": "repo", "domain": "test",
        "source_file": "file.md", "line_start": 1, "line_end": 5,
        "chunk_type": "method", "class_name": "Node3D",
        "name": "rotate", "signature": "void rotate()",
        "page_start": 42, "page_end": 43,
        "section_path": "Chapter 1 > Section 2",
    }]
    results = rrf_fusion([], dense)
    r = results[0]
    assert r["source_type"] == "repo"
    assert r["domain"] == "test"
    assert r["source_file"] == "file.md"
    assert r["page_start"] == 42
    assert r["section_path"] == "Chapter 1 > Section 2"
```

- [ ] **Step 2: Run RRF tests**

```bash
cd /Users/noahk/Documents/work/knowledge-hub
.venv/bin/pytest tests/unit/test_rrf_fusion.py -v -m unit
```

Expected: all tests PASS.

- [ ] **Step 3: Run all unit tests together to verify no interference**

```bash
.venv/bin/pytest tests/unit/ -v -m unit
```

Expected: all unit tests PASS.

- [ ] **Step 4: Commit**

```bash
git add tests/unit/test_rrf_fusion.py
git commit -m "test(unit): add RRF fusion logic tests"
```

---

## Task 6: Integration Test Fixtures (conftest.py)

**Files:**
- Create: `tests/conftest.py`

- [ ] **Step 1: Write tests/conftest.py**

```python
"""Shared pytest fixtures for Knowledge Hub tests.

Unit tests need no fixtures (pure functions).
Integration tests use `tmp_hub` and `dummy_domain` fixtures.
E2E tests use the real prebuilt index (no fixtures needed).
"""

import os
import sys
from pathlib import Path

import pytest

HUB_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def tmp_hub(tmp_path, monkeypatch):
    """Create a temporary HUB_ROOT-like directory structure and monkeypatch
    all module-level path constants.

    This allows integration tests to build a tiny ChromaDB index in an
    isolated tmp directory without touching the real chromadb_data/.
    """
    # Create directory structure
    (tmp_path / "domains").mkdir()
    (tmp_path / "chromadb_data").mkdir()
    (tmp_path / "scripts").mkdir()

    # Monkeypatch config paths
    from mcp_servers.knowledge_hub import config as cfg
    monkeypatch.setattr(cfg, "HUB_ROOT", tmp_path)
    monkeypatch.setattr(cfg, "DOMAINS_DIR", tmp_path / "domains")
    monkeypatch.setattr(cfg, "CHROMA_DIR", tmp_path / "chromadb_data")
    monkeypatch.setattr(cfg, "SCRIPTS_DIR", tmp_path / "scripts")

    # Monkeypatch model_manager paths (it imports from config at module load)
    import model_manager as mm
    monkeypatch.setattr(mm, "_chroma_clients", {})
    monkeypatch.setattr(mm, "_bm25_cache", __import__("collections").OrderedDict())

    # Monkeypatch bm25_search path function (it calls domain_bm25_path from config)
    # config.domain_bm25_path reads CHROMA_DIR, which we already patched
    # but bm25_search imported domain_bm25_path at module load — it reads
    # config.CHROMA_DIR dynamically via the function, so it's fine.

    # Clear the chroma clients cache so each test gets a fresh client
    yield tmp_path

    # Cleanup: close any chroma clients
    mm._chroma_clients.clear()
    mm._bm25_cache.clear()


@pytest.fixture
def dummy_domain(tmp_hub):
    """Create a minimal dummy domain with 3 small source files and 1 personal note.

    Returns the domain name ("dummy").
    """
    domain_dir = tmp_hub / "domains" / "dummy"
    sources_dir = domain_dir / "sources"
    personal_dir = domain_dir / "personal"
    sources_dir.mkdir(parents=True)
    personal_dir.mkdir(parents=True)

    # Write domain.md with Metadaten block
    (domain_dir / "domain.md").write_text("""# Domain: dummy

## Zweck
Test domain for integration tests.

## Metadaten
- Embedding-Model: all-mpnet-base-v2 (768 dims)
- Collection: dummy_knowledge
- ChromaDB-Path: chromadb_data/dummy/chroma/
- BM25-Path: chromadb_data/dummy/dummy_bm25.pkl
- Letztes Update: 2026-06-28

## Lizenz-Hinweis
Test data only.
""", encoding="utf-8")

    # Write 3 source files with distinct topics
    (sources_dir / "node3d-rotation.md").write_text("""# Node3D Rotation

The Node3D class in Godot provides methods to rotate 3D nodes.

## rotate_y(angle)
Rotates the node around the Y axis by the given angle in radians.

```gdscript
var node = get_node("Player")
node.rotate_y(deg_to_rad(90))
```

## rotate_x(angle)
Rotates the node around the X axis.

## set_rotation(rotation: Vector3)
Sets the rotation of the node to the given Vector3.
""", encoding="utf-8")

    (sources_dir / "camera-follow.md").write_text("""# Camera Follow

The Camera3D can follow a target node.

## make_current()
Marks this camera as the current active camera.

## follow_target(target: NodePath)
Makes the camera follow the specified target node, maintaining distance.
""", encoding="utf-8")

    (sources_dir / "audio-bus.md").write_text("""# Audio Bus

Audio buses in Godot route audio through effects.

## set_bus_volume(bus: int, volume: float)
Sets the volume of the specified audio bus.

## add_effect(effect: AudioEffect)
Adds an audio effect to the bus.
""", encoding="utf-8")

    # Write 1 personal note
    (personal_dir / "gotchas.md").write_text("""# Dummy Gotchas

## Node3D rotation gotcha
- **Datum:** 2026-06-28
- **Notiz:** rotate_y uses radians, not degrees. Use deg_to_rad() to convert.

## Camera follow gotcha
- **Datum:** 2026-06-28
- **Notiz:** Call make_current() after follow_target() or the camera won't activate.
""", encoding="utf-8")

    return "dummy"


@pytest.fixture
def indexed_dummy(dummy_domain):
    """Build the ChromaDB + BM25 index for the dummy domain.

    Requires sentence-transformers to be installed and the model to download
    on first run. Skips if not available.
    """
    pytest.importorskip("chromadb")
    pytest.importorskip("sentence_transformers")

    # Import after tmp_hub has patched paths
    import model_manager as mm
    from mcp_servers.knowledge_hub import config as cfg

    # get_domain_config reads domain.md from DOMAINS_DIR (patched)
    # get_embedder loads the model (not patched — real model)
    # get_chroma_client uses domain_chroma_path → patched CHROMA_DIR

    # We need to build the index using the real embed_index logic
    # but with patched paths. The easiest way is to call the functions directly.
    from parser_base import fallback_chunk, Chunk
    from bm25_search import build_bm25_index
    from model_manager import get_embedder, get_chroma_client

    domain = "dummy"
    domain_dir = cfg.DOMAINS_DIR / domain
    chunks = []

    # Parse sources
    sources_dir = domain_dir / "sources"
    if sources_dir.is_dir():
        for f in sorted(sources_dir.glob("*.md")):
            content = f.read_text(encoding="utf-8")
            fallback = fallback_chunk(content, domain=domain, source_type="repo", source_file=f.name)
            for i, c in enumerate(fallback):
                c.chunk_id = f"{domain}::fallback::repo::{f.stem}::{i}"
                c.chunk_id_in_file = i
            chunks.extend(fallback)

    # Parse personal
    personal_dir = domain_dir / "personal"
    if personal_dir.is_dir():
        for f in sorted(personal_dir.glob("*.md")):
            content = f.read_text(encoding="utf-8")
            category = f.stem
            fallback = fallback_chunk(content, domain=domain, source_type="personal", source_file=f.name)
            for i, c in enumerate(fallback):
                c.chunk_id = f"{domain}::personal::{category}::{i}"
                c.chunk_id_in_file = i
                c.name = category
            chunks.extend(fallback)

    assert len(chunks) > 0, "No chunks were created from dummy domain"

    # Embed and index
    model = get_embedder(domain)
    texts = [c.text for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=False)

    client = get_chroma_client(domain)
    collection_name = f"{domain}_knowledge"

    try:
        client.delete_collection(collection_name)
    except Exception:
        pass

    collection = client.create_collection(
        name=collection_name,
        metadata={"domain": domain, "hnsw:space": "cosine"},
    )

    batch_size = 500
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        collection.add(
            ids=[c.chunk_id for c in batch],
            embeddings=embeddings[i:i + batch_size].tolist(),
            documents=[c.text for c in batch],
            metadatas=[c.to_chromadb_metadata() for c in batch],
        )

    build_bm25_index(domain, chunks)

    return domain
```

- [ ] **Step 2: Verify conftest imports cleanly**

```bash
cd /Users/noahk/Documents/work/knowledge-hub
.venv/bin/python3 -c "import tests.conftest; print('conftest imports OK')"
```

Expected: `conftest imports OK` (no exceptions).

- [ ] **Step 3: Commit**

```bash
git add tests/conftest.py
git commit -m "test: add shared pytest fixtures (tmp_hub, dummy_domain, indexed_dummy)"
```

---

## Task 7: Integration Tests — embed_index and bm25_search

**Files:**
- Create: `tests/integration/test_embed_index.py`
- Create: `tests/integration/test_bm25_search.py`

- [ ] **Step 1: Write tests/integration/test_embed_index.py**

```python
"""Integration tests for embed_index.build_index with a dummy domain."""

import pytest

pytestmark = pytest.mark.integration


def test_build_index_creates_collection(indexed_dummy):
    """Verify the collection was created and has chunks."""
    from model_manager import get_chroma_client

    client = get_chroma_client(indexed_dummy)
    collection = client.get_collection(f"{indexed_dummy}_knowledge")
    assert collection.count() > 0
    # Should have chunks from 3 source files + 1 personal note
    assert collection.count() >= 4


def test_build_index_chunks_have_metadata(indexed_dummy):
    """Verify chunks have correct source_type and source_file metadata."""
    from model_manager import get_chroma_client

    client = get_chroma_client(indexed_dummy)
    collection = client.get_collection(f"{indexed_dummy}_knowledge")
    result = collection.get(limit=5, include=["metadatas"])
    metas = result["metadatas"]
    assert len(metas) > 0
    for m in metas:
        assert m["source_type"] in ("repo", "personal")
        assert m["domain"] == indexed_dummy
        assert "source_file" in m
        assert "line_start" in m
        assert "line_end" in m


def test_build_index_bm25_pickle_exists(indexed_dummy):
    """Verify BM25 index file was created."""
    from mcp_servers.knowledge_hub.config import domain_bm25_path

    bm25_path = domain_bm25_path(indexed_dummy)
    assert bm25_path.exists()
    assert bm25_path.stat().st_size > 0


def test_build_index_chunk_ids_start_with_domain(indexed_dummy):
    """Verify chunk IDs follow the domain:: prefix convention."""
    from model_manager import get_chroma_client

    client = get_chroma_client(indexed_dummy)
    collection = client.get_collection(f"{indexed_dummy}_knowledge")
    result = collection.get(limit=10, include=["metadatas"])
    for cid in result["ids"]:
        assert cid.startswith(f"{indexed_dummy}::")
```

- [ ] **Step 2: Write tests/integration/test_bm25_search.py**

```python
"""Integration tests for bm25_search with a real (small) index."""

import pytest

pytestmark = pytest.mark.integration


def test_bm25_finds_node3d_results(indexed_dummy):
    """BM25 should find results for 'Node3D rotate'."""
    from bm25_search import bm25_search

    results = bm25_search(indexed_dummy, "Node3D rotate", top_k=10)
    assert len(results) >= 1
    assert results[0]["score"] > 0
    assert results[0]["match_type"] == "bm25"


def test_bm25_no_results_for_gibberish(indexed_dummy):
    """BM25 should return empty list for non-matching query."""
    from bm25_search import bm25_search

    results = bm25_search(indexed_dummy, "zzznonexistentword12345", top_k=10)
    assert results == []


def test_bm25_top_k_limits_results(indexed_dummy):
    """top_k should limit the number of results."""
    from bm25_search import bm25_search

    results = bm25_search(indexed_dummy, "Node3D", top_k=1)
    assert len(results) <= 1


def test_bm25_score_positive(indexed_dummy):
    """All returned results should have positive scores."""
    from bm25_search import bm25_search

    results = bm25_search(indexed_dummy, "camera follow", top_k=10)
    for r in results:
        assert r["score"] > 0


def test_bm25_tokenized_query(indexed_dummy):
    """BM25 should handle multi-word queries."""
    from bm25_search import bm25_search

    results = bm25_search(indexed_dummy, "audio bus volume", top_k=10)
    assert len(results) >= 1
```

- [ ] **Step 3: Run integration tests for embed_index + bm25**

```bash
cd /Users/noahk/Documents/work/knowledge-hub
.venv/bin/pytest tests/integration/test_embed_index.py tests/integration/test_bm25_search.py -v -m integration
```

Expected: all tests PASS (may take ~30-60s on first run due to model loading).

- [ ] **Step 4: Commit**

```bash
git add tests/integration/test_embed_index.py tests/integration/test_bm25_search.py
git commit -m "test(integration): add embed_index and bm25_search integration tests"
```

---

## Task 8: Integration Tests — embed_search, hybrid_search, personal_notes, migration

**Files:**
- Create: `tests/integration/test_embed_search.py`
- Create: `tests/integration/test_hybrid_search.py`
- Create: `tests/integration/test_personal_notes.py`
- Create: `tests/integration/test_migration.py`

- [ ] **Step 1: Write tests/integration/test_embed_search.py**

```python
"""Integration tests for embed_search.semantic_search with a real (small) index."""

import pytest

pytestmark = pytest.mark.integration


def test_semantic_search_returns_results(indexed_dummy):
    """Semantic search should return results for a relevant query."""
    from embed_search import semantic_search

    results = semantic_search(indexed_dummy, "How to rotate a 3D node", top_k=5)
    assert len(results) >= 1
    r = results[0]
    assert r["score"] > 0
    assert r["text"]  # non-empty
    assert r["source_file"]  # has source metadata


def test_semantic_search_has_correct_match_type(indexed_dummy):
    """All results should have match_type='semantic'."""
    from embed_search import semantic_search

    results = semantic_search(indexed_dummy, "camera", top_k=3)
    for r in results:
        assert r["match_type"] == "semantic"


def test_semantic_search_ranks_assigned(indexed_dummy):
    """Results should have incremental rank numbers."""
    from embed_search import semantic_search

    results = semantic_search(indexed_dummy, "audio", top_k=5)
    for i, r in enumerate(results):
        assert r["rank"] == i + 1


def test_semantic_search_chunk_ids(indexed_dummy):
    """All chunk IDs should start with the domain prefix."""
    from embed_search import semantic_search

    results = semantic_search(indexed_dummy, "Node3D", top_k=3)
    for r in results:
        assert r["chunk_id"].startswith(f"{indexed_dummy}::")
```

- [ ] **Step 2: Write tests/integration/test_hybrid_search.py**

```python
"""Integration tests for hybrid_search.search with all three modes."""

import pytest

pytestmark = pytest.mark.integration


def test_hybrid_search_returns_results(indexed_dummy):
    """Hybrid search should return results for a relevant query."""
    from hybrid_search import search

    result = search(indexed_dummy, "Node3D rotate", mode="hybrid", top_k=10)
    assert result["total_found"] >= 1
    assert "results" in result
    assert "query_time_ms" in result
    assert result["mode"] == "hybrid"


def test_exact_mode_returns_bm25_results(indexed_dummy):
    """Exact mode should return results with match_type='bm25'."""
    from hybrid_search import search

    result = search(indexed_dummy, "Node3D rotate", mode="exact", top_k=10)
    assert result["mode"] == "exact"
    if result["results"]:
        assert result["results"][0]["match_type"] == "bm25"


def test_semantic_mode_returns_semantic_results(indexed_dummy):
    """Semantic mode should return results with match_type='semantic'."""
    from hybrid_search import search

    result = search(indexed_dummy, "Node3D rotate", mode="semantic", top_k=10)
    assert result["mode"] == "semantic"
    if result["results"]:
        assert result["results"][0]["match_type"] == "semantic"


def test_hybrid_mode_returns_hybrid_results(indexed_dummy):
    """Hybrid mode should return results with match_type='hybrid'."""
    from hybrid_search import search

    result = search(indexed_dummy, "Node3D rotate", mode="hybrid", top_k=10)
    assert result["mode"] == "hybrid"
    if result["results"]:
        assert result["results"][0]["match_type"] == "hybrid"


def test_source_filter_repo_only(indexed_dummy):
    """source_filter=['repo'] should only return repo-sourced results."""
    from hybrid_search import search

    result = search(indexed_dummy, "Node3D", mode="hybrid", top_k=10, source_filter=["repo"])
    for r in result["results"]:
        assert r.get("source_type") == "repo"


def test_source_filter_personal_only(indexed_dummy):
    """source_filter=['personal'] should only return personal-sourced results."""
    from hybrid_search import search

    result = search(indexed_dummy, "Node3D", mode="hybrid", top_k=10, source_filter=["personal"])
    for r in result["results"]:
        assert r.get("source_type") == "personal"


def test_result_dict_structure(indexed_dummy):
    """Result dict should contain required keys."""
    from hybrid_search import search

    result = search(indexed_dummy, "camera", top_k=5)
    assert "results" in result
    assert "total_found" in result
    assert "mode" in result
    assert "query_time_ms" in result
    assert isinstance(result["total_found"], int)
    assert isinstance(result["query_time_ms"], int)


def test_results_have_text(indexed_dummy):
    """Each result should have non-empty text."""
    from hybrid_search import search

    result = search(indexed_dummy, "Node3D rotate", top_k=5)
    for r in result["results"]:
        assert r.get("text")  # non-empty string
```

- [ ] **Step 3: Write tests/integration/test_personal_notes.py**

```python
"""Integration tests for tools.py personal note functions."""

import pytest

pytestmark = pytest.mark.integration


def test_add_personal_note_success(dummy_domain):
    """add_personal_note should append to the category file."""
    from mcp_servers.knowledge_hub.tools import add_personal_note

    result = add_personal_note(
        domain=dummy_domain,
        topic="Test Topic",
        content="This is a test note.",
        category="gotchas",
    )
    assert result["status"] == "added"
    assert result["domain"] == dummy_domain
    assert "gotchas" in result["file"]


def test_list_personal_notes_returns_entries(dummy_domain):
    """list_personal_notes should parse the notes file."""
    from mcp_servers.knowledge_hub.tools import add_personal_note, list_personal_notes

    add_personal_note(dummy_domain, "Topic A", "Content A", "gotchas")
    add_personal_note(dummy_domain, "Topic B", "Content B", "tips")

    result = list_personal_notes(dummy_domain)
    assert result["domain"] == dummy_domain
    assert "gotchas" in result["notes"]
    assert "tips" in result["notes"]
    assert len(result["notes"]["gotchas"]) >= 1
    assert len(result["notes"]["tips"]) >= 1


def test_add_personal_note_invalid_category(dummy_domain):
    """Invalid category name should return an error dict."""
    from mcp_servers.knowledge_hub.tools import add_personal_note

    result = add_personal_note(dummy_domain, "T", "C", "bad/cat")
    assert "error" in result


def test_add_personal_note_uppercase_category_rejected(dummy_domain):
    """Uppercase category should be rejected by the regex."""
    from mcp_servers.knowledge_hub.tools import add_personal_note

    result = add_personal_note(dummy_domain, "T", "C", "UPPERCASE")
    assert "error" in result


def test_list_personal_notes_category_filter(dummy_domain):
    """list_personal_notes with category filter should return only that category."""
    from mcp_servers.knowledge_hub.tools import add_personal_note, list_personal_notes

    add_personal_note(dummy_domain, "Topic A", "Content A", "gotchas")
    add_personal_note(dummy_domain, "Topic B", "Content B", "tips")

    result = list_personal_notes(dummy_domain, category="gotchas")
    assert "gotchas" in result["notes"]
    assert "tips" not in result["notes"]


def test_list_personal_notes_nonexistent_domain():
    """list_personal_notes on a nonexistent domain should return error."""
    from mcp_servers.knowledge_hub.tools import list_personal_notes

    result = list_personal_notes("totally_nonexistent_domain_xyz")
    assert "error" in result
```

- [ ] **Step 4: Write tests/integration/test_migration.py**

```python
"""Integration tests for migration.migrate_legacy_layout.

Uses tmp_path to simulate legacy and per-domain layouts without touching
the real chromadb_data/.
"""

import pickle
import pytest
from pathlib import Path

pytestmark = pytest.mark.integration


def test_migration_no_chroma_dir(tmp_path, monkeypatch):
    """If chromadb_data doesn't exist, migration returns False."""
    import migration
    monkeypatch.setattr(migration, "CHROMA_DIR", tmp_path / "nonexistent")
    assert migration.migrate_legacy_layout() is False


def test_migration_empty_chroma_dir(tmp_path, monkeypatch):
    """Empty chromadb_data → nothing to migrate → False."""
    (tmp_path / "chroma").mkdir()
    import migration
    monkeypatch.setattr(migration, "CHROMA_DIR", tmp_path / "chroma")
    assert migration.migrate_legacy_layout() is False


def test_migration_idempotent_empty(tmp_path, monkeypatch):
    """Running migration twice on empty dir should both return False."""
    (tmp_path / "chroma").mkdir()
    import migration
    monkeypatch.setattr(migration, "CHROMA_DIR", tmp_path / "chroma")
    assert migration.migrate_legacy_layout() is False
    assert migration.migrate_legacy_layout() is False


def test_migration_moves_legacy_collection(tmp_path, monkeypatch):
    """Legacy <domain>_knowledge/ dir should be moved to <domain>/chroma/."""
    chroma = tmp_path / "chroma"
    chroma.mkdir()
    # Create legacy collection dir
    legacy_coll = chroma / "testdomain_knowledge"
    legacy_coll.mkdir()
    (legacy_coll / "somefile.txt").write_text("data")

    import migration
    monkeypatch.setattr(migration, "CHROMA_DIR", chroma)
    result = migration.migrate_legacy_layout()
    assert result is True
    # New location
    assert (chroma / "testdomain" / "chroma" / "testdomain_knowledge" / "somefile.txt").exists()
    # Old location gone
    assert not legacy_coll.exists()


def test_migration_moves_legacy_bm25(tmp_path, monkeypatch):
    """Legacy <domain>_bm25.pkl should be moved to <domain>/."""
    chroma = tmp_path / "chroma"
    chroma.mkdir()
    # Create legacy collection + bm25
    (chroma / "testdomain_knowledge").mkdir()
    (chroma / "testdomain_knowledge" / "f.txt").write_text("x")
    legacy_bm25 = chroma / "testdomain_bm25.pkl"
    with open(legacy_bm25, "wb") as f:
        pickle.dump({"index": "fake"}, f)

    import migration
    monkeypatch.setattr(migration, "CHROMA_DIR", chroma)
    result = migration.migrate_legacy_layout()
    assert result is True
    assert (chroma / "testdomain" / "testdomain_bm25.pkl").exists()
    assert not legacy_bm25.exists()


def test_migration_creates_backup(tmp_path, monkeypatch):
    """Migration should create a _legacy_backup/ with copies."""
    chroma = tmp_path / "chroma"
    chroma.mkdir()
    (chroma / "td_knowledge").mkdir()
    (chroma / "td_knowledge" / "f.txt").write_text("x")

    import migration
    monkeypatch.setattr(migration, "CHROMA_DIR", chroma)
    migration.migrate_legacy_layout()
    assert (chroma / "_legacy_backup" / "td_knowledge" / "f.txt").exists()


def test_migration_skips_already_migrated(tmp_path, monkeypatch):
    """If new layout already exists, migration should skip (no error)."""
    chroma = tmp_path / "chroma"
    chroma.mkdir()
    # Create both legacy AND new layout
    (chroma / "td_knowledge").mkdir()
    (chroma / "td_knowledge" / "old.txt").write_text("old")
    (chroma / "td" / "chroma" / "td_knowledge").mkdir(parents=True)
    (chroma / "td" / "chroma" / "td_knowledge" / "new.txt").write_text("new")

    import migration
    monkeypatch.setattr(migration, "CHROMA_DIR", chroma)
    result = migration.migrate_legacy_layout()
    # First pass skips because new collection dir exists → False from first pass
    # But orphaned BM25 pass might also be False
    assert result is False
    # Legacy dir should still be there (not moved)
    assert (chroma / "td_knowledge").exists()


def test_migration_orphaned_bm25_second_pass(tmp_path, monkeypatch):
    """Orphaned BM25 pkl (collection already migrated) should be moved."""
    chroma = tmp_path / "chroma"
    chroma.mkdir()
    # Domain dir exists (collection already migrated) but BM25 still at root
    (chroma / "td" / "chroma").mkdir(parents=True)
    legacy_bm25 = chroma / "td_bm25.pkl"
    with open(legacy_bm25, "wb") as f:
        pickle.dump({"index": "fake"}, f)

    import migration
    monkeypatch.setattr(migration, "CHROMA_DIR", chroma)
    result = migration.migrate_legacy_layout()
    assert result is True
    assert (chroma / "td" / "td_bm25.pkl").exists()
    assert not legacy_bm25.exists()
```

- [ ] **Step 5: Run all integration tests**

```bash
cd /Users/noahk/Documents/work/knowledge-hub
.venv/bin/pytest tests/integration/ -v -m integration
```

Expected: all tests PASS (~60-90s including model loading on first run).

- [ ] **Step 6: Commit**

```bash
git add tests/integration/test_embed_search.py tests/integration/test_hybrid_search.py tests/integration/test_personal_notes.py tests/integration/test_migration.py
git commit -m "test(integration): add embed_search, hybrid_search, personal_notes, migration tests"
```

---

## Task 9: E2E Regression Tests (real index)

**Files:**
- Create: `tests/e2e/test_godot_regression.py`
- Create: `tests/e2e/test_davinci_regression.py`

- [ ] **Step 1: Write tests/e2e/test_godot_regression.py**

```python
"""E2E regression tests against the prebuilt Godot index.

These tests require chromadb_data/godot/ to exist (prebuilt via
embed_index.py --domain godot). They verify that the real index returns
content-relevant results, not just any results.

Run: pytest tests/e2e/test_godot_regression.py -v -m e2e
"""

import pytest

from pathlib import Path

HUB_ROOT = Path(__file__).resolve().parent.parent.parent
GODOT_INDEX = HUB_ROOT / "chromadb_data" / "godot" / "chroma"

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.skipif(
        not GODOT_INDEX.exists(),
        reason="Godot index not built. Run: python scripts/embed_index.py --domain godot",
    ),
]


def test_godot_node3d_search_finds_relevant_results():
    """Search for 'Node3D rotate' should return results mentioning Node3D/Spatial/rotate."""
    from hybrid_search import search

    result = search("godot", "Node3D rotate", mode="hybrid", top_k=10)
    assert result["total_found"] >= 1
    # Content relevance: top 3 results should mention the topic
    top3_text = " ".join(r.get("text", "") for r in result["results"][:3]).lower()
    assert any(kw in top3_text for kw in ["node3d", "spatial", "rotate", "rotation"])


def test_godot_search_returns_metadata():
    """First result should have source_file and non-empty text."""
    from hybrid_search import search

    result = search("godot", "Node3D", top_k=5)
    assert result["total_found"] >= 1
    r = result["results"][0]
    assert r.get("source_file")
    assert r.get("text")
    assert r["chunk_id"].startswith("godot::")


def test_godot_all_search_modes_work():
    """exact, semantic, and hybrid modes should all return results."""
    from hybrid_search import search

    for mode in ["exact", "semantic", "hybrid"]:
        result = search("godot", "Node3D rotate", mode=mode, top_k=5)
        assert result["total_found"] >= 1, f"mode={mode} returned no results"


def test_godot_hybrid_under_10_seconds():
    """Hybrid search should complete in under 10 seconds."""
    from hybrid_search import search

    result = search("godot", "Node3D rotate", mode="hybrid", top_k=10)
    assert result["query_time_ms"] <= 10000


def test_godot_search_result_structure():
    """Result dict should have all required keys."""
    from hybrid_search import search

    result = search("godot", "camera", top_k=3)
    assert "results" in result
    assert "total_found" in result
    assert "mode" in result
    assert "query_time_ms" in result
    assert isinstance(result["results"], list)
```

- [ ] **Step 2: Write tests/e2e/test_davinci_regression.py**

```python
"""E2E regression tests against the prebuilt DaVinci Resolve index.

These tests require chromadb_data/davinci_resolve/ to exist (prebuilt via
embed_index.py --domain davinci_resolve). They verify that the real index
returns content-relevant results from the 10 Blackmagic PDFs.

Run: pytest tests/e2e/test_davinci_regression.py -v -m e2e
"""

import pytest
from pathlib import Path

HUB_ROOT = Path(__file__).resolve().parent.parent.parent
DAVINCI_INDEX = HUB_ROOT / "chromadb_data" / "davinci_resolve" / "chroma"

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.skipif(
        not DAVINCI_INDEX.exists(),
        reason="DaVinci index not built. Run: python scripts/embed_index.py --domain davinci_resolve",
    ),
]


def test_davinci_trim_clip_search_finds_relevant_results():
    """Search for 'trim clip edit' should return results about trimming/editing."""
    from hybrid_search import search

    result = search("davinci_resolve", "trim clip edit", mode="hybrid", top_k=10)
    assert result["total_found"] >= 1
    top3_text = " ".join(r.get("text", "") for r in result["results"][:3]).lower()
    assert any(kw in top3_text for kw in ["trim", "edit", "clip"])


def test_davinci_color_grading_search():
    """Search for 'color grading primary correction' should find color-related content."""
    from hybrid_search import search

    result = search("davinci_resolve", "color grading primary correction", mode="hybrid", top_k=10)
    assert result["total_found"] >= 1
    top3_text = " ".join(r.get("text", "") for r in result["results"][:3]).lower()
    assert any(kw in top3_text for kw in ["color", "primary", "correction", "grade"])


def test_davinci_render_deliver_search():
    """Search for 'render deliver settings' should find deliver-related content."""
    from hybrid_search import search

    result = search("davinci_resolve", "render deliver settings", mode="hybrid", top_k=10)
    assert result["total_found"] >= 1
    top3_text = " ".join(r.get("text", "") for r in result["results"][:3]).lower()
    assert any(kw in top3_text for kw in ["deliver", "render", "export", "settings"])


def test_davinci_search_returns_pdf_metadata():
    """At least one result should have page_start set (PDF page number)."""
    from hybrid_search import search

    result = search("davinci_resolve", "trim clip", top_k=10)
    has_page = any(r.get("page_start") is not None for r in result["results"])
    assert has_page, "No result had page_start metadata (expected from PDF source)"


def test_davinci_hybrid_under_10_seconds():
    """Hybrid search should complete in under 10 seconds."""
    from hybrid_search import search

    result = search("davinci_resolve", "trim clip edit", mode="hybrid", top_k=10)
    assert result["query_time_ms"] <= 10000


def test_davinci_all_search_modes_work():
    """exact, semantic, and hybrid modes should all return results."""
    from hybrid_search import search

    for mode in ["exact", "semantic", "hybrid"]:
        result = search("davinci_resolve", "color grading", mode=mode, top_k=5)
        assert result["total_found"] >= 1, f"mode={mode} returned no results"


def test_davinci_result_structure():
    """Result dict should have all required keys."""
    from hybrid_search import search

    result = search("davinci_resolve", "fairlight audio", top_k=3)
    assert "results" in result
    assert "total_found" in result
    assert "mode" in result
    assert "query_time_ms" in result
```

- [ ] **Step 3: Run E2E tests**

```bash
cd /Users/noahk/Documents/work/knowledge-hub
.venv/bin/pytest tests/e2e/ -v -m e2e
```

Expected: all tests PASS (if indexes exist). If indexes don't exist, tests are skipped.

- [ ] **Step 4: Commit**

```bash
git add tests/e2e/test_godot_regression.py tests/e2e/test_davinci_regression.py
git commit -m "test(e2e): add regression tests against real godot and davinci indexes"
```

---

## Task 10: MCP Contract Tests

**Files:**
- Create: `tests/mcp/test_mcp_contract.py`

- [ ] **Step 1: Write tests/mcp/test_mcp_contract.py**

```python
"""MCP Contract Tests — verify the 6 tool functions return correct contracts.

Calls the actual tool functions (not via stdio transport) and verifies
return types, required keys, and error handling.

Run: pytest tests/mcp/test_mcp_contract.py -v -m mcp
"""

import pytest

pytestmark = pytest.mark.mcp


@pytest.fixture(autouse=True)
def reset_scope():
    """Reset domain scope before and after each test."""
    from mcp_servers.knowledge_hub.tools import set_domain_scope
    set_domain_scope(None)
    yield
    set_domain_scope(None)


class TestListDomains:
    def test_list_domains_returns_list(self):
        """list_domains should return a list of strings."""
        from mcp_servers.knowledge_hub.tools import list_domains

        result = list_domains()
        assert isinstance(result, list)
        for d in result:
            assert isinstance(d, str)

    def test_list_scoped_domains_unscoped(self):
        """Without scope, list_scoped_domains == list_domains."""
        from mcp_servers.knowledge_hub.tools import list_domains, list_scoped_domains

        assert list_scoped_domains() == list_domains()

    def test_list_scoped_domains_with_scope(self):
        """With scope, only scoped domains are returned."""
        from mcp_servers.knowledge_hub.tools import list_domains, set_domain_scope, list_scoped_domains

        all_domains = list_domains()
        if not all_domains:
            pytest.skip("no domains available")
        target = all_domains[0]
        set_domain_scope([target])
        assert list_scoped_domains() == [target]


class TestSearchKnowledge:
    def test_search_returns_dict_with_required_keys(self):
        """search_knowledge should return a dict with results, total_found, mode, query_time_ms."""
        from mcp_servers.knowledge_hub.tools import list_domains, search_knowledge

        domains = list_domains()
        if not domains:
            pytest.skip("no domains available")
        result = search_knowledge(domain=domains[0], query="test", max_results=3)
        assert isinstance(result, dict)
        assert "results" in result
        assert "total_found" in result
        assert "mode" in result
        assert "query_time_ms" in result

    def test_search_out_of_scope_returns_error(self):
        """Out-of-scope domain should return an error dict, not raise."""
        from mcp_servers.knowledge_hub.tools import list_domains, set_domain_scope, search_knowledge

        all_domains = list_domains()
        if len(all_domains) < 2:
            pytest.skip("need at least 2 domains")
        set_domain_scope([all_domains[0]])
        result = search_knowledge(domain=all_domains[1], query="test")
        assert "error" in result
        assert all_domains[0] in result["error"]


class TestGetDomainStatus:
    def test_status_for_single_domain(self):
        """get_domain_status(domain) should return a dict with status keys."""
        from mcp_servers.knowledge_hub.tools import list_domains, get_domain_status

        domains = list_domains()
        if not domains:
            pytest.skip("no domains available")
        result = get_domain_status(domains[0])
        assert domains[0] in result
        info = result[domains[0]]
        assert "sources" in info
        assert "personal_notes" in info
        assert "index_exists" in info
        assert "index_size_mb" in info

    def test_status_for_all_domains(self):
        """get_domain_status() (no arg) should return all scoped domains."""
        from mcp_servers.knowledge_hub.tools import list_scoped_domains, get_domain_status

        result = get_domain_status()
        assert isinstance(result, dict)
        for d in list_scoped_domains():
            assert d in result

    def test_status_out_of_scope_returns_error(self):
        """Out-of-scope domain should return an error dict."""
        from mcp_servers.knowledge_hub.tools import list_domains, set_domain_scope, get_domain_status

        all_domains = list_domains()
        if len(all_domains) < 2:
            pytest.skip("need at least 2 domains")
        set_domain_scope([all_domains[0]])
        result = get_domain_status(all_domains[1])
        assert "error" in result


class TestAddPersonalNote:
    def test_add_note_returns_status_added(self, tmp_path, monkeypatch):
        """add_personal_note should return status='added'."""
        from mcp_servers.knowledge_hub.tools import add_personal_note

        # Create a fake domain
        domain_dir = tmp_path / "domains" / "testdomain"
        (domain_dir / "personal").mkdir(parents=True)
        (domain_dir / "domain.md").write_text("# Domain: testdomain\n")

        from mcp_servers.knowledge_hub import config
        monkeypatch.setattr(config, "DOMAINS_DIR", tmp_path / "domains")

        result = add_personal_note("testdomain", "Topic", "Content", "gotchas")
        assert result["status"] == "added"

    def test_add_note_invalid_category(self, tmp_path, monkeypatch):
        """Invalid category should return error."""
        from mcp_servers.knowledge_hub.tools import add_personal_note

        domain_dir = tmp_path / "domains" / "testdomain"
        (domain_dir / "personal").mkdir(parents=True)
        (domain_dir / "domain.md").write_text("# Domain: testdomain\n")

        from mcp_servers.knowledge_hub import config
        monkeypatch.setattr(config, "DOMAINS_DIR", tmp_path / "domains")

        result = add_personal_note("testdomain", "T", "C", "bad/cat")
        assert "error" in result


class TestListPersonalNotes:
    def test_list_notes_nonexistent_domain(self):
        """list_personal_notes on nonexistent domain should return error."""
        from mcp_servers.knowledge_hub.tools import list_personal_notes

        result = list_personal_notes("totally_nonexistent_xyz")
        assert "error" in result


class TestUpdateDomain:
    def test_update_nonexistent_domain(self):
        """update_domain on nonexistent domain should return error (no update.sh)."""
        from mcp_servers.knowledge_hub.tools import update_domain

        result = update_domain("totally_nonexistent_xyz")
        assert "error" in result
        assert "update.sh" in result["error"]
```

- [ ] **Step 2: Run MCP contract tests**

```bash
cd /Users/noahk/Documents/work/knowledge-hub
.venv/bin/pytest tests/mcp/ -v -m mcp
```

Expected: all tests PASS.

- [ ] **Step 3: Commit**

```bash
git add tests/mcp/test_mcp_contract.py
git commit -m "test(mcp): add MCP contract tests for all 6 tool functions"
```

---

## Task 11: Full Test Run and Coverage Check

**Files:** none (validation only)

- [ ] **Step 1: Run ALL tests together**

```bash
cd /Users/noahk/Documents/work/knowledge-hub
.venv/bin/pytest -v
```

Expected: all tests PASS (unit fast, integration ~60s, e2e ~30s, mcp ~10s).

- [ ] **Step 2: Run with coverage**

```bash
.venv/bin/pytest --cov=scripts --cov=mcp_servers/knowledge_hub --cov-report=term-missing -q
```

Expected: Coverage > 60% for `scripts/` and `mcp_servers/knowledge_hub/`.

- [ ] **Step 3: Run only unit tests to confirm they're fast**

```bash
.venv/bin/pytest -m unit -q
```

Expected: completes in < 10 seconds.

- [ ] **Step 4: Document test running in README or docs**

Add a `## Testing` section to the project README (or create `docs/testing.md`):

```markdown
## Testing

The Knowledge Hub has a four-layer test suite:

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run only fast unit tests (< 10s)
pytest -m unit

# Run integration tests with temp ChromaDB (~60s)
pytest -m integration

# Run E2E regression against real indexes (~30s, requires prebuilt indexes)
pytest -m e2e

# Run MCP contract tests (~10s)
pytest -m mcp

# Run with coverage report
pytest --cov=scripts --cov=mcp_servers/knowledge_hub --cov-report=term-missing
```

E2E tests require prebuilt indexes:
```bash
python scripts/embed_index.py --domain godot
python scripts/embed_index.py --domain davinci_resolve
```
```

- [ ] **Step 5: Commit**

```bash
git add docs/testing.md  # or README.md if that's where it went
git commit -m "docs: document test suite usage and running instructions"
```

---

## Self-Review Checklist

After all tasks:

- [ ] **Spec coverage:**
  - Schicht 1 (Unit): Tasks 2, 3, 4, 5
  - Schicht 2 (Integration): Tasks 6, 7, 8
  - Schicht 3 (E2E): Task 9
  - Schicht 4 (MCP): Task 10
  - Test infrastructure: Task 1
  - Full run + coverage: Task 11
  - All 4 layers covered ✅

- [ ] **No placeholders:** every code block is complete and runnable

- [ ] **Type consistency:**
  - `search()` signature: `search(domain, query, mode="hybrid", top_k=10, source_filter=None)` — consistent across all test files
  - `rrf_fusion()` signature: `rrf_fusion(sparse_results, dense_results, k=60, top_n=50)` — matches source
  - `set_domain_scope()` / `_check_domain_scope()` — consistent in tools tests
  - `bm25_cache_get/set/invalidate` — consistent in model_manager tests

- [ ] **Import paths:** tests import from `hybrid_search`, `bm25_search`, `embed_search`, `model_manager`, `parser_base`, `mcp_servers.knowledge_hub.tools`, `mcp_servers.knowledge_hub.config` — all verified against the source code

- [ ] **Fixture isolation:** `tmp_hub` monkeypatches config paths and clears model_manager caches; `reset_scope` fixture resets domain scope

- [ ] **Skip conditions:** E2E tests skip if index not built; domain-specific unit tests skip if domain.md doesn't exist
