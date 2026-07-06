# Knowledge Hub OpenCode Standard Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate `knowledge-hub` to Noahs current Single-Repo OpenCode standard with file-based agents, root onboarding, validation scripts, updated AI docs, and a Knowledge-QA-focused `test-hub-feature` agent.

**Architecture:** Keep `knowledge-hub` as one Git repository. Move inline OpenCode agents from `.opencode/opencode.json` into `.opencode/agents/*.md`, keep `.opencode/opencode.json` as thin project config, add root `AGENTS.md`, add workspace-style status/check scripts, and update docs to explain the standard workflow.

**Tech Stack:** OpenCode project config, Markdown agent files with YAML frontmatter, Bash validation helpers, Python 3.11+/pytest Knowledge Hub tests, MCP stdio server, ChromaDB/BM25 retrieval.

---

## Preconditions and Guardrails

- Worktree path: `/Users/noahk/Documents/work/knowledge-hub`.
- Do not commit unless Noah explicitly asks.
- Do not modify `domains/davinci_resolve/sources/*.md`.
- Do not modify `chromadb_data/`.
- Do not rebuild indexes.
- Do not delete existing Git data.
- Preserve user changes already present in the worktree.
- Current known dirty files before this migration:
  - `domains/davinci_resolve/sources/davinci-resolve-20-advanced-visual-effects.md`
  - `domains/davinci_resolve/sources/davinci-resolve-20-beginners-guide.md`
  - `domains/davinci_resolve/sources/davinci-resolve-20-colorist-guide.md`
  - `domains/davinci_resolve/sources/davinci-resolve-20-editors-guide.md`
  - `domains/davinci_resolve/sources/davinci-resolve-20-fairlight-audio-post.md`
  - `domains/davinci_resolve/sources/davinci-resolve-20-fusion-visual-effects.md`
  - `domains/davinci_resolve/sources/davinci-resolve-20.3-reference-manual.md`
  - `domains/davinci_resolve/sources/davinci-resolve-21-new-features-guide.md`
  - `domains/davinci_resolve/sources/fairlight-live-user-manual.md`
  - `domains/davinci_resolve/sources/fusion-20.3-manual.md`
  - untracked `.coverage`
  - untracked `.coverage.MacBookProM1MaxNoah_fritz_box.pid70554.X9DAkEjx.HNQIp837rWOh`

## Blindspot Review Updates

- 2026-06-29 blindspot review returned `PLAN UPDATE REQUIRED`.
- `.opencode/agents/` (plural) is intentionally used because OpenCode supports both `agent/` and `agents/` and Noah's current standard uses the plural form.
- Generated YAML frontmatter must quote all keys and string values so entries like `*`, `/Users/noahk/**`, bash globs, and values containing colons remain valid YAML.
- Add a prompt roundtrip check after extracting agents (see Task 3 Step 4) to confirm prompts are preserved verbatim.
- OpenCode permission order is intentional: last-match-wins, broad `"*": "ask"` first, specific allows after, dangerous denies last. Do not move the `"*"` entry to the end of a permission block.
- `workspace_check.sh` must inspect only the YAML frontmatter of agent files, not the prompt body prose, when checking task permission entries.
- For domain/source changes, `test-hub-feature` must run at least one websearch-derived real-world problem question or report `[skip: websearch unavailable]`.
- Preserve existing validation checks in `docs/ai/validation.md` and append the new validation sections; do not replace existing content.
- Do not restart OpenCode before Task 7 completes, because Task 5 references `docs/ai/security.md` which is created later in Task 7 Step 2.

## Files

- Create: `AGENTS.md`
- Create: `.opencode/agents/orchestrator-knowledge.md`
- Create: `.opencode/agents/read-hub-docs.md`
- Create: `.opencode/agents/inspect-hub-project.md`
- Create: `.opencode/agents/research-knowledge-domain.md`
- Create: `.opencode/agents/plan-hub-change.md`
- Create: `.opencode/agents/review-hub-plan-blindspots.md`
- Create: `.opencode/agents/implement-hub-change.md`
- Create: `.opencode/agents/validate-hub-project.md`
- Create: `.opencode/agents/test-hub-feature.md`
- Create: `.opencode/agents/review-hub-security.md`
- Create: `.opencode/agents/review-hub-diff.md`
- Create: `.opencode/agents/update-hub-docs.md`
- Create: `.opencode/agents/retrospect-iteration.md`
- Create: `.opencode/agents/explain-location.md`
- Modify: `.opencode/opencode.json`
- Create: `scripts/workspace_check.sh`
- Create: `scripts/workspace_status.sh`
- Create: `docs/ai/security.md`
- Create: `docs/ai/fixes.md`
- Create: `docs/ai/handoffs/.gitkeep`
- Create: `docs/superpowers/explanations/.gitkeep`
- Create: `docs/superpowers/retrospectives/.gitkeep`
- Modify: `docs/ai/README.md`
- Modify: `docs/ai/project-context.md`
- Modify: `docs/ai/validation.md`
- Modify: `docs/ai/known-issues.md`
- Modify: `docs/ai/changelog.md`
- Modify: `docs/README.md`
- Modify: `README.md`
- Modify: `.gitignore`

## Task 1: Snapshot Current OpenCode Config and Worktree

**Files:**
- Read: `.opencode/opencode.json`
- Read: `docs/ai/README.md`
- Read: `docs/testing.md`

