# DaVinci Resolve Knowledge Domain — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform the Knowledge Hub into a Per-Domain-isolated, RAM-bewussten MCP-Server mit Domain-Scoping und einer neuen DaVinci-Resolve-Domain, deren Wissen aus Blackmagic-PDFs via PyMuPDF4LLM (AGPL Process Boundary) konvertiert wird.

**Architecture:** Jede Domain bekommt eine eigene ChromaDB-Datenbank (`chromadb_data/<domain>/chroma/`) und einen eigenen BM25-Index. Der MCP-Server akzeptiert ein `--domains` CLI-Flag, das nur die konfigurierten Domains sichtbar macht. Ein zentraler `model_manager.py` lädt Embedding- und Reranker-Modelle lazy und cached sie. PDFs werden einmalig durch ein AGPL-lizenziertes Build-Script (`parse_pdf_to_markdown.py`) in Markdown konvertiert; der Runtime-Code importiert niemals PyMuPDF.

**Tech Stack:** Python 3.10+, ChromaDB (LRU-Cache), sentence-transformers (all-mpnet-base-v2), rank-bm25, mcp, PyMuPDF4LLM (Build-Tool only), Apple Silicon M1 Max (CPU inference).

**Spec:** `docs/superpowers/specs/2026-06-27-davinci-resolve-knowledge-domain-design.md`

---

## File Structure

### Neue Dateien

| Datei | Lizenz | Verantwortung |
|---|---|---|
| `scripts/model_manager.py` | MIT | Zentraler Lazy-Model-Cache (Embedder + Reranker), Per-Domain-ChromaDB-Clients, unload_domain() |
| `scripts/migration.py` | MIT | Legacy-Layout → Per-Domain-Layout Migration mit Backup |
| `scripts/parse_pdf_to_markdown.py` | AGPL-3.0 | PDF → Markdown via PyMuPDF4LLM (Build-Tool, nie importiert vom Runtime) |
| `scripts/validate_search.py` | MIT | Regressionstest-Skript für Such-Ergebnisse |
| `domains/davinci_resolve/domain.md` | MIT | Domain-Konfiguration mit Quellen, Metadaten, Lizenz-Hinweis |
| `domains/davinci_resolve/personal/ui-map.md` | MIT | Persönliche UI-Lernkarte (Stub) |
| `requirements-pdf.txt` | — | PyMuPDF + PyMuPDF4LLM (AGPL-Build-Tool) |
| `THIRD_PARTY_LICENSES.md` | MIT | Liste aller Third-Party-Lizenzen |

### Geänderte Dateien

| Datei | Änderung |
|---|---|
| `scripts/embed_index.py` | Per-Domain-ChromaDB-Pfade, nutzt model_manager |
| `scripts/embed_search.py` | nutzt model_manager.get_embedder + get_chroma_client |
| `scripts/bm25_search.py` | Per-Domain-Pfade, LRU-Cache-Eviction |
| `scripts/hybrid_search.py` | nutzt model_manager, Per-Domain-ChromaDB-Clients |
| `scripts/reranker.py` | nutzt model_manager.get_reranker |
| `mcp_servers/knowledge_hub/server.py` | `--domains` CLI-Flag, Scoping-Validierung |
| `mcp_servers/knowledge_hub/config.py` | Per-Domain-Pfad-Helfer |
| `mcp_servers/knowledge_hub/tools.py` | Domain-Scoping-Check, nutzt model_manager |
| `requirements.txt` | Hinweis: kein pymupdf hier |
| `.gitignore` | `domains/*/sources/raw/` hinzufügen |

---

## Task 1: Domain Config Reader & Migration Foundation

**Files:**
- Create: `scripts/model_manager.py`
- Create: `scripts/migration.py`
- Modify: `mcp_servers/knowledge_hub/config.py`

- [ ] **Step 1: Erweitere config.py mit Per-Domain-Pfad-Helfern**

Ersetze den Inhalt von `mcp_servers/knowledge_hub/config.py` mit:

```python
"""Configuration for Knowledge Hub MCP Server."""

from pathlib import Path

# Repository root (knowledge-hub/)
HUB_ROOT = Path(__file__).resolve().parent.parent.parent
DOMAINS_DIR = HUB_ROOT / "domains"
SCRIPTS_DIR = HUB_ROOT / "scripts"
CHROMA_DIR = HUB_ROOT / "chromadb_data"
PERSONAL_DIR = HUB_ROOT / "personal"

# Cross-encoder model (Stage 2 reranking)
CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L-12-v2"

# Default embedding model (can be overridden per-domain in domain.md)
DEFAULT_MODEL_NAME = "all-mpnet-base-v2"

# LRU cache limit for BM25 (max domains held in RAM simultaneously)
BM25_CACHE_MAX = 3

# Per-domain ChromaDB RAM budget (2 GB per domain)
CHROMA_MEMORY_LIMIT_BYTES = 2 * 1024 * 1024 * 1024


def domain_chroma_path(domain: str) -> Path:
    """ChromaDB directory for a domain's isolated database."""
    return CHROMA_DIR / domain / "chroma"


def domain_bm25_path(domain: str) -> Path:
    """BM25 pickle file path for a domain."""
    return CHROMA_DIR / domain / f"{domain}_bm25.pkl"


def legacy_bm25_path(domain: str) -> Path:
    """Legacy BM25 pickle file path (pre-migration layout)."""
    return CHROMA_DIR / f"{domain}_bm25.pkl"


def legacy_collection_path(domain: str) -> Path:
    """Legacy ChromaDB collection directory (pre-migration layout)."""
    return CHROMA_DIR / f"{domain}_knowledge"
```

- [ ] **Step 2: Schreibe scripts/model_manager.py**

```python
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
import re
from collections import OrderedDict
from pathlib import Path

import chromadb
from chromadb.config import Settings
from sentence_transformers import CrossEncoder, SentenceTransformer

# Import config (add scripts/ to path for standalone use)
import sys as _sys
_pkg_root = Path(__file__).resolve().parent.parent
_mcp_config = _pkg_root / "mcp_servers" / "knowledge_hub"
if str(_pkg_root) not in _sys.path:
    _sys.path.insert(0, str(_pkg_root))
if str(_mcp_config.parent) not in _sys.path:
    _sys.path.insert(0, str(_mcp_config.parent))

from config import (
    CHROMA_DIR,
    domain_chroma_path,
    domain_bm25_path,
    DEFAULT_MODEL_NAME,
    CROSS_ENCODER_MODEL,
    CHROMA_MEMORY_LIMIT_BYTES,
    BM25_CACHE_MAX,
)

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


def get_domain_config(domain: str) -> dict:
    """Read domain.md Metadaten block and return a config dict.

    Returns:
        {
            "embedding_model": "all-mpnet-base-v2",
            "collection": "<domain>_knowledge",
            "chroma_path": Path,
            "bm25_path": Path,
        }
    """
    domain_md = Path(__file__).resolve().parent.parent / "domains" / domain / "domain.md"
    if not domain_md.exists():
        # Fallback to defaults
        return {
            "embedding_model": DEFAULT_MODEL_NAME,
            "collection": f"{domain}_knowledge",
            "chroma_path": domain_chroma_path(domain),
            "bm25_path": domain_bm25_path(domain),
        }

    text = domain_md.read_text(encoding="utf-8")
    meta_block = _DOMAIN_META_RE.search(text)
    model_name = DEFAULT_MODEL_NAME
    if meta_block:
        m = _EMBEDDING_MODEL_RE.search(meta_block.group(1))
        if m:
            model_name = m.group(1).strip()

    return {
        "embedding_model": model_name,
        "collection": f"{domain}_knowledge",
        "chroma_path": domain_chroma_path(domain),
        "bm25_path": domain_bm25_path(domain),
    }


def get_embedder(domain: str) -> SentenceTransformer:
    """Lazy-load embedding model for a domain. Cached per model_name."""
    cfg = get_domain_config(domain)
    model_name = cfg["embedding_model"]
    key = f"embedder:{model_name}"
    if key not in _model_cache:
        _model_cache[key] = SentenceTransformer(model_name)
    return _model_cache[key]


def get_reranker() -> CrossEncoder:
    """Lazy-load cross-encoder. Only loads on first hybrid search."""
    if "reranker" not in _model_cache:
        _model_cache["reranker"] = CrossEncoder(CROSS_ENCODER_MODEL)
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
```

- [ ] **Step 3: Schreibe scripts/migration.py**

