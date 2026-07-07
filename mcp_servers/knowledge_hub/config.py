"""Configuration for Knowledge Hub MCP Server."""

import os
from pathlib import Path

# Repository root (knowledge-hub/)
HUB_ROOT = Path(__file__).resolve().parent.parent.parent
DOMAINS_DIR = HUB_ROOT / "domains"
SCRIPTS_DIR = HUB_ROOT / "scripts"
CHROMA_DIR = HUB_ROOT / "chromadb_data"
PERSONAL_DIR = HUB_ROOT / "personal"

# Cross-encoder model (Stage 2 reranking).
# Configurable via KH_RERANKER_MODEL environment variable.
# Default keeps the legacy ms-marco MiniLM so existing installs work
# without a ~1.1 GB model download. Recommended override:
#   jinaai/jina-reranker-v2-base-multilingual (multilingual, 1024 tokens,
#   CC-BY-NC-4.0 — see THIRD_PARTY_LICENSES.md).
CROSS_ENCODER_MODEL = os.environ.get(
    "KH_RERANKER_MODEL",
    "cross-encoder/ms-marco-MiniLM-L-12-v2",
)

# Default embedding model. Used as a fallback constant only — the live
# model name is resolved in ``model_manager.get_embedder()`` from
# (1) the ``KH_EMBEDDING_MODEL`` env var, (2) the domain.md ``Metadaten``
# block, (3) this constant, in that order (Decision 2.7).
DEFAULT_MODEL_NAME = "all-mpnet-base-v2"

# Name of the environment variable that overrides the embedding model at
# runtime (Phase 2a, Decision 2.2). Kept as a constant so callers don't
# hard-code the string in multiple places.
EMBEDDING_MODEL_ENV_VAR = "KH_EMBEDDING_MODEL"

# Phase 3.1 Contextual Retrieval — local LLM defaults.
# Reference constants (env-aware at import time) for documentation and
# other modules. The live model is resolved in model_manager.get_llm()
# from the KH_LLM_MODEL / KH_LLM_BACKEND env vars on every cache-miss,
# with the STATIC fallbacks in model_manager.py (DEFAULT_LLM_MODEL /
# DEFAULT_LLM_BACKEND) — same dual-source pattern as CROSS_ENCODER_MODEL
# (config.py, env-aware) vs DEFAULT_RERANKER_MODEL (model_manager.py,
# static). Functionally identical because get_llm() reads the env live.
DEFAULT_LLM_MODEL = os.environ.get(
    "KH_LLM_MODEL",
    "gemma4:12b-mlx",
)
DEFAULT_LLM_BACKEND = os.environ.get("KH_LLM_BACKEND", "ollama")

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


# Vision Retrieval Feature — Multimodal Embedding + Vision LLM defaults.
# Reference constants (env-aware at import time) for documentation and other
# modules. The live model is resolved in model_manager.get_multimodal_embedder()
# from the KH_MULTIMODAL_MODEL env var on every cache-miss, with the STATIC
# fallback in model_manager.py (DEFAULT_MULTIMODAL_MODEL) — same dual-source
# pattern as CROSS_ENCODER_MODEL (config.py, env-aware) vs
# DEFAULT_RERANKER_MODEL (model_manager.py, static).
#
# Default: google/siglip2-so400m-patch16-512 (Apache 2.0, kommerziell sicher,
# English-only, 512x512, 1152 dims). Optional: jinaai/jina-clip-v2
# (CC-BY-NC-4.0, multilingual, 1024 dims, analog jina-reranker-v2).
DEFAULT_MULTIMODAL_MODEL = os.environ.get(
    "KH_MULTIMODAL_MODEL",
    "google/siglip2-so400m-patch16-512",
)
DEFAULT_MULTIMODAL_DEVICE = os.environ.get("KH_MULTIMODAL_DEVICE", "cpu")
DEFAULT_MULTIMODAL_BATCH_SIZE = int(os.environ.get("KH_MULTIMODAL_BATCH_SIZE", "32"))

# Vision LLM for image captioning (Gemma 4 via Ollama Cloud, analog
# Contextual Retrieval). Default uses the same KH_LLM_MODEL env var so the
# captioning pipeline can share the Ollama-Cloud routing. KH_VISION_LLM_WORKERS
# mirrors KH_LLM_WORKERS for parallel cloud calls.
DEFAULT_VISION_LLM_MODEL = os.environ.get("KH_VISION_LLM_MODEL", DEFAULT_LLM_MODEL)
DEFAULT_VISION_LLM_WORKERS = int(os.environ.get("KH_VISION_LLM_WORKERS", "1"))


def domain_images_dir(domain: str) -> Path:
    """Directory holding extracted PNGs for a domain.

    Layout: domains/<domain>/images/<source-file>/<page>-<idx>.png.
    Created on demand.
    """
    return DOMAINS_DIR / domain / "images"


def domain_image_bm25_path(domain: str) -> Path:
    """BM25 pickle file path for a domain's image-caption index."""
    return CHROMA_DIR / domain / f"{domain}_images_bm25.pkl"


def domain_image_manifest_path(domain: str) -> Path:
    """JSON manifest of extracted images for a domain.

    Layout: chromadb_data/<domain>/image_manifest.json (gitignored).
    """
    return CHROMA_DIR / domain / "image_manifest.json"
