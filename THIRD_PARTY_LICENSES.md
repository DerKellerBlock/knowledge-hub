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