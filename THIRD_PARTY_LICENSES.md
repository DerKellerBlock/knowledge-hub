# Third-Party Licenses

This file lists all third-party software used by the Knowledge Hub project.

## MIT-Licensed Dependencies (Runtime)

These packages are imported by the MIT-licensed Knowledge Hub runtime code.

| Package | License | Purpose |
|---------|---------|---------|
| chromadb | Apache-2.0 | Vector database for semantic search |
| sentence-transformers | Apache-2.0 | Embedding models for semantic search |
| mcp | MIT | Model Context Protocol server |
| rank-bm25 | Apache-2.0 | BM25 sparse retrieval |
| einops | Apache-2.0 | Tensor reshaping utilities — imported by the jina-reranker-v2 custom code (see CC-BY-NC-4.0 section below). No-op for the default ms-marco MiniLM reranker. |

## MIT-Licensed Model Weights (Runtime, Configurable Embedding)

These embedding model weights are downloaded on demand at index-build
and query time. The default is `all-mpnet-base-v2` (English-only); the
Phase-2a override is `BAAI/bge-m3` (multilingual), selectable via the
`KH_EMBEDDING_MODEL` environment variable. Both are MIT-licensed.

### BAAI/bge-m3

- **Repository:** https://huggingface.co/BAAI/bge-m3
- **License:** MIT
- **Copyright:** Beijing Academy of Artificial Intelligence (BAAI)
- **Usage:** Phase-2a default embedding model. Multilingual (100+
  languages incl. German), 1024 dims, 8192 token context, ~2.2 GB
  download on first use. Selectable via
  `KH_EMBEDDING_MODEL=BAAI/bge-m3` (Decision 2.2).
- **License file:** https://huggingface.co/BAAI/bge-m3/blob/main/LICENSE

### sentence-transformers/all-mpnet-base-v2

- **Repository:** https://huggingface.co/sentence-transformers/all-mpnet-base-v2
- **License:** Apache-2.0
- **Copyright:** sentence-transformers (UKPLab)
- **Usage:** Default embedding model (fallback). English-only, 768
  dims, 384 token context, ~420 MB download. Used when
  `KH_EMBEDDING_MODEL` is unset and `domain.md` does not override.

## MIT-Licensed Dependencies (Dev / Quality Evaluation Platform)

These packages are imported ONLY by the development-time Quality
Evaluation Platform (`scripts/quality/`, `tests/quality/`) and the
test suite. The MIT-licensed runtime code NEVER imports them.

| Package | License | Purpose |
|---------|---------|---------|
| pyyaml | MIT | YAML parser for Golden Dataset files (`quality/golden/*.yaml`) and pytest configuration |
| pytest | MIT | Test runner |
| pytest-asyncio | Apache-2.0 | Async test support for MCP contract tests |
| pytest-cov | MIT | Coverage reporting |

## CC-BY-NC-4.0 Licensed Dependencies (Runtime, Configurable)

These model weights are downloaded on demand at query time and are
**optional** — the Knowledge Hub defaults to the MIT-context ms-marco
MiniLM reranker (see above) and only switches to these weights if the
operator sets `KH_RERANKER_MODEL=<id>`. They are loaded by the
MIT-licensed `sentence-transformers` library, but the model artifacts
themselves carry a non-commercial license.

Acceptable for Noah's personal local Hub (no commercial distribution).
A shared or commercial deployment would need a different reranker or a
commercial Jina AI license.

### jinaai/jina-reranker-v2-base-multilingual

- **Repository:** https://huggingface.co/jinaai/jina-reranker-v2-base-multilingual
- **License:** CC-BY-NC-4.0 (Creative Commons Attribution-NonCommercial 4.0)
- **Copyright:** Jina AI GmbH
- **Usage:** Optional Stage-2 reranker. Multilingual (cross-lingual DE↔EN),
  1024 token context, 278M parameters, ~1.1 GB download on first use.
  Selectable via `KH_RERANKER_MODEL=jinaai/jina-reranker-v2-base-multilingual`.
- **License file:** https://huggingface.co/jinaai/jina-reranker-v2-base-multilingual/blob/main/LICENSE
- **Custom code:** The model ships an `auto_map` in `config.json`; we
  pass `trust_remote_code=True` to `CrossEncoder(...)` in
  `scripts/model_manager.py::get_reranker()`. The default ms-marco
  MiniLM has no `auto_map` and ignores this flag.

## AGPL-Licensed Dependencies (Build Tool Only)

These packages are imported ONLY by `scripts/parse_pdf_to_markdown.py`,
a standalone build tool that runs via subprocess. The MIT-licensed
Knowledge Hub runtime code NEVER imports these packages.

### PyMuPDF

- **Repository:** https://github.com/pymupdf/PyMuPDF
- **License:** GNU AGPL v3.0 (or commercial license from Artifex)
- **Copyright:** Artifex Software, Inc.
- **Usage:** PDF text extraction with font/position metadata
- **License file:** See https://github.com/pymupdf/PyMuPDF/blob/master/COPYING

### PyMuPDF4LLM

- **Repository:** https://github.com/pymupdf/pymupdf4llm
- **License:** GNU AGPL v3.0 (or commercial license from Artifex)
- **Copyright:** Artifex Software, Inc.
- **Usage:** PDF → Markdown conversion for RAG pipelines
- **License file:** See https://github.com/pymupdf/pymupdf4llm/blob/main/LICENSE

### Process Boundary Explanation

The Knowledge Hub uses the "Process Boundary" principle to keep its
MIT license while using AGPL-licensed PyMuPDF:

1. `scripts/parse_pdf_to_markdown.py` imports PyMuPDF (AGPL) and runs
   as a standalone script via `python scripts/parse_pdf_to_markdown.py`.
2. The MIT-licensed runtime (`embed_index.py`, `hybrid_search.py`,
   `mcp_servers/`) reads only the resulting `.md` files — it never
   imports PyMuPDF.
3. This is analogous to calling GCC (GPL) from a proprietary build
   system: separate processes are separate works.

See: https://www.gnu.org/licenses/gpl-faq.en.html#GPLInProprietarySystem