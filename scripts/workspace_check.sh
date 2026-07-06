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
  "docs/ai/open-work.md"
  "docs/issues/.gitkeep"
)

required_dirs=(
  ".opencode/agents"
  "docs/ai"
  "docs/issues"
  "tests/unit"
  "tests/integration"
  "tests/e2e"
  "tests/mcp"
  "tests/quality"
  "quality/golden"
  "scripts/quality"
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
not_allowed = [name for name in required if not re.search(rf'(?m)^\s*"?{re.escape(name)}"?:\s*"?allow"?\s*$', frontmatter)]
# Check abbreviated allow entries only within the frontmatter.
abbreviated_names = ['plan', 'review', 'docs', 'inspect', 'implement', 'validate', 'explain']
abbreviated = [name for name in abbreviated_names if re.search(rf'(?m)^\s*"?{re.escape(name)}"?:\s*"?allow"?\s*$', frontmatter)]
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