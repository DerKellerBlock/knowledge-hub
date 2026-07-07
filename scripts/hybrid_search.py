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
from bm25_search import bm25_search, image_bm25_search, get_image_bm25_index_size_mb
from reranker import rerank
from mcp_servers.knowledge_hub.config import domain_image_bm25_path

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
                "context_prefix": r.get("context_prefix"),
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


def _image_semantic_search(domain: str, query: str, top_k: int, model) -> list[dict]:
    """Semantic search over the <domain>_images ChromaDB collection.

    Returns caption-modality results (text embeddings of captions) since
    the cross-encoder reranker only works on text. Image-modality results
    are mixed in by RRF rank only (AugmentCode: don't rerank images with
    a text cross-encoder — modality gap).

    Returns an empty list if the images collection does not exist
    (backward-compat for domains without vision retrieval).
    """
    try:
        client = get_chroma_client(domain)
        collection = client.get_collection(f"{domain}_images")
    except Exception:
        return []

    # Encode the query with the multimodal text encoder.
    # We use the same text embedder (BGE-M3) that indexed the captions
    # via the multimodal model's text head — BUT the multimodal caption
    # embeddings live in a different vector space than BGE-M3 text
    # embeddings. So we must use the multimodal model's text encoder here.
    from model_manager import get_multimodal_embedder
    try:
        processor, mm_model, device, _ = get_multimodal_embedder()
    except Exception:
        return []

    import torch
    import numpy as np
    torch_device = torch.device(device)
    inputs = processor(text=[query], return_tensors="pt", padding=True, truncation=True)
    inputs = {k: v.to(torch_device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = mm_model.get_text_features(**inputs)
    q_emb = outputs.cpu().float().numpy()
    # Squeeze batch dim if present: shape (1, dim) -> (dim,).
    if q_emb.ndim == 2 and q_emb.shape[0] == 1:
        q_emb = q_emb[0]
    norms = np.linalg.norm(q_emb, axis=-1, keepdims=True)
    norms = np.where(norms == 0, 1, norms)
    q_emb = q_emb / norms

    # Query only caption-modality entries (image entries are mixed in by
    # RRF from the image_bm25 + image-vector lists, but NOT reranked).
    results = collection.query(
        query_embeddings=[q_emb.tolist()],
        n_results=top_k,
        where={"modality": "caption"},
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
        entry = {
            "chunk_id": results["ids"][0][i],  # caption entry id
            "image_id": meta.get("image_id", ""),
            "score": score,
            "text": (results["documents"][0][i] or "")[:5000],
            "match_type": "image_semantic",
            "modality": "caption",
            "source_file": meta.get("source_file", ""),
            "image_path": meta.get("image_path", ""),
            "page": meta.get("page"),
            "idx": meta.get("idx"),
            "caption": meta.get("caption", ""),
            "quality": meta.get("quality", "unchecked"),
            "domain": meta.get("domain", domain),
        }
        formatted.append(entry)
    return formatted


def _resolve_image_metadata(domain: str, image_bm25_results: list[dict]) -> list[dict]:
    """Enrich image_bm25_search results with caption + image_path from ChromaDB."""
    if not image_bm25_results:
        return []
    try:
        client = get_chroma_client(domain)
        collection = client.get_collection(f"{domain}_images")
    except Exception:
        return []
    # Look up the caption entries (image_id + "::cap") for each image_id.
    cap_ids = [f"{r['image_id']}::cap" for r in image_bm25_results]
    try:
        batch = collection.get(ids=cap_ids, include=["metadatas", "documents"])
    except Exception:
        return []
    id_to_meta = {}
    id_to_doc = {}
    for cid, meta, doc in zip(batch["ids"], batch["metadatas"], batch["documents"]):
        id_to_meta[cid] = meta
        id_to_doc[cid] = doc
    enriched = []
    for r in image_bm25_results:
        cap_id = f"{r['image_id']}::cap"
        meta = id_to_meta.get(cap_id, {})
        doc = id_to_doc.get(cap_id, "")
        enriched.append({
            "chunk_id": r["image_id"],  # use image_id as chunk_id for RRF
            "image_id": r["image_id"],
            "score": r["score"],
            "text": (doc or "")[:5000],
            "match_type": "image_bm25",
            "modality": "image",
            "source_file": meta.get("source_file", ""),
            "image_path": meta.get("image_path", ""),
            "page": meta.get("page"),
            "idx": meta.get("idx"),
            "caption": meta.get("caption", ""),
            "quality": meta.get("quality", "unchecked"),
            "domain": meta.get("domain", domain),
        })
    return enriched


def rrf_fusion_4list(
    text_sparse: list[dict],
    text_dense: list[dict],
    image_sparse: list[dict],
    image_dense: list[dict],
    k_text: int = 60,
    k_image: int = 30,
    top_n: int = 50,
) -> list[dict]:
    """4-Listen-RRF für Text + Bild (Vision Retrieval Feature).

    Modality-Gap-Berücksichtigung (Spheron Benchmark): Bild-Listen
    bekommen einen kleineren k-Wert (k_image=30) so dass Bild-Treffer
    stärker gewichtet werden (1/(30+rank) > 1/(60+rank)) — das
    Kompensiert den Modality-Gap zwischen Text- und Bild-Embeddings.

    Text- und Bild-Listen haben unterschiedliche chunk_id-Räume
    (Text: ``<domain>::...``, Bild: ``<domain>::img::...``), sodass sie
    sich in der RRF-Score-Map nicht gegenseitig überschreiben.
    """
    scores: dict[str, float] = {}
    meta: dict[str, dict] = {}

    def _add_list(results: list[dict], source_tag: str, k: int):
        for i, r in enumerate(results):
            cid = r["chunk_id"]
            rank = i + 1
            scores[cid] = scores.get(cid, 0) + 1.0 / (k + rank)
            if cid not in meta:
                meta[cid] = {
                    "chunk_id": cid,
                    "stage1_sources": [source_tag],
                    "text": r.get("text", ""),
                    "modality": r.get("modality", "text"),
                }
                # Propagate all fields from the result.
                for key, value in r.items():
                    if key in ("chunk_id", "stage1_sources"):
                        continue
                    if value is not None:
                        meta[cid][key] = value
            else:
                if source_tag not in meta[cid]["stage1_sources"]:
                    meta[cid]["stage1_sources"].append(source_tag)
                # Merge non-None fields.
                for key, value in r.items():
                    if key in ("chunk_id", "stage1_sources"):
                        continue
                    if value is not None and meta[cid].get(key) is None:
                        meta[cid][key] = value

    _add_list(text_sparse, "text_bm25", k_text)
    _add_list(text_dense, "text_semantic", k_text)
    _add_list(image_sparse, "image_bm25", k_image)
    _add_list(image_dense, "image_semantic", k_image)

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]

    results = []
    for idx, (cid, rrf_score) in enumerate(ranked):
        entry = dict(meta[cid])
        entry["rank"] = idx + 1
        entry["score"] = round(rrf_score, 4)
        entry["match_type"] = "hybrid_4list" if (image_sparse or image_dense) else "hybrid"
        results.append(entry)
    return results


def _has_image_index(domain: str) -> bool:
    """Check whether a domain has an image BM25 + images collection.

    Returns True only if BOTH the image BM25 pickle AND the images
    ChromaDB collection exist. Used to decide whether to attempt the
    4-list path or fall back to 2-list RRF (backward-compat).
    """
    if not domain_image_bm25_path(domain).exists():
        return False
    try:
        client = get_chroma_client(domain)
        client.get_collection(f"{domain}_images")
        return True
    except Exception:
        return False


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
                r["context_prefix"] = r.get("context_prefix") or meta.get("context_prefix")
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

    # Hybrid — use 4-list RRF if the domain has an image index, else 2-list.
    model = get_embedder(domain)
    bm25_results = bm25_search(domain, query, top_k=100)
    dense_results = semantic_search(domain, query, 100, model)

    if source_filter:
        bm25_results = [r for r in bm25_results if r.get("source_type") in source_filter]
        dense_results = [r for r in dense_results if r.get("source_type") in source_filter]

    if _has_image_index(domain):
        # Vision Retrieval Feature: 4-list RRF.
        img_bm25_raw = image_bm25_search(domain, query, top_k=50)
        img_bm25_results = _resolve_image_metadata(domain, img_bm25_raw)
        img_dense_results = _image_semantic_search(domain, query, 50, model)
        fused = rrf_fusion_4list(
            bm25_results, dense_results,
            img_bm25_results, img_dense_results,
            k_text=60, k_image=30, top_n=50,
        )
        # Resolve text for text-modality entries missing text.
        _resolve_texts_via_chromadb(domain, fused)
    else:
        # Legacy 2-list RRF (backward-compat for domains without images).
        fused = rrf_fusion(bm25_results, dense_results, k=60, top_n=50)
        _resolve_texts_via_chromadb(domain, fused)

    # Cross-encoder reranking: ONLY on text-modality entries. Image
    # entries lack a text cross-encoder (modality gap) — they stay by
    # RRF rank. We split, rerank text, then re-merge by score.
    text_entries = [r for r in fused if r.get("modality", "text") == "text"]
    image_entries = [r for r in fused if r.get("modality") == "image" or r.get("modality") == "caption"]

    if is_reranker_available() and len(text_entries) > 0:
        try:
            text_entries = rerank(query, text_entries, top_k=top_k)
        except Exception as e:
            logger.warning(f"Cross-encoder reranking failed: {e}. Using RRF-only.")
            text_entries = text_entries[:top_k]
    else:
        text_entries = text_entries[:top_k]

    # Re-merge: interleave by rerank_score (text) / rrf_score (image).
    # Mixed-modality merge: reserve up to 1/3 of top_k slots for image
    # entries so image-centric queries get at least one image result.
    # Text entries are sorted by rerank_score, images by RRF score.
    for r in image_entries:
        r["rerank_score"] = None
        r["stage1_score"] = r.get("score")

    text_entries.sort(key=lambda r: r.get("rerank_score", r.get("score", 0)), reverse=True)
    image_entries.sort(key=lambda r: r.get("stage1_score", r.get("score", 0)), reverse=True)

    image_budget = min(len(image_entries), max(1, top_k // 3)) if image_entries else 0
    text_budget = top_k - image_budget

    merged = text_entries[:text_budget] + image_entries[:image_budget]
    def _sort_key(r):
        if r.get("rerank_score") is not None:
            return (1, r["rerank_score"])
        return (0, r.get("stage1_score", r.get("score", 0)))
    merged.sort(key=_sort_key, reverse=True)
    fused = merged[:top_k]
    # Re-assign sequential ranks 1..N after the merge so consumers see a
    # contiguous ranking (the RRF rank and rerank position would otherwise
    # leak through as non-sequential numbers).
    for i, entry in enumerate(fused):
        entry["rank"] = i + 1

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
