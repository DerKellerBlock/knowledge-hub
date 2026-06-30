# Phase 1 Low-Hanging-Fruit — Wo die Dateien leben

> **Anfängerfreundliche Erklärung** | 2026-06-30 | 5 Maßnahmen für schnelle Qualitätsgewinne

## Was wurde geändert — und warum?

Phase 1 der Verbesserungs-Roadmap implementiert **5 Low-Hanging-Fruit-Maßnahmen** — kleine Änderungen mit großer Wirkung:

| # | Maßnahme | Warum? |
|---|----------|--------|
| 1 | **CI Test-Workflow** | Sichert die 302 Tests vor Regression — kein kaputter Code mehr auf `main` |
| 2 | **Reranker-Env-Var** | Ermöglicht Modellwechsel ohne Code-Änderung (Nachhaltigkeits-Hebel) |
| 3 | **BM25 CamelCase-Splitting** | Löst die „CharacterBody3D nicht gefunden“-Klasse von Problemen |
| 4 | **Chunk-Overlap 200→400** | Reduziert „lost context“ an Chunk-Grenzen |
| 5 | **faq.md füllen** | 3 häufige Anfängerfragen beantwortet (Lifecycle, Data Saving, 3D Visibility) |

## Wo leben die geänderten Dateien?

### CI (neu)

| Pfad | Was es tut |
|------|-----------|
| `.github/workflows/test.yml` | GitHub Actions Workflow: Python 3.11, ubuntu-latest, unit+integration+mcp, HuggingFace-Cache |

### Search / Pipeline

| Pfad | Was sich geändert hat |
|------|----------------------|
| `mcp_servers/knowledge_hub/config.py` | `KH_RERANKER_MODEL`-Env-Var (Default ms-marco, Optional jina) |
| `scripts/model_manager.py` | `trust_remote_code=True` für jina-Custom-Code |
| `scripts/reranker.py` | Score-Skala-Kommentar (ms-marco logits vs jina sigmoid) |
| `scripts/bm25_search.py` | Unicode-aware `tokenize()` mit CamelCase-Splitting |
| `scripts/parser_base.py` | `FALLBACK_CHUNK_OVERLAP` 200→400 Tokens |
| `requirements.txt` | `einops>=0.7.0` (für jina) |
| `THIRD_PARTY_LICENSES.md` | CC-BY-NC-4.0 Kategorie für jina |

### Content

| Pfad | Was sich geändert hat |
|------|----------------------|
| `domains/godot/personal/faq.md` | 3 Sektionen gefüllt: Lifecycle, Data Saving, 3D Visibility |
| `quality/golden/godot.yaml` | `godot-008` eingefügt (3D Visibility, 2 expected_sources) |

### Tests

| Pfad | Was sich geändert hat |
|------|----------------------|
| `tests/unit/test_config.py` | 2 neue Tests (env-var-override, default) |
| `tests/unit/test_bm25_tokenizer.py` | 15 Tests (7 angepasst + 8 neu) |
| `tests/unit/test_parser_base.py` | 1 Assert geändert (800→1600) |

### Dokumentation

| Pfad | Was sich geändert hat |
|------|----------------------|
| `docs/ai/best-practices.md` | Abschnitt „Umgebungsvariablen“ |
| `docs/ai/changelog.md` | Phase-1-Einträge |
| `docs/ai/known-issues.md` | godot-008-Lücke dokumentiert |
| `docs/ai/architecture.md` | BM25-CamelCase, Overlap-Änderung |

### Quality Reports (archiviert)

| Pfad | Inhalt |
|------|--------|
| `docs/superpowers/quality-reports/godot_2026-06-30.md` | Re-Evaluation: 7 pass + 1 weak, avg composite 0.8321 |
| `docs/superpowers/quality-reports/godot_2026-06-30.json` | Rohdaten der Evaluation |
| `docs/superpowers/quality-reports/davinci_resolve_2026-06-30.md` | DaVinci Re-Evaluation |
| `docs/superpowers/quality-reports/davinci_resolve_2026-06-30.json` | Rohdaten der Evaluation |

### Index (nicht committet, `.gitignored`)

- `chromadb_data/godot/` — Rebuild: 24.588 Chunks
- `chromadb_data/davinci_resolve/` — Rebuild: 2.511 Chunks
- `chromadb_data/godot.bak.phase1/` — Backup (Noah freigibt zum Entfernen)
- `chromadb_data/davinci_resolve.bak.phase1/` — Backup (Noah freigibt zum Entfernen)

## OpenCode-Konfiguration

Die Projektkonfiguration lebt in zwei Dateien — **beide wurden in Phase 1 nicht geändert:**

- **`.opencode/opencode.json`** — Definiert den primären Agenten (`orchestrator-knowledge`), das Modell, die MCP-Server, Bash-Permissions und welche Doku-Dateien beim Start geladen werden.
- **`.opencode/agents/*.md`** — 14 Agent-Prompt-Dateien. Jede Datei enthält die vollständige Anweisung für einen spezialisierten Agenten.

