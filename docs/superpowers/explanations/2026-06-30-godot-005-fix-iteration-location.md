# godot-005-Fix-Iteration — Wo die Dateien leben

> **Anfängerfreundliche Erklärung** | 2026-06-30 | Markdown Section Chunking für Personal Notes

## Was wurde geändert — und warum?

Die Frage **godot-005** („How do I fix GLB model import scale issues from Meshy in Godot 4?“) war im Golden Dataset von **pass auf weak gefallen** (Composite 0.42, Source Recall 0.0). Die Antwort stand in `gotchas.md` — aber der Index fand sie nicht.

**Wurzelursache:** `gotchas.md` (3.454 Zeichen, 7 Gotcha-Einträge) wurde als **ein einziger Chunk** indexiert. Der Cross-Encoder sah einen Text mit 6 irrelevanten Einträgen und einem relevanten — die Semantik war verwässert, der Chunk rankte nicht.

**Lösung:** Eine neue Chunking-Funktion `markdown_section_chunk()` splittet Personal Notes an `##`-Headern in eigenständige Sektionen. Jeder Gotcha, jeder Tip, jede Best Practice wird ein eigener Chunk — und damit einzeln suchbar.

**Ergebnis:** godot-005 von 0.42 (weak) → 0.86 (pass). Alle 7 Godot-Fragen pass (avg composite 0.84).

## Wo leben die geänderten Dateien?

### Code (die eigentliche Änderung)

| Pfad | Was sich geändert hat |
|---|---|
| `scripts/parser_base.py` | Neue Funktion `markdown_section_chunk()` — splittet Markdown an `##`-Headern, defensive Skip-Bedingung (<50 Zeichen), Fallback auf `fallback_chunk()` |
| `scripts/embed_index.py` | Personal-Loop von `fallback_chunk()` auf `markdown_section_chunk()` umgestellt |
| `tests/unit/test_parser_base.py` | Neue `TestMarkdownSectionChunk`-Klasse mit 13 Tests |
| `tests/conftest.py` | `indexed_dummy`-Fixture aktualisiert (spiegelt embed_index.py wider) |

### Dokumentation (was Agenten und Noah wissen müssen)

| Pfad | Was sich geändert hat |
|---|---|
| `docs/ai/changelog.md` | Neuer Eintrag 2026-06-30 mit allen Details |
| `docs/ai/known-issues.md` | LIM-002 aktualisiert (section_path bei Preamble-Chunks), LIM-006 neu (line_end-Offset), godot-007-Lücke dokumentiert |
| `docs/ai/architecture.md` | `markdown_section_chunk` als neue Komponente |
| `docs/ai/domain-model.md` | `personal_section` als neuer `chunk_type` |
| `docs/ai/fixes.md` | Neuer Eintrag godot-005-Regression |

### Quality Reports (archivierte Evaluationsergebnisse)

| Pfad | Was es enthält |
|---|---|
| `docs/superpowers/quality-reports/godot_2026-06-30.md` | Vollständiger Re-Evaluations-Report (Markdown) |
| `docs/superpowers/quality-reports/godot_2026-06-30.json` | Rohdaten der Evaluation (JSON) |

### Index (nicht committet, `.gitignored`)

- `chromadb_data/godot/` — Rebuild: 24.552 → 24.564 Chunks (+12 personal section chunks)
- `chromadb_data/godot.bak.20260630/` — Backup vor Rebuild (nach Noahs Review löschen)

## OpenCode-Konfiguration

Die Projektkonfiguration lebt in zwei Dateien:

- **`.opencode/opencode.json`** — Definiert den primären Agenten (`orchestrator-knowledge`), das Modell, die MCP-Server, Bash-Permissions und welche Doku-Dateien beim Start geladen werden (`AGENTS.md`, `docs/ai/*.md`).
- **`.opencode/agents/*.md`** — 14 Agent-Prompt-Dateien. Jede Datei enthält die vollständige Anweisung für einen spezialisierten Agenten. Die Dateinamen (ohne `.md`) sind die Task-Permission-Namen, die in `opencode.json` referenziert werden.

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
find . -name "*.sh" -not -path "*/.venv/*" -not -path "*/chromadb_data/*" -exec bash -n {} \;
find . -name "*.py" -not -path "*/__pycache__/*" -not -path "*/.venv/*" -not -path "*/chromadb_data/*" -exec python3 -m py_compile {} \;
python3 -m json.tool .opencode/opencode.json > /dev/null

# Workspace-Struktur
./scripts/workspace_check.sh
./scripts/workspace_status.sh

