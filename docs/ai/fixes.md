# Fixes — Knowledge Hub

This file records completed fixes that are useful for future AI agents.

## Format

```markdown
## YYYY-MM-DD — Short title

- Problem: What was broken or risky.
- Fix: What changed.
- Validation: Commands actually run.
- Status: Fixed / Partially fixed / Follow-up required.
```

## 2026-06-29 — OpenCode standard migration

- Problem: Knowledge Hub used inline OpenCode agents inside `.opencode/opencode.json`, had no root `AGENTS.md`, no workspace validation scripts, incomplete `docs/ai/` tree (missing `security.md`, `fixes.md`, `handoffs/`), and no Knowledge-QA agent. `.opencode/.gitignore` blanket-ignored all files except `.gitignore` and `opencode.json`, so any new agent files would not be tracked by git.
- Fix: Migrated to file-based agents in `.opencode/agents/*.md` (11 extracted + 3 new: `test-hub-feature`, `retrospect-iteration`, `explain-location`). Slimmed `.opencode/opencode.json` (removed inline `agent` block, added `AGENTS.md` and `docs/ai/security.md` to instructions). Added root `AGENTS.md`, `scripts/workspace_check.sh`, `scripts/workspace_status.sh`, `docs/ai/security.md`, `docs/ai/fixes.md`, `docs/ai/handoffs/.gitkeep`, `docs/superpowers/explanations/.gitkeep`, `docs/superpowers/retrospectives/.gitkeep`. Fixed `.opencode/.gitignore` to un-ignore `agents/` and `agents/**`. Updated `docs/ai/README.md`, `docs/ai/project-context.md`, `docs/ai/validation.md`, `docs/ai/known-issues.md`, `docs/ai/changelog.md`, `docs/README.md`, `README.md`, and `.gitignore`. Implementation details are tracked in `docs/superpowers/plans/2026-06-29-knowledge-hub-opencode-standard-migration.md`.
- Validation: Commands actually run in this session (all passed):
  ```bash
  ./scripts/workspace_check.sh                                   # PASS, exit 0
  ./scripts/workspace_status.sh                                  # reports 14 agents, all AI docs present, all test dirs present
  python3 -m json.tool .opencode/opencode.json >/dev/null        # valid JSON, no inline agent block
  bash -n scripts/workspace_check.sh scripts/workspace_status.sh # bash syntax OK
  .venv/bin/python -m pytest -m unit                             # 78 passed, 59 deselected, 2 warnings in 3.79s
  ```
  Prompt roundtrip verified against `git show HEAD:.opencode/opencode.json`: all 10 preserved inline-agent prompts match the body of their `.opencode/agents/*.md` files (`prompt roundtrip ok`).
  DaVinci source files and `chromadb_data/` were not modified by the migration.
- Status: Implemented. Follow-up required: restart OpenCode to load new agent config; run `pytest -m integration`, `pytest -m e2e`, `pytest -m mcp` to confirm full test suite.

## 2026-06-30 — godot-005-Regression: Markdown Section Chunking für Personal Notes

- Problem: `gotchas.md` (3.454 Zeichen, 7 Gotcha-Einträge) wurde als 1 Chunk indexiert. Die Cross-Encoder-Semantik wurde durch 6 irrelevante Einträge verwässert, sodass die relevante GLB-Import-Sektion nicht rankte. godot-005 (GLB import mesh origin) war weak (composite 0.4219, SR 0.0).
- Fix: Neue Funktion `markdown_section_chunk()` in `scripts/parser_base.py` — splittet Markdown an `##`-Headern in per-section Chunks (`chunk_type="personal_section"`, `name=Sektionsüberschrift`). Defensive Skip-Bedingung für Sektionen/Preambles <50 Zeichen nach Strip (filtert TODO-Platzhalter). Fallback auf `fallback_chunk()` bei Dateien ohne `##`-Header. `scripts/embed_index.py`: Personal-Loop von `fallback_chunk()` auf `markdown_section_chunk()` umgestellt. `c.name = category` entfernt (wird jetzt von neuer Funktion als Sektions-Überschrift gesetzt — BM25-Tokenisierung gewichtet `chunk.name` 2x, spezifischere Sektionsnamen verbessern BM25-Ranking). 13 neue Unit-Tests in `tests/unit/test_parser_base.py` (`TestMarkdownSectionChunk`). `tests/conftest.py`: `indexed_dummy`-Fixture aktualisiert.
- Validation: Commands actually run in this session (all passed):
  ```bash
  pytest -m unit        # 97 passed (84 alt + 13 neu)
  pytest -m integration # 35 passed
  pytest -m quality     # 136 passed
  pytest -m e2e         # 12 passed
  pytest -m mcp         # 12 passed
  ```
  Index-Rebuild: 24.552 → 24.564 Chunks (+12 personal section chunks: gotchas.md 1→8, best-practices.md 1→4, tips.md 1→4, faq.md 1→0 wegen defensive Skip). BM25-Pickle neu gebaut, ChromaDB ~589 MB.
  Quality Re-Evaluation: godot-005 0.4219 (weak) → 0.8594 (pass), SR 1.0 (gotchas.md Top-1 "GLB-Import — Mesh Origin Bug"). Alle 7 godot-Fragen pass (avg composite 0.8386). godot-007 bleibt bei 0.7136 (bestehende Lücke aus Gap-Closing-Iteration f5be7e0, nicht durch diese Iteration verursacht).
  Security-Verdict: SAFE MIT HINWEISEN (keine neuen Dependencies, keine Secrets, Regex sicher, Pickle-BM25-Rebuild aus lokalen Dateien). Diff-Verdict: APPROVE MIT HINWEISEN (Code-Qualität, Richtigkeit, Test-Qualität, Architektur-Konsistenz alle ✅).
- Status: Fixed. godot-005 pass 0.86. godot-007 bleibt als bekannte Lücke dokumentiert (LIM-006, godot-007 in known-issues.md).

## 2026-06-30 — godot-007 Retrieval-Lücke geschlossen via tips.md Code-Snippet

- Problem: godot-007 (3D character controller, difficulty: hard) hatte die niedrigste Source Recall (0.6667) und den niedrigsten Composite Score (0.7136) aller 7 godot-Fragen. Zwei Bottlenecks: (1) BM25-Token-Overlap = 0 (deutsche Sektion, englische Query, keine Query-Keywords als Tokens), (2) Cross-Encoder (ms-marco-MiniLM-L-12-v2) bewertete -8.53 (kein Character-Controller-Kontext, nur Stair-Stepping-Bullet-Liste).
- Fix: `tips.md`/CharacterBody3D Stair Stepping-Sektion um Untertitel "### Integration in einen vollständigen CharacterBody3D-Controller", Einleitungstext, GDScript-Code-Snippet (Godot-4-Stable-APIs plus PR-#114447-APIs klar gekennzeichnet) und Tokens-Liste erweitert. Sektion wuchs von ~460 auf ~3061 Zeichen. Re-Indexierung und Re-Evaluation durchgeführt.
- Validation: Quality Re-Evaluation: godot-007 Composite 0.8594 (pass), SR 1.0, tips.md Top-2 (Score +0.71, vorher Rank 32 Score -8.53). Keine Regressionen bei godot-001..006. 292 Tests grün (97 unit + 136 quality + 35 integration + 12 e2e + 12 mcp). Security: SAFE. Diff: APPROVE.
- Status: Fixed. godot-007 pass 0.86, SR 1.0.