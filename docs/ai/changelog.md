# AI Changelog

## 2026-06-27

- **feat:** Per-Domain ChromaDB-Isolation (eigene DB pro Domain)
- **feat:** Domain-Scoped MCP-Server (`--domains` CLI-Flag)
- **feat:** Central Model Manager (lazy loading, LRU cache, unload)
- **feat:** PDF → Markdown Build-Script (PyMuPDF4LLM, AGPL Process Boundary)
- **feat:** DaVinci Resolve Domain (10 Blackmagic PDF-Quellen)
- **feat:** Search regression validation script
- **feat:** Automatic legacy layout migration with backup
- **docs:** THIRD_PARTY_LICENSES.md, ADRs for isolation + AGPL boundary
- **refactor:** All search modules use model_manager instead of direct
  SentenceTransformer/CrossEncoder instantiation

## 2026-06-29

- **docs:** Planned Single-Repo OpenCode standard migration.
- **docs:** Added Knowledge-QA responsibilities for `test-hub-feature`.
- **docs:** Deferred durable Golden Dataset / Quality Evaluation Platform to a separate future feature.
- **feat:** Migrated 11 inline OpenCode agents from `.opencode/opencode.json` to `.opencode/agents/*.md` (prompt roundtrip verified).
- **feat:** Added 3 new agents: `test-hub-feature` (pytest + report-only Knowledge-QA), `retrospect-iteration`, `explain-location`.
- **refactor:** Slimmed `.opencode/opencode.json`: removed inline `agent` block; kept `default_agent: orchestrator-knowledge`; added `AGENTS.md` and `docs/ai/security.md` to `instructions`.
- **feat:** Added root `AGENTS.md` agent onboarding (project purpose, onboarding order, workflow, validation, Knowledge Quality standard, safety rules).
- **feat:** Added `scripts/workspace_check.sh` (structural validation: required files/dirs, JSON syntax, bash syntax, no inline agents, orchestrator task-permission match against agent filenames) and `scripts/workspace_status.sh` (status summary).
- **feat:** Added `docs/ai/security.md`, `docs/ai/fixes.md`, `docs/ai/handoffs/.gitkeep`, `docs/superpowers/explanations/.gitkeep`, `docs/superpowers/retrospectives/.gitkeep`.
- **fix:** `.opencode/.gitignore` now tracks `agents/` and `agents/**` (previously blanket-ignored everything except `.gitignore` and `opencode.json`).
- **fix:** `.gitignore` now ignores `.coverage`, `.coverage.*`, `htmlcov/`.
- **docs:** Updated `docs/ai/README.md` (added `fixes.md`, `security.md`, `changelog.md`, `handoffs/` rows), `docs/ai/project-context.md` (2026-06-29 migration section), `docs/ai/validation.md` (appended Structure Validation, Test Suite, Knowledge-QA Checklist sections), `docs/ai/known-issues.md` (replaced stale "Keine Test-Suite" note with deferred Golden Dataset note), `docs/README.md` (added documentation area rows), `README.md` (replaced AI section).
- **docs:** Added retrospective `docs/superpowers/retrospectives/2026-06-29-knowledge-hub-opencode-standard-migration-retro.md` and location explanation `docs/superpowers/explanations/2026-06-29-knowledge-hub-opencode-standard-migration-location.md`.
- **validation:** `./scripts/workspace_check.sh` PASS (exit 0); `python3 -m json.tool .opencode/opencode.json` OK; `bash -n` on both scripts OK; `.venv/bin/python -m pytest -m unit` → 78 passed, 59 deselected (3.79s). Integration/e2e/mcp tests deferred until after OpenCode restart.
- **safety:** `domains/davinci_resolve/sources/*.md` and `chromadb_data/` not modified by the migration; pre-existing user changes preserved.