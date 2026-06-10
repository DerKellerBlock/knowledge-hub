# Retrieval 2.0 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace ripgrep with BM25, add plugin-based structured parsing (Godot RST reference impl), add cross-encoder reranking, and deduplicate search logic from MCP tools.

**Architecture:** Plugin system via `parser_base.py` (Chunk dataclass + DomainParser ABC). Godot parser as first implementation. BM25 (`rank_bm25` + pickle) replaces ripgrep entirely. Cross-encoder (`ms-marco-MiniLM-L-12-v2`) re-ranks fused Stage-1 results. `tools.py` delegates all search to `scripts/` (no duplicate logic).

**Tech Stack:** Python 3.11+, rank-bm25, sentence-transformers (CrossEncoder), chromadb, pickle, importlib

**Spec:** `docs/superpowers/specs/2026-06-09-retrieval-2-0-design.md`

---

## File Structure Overview

| File | Action | Responsibility |
|------|--------|----------------|
| `scripts/parser_base.py` | **Create** | Chunk dataclass + DomainParser ABC + fallback chunker |
| `scripts/bm25_search.py` | **Create** | BM25 index loading, search, field-boosting |
| `scripts/reranker.py` | **Create** | Cross-Encoder singleton + rerank function |
| `domains/godot/parser.py` | **Create** | Godot RST structured parser |
| `scripts/embed_index.py` | **Modify** | Plugin discovery, Chunk objects, BM25 index build |
| `scripts/hybrid_search.py` | **Modify** | BM25 replaces ripgrep, cross-encoder reranking |
| `scripts/embed_search.py` | **Modify** | Return new Chunk fields from ChromaDB metadata |
| `mcp_servers/knowledge_hub/tools.py` | **Modify** | Remove ripgrep + duplicate RRF, delegate to scripts |
| `mcp_servers/knowledge_hub/config.py` | **Modify** | New paths + model config |
| `mcp_servers/knowledge_hub/server.py` | **Modify** | Updated tool descriptions |
| `requirements.txt` | **Modify** | Add `rank-bm25` |
| `domains/godot/domain.md` | **Modify** | Parser field, updated metadata |

---

### Task 1: Create parser_base.py — Chunk dataclass + DomainParser interface

**Files:**
- Create: `scripts/parser_base.py`

- [ ] **Step 1: Write parser_base.py**

```python
#!/usr/bin/env python3
"""
Plugin system for domain-specific structured parsing.

Defines the Chunk dataclass (unified schema for all chunks) and the
DomainParser abstract base class. Domains MAY provide a parser.py that
subclasses DomainParser. If no parser exists, fallback_chunk() is used.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class Chunk:
    """Unified chunk schema for indexing, search, and reranking.

    Pflichtfelder (immer befüllt):
        chunk_id, domain, text, source_type, source_file, line_start, line_end

    Struktur-Felder (None bei Fallback-Chunking):
        chunk_type, class_name, name, signature, inherits_from, docstring
    """

    # Pflichtfelder
    chunk_id: str
    domain: str
    text: str
    source_type: str  # "repo" | "personal"

    # Struktur-Felder (optional)
    chunk_type: str | None = None       # "class" | "method" | "property" | "signal" | "enum" | "section"
    class_name: str | None = None       # z.B. "Node3D"
    name: str | None = None             # Methoden-/Property-Name, z.B. "rotate_y"
    signature: str | None = None        # "void rotate_y(angle: float)"
    inherits_from: list[str] | None = None  # ["Node"]
    docstring: str | None = None        # Beschreibungstext

    # Position
    source_file: str = ""
    line_start: int = 0
    line_end: int = 0

    # Intern (wird von embed_index.py gesetzt)
    chunk_id_in_file: int = 0

    def to_chromadb_metadata(self) -> dict:
        """Convert to ChromaDB-compatible metadata dict.

        ChromaDB metadata only supports str, int, float, bool — no lists or None.
        """
        meta = {
            "source_type": self.source_type,
            "domain": self.domain,
            "source_file": self.source_file,
            "line_start": self.line_start,
            "line_end": self.line_end,
            "chunk_id_in_file": self.chunk_id_in_file,
        }
        if self.chunk_type:
            meta["chunk_type"] = self.chunk_type
        if self.class_name:
            meta["class_name"] = self.class_name
        if self.name:
            meta["name"] = self.name
        if self.signature:
            meta["signature"] = self.signature
        if self.inherits_from:
            meta["inherits_from"] = "::".join(self.inherits_from)
        if self.docstring:
            meta["docstring"] = self.docstring[:500]
        return meta

    @staticmethod
    def from_chromadb_metadata(chunk_id: str, text: str, meta: dict) -> "Chunk":
        """Reconstruct a Chunk from ChromaDB metadata (used in search results)."""
        inherits = None
        if meta.get("inherits_from"):
            inherits = meta["inherits_from"].split("::")
        return Chunk(
            chunk_id=chunk_id,
            domain=meta.get("domain", ""),
            text=text,
            source_type=meta.get("source_type", "unknown"),
            chunk_type=meta.get("chunk_type"),
            class_name=meta.get("class_name"),
            name=meta.get("name"),
            signature=meta.get("signature"),
            inherits_from=inherits,
            docstring=meta.get("docstring"),
            source_file=meta.get("source_file", ""),
            line_start=meta.get("line_start", 0),
            line_end=meta.get("line_end", 0),
        )


class DomainParser(ABC):
    """Base class for domain-specific parsers.

    Subclass this in domains/<name>/parser.py and name the class 'Parser'.
    """

    @abstractmethod
    def parse(self, file_path: str, content: str) -> list[Chunk]:
        """Parse source content into structured Chunk objects."""
        ...

    @property
    @abstractmethod
    def source_type_name(self) -> str:
        """Identifier, e.g. 'rst-godot'."""
        ...


# ── Fallback chunking ─────────────────────────────────────────────────────

FALLBACK_CHUNK_SIZE = 500   # approximate tokens
FALLBACK_CHUNK_OVERLAP = 100
CHARS_PER_TOKEN = 4
FALLBACK_CHUNK_CHARS = FALLBACK_CHUNK_SIZE * CHARS_PER_TOKEN       # 2000
FALLBACK_OVERLAP_CHARS = FALLBACK_CHUNK_OVERLAP * CHARS_PER_TOKEN  # 400


def fallback_chunk(
    text: str,
    domain: str,
    source_type: str,
    source_file: str,
    chunk_size: int = FALLBACK_CHUNK_CHARS,
    overlap: int = FALLBACK_OVERLAP_CHARS,
) -> list[Chunk]:
    """Sliding-window chunking (fallback when no parser exists)."""
    chunks = []
    start = 0
    chunk_idx = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk_text_slice = text[start:end]
        line_offset = text[:start].count("\n") + 1
        line_end = text[:end].count("\n") + 1

        chunks.append(Chunk(
            chunk_id=f"{domain}::fallback::{chunk_idx}",
            domain=domain,
            text=chunk_text_slice,
            source_type=source_type,
            source_file=source_file,
            line_start=line_offset,
            line_end=line_end,
            chunk_id_in_file=chunk_idx,
        ))

        chunk_idx += 1
        start += (chunk_size - overlap)

    return chunks
```

