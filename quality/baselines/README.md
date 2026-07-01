# Quality Baselines

This directory stores the latest quality-evaluation baselines used by the
CI Quality Regression Gate (`.github/workflows/quality-gate.yml`).

## Update Protocol (Decision 2.4)

Baselines are updated **manually** by Noah after a successful iteration
that improves or stabilizes the composite scores. There is **no automatic
update** — this prevents score-creep where a slow decline is masked by
each new weak result becoming the new baseline.

## When to update

After a code/content change that has been:
1. Validated locally (`pytest -m unit/integration/quality/e2e/mcp` green).
2. Re-evaluated (`python scripts/quality/run_evaluation.py --domain <d>`).
3. Confirmed not to regress below `baseline.avg_composite - 0.1` AND not
   to drop any single question from `pass` to `weak` or `fail`.

If both conditions hold, copy the new evaluation output here:

```bash
cp /tmp/<domain>-<iteration>.json quality/baselines/<domain>-latest.json
git add quality/baselines/<domain>-latest.json
git commit -m "chore(quality): update <domain> baseline after <iteration>"
```

## Regression Gate (CI)

The Quality Gate workflow compares the current run against
`<domain>-latest.json` via `scripts/quality/run_evaluation.py --baseline`.
`scripts/quality/check_regression_exit.py` exits with code 1 if any of the
following regression conditions are met (Decision 2.4):

- `avg_composite < baseline.avg_composite - 0.1`, OR
- A question that was `pass` in the baseline is now `weak` or `fail`, OR
- A question that was `weak` in the baseline is now `fail`.

The first Quality Gate run after a baseline change may show a transient
"improvement" (current better than baseline) — that is not a regression
and the gate passes. Noah then updates the baseline manually.

## File Format

Same structure as `run_evaluation.py --output` output:
`domain`, `date`, `evaluations[]`, `summary{avg_composite, ...}`.

## Current Baselines

| File | Domain | Date | Avg Composite | Questions |
|------|--------|------|---------------|----------|
| `godot-latest.json` | godot | 2026-06-30 | 0.8594 | 9 |
| `davinci_resolve-latest.json` | davinci_resolve | 2026-06-30 | 0.7246 | 7 |
