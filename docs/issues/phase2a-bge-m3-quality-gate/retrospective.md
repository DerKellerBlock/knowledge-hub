# Phase 2a BGE-M3 + Quality Gate Retrospective

## Goal

Swap the embedding model from `all-mpnet-base-v2` (English-only, 768d) to `BAAI/bge-m3` (multilingual, 1024d, 8192 token context), establish a CI quality regression gate with manual baselines, and re-evaluate both domains. The primary motivation: systematically close the DE↔EN language barrier that had been open since Phase 1.

## What went well

- **BGE-M3 multilingual closed godot-008.** The English query "Why is my 3D model not visible" against the German `faq.md` went from weak (0.6404) to pass (0.8594). No content workaround needed — the embedding model itself solved the language barrier. This is the systematic fix, not a per-question patch.
- **`_encode_robust()` solved the MPS/SDPA OOM bug.** BGE-M3 on Apple Silicon cannot handle mixed long/short batches. Length-sorting + bs=32 for short chunks + bs=1 for long chunks (>8000 chars) is the robust solution. DaVinci chunks are now fully processed (8192 token context) instead of truncated at 384 tokens.
- **Blind-spot review caught the `np.stack()` bug before the full rebuild.** The smoke test only checked `len()`/`len([0])`, not the `.tolist()` path. The Godot collection was deleted before the error surfaced → index broken → backup restore needed. The fix was applied and the rebuild restarted successfully.
- **Env-var pattern consistent with Phase 1.** `KH_EMBEDDING_MODEL` mirrors `KH_RERANKER_MODEL` — all future model swaps are now configurable without code changes. Precedence: Env-Var > domain.md > DEFAULT_MODEL_NAME.
- **Re-evaluation showed improvement, not just "no regression".** Godot +0.0243 (0.8351 → 0.8594), DaVinci +0.0028 (0.7218 → 0.7246). All 16 questions pass (9 godot + 7 davinci).
- **Quality Gate workflow with B5/B6 fixes.** Cache key includes `config.py` (B5), LFS checkout uses `lfs:true` (B6). Weekly Monday 05:00 UTC + `workflow_dispatch`. Manual baselines prevent score creep.

## What was surprising or difficult

- **First rebuild attempt failed with `AttributeError: 'list' object has no attribute 'tolist'`.** `_encode_robust()` returned a list-of-arrays, `build_index()` expected an ndarray. The smoke test didn't catch it because it only validated `len(embs)` and `len(embs[0])`, not the `.tolist()` call path. Godot collection was already deleted → backup restore required.
- **implement-hub-change hit the step limit twice.** Once during the 18,222-chunk encoding, once during subsequent steps. Phase 2a needed 3 task continuations.
- **BGE-M3 ~2.2 GB download + 18,222 chunks encoding took ~20 min for Godot locally.** In CI with a cold cache, this could be 40–50 min — the 60 min timeout is tight.
- **LIM-009 confounder: embedding model swap + effective chunk length change happened simultaneously.** BGE-M3 8192 tokens processes DaVinci chunks fully (previously all-mpnet truncated at 384 tokens). The re-evaluation mixes both effects — not isolatable.

## Lessons learned

- **BGE-M3 multilingual is the systematic fix for DE↔EN language barriers** — not content workarounds (code snippets in tips.md) or question reformulations. The investment pays off for all future domains (Blender, FreeCAD with German personal notes).
- **Smoke tests must exercise the real code path.** `len(embs)` does not validate `batch_embeddings.tolist()`. A mini `collection.add()` probe insert would have been safer.
- **`_encode_robust()` is critical for long-context models on Apple Silicon.** MPS/SDPA cannot handle mixed long/short batches. Length-sorting + bs=1 for long chunks is the robust solution.
- **Quality gate with manual baselines is more sustainable than auto-update.** Prevents score creep, forces Noah to consciously review score changes.

## Follow-up candidates

1. **jina reranker test (LIM-007)** — `KH_RERANKER_MODEL=jinaai/jina-reranker-v2-base-multilingual python scripts/quality/run_evaluation.py --domain godot`. Compare avg_composite with BGE-M3+ms-marco baseline (0.8594). Resolves LIM-008 (BGE-M3+ms-marco transitional).
2. **Phase 2b: Late Chunking (2.2) + Golden Dataset 20–30 (2.4)** — Spec under `docs/superpowers/specs/2026-06-30-improvement-roadmap-phase2-embedding-upgrade-design.md`.
3. **Phase 3: Contextual Retrieval + RAGAS + DaVinci Personal Notes + BGE-M3 Sparse + Multi-Modal (deferred)** — Spec under `docs/superpowers/specs/2026-06-30-improvement-roadmap-phase3-advanced-rag-design.md`.

## References

- Spec: `docs/superpowers/specs/2026-06-30-improvement-roadmap-phase2-embedding-upgrade-design.md` (Decisions 2.1–2.12)
- Known issues: `docs/ai/known-issues.md` (LIM-007 jina unverified, LIM-008 transitional, LIM-009 long-context confounder)
- Quality reports: `docs/superpowers/quality-reports/godot_2026-06-30.md`, `docs/superpowers/quality-reports/davinci_resolve_2026-06-30.md`
- Baselines: `quality/baselines/godot-latest.json`, `quality/baselines/davinci_resolve-latest.json`
- CI: `.github/workflows/quality-gate.yml`