```python
#!/usr/bin/env python3
"""
Migrate legacy ChromaDB layout to Per-Domain isolated layout.

Legacy:
    chromadb_data/godot_knowledge/   (collection)
    chromadb_data/godot_bm25.pkl     (BM25 index)

New:
    chromadb_data/godot/chroma/godot_knowledge/
    chromadb_data/godot/godot_bm25.pkl

Idempotent: only runs if legacy layout exists and new layout doesn't.
Creates a backup before migrating.

License: MIT.
"""

import shutil
from pathlib import Path

CHROMA_DIR = Path(__file__).resolve().parent.parent / "chromadb_data"


def migrate_legacy_layout() -> bool:
    """Migrate legacy layout to per-domain layout. Returns True if migrated.

    Scans for legacy patterns: chromadb_data/<domain>_knowledge/ and
    chromadb_data/<domain>_bm25.pkl and moves them into chromadb_data/<domain>/.
    """
    if not CHROMA_DIR.is_dir():
        return False

    migrated = False
    backup_dir = CHROMA_DIR / "_legacy_backup"

    # Find legacy collections: directories named <domain>_knowledge
    for entry in sorted(CHROMA_DIR.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name == "_legacy_backup":
            continue
        # Match <domain>_knowledge pattern (exclude already-migrated <domain>/ dirs)
        if not entry.name.endswith("_knowledge"):
            continue

        domain = entry.name[: -len("_knowledge")]
        new_domain_dir = CHROMA_DIR / domain / "chroma"
        new_collection_dir = new_domain_dir / entry.name

        # Skip if already migrated
        if new_collection_dir.exists():
            continue

        # Create backup
        backup_dir.mkdir(exist_ok=True)
        backup_collection = backup_dir / entry.name
        if not backup_collection.exists():
            shutil.copytree(str(entry), str(backup_collection))
            print(f"[MIGRATION] Backup: {entry.name} → _legacy_backup/")

        # Migrate collection
        new_domain_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(entry), str(new_collection_dir))
        print(f"[MIGRATION] Collection: {entry.name} → {new_collection_dir.relative_to(CHROMA_DIR)}")
        migrated = True

        # Migrate BM25 if exists
        legacy_bm25 = CHROMA_DIR / f"{domain}_bm25.pkl"
        if legacy_bm25.exists():
            backup_bm25 = backup_dir / legacy_bm25.name
            if not backup_bm25.exists():
                shutil.copy2(str(legacy_bm25), str(backup_bm25))
            new_bm25 = CHROMA_DIR / domain / legacy_bm25.name
            shutil.move(str(legacy_bm25), str(new_bm25))
            print(f"[MIGRATION] BM25: {legacy_bm25.name} → {new_bm25.relative_to(CHROMA_DIR)}")

    if migrated:
        print("[MIGRATION] Done. Backup in chromadb_data/_legacy_backup/")
    return migrated


if __name__ == "__main__":
    migrate_legacy_layout()
```

- [ ] **Step 4: Syntax-Validierung**

```bash
python3 -m py_compile mcp_servers/knowledge_hub/config.py
python3 -m py_compile scripts/model_manager.py
python3 -m py_compile scripts/migration.py
```

Expected: keine Ausgabe (alle kompilieren).

- [ ] **Step 5: Commit**

```bash
git add mcp_servers/knowledge_hub/config.py scripts/model_manager.py scripts/migration.py
git commit -m "feat(core): add model_manager, migration, per-domain config helpers"
```

---

## Task 2: Refactor Search Modules to Use model_manager

**Files:**
- Modify: `scripts/bm25_search.py`
- Modify: `scripts/embed_search.py`
- Modify: `scripts/hybrid_search.py`
- Modify: `scripts/reranker.py`
- Modify: `scripts/embed_index.py`

- [ ] **Step 1: Refactore bm25_search.py für Per-Domain-Pfade und LRU-Cache**

Ersetze den Inhalt von `scripts/bm25_search.py` mit:

```python
#!/usr/bin/env python3
"""
BM25 sparse retrieval for Knowledge Hub.

Per-Domain isolated BM25 index at chromadb_data/<domain>/<domain>_bm25.pkl.
LRU-cached in memory (max BM25_CACHE_MAX domains held simultaneously).

Usage:
  from bm25_search import build_bm25_index, bm25_search, tokenize
"""

import pickle
import re
from pathlib import Path

import numpy as np
from rank_bm25 import BM25Okapi

import sys as _sys
_pkg_root = Path(__file__).resolve().parent.parent
if str(_pkg_root) not in _sys.path:
    _sys.path.insert(0, str(_pkg_root))
from mcp_servers.knowledge_hub.config import domain_bm25_path
from model_manager import bm25_cache_get, bm25_cache_set, bm25_cache_invalidate


def tokenize(text: str) -> list[str]:
    """Simple tokenizer: lowercase, split on non-alphanumeric."""
    return re.findall(r"\w+", text.lower())


def build_bm25_index(domain: str, chunks: list) -> bool:
    """Build and persist a BM25 index from a list of Chunk objects."""
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
        return False

    bm25 = BM25Okapi(corpus)
    bm25_path = domain_bm25_path(domain)
    bm25_path.parent.mkdir(parents=True, exist_ok=True)
    with open(bm25_path, "wb") as f:
        pickle.dump({"index": bm25, "chunk_ids": chunk_ids}, f)

    bm25_cache_invalidate(domain)
    return True


def _load_index(domain: str) -> dict:
    """Load BM25 index from pickle, with LRU in-memory caching."""
    cached = bm25_cache_get(domain)
    if cached is not None:
        return cached

    index_path = domain_bm25_path(domain)
    if not index_path.exists():
        raise FileNotFoundError(
            f"BM25 index not found for domain '{domain}' at {index_path}. "
            f"Run embed_index.py --domain {domain} first."
        )

    with open(index_path, "rb") as f:
        data = pickle.load(f)

    bm25_cache_set(domain, data)
    return data


def bm25_search(domain: str, query: str, top_k: int = 100) -> list[dict]:
    """BM25 sparse retrieval with field boosting."""
    data = _load_index(domain)
    bm25: BM25Okapi = data["index"]
    chunk_ids: list[str] = data["chunk_ids"]

    tokens = tokenize(query)
    scores = bm25.get_scores(tokens)

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
    index_path = domain_bm25_path(domain)
    if index_path.exists():
        return round(index_path.stat().st_size / 1024 / 1024, 2)
    return 0.0
```

- [ ] **Step 2: Refactore embed_search.py für model_manager**

Ersetze den Inhalt von `scripts/embed_search.py` mit:

```python
#!/usr/bin/env python3
"""
Semantic query against ChromaDB index (per-domain isolated).

Usage:
  python scripts/embed_search.py --domain godot --query "How to add gravity?" --top 5
"""

import argparse
import json
import sys
from pathlib import Path

import sys as _sys
_pkg_root = Path(__file__).resolve().parent.parent
if str(_pkg_root) not in _sys.path:
    _sys.path.insert(0, str(_pkg_root))
from model_manager import get_embedder, get_chroma_client
from mcp_servers.knowledge_hub.config import DEFAULT_MODEL_NAME


def semantic_search(
    domain: str, query: str, top_k: int = 5, model=None
) -> list[dict]:
    """Semantic search in a domain's knowledge index."""
    collection_name = f"{domain}_knowledge"

    if model is None:
        model = get_embedder(domain)

    client = get_chroma_client(domain)

    try:
        collection = client.get_collection(collection_name)
    except Exception:
        print(f"[ERROR] Collection '{collection_name}' not found. Run embed_index.py first.")
        if __name__ != "__main__":
            raise
        sys.exit(1)

    query_embedding = model.encode([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    formatted = []
    for i in range(len(results["ids"][0])):
        meta = results["metadatas"][0][i]
        distance = results["distances"][0][i]
        if distance > 2.0:
            score = round(1.0 / (1.0 + distance), 4)
        else:
            score = round(1.0 - distance, 4)

        inherits = None
        if meta.get("inherits_from"):
            try:
                inherits = json.loads(meta["inherits_from"])
            except (json.JSONDecodeError, TypeError):
                pass

        entry = {
            "rank": i + 1,
            "score": score,
            "chunk_id": results["ids"][0][i],
            "text": results["documents"][0][i][:5000],
            "match_type": "semantic",
            "source_type": meta.get("source_type", "unknown"),
            "domain": meta.get("domain", domain),
            "source_file": meta.get("source_file", ""),
            "line_start": meta.get("line_start", 0),
            "line_end": meta.get("line_end", 0),
            "chunk_type": meta.get("chunk_type"),
            "class_name": meta.get("class_name"),
            "name": meta.get("name"),
            "signature": meta.get("signature"),
            "inherits_from": inherits,
            "page_start": meta.get("page_start"),
            "page_end": meta.get("page_end"),
            "section_path": meta.get("section_path"),
        }
        formatted.append(entry)

    return formatted


def main():
    parser = argparse.ArgumentParser(description="Semantic search in Knowledge Hub")
    parser.add_argument("--domain", type=str, required=True)
    parser.add_argument("--query", type=str, required=True)
    parser.add_argument("--top", type=int, default=5)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    print(f"[INFO]  Semantic search in '{args.domain}_knowledge': {args.query}")
    results = semantic_search(args.domain, args.query, args.top)

    if args.json:
        print(json.dumps({"results": results, "total_found": len(results)}, indent=2))
    else:
        for r in results:
            source_label = f"[{r['source_type']}:{r['source_file']}]"
            print(f"\n  #{r['rank']} {source_label} (score: {r['score']})")
            print(f"  {r['text'][:200]}...")
    print(f"\n[INFO]  Found {len(results)} results")


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Refactore reranker.py für model_manager**

Ersetze den Inhalt von `scripts/reranker.py` mit:

```python
#!/usr/bin/env python3
"""
Cross-Encoder reranking for Knowledge Hub (Stage 2 retrieval).

Model: cross-encoder/ms-marco-MiniLM-L-12-v2 (~130 MB).
Loaded lazily via model_manager.get_reranker().
"""

import logging
from pathlib import Path

import sys as _sys
_pkg_root = Path(__file__).resolve().parent.parent
if str(_pkg_root) not in _sys.path:
    _sys.path.insert(0, str(_pkg_root))
from model_manager import get_reranker, is_reranker_available

logger = logging.getLogger(__name__)


