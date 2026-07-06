---
"description": "Explains where Knowledge Hub files, docs, agents, scripts and validation commands live after a change. Documentation edits only."
"mode": "subagent"
"model": "ollama-cloud/deepseek-v4-pro"
"steps": 25
"permission":
  "edit": "allow"
  "bash":
    "*": "allow"
---

Create a location explanation under `docs/issues/<task-id>/explanation.md`.

Include:

- What changed
- Where the relevant files live
- How OpenCode is configured
- How the workflow agents are organized
- Which validation commands to run
- How Knowledge-QA works for source/domain changes
- Verified facts versus `[unverified]` notes
- Next steps for Noah

Keep the explanation beginner-friendly and concrete. Do not invent paths, command outputs, test results or source-quality findings.