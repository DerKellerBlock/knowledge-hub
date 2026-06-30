"""Shared pytest configuration for Knowledge Hub tests.

Auto-applies the layer markers (unit/integration/e2e/mcp) based on the test
file's directory, so individual test files do not need to repeat
``@pytest.mark.<layer>`` on every test. This keeps the marker-based layer
selection (``-m unit`` etc.) working with the plan's test files.

Task 6 of the test-suite plan extends this file with the ``tmp_hub``,
``dummy_domain`` and ``indexed_dummy`` fixtures.
"""

import pytest


def pytest_collection_modifyitems(items):
    """Auto-mark tests by directory so ``-m <layer>`` works without per-test
    decorators."""
    for item in items:
        # item.fspath is the path to the test file
        parts = item.fspath.strpath.split("/tests/")
        if len(parts) != 2:
            continue
        layer = parts[1].split("/")[0]  # unit | integration | e2e | mcp
        marker = getattr(pytest.mark, layer, None)
        if marker is not None:
            item.add_marker(marker)


# ── Integration / E2E fixtures (Task 6) ────────────────────────────────────

import os
import sys
from pathlib import Path

HUB_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def tmp_hub(tmp_path, monkeypatch):
    """Create a temporary HUB_ROOT-like directory structure and monkeypatch
    all module-level path constants.

    This allows integration tests to build a tiny ChromaDB index in an
    isolated tmp directory without touching the real chromadb_data/.
    """
    # Create directory structure
    (tmp_path / "domains").mkdir()
    (tmp_path / "chromadb_data").mkdir()
    (tmp_path / "scripts").mkdir()

    # Monkeypatch config paths
    from mcp_servers.knowledge_hub import config as cfg
    monkeypatch.setattr(cfg, "HUB_ROOT", tmp_path)
    monkeypatch.setattr(cfg, "DOMAINS_DIR", tmp_path / "domains")
    monkeypatch.setattr(cfg, "CHROMA_DIR", tmp_path / "chromadb_data")
    monkeypatch.setattr(cfg, "SCRIPTS_DIR", tmp_path / "scripts")

    # Monkeypatch model_manager paths (it imports from config at module load)
    import model_manager as mm
    monkeypatch.setattr(mm, "_chroma_clients", {})
    monkeypatch.setattr(mm, "_bm25_cache", __import__("collections").OrderedDict())

    # Monkeypatch bm25_search path function (it calls domain_bm25_path from config)
    # config.domain_bm25_path reads CHROMA_DIR, which we already patched
    # but bm25_search imported domain_bm25_path at module load — it reads
    # config.CHROMA_DIR dynamically via the function, so it's fine.

    # Clear the chroma clients cache so each test gets a fresh client
    yield tmp_path

    # Cleanup: close any chroma clients
    mm._chroma_clients.clear()
    mm._bm25_cache.clear()


