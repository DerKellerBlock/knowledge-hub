# Phase 3.3a Acceleration Retrospective

## Goal

Three acceleration measures for the Contextual Retrieval pipeline: (1) MPS GPU encoding (`KH_EMBEDDING_DEVICE`, ~4.7× Speedup, LIM-011 RESOLVED), (2) parallel LLM calls (`KH_LLM_WORKERS`, ThreadPoolExecutor, ~3× Speedup), (3) SQLite safety (`busy_timeout`, `check_same_thread`, `write_lock`). No rebuild or eval — infrastructure-only. 226 unit + 108 integration tests. 2 rounds of blind-spot review. Diff-review: 15 findings, 2 code fixes (F3 usage-limit attr, F14 pending_writes flush), 5 doc fixes.

## What went well

- **MPS works on M1 Max.** `torch` 2.12.0 resolved the BGE-M3 + `transformers` 4.57.6 MPS deadlock. Encoding: 0.22 s/chunk (MPS) vs. 1.02 s/chunk (CPU) — 4.7× Speedup. LIM-011 documented 2026-07-02, resolved 2 days later.
- **Backward-compat preserved.** Defaults `cpu` / `workers=1` — no existing pipeline breaks. Operators opt in via env vars.
- **Diff-review caught real bugs.** F3 (fragile `"Usage limit"` string-match in `cancel_event` propagation) and F14 (`pending_writes` loss on HTTP 429) — both fixed before merge.
- **SQLite safety works.** `busy_timeout=5000` + `check_same_thread=False` + `write_lock` prevents `database is locked` with 3 workers. Integration test `test_parallel_cache_write_no_lock` verifies.
- **Spec + docs + tests all green.** 10 unit tests, 2 integration tests, no regressions.

## What went less well

- **2 rounds of blind-spot review needed.** Round 1 found B1 (chunk count 24,593 vs. 196,565 — spec had wrong total). Round 2 found B-R2-3 (godot cache schema empty — `init_schema()` not called before promote). Both were real issues that would have caused failures.
- **Reviewer false positives cost time.** B-R2-1 (ChromaDB corrupt) and B-R2-2 (sources 0 bytes) were incorrect — investigation confirmed no actual problem. Reviewer hallucinated issues from incomplete context.
- **Stale doc caught late.** `best-practices.md` L40–44 (BGE-M3 MPS Hang) was outdated after the change — diff-review caught it (F8), but it should have been updated during implementation.
- **Spec/test discrepancy.** Spec R1.1 said "100 chunks" for pre-flight, test used 10 — caught in diff-review (F13). Spec was corrected to 10.

## Lessons learned

- **MPS GPU is the single biggest lever.** 4.7× embedding speedup makes Godot rebuild ~17 min (was ~80 min CPU). This alone makes the promote economically viable.
- **Parallel LLM calls need careful thread-safety.** Pre-warm `get_llm()` before ThreadPool, `cancel_event` for usage-limit propagation, `write_lock` around SQLite writes, `check_same_thread=False`. Each detail matters — missing any one would cause silent corruption or deadlocks.
- **DaVinci has only 1 Path-A chunk** (`ui-map.md`). The smoke test validates infrastructure, not quality. No `+0.02` gate applies.
- **Godot promote needs 24,593 new LLM calls** (R5: `rst-godot` parser ≠ `fallback_chunk` → 0 cache hits from eval domains). ~5.7 h with 3 parallel workers on `gemma4:cloud`.

## Next steps

1. **3.3b: DaVinci Smoke-Test.** Build with MPS + 1 LLM call. Verify: no crash, cache entry written, `context_prefix` not `None`, Contextual BM25 active. Direct production apply (R4: `late_chunk` follows same parser path → cache hits on subsequent runs).
2. **3.3c: Godot Promote.** Run `embed_index.py --domain godot --contextualize --contextualize-bm25` with `gemma4:cloud` + 3 workers on the productive `godot` index. ~5.7 h. Pre-promote baseline, post-promote eval against `godot.yaml`. Expect `godot-008`/`godot-012` pass, no regression.

## References

- Spec: `docs/superpowers/specs/2026-07-04-acceleration-mps-parallel-design.md`
- Changelog: `docs/ai/changelog.md` (2026-07-04 Phase 3.3a)
- Known issues: `docs/ai/known-issues.md` (LIM-011 resolved)
- Architecture: `docs/ai/architecture.md` (KH_EMBEDDING_DEVICE, KH_LLM_WORKERS)
- Best practices: `docs/ai/best-practices.md` (MPS Pre-Flight, Parallel LLM, SQLite Safety)
- Phase 3.1 retrospective: `docs/superpowers/retrospectives/2026-07-04-phase-3-1-contextual-retrieval-no-go.md`
- Phase 3.2 retrospective: `docs/superpowers/retrospectives/2026-07-04-phase-3-2-contextual-bm25.md`
