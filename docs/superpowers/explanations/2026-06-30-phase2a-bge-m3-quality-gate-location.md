# Phase 2a BGE-M3 + Quality Gate — Wo die Dateien leben

> **Anfängerfreundliche Erklärung** | 2026-06-30 | Embedding-Modell-Wechsel + CI Quality Regression Gate

## Was wurde geändert — und warum?

Phase 2a der Verbesserungs-Roadmap implementiert den **Wechsel des Embedding-Modells** von `all-mpnet-base-v2` (English-only, 768d) zu `BAAI/bge-m3` (multilingual, 1024d, 8192 Token Kontext) und ein **CI Quality Regression Gate** mit manuellen Baselines.

| # | Maßnahme | Warum? |
|---|----------|--------|
| 1 | **BGE-M3 Embedding-Modell** | Schließt die DE↔EN-Sprachbarriere systematisch — godot-008 (englische Query gegen deutsche faq.md) von weak → pass |
| 2 | **KH_EMBEDDING_MODEL Env-Var** | Modellwechsel ohne Code-Änderung (analog KH_RERANKER_MODEL aus Phase 1) |
| 3 | **_encode_robust()** | Löst MPS/SDPA-OOM-Bug auf Apple Silicon bei langen Chunks (DaVinci ~8000 chars) |
| 4 | **Spec-compliant Regression Thresholds** | `check_regression()` + `check_regression_exit.py` für CI exit-code |
| 5 | **CI Quality Gate** | Weekly Regression-Check (Montag 05:00 UTC) + manuelle Baselines verhindern Score-Creep |

## Wo leben die geänderten Dateien?

### Embedding / Pipeline

| Pfad | Was sich geändert hat |
|------|----------------------|
| `scripts/model_manager.py` | `get_embedder()` liest `KH_EMBEDDING_MODEL` live (analog `get_reranker()`). `_encode_robust()` für lange Chunks (Längen-Sortierung + bs=32/bs=1-Bucketing) |
| `mcp_servers/knowledge_hub/config.py` | `DEFAULT_MODEL_NAME` auf `BAAI/bge-m3` (1024d) |
| `scripts/embed_index.py` | Collection-Dimension 768→1024, `_encode_robust()`-Integration |
| `scripts/embed_search.py` | Query-Embedding mit BGE-M3 1024d |
| `domains/godot/domain.md` | `Embedding-Model: BAAI/bge-m3 (1024 dims)` |
| `domains/davinci_resolve/domain.md` | `Embedding-Model: BAAI/bge-m3 (1024 dims)` |
| `THIRD_PARTY_LICENSES.md` | BGE-M3 MIT-Lizenz dokumentiert |

### Quality Gate

| Pfad | Was sich geändert hat |
|------|----------------------|
| `scripts/quality/check_regression.py` | `check_regression()`: avg_composite < baseline − 0.1 ODER pass→weak/fail ODER weak→fail |
| `scripts/quality/check_regression_exit.py` | **Neu.** CLI-Wrapper für CI exit-code (0=pass, 1=regression) |
| `.github/workflows/quality-gate.yml` | **Neu.** Weekly Monday 05:00 UTC + `workflow_dispatch`. LFS-Checkout, HuggingFace-Cache mit config.py-Key, Index-Rebuild, `run_evaluation --baseline`, `check_regression_exit` |
| `quality/baselines/godot-latest.json` | **Neu.** Manuelle Baseline für Godot (avg_composite 0.8594) |
| `quality/baselines/davinci_resolve-latest.json` | **Neu.** Manuelle Baseline für DaVinci (avg_composite 0.7246) |
| `quality/baselines/README.md` | **Neu.** Dokumentation des Baseline-Update-Prozesses |
| `.github/workflows/test.yml` | Cache-Key um `config.py` erweitert (B5-Fix) |

### Tests

| Pfad | Was sich geändert hat |
|------|----------------------|
| `tests/integration/test_embedder_config.py` | 3 Tests: env-var-override, domain-md-fallback, default |
| `tests/unit/test_config.py` | 2 Tests: KH_EMBEDDING_MODEL env-var |
| `tests/unit/test_check_regression.py` | 10 Tests: avg_composite, pass→weak, weak→fail, no-regression |