def rerank(
    query: str,
    candidates: list[dict],
    top_k: int = 10,
) -> list[dict]:
    """Cross-Encoder re-ranks Stage-1 candidates."""
    if not candidates:
        return []

    model = get_reranker()
    pairs = [(query, c["text"]) for c in candidates]
    scores = model.predict(pairs)

    for c, score in zip(candidates, scores):
        c["rerank_score"] = float(score)
        c["stage1_score"] = c.get("score")
        c["score"] = float(score)

    candidates.sort(key=lambda c: c["score"], reverse=True)
    return candidates[:top_k]
```

- [ ] **Step 4: Refactore hybrid_search.py für model_manager und Per-Domain-Clients**

Ersetze den Inhalt von `scripts/hybrid_search.py` mit:

```python
#!/usr/bin/env python3
"""
Hybrid search: BM25 (sparse) + ChromaDB (dense) → RRF fusion → Cross-Encoder rerank.

Per-Domain isolated: each domain has its own ChromaDB client and BM25 index.
Models loaded via model_manager (lazy, cached).

Usage:
  python scripts/hybrid_search.py --domain godot --query "rotate Node3D Y axis" --top 10
"""

import argparse
import gc
import json
import logging
import sys
import time
from pathlib import Path

import chromadb

import sys as _sys
_pkg_root = Path(__file__).resolve().parent.parent
if str(_pkg_root) not in _sys.path:
    _sys.path.insert(0, str(_pkg_root))
from model_manager import get_embedder, get_chroma_client, is_reranker_available
from embed_search import semantic_search
from bm25_search import bm25_search
from reranker import rerank

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def rrf_fusion(
    sparse_results: list[dict],
    dense_results: list[dict],
    k: int = 60,
    top_n: int = 50,
) -> list[dict]:
    """Reciprocal Rank Fusion for BM25 and Dense results."""
    scores: dict[str, float] = {}
    meta: dict[str, dict] = {}

    for i, r in enumerate(sparse_results):
        cid = r["chunk_id"]
        rank = i + 1
        scores[cid] = scores.get(cid, 0) + 1.0 / (k + rank)
        if cid not in meta:
            meta[cid] = {
                "chunk_id": cid,
                "stage1_sources": ["bm25"],
                "bm25_score": r.get("score", 0),
                "text": "",
            }

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
                "page_start": r.get("page_start"),
                "page_end": r.get("page_end"),
                "section_path": r.get("section_path"),
            }
        else:
            meta[cid]["stage1_sources"].append("semantic")
            for key, value in r.items():
                if key in ("chunk_id", "stage1_sources"):
                    continue
                if value is not None and (meta[cid].get(key) is None or key == "text"):
                    if key == "text" and meta[cid].get("text"):
                        continue
                    meta[cid][key] = value

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
    """Fill missing 'text' fields by querying ChromaDB in one batch."""
    missing_ids = [r["chunk_id"] for r in results if not r.get("text")]
    if not missing_ids:
        return

    try:
        client = get_chroma_client(domain)
        collection_name = f"{domain}_knowledge"
        collection = client.get_collection(collection_name)
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
                r["text"] = id_to_text[r["chunk_id"]][:5000]
                meta = id_to_meta.get(r["chunk_id"], {})
                r["source_type"] = r.get("source_type") or meta.get("source_type", "unknown")
                r["source_file"] = r.get("source_file") or meta.get("source_file", "")
                r["line_start"] = r.get("line_start") or meta.get("line_start", 0)
                r["line_end"] = r.get("line_end") or meta.get("line_end", 0)
                r["chunk_type"] = r.get("chunk_type") or meta.get("chunk_type")
                r["class_name"] = r.get("class_name") or meta.get("class_name")
                r["name"] = r.get("name") or meta.get("name")
                r["signature"] = r.get("signature") or meta.get("signature")
                if not r.get("inherits_from") and meta.get("inherits_from"):
                    try:
                        r["inherits_from"] = json.loads(meta["inherits_from"])
                    except (json.JSONDecodeError, TypeError):
                        pass
                r["page_start"] = r.get("page_start") or meta.get("page_start")
                r["page_end"] = r.get("page_end") or meta.get("page_end")
                r["section_path"] = r.get("section_path") or meta.get("section_path")
    except Exception as e:
        logger.warning(f"Failed to resolve texts via ChromaDB: {e}")


def search(
    domain: str,
    query: str,
    mode: str = "hybrid",
    top_k: int = 10,
    source_filter: list[str] | None = None,
) -> dict:
    """Search knowledge in a domain."""
    t0 = time.time()

    if mode == "exact":
        results = bm25_search(domain, query, top_k=top_k)
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
        model = get_embedder(domain)
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

    # Hybrid
    model = get_embedder(domain)
    bm25_results = bm25_search(domain, query, top_k=100)
    dense_results = semantic_search(domain, query, 100, model)

    if source_filter:
        bm25_results = [r for r in bm25_results if r.get("source_type") in source_filter]
        dense_results = [r for r in dense_results if r.get("source_type") in source_filter]

    fused = rrf_fusion(bm25_results, dense_results, k=60, top_n=50)
    _resolve_texts_via_chromadb(domain, fused)

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
    parser = argparse.ArgumentParser(description="Hybrid search (BM25 + ChromaDB + Cross-Encoder)")
    parser.add_argument("--domain", type=str, required=True)
    parser.add_argument("--query", type=str, required=True)
    parser.add_argument("--mode", type=str, default="hybrid", choices=["exact", "semantic", "hybrid"])
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--json", action="store_true")
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
            text = r.get("text", "")[:5000]
            print(f"  {text}...")

    print(f"\n[INFO]  Found {result['total_found']} results in {result['query_time_ms']}ms")


if __name__ == "__main__":
    main()
```

- [ ] **Step 5: Refactore embed_index.py für Per-Domain-ChromaDB-Pfade und model_manager**

Ersetze den Inhalt von `scripts/embed_index.py` mit:

```python
#!/usr/bin/env python3
"""
Build ChromaDB + BM25 index from all domain sources.

Per-Domain isolated: each domain gets its own ChromaDB at
chromadb_data/<domain>/chroma/ and BM25 at chromadb_data/<domain>/<domain>_bm25.pkl.

Usage:
  python scripts/embed_index.py --domain godot
  python scripts/embed_index.py --all
"""

import argparse
import importlib.util
import os
import sys
from pathlib import Path

import sys as _sys
_pkg_root = Path(__file__).resolve().parent.parent
if str(_pkg_root) not in _sys.path:
    _sys.path.insert(0, str(_pkg_root))
from model_manager import get_embedder, get_chroma_client
from mcp_servers.knowledge_hub.config import (
    DOMAINS_DIR,
    domain_chroma_path,
    domain_bm25_path,
)
from parser_base import Chunk, DomainParser, fallback_chunk
from bm25_search import build_bm25_index as build_bm25, get_bm25_index_size_mb
from migration import migrate_legacy_layout


def get_parser(domain: str) -> DomainParser | None:
    """Discover and load a domain-specific parser, if one exists."""
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
    """Load all source files for a domain. Returns list[Chunk]."""
    domain_dir = DOMAINS_DIR / domain
    parser = get_parser(domain)
    chunks: list[Chunk] = []

    sources_dir = domain_dir / "sources"
    if sources_dir.is_dir():
        for file in sorted(sources_dir.glob("*.md")):
            content = file.read_text(encoding="utf-8")

            if parser:
                try:
                    parsed = parser.parse(str(file), content)
                    for c in parsed:
                        c.source_file = file.name
                        if not c.chunk_id.startswith(f"{domain}::"):
                            c.chunk_id = f"{domain}::{c.chunk_id}"
                    chunks.extend(parsed)
                    if parsed:
                        print(f"[INFO]  Parser '{parser.source_type_name}': "
                              f"{len(parsed)} structured chunks from {file.name}")
                        continue
                    else:
                        print(f"[INFO]  Parser '{parser.source_type_name}': "
                              f"0 structured chunks from {file.name} — falling back")
                except Exception as e:
                    print(f"[WARN]  Parser failed for {file.name}: {e} — falling back")

            fallback = fallback_chunk(
                content, domain=domain, source_type="repo", source_file=file.name
            )
            for i, c in enumerate(fallback):
                c.chunk_id = f"{domain}::fallback::repo::{file.stem}::{i}"
                c.chunk_id_in_file = i
            chunks.extend(fallback)

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
                c.name = category
            chunks.extend(fallback)

    return chunks


def build_index(domain: str) -> None:
    """Build ChromaDB + BM25 index for a single domain."""
    collection_name = f"{domain}_knowledge"

    print(f"[INFO]  Loading domain: {domain}")
    chunks = load_domain_sources(domain)

    if not chunks:
        print(f"[WARN]  No chunks found for domain '{domain}'")
        return

    repo_count = sum(1 for c in chunks if c.source_type == "repo")
    personal_count = sum(1 for c in chunks if c.source_type == "personal")
    print(f"[INFO]  Parsed into {len(chunks)} chunks "
          f"(repo: {repo_count}, personal: {personal_count})")

    model = get_embedder(domain)
    print(f"[INFO]  Embedding with {model.__class__.__name__}...")
    texts = [c.text for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=True)

    client = get_chroma_client(domain)

    try:
        client.delete_collection(collection_name)
        print(f"[INFO]  Deleted existing collection '{collection_name}'")
    except Exception:
        pass

    collection = client.create_collection(
        name=collection_name,
        metadata={
            "domain": domain,
            "hnsw:space": "cosine",
        },
    )

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

    print(f"[INFO]  Building BM25 index...")
    build_bm25(domain, chunks)
    bm25_mb = get_bm25_index_size_mb(domain)

    chroma_path = domain_chroma_path(domain)
    chroma_size = sum(
        os.path.getsize(os.path.join(r, f))
        for r, _, fs in os.walk(str(chroma_path))
        for f in fs
        if os.path.exists(os.path.join(r, f))
    )
    print(f"[INFO]  ✓ Collection '{collection_name}' built: "
          f"{len(chunks)} chunks, ChromaDB ~{chroma_size / 1024 / 1024:.0f} MB, "
          f"BM25 {bm25_mb} MB")


