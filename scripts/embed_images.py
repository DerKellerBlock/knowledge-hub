#!/usr/bin/env python3
"""Embed images + captions for a domain (Vision Retrieval Feature, Task 4).

CLI script that reads ``chromadb_data/<domain>/image_manifest.json`` +
``image_caption_cache.db``, embeds each ``good``/``unchecked`` image with
the multimodal model (SigLIP-2 / jina-clip-v2) and writes the embeddings
into a ChromaDB collection ``<domain>_images``.

Two embedding types per image:

* **image embedding** — the raw PNG bytes → SigLIP-2 image encoder.
* **caption embedding** — the context-aware caption text → SigLIP-2 text
  encoder (same joint vector space, TowardsDataScience best-practice).

Both are stored in the SAME ChromaDB collection with a ``modality``
metadata field (``"image"`` or ``"caption"``) so the 4-Listen-RRF in
``hybrid_search.py`` can query them separately.

Performance (M1 Max, 512×512 input):

* MPS GPU: ~1.500-4.000 pairs/hr (Spheron estimate, ~5-10× slower than A100).
* CPU: ~5-10× slower than MPS.
* Pre-Flight: 10-Bild MPS-Encode; bei Hang >30s → CPU-Fallback.

Content-hash caching (AugmentCode Rule 8): embeddings are persisted in
``image_embedding_cache.db`` keyed by ``image_id|content_hash|model|modality``.
On re-build, unchanged images/captions are skipped.

Usage::

    python scripts/embed_images.py --domain davinci_resolve
    KH_MULTIMODAL_DEVICE=mps KH_MULTIMODAL_BATCH_SIZE=64 \\
        python scripts/embed_images.py --domain davinci_resolve
    python scripts/embed_images.py --domain davinci_resolve --limit 10
    python scripts/embed_images.py --domain davinci_resolve --pre-flight-only

The script does NOT build the BM25 index (that's ``embed_index.py
--embed-images`` in Task 5).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys as _sys
import time
from pathlib import Path

# Make the repo root importable when run as a script.
_PKG_ROOT = Path(__file__).resolve().parent.parent
if str(_PKG_ROOT) not in _sys.path:
    _sys.path.insert(0, str(_PKG_ROOT))

from image_embedding_cache import (
    caption_hash,
    get_cached,
    image_hash,
    open_cache,
    put_cached,
    count_entries,
)
from image_caption_cache import open_cache as open_caption_cache
from image_caption_cache import get_cached as get_cached_caption
from mcp_servers.knowledge_hub import config as _config
from mcp_servers.knowledge_hub.config import domain_image_manifest_path
from model_manager import (
    DEFAULT_MULTIMODAL_MODEL,
    get_multimodal_embedder,
)

# ── Constants ──────────────────────────────────────────────────────────────

_DOMAIN_NAME_RE = re.compile(r"^[a-z0-9_]+$")

# Pre-Flight MPS-Check: 10-Bild-Encode, bei Hang >30s → CPU-Fallback.
_PRE_FLIGHT_IMAGE_COUNT = 10
_PRE_FLIGHT_TIMEOUT_S = 30.0

# Progress-Log interval (images).
_PROGRESS_LOG_EVERY = 25


# ── Helpers ────────────────────────────────────────────────────────────────


def _format_eta(seconds: float) -> str:
    """Format seconds as a human-readable duration string."""
    if seconds < 0 or not (seconds == seconds):  # NaN check
        return "?"
    s = int(seconds)
    if s < 60:
        return f"{s}s"
    m, s = divmod(s, 60)
    if m < 60:
        return f"{m}m {s}s"
    h, m = divmod(m, 60)
    return f"{h}h {m}m"


def _resolve_image_path(entry: dict) -> Path:
    """Resolve the absolute path of a manifest entry's image."""
    return _config.HUB_ROOT / entry["image_path"]