### Dokumentation

| Pfad | Was sich geändert hat |
|------|----------------------|
| `docs/ai/architecture.md` | BGE-M3 1024d/8192 Token, `_encode_robust()` |
| `docs/ai/best-practices.md` | `KH_EMBEDDING_MODEL`-Env-Var dokumentiert |
| `docs/ai/known-issues.md` | LIM-008 (BGE-M3+ms-marco transitional), LIM-009 (long-context confounder) |

### Quality Reports (archiviert)

| Pfad | Inhalt |
|------|--------|
| `docs/superpowers/quality-reports/godot_2026-06-30.md` | Re-Evaluation: 9/9 pass, avg composite 0.8594 |
| `docs/superpowers/quality-reports/godot_2026-06-30.json` | Rohdaten der Evaluation |
| `docs/superpowers/quality-reports/davinci_resolve_2026-06-30.md` | DaVinci Re-Evaluation: 7/7 pass, avg composite 0.7246 |
| `docs/superpowers/quality-reports/davinci_resolve_2026-06-30.json` | Rohdaten der Evaluation |

### Index (nicht committet, `.gitignored`)

- `chromadb_data/godot/` — Rebuild: 24.588 Chunks, 1.326 MB, Dimension 1024
- `chromadb_data/davinci_resolve/` — Rebuild: 2.511 Chunks, 471 MB, Dimension 1024
- Backups wurden nach erfolgreichem Rebuild entfernt

## Validierungsbefehle

```bash
# Tests (alle 319 müssen grün sein)
pytest -m unit          # 109 passed
pytest -m integration   # 41 passed
pytest -m quality       # 145 passed
pytest -m e2e           # 12 passed
pytest -m mcp            # 12 passed

# Quality Evaluation
python scripts/quality/run_evaluation.py --domain godot
python scripts/quality/run_evaluation.py --domain godot --baseline quality/baselines/godot-latest.json
python scripts/quality/check_regression_exit.py --results results.json --baseline quality/baselines/godot-latest.json

# CI Quality Gate (manuell triggern)
gh workflow run quality-gate.yml
```

## Was ist neu in Phase 2a?

### `KH_EMBEDDING_MODEL`-Env-Var
Konfigurierbares Embedding-Modell ohne Code-Änderung. Default ist `BAAI/bge-m3` (1024d, multilingual, 8192 Token Kontext, ~2.2 GB Download, MIT). Precedence: Env-Var > domain.md > `config.DEFAULT_MODEL_NAME`. Gesetzt in `mcp_servers/knowledge_hub/config.py`, ausgewertet von `scripts/model_manager.py:get_embedder()`.

### `_encode_robust()`
Build-time-Helper für lange Chunks auf Apple Silicon. MPS/SDPA kann keine gemischten Lang/Kurz-Batches verarbeiten. Lösung: Chunks nach Länge sortieren, kurze Chunks mit bs=32 encoden, lange Chunks (>8000 chars) mit bs=1. Verhindert OOM bei DaVinci-Fallback-Chunks.

### `check_regression_exit.py`
CI-freundlicher CLI-Wrapper für `check_regression()`. Exit 0 = keine Regression, Exit 1 = Regression erkannt. Prüft: avg_composite < baseline − 0.1, pass→weak/fail, weak→fail.

### `quality-gate.yml`
GitHub Actions Workflow: läuft weekly (Montag 05:00 UTC) und via `workflow_dispatch`. Schritte: LFS-Checkout, Python 3.11, HuggingFace-Cache (Key inkl. config.py), Index-Rebuild für beide Domains, `run_evaluation --baseline`, `check_regression_exit`. Timeout: 60 Min.

### `quality/baselines/`
Manuelle Baseline-Dateien für beide Domains. Werden NUR von Noah aktualisiert (nicht automatisch) — verhindert Score-Creep. `README.md` dokumentiert den Update-Prozess.

## Wo kann ich das Ergebnis sehen?