def main():
    parser = argparse.ArgumentParser(description="Build ChromaDB + BM25 index")
    parser.add_argument("--domain", type=str, help="Single domain to index")
    parser.add_argument("--all", action="store_true", help="Index all domains")
    args = parser.parse_args()

    if not args.domain and not args.all:
        parser.print_help()
        sys.exit(1)

    # Run migration if needed
    print("[INFO]  Checking for legacy layout migration...")
    migrate_legacy_layout()

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

    for domain in domains:
        print(f"\n{'=' * 60}")
        print(f"  Building index for: {domain}")
        parser_info = get_parser(domain)
        if parser_info:
            print(f"  Parser: {parser_info.source_type_name}")
        else:
            print(f"  Parser: none (fallback chunking)")
        print(f"{'=' * 60}")
        build_index(domain)

    print(f"\n[INFO]  Done.")


if __name__ == "__main__":
    main()
```

- [ ] **Step 6: Syntax-Validierung aller geänderten Dateien**

```bash
python3 -m py_compile scripts/bm25_search.py
python3 -m py_compile scripts/embed_search.py
python3 -m py_compile scripts/reranker.py
python3 -m py_compile scripts/hybrid_search.py
python3 -m py_compile scripts/embed_index.py
```

Expected: keine Ausgabe.

- [ ] **Step 7: Commit**

```bash
git add scripts/bm25_search.py scripts/embed_search.py scripts/reranker.py scripts/hybrid_search.py scripts/embed_index.py
git commit -m "refactor(search): per-domain ChromaDB paths, model_manager integration, LRU cache"
```

---

## Task 3: Domain Scoping im MCP-Server

**Files:**
- Modify: `mcp_servers/knowledge_hub/server.py`
- Modify: `mcp_servers/knowledge_hub/tools.py`

- [ ] **Step 1: Erweitere tools.py mit Domain-Scoping-Validierung**

Ersetze den Inhalt von `mcp_servers/knowledge_hub/tools.py` mit:

```python
"""Tool implementations for Knowledge Hub MCP Server."""

import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from .config import DOMAINS_DIR, CHROMA_DIR, SCRIPTS_DIR, PERSONAL_DIR, DEFAULT_MODEL_NAME

import sys as _sys
_SCRIPTS = str(Path(__file__).resolve().parent.parent.parent / "scripts")
if _SCRIPTS not in _sys.path:
    _sys.path.insert(0, _SCRIPTS)

from hybrid_search import search as hybrid_search_fn
from bm25_search import get_bm25_index_size_mb
from model_manager import get_chroma_client, get_domain_config

# ── Domain scoping ────────────────────────────────────────────────────────
_SCOPED_DOMAINS: set[str] | None = None  # None = all domains visible


def set_domain_scope(domains: list[str] | None) -> None:
    """Set the visible domains for this server instance.

    Pass None or empty list to make all domains visible (backward compat).
    Validates that scoped domains exist; raises ValueError on invalid domain.
    """
    global _SCOPED_DOMAINS
    if not domains:
        _SCOPED_DOMAINS = None
        return

    available = list_domains()
    invalid = [d for d in domains if d not in available]
    if invalid:
        raise ValueError(
            f"Domain(s) not found: {invalid}. Available: {available}"
        )
    _SCOPED_DOMAINS = set(domains)


def _check_domain_scope(domain: str) -> dict | None:
    """Return error dict if domain is out of scope, None if OK."""
    if _SCOPED_DOMAINS is not None and domain not in _SCOPED_DOMAINS:
        available = sorted(_SCOPED_DOMAINS)
        return {
            "error": f"Domain '{domain}' not available in this server scope. "
                     f"Available: {available}"
        }
    return None


# ── Domain helpers ────────────────────────────────────────────────────────

_DOMAIN_NAME_RE = re.compile(r'^[a-z0-9_-]+$')
_CATEGORY_RE = re.compile(r'^[a-z0-9_-]+$')


def list_domains() -> list[str]:
    """List all available domains (folders with domain.md)."""
    if not DOMAINS_DIR.is_dir():
        return []
    return sorted(
        d.name
        for d in DOMAINS_DIR.iterdir()
        if d.is_dir() and (d / "domain.md").exists()
    )


def list_scoped_domains() -> list[str]:
    """List domains visible in current scope (filtered by _SCOPED_DOMAINS)."""
    all_domains = list_domains()
    if _SCOPED_DOMAINS is None:
        return all_domains
    return [d for d in all_domains if d in _SCOPED_DOMAINS]


# ── Search ────────────────────────────────────────────────────────────────


def search_knowledge(
    domain: str,
    query: str,
    mode: str = "hybrid",
    max_results: int = 10,
    source_filter: list[str] | None = None,
) -> dict:
    """Search a domain's knowledge."""
    scope_error = _check_domain_scope(domain)
    if scope_error:
        return scope_error
    return hybrid_search_fn(
        domain=domain,
        query=query,
        mode=mode,
        top_k=max_results,
        source_filter=source_filter,
    )


# ── Status ────────────────────────────────────────────────────────────────


def get_domain_status(domain: str | None = None) -> dict:
    """Get status for one or all (scoped) domains."""
    if domain:
        scope_error = _check_domain_scope(domain)
        if scope_error:
            return scope_error
        domains = [domain]
    else:
        domains = list_scoped_domains()

    result = {}
    for d in domains:
        domain_dir = DOMAINS_DIR / d
        sources = list(domain_dir.glob("sources/*.md")) if domain_dir.is_dir() else []
        personal = list(domain_dir.glob("personal/*.md")) if domain_dir.is_dir() else []
        has_parser = (domain_dir / "parser.py").exists()

        index_exists = False
        index_size_mb = 0
        try:
            client = get_chroma_client(d)
            client.get_collection(f"{d}_knowledge")
            index_exists = True
            cfg = get_domain_config(d)
            chroma_path = cfg["chroma_path"]
            if chroma_path.exists():
                total = sum(f.stat().st_size for f in chroma_path.rglob("*") if f.is_file())
                index_size_mb = round(total / 1024 / 1024)
        except Exception:
            pass

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


# ── Personal Notes ──────────────────────────────────────────────────────────


def add_personal_note(
    domain: str, topic: str, content: str, category: str = "gotchas"
) -> dict:
    """Add a personal note to a domain's knowledge."""
    scope_error = _check_domain_scope(domain)
    if scope_error:
        return scope_error

    domain_dir = DOMAINS_DIR / domain
    if not domain_dir.is_dir():
        return {"error": f"Domain '{domain}' not found"}

    if not _CATEGORY_RE.match(category):
        return {"error": f"Invalid category name: {category} (must match [a-z0-9_-]+)"}

    target = domain_dir / "personal" / f"{category}.md"
    target.parent.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = f"""

## {topic}
- **Datum:** {now}
- **Notiz:** {content}
"""

    with open(target, "a") as f:
        f.write(entry)

    return {"status": "added", "domain": domain, "category": category, "topic": topic, "file": f"domains/{domain}/personal/{category}.md"}


def list_personal_notes(domain: str, category: str | None = None) -> dict:
    """List personal notes for a domain."""
    scope_error = _check_domain_scope(domain)
    if scope_error:
        return scope_error

    domain_dir = DOMAINS_DIR / domain
    if not domain_dir.is_dir():
        return {"error": f"Domain '{domain}' not found"}

    personal_dir = domain_dir / "personal"
    if not personal_dir.is_dir():
        return {"domain": domain, "notes": []}

    notes = {}
    files = list(personal_dir.glob("*.md")) if category is None else [personal_dir / f"{category}.md"]
    for f in files:
        if not f.exists():
            continue
        entries = []
        current = {}
        for line in f.read_text().split("\n"):
            if line.startswith("## "):
                if current:
                    entries.append(current)
                current = {"topic": line[3:].strip()}
            elif line.startswith("- **"):
                key = line.split("**")[1] if "**" in line else ""
                val = line.split(":** ")[-1] if ":** " in line else line
                current[key] = val.strip()
        if current:
            entries.append(current)
        notes[f.stem] = entries

    return {"domain": domain, "notes": notes}


# ── Update ────────────────────────────────────────────────────────────────


def update_domain(domain: str, rebuild_index: bool = True) -> dict:
    """Update a domain's knowledge sources and optionally rebuild index."""
    scope_error = _check_domain_scope(domain)
    if scope_error:
        return scope_error

    update_script = DOMAINS_DIR / domain / "scripts" / "update.sh"
    if not update_script.exists():
        return {"error": f"No update.sh found for domain '{domain}'"}

    cmd = ["bash", str(update_script)]
    if not rebuild_index:
        cmd.append("--no-index")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        return {
            "status": "updated",
            "domain": domain,
            "rebuild_index": rebuild_index,
            "output": result.stdout[-500:] if result.stdout else "",
            "error": result.stderr[-200:] if result.stderr else "",
        }
    except subprocess.TimeoutExpired:
        return {"error": "Update timed out (>10 min)"}
