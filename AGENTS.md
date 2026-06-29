# Knowledge Hub Agent Instructions

## Project Purpose

Knowledge Hub is Noahs personal, domain-agnostic knowledge system for technical tools such as Godot, DaVinci Resolve, Blender and future domains. It combines repository/documentation knowledge, PDF-derived sources, personal notes, embeddings, BM25, hybrid retrieval and an MCP server for OpenCode integration.

## AI Agent Onboarding

1. Read `docs/ai/README.md` first.
2. Read `docs/ai/project-context.md` for current project state.
3. Read `docs/ai/architecture.md` and `docs/ai/domain-model.md` before touching domains, search, indexes or MCP code.
4. Read `docs/ai/best-practices.md`, `docs/ai/validation.md` and `docs/ai/security.md` before implementing changes.
5. For feature work, read the relevant spec and plan under `docs/superpowers/`.
6. Never invent project facts, test results, index rebuilds, MCP starts, web sources, source citations or PDF page numbers.

## Workflow

Use the Knowledge Hub feedback loop:

```text
read-hub-docs -> inspect-hub-project -> research-knowledge-domain -> plan-hub-change -> review-hub-plan-blindspots -> implement-hub-change -> validate-hub-project -> test-hub-feature -> review-hub-security -> review-hub-diff -> update-hub-docs -> retrospect-iteration -> explain-location
```

`research-knowledge-domain` is required for new domains, new source collections, changed external-source strategy or quality checks that depend on web research.

## OpenCode Configuration

- Project config lives in `.opencode/opencode.json`.
- Agent prompts live in `.opencode/agents/*.md`.
- `orchestrator-knowledge` is the primary agent.
- Task permission names must match real agent filenames without `.md`.
- Do not inline large agent prompts in `.opencode/opencode.json`.

## Validation

Use:

```bash
./scripts/workspace_check.sh
./scripts/workspace_status.sh
pytest -m unit
pytest -m integration
pytest -m e2e
pytest -m mcp
```

Skip unavailable or irrelevant test stages with an explicit `[skip: <reason>]`. Never invent successful test or scan results.

## Knowledge Quality Standard

Knowledge Hub changes should improve practical retrieval quality, not only compile. For source or domain changes, quality review should check:

- relevant answers for realistic user questions
- source filename in results
- PDF page metadata when available
- clear evidence snippets
- documented gaps when retrieval is weak

For PDF-derived domains, missing page metadata must be reported as `[fail: missing page metadata]` for the affected result.

## Safety Rules

- Do not modify `chromadb_data/` unless a plan explicitly requires an index migration.
- Do not rebuild indexes unless the user approves it.
- Do not commit `.coverage*`, local caches, virtualenvs or generated ChromaDB data.
- Do not store secrets in config or personal notes.
- Do not commit without explicit user approval.