"""Configuration for Knowledge Hub MCP Server."""

from pathlib import Path

# Repository root (knowledge-hub/)
HUB_ROOT = Path(__file__).resolve().parent.parent.parent
DOMAINS_DIR = HUB_ROOT / "domains"
SCRIPTS_DIR = HUB_ROOT / "scripts"
CHROMA_DIR = HUB_ROOT / "chromadb_data"
PERSONAL_DIR = HUB_ROOT / "personal"

MODEL_NAME = "all-mpnet-base-v2"
