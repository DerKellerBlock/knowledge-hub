"""Configuration for Knowledge Hub MCP Server."""

from pathlib import Path

# Repository root (knowledge-hub/)
HUB_ROOT = Path(__file__).resolve().parent.parent.parent
DOMAINS_DIR = HUB_ROOT / "domains"
SCRIPTS_DIR = HUB_ROOT / "scripts"
CHROMA_DIR = HUB_ROOT / "chromadb_data"
PERSONAL_DIR = HUB_ROOT / "personal"

# BM25 index path pattern (built by embed_index.py)
BM25_INDEX_PATTERN = "{domain}_bm25.pkl"  # relative to CHROMA_DIR

# Cross-encoder model (Stage 2 reranking)
CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L-12-v2"

MODEL_NAME = "all-mpnet-base-v2"