```

- [ ] **Step 2: Erweitere server.py mit --domains CLI-Flag und Scoping**

Ersetze den Inhalt von `mcp_servers/knowledge_hub/server.py` mit:

```python
#!/usr/bin/env python3
"""Knowledge Hub MCP Server — stdio transport.

Usage:
  python -m mcp_servers.knowledge_hub.server
  python -m mcp_servers.knowledge_hub.server --domains godot
  python -m mcp_servers.knowledge_hub.server --domains davinci_resolve
  KNOWLEDGE_HUB_DOMAINS=godot python -m mcp_servers.knowledge_hub.server

OpenCode config:
  "mcp": {
    "knowledge_hub": {
      "type": "local",
      "command": ["python3", "-m", "mcp_servers.knowledge_hub.server", "--domains", "godot"],
      "enabled": true
    }
  }
"""

import argparse
import json
import os
import sys
from pathlib import Path

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .tools import (
    search_knowledge,
    get_domain_status,
    update_domain,
    add_personal_note,
    list_personal_notes,
    list_domains,
    list_scoped_domains,
    set_domain_scope,
)

# ── CLI argument parsing (before MCP server starts) ───────────────────────


def _parse_domains_arg() -> list[str] | None:
    """Parse --domains CLI flag or KNOWLEDGE_HUB_DOMAINS env var.

    Returns None if neither is set (all domains visible).
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--domains", type=str, default=None,
                        help="Comma-separated list of domains to expose")
    args, _ = parser.parse_known_args()

    if args.domains:
        return [d.strip() for d in args.domains.split(",") if d.strip()]

    env = os.environ.get("KNOWLEDGE_HUB_DOMAINS")
    if env:
        return [d.strip() for d in env.split(",") if d.strip()]

    return None


server = Server("knowledge-hub")


@server.list_tools()
async def list_tools_handler() -> list[Tool]:
    return [
        Tool(
            name="search_knowledge",
            description="Search knowledge in a domain (exact=BM25, semantic=ChromaDB, hybrid=both + CrossEncoder rerank). Finds API references, code examples, and personal notes.",
            inputSchema={
                "type": "object",
                "properties": {
                    "domain": {"type": "string", "description": "Domain to search (e.g., 'godot', 'davinci_resolve')"},
                    "query": {"type": "string", "description": "Search query (natural language)"},
                    "mode": {"type": "string", "enum": ["exact", "semantic", "hybrid"], "description": "Search mode: exact=BM25, semantic=ChromaDB, hybrid=both", "default": "hybrid"},
                    "max_results": {"type": "integer", "description": "Maximum number of results", "default": 10},
                    "source_filter": {"type": "array", "items": {"type": "string", "enum": ["repo", "personal"]}, "description": "Filter by source type (repo and/or personal)"},
                },
                "required": ["domain", "query"],
            },
        ),
        Tool(
            name="get_domain_status",
            description="Get status of one or all knowledge domains (sources, personal notes, index state).",
            inputSchema={
                "type": "object",
                "properties": {
                    "domain": {"type": "string", "description": "Specific domain (omitted = all scoped domains)"},
                },
            },
        ),
        Tool(
            name="update_domain",
            description="Update a domain's knowledge: refresh repo sources (via repomix) and rebuild ChromaDB + BM25 index.",
            inputSchema={
                "type": "object",
                "properties": {
                    "domain": {"type": "string", "description": "Domain to update"},
                    "rebuild_index": {"type": "boolean", "description": "Rebuild ChromaDB index after update", "default": True},
                },
                "required": ["domain"],
            },
        ),
        Tool(
            name="add_personal_note",
            description="Add a personal note (gotcha, tip, FAQ) to a domain's knowledge base.",
            inputSchema={
                "type": "object",
                "properties": {
                    "domain": {"type": "string", "description": "Domain to add to"},
                    "topic": {"type": "string", "description": "Short topic title"},
                    "content": {"type": "string", "description": "Note content (markdown)"},
                    "category": {"type": "string", "enum": ["gotchas", "tips", "best-practices", "faq"], "description": "Category of note", "default": "gotchas"},
                },
                "required": ["domain", "topic", "content"],
            },
        ),
        Tool(
            name="list_personal_notes",
            description="List personal notes for a domain.",
            inputSchema={
                "type": "object",
                "properties": {
                    "domain": {"type": "string", "description": "Domain to list notes for"},
                    "category": {"type": "string", "description": "Filter by category (gotchas, tips, best-practices, faq)"},
                },
                "required": ["domain"],
            },
        ),
        Tool(
            name="list_domains",
            description="List all available knowledge domains (scoped to this server).",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
    ]


@server.call_tool()
async def call_tool_handler(name: str, arguments: dict) -> list[TextContent]:
    try:
        if name == "search_knowledge":
            result = search_knowledge(
                domain=arguments["domain"],
                query=arguments["query"],
                mode=arguments.get("mode", "hybrid"),
                max_results=arguments.get("max_results", 10),
                source_filter=arguments.get("source_filter"),
            )
        elif name == "get_domain_status":
            result = get_domain_status(domain=arguments.get("domain"))
        elif name == "update_domain":
            result = update_domain(
                domain=arguments["domain"],
                rebuild_index=arguments.get("rebuild_index", True),
            )
        elif name == "add_personal_note":
            result = add_personal_note(
                domain=arguments["domain"],
                topic=arguments["topic"],
                content=arguments["content"],
                category=arguments.get("category", "gotchas"),
            )
        elif name == "list_personal_notes":
            result = list_personal_notes(
                domain=arguments["domain"],
                category=arguments.get("category"),
            )
        elif name == "list_domains":
            domains = list_scoped_domains()
            result = {"domains": domains, "count": len(domains)}
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": str(e)}))]


async def main():
    # Parse and apply domain scoping before starting MCP loop
    domains = _parse_domains_arg()
    if domains:
        print(f"[INFO]  Domain scope: {domains}", file=sys.stderr)
        set_domain_scope(domains)
    else:
        print(f"[INFO]  Domain scope: ALL (no --domains flag)", file=sys.stderr)

    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

- [ ] **Step 3: Syntax-Validierung**

```bash
python3 -m py_compile mcp_servers/knowledge_hub/tools.py
python3 -m py_compile mcp_servers/knowledge_hub/server.py
```

Expected: keine Ausgabe.

- [ ] **Step 4: Commit**

```bash
git add mcp_servers/knowledge_hub/tools.py mcp_servers/knowledge_hub/server.py
git commit -m "feat(server): add --domains CLI flag for domain-scoped MCP server"
```

---

## Task 4: PDF Build-Script (AGPL) & Lizenz-Dateien

**Files:**
- Create: `scripts/parse_pdf_to_markdown.py`
- Create: `requirements-pdf.txt`
- Create: `THIRD_PARTY_LICENSES.md`
- Modify: `requirements.txt`
- Modify: `.gitignore`

- [ ] **Step 1: Schreibe scripts/parse_pdf_to_markdown.py (AGPL)**

```python
#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# PDF → Markdown converter for Knowledge Hub.
#
# This script imports PyMuPDF4LLM (AGPL-3.0, Artifex Software).
# It is a STANDALONE BUILD TOOL, NOT part of the MIT-licensed runtime.
# The MIT-licensed Knowledge Hub code NEVER imports pymupdf.
#
# See THIRD_PARTY_LICENSES.md for licensing details.
#
# Usage:
#   pip install -r requirements-pdf.txt
#   python scripts/parse_pdf_to_markdown.py --pdf <input.pdf> --out <output.md>

"""Convert a PDF to section-aware Markdown using PyMuPDF4LLM.