## Die Agenten-Rollen (kurz)

| Agent | Aufgabe |
|---|---|
| `orchestrator-knowledge` | Koordiniert die Feedback-Schleife, synthetisiert Antworten, delegiert an Subagenten |
| `read-hub-docs` | Liest Doku, fasst zusammen |
| `inspect-hub-project` | Inspiziert Code lesend, liefert Fakten |
| `research-knowledge-domain` | Recherchiert externe Quellen (für neue Domains/Quellen) |
| `plan-hub-change` | Erstellt Implementierungspläne |
| `review-hub-plan-blindspots` | Prüft Pläne auf übersehene Risiken |
| `implement-hub-change` | Implementiert Code-Änderungen |
| `validate-hub-project` | Führt Syntax/Struktur-Checks aus |
| `test-hub-feature` | Führt pytest + Knowledge-QA aus (read-only) |
| `review-hub-security` | Security-Review (Secrets, Pfade, Dependencies) |
| `review-hub-diff` | Diff-Review (Code-Qualität, Regressionen, Doku-Lücken) |
| `update-hub-docs` | Aktualisiert Doku nach Änderungen |
| `retrospect-iteration` | Schreibt Retrospektiven |
| `explain-location` | Schreibt Location-Erklärungen (das hier) |

## Validierungsbefehle

Diese Befehle kann Noah (und der `validate-hub-project`-Agent) ausführen:

```bash
# Syntax-Checks
find . -name "*.py" -not -path "*/__pycache__/*" -not -path "*/.venv/*" -not -path "*/chromadb_data/*" -exec python3 -m py_compile {} \;
find . -name "*.sh" -not -path "*/.venv/*" -not -path "*/chromadb_data/*" -exec bash -n {} \;

# Workspace-Struktur
./scripts/workspace_check.sh
./scripts/workspace_status.sh

# Tests (alle 302 müssen grün sein)
pytest -m unit          # 107 passed
pytest -m integration   # 35 passed
pytest -m quality       # 136 passed
pytest -m e2e           # 12 passed
pytest -m mcp            # 12 passed

# Quality Evaluation
python scripts/quality/run_evaluation.py --domain godot
python scripts/quality/validate_dataset.py --domain godot --check-sources

# Manuelle Suche (BM25 CamelCase-Split testen)
python scripts/hybrid_search.py --domain godot --query "CharacterBody3D move_and_slide" --mode hybrid --top-k 10
# Erwartet: move_and_slide Methode Top-1 (BM25 CamelCase Split)

# jina-Reranker testen (erfordert ~1.1 GB Download, Noah freigibt)
KH_RERANKER_MODEL=jinaai/jina-reranker-v2-base-multilingual python scripts/hybrid_search.py --domain godot --query "..." --mode hybrid
```

## Knowledge-QA-Ablauf (wie die Qualität geprüft wird)

1. **`run_evaluation.py --domain godot`** führt alle Golden-Dataset-Fragen gegen den Live-Index aus. Jede Frage wird via `hybrid_search.search()` abgefragt.
2. **`scorer.py`** berechnet den **Composite Score** aus vier Metriken:
   - **SR** (Source Recall) — Sind die erwarteten Quellen in den Top-Ergebnissen?
   - **PMA** (Page Metadata Accuracy) — Sind PDF-Seiten korrekt? (N/A für Godot, Gewichte werden umverteilt)
   - **TKR** (Top-K Relevance) — Wie viele der Top-10-Ergebnisse sind relevant?
   - **EQ** (Evidence Quality) — Enthalten die Snippets verwertbare Informationen?
3. **Schwellen:** pass ≥ 0.7, weak 0.4–0.7, fail < 0.4.
4. **`generate_report.py --archive`** schreibt einen Markdown-Report + JSON nach `docs/superpowers/quality-reports/`.
5. Der Report enthält eine **Real-World Source Comparison** mit Online-Quellen (URLs aus dem Golden Dataset) und GFM-Checkboxen für manuelle Evaluation (Source Coverage, Solution Alignment, Gap Detection).

## Was ist neu in Phase 1?

### `KH_RERANKER_MODEL`-Env-Var
Konfigurierbarer Reranker ohne Code-Änderung. Default ist `cross-encoder/ms-marco-MiniLM-L-12-v2` (~140 MB). Optional: `jinaai/jina-reranker-v2-base-multilingual` (multilingual, 1024 Token Kontext, ~1.1 GB Download, CC-BY-NC-4.0). Gesetzt in `mcp_servers/knowledge_hub/config.py`, ausgewertet von `scripts/model_manager.py`.

### Unicode-aware BM25-Tokenizer
CamelCase-Splitting mit Regex: `CharacterBody3D` → `["character", "body", "3", "d"]`. Umlaute bleiben erhalten (`Größe` → `["größe"]`). ALLCAPS-Akronyme bleiben intakt (`GPU` → `["gpu"]`). Symmetrisch für Index und Query. Implementiert in `scripts/bm25_search.py:tokenize()`.

