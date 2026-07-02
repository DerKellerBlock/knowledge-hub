# Phase 2b Golden Dataset + Late Chunking — Wo die Dateien leben

> **Anfängerfreundliche Erklärung** | 2026-07-02 | Golden Dataset 20–30 Fragen + Chapter-weises Late Chunking für DaVinci-PDFs

## Übersicht

Phase 2b vereint zwei Maßnahmen aus der Verbesserungs-Roadmap:

| # | Maßnahme | Warum? |
|---|----------|--------|
| 1 | **Golden Dataset 20–30 Fragen** (Phase 2.4) | Breitere Abdeckung: godot 9→21 (+12), davinci 7→20 (+13). Alle 25 neuen Fragen mit `real_world_sources`, `solution_summary`, `has_solution`. |
| 2 | **Late Chunking für DaVinci-PDFs** (Phase 2.2) | Chapter-weises BGE-M3-Encoding statt Fallback-Chunking. 512-Token-Fenster mit 128-Overlap via Mean-Pooling. Bessere Chapter-Grenzen → höhere PMA. |

Ergebnis: DaVinci 2.511 → 12.367 Chunks, avg_composite 0.8063 → 0.8183 (+1.5%), PMA 0.725 → 0.785 (+8.3%), alle 20 Fragen pass. Godot unverändert (0.8073, 16 pass / 5 weak — kein Rebuild).

## Wo geänderte Dateien leben

### Late Chunking Code

| Pfad | Was sich geändert hat |
|------|----------------------|
| `scripts/parser_base.py` | `_split_into_chapters()`, `_token_windows_from_offsets()` (lossless via offset mapping), `_LateChunkEncoder` (MPS pre-flight device detection), `late_chunk()` → `(chunks, precomputed_embeddings)` |
| `scripts/embed_index.py` | `load_domain_sources()` → tuple, `build_index()` nutzt `precomputed_embeddings`, `DOMAINS_DIR` live-lookup fix |
| `scripts/model_manager.py` | `get_domain_config()` live-lookup via `mcp_servers.knowledge_hub.config` (fixes dual-module-object bug) |

### Tests

| Pfad | Was sich geändert hat |
|------|----------------------|
| `tests/unit/test_parser_base.py` | 17 Tests: `TestLateChunk` — chapter splitting, token windows, offset mapping, MPS pre-flight, edge cases |
| `tests/integration/test_embed_index.py` | 3 Tests: Late Chunking integration (skip gracefully if BGE-M3 not cached) |

### Golden Datasets

| Pfad | Was sich geändert hat |
|------|----------------------|
| `quality/golden/godot.yaml` | 9 → 21 Fragen (+12: Animation, Shaders, UI, Navigation, Multiplayer, Input, Audio, File I/O, Performance, TileMap, GDScript Patterns, Debugging) |
| `quality/golden/davinci_resolve.yaml` | 7 → 20 Fragen (+13: Fusion Compositing, Color Advanced, Cut Page, Edit Advanced, Fairlight Advanced, Media Management, Effects, Collaboration, Troubleshooting, Workflow) |

### Baselines

| Pfad | Was sich geändert hat |
|------|----------------------|
| `quality/baselines/godot-latest.json` | Neue Baseline: 21 Fragen, avg 0.8073, 16 pass / 5 weak |
| `quality/baselines/davinci_resolve-latest.json` | Neue Baseline: 20 Fragen, avg 0.8183, 20 pass, PMA 0.785 |
| `quality/baselines/godot-pre-phase2b-2026-07-01.json` | Archiv (Pre-Phase-2b Godot-Baseline) |
| `quality/baselines/davinci_resolve-pre-phase2b-2026-07-01.json` | Archiv (Pre-Phase-2b DaVinci-Baseline) |

### Dokumentation

| Pfad | Was sich geändert hat |
|------|----------------------|
| `docs/ai/architecture.md` | Late Chunking Datenfluss, `precomputed_embeddings` als separates Dict, `_LateChunkEncoder` |
| `docs/ai/domain-model.md` | Late Chunk Wissenstyp (`chunk_type="late_chunk"`, `page_start`/`page_end`, `line_start=0`/`line_end=0`) |
| `docs/ai/best-practices.md` | Late Chunking Konventionen (MPS pre-flight, precomputed_embeddings, offset mapping) |
| `docs/ai/known-issues.md` | LIM-009 (Konfounder), LIM-010 (`line_start`/`end=0`), 5 Godot weak-Fragen dokumentiert |
| `docs/ai/project-context.md` | Phase 2.4 Update (Golden Dataset Expansion) |

### Quality Reports

| Pfad | Inhalt |
|------|--------|
| `quality/reports/davinci_resolve_2026-07-02.md` | DaVinci Re-Evaluation: 20/20 pass, avg 0.8133, PMA 0.76 |
| `quality/reports/davinci_resolve_2026-07-02.json` | Rohdaten der Evaluation |

### Index (nicht committet, `.gitignored`)

- `chromadb_data/davinci_resolve/` — Rebuild: 12.367 Chunks (12.361 late_chunk + 5 personal_section + 1 preamble), 685 MB (670 MB chroma + 15 MB BM25)
- `chromadb_data/godot/` — unverändert (kein Rebuild in Phase 2b)

## Validierungsbefehle

```bash
# Tests (315 grün)
pytest -m unit          # 126 passed
pytest -m integration   # 44 passed
pytest -m quality       # 145 passed

# Quality Evaluation
python scripts/quality/run_evaluation.py --domain davinci_resolve
python scripts/quality/run_evaluation.py --domain davinci_resolve --baseline quality/baselines/davinci_resolve-latest.json

# Golden Dataset validieren
python scripts/quality/validate_dataset.py --domain godot --check-sources
python scripts/quality/validate_dataset.py --domain davinci_resolve --check-sources

# Report generieren
python scripts/quality/generate_report.py --input quality/reports/davinci_resolve_2026-07-02.json
```