Outputs GitHub-compatible Markdown with:
- # / ## / ### heading hierarchy derived from font sizes
- Tables as GFM pipe tables
- Correct reading order for multi-column pages
- Page number metadata preserved as HTML comments
"""

import argparse
import sys
from pathlib import Path

import pymupdf          # AGPL-3.0
import pymupdf4llm      # AGPL-3.0


def convert_pdf(pdf_path: Path, out_path: Path) -> dict:
    """Convert a PDF to section-aware Markdown.

    Returns a summary dict with stats.
    """
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    # Phase 1a: Markdown extraction via PyMuPDF4LLM
    print(f"[INFO]  Converting: {pdf_path.name}")
    md_text = pymupdf4llm.to_markdown(str(pdf_path))

    if not md_text or not md_text.strip():
        raise RuntimeError(f"PDF produced empty Markdown: {pdf_path}")

    # Phase 1b: Extract TOC for metadata (optional, appended as comment)
    doc = pymupdf.open(str(pdf_path))
    toc = doc.get_toc()  # [[level, title, page], ...]
    doc.close()

    # Build header comment with TOC summary
    toc_lines = []
    if toc:
        toc_lines.append("<!-- TOC")
        for level, title, page in toc:
            indent = "  " * (level - 1)
            toc_lines.append(f"{indent}- {title} (p.{page})")
        toc_lines.append("-->")
        toc_lines.append("")

    full_md = "\n".join(toc_lines) + md_text

    # Write output
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(full_md, encoding="utf-8")

    stats = {
        "pdf": str(pdf_path),
        "output": str(out_path),
        "chars": len(full_md),
        "toc_entries": len(toc),
        "headings": full_md.count("\n# ") + full_md.count("\n## ") + full_md.count("\n### "),
    }
    print(f"[OK]    {pdf_path.name} → {out_path.name} "
          f"({stats['chars']} chars, {stats['toc_entries']} TOC entries, "
          f"{stats['headings']} headings)")
    return stats


def main():
    parser = argparse.ArgumentParser(
        description="PDF → Markdown converter (AGPL build tool, uses PyMuPDF4LLM)"
    )
    parser.add_argument("--pdf", required=True, type=Path, help="Input PDF file")
    parser.add_argument("--out", required=True, type=Path, help="Output Markdown file")
    args = parser.parse_args()

    try:
        convert_pdf(args.pdf, args.out)
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Schreibe requirements-pdf.txt**

```text
# Knowledge Hub — PDF Build Tool Dependencies (AGPL)
#
# This file is ONLY for the PDF → Markdown conversion script
# (scripts/parse_pdf_to_markdown.py). It is NOT imported by the
# MIT-licensed runtime code. See THIRD_PARTY_LICENSES.md.
#
# Installation (only needed for PDF conversion):
#   pip install -r requirements-pdf.txt
#
# License: PyMuPDF and PyMuPDF4LLM are AGPL-3.0 (Artifex Software).
# Using them via subprocess (separate script) keeps the Knowledge Hub
# runtime MIT-licensed via the Process Boundary principle.

PyMuPDF>=1.24.0,<2.0.0
pymupdf4llm>=0.0.17,<1.0.0
```

- [ ] **Step 3: Schreibe THIRD_PARTY_LICENSES.md**

```markdown
# Third-Party Licenses

This file lists all third-party software used by the Knowledge Hub project.

## MIT-Licensed Dependencies (Runtime)

These packages are imported by the MIT-licensed Knowledge Hub runtime code.

| Package | License | Purpose |
|---------|---------|---------|
| chromadb | Apache-2.0 | Vector database for semantic search |
| sentence-transformers | Apache-2.0 | Embedding models for semantic search |
| mcp | MIT | Model Context Protocol server |
| rank-bm25 | Apache-2.0 | BM25 sparse retrieval |

## AGPL-Licensed Dependencies (Build Tool Only)

These packages are imported ONLY by `scripts/parse_pdf_to_markdown.py`,
a standalone build tool that runs via subprocess. The MIT-licensed
Knowledge Hub runtime code NEVER imports these packages.

### PyMuPDF

- **Repository:** https://github.com/pymupdf/PyMuPDF
- **License:** GNU AGPL v3.0 (or commercial license from Artifex)
- **Copyright:** Artifex Software, Inc.
- **Usage:** PDF text extraction with font/position metadata
- **License file:** See https://github.com/pymupdf/PyMuPDF/blob/master/COPYING

### PyMuPDF4LLM

- **Repository:** https://github.com/pymupdf/pymupdf4llm
- **License:** GNU AGPL v3.0 (or commercial license from Artifex)
- **Copyright:** Artifex Software, Inc.
- **Usage:** PDF → Markdown conversion for RAG pipelines
- **License file:** See https://github.com/pymupdf/pymupdf4llm/blob/main/LICENSE

### Process Boundary Explanation

The Knowledge Hub uses the "Process Boundary" principle to keep its
MIT license while using AGPL-licensed PyMuPDF:

1. `scripts/parse_pdf_to_markdown.py` imports PyMuPDF (AGPL) and runs
   as a standalone script via `python scripts/parse_pdf_to_markdown.py`.
2. The MIT-licensed runtime (`embed_index.py`, `hybrid_search.py`,
   `mcp_servers/`) reads only the resulting `.md` files — it never
   imports PyMuPDF.
3. This is analogous to calling GCC (GPL) from a proprietary build
   system: separate processes are separate works.

See: https://www.gnu.org/licenses/gpl-faq.en.html#GPLInProprietarySystem
```

- [ ] **Step 4: Aktualisiere requirements.txt mit Lizenz-Hinweis**

Ersetze den Inhalt von `requirements.txt` mit:

```text
# Knowledge Hub — Python Dependencies (Runtime, MIT)
#
# IMPORTANT: PyMuPDF / PyMuPDF4LLM are NOT included here.
# They are AGPL-3.0 and only used in the build tool.
# See requirements-pdf.txt and THIRD_PARTY_LICENSES.md.
#
# Installation:
#   pip install -r requirements.txt

chromadb>=0.5.0,<1.0.0
sentence-transformers>=3.0.0,<4.0.0
mcp>=1.0.0
rank-bm25>=0.2.2,<1.0.0
```

- [ ] **Step 5: Aktualisiere .gitignore für sources/raw/**

Füge am Ende von `.gitignore` hinzu:

```text

# Original PDFs (too large for Git, converted to .md via build tool)
domains/*/sources/raw/
```

- [ ] **Step 6: Syntax-Validierung des Build-Scripts (ohne pymupdf installiert)**

```bash
python3 -m py_compile scripts/parse_pdf_to_markdown.py
```

Expected: kompiliert (Import-Fehler kommt erst zur Laufzeit, nicht bei `py_compile`).

- [ ] **Step 7: Commit**

```bash
git add scripts/parse_pdf_to_markdown.py requirements-pdf.txt THIRD_PARTY_LICENSES.md requirements.txt .gitignore
git commit -m "feat(pdf): add AGPL build script for PDF→Markdown, license docs, gitignore raw PDFs"
```

---

## Task 5: DaVinci Resolve Domain Setup

**Files:**
- Create: `domains/davinci_resolve/domain.md`
- Create: `domains/davinci_resolve/personal/ui-map.md`

- [ ] **Step 1: Erstelle domains/davinci_resolve/domain.md**

```markdown
# Domain: davinci_resolve

## Zweck
Wissen für Videoschnitt-Produktion mit DaVinci Resolve Studio 21.
Fokus: Wo finde ich Werkzeuge in der UI, wie produziere ich erfolgreich Videos.
Deckt: Cut, Edit, Color, Fairlight, Fusion, Deliver, Photo (ab Resolve 21).

## Quellen (Repo-Wissen)
| Name | Datei | Ursprung | Konvertiert am |
|------|-------|----------|---------------|
| Resolve 20 Reference Manual | sources/davinci-resolve-20-reference-manual.md | Blackmagic PDF | TODO |
| Resolve 21 New Features Guide | sources/davinci-resolve-21-new-features-guide.md | Blackmagic PDF | TODO |
| Resolve 20 Editor's Guide | sources/davinci-resolve-20-editors-guide.md | Blackmagic PDF | TODO |
| Resolve 20 Colorist Guide | sources/davinci-resolve-20-colorist-guide.md | Blackmagic PDF | TODO |
| Resolve 20 Fairlight Audio Guide | sources/davinci-resolve-20-fairlight-audio-guide.md | Blackmagic PDF | TODO |
| Resolve 20 Visual Effects Guide | sources/davinci-resolve-20-fusion-visual-effects.md | Blackmagic PDF | TODO |
| Resolve 20 Beginner's Guide | sources/davinci-resolve-20-beginners-guide.md | Blackmagic PDF | TODO |

## Persönliches Wissen
| Datei | Beschreibung |
|-------|-------------|
| personal/ui-map.md | UI-Lernkarte: Page → Panel → Aktion |
| personal/beginner-questions.md | Anfängerfragen und Antworten |
| personal/gotchas.md | Fallen, Bugs, Workarounds |
| personal/workflow-notes.md | Eigene Reel-Produktions-Workflows |

## Metadaten
- Embedding-Model: all-mpnet-base-v2 (768 dims)
- Collection: davinci_resolve_knowledge
- ChromaDB-Path: chromadb_data/davinci_resolve/chroma/
- BM25-Path: chromadb_data/davinci_resolve/davinci_resolve_bm25.pkl
- Letztes Update: TODO

## Lizenz-Hinweis
Quelldokumente © Blackmagic Design. Ursprüngliche PDFs in sources/raw/ (gitignored).
Konvertierte Markdown-Dateien sind interne Arbeitsprodukte, nicht zur Weitergabe.
PyMuPDF/PyMuPDF4LLM (AGPL-3.0) wird nur im Build-Script verwendet, nicht im Runtime-Code.
Siehe THIRD_PARTY_LICENSES.md und docs/decisions/.
```

- [ ] **Step 2: Erstelle domains/davinci_resolve/personal/ui-map.md (Stub)**

```markdown
# DaVinci Resolve — UI-Lernkarte

Diese Datei sammelt "Wo finde ich was?"-Notizen aus der Praxis.

## Cut Page
<!-- TODO: Notizen zur Cut Page -->

## Edit Page
<!-- TODO: Notizen zur Edit Page -->

## Color Page
<!-- TODO: Notizen zur Color Page -->

## Fairlight Page
<!-- TODO: Notizen zur Fairlight Page -->

## Fusion Page
<!-- TODO: Notizen zur Fusion Page -->

## Deliver Page
<!-- TODO: Notizen zur Deliver Page -->

## Photo Page (ab Resolve 21)
<!-- TODO: Notizen zur Photo Page -->
```

- [ ] **Step 3: Commit**

```bash
git add domains/davinci_resolve/domain.md domains/davinci_resolve/personal/ui-map.md
git commit -m "feat(domain): add davinci_resolve domain config and UI-map stub"
```

---

## Task 6: Regression Test Script

**Files:**
- Create: `scripts/validate_search.py`

- [ ] **Step 1: Schreibe scripts/validate_search.py**

```python
#!/usr/bin/env python3
"""
Regression test for Knowledge Hub search.

Verifies that a domain's search returns results within time and quality bounds.

Usage:
  python scripts/validate_search.py --domain godot --query "Node3D rotate" --expected-min-results 1
  python scripts/validate_search.py --domain davinci_resolve --query "trim clip edit" --expected-min-results 1
