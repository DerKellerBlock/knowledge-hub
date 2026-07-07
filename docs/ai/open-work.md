# Open Work — Knowledge Hub

> Index der offenen Tasks. Agenten lesen diese Datei beim Onboarding,
> wählen einen Task, und laden NUR den entsprechenden `docs/issues/<task-id>/`-Ordner.
>
> Workflow: 1. open-work.md lesen → 2. Task wählen → 3. docs/issues/<task-id>/ laden
> → 4. spec.md + plan.md + context/ abarbeiten → 5. bei Abschluss:
> retrospective.md + explanation.md schreiben, Status hier auf "done" setzen.

## Offene Tasks

| Task-ID | Spec | Plan | Priorität | Status | Kurzbeschreibung |
|---|---|---|---|---|---|
| quality-metrics-v2 | docs/issues/quality-metrics-v2/spec.md | docs/issues/quality-metrics-v2/plan.md | high | done | Diskriminative Eval-Metriken (NDCG@10, Jaccard, WSR, Diversity) + HyDE + Page Range Kuratie — 0.7234→0.8017, 15→21 pass |
| visual-question-answering | docs/issues/visual-question-answering/spec.md | docs/issues/visual-question-answering/plan.md | high | open | Visual Question Answering via MCP — search_knowledge akzeptiert image_path, SigLIP-2 findet ähnliche Screenshots, optional MiniMax M3 Vision-LLM |



## Abgeschlossene Tasks

| Task-ID | Abschluss | Retrospektive | Zusammenfassung |
|---|---|---|---|
| vision-retrieval-feature | 2026-07-07 | docs/issues/vision-retrieval-feature/retrospective.md | Vision Retrieval Feature (Multimodal-RAG: 23182 images, 4-Listen-RRF, Eval 0.6945, 6 Bild-Fragen) |
| acceleration-mps-parallel | 2026-07-04 |  | Acceleration Mps Parallel |
| answer-synthesis | 2026-06-29 | docs/issues/answer-synthesis/retrospective.md | Answer Synthesis |
| davinci-resolve-knowledge-domain | 2026-06-27 |  | Davinci Resolve Knowledge Domain |
| davinci-resolve-real-world-eval | 2026-06-30 |  | Davinci Resolve Real World Eval |
| davinci_resolve_2026-06-30 | unknown |  | Davinci_Resolve_2026 06 30 |
| gap-closing-godot-gotchas | 2026-06-30 |  | Gap Closing Godot Gotchas |
| godot-005-fix | 2026-06-30 | docs/issues/godot-005-fix/retrospective.md | Godot 005 Fix |
| godot-007-fix | 2026-06-30 | docs/issues/godot-007-fix/retrospective.md | Godot 007 Fix |
| godot-gap-closing-report | 2026-06-30 |  | Godot Gap Closing Report |
| godot-real-world-eval | 2026-06-30 |  | Godot Real World Eval |
| godot-rst-parser | 2026-06-10 |  | Godot Rst Parser |
| godot_2026-06-30 | unknown |  | Godot_2026 06 30 |
| improvement-roadmap-phase1-low-hanging-fruit | 2026-06-30 |  | Improvement Roadmap Phase1 Low Hanging Fruit |
| improvement-roadmap-phase2-embedding-upgrade | 2026-06-30 |  | Improvement Roadmap Phase2 Embedding Upgrade |
| improvement-roadmap-phase3-advanced-rag | 2026-06-30 |  | Improvement Roadmap Phase3 Advanced Rag |
| jina-reranker-test | 2026-07-01 | docs/issues/jina-reranker-test/retrospective.md | Jina Reranker Test |
| knowledge-hub | 2026-06-09 |  | Knowledge Hub |
| knowledge-hub-opencode-standard-migration | 2026-06-29 | docs/issues/knowledge-hub-opencode-standard-migration/retrospective.md | Knowledge Hub Opencode Standard Migration |
| knowledge-hub-quality-evaluation-platform | 2026-06-29 |  | Knowledge Hub Quality Evaluation Platform |
| knowledge-hub-quality-evaluation-platform-phase-1 | 2026-06-29 | docs/issues/knowledge-hub-quality-evaluation-platform-phase-1/retrospective.md | Knowledge Hub Quality Evaluation Platform Phase 1 |
| knowledge-hub-quality-evaluation-platform-phase-2 | 2026-06-29 | docs/issues/knowledge-hub-quality-evaluation-platform-phase-2/retrospective.md | Knowledge Hub Quality Evaluation Platform Phase 2 |
| knowledge-hub-test-suite | 2026-06-28 |  | Knowledge Hub Test Suite |
| phase-1-review | 2026-06-09 |  | Phase 1 Review |
| phase-2-final-review | 2026-06-09 |  | Phase 2 Final Review |
| phase-3-1-contextual-retrieval | 2026-07-02 |  | Phase 3 1 Contextual Retrieval |
| phase-3-1-contextual-retrieval-no-go | 2026-07-04 | docs/issues/phase-3-1-contextual-retrieval-no-go/retrospective.md | Phase 3 1 Contextual Retrieval No Go |
| phase-3-2-contextual-bm25 | 2026-07-04 | docs/issues/phase-3-2-contextual-bm25/retrospective.md | Phase 3 2 Contextual Bm25 |
| phase-3-3a-acceleration | 2026-07-04 | docs/issues/phase-3-3a-acceleration/retrospective.md | Phase 3 3A Acceleration |
| phase-3-review | 2026-06-09 |  | Phase 3 Review |
| phase1-low-hanging-fruit | 2026-06-30 | docs/issues/phase1-low-hanging-fruit/retrospective.md | Phase1 Low Hanging Fruit |
| phase2a-bge-m3-quality-gate | 2026-06-30 | docs/issues/phase2a-bge-m3-quality-gate/retrospective.md | Phase2A Bge M3 Quality Gate |
| phase2b-golden-dataset-late-chunking | 2026-07-02 | docs/issues/phase2b-golden-dataset-late-chunking/retrospective.md | Phase2B Golden Dataset Late Chunking |
| quality-evaluation-followups | 2026-06-29 |  | Quality Evaluation Followups |
| real-world-source-evaluation | 2026-06-29 | docs/issues/real-world-source-evaluation/retrospective.md | Real World Source Evaluation |
| retrieval-2-0 | 2026-06-09 |  | Retrieval 2 0 |

## Cleanup-Tasks

- [ ] `docs/superpowers.bak-migration/` löschen nach Verifikation (Rollback nicht mehr nötig)
- [ ] Referenzen in AGENTS.md, docs/ai/README.md, .opencode/agents/*.md auf neue Struktur umstellen
