# Knowledge Hub OpenCode Standard Migration Location Guide

## What changed
The Knowledge Hub was migrated to Noahs current Single-Repo OpenCode standard. Inline agents were moved from .opencode/opencode.json to .opencode/agents/*.md. Root AGENTS.md onboarding, workspace validation scripts, security/fixes docs, and a Knowledge-QA test agent were added.

## Workspace layout

```
knowledge-hub/
├── AGENTS.md                          # Root agent onboarding (NEW)
├── .opencode/
│   ├── opencode.json                  # Slim project config (MODIFIED)
│   ├── .gitignore                     # Fixed to track agents/ (MODIFIED)
│   └── agents/                        # File-based agents (NEW)
│       ├── orchestrator-knowledge.md
│       ├── read-hub-docs.md
│       ├── inspect-hub-project.md
│       ├── research-knowledge-domain.md
│       ├── plan-hub-change.md
│       ├── review-hub-plan-blindspots.md
│       ├── implement-hub-change.md
│       ├── validate-hub-project.md
│       ├── test-hub-feature.md        # NEW: pytest + Knowledge-QA
│       ├── review-hub-security.md
│       ├── review-hub-diff.md
│       ├── update-hub-docs.md
│       ├── retrospect-iteration.md    # NEW
│       └── explain-location.md        # NEW
├── scripts/
│   ├── workspace_check.sh             # NEW: structural validation
│   └── workspace_status.sh           # NEW: status summary
└── docs/
    ├── ai/
    │   ├── README.md                   # MODIFIED: added fixes/security/changelog/handoffs
    │   ├── project-context.md         # MODIFIED: added 2026-06-29 section
    │   ├── validation.md              # MODIFIED: appended structure/test/Knowledge-QA sections
    │   ├── known-issues.md            # MODIFIED: replaced stale test-suite note
    │   ├── changelog.md               # MODIFIED: added 2026-06-29 entry
    │   ├── security.md                # NEW
    │   ├── fixes.md                    # NEW
    │   └── handoffs/.gitkeep           # NEW
    ├── superpowers/
    │   ├── explanations/.gitkeep      # NEW
    │   └── retrospectives/.gitkeep    # NEW
    ├── README.md                      # MODIFIED: added documentation area rows
└── README.md                          # MODIFIED: replaced AI section
```

## Where OpenCode config lives
- `.opencode/opencode.json` — project config: model, default_agent, instructions, mcp, permission
- `.opencode/agents/*.md` — agent prompts with YAML frontmatter (description, mode, model, steps, permission)

## Where agents live
`.opencode/agents/` contains 14 agent files. The primary agent is `orchestrator-knowledge`. Task permissions in orchestrator-knowledge.md use full agent filenames (no abbreviations).

## Where validation lives
- `scripts/workspace_check.sh` — structural validation (files, dirs, JSON, bash syntax, agent permissions)
- `scripts/workspace_status.sh` — human-readable status summary
- `docs/ai/validation.md` — validation docs (structure, tests, Knowledge-QA checklist)
- `docs/testing.md` — test suite usage and layers

## How Knowledge-QA works
The test-hub-feature agent runs pytest (unit/integration/e2e/mcp) and performs report-only Knowledge-QA for domain/source changes. For domain/source changes, websearch-derived real-world problem questions are mandatory. Findings include source_file, page_start/page_end for PDF domains, and evidence snippets.

## How to run checks

```bash
./scripts/workspace_check.sh    # must exit 0
./scripts/workspace_status.sh   # status summary
python3 -m json.tool .opencode/opencode.json >/dev/null
bash -n scripts/workspace_check.sh scripts/workspace_status.sh
.venv/bin/python -m pytest -m unit
```

## Verified facts
- workspace_check.sh: PASS (exit 0)
- 78 unit tests pass (3.79s)
- .opencode/opencode.json: valid JSON, no inline agent block
- 14 agent files in .opencode/agents/
- prompt roundtrip: ok
- .opencode/.gitignore: agents/ tracked, node_modules still ignored

## [unverified] notes
- Integration/e2e/mcp tests not run in this migration session
- OpenCode not restarted yet; new agent config active only after restart
- gitleaks/semgrep availability not checked

## Next steps
1. Quit and restart OpenCode so the new agent config is loaded.
2. Run pytest -m integration, pytest -m e2e, pytest -m mcp to confirm full test suite.
3. Plan Ansatz C (Knowledge Hub Quality Evaluation Platform) as a separate feature.
4. Commit the migration when ready.