- [ ] **Step 1: Confirm worktree status**

Run:

```bash
git status --short
```

Expected: output includes the pre-existing DaVinci source modifications and `.coverage*` files. Treat those as pre-existing user changes and do not stage or edit them.

- [ ] **Step 2: Confirm JSON syntax before migration**

Run:

```bash
python3 -m json.tool .opencode/opencode.json >/tmp/knowledge-hub-opencode-before.json
```

Expected: exit code 0. If it fails, stop and report the parse error before editing anything.

- [ ] **Step 3: List current inline agents**

Run:

```bash
python3 - <<'PY'
import json
from pathlib import Path
cfg = json.loads(Path('.opencode/opencode.json').read_text())
for name in cfg.get('agent', {}):
    print(name)
PY
```

Expected names:

```text
orchestrator-knowledge
read-hub-docs
inspect-hub-project
research-knowledge-domain
plan-hub-change
review-hub-plan-blindspots
implement-hub-change
validate-hub-project
review-hub-diff
review-hub-security
update-hub-docs
```

## Task 2: Create Root Agent Onboarding

**Files:**
- Create: `AGENTS.md`

- [ ] **Step 1: Create `AGENTS.md`**

Write exactly this structure, adapting only if a referenced file is renamed during implementation:

```markdown
# Knowledge Hub Agent Instructions

## Project Purpose

Knowledge Hub is Noahs personal, domain-agnostic knowledge system for technical tools such as Godot, DaVinci Resolve, Blender and future domains. It combines repository/documentation knowledge, PDF-derived sources, personal notes, embeddings, BM25, hybrid retrieval and an MCP server for OpenCode integration.

## AI Agent Onboarding

1. Read `docs/ai/README.md` first.
2. Read `docs/ai/project-context.md` for current project state.
3. Read `docs/ai/architecture.md` and `docs/ai/domain-model.md` before touching domains, search, indexes or MCP code.
4. Read `docs/ai/best-practices.md`, `docs/ai/validation.md` and `docs/ai/security.md` before implementing changes.
5. For feature work, read the relevant spec and plan under `docs/superpowers/`.
6. Never invent project facts, test results, index rebuilds, MCP starts, web sources, source citations or PDF page numbers.

## Workflow

Use the Knowledge Hub feedback loop:

```text
read-hub-docs -> inspect-hub-project -> research-knowledge-domain -> plan-hub-change -> review-hub-plan-blindspots -> implement-hub-change -> validate-hub-project -> test-hub-feature -> review-hub-security -> review-hub-diff -> update-hub-docs -> retrospect-iteration -> explain-location
```

`research-knowledge-domain` is required for new domains, new source collections, changed external-source strategy or quality checks that depend on web research.

## OpenCode Configuration

- Project config lives in `.opencode/opencode.json`.
- Agent prompts live in `.opencode/agents/*.md`.
- `orchestrator-knowledge` is the primary agent.
- Task permission names must match real agent filenames without `.md`.
- Do not inline large agent prompts in `.opencode/opencode.json`.

## Validation

Use:

```bash
./scripts/workspace_check.sh
./scripts/workspace_status.sh
pytest -m unit
pytest -m integration
pytest -m e2e
pytest -m mcp
```

Skip unavailable or irrelevant test stages with an explicit `[skip: <reason>]`. Never invent successful test or scan results.

## Knowledge Quality Standard

Knowledge Hub changes should improve practical retrieval quality, not only compile. For source or domain changes, quality review should check:

- relevant answers for realistic user questions
- source filename in results
- PDF page metadata when available
- clear evidence snippets
- documented gaps when retrieval is weak

For PDF-derived domains, missing page metadata must be reported as `[fail: missing page metadata]` for the affected result.

## Safety Rules

- Do not modify `chromadb_data/` unless a plan explicitly requires an index migration.
- Do not rebuild indexes unless the user approves it.
- Do not commit `.coverage*`, local caches, virtualenvs or generated ChromaDB data.
- Do not store secrets in config or personal notes.
- Do not commit without explicit user approval.
```

- [ ] **Step 2: Verify file exists**

Run:

```bash
test -f AGENTS.md
```

Expected: exit code 0.

## Task 3: Extract Existing Inline Agents into `.opencode/agents/*.md`

**Files:**
- Create directory: `.opencode/agents/`
- Create agent files listed in the Files section
- Modify later: `.opencode/opencode.json`

- [ ] **Step 0: Confirm `.opencode/agents/` (plural) directory naming**

OpenCode supports both `.opencode/agent/` and `.opencode/agents/` directory names. Noah's current standard uses the plural form `.opencode/agents/`. Use `.opencode/agents/` for all generated agent files in this migration. Document this decision later in `docs/ai/changelog.md` (Task 7 Step 8).

- [ ] **Step 1: Create `.opencode/agents` directory**

Run:

```bash
mkdir -p .opencode/agents
```

Expected: directory exists.

- [ ] **Step 2: Convert existing inline agents to Markdown files preserving prompts**

Run this conversion command from repo root:

```bash
python3 - <<'PY'
import json
from pathlib import Path

cfg_path = Path('.opencode/opencode.json')
agent_dir = Path('.opencode/agents')
agent_dir.mkdir(parents=True, exist_ok=True)
cfg = json.loads(cfg_path.read_text(encoding='utf-8'))
agents = cfg.get('agent', {})

# Quote YAML keys and string values using json.dumps(..., ensure_ascii=False) so
# entries like "*", "/Users/noahk/**", bash globs and values containing colons
# remain valid YAML. Avoids emitting bare YAML keys such as `*` or `/Users/noahk/**`.
def yaml_key(k):
    return json.dumps(str(k), ensure_ascii=False)

def yaml_scalar(value):
    if isinstance(value, bool):
        return 'true' if value else 'false'
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    raise TypeError(f'unsupported scalar type: {type(value)}')

def dump_yaml(obj, indent=0):
    lines = []
    pad = '  ' * indent
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, dict):
                lines.append(f'{pad}{yaml_key(key)}:')
                lines.extend(dump_yaml(value, indent + 1))
            else:
                lines.append(f'{pad}{yaml_key(key)}: {yaml_scalar(value)}')
    elif isinstance(obj, list):
        for item in obj:
            lines.append(f'{pad}- {yaml_scalar(item)}')
    else:
        raise TypeError(f'unsupported root type: {type(obj)}')
    return lines

for name, data in agents.items():
    prompt = data.get('prompt', '').rstrip() + '\n'
    frontmatter = {k: v for k, v in data.items() if k != 'prompt'}
    content = ['---']
    content.extend(dump_yaml(frontmatter))
    content.append('---')
    content.append('')
    content.append(prompt)
    (agent_dir / f'{name}.md').write_text('\n'.join(content), encoding='utf-8')
    print(f'wrote .opencode/agents/{name}.md')
PY
```

Expected: one file per existing inline agent. This preserves current prompts before manual standardization. All YAML keys and string values are quoted, so no bare keys like `*` or `/Users/noahk/**` are emitted.

- [ ] **Step 3: Confirm generated files**

Run:

```bash
ls .opencode/agents
```

Expected includes:

```text
orchestrator-knowledge.md
read-hub-docs.md
inspect-hub-project.md
research-knowledge-domain.md
plan-hub-change.md
review-hub-plan-blindspots.md
implement-hub-change.md
validate-hub-project.md
review-hub-diff.md
review-hub-security.md
update-hub-docs.md
```

- [ ] **Step 4: Verify prompt roundtrip**

Run this Python command from repo root. It compares each original inline JSON prompt to the body below the second `---` delimiter in the generated `.opencode/agents/<name>.md`:

```bash
python3 - <<'PY'
import json
from pathlib import Path

cfg = json.loads(Path('.opencode/opencode.json').read_text(encoding='utf-8'))
agents = cfg.get('agent', {})
ok = True
for name, data in agents.items():
    original = data.get('prompt', '').rstrip() + '\n'
    path = Path('.opencode/agents') / f'{name}.md'
    text = path.read_text(encoding='utf-8')
    parts = text.split('---')
    if len(parts) < 3:
        print(f'roundtrip FAIL {name}: missing frontmatter delimiters')
        ok = False
        continue
    body = '---'.join(parts[2:])
    # strip the single leading blank line added after frontmatter
    if body.startswith('\n'):
        body = body[1:]
    if body != original:
        print(f'roundtrip FAIL {name}: prompt body differs from original')
        ok = False
if ok:
    print('prompt roundtrip ok')
PY
```

Expected output:

```text
prompt roundtrip ok
```

If any `roundtrip FAIL` line is printed, stop and fix the conversion before proceeding to Task 4.

## Task 4: Add New Standard Agents

**Files:**
- Create: `.opencode/agents/test-hub-feature.md`
- Create: `.opencode/agents/retrospect-iteration.md`
- Create: `.opencode/agents/explain-location.md`
- Modify: `.opencode/agents/orchestrator-knowledge.md`

- [ ] **Step 1: Create `test-hub-feature.md`**

Create `.opencode/agents/test-hub-feature.md` with this content:

```markdown
---
description: Runs Knowledge Hub tests and report-only Knowledge-QA checks for source quality, citations, page metadata and realistic user problems. No edits.
mode: subagent
model: openai/gpt-5.5
steps: 45
permission:
  edit: deny
  bash:
    "*": allow
  webfetch: allow
  websearch: allow
  external_directory:
    "/Users/noahk/**": allow
    "/tmp/**": allow
    "/var/folders/**": allow
---

You are the Knowledge Hub test and Knowledge-QA reviewer. Do not edit files.

First read `docs/ai/validation.md`, `docs/testing.md`, the active plan, and relevant domain documentation. Then decide which checks apply to the current diff.

Technical test order:

1. `pytest -m unit`
2. `pytest -m integration`
3. `pytest -m e2e`
4. `pytest -m mcp`
5. `pytest --cov=scripts --cov=mcp_servers/knowledge_hub --cov-report=term-missing` only when coverage is explicitly requested or the diff changes core search/MCP code.

If a runner is unavailable, irrelevant, or prerequisites are missing, report `[skip: <reason>]`. Never invent successful test results.

Knowledge-QA order for domain/source changes:

1. Identify affected domains and changed sources.
2. Generate source-grounded questions from the affected sources. For PDF-derived sources, prefer questions whose answer can be tied to `source_file` and `page_start`/`page_end` metadata.
3. Websearch-derived real-world problem questions are mandatory for domain/source changes. Use websearch to collect realistic user problems whenever the change affects domain knowledge, retrieval quality, new sources or source parsing. Websearch is used to generate realistic questions and plausibility checks, not as an uncited replacement for the Hub sources. If websearch is unavailable, report `[skip: websearch unavailable]` and continue with the remaining checks.
4. Query the Knowledge Hub through the available MCP tools or local search scripts.
5. Evaluate whether top results are relevant, cite a source file, include PDF page metadata when available, and contain evidence text that a human can inspect.

Report Knowledge-QA findings in this exact shape:

```text
[pass|weak|fail] <short title>
Domain: <domain>
Question: <question>
Real-world source: <URL or [not used - structural diff]>
Hub source: <source_file or [missing]>
Pages: <page_start-page_end or [missing]>
Evidence: <short excerpt or precise result description>
Human follow-up: <concrete recommendation>
```

`Real-world source: [not used - structural diff]` should only be used for purely structural or non-domain diffs. For domain/source changes, a real-world source URL (or `[skip: websearch unavailable]`) is expected.

For PDF-derived domains, if an otherwise relevant result lacks page metadata, report `[fail: missing page metadata]` for that result.

Do not write new tests, new source files, new personal notes, generated questions or golden datasets. If durable quality fixtures are needed, recommend a separate plan for the Knowledge Hub Quality Evaluation Platform.
```

- [ ] **Step 2: Create `retrospect-iteration.md`**

Create `.opencode/agents/retrospect-iteration.md` with this content:

```markdown
---
description: Writes a short retrospective after a Knowledge Hub workflow iteration. Documentation edits only.
mode: subagent
model: ollama-cloud/deepseek-v4-pro
steps: 25
permission:
  edit: allow
  bash:
    "*": allow
---

Write a concise retrospective for the completed Knowledge Hub iteration under `docs/superpowers/retrospectives/YYYY-MM-DD-<topic>-retro.md`.

Include:

- Goal
- What went well
- What was surprising or difficult
- Concrete lessons learned
- What to do differently next time
- Follow-up candidates
- Uncertainties
- References to the spec, plan and explanation

Document only verified facts. Do not invent test results, index rebuilds, MCP starts, security scan results, source quality findings or commits.
```

- [ ] **Step 3: Create `explain-location.md`**

Create `.opencode/agents/explain-location.md` with this content:

```markdown
---
description: Explains where Knowledge Hub files, docs, agents, scripts and validation commands live after a change. Documentation edits only.
mode: subagent
model: ollama-cloud/deepseek-v4-pro
steps: 25
permission:
  edit: allow
  bash:
    "*": allow
---

Create a location explanation under `docs/superpowers/explanations/YYYY-MM-DD-<topic>-location.md`.

Include:

- What changed
- Where the relevant files live
- How OpenCode is configured
- How the workflow agents are organized
- Which validation commands to run
- How Knowledge-QA works for source/domain changes
- Verified facts versus `[unverified]` notes
- Next steps for Noah

Keep the explanation beginner-friendly and concrete. Do not invent paths, command outputs, test results or source-quality findings.
```

- [ ] **Step 4: Update `orchestrator-knowledge.md` workflow references**

Modify `.opencode/agents/orchestrator-knowledge.md` so its prompt includes `test-hub-feature`, `retrospect-iteration` and `explain-location` in the workflow after `validate-hub-project`, `update-hub-docs`, and final explanation.

The orchestrator task permission block must include these entries, with the broad deny before specific allows:

```yaml
permission:
  task:
    "*": deny
    read-hub-docs: allow
    inspect-hub-project: allow
    research-knowledge-domain: allow
    plan-hub-change: allow
    review-hub-plan-blindspots: allow
    implement-hub-change: allow
    validate-hub-project: allow
    test-hub-feature: allow
    review-hub-security: allow
    review-hub-diff: allow
    update-hub-docs: allow
    retrospect-iteration: allow
    explain-location: allow
```

Expected: no abbreviated task names are present.

## Task 5: Slim `.opencode/opencode.json`

**Files:**
- Modify: `.opencode/opencode.json`

- [ ] **Step 1: Remove inline `agent` block**

Rewrite `.opencode/opencode.json` so it keeps project config and MCP config but removes the top-level `agent` object. Preserve these existing fields:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "default_agent": "orchestrator-knowledge",
  "model": "openai/gpt-5.5",
  "small_model": "openai/gpt-5.5",
  "compaction": {
    "auto": true,
    "prune": true,
    "reserved": 10000
  },
  "instructions": [
    "AGENTS.md",
    "docs/ai/README.md",
    "docs/ai/project-context.md",
    "docs/ai/architecture.md",
    "docs/ai/domain-model.md",
    "docs/ai/best-practices.md",
    "docs/ai/known-issues.md",
    "docs/ai/validation.md",
    "docs/ai/security.md"
  ],
  "mcp": {
    "knowledge_hub": {
      "type": "local",
      "command": ["python3", "-m", "mcp_servers.knowledge_hub.server"],
      "enabled": true
    }
  },
  "permission": {
    "bash": {
      "*": "ask",
      "git status*": "allow",
      "git diff*": "allow",
      "git log*": "allow",
      "python3 -m json.tool *": "allow",
      "bash -n *": "allow",
      "pytest*": "ask",
      "./scripts/workspace_check.sh*": "allow",
      "./scripts/workspace_status.sh*": "allow",
      "rm *": "deny",
      "rm -rf *": "deny",
      "git push*": "deny",
      "git reset --hard*": "deny"
    },
    "skill": "allow",
    "task": "allow"
  }
}
```

Note: if OpenCode schema validation shows that the existing MCP environment key shape must be preserved or changed, follow the schema and document the decision in `docs/ai/changelog.md`.

**Permission order note:** The `permission.bash` block ordering is intentional. OpenCode uses last-match-wins semantics for permission rules: the broad `"*": "ask"` entry is listed first, specific allow entries (such as `git status*`, `python3 -m json.tool *`, `./scripts/workspace_check.sh*`) come after it, and dangerous deny entries (`rm *`, `rm -rf *`, `git push*`, `git reset --hard*`) are placed last so they always win. Do not move the `"*"` entry to the end of the block, or the specific allows would be shadowed and the dangerous denies would stop being the final match.

**Restart warning:** Do not restart OpenCode after this task. Task 5's `instructions` list references `docs/ai/security.md`, which is not created until Task 7 Step 2. Restarting OpenCode now would load a config that points at a missing file. Wait until Task 7 completes before restarting OpenCode.

- [ ] **Step 2: Validate JSON syntax**

Run:

```bash
python3 -m json.tool .opencode/opencode.json >/tmp/knowledge-hub-opencode-after.json
```

Expected: exit code 0.

- [ ] **Step 3: Confirm inline agents removed**

Run:

```bash
python3 - <<'PY'
import json
from pathlib import Path
cfg = json.loads(Path('.opencode/opencode.json').read_text())
print('agent' in cfg)
PY
```

Expected:

```text
False
```

## Task 6: Add Workspace Status and Check Scripts

**Files:**
- Create: `scripts/workspace_check.sh`
- Create: `scripts/workspace_status.sh`

- [ ] **Step 1: Create `scripts/workspace_status.sh`**

Write `scripts/workspace_status.sh` using the exact body in **Appendix A: workspace_status.sh**.

- [ ] **Step 2: Create `scripts/workspace_check.sh`**

Write `scripts/workspace_check.sh` using the exact body in **Appendix B: workspace_check.sh**. It must fail on missing standard files, invalid JSON, Bash syntax errors, missing agents, inline agents in `.opencode/opencode.json`, and task permissions that reference missing agent files.

The script must include checks for:

```text
AGENTS.md
.opencode/opencode.json
.opencode/agents/orchestrator-knowledge.md
.opencode/agents/test-hub-feature.md
docs/ai/security.md
docs/ai/fixes.md
docs/ai/handoffs/.gitkeep
docs/superpowers/explanations/.gitkeep
docs/superpowers/retrospectives/.gitkeep
```

It must run:

```bash
python3 -m json.tool .opencode/opencode.json >/dev/null
bash -n scripts/workspace_check.sh
bash -n scripts/workspace_status.sh
```

It must check that `.opencode/opencode.json` has no top-level `agent` key.

It must check that every `permission.task` allow in `orchestrator-knowledge.md` references an existing `.opencode/agents/<name>.md` file or is a deliberate wildcard. The parser must inspect only the YAML frontmatter (between the first two `---` delimiters) of `orchestrator-knowledge.md`, not the prompt body prose, to avoid false matches in prose. If parsing cannot be done robustly, fail closed with a clear message.

- [ ] **Step 3: Make scripts executable**

Run:

```bash
chmod +x scripts/workspace_check.sh scripts/workspace_status.sh
```

- [ ] **Step 4: Validate Bash syntax**

Run:

```bash
bash -n scripts/workspace_check.sh
bash -n scripts/workspace_status.sh
```

Expected: both exit code 0.

## Task 7: Complete AI Documentation Tree

**Files:**
- Create: `docs/ai/security.md`
- Create: `docs/ai/fixes.md`
- Create: `docs/ai/handoffs/.gitkeep`
- Modify: `docs/ai/README.md`
- Modify: `docs/ai/project-context.md`
- Modify: `docs/ai/validation.md`
- Modify: `docs/ai/known-issues.md`
- Modify: `docs/ai/changelog.md`

- [ ] **Step 1: Create missing directories and keep files**

Run:

```bash
mkdir -p docs/ai/handoffs docs/superpowers/explanations docs/superpowers/retrospectives
touch docs/ai/handoffs/.gitkeep docs/superpowers/explanations/.gitkeep docs/superpowers/retrospectives/.gitkeep
```

Expected: directories and `.gitkeep` files exist.

- [ ] **Step 2: Create `docs/ai/security.md`**

Write `docs/ai/security.md` using the exact content in **Appendix C: docs/ai/security.md**.

- [ ] **Step 3: Create `docs/ai/fixes.md`**

Write `docs/ai/fixes.md` using the exact content in **Appendix D: docs/ai/fixes.md**.

- [ ] **Step 4: Update `docs/ai/README.md` file list**

Update `docs/ai/README.md` so its file list includes these exact entries: `fixes.md` — completed fixes for future agents; `security.md` — security review baseline; `changelog.md` — AI-visible project changes; `handoffs/` — handoff notes for future sessions.

Preserve existing `docs/ai/README.md` entries and append the new entries; do not remove or rewrite existing file-list rows.

- [ ] **Step 5: Update `docs/ai/project-context.md`**

Add the exact project-context section from **Appendix E: Project Context Update**.

- [ ] **Step 6: Update `docs/ai/validation.md`**

Add the exact validation sections from **Appendix F: Validation Update**.

Preserve existing `docs/ai/validation.md` content, including any existing MCP quick-test, domain status, and GitHub Action checks. Append the new validation sections rather than replacing existing ones.

- [ ] **Step 7: Update `docs/ai/known-issues.md`**

Replace the stale `Keine Test-Suite` item with a note that the durable Golden Dataset for Knowledge-QA is deferred to a separate future feature.

- [ ] **Step 8: Update `docs/ai/changelog.md`**

Add the exact changelog entry from **Appendix G: Changelog Entry**.

## Task 8: Update Human-Facing Docs

**Files:**
- Modify: `docs/README.md`
- Modify: `README.md`
- Modify: `.gitignore`

- [ ] **Step 1: Update `docs/README.md` areas**

Update `docs/README.md` with the exact documentation area rows from **Appendix H: docs/README.md Rows**.

- [ ] **Step 2: Update `README.md` AI section**

Replace the README AI section with the exact text in **Appendix I: README AI Section**.

- [ ] **Step 3: Ensure `.coverage*` is ignored**

Add these lines to `.gitignore` if not already present:

```gitignore
.coverage
.coverage.*
htmlcov/
```

Do not delete existing `.coverage*` files in this migration unless Noah explicitly asks.

## Task 9: Validate Structure and Tests

**Files:**
- Read: all changed files

- [ ] **Step 1: Run workspace status**

Run:

```bash
./scripts/workspace_status.sh
```

Expected: status prints root, git status, OpenCode config, agent count, docs and tests.

- [ ] **Step 2: Run workspace check**

Run:

```bash
./scripts/workspace_check.sh
```

Expected: PASS. If it fails, fix only migration-owned files.

- [ ] **Step 3: Validate JSON**

Run:

```bash
python3 -m json.tool .opencode/opencode.json >/dev/null
```

Expected: exit code 0.

- [ ] **Step 4: Validate Bash syntax**

Run:

```bash
bash -n scripts/workspace_check.sh
bash -n scripts/workspace_status.sh
```

Expected: exit code 0.

- [ ] **Step 5: Run fast test stage**

Run:

```bash
pytest -m unit
```

Expected: pass or report exact failures. Do not invent results.

- [ ] **Step 6: Decide heavier tests based on time and environment**

Run when environment permits:

```bash
pytest -m integration
pytest -m e2e
pytest -m mcp
```

Expected: pass, fail with exact output, or `[skip: reason]` if prerequisites are unavailable.

## Task 10: Review Diff and Protect Pre-Existing Changes

**Files:**
- Read: `git diff`
- Read: `git status --short`

- [ ] **Step 1: Inspect diff**

Run:

```bash
git diff -- . ':!domains/davinci_resolve/sources/*'
```

Expected: diff only includes migration-owned files.

- [ ] **Step 2: Confirm DaVinci source files were not modified by migration**

Run:

```bash
git diff --name-only -- domains/davinci_resolve/sources
```

Expected: the same pre-existing source files may be listed, but this migration must not add additional changes to them. If uncertain, stop and ask Noah.

- [ ] **Step 3: Confirm no generated index data is staged or changed**

Run:

```bash
git status --short -- chromadb_data
```

Expected: no migration changes.

## Task 11: Documentation Closure

**Files:**
- Create: `docs/superpowers/retrospectives/2026-06-29-knowledge-hub-opencode-standard-migration-retro.md`
- Create: `docs/superpowers/explanations/2026-06-29-knowledge-hub-opencode-standard-migration-location.md`
- Modify: `docs/ai/fixes.md`
- Modify: `docs/ai/changelog.md`

- [ ] **Step 1: Write retrospective after implementation**

Create a concise retrospective with verified facts from the implementation.

- [ ] **Step 2: Write location explanation**

Create a beginner-friendly explanation covering what changed, OpenCode config, agents, validation, Knowledge-QA, verified facts, and next steps.

- [ ] **Step 3: Update fixes and changelog from planned to completed**

In `docs/ai/fixes.md`, change the migration status from `Planned` to the actual result and include commands actually run. In `docs/ai/changelog.md`, add implementation results and validation outcomes that actually happened.

## Task 12: Final User Handoff

**Files:**
- Read: `git status --short`

- [ ] **Step 1: Final status**

Run:

```bash
git status --short
```

Expected: migration files are modified/created; pre-existing DaVinci source and `.coverage*` entries may still appear.

- [ ] **Step 2: Tell Noah to restart OpenCode**

Final response must include:

```text
Because `.opencode/opencode.json` and `.opencode/agents/*.md` changed, quit and restart OpenCode so the new agent config is loaded.
```

- [ ] **Step 3: Offer next phase**

Offer two next steps:

1. Execute this migration plan now.
2. Plan Ansatz C as separate `Knowledge Hub Quality Evaluation Platform` feature.
```


## Appendix A: `scripts/workspace_status.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"

printf 'Knowledge Hub workspace status\n'
printf 'Root: %s\n' "${ROOT}"

printf '\nGit status:\n'
git status --short || true

printf '\nOpenCode:\n'
if [ -f .opencode/opencode.json ]; then
  printf 'config=yes .opencode/opencode.json\n'
else
  printf 'config=no .opencode/opencode.json\n'
fi
if [ -d .opencode/agents ]; then
  count="$(find .opencode/agents -maxdepth 1 -name '*.md' | wc -l | tr -d ' ')"
  printf 'agents=%s .opencode/agents\n' "${count}"
else
  printf 'agents=0 .opencode/agents missing\n'
fi

printf '\nAI docs:\n'
for f in docs/ai/README.md docs/ai/project-context.md docs/ai/architecture.md docs/ai/domain-model.md docs/ai/best-practices.md docs/ai/validation.md docs/ai/security.md docs/ai/fixes.md docs/ai/changelog.md; do
  if [ -f "${f}" ]; then
    printf 'yes %s\n' "${f}"
  else
    printf 'no  %s\n' "${f}"
  fi
done

printf '\nSuperpowers docs:\n'
for d in docs/superpowers/specs docs/superpowers/plans docs/superpowers/explanations docs/superpowers/retrospectives; do
  if [ -d "${d}" ]; then
    printf 'yes %s\n' "${d}"
  else
    printf 'no  %s\n' "${d}"
  fi
done

printf '\nTests:\n'
for d in tests/unit tests/integration tests/e2e tests/mcp; do
  if [ -d "${d}" ]; then
    printf 'yes %s\n' "${d}"
  else
    printf 'no  %s\n' "${d}"
  fi
done
```

## Appendix B: `scripts/workspace_check.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"

failures=0

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  failures=$((failures + 1))
}

pass() {
  printf 'PASS: %s\n' "$1"
}

require_file() {
  if [ -f "$1" ]; then
    pass "file exists: $1"
  else
    fail "missing file: $1"
  fi
}

require_dir() {
  if [ -d "$1" ]; then
    pass "directory exists: $1"
  else
    fail "missing directory: $1"
  fi
}

required_files=(
  "AGENTS.md"
  ".opencode/opencode.json"
  ".opencode/agents/orchestrator-knowledge.md"
  ".opencode/agents/read-hub-docs.md"
  ".opencode/agents/inspect-hub-project.md"
  ".opencode/agents/research-knowledge-domain.md"
  ".opencode/agents/plan-hub-change.md"
  ".opencode/agents/review-hub-plan-blindspots.md"
  ".opencode/agents/implement-hub-change.md"
  ".opencode/agents/validate-hub-project.md"
  ".opencode/agents/test-hub-feature.md"
  ".opencode/agents/review-hub-security.md"
  ".opencode/agents/review-hub-diff.md"
  ".opencode/agents/update-hub-docs.md"
  ".opencode/agents/retrospect-iteration.md"
  ".opencode/agents/explain-location.md"
  "docs/ai/security.md"
  "docs/ai/fixes.md"
  "docs/ai/handoffs/.gitkeep"
  "docs/superpowers/explanations/.gitkeep"
  "docs/superpowers/retrospectives/.gitkeep"
)

required_dirs=(
  ".opencode/agents"
  "docs/ai"
  "docs/superpowers/specs"
  "docs/superpowers/plans"
  "docs/superpowers/explanations"
  "docs/superpowers/retrospectives"
  "tests/unit"
  "tests/integration"
  "tests/e2e"
  "tests/mcp"
)

for file in "${required_files[@]}"; do
  require_file "${file}"
done

for dir in "${required_dirs[@]}"; do
  require_dir "${dir}"
done

if python3 -m json.tool .opencode/opencode.json >/dev/null; then
  pass "opencode JSON syntax"
else
  fail "opencode JSON syntax"
fi

if bash -n scripts/workspace_status.sh; then
  pass "workspace_status.sh bash syntax"
else
  fail "workspace_status.sh bash syntax"
fi

if bash -n scripts/workspace_check.sh; then
  pass "workspace_check.sh bash syntax"
else
  fail "workspace_check.sh bash syntax"
fi

if python3 - <<'PY'
import json, sys
from pathlib import Path
cfg = json.loads(Path('.opencode/opencode.json').read_text())
if 'agent' in cfg:
    print('inline agent block still present in .opencode/opencode.json')
    sys.exit(1)
PY
then
  pass "no inline agent block in .opencode/opencode.json"
else
  fail "inline agent block removed"
fi

if python3 - <<'PY'
from pathlib import Path
import re

agent_dir = Path('.opencode/agents')
orch = agent_dir / 'orchestrator-knowledge.md'
raw = orch.read_text(encoding='utf-8') if orch.exists() else ''

# Parse only the YAML frontmatter (between the first two '---' delimiters).
# Do not search the prompt body prose for task permission entries.
frontmatter = ''
if raw.startswith('---'):
    parts = raw.split('---', 2)
    if len(parts) >= 3:
        frontmatter = parts[1]
    else:
        raise SystemExit('orchestrator-knowledge.md: frontmatter delimiters missing')

required = [
    'read-hub-docs',
    'inspect-hub-project',
    'research-knowledge-domain',
    'plan-hub-change',
    'review-hub-plan-blindspots',
    'implement-hub-change',
    'validate-hub-project',
    'test-hub-feature',
    'review-hub-security',
    'review-hub-diff',
    'update-hub-docs',
    'retrospect-iteration',
    'explain-location',
]
missing = [name for name in required if not (agent_dir / f'{name}.md').exists()]
# Check required allow entries only within the frontmatter.
not_allowed = [name for name in required if not re.search(rf'(^|\n)\s*"?{re.escape(name)}"?:\s*allow\b', frontmatter)]
# Check abbreviated allow entries only within the frontmatter.
abbreviated_names = ['plan', 'review', 'docs', 'inspect', 'implement', 'validate', 'explain']
abbreviated = [name for name in abbreviated_names if re.search(rf'(^|\n)\s*"?{re.escape(name)}"?:\s*allow\b', frontmatter)]
if missing:
    raise SystemExit(f'missing agent files: {missing}')
if not_allowed:
    raise SystemExit(f'orchestrator task permissions missing allows: {not_allowed}')
if abbreviated:
    raise SystemExit(f'abbreviated task permission names are forbidden: {abbreviated}')
PY
then
  pass "orchestrator task permissions match agent files"
else
  fail "orchestrator task permissions"
fi

if [ "${failures}" -eq 0 ]; then
  printf '\nAll workspace checks passed.\n'
else
  printf '\nWorkspace checks failed: %s\n' "${failures}" >&2
  exit 1
fi
```

## Appendix C: `docs/ai/security.md`

````markdown
# Security — Knowledge Hub

## Baseline

- No secrets, API keys or tokens in tracked files.
- Use environment variables for credentials.
- Do not index private data accidentally through `domains/*/sources/` or `personal/`.
- Treat external source ingestion as untrusted until reviewed.
- Avoid unsafe shell patterns and always quote paths.
- MCP server is stdio-oriented for local OpenCode use; do not expose it publicly without a separate security plan.

## Dependency and License Checks

- Review `requirements.txt`, `requirements-dev.txt`, `requirements-pdf.txt` and `THIRD_PARTY_LICENSES.md` when dependencies change.
- Keep the PyMuPDF4LLM AGPL process-boundary decision documented in `docs/decisions/2026-06-27-agpl-process-boundary.md`.

## Known Accepted Risk

BM25 indexes use Python pickle through `rank_bm25` serialization. This is accepted for Noahs personal local Hub where index files are generated locally and not consumed from untrusted sources. A shared or production Hub would need a safer serialization format.

## Review Commands

```bash
git status --short
python3 -m json.tool .opencode/opencode.json
find . -name "*.py" -not -path "*/__pycache__/*" -exec python3 -m py_compile {} \;
find . -name "*.sh" -exec bash -n {} \;
```

If secret scanners such as `gitleaks` or SAST tools such as `semgrep` are installed, run them for security-sensitive changes and report exact findings. If unavailable, report `[skip: tool not installed]`.
````

## Appendix D: `docs/ai/fixes.md`

````markdown
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

- Problem: Migration planned; implementation details are tracked in `docs/superpowers/plans/2026-06-29-knowledge-hub-opencode-standard-migration.md`.
- Fix: Pending implementation.
- Validation: Pending implementation.
- Status: Planned.
````

## Appendix E: Project Context Update

```markdown
## Update 2026-06-29: OpenCode Standard Migration Planned

