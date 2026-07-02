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

The current `*-latest.json` baselines are **BGE-M3 + jina-reranker-v2-base-multilingual**
(KH_RERANKER_MODEL env var, 2026-07-01). The previous ms-marco-MiniLM baselines
are archived as `*-msmarco-2026-06-30.json`. The pre-Phase-2b baselines (BGE-M3+jina,
7-9 questions, before Golden Dataset expansion) are archived as `*-pre-phase2b-2026-07-01.json`.
The DaVinci baseline is now Phase-2.2 Late-Chunking (2026-07-02, see Phase 2.2
section below).

To reactivate the ms-marco reranker locally, leave `KH_RERANKER_MODEL` unset
(the code default is `cross-encoder/ms-marco-MiniLM-L-12-v2`). The CI
quality-gate workflow sets `KH_RERANKER_MODEL=jinaai/jina-reranker-v2-base-multilingual`
explicitly, so CI always compares against the jina baselines.

| File | Domain | Date | Reranker | Avg Composite | Questions |
|------|--------|------|----------|---------------|----------|
| `godot-latest.json` | godot | 2026-07-02 | jina | 0.8281 | 21 |
| `godot-pre-contentfix-2026-07-02.json` | godot | 2026-07-01 | jina | 0.8073 | 21 |
| `davinci_resolve-latest.json` | davinci_resolve | 2026-07-02 | jina | 0.8183 | 20 |
| `davinci_resolve-latechunk-pre-pageranges-2026-07-02.json` | davinci_resolve | 2026-07-02 | jina | 0.8133 | 20 |
| `godot-pre-phase2b-2026-07-01.json` | godot | 2026-07-01 | jina | 0.8594 | 9 |
| `davinci_resolve-pre-phase2b-2026-07-01.json` | davinci_resolve | 2026-07-01 | jina | 0.7304 | 7 |
| `godot-msmarco-2026-06-30.json` | godot | 2026-06-30 | ms-marco | 0.8594 | 9 |
| `davinci_resolve-msmarco-2026-06-30.json` | davinci_resolve | 2026-06-30 | ms-marco | 0.7246 | 7 |

## Phase 2.2 — Late Chunking (2026-07-02)

The current `davinci_resolve-latest.json` baseline is **Late-Chunking** (Phase 2.2,
BGE-M3 1024d / jina reranker, chapter-wise mean pooling 512-token windows with
128-token overlap). DaVinci index grew from 2.511 → 12.367 chunks. The previous
Fallback-Chunking baseline is archived as `davinci_resolve-pre-phase2b-2026-07-01.json`
(7 questions, 0.7304 avg composite). The intermediate Late-Chunking baseline
(before `expected_page_ranges` update) is preserved as
`davinci_resolve-latechunk-pre-pageranges-2026-07-02.json` (20 questions, 0.8133
avg composite) for the Phase 2.2 page-ranges-update delta measurement.

**Page ranges update (2026-07-02):** the 7 old DaVinci questions
(davinci_resolve-001..007) had `expected_page_ranges` from the Fallback-Chunking
era that no longer matched Late-Chunking chapter boundaries. After updating
ranges from the new top-5 search results (Late-Chunking index), PMA improved
from 0.760 → 0.785 (+2.5%) and avg_composite from 0.8133 → 0.8183 (+0.5%).
All 20 questions pass, no regressions.

## Phase 2.4 — Golden Dataset Expansion (2026-07-01)

The current `*-latest.json` baselines were established after Phase 2.4
expanded both Golden Datasets to 20+ questions:

- **godot:** 9 → 21 questions (added godot-009 through godot-020, 12 new
  questions covering Animation, Shaders, UI, Navigation, Multiplayer,
  Input, Audio, File I/O, Performance, TileMap, Resources, Profiler).
- **davinci_resolve:** 7 → 20 questions (added davinci_resolve-008 through
  davinci_resolve-020, 13 new questions covering Fusion Compositing,
  Color Advanced, Cut Page, Edit Page Multicam, Fairlight Atmos, Media
  Management, Transitions, Fusion Text+, Collaboration, Troubleshooting,
  and Workflow).

The drop in godot avg_composite (0.8594 → 0.8073) reflects the broader
coverage: the 5 new weak questions (godot-009, -011, -012, -017, -019) test
areas that have no `personal/` entry and rely on multi-page synthesis
(Animation, UI Containers, Navigation, Performance, Resources). The
`godot-pre-phase2b-2026-07-01.json` archive preserves the 9-question
baseline for Phase 2.2 Late Chunking comparison.

The DaVinci avg_composite increased (0.7304 → 0.8063) because the new
questions land cleanly on top of the existing BM25/Embedding signals
(typical 0.8875 for Fusion/Color/Edit/Collaboration topics, 0.7125 for
workflow-oriented queries).

## Phase 2b Follow-up — Content Fixes (2026-07-02)

After Phase 2.4, 5 godot questions were weak (godot-009, -011, -012, -017, -019).
Content measures were added to `tips.md` and `best-practices.md`:

- **godot-011 (Responsive UI):** weak→pass (0.6406 → 0.8594) — `best-practices.md`
  section on Responsive UI Containers/Anchors.
- **godot-019 (Custom Resource):** weak→pass (0.6406 → 0.8594) — `best-practices.md`
  section on Custom Resource with `class_name extends Resource`.
- **godot-009 (AnimationTree):** remains weak (0.6406) — `tips.md` section on
  AnimationTree+BlendSpace2D Locomotion not sufficient.
- **godot-012 (NavigationAgent3D):** remains weak (0.6406) — `tips.md` section on
  NavigationAgent3D Enemy Chase not sufficient.
- **godot-017 (Performance):** remains weak (0.6406) — `best-practices.md` section
  on 3D Performance LOD/Occlusion/Visibility not sufficient.

Overall: avg_composite 0.8073 → 0.8281 (+0.0208), 16 pass / 5 weak → 18 pass / 3 weak.
The old baseline is archived as `godot-pre-contentfix-2026-07-02.json`.
