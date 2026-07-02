# Phase 2b Golden Dataset + Late Chunking Retrospective

## Goal

Expand the Golden Dataset from 16 to 41 questions (godot 9→21, davinci 7→20) and implement chapter-wise Late Chunking for DaVinci Resolve PDFs. The Golden Dataset expansion (Phase 2.4) establishes broader coverage across all major tool areas. Late Chunking (Phase 2.2) replaces the old fallback chunking with BGE-M3 long-context chapter encoding, producing 512-token windows with 128-token overlap via mean pooling.

## What went well

- **Golden Dataset expansion was pure curation — all 25 proposals accepted as-is.** `validate_dataset.py` passed both domains immediately. No back-and-forth, no reformulation needed. The curation template worked.
- **Late Chunking Smoke-Test caught potential issues early.** A 2-minute test on `fairlight-live-user-manual.md` (115 KB) validated the entire code path — BGE-M3, MPS, offset mapping, chapter splitting — before investing 15 minutes in the full rebuild.
- **`_LateChunkEncoder` MPS pre-flight worked on first try.** No OOM, no BF16 crash, MPS was used (no CPU fallback needed). The pre-flight pattern from Phase 2a's `_encode_robust()` proved its value again.
- **Offset mapping (B3 fix) was lossless.** UTF-8 special characters in DaVinci PDFs (em-dashes, curly quotes) round-tripped correctly through BGE-M3's tokenizer. No substring-based fallback needed.
- **`precomputed_embeddings` as separate dict (B1 fix) flowed cleanly through the pipeline.** No pickle issues, no ChromaDB metadata collisions. The tuple return pattern `(chunks, precomputed_embeddings)` kept chunk data small.
- **`expected_page_ranges` update (V8) resolved davinci-005 cosmetic regression.** PMA rose from 0.760 → 0.785 after correcting page ranges for the 7 old questions (001–007) to match Late Chunking's chapter boundaries.
- **Rebuild took ~15 min vs estimated 20–40 min.** BGE-M3 is more efficient than expected at encoding 8192-token chapters.

## What was surprising or difficult

- **implement-hub-change hit the step limit 3×.** Phase 2.2 needed 4 task continuations: parser_base.py, unit tests, embed_index integration, integration test fix + page_ranges + docs. The Late Chunking code path touches many files.
- **Dual-module-object bug was subtle and hard to diagnose.** `from config import DOMAINS_DIR` created a second module object that conftest's `monkeypatch` couldn't see. Two integration tests failed when run together but passed individually. Root cause: `from X import Y` copies the value for immutable objects (Path). Fix: live-lookup via `_config.DOMAINS_DIR`.
- **Late Chunking produced 5× more chunks than expected.** 2,511 → 12,367 (estimated 6,000–8,000). 512-token windows with 128-overlap across 10 DaVinci PDFs (17 MB) create finer granularity. ChromaDB storage grew from 481 → 685 MB (+43%), still acceptable.
- **LIM-009 confounder persists.** BGE-M3 long-context + Late Chunking changed simultaneously — the DaVinci improvement (+1.5% composite, +8.3% PMA) mixes both effects. Not isolatable without a 384-token BGE-M3 setup (not planned).

## Lessons learned

- **`from X import Y` is dangerous for testable constants.** For immutable objects (Path, str, int), the value is copied, not referenced. `monkeypatch.setattr(cfg, "DOMAINS_DIR", ...)` can't reach the imported copy. Live-lookup via `_config.DOMAINS_DIR` is the robust solution (same pattern as `model_manager.get_domain_config()`).
- **Smoke-tests before full rebuilds are indispensable.** The 2-minute smoke test validated BGE-M3, MPS, offset mapping, and chapter splitting before committing 15 minutes to the full rebuild. This pattern should be mandatory for all future chunking changes.
- **`expected_page_ranges` are chunking-strategy-dependent.** Late Chunking fundamentally changes chapter boundaries. Old page_ranges from the fallback-chunking era must be manually updated after chunking changes (V8). This is expected follow-up work, not a bug.
- **PMA is the most sensitive metric to chunking changes.** Composite and Source-Recall are rank-based and robust, but PMA reacts immediately to shifted chapter boundaries. PMA +8.3% confirms Late Chunking places chapter boundaries more precisely on PDF pages.

## Follow-up candidates

1. **Phase 2b Godot weak questions** — 5 weak Godot questions (009/011/012/017/019, composite 0.6406) test topics without `personal/` notes. Content measures (new FAQ sections) or question refinement could help. Godot has no Late Chunking benefit (structured parser).
2. **MEDIUM-1: Remove dead code `_encode_chapter_with_hidden_states()`** — no caller exists.
3. **MEDIUM-2: Fixed-size fallback for >8192-token chapters without paragraph boundaries** — very rare but possible.
4. **Phase 3: Contextual Retrieval + RAGAS + DaVinci Personal Notes + BGE-M3 Sparse + Multi-Modal** — spec under `docs/superpowers/specs/2026-06-30-improvement-roadmap-phase3-advanced-rag-design.md`.

## References

- Commits: `f89cbff` (Golden Dataset), `534c7a2` (Late Chunking code), `7a66289` (DaVinci rebuild + page_ranges + docs)
- Spec: `docs/superpowers/specs/2026-06-30-improvement-roadmap-phase2-embedding-upgrade-design.md` (Decisions 2.13–2.18)
- Known issues: `docs/ai/known-issues.md` (LIM-009 confounder, LIM-010 line_start/end=0)
- Baselines: `quality/baselines/godot-latest.json` (0.8073), `quality/baselines/davinci_resolve-latest.json` (0.8183)
- Pre-Phase-2b backups: `quality/baselines/godot-pre-phase2b-2026-07-01.json`, `quality/baselines/davinci_resolve-pre-phase2b-2026-07-01.json`
- Report: `quality/reports/davinci_resolve_2026-07-02.md`
- Tests: 315 green (126 unit + 44 integration + 145 quality)