- Knowledge Hub remains a Single-Repo project.
- OpenCode agent prompts are being migrated from inline `.opencode/opencode.json` definitions to `.opencode/agents/*.md` files.
- `test-hub-feature` is planned as a combined pytest + Knowledge-QA report-only agent.
- Ansatz C, a durable Knowledge Quality Evaluation Platform with Golden Dataset and quality reports, is intentionally deferred to a separate future feature.
```

## Appendix F: Validation Update

````markdown
## Structure Validation

```bash
./scripts/workspace_check.sh
./scripts/workspace_status.sh
python3 -m json.tool .opencode/opencode.json
bash -n scripts/workspace_check.sh scripts/workspace_status.sh
```

## Test Suite

```bash
pytest -m unit
pytest -m integration
pytest -m e2e
pytest -m mcp
pytest --cov=scripts --cov=mcp_servers/knowledge_hub --cov-report=term-missing
```

## Knowledge-QA Checklist

For domain/source changes, `test-hub-feature` checks:

- realistic questions from changed sources
- real-world problem prompts from websearch for domain/source changes
- relevant top search results
- `source_file` present
- PDF `page_start`/`page_end` present when available
- evidence snippets human can inspect
- weak or missing coverage documented as findings
````

## Appendix G: Changelog Entry

```markdown
## 2026-06-29

