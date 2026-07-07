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
from hyde import generate_hypothetical_document, should_use_hyde
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


    return enriched


def image_similarity_search(
    domain: str,
    image_path: str,
    top_k: int = 10,
) -> list[dict]:
    """Find similar screenshots by image embedding (VQA Feature, Task 1).

    Loads the query image, embeds it with the multimodal model (SigLIP-2 /
    jina-clip-v2 — same vector space as the indexed screenshots), and queries
    the ``<domain>_images`` ChromaDB collection (``modality="image"``) by
    cosine similarity. The top-k image entries are enriched with their
    caption + page + source_file metadata from the matching
    ``<image_id>::cap`` caption entry so the caller can explain what the
    screenshot shows.

    Content-hash caching: query-image embeddings are persisted in
    ``image_embedding_cache.db`` with ``modality="query_image"`` (NOT
    ``"image"`` — that is the modality of the indexed screenshots, and we
    must not collide the cache keyspace). Cache-Key is
    ``image_id="query"`` (a stable placeholder) + content_hash of the
    query image bytes + model + ``"query_image"``.

    Graceful failure: any error (file missing, PIL decode failure,
    SigLIP-2 not available, images collection missing) returns an empty
    list + a warning log. The caller (``search_knowledge``) treats an
    empty list as "no image_match results" — fully backward compatible.

    Args:
        domain: Domain name (must have an ``<domain>_images`` collection).
        image_path: Absolute path to a query image file (PNG/JPG/...).
        top_k: Number of similar screenshots to return.

    Returns:
        List of ``image_match`` result dicts sorted by ``similarity_score``
        (descending). Each entry has:

        * ``chunk_id`` — the image entry id (``<image_id>::img``)
        * ``image_id`` — stable image identifier
        * ``modality`` — ``"image_match"`` (distinguishes from text/image/caption)
        * ``match_type`` — ``"image_similarity"``
        * ``similarity_score`` — cosine similarity (0..1, higher = more similar)
        * ``score`` — alias of ``similarity_score`` (for sort-compat with RRF)
        * ``caption`` — caption text of the matched screenshot
        * ``image_path`` — relative path of the matched screenshot
        * ``source_file`` — source PDF / markdown file
        * ``page`` — 0-based PDF page (VRF-001)
        * ``idx`` — image index on the page
        * ``quality`` — caption quality flag
        * ``domain`` — domain name
        * ``text`` — the caption text (so the reranker / LLM can read it)
    """
    # ── Validate input path ────────────────────────────────────────────
    p = Path(image_path)
    if not p.is_file():
        logger.warning(
            "image_similarity_search: image not found: %s — returning []",
            image_path,
        )
        return []

    # ── Load image via PIL ─────────────────────────────────────────────
    try:
        from PIL import Image
        img = Image.open(p).convert("RGB")
    except Exception as e:
        logger.warning(
            "image_similarity_search: PIL failed to open %s: %s: %s — returning []",
            image_path, type(e).__name__, e,
        )
        return []

    # ── Load multimodal embedder ───────────────────────────────────────
    from model_manager import get_multimodal_embedder
    try:
        processor, mm_model, device, _ = get_multimodal_embedder()
    except Exception as e:
        logger.warning(
            "image_similarity_search: multimodal embedder unavailable: %s: %s — returning []",
            type(e).__name__, e,
        )
        return []

    # ── Content-hash cache lookup ──────────────────────────────────────
    # Query-image embeddings use modality="query_image" so they don't
    # collide with indexed-screenshot embeddings (modality="image").
    import os
    from image_embedding_cache import (
        open_cache as open_emb_cache,
        get_cached as get_emb_cached,
        put_cached as put_emb_cached,
        image_hash as _image_hash,
    )
    model_name = os.environ.get(
        "KH_MULTIMODAL_MODEL",
        "google/siglip2-so400m-patch16-512",
    )
    try:
        img_hash = _image_hash(p)
    except OSError as e:
        logger.warning(
            "image_similarity_search: hash failed for %s: %s — returning []",
            image_path, e,
        )
        return []

    # Use a stable placeholder image_id for query images so the cache key
    # is deterministic across calls for the same image bytes + model.
    query_image_id = "query"

    embedding = None
    try:
        conn = open_emb_cache(domain)
        try:
            embedding = get_emb_cached(
                conn, query_image_id, img_hash, model_name, "query_image",
            )
        finally:
            conn.close()
    except Exception as e:
        logger.warning(
            "image_similarity_search: cache lookup failed: %s: %s — proceeding without cache",
            type(e).__name__, e,
        )

    # ── Embed the query image with SigLIP-2 ────────────────────────────
    if embedding is None:
        try:
            import torch
            import numpy as np
            torch_device = torch.device(device)
            inputs = processor(images=[img], return_tensors="pt")
            inputs = {k: v.to(torch_device) for k, v in inputs.items()}
            with torch.no_grad():
                outputs = mm_model.get_image_features(**inputs)
            emb = outputs.cpu().float().numpy()
            if emb.ndim == 2 and emb.shape[0] == 1:
                emb = emb[0]
            norms = np.linalg.norm(emb, axis=-1, keepdims=True)
            norms = np.where(norms == 0, 1, norms)
            embedding = emb / norms
        except Exception as e:
            logger.warning(
                "image_similarity_search: SigLIP-2 encode failed: %s: %s — returning []",
                type(e).__name__, e,
            )
            return []

        # Persist in cache so subsequent queries for the same image are free.
        try:
            conn = open_emb_cache(domain)
            try:
                put_emb_cached(
                    conn, query_image_id, img_hash, model_name,
                    "query_image", embedding,
                )
            finally:
                conn.close()
        except Exception as e:
            logger.warning(
                "image_similarity_search: cache write failed: %s: %s — ignoring",
                type(e).__name__, e,
            )

    # ── Query ChromaDB <domain>_images (modality="image") ──────────────
    try:
        client = get_chroma_client(domain)
        collection = client.get_collection(f"{domain}_images")
    except Exception as e:
        logger.warning(
            "image_similarity_search: %s_images collection missing for domain '%s': %s — returning []",
            domain, domain, e,
        )
        return []

    try:
        results = collection.query(
            query_embeddings=[embedding.tolist()],
            n_results=top_k,
            where={"modality": "image"},
            include=["metadatas", "distances"],
        )
    except Exception as e:
        logger.warning(
            "image_similarity_search: ChromaDB query failed: %s: %s — returning []",
            type(e).__name__, e,
        )
        return []

    # ── Build result list ──────────────────────────────────────────────
    # ChromaDB returns cosine *distance* (lower = more similar). Convert
    # to similarity score (1 - distance, clamped to [0, 1]).
    formatted = []
    ids = results.get("ids", [[]])
    metas = results.get("metadatas", [[]])
    dists = results.get("distances", [[]])
    if not ids or not ids[0]:
        return []

    for i in range(len(ids[0])):
        meta = metas[0][i] or {}
        distance = dists[0][i]
        # ChromaDB cosine: distance in [0, 2]; similarity = 1 - distance.
        similarity = max(0.0, min(1.0, 1.0 - float(distance)))
        image_id = meta.get("image_id", "")
        formatted.append({
            "chunk_id": ids[0][i],
            "image_id": image_id,
            "modality": "image_match",
            "match_type": "image_similarity",
            "similarity_score": round(similarity, 4),
            "score": round(similarity, 4),  # sort-compat alias
            "image_path": meta.get("image_path", ""),
            "source_file": meta.get("source_file", ""),
            "page": meta.get("page"),
            "idx": meta.get("idx"),
            "caption": meta.get("caption", ""),
            "quality": meta.get("quality", "unchecked"),
            "domain": meta.get("domain", domain),
            "text": (meta.get("caption", "") or "")[:5000],
            "rerank_score": None,
            "stage1_score": round(similarity, 4),
        })

    # Sort by similarity descending (ChromaDB may already sort, but be explicit).
    formatted.sort(key=lambda r: r["similarity_score"], reverse=True)

    # Reassign sequential ranks 1..N.
    for i, entry in enumerate(formatted):
        entry["rank"] = i + 1

    return formatted


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
    image_path: str | None = None,
) -> dict:
    """Search knowledge in a domain.

    When ``image_path`` is set (Visual Question Answering Feature), an
    additional :func:`image_similarity_search` is run: the query image is
    embedded with SigLIP-2 and similar screenshots from the
    ``<domain>_images`` collection are appended to the results with
    ``modality="image_match"``. The text/image/caption search pipeline
    runs unchanged (4-list RRF + cross-encoder rerank). Without
    ``image_path`` the behavior is identical to the previous signature
    (backward compatible).
    """
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
    # HyDE: generate hypothetical document for better embedding match.
    # BM25 still uses the raw query (keyword overlap is important).
    query_for_embedding = query
    if should_use_hyde(query):
        query_for_embedding = generate_hypothetical_document(query)
    dense_results = semantic_search(domain, query_for_embedding, 100, model)

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

    # Re-merge: interleave text and image entries so image-centric queries
    # get visible image results. The cross-encoder reranker scores text
    # entries in a much higher range (~5-7) than image RRF scores (~0.03),
    # so a pure score-sort would push all images to the bottom. Instead we
    # reserve 1/3 of top_k slots for images and interleave: the best image
    # appears at rank 2, the second at rank 4, etc., so a user scanning
    # top-5 sees both text and image results.
    for r in image_entries:
        r["rerank_score"] = None
        r["stage1_score"] = r.get("score")

    text_entries.sort(key=lambda r: r.get("rerank_score", r.get("score", 0)), reverse=True)
    image_entries.sort(key=lambda r: r.get("stage1_score", r.get("score", 0)), reverse=True)

    image_budget = min(len(image_entries), max(1, top_k // 3)) if image_entries else 0
    text_budget = top_k - image_budget

    # Interleave: take 2 text, 1 image, 2 text, 1 image, ...
    # This gives images visible positions without a pure score-sort
    # that would bury them at the bottom.
    merged = []
    ti = 0  # text index
    ii = 0  # image index
    text_slice = text_entries[:text_budget]
    image_slice = image_entries[:image_budget]
    while ti < len(text_slice) or ii < len(image_slice):
        # Take 2 text entries (or 1 if only 1 left)
        for _ in range(2):
            if ti < len(text_slice):
                merged.append(text_slice[ti])
                ti += 1
        # Take 1 image entry
        if ii < len(image_slice):
            merged.append(image_slice[ii])
            ii += 1
    fused = merged[:top_k]

    # ── Visual Question Answering: image similarity matches ───────────
    # When image_path is set, run image_similarity_search ADDITIONALLY
    # to the 4-list RRF and prepend the image_match results to the
    # merged list. They get their own modality="image_match" so consumers
    # can distinguish them from text/image/caption hits. Without
    # image_path this block is skipped entirely (backward-compat).
    image_match_results: list[dict] = []
    if image_path:
        try:
            image_match_results = image_similarity_search(
                domain, image_path, top_k=top_k,
            )
        except Exception as e:
            logger.warning(
                "search: image_similarity_search failed for image_path=%s: %s: %s — continuing without image_match results",
                image_path, type(e).__name__, e,
            )
            image_match_results = []

    # Prepend image_match results so the LLM sees the most similar
    # screenshots first (highest similarity_score). They are NOT mixed
    # into the interleave budget — they are additive on top of the
    # text/image/caption results.
    if image_match_results:
        # Cap image_match to top_k so the combined list does not exceed
        # 2*top_k (text top_k + image_match top_k).
        image_match_results = image_match_results[:top_k]
        fused = image_match_results + fused

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
        "image_match_count": len(image_match_results),
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