- **`docs/superpowers/quality-reports/godot_2026-06-30.md`** — Re-Evaluation: 9/9 pass, avg composite 0.8594. godot-008 weak→pass (Sprachbarriere gelöst!)
- **`docs/superpowers/quality-reports/davinci_resolve_2026-06-30.md`** — DaVinci: 7/7 pass, avg composite 0.7246
- **`docs/ai/changelog.md`** — Phase-2a-Einträge
- **`docs/ai/known-issues.md`** — LIM-008 (transitional), LIM-009 (long-context confounder)
- **Manuell testen:**
  ```bash
  # BGE-M3 multilingual testen (godot-008 — englische Query, deutsche faq.md)
  python scripts/hybrid_search.py --domain godot --query "Why is my 3D model not visible" --mode hybrid --top-k 10
  # → faq.md sollte jetzt in Top-10 ranken (vorher Rank 32)
  ```

## Wichtige Hinweise

- **BGE-M3 ~2.2 GB Download** — beim ersten `embed_index.py`-Lauf. In CI mit kaltem Cache kann der Rebuild 40–50 Min dauern (Timeout 60 Min ist knapp).
- **LIM-008: BGE-M3 + ms-marco ist eine Übergangskonfiguration.** BGE-M3 erzeugt multilingual starke Candidates, aber der Stage-2-Reranker (ms-marco) ist English-only und kann gute deutsche Candidates verwerfen. jina-reranker-Test (LIM-007) ist die geplante Lösung.
- **LIM-009: Embedding-Modell-Wechsel + effektive Chunk-Länge ändern sich gleichzeitig.** BGE-M3 8192 Token verarbeitet DaVinci-Chunks vollständig (vorher all-mpnet trunciert auf 384 Token). Die Re-Evaluation mischt beide Effekte — nicht isoliert messbar.
- **Baselines sind manuell** — Noah muss sie nach signifikanten Qualitätsverbesserungen bewusst aktualisieren. Der Quality-Gate-Workflow schlägt fehl, wenn die aktuellen Scores die Baseline unterschreiten.
- **jina-Reranker-Test (LIM-007) steht noch aus** — nach Phase 2a empfohlen. `KH_RERANKER_MODEL=jinaai/jina-reranker-v2-base-multilingual python scripts/quality/run_evaluation.py --domain godot`.

## Verified facts

- 319 Tests grün: 109 unit + 41 integration + 145 quality + 12 e2e + 12 mcp
- godot Re-Evaluation: 9/9 pass, avg composite 0.8594 (+0.0243 vs Phase 1)
- davinci_resolve Re-Evaluation: 7/7 pass, avg composite 0.7246 (+0.0028 vs Phase 1)
- godot-008: weak (0.6404) → pass (0.8594) — Sprachbarriere gelöst
- Godot Index: 24.588 Chunks, 1.326 MB, Dimension 1024
- DaVinci Index: 2.511 Chunks, 471 MB, Dimension 1024
- Backups nach erfolgreichem Rebuild entfernt

## [unverified] notes

- CI Quality Gate Workflow nicht auf GitHub ausgeführt (nur lokal validiert)
- jina-Reranker nicht heruntergeladen oder getestet (LIM-007)
- gitleaks/semgrep availability nicht geprüft

## Next steps

1. jina-Reranker-Test (LIM-007) — Noah entscheidet über Download
2. Phase 2b planen: Late Chunking (2.2) + Golden Dataset 20–30 (2.4)
3. Phase 3: Contextual Retrieval + RAGAS + DaVinci Personal Notes + BGE-M3 Sparse + Multi-Modal

## Weiterlesen

- **Phase 1 Low-Hanging Fruit:** `docs/superpowers/explanations/2026-06-30-phase1-low-hanging-fruit-location.md`
- **godot-007-Fix:** `docs/superpowers/explanations/2026-06-30-godot-007-fix-iteration-location.md`
- **godot-005-Fix:** `docs/superpowers/explanations/2026-06-30-godot-005-fix-iteration-location.md`
- **Domain-Modell:** `docs/ai/domain-model.md` — wie Embedding-Modelle pro Domain konfiguriert werden
- **Validierung:** `docs/ai/validation.md` — alle CLI-Befehle und Test-Stufen
- **Quality Platform:** `docs/superpowers/explanations/2026-06-29-knowledge-hub-quality-evaluation-platform-phase-2-location.md`
