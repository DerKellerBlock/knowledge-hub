# Explanation — Vision Retrieval Feature + Quality Metrics v2

**Datum:** 2026-07-07
**Status:** Abgeschlossen
**Commits:** 7 (3fc9cd1 → 1ce7838)

## Was gebaut wurde

### 1. Vision Retrieval Feature (Multimodal-RAG)

Additive Bild-Suche für PDF-Domains mit Screenshots. Bestehende Text-Suche bleibt unverändert; Bild-Pipeline ist ein zusätzliches Retrieval-Signal.

**Pipeline:**
```
PDFs → extract_pdf_images.py (PyMuPDF4LLM, AGPL)
     → caption_images.py (Gemma 4 Cloud, 3 Worker)
     → embed_images.py (SigLIP-2, MPS GPU)
     → ChromaDB <domain>_images + <domain>_images_bm25.pkl
     → hybrid_search.py 4-Listen-RRF (text+image, Modality-Gap)
```

**Full DaVinci Build:**
- 10 PDFs → 19.183 Bilder extrahiert (12 min)
- 7.592 als poor markiert (<20KB, Logos/Icons)
- 11.591 Bilder captioned (3h 28m, 0.9 img/s, 3 Worker)
- 23.182 ChromaDB entries embedded (1h 9m, 2.8 img/s, MPS)
- 5.32 MB Bild-BM25

### 2. Caption Cleaning

PDF-Header/Footer-Rausch aus Captions gestrippt (dauerhaft in `caption_images.py` integriert):
- `--- end of page=N ---`, DaVinci Section Header, `**N**` Seitenzahlen, Unicode-Balken, Markdown-Header
- BM25 "Color Wheels": Cover-Bild → echte Color Wheels Screenshots

### 3. Quality Metrics v2 (Diskriminative Metriken)

40% des Eval-Composite-Scores waren Konstanten (TKR=0.55, EQ=1.0). Ersetzt durch:

| Alt (konstant) | Neu (diskriminativ) | Range |
|----------------|---------------------|-------|
| TKR = 0.55 | NDCG@10 (4-stufige Relevanz) | 0.67–0.99 |
| PMA ±2 (binär) | Jaccard Page Overlap (kontinuierlich) | 0.03–1.0 |
| SR (binär) | Weighted Source Recall (mit Gewichten) | 0.5–1.0 |
| — | Source Diversity (Shannon-Entropie, neu) | 0.47–0.99 |

### 4. HyDE (Hypothetical Document Embeddings)

LLM generiert hypothetisches Dokument mit technischer Terminologie → besseres semantisches Embedding. Optional via `KH_HYDE_ENABLED=1`.

## Neue Dateien

| Datei | Lizenz | Zweck |
|------|--------|-------|
| `scripts/extract_pdf_images.py` | AGPL | PDF → PNG + Manifest |
| `scripts/caption_images.py` | MIT | Bild → Caption (Cloud, parallel) |
| `scripts/caption_cleaning.py` | MIT | Caption-Rausch-Stripping |
| `scripts/image_caption_cache.py` | MIT | SQLite-Cache für Captions |
| `scripts/embed_images.py` | MIT | Bild/Caption → ChromaDB |
| `scripts/image_embedding_cache.py` | MIT | SQLite-Cache für Embeddings |
| `scripts/hyde.py` | MIT | HyDE Query-Verbesserung |
| `docs/issues/vision-retrieval-feature/spec.md` | — | SDD Spec |
| `docs/issues/vision-retrieval-feature/plan.md` | — | SDD Plan |
| `docs/issues/vision-retrieval-feature/retrospective.md` | — | Retrospektive |
| `docs/issues/vision-retrieval-feature/explanation.md` | — | Diese Datei |
| `docs/issues/quality-metrics-v2/spec.md` | — | SDD Spec Metrics v2 |
| `docs/issues/quality-metrics-v2/plan.md` | — | SDD Plan Metrics v2 |
| `docs/issues/quality-metrics-v2/retrospective.md` | — | Retrospektive Metrics v2 |

## Geänderte Dateien