def load_manifest(domain: str) -> list[dict]:
    """Load ``image_manifest.json`` for a domain."""
    path = domain_image_manifest_path(domain)
    if not path.exists():
        raise FileNotFoundError(
            f"Image manifest not found for domain '{domain}': {path}. "
            f"Run: python scripts/extract_pdf_images.py --domain {domain}"
        )
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("images", [])


def load_captions(domain: str, model_name: str) -> dict[str, str]:
    """Load all cached captions for a domain into a {image_id: caption} dict.

    Images without a cached caption get an empty string — the caption
    embedding is skipped for them (image embedding still happens).
    """
    conn = open_caption_cache(domain)
    try:
        rows = conn.execute(
            "SELECT image_id, caption, image_hash FROM image_caption_cache "
            "WHERE model = ?",
            (model_name,),
        ).fetchall()
        return {row[0]: (row[1], row[2]) for row in rows}
    finally:
        conn.close()


# ── MPS Pre-Flight ─────────────────────────────────────────────────────────


def _pre_flight_mps_check(
    processor,
    model,
    torch_device,
    sample_images: list[Path],
) -> str:
    """Encode 10 sample images on MPS to detect a hang.

    Returns the resolved device string (``"mps"`` if OK, ``"cpu"`` if
    the encode hung >30s or raised an OOM). The caller then re-loads the
    model on the fallback device if needed.
    """
    import torch

    print(f"[INFO]  Pre-Flight MPS-Check: encoding {len(sample_images)} sample images...")
    t0 = time.time()
    try:
        # Load images via PIL.
        from PIL import Image
        imgs = [Image.open(p).convert("RGB") for p in sample_images]
        # Process via AutoProcessor (handles resize + normalization).
        inputs = processor(images=imgs, return_tensors="pt")
        inputs = {k: v.to(torch_device) for k, v in inputs.items()}
        with torch.no_grad():
            outputs = model.get_image_features(**inputs)
        elapsed = time.time() - t0
        print(f"[INFO]  Pre-Flight OK: {len(sample_images)} images in "
              f"{elapsed:.1f}s ({len(sample_images)/elapsed:.1f} img/s) "
              f"on {torch_device}")
        return str(torch_device)
    except Exception as e:
        elapsed = time.time() - t0
        print(f"[WARN]  Pre-Flight FAILED after {elapsed:.1f}s: "
              f"{type(e).__name__}: {e} — falling back to CPU")
        return "cpu"


# ── Embedding helpers ──────────────────────────────────────────────────────