"""

import argparse
import json
import sys
from pathlib import Path

import sys as _sys
_pkg_root = Path(__file__).resolve().parent.parent
if str(_pkg_root) not in _sys.path:
    _sys.path.insert(0, str(_pkg_root))
from hybrid_search import search


def validate(
    domain: str,
    query: str,
    expected_min_results: int = 1,
    max_query_time_ms: int = 5000,
) -> bool:
    """Run a search and validate the results. Returns True if all checks pass."""
    print(f"[TEST]  domain={domain} query='{query}'")
    try:
        result = search(domain, query, mode="hybrid", top_k=10)
    except Exception as e:
        print(f"[FAIL]  Search raised exception: {e}")
        return False

    # Check 1: results returned
    total = result.get("total_found", 0)
    if total < expected_min_results:
        print(f"[FAIL]  Expected >= {expected_min_results} results, got {total}")
        return False
    print(f"[OK]    Results: {total} (>= {expected_min_results})")

    # Check 2: query time
    query_ms = result.get("query_time_ms", 999999)
    if query_ms > max_query_time_ms:
        print(f"[FAIL]  Query too slow: {query_ms}ms (max {max_query_time_ms}ms)")
        return False
    print(f"[OK]    Query time: {query_ms}ms (<= {max_query_time_ms}ms)")

    # Check 3: metadata present
    results = result.get("results", [])
    if results:
        r = results[0]
        if not r.get("source_file"):
            print(f"[WARN]  First result missing source_file metadata")
        if not r.get("text"):
            print(f"[WARN]  First result missing text")
        if r.get("page_start") is not None:
            print(f"[OK]    Page metadata: page_start={r.get('page_start')}")
        if r.get("section_path"):
            print(f"[OK]    Section path: {r.get('section_path')}")

    print(f"[PASS]  All checks passed for domain={domain}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Regression test for Knowledge Hub search")
    parser.add_argument("--domain", required=True, type=str)
    parser.add_argument("--query", required=True, type=str)
    parser.add_argument("--expected-min-results", type=int, default=1)
    parser.add_argument("--max-query-time-ms", type=int, default=5000)
    args = parser.parse_args()

    success = validate(
        domain=args.domain,
        query=args.query,
        expected_min_results=args.expected_min_results,
        max_query_time_ms=args.max_query_time_ms,
    )
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Syntax-Validierung**

```bash
python3 -m py_compile scripts/validate_search.py
```

Expected: keine Ausgabe.

- [ ] **Step 3: Commit**

```bash
git add scripts/validate_search.py
git commit -m "test: add search regression validation script"
```

---

## Task 7: Integration Test & Migration Validation

**Files:**
- Test: `chromadb_data/` (Migration von Legacy → Per-Domain)
- Test: `scripts/hybrid_search.py` (Godot-Suche funktioniert nach Migration)

- [ ] **Step 1: Legacy-Migration testen (Dry-Run-Check)**

```bash
# Prüfe ob Legacy-Layout existiert
ls -la chromadb_data/ | head -20
```

Wenn `godot_knowledge/` und `godot_bm25.pkl` im Root von `chromadb_data/` existieren, ist das Legacy-Layout vorhanden.

- [ ] **Step 2: Migration ausführen**

```bash
python3 scripts/migration.py
```

Expected output:
```
[MIGRATION] Backup: godot_knowledge → _legacy_backup/
[MIGRATION] Collection: godot_knowledge → godot/chroma/godot_knowledge
[MIGRATION] BM25: godot_bm25.pkl → godot/godot_bm25.pkl
[MIGRATION] Done. Backup in chromadb_data/_legacy_backup/
```

- [ ] **Step 3: Verifiziere neues Layout**

```bash
ls -la chromadb_data/godot/chroma/
ls -la chromadb_data/godot/godot_bm25.pkl
ls -la chromadb_data/_legacy_backup/
```

Expected: `chromadb_data/godot/chroma/godot_knowledge/` existiert, `godot_bm25.pkl` ist in `chromadb_data/godot/`.

- [ ] **Step 4: Godot-Index neu bauen (falls Migration nur Dateien verschoben hat, ChromaDB muss neu geöffnet werden)**

```bash
python3 scripts/embed_index.py --domain godot
```

Expected: "Building index for: godot" → Collection wird neu gebaut im neuen Per-Domain-Pfad.

- [ ] **Step 5: Godot-Suche testen (Regression)**

```bash
python3 scripts/validate_search.py --domain godot --query "Node3D rotate" --expected-min-results 1
```

Expected: `[PASS] All checks passed for domain=godot`

- [ ] **Step 6: Backup löschen (nur wenn Suche funktioniert)**

```bash
rm -rf chromadb_data/_legacy_backup/
```

- [ ] **Step 7: Commit (falls .gitignore Anpassungen nötig)**

```bash
git status
# Falls keine Code-Änderungen: kein Commit nötig
# Die Migration verändert nur chromadb_data/ (gitignored)
```

---

## Task 8: DaVinci Resolve PDF-Konvertierung und Index-Bau

**Files:**
- Input: `domains/davinci_resolve/sources/raw/*.pdf` (manuell bereitzustellen)
- Output: `domains/davinci_resolve/sources/*.md`
- Output: `chromadb_data/davinci_resolve/`

> **Voraussetzung:** Noah muss die Blackmagic-PDFs manuell herunterladen und in `domains/davinci_resolve/sources/raw/` legen. Die URLs stehen in der domain.md und im Spec.

- [ ] **Step 1: Installiere AGPL-Build-Dependencies**

```bash
pip install -r requirements-pdf.txt
```

Expected: PyMuPDF und PyMuPDF4LLM werden installiert.

- [ ] **Step 2: Lege PDFs in sources/raw/ ab**

```bash
mkdir -p domains/davinci_resolve/sources/raw/
# Manuell: PDFs herunterladen von Blackmagic und hier ablegen
# - DaVinci_Resolve_20_Reference_Manual.pdf
# - DaVinci_Resolve_21_New_Features_Guide.pdf
# - DaVinci-Resolve-20-Editors-Guide.pdf
# - DaVinci-Resolve-20-Colorist-Guide.pdf
# - DaVinci-Resolve-20-Fairlight-Audio-Guide.pdf (Name prüfen)
# - DaVinci-Resolve-20-Fusion-Visual-Effects.pdf
# - DaVinci-Resolve-20-Beginners-Guide.pdf (Name prüfen)
```

- [ ] **Step 3: Konvertiere Reference Manual als erstes**

```bash
python3 scripts/parse_pdf_to_markdown.py \
  --pdf domains/davinci_resolve/sources/raw/DaVinci_Resolve_20_Reference_Manual.pdf \
  --out domains/davinci_resolve/sources/davinci-resolve-20-reference-manual.md
```

Expected: `[OK] DaVinci_Resolve_20_Reference_Manual.pdf → davinci-resolve-20-reference-manual.md (X chars, Y TOC entries, Z headings)`

- [ ] **Step 4: Verifiziere Markdown-Qualität**

```bash
head -50 domains/davinci_resolve/sources/davinci-resolve-20-reference-manual.md
grep -c "^## " domains/davinci_resolve/sources/davinci-resolve-20-reference-manual.md
```

Expected: TOC-Kommentar am Anfang, dann Markdown mit `#`/`##`-Headings, Tabellen als GFM.

- [ ] **Step 5: Konvertiere alle weiteren PDFs**

```bash
python3 scripts/parse_pdf_to_markdown.py \
  --pdf domains/davinci_resolve/sources/raw/DaVinci_Resolve_21_New_Features_Guide.pdf \
  --out domains/davinci_resolve/sources/davinci-resolve-21-new-features-guide.md

python3 scripts/parse_pdf_to_markdown.py \
  --pdf domains/davinci_resolve/sources/raw/DaVinci-Resolve-20-Editors-Guide.pdf \
  --out domains/davinci_resolve/sources/davinci-resolve-20-editors-guide.md

# ... für alle weiteren PDFs wiederholen
```

- [ ] **Step 6: DaVinci-Index bauen**

```bash
python3 scripts/embed_index.py --domain davinci_resolve
```

Expected: Collection `davinci_resolve_knowledge` wird in `chromadb_data/davinci_resolve/chroma/` gebaut.

- [ ] **Step 7: DaVinci-Suche testen**

```bash
python3 scripts/validate_search.py --domain davinci_resolve --query "trim clip edit" --expected-min-results 1
python3 scripts/validate_search.py --domain davinci_resolve --query "color grading primary correction" --expected-min-results 1
python3 scripts/validate_search.py --domain davinci_resolve --query "render deliver settings" --expected-min-results 1
```

Expected: alle drei `[PASS]`.

- [ ] **Step 8: domain.md TODOs aktualisieren**

Ersetze in `domains/davinci_resolve/domain.md` die `TODO`-Einträge mit dem aktuellen Datum `2026-06-27`.

- [ ] **Step 9: Commit**

```bash
git add domains/davinci_resolve/domain.md domains/davinci_resolve/sources/*.md
git commit -m "feat(davinci): convert 7 Blackmagic PDFs to Markdown and build index"
```

---

## Task 9: Video-Blog Workspace Einbindung

**Files:**
- Modify: `/Users/noahk/Documents/work/video-blog/meta/.opencode/opencode.json`
- Modify: `/Users/noahk/Documents/work/nak-hopper-game/.opencode/opencode.json`

> **Achtung:** Diese Dateien liegen in anderen Repos. Erst nach Absprache mit Noah ändern. Der Knowledge-Hub-Commit bleibt unabhängig davon.

- [ ] **Step 1: nak-hopper-game opencode.json aktualisieren**

Füge `--domains godot` zum bestehenden knowledge_hub-Eintrag hinzu:

```json
"knowledge_hub": {
  "command": [
    "/Users/noahk/Documents/work/knowledge-hub/.venv/bin/python3",
    "-m", "mcp_servers.knowledge_hub.server",
    "--domains", "godot"
  ],
  "enabled": true
}
```

Validierung:
```bash
python3 -m json.tool /Users/noahk/Documents/work/nak-hopper-game/.opencode/opencode.json
```

- [ ] **Step 2: video-blog opencode.json um knowledge_hub_davinci erweitern**

Füge einen neuen MCP-Server-Eintrag hinzu:

```json
"knowledge_hub_davinci": {
  "command": [
    "/Users/noahk/Documents/work/knowledge-hub/.venv/bin/python3",
    "-m", "mcp_servers.knowledge_hub.server",
    "--domains", "davinci_resolve"
  ],
  "enabled": true,
  "environment": {
    "PYTHONPATH": "/Users/noahk/Documents/work/knowledge-hub"
  }
}
```

Validierung:
```bash
python3 -m json.tool /Users/noahk/Documents/work/video-blog/meta/.opencode/opencode.json
```

- [ ] **Step 3: Domain-Scoping testen**

Teste im nak-hopper-game Workspace:
```bash
# Start server scoped to godot
KNOWLEDGE_HUB_DOMAINS=godot python3 -c "
import sys; sys.path.insert(0, '/Users/noahk/Documents/work/knowledge-hub')
from mcp_servers.knowledge_hub.tools import set_domain_scope, search_knowledge, list_domains
set_domain_scope(['godot'])
print('Scoped domains:', list_domains())
# Should fail:
r = search_knowledge(domain='davinci_resolve', query='test')
print('Out-of-scope result:', r)
"
```

Expected: `Out-of-scope result: {'error': "Domain 'davinci_resolve' not available in this server scope. Available: ['godot']"}`

- [ ] **Step 4: Commits in den jeweiligen Repos**

```bash
# nak-hopper-game
cd /Users/noahk/Documents/work/nak-hopper-game
git add .opencode/opencode.json
git commit -m "chore: scope knowledge_hub MCP to godot domain only"

# video-blog/meta
cd /Users/noahk/Documents/work/video-blog/meta
git add .opencode/opencode.json
git commit -m "feat(mcp): add davinci_resolve knowledge_hub MCP server"
```

---

## Task 10: Dokumentation & Decisions

**Files:**
- Create: `docs/decisions/2026-06-27-per-domain-isolation.md`
- Create: `docs/decisions/2026-06-27-agpl-process-boundary.md`
- Modify: `docs/ai/project-context.md`
- Modify: `docs/ai/architecture.md`
- Modify: `docs/ai/changelog.md`

- [ ] **Step 1: Schreibe docs/decisions/2026-06-27-per-domain-isolation.md**

```markdown
# ADR: Per-Domain ChromaDB Isolation

**Date:** 2026-06-27
**Status:** Accepted

## Context
Der Knowledge Hub lief bisher mit einer einzigen ChromaDB-Instanz für alle
Domains. Bei Hinzufügen einer DaVinci-Resolve-Domain würden beide Domains
RAM verbrauchen, auch wenn nur eine genutzt wird. Auf einem MacBook Pro M1
Max (32 GB) muss DaVinci Resolve Studio + OBS + Knowledge Hub parallel laufen.

## Decision
Jede Domain bekommt eine eigene ChromaDB-Datenbank unter
`chromadb_data/<domain>/chroma/` mit eigenem `PersistentClient` und
eigenem `chroma_memory_limit_bytes` (2 GB). Der MCP-Server akzeptiert ein
`--domains` CLI-Flag, das nur die konfigurierten Domains sichtbar macht.

## Consequences
- RAM-Isolation: nur die aktive Domain belegt Speicher.
- Zwei MCP-Prozesse (Godot + DaVinci) können parallel laufen (~1,7 GB).
- Migration des bestehenden Godot-Index nötig (automatisch mit Backup).
- `nak-hopper-game` und `video-blog` bekommen jeweils ihr `--domains` Flag.
- Embedding-Modell kann künftig per-Domain konfiguriert werden (domain.md).
```

- [ ] **Step 2: Schreibe docs/decisions/2026-06-27-agpl-process-boundary.md**

```markdown
# ADR: AGPL Process Boundary for PyMuPDF

**Date:** 2026-06-27
**Status:** Accepted

## Context
PyMuPDF und PyMuPDF4LLM stehen unter AGPL-3.0 (starkes Copyleft). Der
Knowledge Hub ist MIT-lizenziert und öffentlich auf GitHub. Ein direkter
`import pymupdf` im Runtime-Code würde ein abgeleitetes Werk erzeugen und
den gesamten Knowledge Hub unter AGPL zwingen — inkompatibel mit MIT.

## Decision
PyMuPDF4LLM wird NUR im separaten Build-Script
`scripts/parse_pdf_to_markdown.py` verwendet, das per subprocess aufgerufen
wird. Der MIT-lizenzierte Runtime-Code liest nur fertige `.md`-Dateien und
importiert niemals PyMuPDF. Diese "Process Boundary" ist der Standardweg
für AGPL/GPL-Dependencies in MIT-Projekten (analog GCC aus proprietären
Build-Systemen).

## Consequences
- `requirements.txt` (MIT-Runtime) enthält kein pymupdf.
- `requirements-pdf.txt` (AGPL-Build-Tool) enthält pymupdf + pymupdf4llm.
- `scripts/parse_pdf_to_markdown.py` hat AGPL-3.0 SPDX-Header.
- `THIRD_PARTY_LICENSES.md` dokumentiert die Trennung.
- PDFs werden einmalig konvertiert, danach ist PyMuPDF nicht mehr nötig.
- Die Lizenz-Trennung ist verbindlich — keine Ausnahme.
```

- [ ] **Step 3: Aktualisiere docs/ai/project-context.md**

Füge am Ende hinzu (falls Datei existiert, sonst erst erstellen):

```markdown
## Update 2026-06-27: Per-Domain Isolation + DaVinci Resolve

- Knowledge Hub unterstützt jetzt Per-Domain ChromaDB-Isolation.
- MCP-Server akzeptiert `--domains` CLI-Flag für Domain-Scoping.
- Neue Domain `davinci_resolve` mit 7 Blackmagic-PDF-Quellen.
- AGPL Process Boundary für PyMuPDF4LLM (Build-Tool only).
- Migration des Godot-Index in neues Layout erfolgt automatisch.
- `nak-hopper-game` nutzt `--domains godot`, `video-blog` nutzt `--domains davinci_resolve`.
```

- [ ] **Step 4: Aktualisiere docs/ai/architecture.md (falls vorhanden)**

Füge hinzu (oder erstelle):

```markdown
## Per-Domain Isolation (2026-06-27)

```
chromadb_data/
  godot/
    chroma/                 # eigene DB
    godot_bm25.pkl
  davinci_resolve/
    chroma/
    davinci_resolve_bm25.pkl
```

Model Manager (`scripts/model_manager.py`) ist die einzige Stelle, die
Embedding- und Reranker-Modelle lädt. Lazy-Loading, Per-Domain-Caching,
LRU-Eviction.

Domain-Scoping: `--domains` CLI-Flag auf dem MCP-Server begrenzt sichtbare
Domains. Default (ohne Flag): alle sichtbar (rückwärtskompatibel).
```

- [ ] **Step 5: Aktualisiere docs/ai/changelog.md (falls vorhanden)**

```markdown
## 2026-06-27

- **feat:** Per-Domain ChromaDB-Isolation (eigene DB pro Domain)
- **feat:** Domain-Scoped MCP-Server (`--domains` CLI-Flag)
- **feat:** Central Model Manager (lazy loading, LRU cache, unload)
- **feat:** PDF → Markdown Build-Script (PyMuPDF4LLM, AGPL Process Boundary)
- **feat:** DaVinci Resolve Domain (7 Blackmagic PDF-Quellen)
- **feat:** Search regression validation script
- **feat:** Automatic legacy layout migration with backup
- **docs:** THIRD_PARTY_LICENSES.md, ADRs for isolation + AGPL boundary
- **refactor:** All search modules use model_manager instead of direct
  SentenceTransformer/CrossEncoder instantiation
```

- [ ] **Step 6: Commit**

```bash
git add docs/decisions/ docs/ai/
git commit -m "docs: add ADRs for per-domain isolation and AGPL process boundary"
```

---

## Self-Review Checklist

Nach allen Tasks:

- [ ] Spec Coverage: jeder der 7 Spec-Abschnitte hat mindestens einen Task
  - Abschnitt 1 (Per-Domain Isolation): Tasks 1, 2, 7
  - Abschnitt 2 (Domain-Scoped Server): Task 3, 9
  - Abschnitt 3 (Memory Management): Task 1 (model_manager), Task 2 (refactor)
  - Abschnitt 4 (PDF-Parser): Task 4, 8
  - Abschnitt 5 (Migration): Task 1 (migration.py), Task 7
  - Abschnitt 6 (DaVinci-Domain): Task 5, 8, 9
  - Abschnitt 7 (Testing): Task 6, Task 7 (integration), Task 8 (search tests)

- [ ] Keine Platzhalter: alle Code-Blöcke sind vollständig
- [ ] Typ-Konsistenz: `set_domain_scope`, `list_scoped_domains`, `_check_domain_scope` in tools.py und server.py konsistent
- [ ] Lizenz-Trennung: `requirements.txt` hat kein pymupdf, `requirements-pdf.txt` hat pymupdf
- [ ] Migration ist idempotent und hat Backup
