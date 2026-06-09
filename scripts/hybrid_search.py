#!/usr/bin/env python3
"""
Hybrid search: combination of ripgrep (exact) + ChromaDB (semantic).

Usage:
  python scripts/hybrid_search.py --domain godot --query "CharacterBody3D" --top 10
  python scripts/hybrid_search.py --domain godot --query "gravity" --json

Algorithm:
  1. Parallel queries: ripgrep + ChromaDB
  2. RRF-Fusion (Reciprocal Rank Fusion, k=60)
  3. Deduplication (same chunks merged)
  4. Ranking by combined score

Requirements:
  - ripgrep (brew install ripgrep)
  - chromadb, sentence-transformers (pip install)
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from embed_search import semantic_search

HUB_ROOT = Path(__file__).resolve().parent.parent
DOMAINS_DIR = HUB_ROOT / "domains"
MODEL_NAME = "all-mpnet-base-v2"


def exact_search(domain: str, query: str, max_results: int = 10) -> list[dict]:
    """Exact search using ripgrep on domain source files."""
    sources_dir = DOMAINS_DIR / domain / "sources"
    personal_dir = DOMAINS_DIR / domain / "personal"

    results = []

    for search_dir, source_type in [(sources_dir, "repo"), (personal_dir, "personal")]:
        if not search_dir.is_dir():
            continue

        try:
            output = subprocess.run(
                ["rg", "-L", "--no-ignore", "-n", "-i", "--", query, str(search_dir)],
                capture_output=True,
                text=True,
                timeout=10,
            )
            lines = output.stdout.strip().split("\n")

            for i, line in enumerate(lines[:max_results]):
                if not line.strip():
                    continue
                # Format: filename:lineno:text
                parts = line.split(":", 2)
                if len(parts) >= 3:
                    filename = parts[0]
                    lineno = parts[1]
                    text = parts[2][:500]
                else:
                    filename = "unknown"
                    lineno = "0"
                    text = line[:500]

                # Determine source name from filename
                source_name = Path(filename).stem.replace("-packed", "")

                results.append(
                    {
                        "rank": i + 1,
                        "score": 1.0,
                        "source_type": source_type,
                        "source": source_name,
                        "domain": domain,
                        "filename": Path(filename).name,
                        "line_offset": int(lineno) if lineno.isdigit() else 0,
                        "text": text,
                        "chunk_id": f"exact_{domain}_{i}",
                        "match_type": "exact",
                    }
                )
        except (subprocess.TimeoutExpired, FileNotFoundError):
            # ripgrep not found or timeout
            pass

    return results


def rrf_fusion(
    exact_results: list[dict],
    semantic_results: list[dict],
    k: int = 60,
) -> list[dict]:
    """Reciprocal Rank Fusion: combine exact and semantic results."""
    # Build score map: chunk_id -> accumulated RRF score
    scores: dict[str, float] = {}
    meta: dict[str, dict] = {}

    # Exact results
    for i, r in enumerate(exact_results):
        rank = i + 1
        cid = r.get("chunk_id", f"exact_{i}")
        scores[cid] = scores.get(cid, 0) + 1.0 / (k + rank)

        if cid not in meta or meta[cid].get("match_type") == "exact":
            meta[cid] = dict(r)
            meta[cid]["match_type"] = "hybrid"

    # Semantic results
    for i, r in enumerate(semantic_results):
        rank = i + 1
        cid = r.get("chunk_id", f"semantic_{i}")
        scores[cid] = scores.get(cid, 0) + 1.0 / (k + rank)

        if cid not in meta:
            meta[cid] = dict(r)
            meta[cid]["match_type"] = "hybrid"

    # Sort by combined score, limit to top-N
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_n = min(10, len(ranked))

    hybrid_results = []
    for idx, (cid, score) in enumerate(ranked[:top_n]):
        entry = dict(meta[cid])
        entry["rank"] = idx + 1
        entry["score"] = round(score, 4)
        hybrid_results.append(entry)

    return hybrid_results


def main():
    parser = argparse.ArgumentParser(
        description="Hybrid search (ripgrep + ChromaDB) in Knowledge Hub"
    )
    parser.add_argument("--domain", type=str, required=True, help="Domain to search")
    parser.add_argument("--query", type=str, required=True, help="Search query")
    parser.add_argument("--top", type=int, default=10, help="Max results")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    print(f"[INFO]  Hybrid search in '{args.domain}': {args.query}")
    print(f"[INFO]  Loading model {MODEL_NAME}...")

    model = SentenceTransformer(MODEL_NAME)

    # Exact search
    print(f"[INFO]  ripgrep search...")
    exact = exact_search(args.domain, args.query, args.top)

    # Semantic search
    print(f"[INFO]  ChromaDB search...")
    try:
        semantic = semantic_search(args.domain, args.query, args.top, model)
    except SystemExit:
        semantic = []

    # Fusion
    print(f"[INFO]  RRF fusion (k=60)...")
    all_results = rrf_fusion(exact, semantic)

    # Output
    if args.json:
        print(
            json.dumps(
                {
                    "results": all_results,
                    "total_found": len(all_results),
                    "exact_count": len(exact),
                    "semantic_count": len(semantic),
                },
                indent=2,
            )
        )
    else:
        for r in all_results:
            source_label = f"[{r['source_type']}:{r['source']}]"
            match_label = f"[{r['match_type']}]"
            print(f"\n  #{r['rank']} {source_label} {match_label} (score: {r['score']})")
            print(f"  {r['text'][:200]}...")

    print(f"\n[INFO]  Exact: {len(exact)}, Semantic: {len(semantic)}, "
          f"Hybrid: {len(all_results)} total")


if __name__ == "__main__":
    main()
