"""Configuration for Knowledge Hub MCP Server."""

from pathlib import Path

# Repository root (knowledge-hub/)
HUB_ROOT = Path(__file__).resolve().parent.parent.parent
DOMAINS_DIR = HUB_ROOT / "domains"
SCRIPTS_DIR = HUB_ROOT / "scripts"
CHROMA_DIR = HUB_ROOT / "chromadb_data"
PERSONAL_DIR = HUB_ROOT / "personal"

# Cross-encoder model (Stage 2 reranking)
CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L-12-v2"

# Default embedding model (can be overridden per-domain in domain.md)
DEFAULT_MODEL_NAME = "all-mpnet-base-v2"

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
