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
import time
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

    Both input lists must have "chunk_id" keys.
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
            if r.get("score"):
                meta[cid]["dense_score"] = r.get("score", 0)
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
