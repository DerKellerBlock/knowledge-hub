# Security — Knowledge Hub

## Baseline

- No secrets, API keys or tokens in tracked files.
- Use environment variables for credentials.
- Do not index private data accidentally through `domains/*/sources/` or `personal/`.
- Treat external source ingestion as untrusted until reviewed.
- Avoid unsafe shell patterns and always quote paths.
- MCP server is stdio-oriented for local OpenCode use; do not expose it publicly without a separate security plan.

## Dependency and License Checks

- Review `requirements.txt`, `requirements-dev.txt`, `requirements-pdf.txt` and `THIRD_PARTY_LICENSES.md` when dependencies change.
- Keep the PyMuPDF4LLM AGPL process-boundary decision documented in `docs/decisions/2026-06-27-agpl-process-boundary.md`.

## Known Accepted Risk

BM25 indexes use Python pickle through `rank_bm25` serialization. This is accepted for Noahs personal local Hub where index files are generated locally and not consumed from untrusted sources. A shared or production Hub would need a safer serialization format.

## Review Commands

```bash
git status --short
python3 -m json.tool .opencode/opencode.json
find . -name "*.py" -not -path "*/__pycache__/*" -exec python3 -m py_compile {} \;
find . -name "*.sh" -exec bash -n {} \;
```

If secret scanners such as `gitleaks` or SAST tools such as `semgrep` are installed, run them for security-sensitive changes and report exact findings. If unavailable, report `[skip: tool not installed]`.