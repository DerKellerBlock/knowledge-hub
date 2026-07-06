# godot-007-Fix-Iteration — Wo die Dateien leben

> **Anfängerfreundliche Erklärung** | 2026-06-30 | Content-Only Fix via tips.md Code-Snippet

## Was wurde geändert — und warum?

Die Frage **godot-007** („How do I create a 3D character controller with movement, jumping, and gravity?“) war die schwächste im Golden Dataset: Composite 0.71, Source Recall 0.67 — knapp über der Pass-Schwelle, aber mit deutlichem Abstand zu den anderen 6 Fragen.

**Zwei Bottlenecks blockierten die Suche:**

1. **BM25-Token-Overlap = 0** — Die `tips.md`-Sektion „CharacterBody3D Stair Stepping“ war auf Deutsch geschrieben, die Query auf Englisch. BM25 fand keine übereinstimmenden Tokens (velocity, gravity, jump, move_and_slide).
2. **Cross-Encoder -8.53** — Die Sektion las sich wie ein isolierter Stair-Stepping-Tipp, nicht wie ein vollständiger Character-Controller. Der Cross-Encoder bewertete den Kontext als irrelevant.

**Lösung:** Die Sektion wurde um ein GDScript-Code-Snippet erweitert, das beide Bottlenecks gleichzeitig behebt:
- Das Snippet enthält die englischen Keywords (velocity, gravity, jump, move_and_slide) als Tokens → BM25 findet sie.
- Die Sektion liest sich jetzt als vollständiger CharacterBody3D-Controller mit Movement, Jumping und Gravity → Cross-Encoder erkennt den Kontext.

**Ergebnis:** godot-007 von 0.71 → 0.86 (pass). Alle 7 Godot-Fragen pass (avg composite 0.86, avg SR 1.0).

**Wichtig:** Dies war ein **reiner Content-Edit** — keine Änderung an `hybrid_search.py`, `bm25_search.py`, `parser_base.py` oder `reranker.py`. Guter Content bringt oft mehr als Ranking-Tuning.

## Wo leben die geänderten Dateien?

### Content (die eigentliche Änderung)

| Pfad | Was sich geändert hat |
|---|---|
| `domains/godot/personal/tips.md` | Sektion „CharacterBody3D Stair Stepping“ erweitert (~460 → ~3061 Zeichen). Neuer Untertitel „### Integration in einen vollständigen CharacterBody3D-Controller“, Einleitungstext, GDScript-Code-Snippet, Tokens-Liste. |

### Dokumentation (was Agenten und Noah wissen müssen)

| Pfad | Was sich geändert hat |
|---|---|
| `docs/ai/changelog.md` | Neuer Eintrag `fix(godot): godot-007` |
| `docs/ai/known-issues.md` | KI-004 (godot-007) unter „Behobene Probleme“, „Bekannte Retrieval-Lücken“ jetzt leer |
| `docs/ai/fixes.md` | Neuer Eintrag „2026-06-30 — godot-007 Retrieval-Lücke geschlossen via tips.md Code-Snippet“ |

### Quality Reports (archivierte Evaluationsergebnisse)

| Pfad | Was es enthält |
|---|---|
| `docs/superpowers/quality-reports/godot_2026-06-30.md` | Vollständiger Re-Evaluations-Report (Markdown) |
| `docs/superpowers/quality-reports/godot_2026-06-30.json` | Rohdaten der Evaluation (JSON) |

### Index (nicht committet, `.gitignored`)

- `chromadb_data/godot/` — Rebuild: 24.564 Chunks (unverändert, da nur Content innerhalb eines bestehenden Chunks erweitert wurde)
- `chromadb_data/godot.bak.20260630-v2/` — Backup vor Rebuild (nach Noahs Review löschen: `rm -rf chromadb_data/godot.bak.20260630-v2`)

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
pytest -m unit          # 97 passed
pytest -m integration   # 35 passed
pytest -m quality       # 136 passed
pytest -m e2e           # 12 passed
pytest -m mcp            # 12 passed

# Domain-Status
./domains/godot/scripts/status.sh

# Quality Evaluation
python scripts/quality/run_evaluation.py --domain godot
python scripts/quality/generate_report.py --input <results.json> --archive

