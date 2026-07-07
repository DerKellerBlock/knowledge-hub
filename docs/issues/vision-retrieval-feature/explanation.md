# Explanation — Vision Retrieval Feature

**Task:** Vision-Retrieval-Feature (Multimodal-RAG)
**Datum:** 2026-07-07
**Für:** Anfängerfreundliche Erklärung der geänderten Dateien, OpenCode-Konfiguration, Agenten, Validierung

## Was wurde gebaut

Das Vision Retrieval Feature ist eine **additive Multimodal-RAG-Pipeline** für PDF-Domains mit Screenshots. Sie erweitert die bestehende Text-Suche um Bild-Suche, ohne den Text-Pfad zu verändern.

### Kernidee
DaVinci-Handbücher enthalten viele UI-Screenshots. Bisher war die Suche nur auf Text-Chunks (BGE-M3 + BM25). Jetzt gibt es einen zusätzlichen Bild-Pfad: extrahiere PNGs aus PDFs, generiere Captions mit Gemma 4, embedde Bilder+Captions mit SigLIP-2, und fusioniere Text- und Bild-Treffer über 4-Listen-RRF.

## Geänderte Dateien

### Neue Skripte (scripts/)
| Skript | Lizenz | Zweck |
|--------|--------|-------|
| `extract_pdf_images.py` | AGPL (PyMuPDF) | PDF → PNG + `image_manifest.json` |
| `caption_images.py` | MIT | Bild → Caption (Gemma 4 Cloud, 3 Worker) |
| `image_caption_cache.py` | MIT | SQLite-Cache für Captions (WAL, content-hash) |
| `embed_images.py` | MIT | Bild/Caption → ChromaDB `<domain>_images` |
| `image_embedding_cache.py` | MIT | SQLite-Cache für Embeddings (base64 float32) |

### Erweiterte Skripte
- `model_manager.py` — `get_multimodal_embedder()` + `is_multimodal_embedder_available()`
- `bm25_search.py` — `build_image_bm25_index()`, `image_bm25_search()`, `get_image_bm25_index_size_mb()`
- `hybrid_search.py` — 4-Listen-RRF, `_image_semantic_search()`, `_resolve_image_metadata()`, Mixed-Modality Merge
- `embed_index.py` — `--embed-images` Flag (baut Bild-BM25)

### Erweiterte MCP-Server-Dateien
- `mcp_servers/knowledge_hub/config.py` — Neue Env-Vars + `domain_images_dir()`, `domain_image_bm25_path()`, `domain_image_manifest_path()`
- `mcp_servers/knowledge_hub/tools.py` — `get_domain_status` mit `image_count`, `image_index_exists`, `image_bm25_index_size_mb`
- `mcp_servers/knowledge_hub/server.py` — `search_knowledge` Beschreibung aktualisiert

### Erweiterte Doku
- `docs/ai/architecture.md` — Vision Retrieval Feature Sektion mit Pipeline-Diagramm
- `docs/ai/best-practices.md` — Neue Env-Vars, CLI-Skripte, Pre-Flight, Context-Aware Captions
- `docs/ai/security.md` — SigLIP-2/jina-clip-v2 Lizenzen, Datenexfiltration, AGPL Process Boundary
- `docs/ai/known-issues.md` — VRF-001 bis VRF-005

### Erweiterte Konfiguration
- `requirements.txt` — `pillow`, `torch>=2.12.0`, `transformers>=4.57.0`
- `THIRD_PARTY_LICENSES.md` — SigLIP-2 (Apache 2.0), jina-clip-v2 (CC-BY-NC-4.0), pillow/torch/transformers
- `domains/davinci_resolve/domain.md` — Multimodal-Model, Vision-LLM, Image-Collection Metadaten

## OpenCode-Konfiguration

Die `.opencode/opencode.json` wurde NICHT geändert — das Vision Retrieval Feature nutzt die bestehende MCP-Server-Infrastruktur. Der `search_knowledge` MCP-Tool-Aufruf bleibt identisch; die `modality`/`image_path`/`caption` Felder sind zusätzliche Felder in den Ergebnissen (backward-kompatibel).

