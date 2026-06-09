"""Tool implementations for Knowledge Hub MCP Server."""

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from .config import DOMAINS_DIR, CHROMA_DIR, SCRIPTS_DIR, PERSONAL_DIR, MODEL_NAME

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
    """Search a domain's knowledge (exact, semantic, or hybrid)."""
    collection_name = f"{domain}_knowledge"

    if mode == "exact":
        # ripgrep exact search
        sources_dir = DOMAINS_DIR / domain / "sources"
        results = []
        if sources_dir.is_dir():
            try:
                output = subprocess.run(
                    ["rg", "--no-ignore", "-n", "-i", "--", query, str(sources_dir)],
                    capture_output=True, text=True, timeout=10,
                )
                for i, line in enumerate(output.stdout.strip().split("\n")[:max_results]):
                    if not line.strip():
                        continue
                    parts = line.split(":", 2)
                    text = parts[2][:300] if len(parts) >= 3 else line[:300]
                    results.append({
                        "rank": i + 1, "score": 1.0,
                        "source_type": "repo", "source": Path(parts[0]).stem,
                        "domain": domain, "text": text,
                        "match_type": "exact",
                    })
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass
        return {"results": results, "total_found": len(results), "mode": "exact"}

    # Semantic or hybrid
    model = get_model()
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    try:
        collection = client.get_collection(collection_name)
    except Exception:
        return {"error": f"Collection '{collection_name}' not found. Run embed_index.py first."}

    query_embedding = model.encode([query])[0]
    chroma_results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=max_results,
        include=["documents", "metadatas", "distances"],
    )

    semantic = []
    for i in range(len(chroma_results["ids"][0])):
        meta = chroma_results["metadatas"][0][i]
        st = meta.get("source_type", "unknown")

        # Apply source filter if provided
        if source_filter and st not in source_filter:
            continue

        semantic.append({
            "rank": i + 1,
            "score": round(1.0 - chroma_results["distances"][0][i], 4),
            "source_type": st,
            "source": meta.get("source", "unknown"),
            "domain": meta.get("domain", domain),
            "filename": meta.get("filename", ""),
            "line_offset": meta.get("line_offset", 0),
            "text": chroma_results["documents"][0][i][:300],
            "match_type": "semantic",
        })

    if mode == "semantic":
        return {"results": semantic[:max_results], "total_found": len(semantic), "mode": "semantic"}

    # Hybrid: merge exact + semantic via RRF
    # Exact via ripgrep
    sources_dir = DOMAINS_DIR / domain / "sources"
    personal_dir = DOMAINS_DIR / domain / "personal"
    exact = []
    for search_dir, st in [(sources_dir, "repo"), (personal_dir, "personal")]:
        if not search_dir.is_dir():
            continue
        try:
            output = subprocess.run(
                ["rg", "--no-ignore", "-n", "-i", "--", query, str(search_dir)],
                capture_output=True, text=True, timeout=10,
            )
            for i, line in enumerate(output.stdout.strip().split("\n")[:5]):
                if not line.strip():
                    continue
                parts = line.split(":", 2)
                text = parts[2][:300] if len(parts) >= 3 else line[:300]
                exact.append({
                    "source_type": st, "source": Path(parts[0]).stem,
                    "domain": domain, "text": text, "exact_rank": i + 1,
                })
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

    # RRF fusion
    k = 60
    scores: dict[str, float] = {}
    merged: dict[str, dict] = {}

    for r in semantic:
        cid = f"sem_{r['rank']}"
        scores[cid] = 1.0 / (k + r["rank"])
        merged[cid] = dict(r)
        merged[cid]["match_type"] = "hybrid"

    for i, r in enumerate(exact):
        cid = f"exact_{i}"
        scores[cid] = scores.get(cid, 0) + 1.0 / (k + i + 1)
        merged[cid] = dict(r)
        merged[cid]["match_type"] = "hybrid"
        merged[cid]["rank"] = i + 1

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:max_results]
    hybrid = []
    for idx, (cid, score) in enumerate(ranked):
        entry = dict(merged[cid])
        entry["rank"] = idx + 1
        entry["score"] = round(score, 4)
        hybrid.append(entry)

    return {"results": hybrid, "total_found": len(hybrid), "mode": "hybrid"}


# ── Status ────────────────────────────────────────────────────────────────


def get_domain_status(domain: str | None = None) -> dict:
    """Get status for one or all domains."""
    domains = [domain] if domain else list_domains()
    result = {}

    for d in domains:
        domain_dir = DOMAINS_DIR / d
        sources = list(domain_dir.glob("sources/*.md")) if domain_dir.is_dir() else []
        personal = list(domain_dir.glob("personal/*.md")) if domain_dir.is_dir() else []

        index_exists = False
        index_size_mb = 0
        if CHROMA_DIR.is_dir():
            col_dir = CHROMA_DIR  # chromadb stores all collections in one dir
            if col_dir.is_dir():
                total = sum(
                    f.stat().st_size for f in col_dir.rglob("*") if f.is_file()
                )
                index_size_mb = round(total / 1024 / 1024)

        # Check if collection exists
        try:
            client = chromadb.PersistentClient(path=str(CHROMA_DIR))
            client.get_collection(f"{d}_knowledge")
            index_exists = True
        except Exception:
            pass

        result[d] = {
            "sources": len(sources),
            "source_files": [s.name for s in sources],
            "personal_notes": len(personal),
            "personal_files": [p.name for p in personal],
            "index_exists": index_exists,
            "index_size_mb": index_size_mb,
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

    return {"status": "added", "domain": domain, "category": category, "topic": topic, "file": str(target)}


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