- [ ] **Step 2: Verify syntax**

Run: `python3 -m py_compile scripts/parser_base.py`
Expected: No output (success)

- [ ] **Step 3: Commit**

```bash
git add scripts/parser_base.py
git commit -m "feat: add parser_base.py with Chunk dataclass and DomainParser ABC"
```

---

### Task 2: Add rank-bm25 to requirements.txt

**Files:**
- Modify: `requirements.txt`

- [ ] **Step 1: Add dependency**

Append to `requirements.txt` after line 11 (`mcp>=1.0.0`):

```
rank-bm25>=0.2.2,<1.0.0
```

- [ ] **Step 2: Install dependency**

Run: `pip install rank-bm25>=0.2.2`
Expected: Successfully installed rank-bm25

- [ ] **Step 3: Verify import**

Run: `python3 -c "from rank_bm25 import BM25Okapi; print('OK')"`
Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add requirements.txt
git commit -m "feat: add rank-bm25 dependency for BM25 sparse retrieval"
```

---

### Task 3: Create bm25_search.py — BM25 indexing and search

**Files:**
- Create: `scripts/bm25_search.py`

- [ ] **Step 1: Write bm25_search.py**

```python
#!/usr/bin/env python3
"""
BM25 sparse retrieval for Knowledge Hub.

Usage:
  from bm25_search import build_bm25_index, bm25_search, tokenize

The BM25 index is built during embed_index.py and persisted via pickle to
chromadb_data/<domain>_bm25.pkl. Each query loads the index (cached in memory)
and returns scored chunk_ids.
"""

import pickle
import re
from pathlib import Path

import numpy as np
from rank_bm25 import BM25Okapi

HUB_ROOT = Path(__file__).resolve().parent.parent
CHROMA_DIR = HUB_ROOT / "chromadb_data"

# ── Caching ────────────────────────────────────────────────────────────────
_bm25_cache: dict[str, dict] = {}


def tokenize(text: str) -> list[str]:
    """Simple tokenizer: lowercase, split on non-alphanumeric."""
    return re.findall(r"\w+", text.lower())


def build_bm25_index(domain: str, chunks: list) -> None:
    """Build and persist a BM25 index from a list of Chunk objects.

    Args:
        domain: Domain name (e.g. 'godot')
        chunks: List of Chunk objects (from parser_base)

    Field-boosting: chunk.name (2x), chunk.signature (3x) tokens appended
    to increase their weight in the BM25 index.
    """
    corpus = []
    chunk_ids = []

    for chunk in chunks:
        tokens = tokenize(chunk.text)
        if chunk.name:
            tokens.extend(tokenize(chunk.name) * 2)
        if chunk.signature:
            tokens.extend(tokenize(chunk.signature) * 3)
        corpus.append(tokens)
        chunk_ids.append(chunk.chunk_id)

    if not corpus:
        return

    bm25 = BM25Okapi(corpus)
    index_path = CHROMA_DIR / f"{domain}_bm25.pkl"
    with open(index_path, "wb") as f:
        pickle.dump({"index": bm25, "chunk_ids": chunk_ids}, f)

    # Invalidate cache for this domain
    _bm25_cache.pop(domain, None)


def _load_index(domain: str) -> dict:
    """Load BM25 index from pickle, with in-memory caching."""
    if domain in _bm25_cache:
        return _bm25_cache[domain]

    index_path = CHROMA_DIR / f"{domain}_bm25.pkl"
    if not index_path.exists():
        raise FileNotFoundError(
            f"BM25 index not found for domain '{domain}'. "
            f"Run embed_index.py --domain {domain} first."
        )

    with open(index_path, "rb") as f:
        data = pickle.load(f)

    _bm25_cache[domain] = data
    return data


def bm25_search(domain: str, query: str, top_k: int = 100) -> list[dict]:
    """BM25 sparse retrieval with field boosting.

    Returns:
        [
            {"chunk_id": "godot::Node3D::method::rotate_y",
             "score": 12.45,
             "match_type": "bm25"},
            ...
        ]
    """
    data = _load_index(domain)
    bm25: BM25Okapi = data["index"]
    chunk_ids: list[str] = data["chunk_ids"]

    tokens = tokenize(query)
    scores = bm25.get_scores(tokens)

    # Get top-k indices by score
    if len(scores) == 0:
        return []

    top_indices = np.argsort(scores)[::-1][:top_k]

    return [
        {
            "chunk_id": chunk_ids[i],
            "score": float(scores[i]),
            "match_type": "bm25",
        }
        for i in top_indices
        if scores[i] > 0
    ]


def get_bm25_index_size_mb(domain: str) -> float:
    """Get BM25 index file size in MB."""
    index_path = CHROMA_DIR / f"{domain}_bm25.pkl"
    if index_path.exists():
        return round(index_path.stat().st_size / 1024 / 1024, 2)
    return 0.0
```

- [ ] **Step 2: Verify syntax**

Run: `python3 -m py_compile scripts/bm25_search.py`
Expected: No output

- [ ] **Step 3: Commit**

```bash
git add scripts/bm25_search.py
git commit -m "feat: add bm25_search.py with BM25 index build, caching, and search"
```

---

### Task 4: Create reranker.py — Cross-Encoder reranking

**Files:**
- Create: `scripts/reranker.py`

- [ ] **Step 1: Write reranker.py**

```python
#!/usr/bin/env python3
"""
Cross-Encoder reranking for Knowledge Hub (Stage 2 retrieval).

Model: cross-encoder/ms-marco-MiniLM-L-12-v2 (~130 MB, auto-downloaded by
sentence-transformers on first use).

Usage:
  from reranker import rerank, is_reranker_available
"""

import logging
from sentence_transformers import CrossEncoder

logger = logging.getLogger(__name__)

CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L-12-v2"

# ── Singleton ──────────────────────────────────────────────────────────────
_model: CrossEncoder | None = None
_load_error: str | None = None


def get_reranker() -> CrossEncoder:
    """Load or return cached CrossEncoder model."""
    global _model, _load_error
    if _model is None and _load_error is None:
        try:
            _model = CrossEncoder(CROSS_ENCODER_MODEL)
        except Exception as e:
            _load_error = str(e)
            raise
    if _load_error:
        raise RuntimeError(f"Cross-encoder unavailable: {_load_error}")
    return _model


def is_reranker_available() -> bool:
    """Check if cross-encoder loaded successfully. Does NOT trigger download."""
    global _load_error
    if _model is not None:
        return True
    if _load_error is not None:
        return False
    try:
        get_reranker()
        return True
    except Exception:
        return False


