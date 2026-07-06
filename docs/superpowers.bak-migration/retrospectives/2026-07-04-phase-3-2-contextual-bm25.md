# Phase 3.2 Contextual BM25 Retrospective

## Goal

Implement Contextual BM25: BM25-Corpus = `context_prefix + " " + text` (D1-Aufhebung E18, opt-in via `--contextualize-bm25`). A/B/C comparison against `godot.yaml` (21 questions). Decision gate: promote to production if composite delta ≥ +0.02.

## What went well

- **Cache-Reuse worked perfectly.** 4580/4580 cache hits, 0 LLM calls. The domain-independent cache key (E17) proved itself — `cp context_cache.db` from `godot_eval_b` after WAL-checkpoint, zero re-generation needed.
- **Code change was minimal.** ~6 lines in `bm25_search.py` (`build_bm25_index` with `use_context_prefix`), ~4 lines in `embed_index.py` (`--contextualize-bm25` flag wiring). The infrastructure from Phase 3.1 carried the weight.
- **A/B/C comparison was cleanly isolated.** E13 eval domains (`godot_eval_a`/`godot_eval_b`/`godot_eval_c`) kept the productive `godot` index untouched. No backup/restore risk.
- **GO result: +0.0209 ≥ +0.02.** C (Embeddings + Contextual BM25) reached avg_composite 0.8490, 20 pass / 1 weak. Two weak questions lifted: godot-008 (3D model visibility, language barrier) and godot-012 (NavigationAgent3D). Only godot-009 (AnimationTree, broad animation) remains weak.
- **Blind-spot review (GO MIT HINWEISEN) caught real issues.** BS-1 (WAL-checkpoint before cache copy), BS-4 (TF-test unreliable with small corpora), BS-5 (hybrid_search integration path) — all addressed before the build.

## What went less well

- **BS-6 Tokenizer assumption.** Tests assumed `"characterbody"` as a single token, but the CamelCase splitter produces `"character"` — test assertions had to be corrected to match actual tokenizer behavior.
- **Build took 2h+.** Longer than the 50-minute estimate, because `context_prefix + " " + text` produces longer embedding strings than plain text. BGE-M3 CPU encoding scales with input length.
- **BS-4 TF-Test.** `BM25Okapi` IDF values go negative for small corpora, making score comparisons unreliable. Test was restructured to compare `doc_freqs` instead of raw scores.
- **pass/weak counts were 0 in first analysis.** The evaluation JSON uses `"label"` not `"status"`, and `"evaluations"` not `"questions"` — had to explore the result structure before reporting correct counts.

## Lessons learned

- **Contextual BM25 brings additional benefit over embeddings-only.** C-B delta = +0.0104, confirming Anthropic's 49% vs. 35% pattern. The combination of contextual embeddings + contextual BM25 is stronger than either alone.
- **Language barrier (godot-008) is solvable with Contextual BM25.** The German `faq.md` context in the BM25 corpus helps semantically match the English query — BGE-M3 embeddings alone couldn't bridge this gap. BM25's exact token matching benefits from the English context prefix wrapping German content.
- **R4 (Parser-Confounder) is the critical open item.** The eval used `fallback_chunk` (simple token-count chunking), but the productive `godot` index uses `rst-godot` (structured RST parsing). Results are NOT directly transferable — a separate Cloud run on the productive index is required for promote.
- **Eval-domain isolation (E13) remains the right pattern.** Three domains, one cache, zero risk to production. Should be the default for all future index-changing experiments.

## Next steps

1. **Promote to production (R4).** Run `embed_index.py --domain godot --contextualize --contextualize-bm25` with `gemma4:cloud` on the productive `godot` index (rst-godot parser). Reuse `context_cache.db` from eval_b (domain-independent key). Expect ~3h Cloud run. Re-evaluate against `godot.yaml` to confirm the +0.0209 delta holds with rst-godot chunking.
2. **Keep eval domains.** `godot_eval_a`/`godot_eval_b`/`godot_eval_c` remain for future re-runs (prompt tuning, alternative models).
3. **Document R4 result.** If promote succeeds, update `known-issues.md` (godot-008 resolved, godot-009 remains) and `changelog.md`.

## References

- Spec: `docs/superpowers/specs/2026-07-02-phase-3-1-contextual-retrieval-design.md` (Section 3.1, E18)
- Decisions: `docs/ai/decisions.md` (E17, E18, E19)
- Changelog: `docs/ai/changelog.md` (2026-07-04 Phase 3.2)
- Known issues: `docs/ai/known-issues.md` (Phase 3.2 Ergebnis, R4)
- Architecture: `docs/ai/architecture.md` (Contextual BM25)
- Domain model: `docs/ai/domain-model.md` (Contextual BM25, E18)
- Best practices: `docs/ai/best-practices.md` (Contextual BM25)
- Phase 3.1 retrospective: `docs/superpowers/retrospectives/2026-07-04-phase-3-1-contextual-retrieval-no-go.md`
- Eval results: A=0.8281 (18 pass / 3 weak), B=0.8386 (19 pass / 2 weak), C=0.8490 (20 pass / 1 weak), Delta C-A=+0.0209
- Cache: `chromadb_data/godot_eval_b/context_cache.db` (4580/4580 entries, reused for C)
