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