@pytest.fixture
def dummy_domain(tmp_hub):
    """Create a minimal dummy domain with 3 small source files and 1 personal note.

    Returns the domain name ("dummy").
    """
    domain_dir = tmp_hub / "domains" / "dummy"
    sources_dir = domain_dir / "sources"
    personal_dir = domain_dir / "personal"
    sources_dir.mkdir(parents=True)
    personal_dir.mkdir(parents=True)

    # Write domain.md with Metadaten block
    (domain_dir / "domain.md").write_text("""# Domain: dummy

## Zweck
Test domain for integration tests.

## Metadaten
- Embedding-Model: all-mpnet-base-v2 (768 dims)
- Collection: dummy_knowledge
- ChromaDB-Path: chromadb_data/dummy/chroma/
- BM25-Path: chromadb_data/dummy/dummy_bm25.pkl
- Letztes Update: 2026-06-28

## Lizenz-Hinweis
Test data only.
""", encoding="utf-8")

    # Write 3 source files with distinct topics
    (sources_dir / "node3d-rotation.md").write_text("""# Node3D Rotation

The Node3D class in Godot provides methods to rotate 3D nodes.

## rotate_y(angle)
Rotates the node around the Y axis by the given angle in radians.

```gdscript
var node = get_node("Player")
node.rotate_y(deg_to_rad(90))
```

## rotate_x(angle)
Rotates the node around the X axis.

## set_rotation(rotation: Vector3)
Sets the rotation of the node to the given Vector3.
""", encoding="utf-8")

    (sources_dir / "camera-follow.md").write_text("""# Camera Follow

The Camera3D can follow a target node.

## make_current()
Marks this camera as the current active camera.

## follow_target(target: NodePath)
Makes the camera follow the specified target node, maintaining distance.
""", encoding="utf-8")

    (sources_dir / "audio-bus.md").write_text("""# Audio Bus

Audio buses in Godot route audio through effects.

## set_bus_volume(bus: int, volume: float)
Sets the volume of the specified audio bus.

## add_effect(effect: AudioEffect)
Adds an audio effect to the bus.
""", encoding="utf-8")

    # Write 1 personal note
    (personal_dir / "gotchas.md").write_text("""# Dummy Gotchas

## Node3D rotation gotcha
- **Datum:** 2026-06-28
- **Notiz:** rotate_y uses radians, not degrees. Use deg_to_rad() to convert.

## Camera follow gotcha
- **Datum:** 2026-06-28
- **Notiz:** Call make_current() after follow_target() or the camera won't activate.
""", encoding="utf-8")

    return "dummy"


@pytest.fixture
def indexed_dummy(dummy_domain):
    """Build the ChromaDB + BM25 index for the dummy domain.

    Requires sentence-transformers to be installed and the model to download
    on first run. Skips if not available.
    """
    pytest.importorskip("chromadb")
    pytest.importorskip("sentence_transformers")

    # Import after tmp_hub has patched paths
    import model_manager as mm
    from mcp_servers.knowledge_hub import config as cfg

    # get_domain_config reads domain.md from DOMAINS_DIR (patched)
    # get_embedder loads the model (not patched — real model)
    # get_chroma_client uses domain_chroma_path → patched CHROMA_DIR

    # We need to build the index using the real embed_index logic
    # but with patched paths. The easiest way is to call the functions directly.
    from parser_base import fallback_chunk, markdown_section_chunk, Chunk
    from bm25_search import build_bm25_index
    from model_manager import get_embedder, get_chroma_client

    domain = "dummy"
    domain_dir = cfg.DOMAINS_DIR / domain
    chunks = []

    # Parse sources (repo fallback chunking — unchanged)
    sources_dir = domain_dir / "sources"
    if sources_dir.is_dir():
        for f in sorted(sources_dir.glob("*.md")):
            content = f.read_text(encoding="utf-8")
            fallback = fallback_chunk(content, domain=domain, source_type="repo", source_file=f.name)
            for i, c in enumerate(fallback):
                c.chunk_id = f"{domain}::fallback::repo::{f.stem}::{i}"
                c.chunk_id_in_file = i
            chunks.extend(fallback)

    # Parse personal (markdown section chunking — mirrors embed_index.py)
    personal_dir = domain_dir / "personal"
    if personal_dir.is_dir():
        for f in sorted(personal_dir.glob("*.md")):
            content = f.read_text(encoding="utf-8")
            category = f.stem
            chunks.extend(
                markdown_section_chunk(
                    content,
                    domain=domain,
                    source_type="personal",
                    source_file=f.name,
                    category=category,
                )
            )

    assert len(chunks) > 0, "No chunks were created from dummy domain"

    # Embed and index
    model = get_embedder(domain)
    texts = [c.text for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=False)

    client = get_chroma_client(domain)
    collection_name = f"{domain}_knowledge"

    try:
        client.delete_collection(collection_name)
    except Exception:
        pass

    collection = client.create_collection(
        name=collection_name,
        metadata={"domain": domain, "hnsw:space": "cosine"},
    )

    batch_size = 500
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        collection.add(
            ids=[c.chunk_id for c in batch],
            embeddings=embeddings[i:i + batch_size].tolist(),
            documents=[c.text for c in batch],
            metadatas=[c.to_chromadb_metadata() for c in batch],
        )

    build_bm25_index(domain, chunks)

    return domain