# Manuelle Suche (zum Testen)
python scripts/hybrid_search.py --domain godot --query "How do I create a 3D character controller with movement, jumping, and gravity?" --mode hybrid --top-k 10
# Erwartung: tips.md in Top-10 (Top-2)

python scripts/hybrid_search.py --domain godot --query "CharacterBody3D Stair Stepping" --mode hybrid --top-k 5
# Erwartung: tips.md Top-1
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

Die Sektion **„CharacterBody3D Stair Stepping“** in `domains/godot/personal/tips.md` wurde erweitert:

- **Untertitel** `### Integration in einen vollständigen CharacterBody3D-Controller` — macht den Kontext für den Cross-Encoder klar.
- **Einleitungstext** — erklärt, wie Stair Stepping in einen vollständigen Controller integriert wird.
- **GDScript-Code-Snippet** — enthält Movement (Input.get_vector, transform.basis, move_toward), Jumping (Input.is_action_just_pressed, is_on_floor), Gravity (ProjectSettings.get_setting) und Stair Stepping (step_enabled, step_height, get_visual_position).
- **Tokens-Liste** nach dem Code — erklärt, welche Methoden für Movement, Jumping und Gravity relevant sind.
- **PR-#114447-Kennzeichnung** — `step_enabled`, `step_height` und `get_visual_position` sind explizit als „requires PR #114447, not yet in Godot stable“ markiert. Alle anderen APIs sind Godot-4-Stable.

**Warum das funktioniert:**
- BM25 findet jetzt Tokens wie `velocity`, `gravity`, `jump`, `move_and_slide` im Code-Snippet.
- Der Cross-Encoder sieht einen vollständigen Character-Controller-Kontext (Movement + Jumping + Gravity + Stair Stepping) statt eines isolierten Tipps.
- Die Sektion rankt von Cross-Encoder -8.53 → +0.71 und von Rank 32 → Top-2.

## Wo kann ich das Ergebnis sehen?

- **`docs/superpowers/quality-reports/godot_2026-06-30.md`** — vollständiger Re-Evaluations-Report (alle 7 Fragen pass, Avg Composite 0.86).
- **`docs/ai/changelog.md`** — Eintrag `fix(godot): godot-007` mit technischen Details.
- **`docs/ai/fixes.md`** — godot-007 als behobenes Problem.
- **`docs/ai/known-issues.md`** — „Bekannte Retrieval-Lücken“ jetzt leer (alle 7 godot-Fragen pass).
- **Manuell testen:**
  ```bash
  python scripts/hybrid_search.py --domain godot --query "3D character controller movement jumping gravity" --mode hybrid
  ```
  → `tips.md` sollte Top-2 ranken mit der Sektion „CharacterBody3D Stair Stepping“.

## Wichtige Hinweise

- **PR #114447 ist nicht in Godot Stable:** Das Code-Snippet enthält APIs (`step_enabled`, `step_height`, `get_visual_position`), die erst mit dem offenen PR in Godot einfließen. Das Snippet kennzeichnet sie explizit mit „requires PR #114447, not yet in Godot stable“.
- **Kein Pipeline-Code-Change:** Diese Iteration war ein reiner Content-Edit in einer Personal Note. Keine Änderung an `hybrid_search.py`, `bm25_search.py`, `parser_base.py` oder `reranker.py`. Das zeigt, dass guter Content oft mehr bringt als Ranking-Tuning.
- **Backup beachten:** `chromadb_data/godot.bak.20260630-v2/` existiert noch und kann nach Noahs Review entfernt werden: `rm -rf chromadb_data/godot.bak.20260630-v2`.

## Weiterlesen

- **godot-005-Erklärung:** `docs/superpowers/explanations/2026-06-30-godot-005-fix-iteration-location.md` — die vorherige Fix-Iteration (markdown_section_chunk)
- **Domain-Modell:** `docs/ai/domain-model.md` — wie Personal Notes und Chunk-Typen funktionieren
- **Validierung:** `docs/ai/validation.md` — alle CLI-Befehle und Test-Stufen
- **Quality Platform:** `docs/superpowers/explanations/2026-06-29-knowledge-hub-quality-evaluation-platform-phase-2-location.md`