### Neue Env-Vars (für den Build-Prozess)
```bash
# Captioning (Gemma 4 Cloud, 3 parallele Worker)
export KH_LLM_MODEL=gemma4:cloud
export KH_OLLAMA_HOST=http://localhost:11434
export KH_VISION_LLM_WORKERS=3

# Multimodal Embedding (SigLIP-2, MPS GPU)
export KH_MULTIMODAL_MODEL=google/siglip2-so400m-patch16-512
export KH_MULTIMODAL_DEVICE=mps
export KH_MULTIMODAL_BATCH_SIZE=32
```

## Agenten

Die Implementierung wurde vom `implement-hub-change` Agenten durchgeführt (kein Subagent-Spawning). Die Validierung erfolgt durch:
- `validate-hub-project` — Syntax, Struktur, Index-Status
- `test-hub-feature` — pytest + Knowledge-QA
- `review-hub-diff` — Diff-Review auf Fehler/Regressionen
- `review-hub-security` — Security-Review (MCP, Secrets, Dependencies)

## Validierungsbefehle

### Syntax
```bash
.venv/bin/python -m py_compile scripts/*.py mcp_servers/knowledge_hub/*.py
```

### Unit-Tests
```bash
.venv/bin/pytest -m unit -q
# 226 passed, 227 deselected
```

### Workspace
```bash
./scripts/workspace_check.sh
# All workspace checks passed
```

### End-to-End Build (pro PDF)
```bash
# 1. Extrahieren
python scripts/extract_pdf_images.py --domain davinci_resolve

# 2. Captioning (Cloud, parallel)
KH_LLM_MODEL=gemma4:cloud KH_VISION_LLM_WORKERS=3 \
    python scripts/caption_images.py --domain davinci_resolve --workers 3

# 3. Embedding (MPS GPU)
KH_MULTIMODAL_DEVICE=mps KH_MULTIMODAL_BATCH_SIZE=32 \
    python scripts/embed_images.py --domain davinci_resolve

# 4. Bild-BM25 (additiv zu Text-Index)
python scripts/embed_index.py --domain davinci_resolve --embed-images
```

### Search-Test
```bash
KH_LLM_MODEL=gemma4:cloud KH_MULTIMODAL_MODEL=google/siglip2-so400m-patch16-512 \
KH_MULTIMODAL_DEVICE=mps python scripts/hybrid_search.py \
    --domain davinci_resolve --query "Fairlight mixing console" --top 5
```

## Knowledge-QA Ablauf

Für Quellen-/Domain-Änderungen prüft `test-hub-feature`:
1. Realistische Nutzerfragen aus geänderten Quellen
2. Real-World Problem Prompts (via websearch)
3. Top-Search-Results mit `source_file`
4. PDF `page_start`/`page_end` wenn verfügbar
5. Evidence Snippets
6. Schwache/fehlende Coverage als Findings dokumentiert

Für das Vision Retrieval Feature bedeutet das: Bild-zentrierte Queries sollten Bild-Treffer mit `image_path` und `caption` in den Top-Ergebnissen zeigen.

## Architektur-Entscheidungen

1. **SigLIP-2 als Default** (Apache 2.0) — kommerziell sicher, English-only. jina-clip-v2 (CC-BY-NC-4.0) als multilinguale Option.
2. **Ollama NICHT für Multimodal** — Ollama hat keine Multimodal-Embedding-API (Issue #5304). SigLIP-2 läuft via `transformers`.
3. **4-Listen-RRF mit Modality-Gap** — `k_image=30` (kleiner als `k_text=60`) gewichtet Bilder stärker. Cross-Encoder nur auf Text.
4. **Mixed-Modality Merge** — 1/3 der Top-K-Slots für Bilder reserviert (min 1). Kompromiss zwischen Text- und Bild-Dominanz.
5. **Content-Hash Caching** — SQLite-Caches mit SHA-256 Keys machen Builds crash-resilient und domain-unabhängig.
6. **AGPL Process Boundary** — `extract_pdf_images.py` importiert PyMuPDF (AGPL), Runtime bleibt MIT (analog `parse_pdf_to_markdown.py`).