# Tests (292 Tests, alle grün in dieser Iteration)
pytest -m unit          # 97 passed (inkl. 13 neue markdown_section_chunk-Tests)
pytest -m integration   # 35 passed
pytest -m quality       # 136 passed
pytest -m e2e           # 12 passed
pytest -m mcp           # 12 passed

# Domain-Status
./domains/godot/scripts/status.sh

# Quality Evaluation
python scripts/quality/run_evaluation.py --domain godot
python scripts/quality/generate_report.py --input <results.json> --archive

# Manuelle Suche (zum Testen)
python scripts/hybrid_search.py --domain godot --query "GLB model import scale Meshy" --mode hybrid --top-k 10
```

## Knowledge-QA-Ablauf (wie die Qualität geprüft wird)

1. **`run_evaluation.py --domain godot`** führt alle 7 Golden-Dataset-Fragen gegen den Live-Index aus. Jede Frage wird via `hybrid_search.search()` abgefragt.
2. **`scorer.py`** berechnet den **Composite Score** aus vier Metriken:
   - **SR** (Source Recall) — Sind die erwarteten Quellen in den Top-Ergebnissen?
   - **PMA** (Page Metadata Accuracy) — Sind PDF-Seiten korrekt? (N/A für Godot, Gewichte werden umverteilt)
   - **TKR** (Top-K Relevance) — Wie viele der Top-10-Ergebnisse sind relevant?
   - **EQ** (Evidence Quality) — Enthalten die Snippets verwertbare Informationen?
3. **Schwellen:** pass ≥ 0.7, weak 0.4–0.7, fail < 0.4.
4. **`generate_report.py --archive`** schreibt einen Markdown-Report + JSON nach `docs/superpowers/quality-reports/`.
5. Der Report enthält eine **Real-World Source Comparison** mit Online-Quellen (URLs aus dem Golden Dataset) und GFM-Checkboxen für manuelle Evaluation (Source Coverage, Solution Alignment, Gap Detection).

## Was ist neu in dieser Iteration?

**`markdown_section_chunk()`** — die neue Chunking-Funktion in `scripts/parser_base.py`:

- **Splittet an `##`-Headern** — jede Sektion wird ein eigener Chunk mit `chunk_type="personal_section"` und `name=<Sektionsüberschrift>`.
- **Defensive Skip-Bedingung** — Sektionen und Preambles mit weniger als 50 Zeichen (nach Strip) werden übersprungen. Das filtert TODO-Platzhalter und leere Abschnitte.
- **Preamble-Chunk** — Text vor dem ersten `##`-Header wird nur indexiert, wenn er ≥ 50 Zeichen hat.
- **Fallback** — Dateien ohne `##`-Header fallen auf `fallback_chunk()` zurück (1 Chunk pro Datei).
- **BM25-Verbesserung** — `chunk.name` wird in der BM25-Tokenisierung 2× gewichtet. Spezifischere Sektionsnamen (z. B. „GLB-Import — Mesh Origin Bug“ statt „gotchas“) verbessern das BM25-Ranking.

**Index-Rebuild-Effekt:** 24.552 → 24.564 Chunks (+12):
- `gotchas.md`: 1 → 8 Chunks (7 Gotchas + Preamble)
- `best-practices.md`: 1 → 4 Chunks (3 Sektionen + Preamble)
- `tips.md`: 1 → 4 Chunks (3 Sektionen + Preamble)
- `faq.md`: 1 → 0 Chunks (alle Sektionen < 50 Zeichen, defensive Skip)

## Wo kann ich das Ergebnis sehen?

- **`docs/superpowers/quality-reports/godot_2026-06-30.md`** — vollständiger Re-Evaluations-Report mit allen 7 Fragen, Snippets und Real-World Source Comparison.
- **`docs/ai/changelog.md`** — Eintrag 2026-06-30 mit allen technischen Details.
- **`docs/ai/known-issues.md`** — LIM-002, LIM-006 und godot-007-Lücke.
- **`docs/ai/fixes.md`** — godot-005-Regression als behobenes Problem.
- **Manuell testen:**
  ```bash
  python scripts/hybrid_search.py --domain godot --query "GLB model import scale Meshy" --mode hybrid
  ```
  → `gotchas.md` sollte Top-1 ranken mit der Sektion „GLB-Import — Mesh Origin Bug“.

## Weiterlesen

- **Design-Spec:** `docs/superpowers/specs/2026-06-09-knowledge-hub-design.md` — vollständige Architektur
- **Domain-Modell:** `docs/ai/domain-model.md` — wie Chunk-Typen und Personal Notes funktionieren
- **Validierung:** `docs/ai/validation.md` — alle CLI-Befehle und Test-Stufen
- **Quality Platform Phase 2:** `docs/superpowers/explanations/2026-06-29-knowledge-hub-quality-evaluation-platform-phase-2-location.md`
