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