def rerank(
    query: str,
    candidates: list[dict],
    top_k: int = 10,
) -> list[dict]:
    """Cross-Encoder re-ranks Stage-1 candidates.

    Each candidate dict must have a "text" key (the chunk text).
    Adds "rerank_score" and "stage1_score" fields, updates "score" to
    the cross-encoder score.

    Args:
        query: The search query string.
        candidates: List of candidate dicts with "text" and "score" keys.
        top_k: Number of results to return.

    Returns:
        Re-ranked and truncated list of candidates.
    """
    if not candidates:
        return []

    model = get_reranker()
    pairs = [(query, c["text"]) for c in candidates]
    scores = model.predict(pairs)
    # scores is numpy array or list[float]; higher = more relevant

    for c, score in zip(candidates, scores):
        c["rerank_score"] = float(score)
        c["stage1_score"] = c.get("score")
        c["score"] = float(score)

    candidates.sort(key=lambda c: c["score"], reverse=True)
    return candidates[:top_k]
```

- [ ] **Step 2: Verify syntax**

Run: `python3 -m py_compile scripts/reranker.py`
Expected: No output

- [ ] **Step 3: Commit**

```bash
git add scripts/reranker.py
git commit -m "feat: add reranker.py with CrossEncoder singleton and rerank function"
```

---

### Task 5: Create domains/godot/parser.py — Godot RST structured parser

**Files:**
- Create: `domains/godot/parser.py`

- [ ] **Step 1: Write parser.py**

```python
#!/usr/bin/env python3
"""
Godot RST documentation parser.

Parses Godot's RST class documentation into structured Chunk objects.
Handles: .. class:: ClassName, methods, properties, signals, enums, and
inheritance chains. Non-class content (tutorials, getting-started) falls
through to fallback_chunk() via the caller (embed_index.py).

Reference: https://github.com/godotengine/godot-docs (classes/*.rst)
"""

import re
import sys
from pathlib import Path

# Add scripts/ to path so we can import parser_base
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))

from parser_base import Chunk, DomainParser


class Parser(DomainParser):
    """Parser for Godot RST class documentation files."""

    source_type_name = "rst-godot"

    # ── Regex patterns ─────────────────────────────────────────────────
    CLASS_PATTERN = re.compile(r"^\.\.\s+class::\s+(\w+)")
    INHERITS_PATTERN = re.compile(r"inherits.*?:?\s*(.+)$", re.IGNORECASE)
    METHOD_PATTERN = re.compile(
        r"^\s*(?:static\s+)?(\w+(?:\.\w+)*)\s*\([^)]*\)",
    )
    PROPERTY_PATTERN = re.compile(
        r"^\s*var\s+(\w+)\s*(?::\s*\w+)?",
    )
    SIGNAL_PATTERN = re.compile(r"^\s*signal\s+(\w+)\s*\(([^)]*)\)")
    ENUM_PATTERN = re.compile(r"^\s*enum\s+(\w+)")

    def __init__(self):
        self.domain = "godot"

    def parse(self, file_path: str, content: str) -> list[Chunk]:
        """Parse Godot RST content into structured chunks."""
        chunks = []
        lines = content.splitlines()
        current_class = None
        current_inherits = None
        i = 0

        while i < len(lines):
            line = lines[i]

            # Detect class definition:    .. class:: ClassName
            class_match = self.CLASS_PATTERN.match(line)
            if class_match:
                current_class = class_match.group(1)
                current_inherits = self._parse_inherits(line)
                # Generate class overview chunk from the next few lines
                overview_lines = self._collect_section(lines, i + 1, max_lines=20)
                overview_text = "\n".join(overview_lines)
                chunks.append(self._make_class_chunk(
                    current_class, current_inherits, overview_text, file_path, i
                ))
                i += len(overview_lines) + 1
                continue

            # Detect member within a class
            if current_class:
                chunk = self._try_parse_member(
                    lines, i, current_class, current_inherits, file_path
                )
                if chunk:
                    chunks.append(chunk)
                    i += 1
                    continue

            i += 1

        return chunks

    def _parse_inherits(self, line: str) -> list[str] | None:
        """Extract inheritance from class definition line."""
        m = self.INHERITS_PATTERN.search(line)
        if m:
            raw = m.group(1).strip()
            # Split on comma or whitespace
            return [c.strip() for c in re.split(r"[,\s]+", raw) if c.strip()]
        return None

    def _collect_section(
        self, lines: list[str], start: int, max_lines: int = 20
    ) -> list[str]:
        """Collect lines until empty line or next directive."""
        result = []
        for i in range(start, min(start + max_lines, len(lines))):
            line = lines[i]
            if not line.strip():
                break
            if line.lstrip().startswith(".. "):
                break
            result.append(line)
        return result

    def _make_class_chunk(
        self,
        class_name: str,
        inherits: list[str] | None,
        overview: str,
        file_path: str,
        line_start: int,
    ) -> Chunk:
        inherits_text = ""
        if inherits:
            chain = " → ".join(inherits)
            inherits_text = f" extends {chain}"
        text = f"Class: {class_name}{inherits_text}\n\n{overview}"
        return Chunk(
            chunk_id=f"godot::{class_name}::class",
            domain="godot",
            text=text,
            source_type="repo",
            chunk_type="class",
            class_name=class_name,
            name=class_name,
            inherits_from=inherits,
            docstring=overview[:500],
            source_file=file_path,
            line_start=line_start + 1,
            line_end=line_start + len(overview.splitlines()) + 1,
        )

    def _try_parse_member(
        self,
        lines: list[str],
        i: int,
        class_name: str,
        inherits: list[str] | None,
        file_path: str,
    ) -> Chunk | None:
        """Try to parse a method, property, signal, or enum on this line."""
        line = lines[i].strip()
        if not line:
            return None

        # Method: type name(...)
        method_match = self.METHOD_PATTERN.match(line)
        if method_match:
            name = method_match.group(1)
            signature = line
            doc = self._collect_section(lines, i + 1, max_lines=10)
            text = self._build_member_text(
                "Method", class_name, name, signature, inherits, doc
            )
            return Chunk(
                chunk_id=f"godot::{class_name}::method::{name}",
                domain="godot",
                text=text,
                source_type="repo",
                chunk_type="method",
                class_name=class_name,
                name=name,
                signature=signature,
                inherits_from=inherits,
                docstring="\n".join(doc)[:500] if doc else signature,
                source_file=file_path,
                line_start=i + 1,
                line_end=i + 1 + len(doc),
            )

        # Signal: signal name(...)
        signal_match = self.SIGNAL_PATTERN.match(line)
        if signal_match:
            name = signal_match.group(1)
            params = signal_match.group(2)
            signature = f"signal {name}({params})"
            doc = self._collect_section(lines, i + 1, max_lines=10)
            text = self._build_member_text(
                "Signal", class_name, name, signature, inherits, doc
            )
            return Chunk(
                chunk_id=f"godot::{class_name}::signal::{name}",
                domain="godot",
                text=text,
                source_type="repo",
                chunk_type="signal",
                class_name=class_name,
                name=name,
                signature=signature,
                inherits_from=inherits,
                docstring="\n".join(doc)[:500] if doc else signature,
                source_file=file_path,
                line_start=i + 1,
                line_end=i + 1 + len(doc),
            )

        # Enum: enum Name
        enum_match = self.ENUM_PATTERN.match(line)
        if enum_match:
            name = enum_match.group(1)
            doc = self._collect_section(lines, i + 1, max_lines=10)
            text = f"Enum: {class_name}.{name}\n" + "\n".join(doc)
            return Chunk(
                chunk_id=f"godot::{class_name}::enum::{name}",
                domain="godot",
                text=text,
                source_type="repo",
                chunk_type="enum",
                class_name=class_name,
                name=name,
                inherits_from=inherits,
                docstring="\n".join(doc)[:500] if doc else "",
                source_file=file_path,
                line_start=i + 1,
                line_end=i + 1 + len(doc),
            )

        return None

    def _build_member_text(
        self,
        kind: str,
        class_name: str,
        name: str,
        signature: str,
        inherits: list[str] | None,
        doc: list[str],
    ) -> str:
        """Build rich text for a class member chunk."""
        parts = [f"{kind}: {class_name}.{name}"]
        parts.append(f"Signature: {signature}")
        if inherits:
            parts.append(f"Inherits: {' → '.join(inherits)}")
        if doc:
            parts.append("")
            parts.extend(doc)
        return "\n".join(parts)