- **docs:** Planned Single-Repo OpenCode standard migration.
- **docs:** Added Knowledge-QA responsibilities for `test-hub-feature`.
- **docs:** Deferred durable Golden Dataset / Quality Evaluation Platform to a separate future feature.
```

## Appendix H: `docs/README.md` Rows

```markdown
| `AGENTS.md` | Root onboarding and workflow rules for AI agents |
| `.opencode/agents/` | File-based OpenCode agent prompts |
| `scripts/workspace_check.sh` | Structural validation for OpenCode/docs/test layout |
| `scripts/workspace_status.sh` | Human-readable workspace status summary |
| `docs/ai/security.md` | Security baseline and review commands |
| `docs/ai/fixes.md` | Completed fixes and future-agent notes |
| `docs/superpowers/explanations/` | Beginner-friendly location guides after changes |
| `docs/superpowers/retrospectives/` | Retrospectives after workflow iterations |
```

## Appendix I: README AI Section

```markdown
## Für AI-Agenten

Starte mit `AGENTS.md`. Danach liest du `docs/ai/README.md`, `docs/ai/project-context.md`, `docs/ai/architecture.md`, `docs/ai/domain-model.md`, `docs/ai/validation.md` und `docs/ai/security.md`.

OpenCode-Projektkonfiguration liegt in `.opencode/opencode.json`; Agentenprompts liegen in `.opencode/agents/*.md`.
```