### Chunk-Overlap 400 Tokens
`FALLBACK_CHUNK_OVERLAP` von 200 auf 400 Tokens erhöht (`FALLBACK_OVERLAP_CHARS` 800→1600). Bessere Kontext-Erhaltung an Chunk-Grenzen. In `scripts/parser_base.py`.

### faq.md 3 Sektionen
`domains/godot/personal/faq.md` mit drei häufigen Anfängerfragen gefüllt:
- **Lifecycle** — `_enter_tree()`, `_ready()`, `_process()`, `_physics_process()`, `_exit_tree()`
- **Data Saving** — `ConfigFile`, `FileAccess`, `JSON`, `ResourceSaver`, `user://`-Pfad
- **3D Visibility** — `visible`-Flag, `Camera3D.current`, `cull_mask`/`layers`, `process_mode`, Scale/Position, Material-Transparenz

### CI Test-Workflow
`.github/workflows/test.yml` läuft bei Push und Pull Request auf `main`. Python 3.11, ubuntu-latest, HuggingFace-Cache. Führt unit, integration und mcp Tests aus. Quality und e2e sind ausgeschlossen (benötigen vorgebauten Index).

## Wo kann ich das Ergebnis sehen?

- **`docs/superpowers/quality-reports/godot_2026-06-30.md`** — Re-Evaluation: 7 pass + 1 weak (godot-008), avg composite 0.8321
- **`docs/ai/changelog.md`** — Phase-1-Einträge (Zeilen 52–58)
- **`docs/ai/best-practices.md`** — Umgebungsvariablen-Abschnitt
- **`docs/ai/known-issues.md`** — godot-008-Lücke dokumentiert
- **Manuell testen:**
  ```bash
  python scripts/hybrid_search.py --domain godot --query "CharacterBody3D move_and_slide" --mode hybrid
  ```
  → `move_and_slide` sollte Top-1 ranken (BM25 CamelCase Split).

## Wichtige Hinweise

- **jina-Reranker Download (~1.1 GB) ist optional** — Default ist ms-marco. Noah muss den Download freigeben.
- **`trust_remote_code=True`** — bewusst akzeptiert für persönlichen Hub (jina-Custom-Code). Dokumentiert in `THIRD_PARTY_LICENSES.md`.
- **Backups** — `chromadb_data/godot.bak.phase1/` und `chromadb_data/davinci_resolve.bak.phase1/` existieren. Noah kann sie nach Review entfernen: `rm -rf chromadb_data/*.bak.phase1`.
- **godot-008 weak** — `faq.md` 3D-Visibility-Sektion ist frisch indexiert, aber semantisch nahe an `godot-docs-3d-packed.md`. Die Frage ist breit („warum sehe ich mein 3D-Modell nicht“), `faq.md` rankt nicht in Top-10. Phase 2 (BGE-M3 multilingual) wird helfen.

## Verified facts

- 302 Tests grün: 107 unit + 35 integration + 136 quality + 12 e2e + 12 mcp
- godot Re-Evaluation: 7 pass + 1 weak, avg composite 0.8321
- davinci_resolve Re-Evaluation: 7 pass, avg composite 0.7218
- Godot Index: 24.588 Chunks, ChromaDB ~589 MB
- DaVinci Index: 2.511 Chunks
- `workspace_check.sh`: PASS (exit 0)
- `.opencode/opencode.json`: valid JSON, no inline agent block
- 14 agent files in `.opencode/agents/`

## [unverified] notes

- jina-Reranker nicht heruntergeladen oder getestet (erfordert Noahs Freigabe)
- CI Workflow nicht auf GitHub ausgeführt (nur lokal validiert)
- gitleaks/semgrep availability nicht geprüft

## Next steps

1. Noah reviewed die Backups und entfernt sie: `rm -rf chromadb_data/*.bak.phase1`
2. Noah entscheidet, ob der jina-Reranker heruntergeladen werden soll
3. Phase 2 planen: BGE-M3 multilingual Embeddings für godot-008 und andere semantische Lücken
4. Commit der Phase-1-Änderungen wenn bereit

## Weiterlesen

- **godot-007-Fix:** `docs/superpowers/explanations/2026-06-30-godot-007-fix-iteration-location.md` — vorherige Fix-Iteration (Content-Only)
- **godot-005-Fix:** `docs/superpowers/explanations/2026-06-30-godot-005-fix-iteration-location.md` — markdown_section_chunk
- **Domain-Modell:** `docs/ai/domain-model.md` — wie Personal Notes und Chunk-Typen funktionieren
- **Validierung:** `docs/ai/validation.md` — alle CLI-Befehle und Test-Stufen
- **Quality Platform:** `docs/superpowers/explanations/2026-06-29-knowledge-hub-quality-evaluation-platform-phase-2-location.md`