```

- [ ] **Step 2: Verify syntax**

Run: `python3 -m py_compile domains/godot/parser.py`
Expected: No output

- [ ] **Step 3: Quick import test**

Run: `python3 -c "import sys; sys.path.insert(0,'scripts'); from parser_base import DomainParser; print('imports OK')"`
Expected: `imports OK`

- [ ] **Step 4: Commit**

```bash
git add domains/godot/parser.py
git commit -m "feat: add Godot RST parser with class/method/property/signal/enum extraction"
```

---

### Task 6: Update embed_index.py — Plugin system + Chunk objects + BM25 index

**Files:**
- Modify: `scripts/embed_index.py`

- [ ] **Step 1: Read the current file and note line ranges for changes**

The current file is 230 lines. Changes:
- Lines 1-19: Update docstring
- Lines 21-27: Add imports for parser_base, bm25_search
- Lines 29-42: Remove old CHUNK_SIZE/CHUNK_CHARS constants (moved to parser_base)
- Lines 44-66: Replace chunk_text() with import from parser_base
- Lines 69-113: Rewrite load_domain_sources() to use Chunk objects + parser discovery
- Lines 117-176: Update build_index() to build BM25 index after ChromaDB
- Lines 179-230: Update main() to handle new flow

- [ ] **Step 2: Write the updated embed_index.py**

```python
#!/usr/bin/env python3
"""
Build ChromaDB + BM25 index from all domain sources.

Usage:
  python scripts/embed_index.py --domain godot
  python scripts/embed_index.py --all

Workflow:
  1. Scan domains/<domain>/sources/*.md + personal/*.md
  2. If domain has parser.py: use structured parsing
     Else: fallback to sliding-window chunking (500 tokens, 100 overlap)
  3. Embedding: all-mpnet-base-v2 (768-dim) via sentence-transformers
  4. Store in ChromaDB collection "<domain>_knowledge" + build BM25 index
  5. Delete old collection + BM25 index, create new (complete rebuild)

Requirements:
  pip install chromadb sentence-transformers rank-bm25
  # First run downloads ~420 MB embedding model + ~130 MB cross-encoder (one-time)
"""

import argparse
import importlib.util
import os
import sys
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from parser_base import Chunk, DomainParser, fallback_chunk
from bm25_search import build_bm25_index as build_bm25

# ── Config ──────────────────────────────────────────────────────────────────
HUB_ROOT = Path(__file__).resolve().parent.parent
DOMAINS_DIR = HUB_ROOT / "domains"
CHROMA_DIR = HUB_ROOT / "chromadb_data"
MODEL_NAME = "all-mpnet-base-v2"


def get_parser(domain: str) -> DomainParser | None:
    """Discover and load a domain-specific parser, if one exists.

    Looks for domains/<domain>/parser.py. The file must contain a class
    named 'Parser' that subclasses DomainParser.
    """
    parser_path = DOMAINS_DIR / domain / "parser.py"
    if not parser_path.exists():
        return None

    try:
        module_name = f"{domain}_parser"
        spec = importlib.util.spec_from_file_location(module_name, parser_path)
        if spec is None or spec.loader is None:
            return None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        parser = module.Parser()
        if not isinstance(parser, DomainParser):
            print(f"[WARN]  Parser for '{domain}' is not a DomainParser — ignoring")
            return None
        return parser
    except Exception as e:
        print(f"[WARN]  Failed to load parser for '{domain}': {e}")
        return None


def load_domain_sources(domain: str) -> list[Chunk]:
    """Load all source files for a domain. Returns list[Chunk].

    - If a parser.py exists, uses it for structured chunks.
    - Otherwise falls back to sliding-window chunking.
    - Personal notes always use fallback chunking.
    """
    domain_dir = DOMAINS_DIR / domain
    parser = get_parser(domain)
    chunks: list[Chunk] = []

    # Load repo sources
    sources_dir = domain_dir / "sources"
    if sources_dir.is_dir():
        for file in sorted(sources_dir.glob("*.md")):
            content = file.read_text(encoding="utf-8")

            if parser:
                # Use domain-specific structured parser
                try:
                    parsed = parser.parse(str(file), content)
                    for c in parsed:
                        c.source_file = file.name
                        if not c.chunk_id.startswith(f"{domain}::"):
                            c.chunk_id = f"{domain}::{c.chunk_id}"
                    chunks.extend(parsed)
                    print(f"[INFO]  Parser '{parser.source_type_name}': "
                          f"{len(parsed)} structured chunks from {file.name}")
                    continue
                except Exception as e:
                    print(f"[WARN]  Parser failed for {file.name}: {e} — falling back")

            # Fallback chunking
            fallback = fallback_chunk(
                content, domain=domain, source_type="repo", source_file=file.name
            )
            # Update chunk_ids to be unique across files
            for i, c in enumerate(fallback):
                c.chunk_id = f"{domain}::fallback::repo::{file.stem}::{i}"
                c.chunk_id_in_file = i
            chunks.extend(fallback)

    # Load personal knowledge (always fallback chunking)
    personal_dir = domain_dir / "personal"
    if personal_dir.is_dir():
        for file in sorted(personal_dir.glob("*.md")):
            content = file.read_text(encoding="utf-8")
            category = file.stem
            fallback = fallback_chunk(
                content, domain=domain, source_type="personal", source_file=file.name
            )
            for i, c in enumerate(fallback):
                c.chunk_id = f"{domain}::personal::{category}::{i}"
                c.chunk_id_in_file = i
                c.name = category  # tag with category for BM25 boosting
            chunks.extend(fallback)

    return chunks


