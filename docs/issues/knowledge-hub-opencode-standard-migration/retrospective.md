# Knowledge Hub OpenCode Standard Migration Retrospective

## Goal
Migrate knowledge-hub from inline OpenCode agents in .opencode/opencode.json to file-based .opencode/agents/*.md, add AGENTS.md root onboarding, workspace validation scripts, complete the docs/ai/ tree, and add a Knowledge-QA-focused test-hub-feature agent.

## What went well
- All 11 existing inline agents extracted to .opencode/agents/*.md with prompt roundtrip verification (prompt roundtrip ok)
- 3 new standard agents created (test-hub-feature, retrospect-iteration, explain-location)
- .opencode/opencode.json slimmed: inline agent block removed, JSON valid, no top-level agent key
- .opencode/.gitignore fixed to track agents/ directory (was ignoring all files except .gitignore and opencode.json)
- workspace_check.sh PASS (all 14 agent files, all required dirs, JSON syntax, bash syntax, no inline agents, orchestrator task permissions match agent files)
- workspace_status.sh reports correct state (14 agents, all AI docs present, all test dirs present)
- 78 unit tests pass (pytest -m unit, 3.79s)
- DaVinci source files and chromadb_data untouched by migration
- Blindspot review caught YAML quoting issue, permission parser frontmatter-only requirement, and .gitignore tracking gap before implementation

## What was surprising or difficult
- .opencode/.gitignore had a blanket `*` ignore that hid all agent files from git; without the blindspot review this would have meant agents exist on disk but are not version-controlled
- workspace_check.sh permission parser initially failed because frontmatter values are quoted ("allow" not allow) and the regex needed (?m) multiline flag; required two iterations to fix
- The plan's conversion script had an edge case where content.append('') added an extra blank line that broke the roundtrip check; the implementer correctly deviated to satisfy the roundtrip requirement

## Lessons learned
- Always check .gitignore in .opencode/ before assuming new files are tracked
- YAML frontmatter quoting (json.dumps style) is mandatory for OpenCode agent files with bash globs and external_directory paths
- Permission parsers must use (?m) multiline flag and handle quoted values
- Prompt roundtrip checks catch conversion bugs early

## What to do differently next time
- Add a .gitignore audit step to the initial snapshot task, not as a surprise during Task 5
- Include the (?m) flag and quoted-value handling in the plan's workspace_check.sh template from the start

## Follow-up candidates
- Ansatz C: Knowledge Hub Quality Evaluation Platform (Golden Dataset, scoring, reports) — separate feature
- Run pytest -m integration, pytest -m e2e, pytest -m mcp after OpenCode restart to confirm full test suite
- Consider adding gitleaks/semgrep to security review when tools are installed

## Uncertainties
- Integration/e2e/mcp tests not run in this migration (only unit tests run to avoid touching chromadb_data and .coverage*)
- OpenCode not restarted yet (deferred to user); new agent config only active after restart

## References
- Spec: docs/superpowers/specs/2026-06-29-knowledge-hub-opencode-standard-migration-design.md
- Plan: docs/superpowers/plans/2026-06-29-knowledge-hub-opencode-standard-migration.md
- Explanation: docs/superpowers/explanations/2026-06-29-knowledge-hub-opencode-standard-migration-location.md