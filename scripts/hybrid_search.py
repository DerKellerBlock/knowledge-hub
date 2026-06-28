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
