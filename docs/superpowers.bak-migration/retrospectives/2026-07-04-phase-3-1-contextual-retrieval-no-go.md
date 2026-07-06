# Phase 3.1 Contextual Retrieval Retrospective

## Goal

Implement Anthropic-style Contextual Retrieval: LLM-generated `context_prefix` for every chunk, prepended before embedding. Three sub-phases: 3.1a (infrastructure), 3.1b (generation mechanism + spot-check gate), 3.1c (cloud full-run + full-eval against `godot.yaml`). Decision gate: promote to production only if composite delta ≥ +0.02.

## What went well

- **Cloud setup worked immediately.** `ollama signin && ollama pull gemma4:cloud` — no configuration friction. Zero-retention policy acceptable for trusted Godot docs + personal notes.
- **Resume mechanism proved itself.** A transient 502 cloud outage mid-run was handled cleanly: 2731 cache hits on restart, zero data loss. The domain-independent cache key (OQ-3 Option b) worked across restarts.
- **Usage-limit handling worked.** First account hit HTTP 429 → immediate stop, account switch, resume from cache. No wasted tokens.
- **`num_predict` auto-resolve prevented token waste.** Cloud gemma4 is non-reasoning (unlike local Gemma 4 12B MLX), so `num_predict` auto-resolved to 100 instead of 800 — faster and cheaper.
- **3 rounds of blind-spot review caught real problems.** C1 (spot-check worthless with only 2 questions), C2 (`run_evaluation.py` hardcoded dataset path), NB-6 (BGE-M3 missing from spot-check domain), NB-7 (backoff too short). Each round improved the plan before implementation.
- **Eval-domain isolation (E13) protected the production index.** `godot_eval_a`/`godot_eval_b` as separate domains with symlinks — no backup/restore needed, no risk to the live `godot` index.
- **Zero regressions in A/B eval.** Clean experiment: 18→19 pass, 0 questions degraded.

## What went less well

- **Chunk count confusion.** The spec referenced 24,593 total chunks, but after the `chunk_type != "late_chunk"` filter (Path A), only 4,580 remained. Throughput estimates based on 24,593 were misleading.
- **3.1c throughput estimate was off.** Pre-run estimate: ~4h. Actual: ~3h (2.5s/chunk average, varying by chunk size and source file). Cloud rates are unpredictable.
- **Composite delta +0.0105 is small.** Contextual Retrieval alone doesn't reach the +0.02 threshold. The main expected benefit (repo API-reference chunks without context) didn't materialize — the one improvement came from a personal-notes question (godot-012, NavigationAgent3D Enemy Chase), not from repo chunks.
- **3 rounds of plan review were necessary.** The initial plan had 2 CRITICAL blind spots (C1, C2). Iterative plan revision was expensive but unavoidable.

## Lessons learned

- **Contextual Retrieval has a real but small benefit on this dataset.** +0.0105 composite, 1 question lifted (godot-012 weak→pass). Not enough for a production rollout, but the mechanism works correctly.
- **Cloud LLM is viable for batch preprocessing.** ~3h for 4,580 chunks with gemma4:cloud (32.7B). Resume + cache make it robust against transient failures. The domain-independent cache key design (OQ-3 Option b) is validated.
- **Eval-domain isolation (E13) is the right pattern for A/B experiments.** No backup/restore risk, clean separation, easy to keep for future re-runs. Should be the default for all future index-changing experiments.
- **Blind-spot reviews before implementation are high-leverage.** C1 and C2 would have wasted a full implementation cycle. The 3-round review process, while expensive, prevented rework.
- **Contextual BM25 is the obvious next step.** The infrastructure is in place (`--contextualize-bm25` flag accepted but unused). Anthropic reports +14% additional reduction from contextual BM25 on top of contextual embeddings. This could push the composite delta above +0.02.

## Next steps

1. **Contextual BM25 experiment** — Re-run eval with `--contextualize-bm25` on `godot_eval_b`. BM25 input = `context_prefix + "\n" + text`. Anthropic reports +14% additional reduction. Low effort (flag already exists, cache already populated).
2. **Prompt tuning** — Current outputs are descriptive ("This chunk contains…"). Shorter, more contextual situating might improve embedding quality. Test on a small subset.
3. **Alternative cloud model** — `gpt-oss:20b-cloud` (Usage Level 1, cheaper) might produce different context style. Cache is model-specific, so a fresh run is needed.
4. **Local Gemma 4 12B comparison** — Cloud gemma4 (32.7B) ≠ local Gemma 4 12B MLX. Context quality could differ. A small-sample comparison would resolve the confounder.
5. **Keep eval domains** — `godot_eval_a`/`godot_eval_b`/`godot_spotcheck` remain for future re-runs. No cleanup needed.

## References

- Spec: `docs/superpowers/specs/2026-06-30-improvement-roadmap-phase3-advanced-rag-design.md` (Section 3.1)
- Decisions: `docs/ai/decisions.md` (E6, E11–E17)
- Changelog: `docs/ai/changelog.md` (2026-07-02 3.1a, 2026-07-02 3.1b, 2026-07-04 3.1c)
- Known issues: `docs/ai/known-issues.md` (LIM-012, LIM-013, Phase 3.1c Ergebnis, Spot-Check-Gate-Limitation)
- Eval results: A=0.8281 (18 pass / 3 weak), B=0.8386 (19 pass / 2 weak), Delta=+0.0105
- Cache: `chromadb_data/godot_eval_b/context_cache.db` (4580/4580 entries, 0 rejected)