| Datei | Änderung |
|------|----------|
| `scripts/model_manager.py` | `get_multimodal_embedder()` hinzugefügt |
| `scripts/bm25_search.py` | `build_image_bm25_index()`, `image_bm25_search()` |
| `scripts/hybrid_search.py` | 4-Listen-RRF, Interleave-Merge, HyDE-Integration |
| `scripts/embed_index.py` | `--embed-images` Flag |
| `scripts/quality/scorer.py` | NDCG, Jaccard, WSR, Diversity + Report-Update |
| `scripts/quality/config.py` | Neue Weights (70% diskriminativ) |
| `mcp_servers/knowledge_hub/config.py` | 5 neue Env-Vars + Helper |
| `mcp_servers/knowledge_hub/tools.py` | `get_domain_status` mit image_count |
| `mcp_servers/knowledge_hub/server.py` | `search_knowledge` Beschreibung |
| `requirements.txt` | pillow, torch, transformers |
| `THIRD_PARTY_LICENSES.md` | SigLIP-2, jina-clip-v2, pillow/torch |
| `domains/davinci_resolve/domain.md` | 8 neue Metadaten-Felder |
| `quality/golden/davinci_resolve.yaml` | +6 Bild-Fragen, weights, page ranges |
| `.gitignore` | `domains/*/images/` hinzugefügt |
| `docs/ai/architecture.md` | Vision Retrieval Sektion |
| `docs/ai/best-practices.md` | Neue Env-Vars + CLI |
| `docs/ai/security.md` | Multimodal + AGPL Boundary |
| `docs/ai/known-issues.md` | VRF-001 bis VRF-006 |
| `docs/ai/open-work.md` | 2 Tasks als done markiert |

## Neue Env-Vars

| Var | Default | Zweck |
|-----|---------|-------|
| `KH_MULTIMODAL_MODEL` | `google/siglip2-so400m-patch16-512` | Multimodal-Embedding-Modell |
| `KH_MULTIMODAL_DEVICE` | `cpu` | Compute-Device (opt-in `mps`) |
| `KH_MULTIMODAL_BATCH_SIZE` | `32` | Batch-Size |
| `KH_VISION_LLM_MODEL` | folgt `KH_LLM_MODEL` | Vision-LLM für Captioning |
| `KH_VISION_LLM_WORKERS` | `1` | Parallele Worker (opt-in `3`) |
| `KH_HYDE_ENABLED` | `0` | HyDE aktivieren (opt-in `1`) |

## CLI-Skripte

```bash
# Vision Retrieval Build
python scripts/extract_pdf_images.py --domain davinci_resolve
KH_LLM_MODEL=gemma4:cloud KH_VISION_LLM_WORKERS=3 \
    python scripts/caption_images.py --domain davinci_resolve --workers 3
KH_MULTIMODAL_DEVICE=mps python scripts/embed_images.py --domain davinci_resolve
python scripts/embed_index.py --domain davinci_resolve --embed-images

# Eval mit neuen Metriken
python scripts/quality/run_evaluation.py --domain davinci_resolve
python scripts/quality/generate_report.py --input results.json

# HyDE (optional)
KH_HYDE_ENABLED=1 python scripts/hybrid_search.py --domain davinci_resolve --query "..."
```

## Eval-Ergebnis

| Version | Avg Composite | Pass | Weak | Fail |
|---------|--------------|------|------|------|
| Pre-Session (konstante Metriken) | 0.7234 | 15 (58%) | 11 (42%) | 0 |
| +v2 Metriken | 0.7928 | 20 (77%) | 6 (23%) | 0 |
| **+Page Ranges +HyDE (FINAL)** | **0.8017** | **21 (81%)** | **5 (19%)** | **0** |

**Godot (backward-compat):** 0.9153 avg, 19 pass, 2 weak, 0 fail (unverändert)

## Validierung

```bash
.venv/bin/python -m py_compile scripts/*.py mcp_servers/knowledge_hub/*.py  # OK
.venv/bin/pytest -m unit -q                                                 # 226 passed
./scripts/workspace_check.sh                                               # All checks passed
.venv/bin/python scripts/quality/validate_dataset.py --domain davinci_resolve  # OK
.venv/bin/python scripts/quality/validate_dataset.py --domain godot            # OK
```
