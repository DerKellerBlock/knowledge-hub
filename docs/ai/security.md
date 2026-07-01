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

`trust_remote_code=True` in `scripts/model_manager.py:get_reranker()` allows HuggingFace models to execute arbitrary Python code shipped in their repository (via `auto_map` in `config.json`). This is required for `jinaai/jina-reranker-v2-base-multilingual`, which ships custom code for its `JinaReranker` class. The legacy `cross-encoder/ms-marco-MiniLM-L-12-v2` has no `auto_map` and ignores the flag. Accepted for the personal Hub: the model comes from a known vendor (Jina AI), there is no multi-tenant access, and no untrusted external input feeds the reranker. For a production or shared Hub: pin the model to a known commit hash or audit the custom code before enabling `trust_remote_code`.

## Review Commands

```bash
git status --short
python3 -m json.tool .opencode/opencode.json
find . -name "*.py" -not -path "*/__pycache__/*" -exec python3 -m py_compile {} \;
find . -name "*.sh" -exec bash -n {} \;
```

For changes touching `model_manager.py:get_reranker()` or any model loaded with `trust_remote_code=True`, additionally review the upstream model repository and confirm the commit hash matches the documented trusted source. `gitleaks`/`semgrep` are optional but recommended for security-sensitive changes.