"""Tool implementations for Knowledge Hub MCP Server."""

import re
import subprocess
from datetime import datetime
from pathlib import Path

from .config import DOMAINS_DIR

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
