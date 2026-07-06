# Knowledge Hub Answer-Synthese Retrospective

## Goal
Make the Knowledge Hub orchestrator synthesize source-attributed, honest answers from `search_knowledge` results instead of forwarding raw hit lists. Apply domain-agnostic source prioritization, clarify PDF page vs. printed page, handle text truncation, and refuse to hallucinate when sources are insufficient.

## What went well
- Full feedback loop completed: read-hub-docs → inspect-hub-project → plan-hub-change → review-hub-plan-blindspots → plan revision → implement-hub-change → validate-hub-project → test-hub-feature → review-hub-security → review-hub-diff → implement-hub-change (correction) → validate-hub-project → test-hub-feature.
- Blind-spot review caught 4 critical issues (DaVinci-specific prioritization, PDF pages vs. printed pages, truncation, missing QA protocol) — plan revision was essential and significantly improved quality.
- Security review caught prompt-injection risk (orchestrator has `bash: allow`) — correction added to the prompt.
- All tests green: 78 unit, 35 integration, 12 e2e, 12 mcp.
- Cross-consistency validation confirmed all code references in spec/prompt match (`hybrid_search.py:127`, `embed_search.py:69`, etc.).
- Only 4 files touched, no pipeline, MCP server, index, or code changes — minimal diff, low risk.

## What was surprising or difficult
- `test-hub-feature` could only validate retrieval quality, not actual answer synthesis (which is only verifiable in a live OpenCode chat). 3 of 6 QA test cases were "weak" due to pre-existing retrieval ranking issues (e.g., `ui-map.md` personal TODO ranked top for a Planar Tracker query). These are follow-ups, not caused by this change.
- The first plan was too DaVinci-specific and would not have covered Godot or future domains — the blind-spot review was essential to catch this.
- Source prioritization is now hardcoded in the orchestrator prompt; a cleaner approach would be a `source_priority` field in `domain.md` (deferred to follow-up).

## Lessons learned
- Blind-spot review before implementation is high-value for prompt-only changes too, not just code changes.
- Prompt-injection risk is real when an agent with `bash: allow` processes untrusted search results — always add explicit guardrails.
- QA test cases that depend on live LLM synthesis cannot be fully automated with current tooling; manual validation remains necessary.

## What to do differently next time
- Design source prioritization as domain-configurable from the start (e.g., `source_priority` in `domain.md`) rather than hardcoding in the prompt.
- Include a prompt-injection guardrail in the spec itself, not as a post-hoc security review finding.

## Follow-up candidates
- Retrieval ranking: empty/TODO personal notes (e.g., `ui-map.md`) should not rank top — consider content-quality filter or exclude near-empty notes.
- `source_priority` field in `domain.md` as configuration, injected by MCP server into metadata.
- Live validation of answer synthesis in OpenCode chat using the 6 QA test cases from the spec.
- Book page detection (PDF page → printed book page mapping) as a separate feature.

## Uncertainties
- Actual synthesis quality in live OpenCode chat not yet validated — depends on LLM behavior with the new prompt section.
- Whether the domain-agnostic filename-keyword heuristic is sufficient for all future domains (Blender, FreeCAD, etc.) remains to be seen.

## References
- Spec: `docs/superpowers/specs/2026-06-29-answer-synthesis-design.md`
- Changed files: `.opencode/agents/orchestrator-knowledge.md`, `docs/ai/known-issues.md`, `docs/ai/changelog.md`