def build_index(domain: str, model: SentenceTransformer) -> None:
    """Build ChromaDB + BM25 index for a single domain."""
    collection_name = f"{domain}_knowledge"

    print(f"[INFO]  Loading domain: {domain}")
    chunks = load_domain_sources(domain)

    if not chunks:
        print(f"[WARN]  No chunks found for domain '{domain}'")
        return

    source_types = set(c.source_type for c in chunks)
    print(f"[INFO]  Parsed into {len(chunks)} chunks "
          f"(repo: {sum(1 for c in chunks if c.source_type == 'repo')}, "
          f"personal: {sum(1 for c in chunks if c.source_type == 'personal')})")

    # Embed
    print(f"[INFO]  Embedding with {MODEL_NAME} (768 dims)...")
    texts = [c.text for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=True)

    # Connect to ChromaDB
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    # Delete existing collection, create new
    try:
        client.delete_collection(collection_name)
        print(f"[INFO]  Deleted existing collection '{collection_name}'")
    except Exception:
        pass

    collection = client.create_collection(
        name=collection_name,
        metadata={
            "domain": domain,
            "model": MODEL_NAME,
            "dimensions": 768,
            "hnsw:space": "cosine",
        },
    )

    # Insert in batches
    batch_size = 500
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        batch_embeddings = embeddings[i : i + batch_size]

        collection.add(
            ids=[c.chunk_id for c in batch],
            embeddings=batch_embeddings.tolist(),
            documents=[c.text for c in batch],
            metadatas=[c.to_chromadb_metadata() for c in batch],
        )
        print(f"[INFO]  Inserted batch {i // batch_size + 1}: {len(batch)} chunks")

    # Build BM25 index
    print(f"[INFO]  Building BM25 index...")
    build_bm25(domain, chunks)
    from bm25_search import get_bm25_index_size_mb
    bm25_mb = get_bm25_index_size_mb(domain)
    print(f"[INFO]  BM25 index built: {bm25_mb} MB")

    # Summary
    chroma_size = sum(
        os.path.getsize(os.path.join(r, f))
        for r, _, fs in os.walk(str(CHROMA_DIR))
        for f in fs
        if os.path.exists(os.path.join(r, f))
    )
    print(f"[INFO]  ✓ Collection '{collection_name}' built: "
          f"{len(chunks)} chunks, ChromaDB ~{chroma_size / 1024 / 1024:.0f} MB, "
          f"BM25 {bm25_mb} MB")


