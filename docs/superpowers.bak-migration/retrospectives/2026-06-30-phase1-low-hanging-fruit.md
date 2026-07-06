# Phase 1 Low-Hanging Fruit Retrospective

## Goal

Implement 5 low-hanging-fruit measures from the improvement roadmap: CI test workflow, reranker upgrade (jina optional), BM25 CamelCase-splitting, chunk overlap 200→400, and godot faq.md expansion with godot-008 gap closure.

## What went well

- **Blind-spot review caught `trust_remote_code` and `einops` before implementation.** The plan only mentioned a `config.py` change, but jina-reranker-v2 requires `trust_remote_code=True` in `model_manager.py` and imports `einops` (not in `requirements.txt`). Both were added pre-implementation — no runtime failures.
- **Unicode-aware BM25 tokenizer instead of ASCII-only regex.** The implement-hub-change agent proposed a better variant than the plan: CamelCase-boundaries + `[^\W\d_]+|\d+` with `re.UNICODE`, preserving German umlauts. Good agent initiative, approved by orchestrator.
- **Env-var pattern established.** `KH_RERANKER_MODEL` is the first model-configuration env var. The pattern carries forward to Phase 2 (`KH_EMBEDDING_MODEL`) and Phase 3 (`KH_LLM_MODEL`, `KH_JUDGE_MODEL`, `KH_SPARSE_MODE`).
- **Manual YAML edit instead of `add_question.py`.** Blind-spot review warned that `add_question.py` uses `yaml.dump` and destroys header comments. Manual editing preserved them.
- **godot-007 stable.** `tips.md` remains top-1 despite BM25 CamelCase changes. No regression.
- **302 tests green** (107 unit + 35 integration + 136 quality + 12 e2e + 12 mcp).

## What was surprising or difficult

- **godot-008 remains weak** (SR 0.5, `faq.md` missing from top-10). The 3D Visibility section is freshly indexed but semantically close to `godot-docs-3d-packed.md`. The question is broad ("why can't I see my 3D model"), and the Cross-Encoder ranks API-doc chunks higher than the German FAQ. Acceptable per exit criterion (SR ≥ 0.5), but an open gap for Phase 2.
- **godot avg_composite dropped 0.0273** (0.8594 → 0.8321). Not a code regression — godot-008 (weak) pulls the average down. The other 7 questions have identical scores. No real degradation.
- **jina reranker download (1.1 GB) skipped.** The short evaluation was not performed because the download requires Noah's explicit approval. jina remains documented as an optional env var; default is ms-marco. Actual reranker performance is untested — a risk for Phase 2.
- **davinci avg_composite 0.7218** — new baseline (not previously measured with identical tooling). PMA 0.1714 is low (±2 page tolerance, PDF chunking variance). Not caused by Phase 1, but surfaced by it.
- **implement-hub-change step limit.** The first agent hit the step limit after 1.2+1.1. A second agent was tasked with 1.3+1.4+1.5+rebuild. Workflow aspect, not a technical problem.
- **`.opencode/agents/*.md` accidentally modified.** OpenCode changed model names in 5 agent files (minimax-m3 → glm-5.2) during agent execution. Reverted before commit — not part of Phase 1.

## Lessons learned

- **Blind-spot review pays off especially for dependency changes.** `trust_remote_code` and `einops` were not in the original plan but were found. Always run blind-spot for reranker/embedding/LLM swaps.
- **Agent initiative can improve plans.** The Unicode-aware BM25 variant was better than the strict ASCII plan. Agents should show initiative with well-founded reasoning; the orchestrator decides.
- **Env-var configurability is an architectural lever.** `KH_RERANKER_MODEL` is more than a feature — it's a pattern enabling all future model swaps without code changes.
- **godot-008 shows the limit of content-only improvements.** Filling `faq.md` isn't enough when the question is broad and API docs are semantically similar. Phase 2 (BGE-M3 multilingual) will help, but the gap remains open until then.
- **Model downloads (>100 MB) need Noah's explicit approval.** Saves disk space and gives Noah control over model selection.

## What to do differently next time

- For multi-measure iterations with step-limited agents, split the plan into agent-sized chunks upfront (e.g., 1.1+1.2 for agent A, 1.3+1.4+1.5+rebuild for agent B) rather than discovering the limit mid-execution.
- When introducing new env-var patterns, document the pattern in `docs/ai/decisions.md` so future phases can reference it.

## Follow-up candidates

1. **jina reranker download + short evaluation** — Noah decides whether to download 1.1 GB. If yes: run `KH_RERANKER_MODEL=jinaai/jina-reranker-v2-base-multilingual python scripts/quality/run_evaluation.py --domain godot` and compare avg_composite with ms-marco baseline.
2. **godot-008 gap closure** — strengthen FAQ visibility section with English search anchors, OR BGE-M3 multilingual in Phase 2, OR make the question more specific. Separate iteration.
3. **DaVinci PMA low (0.1714)** — investigate chunking/page-range tolerances. Separate iteration (likely Phase 2 Late Chunking).
4. **Phase 2 start** — BGE-M3 embedding model swap (systematically solves DE↔EN), Late Chunking for DaVinci PDFs, CI quality gate, Golden Dataset expansion.

## References

- Spec: `docs/superpowers/specs/2026-06-30-improvement-roadmap-phase1-low-hanging-fruit-design.md`
- Plan: `docs/superpowers/plans/2026-06-30-phase1-low-hanging-fruit-plan.md`
- Explanation: `docs/superpowers/explain-location/2026-06-30-phase1-low-hanging-fruit.md`
