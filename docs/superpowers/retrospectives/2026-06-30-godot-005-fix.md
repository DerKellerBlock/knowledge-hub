# Godot-005 Fix Retrospective

## Goal
Fix the godot-005 regression (pass 0.86 → weak 0.42) introduced in the Gap-Closing iteration (commit f5be7e0).

## Root cause
Chunk dilution: `gotchas.md` (3,454 chars, 7 gotcha entries) was indexed as 1 chunk (FALLBACK_CHUNK_CHARS=8000). The Cross-Encoder scores `[query, chunk_text]` pairs — 6 irrelevant entries in the same chunk diluted semantic similarity to the GLB/Meshy/Scale query. The focused `best-practices.md` (1,129 bytes, 1 chunk) ranked instead with score 1.03.

## Solution
Markdown section chunking for personal notes (`markdown_section_chunk()` in `scripts/parser_base.py`): splits on `##` headers, defensive skip for sections <50 chars (filters TODO placeholders like faq.md), fallback to `fallback_chunk()` for files without `##` headers. Chosen over query reformulation (symptom treatment) and ranking tuning (regression risk, architecture violation).

## What went well
- Blind-spot review caught that `markdown_section_chunk()` affects ALL personal notes, not just gotchas.md — re-evaluation of all 7 godot questions was mandatory and correctly performed.
- Defensive skip (<50 chars) cleanly filtered TODO placeholders (faq.md) — no index pollution.
- BM25 tokenization benefits from more specific section names as `chunk.name` (2x weighting in bm25_search.py).
- Cross-Encoder reranking now much cleaner: each gotcha entry is an independent `[query, chunk_text]` pair without dilution.
- Re-evaluation confirmed godot-007 is NOT caused by this iteration (originates from f5be7e0); chunking actually improved it slightly (cosine 0.45 vs 0.35).

## What was surprising or difficult
- godot-007 dropped from 0.86 to 0.7136, initially perceived as a regression. Diagnosis revealed it was already at 0.7136 in f5be7e0 state (expected_source_files was expanded to include tips.md without the Stair-Stepping chunk ranking strongly enough). This confusion cost a diagnosis round.
- First `implement-hub-change` run hit the step limit and only partially delivered the godot-007 diagnosis. A second diagnosis session was needed.
- LIM-005 discrepancy surfaced: known-issues.md says "all 14 solution_summary null", but godot-005 has filled solution_summaries. Not part of this iteration, but became visible.

## Results
- godot-005: 0.4219 (weak) → 0.8594 (pass), SR=1.0. Top-1 ranking of "GLB Import — Mesh Origin Bug" chunk confirmed.
- 292 tests green (97 unit + 136 quality + 35 integration + 12 e2e + 12 mcp).
- Index rebuild: 24,552 → 24,564 chunks (+12 personal section chunks). gotchas.md 1→8, best-practices.md 1→4, tips.md 1→4, faq.md 1→0.
- Avg Composite godot: 0.8386 (7/7 pass).
- Security: SAFE with notes (no blockers, info-level only).
- Diff: APPROVE with notes (no blockers).

## Lessons learned
- **Personal notes chunking is a lever** — `##`-header-based splitting is a generic, domain-agnostic improvement. It eliminates a systematic weakness of the fallback chunker (1-chunk-per-file for small markdown files).
- **Diagnose before fix:** The godot-007 "regression" could have been avoided by comparing previous report values (f5be7e0) with the prior Avg Composite before implementation. Instead, it only became clear after implementation that godot-007 is a pre-existing gap.
- **Blind-spot review pays off** — the hints (re-evaluate all 7 questions, conftest.py fixture, defensive skip) made the implementation more robust.
- **LIM-005 may be stale** — should be verified in a follow-up iteration (separate issue).

## What to do differently next time
- Before implementing a fix for a regression, compare the previous evaluation report against the baseline to distinguish pre-existing gaps from newly introduced regressions.
- When a subagent hits a step limit, restart with a narrower scope rather than trying to pack everything into one session.

## Follow-up candidates
1. **Close godot-007 gap** — expand tips.md Stair-Stepping section with concrete code snippets, OR adjust Golden Dataset expected_source_files, OR increase Hybrid-Search Stage-1 top-K. Separate iteration.
2. **Verify LIM-005** — cross-check known-issues.md against quality/golden/*.yaml. Separate iteration.
3. **DaVinci personal notes** — if DaVinci index is rebuilt, TODO placeholders in ui-map.md will be filtered by defensive skip. Verify before a DaVinci rebuild.

## References
- Spec: `docs/superpowers/specs/2026-06-09-knowledge-hub-design.md`
- Plan: `docs/superpowers/plans/2026-06-30-godot-005-fix.md`
- Explanation: `docs/superpowers/plans/2026-06-30-godot-005-fix-explanation.md`