def main():
    parser = argparse.ArgumentParser(
        description="Build ChromaDB + BM25 index from domain sources"
    )
    parser.add_argument(
        "--domain", type=str, help="Single domain to index (e.g., 'godot')"
    )
    parser.add_argument(
        "--all", action="store_true", help="Index all available domains"
    )

    args = parser.parse_args()

    if not args.domain and not args.all:
        parser.print_help()
        sys.exit(1)

    # Load model (once)
    print(f"[INFO]  Loading embedding model: {MODEL_NAME}")
    print(f"[INFO]  (first run downloads ~420 MB — please wait)")
    model = SentenceTransformer(MODEL_NAME)

    # Import bm25 module to ensure it's available
    from bm25_search import build_bm25_index  # noqa: F811 — validate import

    # Determine domains
    if args.all:
        domains = [
            d.name
            for d in DOMAINS_DIR.iterdir()
            if d.is_dir() and (d / "domain.md").exists()
        ]
        if not domains:
            print("[ERROR] No domains found with domain.md")
            sys.exit(1)
        print(f"[INFO]  Found {len(domains)} domain(s): {', '.join(domains)}")
    else:
        domains = [args.domain]

    # Build index per domain
    for domain in domains:
        print(f"\n{'=' * 60}")
        print(f"  Building index for: {domain}")
        parser_info = get_parser(domain)
        if parser_info:
            print(f"  Parser: {parser_info.source_type_name}")
        else:
            print(f"  Parser: none (fallback chunking)")
        print(f"{'=' * 60}")
        build_index(domain, model)

    print(f"\n[INFO]  Done. Index stored at: {CHROMA_DIR}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Verify syntax**

Run: `python3 -m py_compile scripts/embed_index.py`
Expected: No output (may warn about unused import `build_bm25_index` in main — acceptable)

- [ ] **Step 4: Commit**

```bash
git add scripts/embed_index.py
git commit -m "feat: integrate plugin system, Chunk objects, and BM25 index into embed_index.py"
```

---

### Task 7: Update embed_search.py — return new Chunk fields from ChromaDB

**Files:**
- Modify: `scripts/embed_search.py`

- [ ] **Step 1: Update semantic_search() to return new metadata fields**

The `semantic_search()` function (lines 25-70) needs to include the new structured fields from ChromaDB metadata. Replace lines 54-70 (the result formatting loop) with:

```python
    # Format results with full Chunk metadata
    formatted = []
    for i in range(len(results["ids"][0])):
        meta = results["metadatas"][0][i]
        distance = results["distances"][0][i]
        # Normalize distance to similarity score
        if distance > 2.0:
            score = round(1.0 / (1.0 + distance), 4)   # L2 fallback
        else:
            score = round(1.0 - distance, 4)            # Cosine

        entry = {
            "rank": i + 1,
            "score": score,
            "chunk_id": results["ids"][0][i],
            "text": results["documents"][0][i][:500],
            "match_type": "semantic",
            "source_type": meta.get("source_type", "unknown"),
            "domain": meta.get("domain", domain),
            "source_file": meta.get("source_file", ""),
            "line_start": meta.get("line_start", 0),
            "line_end": meta.get("line_end", 0),
            # Structured fields (None if not present)
            "chunk_type": meta.get("chunk_type"),
            "class_name": meta.get("class_name"),
            "name": meta.get("name"),
            "signature": meta.get("signature"),
        }
        # Add inherits_from only if present (stored as "::"-joined string)
        if meta.get("inherits_from"):
            entry["inherits_from"] = meta["inherits_from"].split("::")
        else:
            entry["inherits_from"] = None

        formatted.append(entry)

    return formatted
```

- [ ] **Step 2: Verify syntax**

Run: `python3 -m py_compile scripts/embed_search.py`
Expected: No output

- [ ] **Step 3: Commit**

```bash
git add scripts/embed_search.py
git commit -m "feat: return structured Chunk fields (chunk_type, class_name, name, signature) from semantic search"
```

---

### Task 8: Overhaul hybrid_search.py — BM25 replaces ripgrep, add cross-encoder

**Files:**
- Modify: `scripts/hybrid_search.py`

- [ ] **Step 1: Rewrite the entire file**

The current file mixes ripgrep + ChromaDB + RRF. Replace entirely with the BM25 + Dense + Cross-Encoder flow.

```python
#!/usr/bin/env python3
"""
Hybrid search: BM25 (sparse) + ChromaDB (dense) → RRF fusion → Cross-Encoder rerank.

Usage:
  python scripts/hybrid_search.py --domain godot --query "rotate Node3D Y axis" --top 10
  python scripts/hybrid_search.py --domain godot --query "gravity" --json

Algorithm (two-stage retrieval):
  Stage 1: BM25 (sparse) + ChromaDB (dense) — parallel, up to 100 candidates each
           RRF-Fusion (Reciprocal Rank Fusion, k=60) → ~20-50 unified candidates
  Stage 2: Cross-Encoder (ms-marco-MiniLM-L-12-v2) reranks candidates → Top-k

Modes:
  exact    → BM25 only
  semantic → ChromaDB only
  hybrid   → BM25 + ChromaDB + Cross-Encoder (default)
"""

import argparse
import json
import logging
import sys
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from embed_search import semantic_search
from bm25_search import bm25_search
from reranker import rerank, is_reranker_available

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

HUB_ROOT = Path(__file__).resolve().parent.parent
DOMAINS_DIR = HUB_ROOT / "domains"
CHROMA_DIR = HUB_ROOT / "chromadb_data"
MODEL_NAME = "all-mpnet-base-v2"


def rrf_fusion(
    sparse_results: list[dict],
    dense_results: list[dict],
    k: int = 60,
    top_n: int = 50,
) -> list[dict]:
    """Reciprocal Rank Fusion for BM25 and Dense results.

    Both input lists must have "chunk_id" and "score" keys.
    Dense results must also have "text" (for downstream reranking).
    Returns unified list with "text", "score" (RRF), "stage1_sources" fields.
    """
    scores: dict[str, float] = {}
    meta: dict[str, dict] = {}

    # Sparse (BM25) results
    for i, r in enumerate(sparse_results):
        cid = r["chunk_id"]
        rank = i + 1
        scores[cid] = scores.get(cid, 0) + 1.0 / (k + rank)
        if cid not in meta:
            meta[cid] = {
                "chunk_id": cid,
                "stage1_sources": ["bm25"],
                "bm25_score": r.get("score", 0),
                "text": "",  # will be filled from dense results or ChromaDB
            }

    # Dense (semantic) results
    for i, r in enumerate(dense_results):
        cid = r["chunk_id"]
        rank = i + 1
        scores[cid] = scores.get(cid, 0) + 1.0 / (k + rank)
        if cid not in meta:
            meta[cid] = {
                "chunk_id": cid,
                "stage1_sources": ["semantic"],
                "dense_score": r.get("score", 0),
                "text": r.get("text", ""),
                "source_type": r.get("source_type", "unknown"),
                "domain": r.get("domain", ""),
                "source_file": r.get("source_file", ""),
                "line_start": r.get("line_start", 0),
                "line_end": r.get("line_end", 0),
                "chunk_type": r.get("chunk_type"),
                "class_name": r.get("class_name"),
                "name": r.get("name"),
                "signature": r.get("signature"),
                "inherits_from": r.get("inherits_from"),
            }
        else:
            meta[cid]["stage1_sources"].append("semantic")
            if r.get("dense_score"):
                meta[cid]["dense_score"] = r.get("dense_score", 0)
            if r.get("text") and not meta[cid].get("text"):
                meta[cid]["text"] = r["text"]

    # Sort by RRF score
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]

    results = []
    for idx, (cid, rrf_score) in enumerate(ranked):
        entry = dict(meta[cid])
        entry["rank"] = idx + 1
        entry["score"] = round(rrf_score, 4)
        entry["match_type"] = "hybrid"
        results.append(entry)

    return results


def _resolve_texts_via_chromadb(domain: str, results: list[dict]) -> None:
    """Fill missing 'text' fields by querying ChromaDB in one batch.

    Some entries may have come from BM25 only (no text). We batch-lookup
    their texts from ChromaDB so the cross-encoder has text to work with.
    """
    missing_ids = [r["chunk_id"] for r in results if not r.get("text")]
    if not missing_ids:
        return

    try:
        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        collection = client.get_collection(f"{domain}_knowledge")
        batch_result = collection.get(
            ids=missing_ids, include=["documents", "metadatas"]
        )
        id_to_text = {}
        id_to_meta = {}
        for cid, doc, meta in zip(
            batch_result["ids"], batch_result["documents"], batch_result["metadatas"]
        ):
            id_to_text[cid] = doc
            id_to_meta[cid] = meta

        for r in results:
            if not r.get("text") and r["chunk_id"] in id_to_text:
                r["text"] = id_to_text[r["chunk_id"]][:500]
                meta = id_to_meta.get(r["chunk_id"], {})
                r["source_type"] = r.get("source_type") or meta.get("source_type", "unknown")
                r["source_file"] = r.get("source_file") or meta.get("source_file", "")
                r["line_start"] = r.get("line_start") or meta.get("line_start", 0)
                r["line_end"] = r.get("line_end") or meta.get("line_end", 0)
    except Exception as e:
        logger.warning(f"Failed to resolve texts via ChromaDB: {e}")


def search(
    domain: str,
    query: str,
    mode: str = "hybrid",
    top_k: int = 10,
    source_filter: list[str] | None = None,
) -> dict:
    """Search knowledge in a domain.

    Args:
        domain: Domain name (e.g. 'godot')
        query: Search query string
        mode: 'exact' (BM25), 'semantic' (ChromaDB), or 'hybrid' (both + rerank)
        top_k: Max number of results to return
        source_filter: Optional filter by source_type ['repo', 'personal']

    Returns:
        {"results": [...], "total_found": int, "mode": str, "query_time_ms": int}
    """
    import time
    t0 = time.time()

    if mode == "exact":
        results = bm25_search(domain, query, top_k=top_k)
        # Enrich BM25 results with text from ChromaDB
        _resolve_texts_via_chromadb(domain, results)
        total = len(results)
        if source_filter:
            results = [r for r in results if r.get("source_type") in source_filter]
        return {
            "results": results[:top_k],
            "total_found": total,
            "mode": mode,
            "query_time_ms": int((time.time() - t0) * 1000),
        }

    if mode == "semantic":
        model = SentenceTransformer(MODEL_NAME)
        results = semantic_search(domain, query, top_k, model)
        total = len(results)
        if source_filter:
            results = [r for r in results if r.get("source_type") in source_filter]
        return {
            "results": results[:top_k],
            "total_found": total,
            "mode": mode,
            "query_time_ms": int((time.time() - t0) * 1000),
        }

    # Hybrid: Stage 1 (BM25 + Dense) → RRF → Stage 2 (Cross-Encoder)
    model = SentenceTransformer(MODEL_NAME)
    bm25_results = bm25_search(domain, query, top_k=100)
    dense_results = semantic_search(domain, query, 100, model)

    # Apply source filter early (before fusion)
    if source_filter:
        bm25_results = [r for r in bm25_results if r.get("source_type") in source_filter]
        dense_results = [r for r in dense_results if r.get("source_type") in source_filter]

    # RRF fusion
    fused = rrf_fusion(bm25_results, dense_results, k=60, top_n=50)

    # Resolve texts for BM25-only entries
    _resolve_texts_via_chromadb(domain, fused)

    # Stage 2: Cross-Encoder reranking
    if is_reranker_available() and len(fused) > top_k:
        try:
            fused = rerank(query, fused, top_k=top_k)
        except Exception as e:
            logger.warning(f"Cross-encoder reranking failed: {e}. Using RRF-only.")
            fused = fused[:top_k]
    else:
        fused = fused[:top_k]

    return {
        "results": fused,
        "total_found": len(fused),
        "mode": mode,
        "query_time_ms": int((time.time() - t0) * 1000),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Hybrid search (BM25 + ChromaDB + Cross-Encoder)"
    )
    parser.add_argument("--domain", type=str, required=True, help="Domain to search")
    parser.add_argument("--query", type=str, required=True, help="Search query")
    parser.add_argument("--mode", type=str, default="hybrid",
                        choices=["exact", "semantic", "hybrid"])
    parser.add_argument("--top", type=int, default=10, help="Max results")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    print(f"[INFO]  Hybrid search in '{args.domain}': {args.query} (mode={args.mode})")

    result = search(args.domain, args.query, mode=args.mode, top_k=args.top)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for r in result["results"]:
            src = f"[{r.get('source_type', '?')}]"
            mt = f"[{r.get('match_type', '?')}]"
            ctype = f" {r.get('chunk_type','')}/{r.get('name','')}" if r.get('name') else ""
            print(f"\n  #{r.get('rank','?')} {src} {mt}{ctype} (score: {r.get('score','?')})")
            text = r.get("text", "")[:200]
            print(f"  {text}...")

    print(f"\n[INFO]  Found {result['total_found']} results "
          f"in {result['query_time_ms']}ms")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Verify syntax**

Run: `python3 -m py_compile scripts/hybrid_search.py`
Expected: No output

- [ ] **Step 3: Commit**

```bash
git add scripts/hybrid_search.py
git commit -m "feat: overhaul hybrid_search with BM25 + CrossEncoder two-stage retrieval"
```

---

### Task 9: Clean up tools.py — remove ripgrep + duplicate RRF, delegate to scripts

**Files:**
- Modify: `mcp_servers/knowledge_hub/tools.py`

- [ ] **Step 1: Rewrite search_knowledge() (lines 43-176) to delegate to scripts**

Replace the entire `search_knowledge()` function body and remove the `subprocess` import (no longer needed for ripgrep). Also remove the duplicate RRF logic from `search_knowledge()`.

Replace lines 1-176 of tools.py with:

```python
"""Tool implementations for Knowledge Hub MCP Server."""

import json
import subprocess
from datetime import datetime
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from .config import DOMAINS_DIR, CHROMA_DIR, SCRIPTS_DIR, PERSONAL_DIR, MODEL_NAME

# ── Add scripts/ to path so we can import search modules ────────────────
import sys as _sys
_SCRIPTS = str(Path(__file__).resolve().parent.parent.parent / "scripts")
if _SCRIPTS not in _sys.path:
    _sys.path.insert(0, _SCRIPTS)

from hybrid_search import search as hybrid_search_fn
from bm25_search import bm25_search, get_bm25_index_size_mb

# ── Lazy-loaded model ────────────────────────────────────────────────────
_model: SentenceTransformer | None = None


def get_model() -> SentenceTransformer:
    """Load or return cached embedding model."""
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


# ── Domain helpers ────────────────────────────────────────────────────────


def list_domains() -> list[str]:
    """List all available domains (folders with domain.md)."""
    if not DOMAINS_DIR.is_dir():
        return []
    return sorted(
        d.name
        for d in DOMAINS_DIR.iterdir()
        if d.is_dir() and (d / "domain.md").exists()
    )


# ── Search ────────────────────────────────────────────────────────────────


def search_knowledge(
    domain: str,
    query: str,
    mode: str = "hybrid",
    max_results: int = 10,
    source_filter: list[str] | None = None,
) -> dict:
    """Search a domain's knowledge (exact=BM25, semantic=ChromaDB, or hybrid).

    Delegates all search logic to scripts/ (hybrid_search.py, bm25_search.py).
    No duplicate search/ranking logic lives in tools.py.
    """
    return hybrid_search_fn(
        domain=domain,
        query=query,
        mode=mode,
        top_k=max_results,
        source_filter=source_filter,
    )
```

**Keep the rest of the file unchanged** (lines 179-306: get_domain_status, add_personal_note, list_personal_notes, update_domain).

But update `get_domain_status()` to include `has_parser` and `bm25_index_size_mb`:

Replace lines 182-219 (the `get_domain_status` function body) with:

```python
def get_domain_status(domain: str | None = None) -> dict:
    """Get status for one or all domains."""
    domains = [domain] if domain else list_domains()
    result = {}

    for d in domains:
        domain_dir = DOMAINS_DIR / d
        sources = list(domain_dir.glob("sources/*.md")) if domain_dir.is_dir() else []
        personal = list(domain_dir.glob("personal/*.md")) if domain_dir.is_dir() else []

        # Check if parser exists
        has_parser = (domain_dir / "parser.py").exists()

        # Check if index exists
        index_exists = False
        index_size_mb = 0
        if CHROMA_DIR.is_dir():
            total = sum(
                f.stat().st_size for f in CHROMA_DIR.rglob("*") if f.is_file()
            )
            index_size_mb = round(total / 1024 / 1024)
            try:
                client = chromadb.PersistentClient(path=str(CHROMA_DIR))
                client.get_collection(f"{d}_knowledge")
                index_exists = True
            except Exception:
                pass

        # BM25 index size
        bm25_mb = get_bm25_index_size_mb(d)

        result[d] = {
            "sources": len(sources),
            "source_files": [s.name for s in sources],
            "personal_notes": len(personal),
            "personal_files": [p.name for p in personal],
            "index_exists": index_exists,
            "index_size_mb": index_size_mb,
            "has_parser": has_parser,
            "bm25_index_size_mb": bm25_mb,
        }

    return result
```

- [ ] **Step 2: Verify syntax**

Run: `python3 -m py_compile mcp_servers/knowledge_hub/tools.py`
Expected: No output

- [ ] **Step 3: Commit**

```bash
git add mcp_servers/knowledge_hub/tools.py
git commit -m "refactor: delegate all search to scripts/, remove ripgrep and duplicate RRF from tools.py"
```

---

### Task 10: Update config.py — add model config

**Files:**
- Modify: `mcp_servers/knowledge_hub/config.py`

- [ ] **Step 1: Add new constants**

Append these lines after line 10 (`PERSONAL_DIR = ...`):

```python
# BM25 index path pattern (built by embed_index.py)
BM25_INDEX_PATTERN = "{domain}_bm25.pkl"  # relative to CHROMA_DIR

# Cross-encoder model (Stage 2 reranking)
CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L-12-v2"
```

- [ ] **Step 2: Verify syntax**

Run: `python3 -m py_compile mcp_servers/knowledge_hub/config.py`
Expected: No output

- [ ] **Step 3: Commit**

```bash
git add mcp_servers/knowledge_hub/config.py
git commit -m "feat: add BM25 and cross-encoder model config to config.py"
```

---

### Task 11: Update server.py — update tool descriptions

**Files:**
- Modify: `mcp_servers/knowledge_hub/server.py`

- [ ] **Step 1: Update search_knowledge tool description**

On line 41 (in the `list_tools_handler`), change `"description"` from:

```
"Search knowledge in a domain (exact, semantic, or hybrid). Finds API references, code examples, and personal notes."
```

To:

```
"Search knowledge in a domain (exact=BM25, semantic=ChromaDB, hybrid=both + CrossEncoder rerank). Finds API references, code examples, and personal notes."
```

And on line 57, change `"exact=ripgrep"` to `"exact=BM25"` (the enum description).

- [ ] **Step 2: Update update_domain tool description**

On line 87, change from:

```
"Update a domain's knowledge: refresh repo sources (via repomix) and rebuild ChromaDB index."
```

To:

```
"Update a domain's knowledge: refresh repo sources (via repomix) and rebuild ChromaDB + BM25 index."
```

- [ ] **Step 3: Verify syntax**

Run: `python3 -m py_compile mcp_servers/knowledge_hub/server.py`
Expected: No output

- [ ] **Step 4: Commit**

```bash
git add mcp_servers/knowledge_hub/server.py
git commit -m "docs: update MCP tool descriptions for BM25 + CrossEncoder retrieval"
```

---

### Task 12: Update domains/godot/domain.md — add parser field

**Files:**
- Modify: `domains/godot/domain.md`

- [ ] **Step 1: Add parser field to metadata section**

After line 24 (`- Embedding-Model: all-mpnet-base-v2 (768 dims)`), add:

```markdown
- Parser: rst-godot (structured parsing of RST class docs)
```

- [ ] **Step 2: Verify the file is valid markdown**

Run: `python3 -c "open('domains/godot/domain.md').read(); print('OK')"`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add domains/godot/domain.md
git commit -m "docs: add parser field to godot domain.md metadata"
```

---

### Task 13: Final validation

**Files:** (none — validation only)

- [ ] **Step 1: Shell syntax check**

Run: `find . -name "*.sh" -exec bash -n {} \;`
Expected: No output (no syntax errors)

- [ ] **Step 2: Python syntax check (all new/modified files)**

Run:
```bash
python3 -m py_compile scripts/parser_base.py && \
python3 -m py_compile scripts/bm25_search.py && \
python3 -m py_compile scripts/reranker.py && \
python3 -m py_compile domains/godot/parser.py && \
python3 -m py_compile scripts/embed_index.py && \
python3 -m py_compile scripts/embed_search.py && \
python3 -m py_compile scripts/hybrid_search.py && \
python3 -m py_compile mcp_servers/knowledge_hub/tools.py && \
python3 -m py_compile mcp_servers/knowledge_hub/config.py && \
python3 -m py_compile mcp_servers/knowledge_hub/server.py && \
echo "All OK"
```
Expected: `All OK`

- [ ] **Step 3: Import chain test**

Run:
```bash
python3 -c "
import sys
sys.path.insert(0, 'scripts')
from parser_base import Chunk, DomainParser, fallback_chunk
from bm25_search import tokenize, bm25_search as _bs
from reranker import is_reranker_available
print('Parser base: OK')
print('BM25 search: OK')
print('Reranker: OK')
"
```
Expected:
```
Parser base: OK
BM25 search: OK
Reranker: OK
```

- [ ] **Step 4: Godot parser import test**

Run:
```bash
python3 -c "
import sys
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'domains/godot')
from parser import Parser
p = Parser()
print(f'Parser loaded: {p.source_type_name}')
# Test with minimal RST content
chunks = p.parse('test.rst', '.. class:: Node3D\n\n   void rotate_y(angle: float)\n   Rotates around Y axis.\n')
print(f'Parsed {len(chunks)} chunks')
for c in chunks:
    print(f'  {c.chunk_type}: {c.name}')
"
```
Expected:
```
Parser loaded: rst-godot
Parsed 2 chunks
  class: Node3D
  method: rotate_y
```

- [ ] **Step 5: MCP tool import test**

Run:
```bash
timeout 10 python3 -c "
from mcp_servers.knowledge_hub.tools import list_domains, search_knowledge
print(list_domains())
print('MCP tools import: OK')
"
```
Expected: `['godot']` and `MCP tools import: OK`

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "chore: final validation — all syntax, imports, and parser tests pass"
```

---

## Implementation Order

Tasks MUST be executed in this order (dependencies):

1. **Task 1** — `parser_base.py` (no dependencies)
2. **Task 2** — `requirements.txt` (install rank-bm25)
3. **Task 3** — `bm25_search.py` (depends on parser_base for Chunk type, but only used at runtime)
4. **Task 4** — `reranker.py` (no dependencies)
5. **Task 5** — `domains/godot/parser.py` (depends on parser_base.py)
6. **Task 6** — `embed_index.py` (depends on 1, 3, 5)
7. **Task 7** — `embed_search.py` (standalone update)
8. **Task 8** — `hybrid_search.py` (depends on 3, 4, 7)
9. **Task 9** — `tools.py` (depends on 3, 8)
10. **Task 10** — `config.py` (standalone)
11. **Task 11** — `server.py` (standalone description update)
12. **Task 12** — `domain.md` (standalone)
13. **Task 13** — Validation (depends on all above)

---

## Post-Implementation Steps (not in this plan)

These steps happen AFTER all tasks are complete and validated:

1. **Rebuild Godot index:** `python scripts/embed_index.py --domain godot`
   - This will use the new Godot parser for structured chunks, build ChromaDB + BM25
   - Expected: ~18K structured chunks (vs. ~18K flat chunks before)

2. **Test search quality:** `python scripts/hybrid_search.py --domain godot --query "rotate Node3D Y axis" --json`
   - Verify `rotate_y` or `rotate` appears in top results
   - Verify `chunk_type: "method"`, `class_name: "Node3D"` in results

3. **Test MCP server:** Restart OpenCode MCP server, test `search_knowledge` tool

4. **Update .agents/skills/godot/SKILL.md** if needed (tool descriptions changed)
