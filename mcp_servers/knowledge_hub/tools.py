"""Tool implementations for Knowledge Hub MCP Server."""

import json
import re
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


# ── Status ────────────────────────────────────────────────────────────────


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


# ── Personal Notes ────────────────────────────────────────────────────────


def add_personal_note(
    domain: str, topic: str, content: str, category: str = "gotchas"
) -> dict:
    """Add a personal note to a domain's knowledge."""
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