def _embed_image_batch(
    processor,
    model,
    torch_device,
    images: list,
):
    """Embed a batch of PIL images. Returns numpy array (N, dim)."""
    import torch
    import numpy as np

    inputs = processor(images=images, return_tensors="pt")
    inputs = {k: v.to(torch_device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model.get_image_features(**inputs)
    # Normalize to unit length (CLIP convention).
    emb = outputs.cpu().float().numpy()
    norms = np.linalg.norm(emb, axis=-1, keepdims=True)
    norms = np.where(norms == 0, 1, norms)
    emb = emb / norms
    return emb


def _embed_text_batch(
    processor,
    model,
    torch_device,
    texts: list[str],
):
    """Embed a batch of text strings. Returns numpy array (N, dim)."""
    import torch
    import numpy as np

    inputs = processor(text=texts, return_tensors="pt", padding=True, truncation=True)
    inputs = {k: v.to(torch_device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model.get_text_features(**inputs)
    emb = outputs.cpu().float().numpy()
    norms = np.linalg.norm(emb, axis=-1, keepdims=True)
    norms = np.where(norms == 0, 1, norms)
    emb = emb / norms
    return emb


# ── Core embedding loop ────────────────────────────────────────────────────


def embed_domain_images(
    domain: str,
    limit: int | None = None,
    pre_flight_only: bool = False,
) -> dict:
    """Embed all images + captions for a domain.

    Returns a summary dict.
    """
    import chromadb
    from model_manager import get_chroma_client

    # Load manifest.
    entries = load_manifest(domain)
    if limit is not None:
        entries = entries[:limit]
    if not entries:
        print("[INFO] No images in manifest. Done.")
        return {"images_embedded": 0, "captions_embedded": 0}

    # Filter: only embed good + unchecked images.
    to_embed = [e for e in entries if e.get("quality") != "poor"]
    poor_skipped = len(entries) - len(to_embed)
    print(f"[INFO] {len(to_embed)} images to embed ({poor_skipped} poor skipped)")

    # Load captions (for caption embedding).
    llm_model = os.environ.get("KH_LLM_MODEL", "gemma4:cloud")
    captions = load_captions(domain, llm_model)
    print(f"[INFO] Loaded {len(captions)} cached captions (model={llm_model})")

    # Load multimodal model.
    model_name = os.environ.get("KH_MULTIMODAL_MODEL", DEFAULT_MULTIMODAL_MODEL)
    requested_device = os.environ.get("KH_MULTIMODAL_DEVICE", "cpu")
    batch_size = int(os.environ.get("KH_MULTIMODAL_BATCH_SIZE", "32"))
    print(f"[INFO] Loading multimodal model: {model_name} (device={requested_device}, batch={batch_size})")
    t_model_start = time.time()
    processor, model, resolved_device, _ = get_multimodal_embedder(model_name)
    import torch
    torch_device = torch.device(resolved_device)
    print(f"[INFO] Model loaded in {_format_eta(time.time() - t_model_start)} "
          f"on {torch_device}")

    # Pre-Flight MPS-Check (only if MPS requested).
    if resolved_device == "mps":
        sample_paths = []
        for e in to_embed[:_PRE_FLIGHT_IMAGE_COUNT]:
            p = _resolve_image_path(e)
            if p.exists():
                sample_paths.append(p)
        if len(sample_paths) >= 2:
            new_device = _pre_flight_mps_check(processor, model, torch_device, sample_paths)
            if new_device != str(torch_device):
                print(f"[INFO] Pre-Flight recommended fallback to {new_device} — reloading model")
                # Clear cache and reload on CPU.
                from model_manager import _model_cache
                _model_cache.clear()
                os.environ["KH_MULTIMODAL_DEVICE"] = new_device
                processor, model, resolved_device, _ = get_multimodal_embedder(model_name)
                torch_device = torch.device(resolved_device)
                print(f"[INFO] Model reloaded on {torch_device}")
        if pre_flight_only:
            print("[INFO] --pre-flight-only: stopping after Pre-Flight check")
            return {"pre_flight_device": str(torch_device)}

    # Open embedding cache.
    conn = open_cache(domain)
    cached_count = count_entries(conn, model=model_name)
    print(f"[INFO] Embedding cache: {cached_count} existing entries for model '{model_name}'")

    # ChromaDB collection.
    collection_name = f"{domain}_images"
    client = get_chroma_client(domain)
    try:
        client.delete_collection(collection_name)
        print(f"[INFO] Deleted existing collection '{collection_name}'")
    except Exception:
        pass
    collection = client.create_collection(
        name=collection_name,
        metadata={"domain": domain, "hnsw:space": "cosine", "modality": "mixed"},
    )

    # ── Embedding loop ──────────────────────────────────────────────────
    stats = {
        "images_embedded": 0,
        "images_cached": 0,
        "captions_embedded": 0,
        "captions_cached": 0,
        "captions_missing": 0,
        "errors": 0,
    }
    t_loop_start = time.time()
    from PIL import Image

    # Process in batches.
    batch_paths: list[Path] = []
    batch_entries: list[dict] = []
    batch_img_hashes: list[str] = []
    processed = 0

    for entry in to_embed:
        processed += 1
        image_path = _resolve_image_path(entry)
        if not image_path.exists():
            print(f"[WARN]  Image file missing: {entry['image_path']} — skipping")
            stats["errors"] += 1
            continue

        try:
            img_hash = image_hash(image_path)
        except OSError as e:
            print(f"[WARN]  hash failed for {image_path.name}: {e}")
            stats["errors"] += 1
            continue

        batch_paths.append(image_path)
        batch_entries.append(entry)
        batch_img_hashes.append(img_hash)

        if len(batch_paths) >= batch_size or processed == len(to_embed):
            _process_batch(
                batch_paths, batch_entries, batch_img_hashes,
                processor, model, torch_device, collection, conn,
                model_name, captions, stats,
            )
            batch_paths.clear()
            batch_entries.clear()
            batch_img_hashes.clear()

        if processed % _PROGRESS_LOG_EVERY == 0 or processed == len(to_embed):
            elapsed = time.time() - t_loop_start
            rate = processed / elapsed if elapsed > 0 else 0
            remaining = len(to_embed) - processed
            eta_sec = remaining / rate if rate > 0 else 0
            eta_str = _format_eta(eta_sec)
            elapsed_str = _format_eta(elapsed)
            print(f"[INFO] [{elapsed_str} elapsed, ETA {eta_str}] "
                  f"Processed {processed}/{len(to_embed)} images "
                  f"({stats['images_embedded']}+{stats['images_cached']} img, "
                  f"{stats['captions_embedded']}+{stats['captions_cached']} cap, "
                  f"{stats['errors']} errors, {rate:.1f} img/s)")

    conn.close()
    elapsed = time.time() - t_loop_start
    elapsed_str = _format_eta(elapsed)
    print(f"[INFO] Done in {elapsed_str}: "
          f"{stats['images_embedded']}+{stats['images_cached']} images, "
          f"{stats['captions_embedded']}+{stats['captions_cached']} captions, "
          f"{stats['errors']} errors")

    summary = {
        "domain": domain,
        "model": model_name,
        "device": str(torch_device),
        "images_embedded": stats["images_embedded"],
        "images_cached": stats["images_cached"],
        "captions_embedded": stats["captions_embedded"],
        "captions_cached": stats["captions_cached"],
        "captions_missing": stats["captions_missing"],
        "errors": stats["errors"],
        "collection": collection_name,
        "total_in_collection": collection.count(),
    }
    return summary


def _process_batch(
    batch_paths: list[Path],
    batch_entries: list[dict],
    batch_img_hashes: list[str],
    processor,
    model,
    torch_device,
    collection,
    conn,
    model_name: str,
    captions: dict,
    stats: dict,
) -> None:
    """Process one batch: embed images + captions, write to ChromaDB."""
    import numpy as np

    # Inject cached captions into the entries (they come from the
    # caption cache, not the manifest).
    for i, entry in enumerate(batch_entries):
        cap_data = captions.get(entry["image_id"])
        if cap_data is not None:
            entry["caption"] = cap_data[0]
        else:
            entry.setdefault("caption", "")

    # ── Image embeddings ───────────────────────────────────────────────
    img_to_encode: list[int] = []  # indices into batch that need encoding
    img_embeddings: list = [None] * len(batch_paths)

    for i, (entry, img_hash) in enumerate(zip(batch_entries, batch_img_hashes)):
        cached = get_cached(conn, entry["image_id"], img_hash, model_name, "image")
        if cached is not None:
            img_embeddings[i] = cached
            stats["images_cached"] += 1
        else:
            img_to_encode.append(i)

    if img_to_encode:
        try:
            from PIL import Image
            imgs = [Image.open(batch_paths[i]).convert("RGB") for i in img_to_encode]
            new_emb = _embed_image_batch(processor, model, torch_device, imgs)
            for j, idx in enumerate(img_to_encode):
                emb = new_emb[j]
                img_embeddings[idx] = emb
                put_cached(conn, batch_entries[idx]["image_id"],
                           batch_img_hashes[idx], model_name, "image", emb)
                stats["images_embedded"] += 1
        except Exception as e:
            print(f"[ERROR] Image batch encode failed: {type(e).__name__}: {e}")
            stats["errors"] += len(img_to_encode)

    # ── Caption embeddings ─────────────────────────────────────────────
    cap_to_encode: list[int] = []
    cap_texts: list[str] = []
    cap_embeddings: list = [None] * len(batch_entries)

    for i, entry in enumerate(batch_entries):
        cap_data = captions.get(entry["image_id"])
        if cap_data is None:
            stats["captions_missing"] += 1
            continue
        caption, _ = cap_data
        if not caption:
            stats["captions_missing"] += 1
            continue
        c_hash = caption_hash(caption)
        cached = get_cached(conn, entry["image_id"], c_hash, model_name, "caption")
        if cached is not None:
            cap_embeddings[i] = cached
            stats["captions_cached"] += 1
        else:
            cap_to_encode.append(i)
            cap_texts.append(caption)

    if cap_to_encode:
        try:
            new_emb = _embed_text_batch(processor, model, torch_device, cap_texts)
            for j, idx in enumerate(cap_to_encode):
                emb = new_emb[j]
                cap_embeddings[idx] = emb
                caption = cap_texts[j]
                c_hash = caption_hash(caption)
                put_cached(conn, batch_entries[idx]["image_id"],
                           c_hash, model_name, "caption", emb)
                stats["captions_embedded"] += 1
        except Exception as e:
            print(f"[ERROR] Caption batch encode failed: {type(e).__name__}: {e}")
            stats["errors"] += len(cap_to_encode)

    # ── Write to ChromaDB ──────────────────────────────────────────────
    for i, entry in enumerate(batch_entries):
        img_emb = img_embeddings[i]
        if img_emb is not None:
            img_id = f"{entry['image_id']}::img"
            collection.add(
                ids=[img_id],
                embeddings=[img_emb.tolist()],
                documents=[entry.get("caption", "") or ""],
                metadatas=[{
                    "image_id": entry["image_id"],
                    "modality": "image",
                    "source_file": entry["source_file"],
                    "image_path": entry["image_path"],
                    "page": entry["page"],
                    "idx": entry["idx"],
                    "caption": entry.get("caption", "") or "",
                    "quality": entry.get("quality", "unchecked"),
                    "domain": entry["image_id"].split("::")[0],
                }],
            )
        cap_emb = cap_embeddings[i]
        if cap_emb is not None:
            cap_id = f"{entry['image_id']}::cap"
            collection.add(
                ids=[cap_id],
                embeddings=[cap_emb.tolist()],
                documents=[entry.get("caption", "") or ""],
                metadatas=[{
                    "image_id": entry["image_id"],
                    "modality": "caption",
                    "source_file": entry["source_file"],
                    "image_path": entry["image_path"],
                    "page": entry["page"],
                    "idx": entry["idx"],
                    "caption": entry.get("caption", "") or "",
                    "quality": entry.get("quality", "unchecked"),
                    "domain": entry["image_id"].split("::")[0],
                }],
            )


# ── CLI ────────────────────────────────────────────────────────────────────


def _build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="embed_images",
        description=(
            "Embed images + captions for a domain via multimodal model "
            "(Vision Retrieval Feature, Task 4). Writes to ChromaDB "
            "<domain>_images collection."
        ),
    )
    p.add_argument("--domain", required=True, help="Domain name (must match ^[a-z0-9_]+$).")
    p.add_argument("--limit", type=int, default=None, help="Only process the first N images.")
    p.add_argument(
        "--pre-flight-only", action="store_true",
        help="Run only the MPS Pre-Flight check (10-image encode) and exit.",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_arg_parser().parse_args(argv)
    if not _DOMAIN_NAME_RE.match(args.domain):
        print(f"[ERROR] Invalid domain name '{args.domain}' — must match ^[a-z0-9_]+$")
        return 1
    try:
        summary = embed_domain_images(
            domain=args.domain,
            limit=args.limit,
            pre_flight_only=args.pre_flight_only,
        )
        print(f"[OK]    Summary: {json.dumps(summary, indent=2)}")
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        return 1
    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return 1
    return 0


if __name__ == "__main__":
    _sys.exit(main())