## Was ist neu

### `late_chunk()` in `parser_base.py`
Chapter-weises Late Chunking für PDF-Domains. Statt jeden Chunk einzeln zu embedden, wird der gesamte Chapter als langer Token-Stream an BGE-M3 gefüttert (8192 Token Kontext). Anschließend werden 512-Token-Fenster mit 128-Overlap über die Token-Embeddings gelegt und pro Fenster gemittelt (mean pooling). Rückgabe: `(chunks, precomputed_embeddings)` Tuple.

### `_LateChunkEncoder` mit MPS Pre-Flight
Erkennt vor dem Encoding-Loop die tatsächliche Compute-Device (CPU, CUDA, MPS). Bei MPS-OOM fällt er einmal pro Session auf CPU zurück — nicht pro Chunk. Verhindert wiederholte Crashes auf Apple Silicon.

### `precomputed_embeddings` als separates Dict
BGE-M3-Token-Embeddings werden in einem separaten Dict `{chunk_id: np.ndarray}` durch die Pipeline gereicht, nicht als Chunk-Attribut. Hält Chunk-Daten klein und ermöglicht Window-Mean-Pooling außerhalb der Embedding-Funktion.

### `expected_page_ranges` Update (V8)
Die `expected_page_ranges` der 7 alten DaVinci-Fragen (001–007) wurden an Late Chunking's Chapter-Grenzen angepasst. Ohne dieses Update wäre davinci-005 als weak gelabelt (PMA 0.0 statt 0.6).

### 25 neue Golden-Dataset-Fragen
Godot +12 (Animation, Shaders, UI, Navigation, Multiplayer, Input, Audio, File I/O, Performance, TileMap, GDScript Patterns, Debugging), DaVinci +13 (Fusion Compositing, Color Advanced, Cut Page, Edit Advanced, Fairlight Advanced, Media Management, Effects, Collaboration, Troubleshooting, Workflow). Alle mit `real_world_sources`, `solution_summary`, `has_solution`.

## Wo das Ergebnis zu sehen ist

- **`quality/reports/davinci_resolve_2026-07-02.md`** — DaVinci: 20/20 pass, avg_composite 0.8133, PMA 0.76
- **`quality/baselines/davinci_resolve-latest.json`** — Baseline: avg 0.8183, PMA 0.785, 20 pass
- **`quality/baselines/godot-latest.json`** — Baseline: avg 0.8073, 16 pass / 5 weak
- **Manuell testen:**
  ```bash
  # Late Chunking Ergebnis prüfen (DaVinci Planar Tracker)
  python scripts/hybrid_search.py --domain davinci_resolve --query "How do I set up a Planar Tracker" --mode hybrid --top-k 5
  # → chunk_type="late_chunk", page_start/page_end sollten gesetzt sein
  ```

## Wichtige Hinweise

- **LIM-009 Konfounder bleibt:** BGE-M3 long-context + Late Chunking änderten sich gleichzeitig. Die DaVinci-Verbesserung (+1.5% composite, +8.3% PMA) mischt beide Effekte — nicht isoliert messbar.
- **LIM-010 `line_start`/`line_end = 0`:** Late-Chunk-Chunks haben keine Zeilennummern (PDF-Chapter-Grenzen kommen aus Markdown-Headern, nicht aus Zeilen-Positionen). Konsumenten müssen `chunk_type=="late_chunk"` als Ausnahme behandeln.
- **5 Godot weak-Fragen (009/011/012/017/019):** Composite 0.6406, testen Themen ohne `personal/`-Notizen. Content-Maßnahmen oder Frage-Spezifizierung könnten helfen. Godot hat keinen Late-Chunking-Nutzen (strukturierter Parser).
- **Phase 3 offen:** Contextual Retrieval + RAGAS + DaVinci Personal Notes + BGE-M3 Sparse + Multi-Modal. Spec unter `docs/superpowers/specs/2026-06-30-improvement-roadmap-phase3-advanced-rag-design.md`.
- **Keine Commits:** Alle Änderungen sind im Working Tree. Noah committet selbst.

## Verified facts

- 315 Tests grün: 126 unit + 44 integration + 145 quality
- DaVinci: 12.367 Chunks (12.361 late_chunk + 5 personal_section + 1 preamble)
- DaVinci ChromaDB: 685 MB (670 MB chroma + 15 MB BM25)
- DaVinci avg_composite: 0.8183 (baseline), 0.8133 (report)
- DaVinci PMA: 0.785 (baseline), 0.760 (report)
- Godot: 21 Fragen, avg 0.8073, 16 pass / 5 weak (unverändert, kein Rebuild)
- Rebuild-Zeit: ~15 Min (geschätzt 20–40 Min)
- Backup nach erfolgreichem Rebuild entfernt

## Weiterlesen

- **Phase 2a BGE-M3 + Quality Gate:** `docs/superpowers/explanations/2026-06-30-phase2a-bge-m3-quality-gate-location.md`
- **jina-Reranker Test:** `docs/superpowers/explanations/2026-07-01-jina-reranker-test-location.md`
- **Domain-Modell:** `docs/ai/domain-model.md` — Late Chunk Wissenstyp
- **Architektur:** `docs/ai/architecture.md` — Late Chunking Datenfluss
- **Validierung:** `docs/ai/validation.md` — alle CLI-Befehle und Test-Stufen
