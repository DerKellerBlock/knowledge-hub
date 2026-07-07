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
| pillow | BSD-3-Clause | Image loading for the multimodal embedders (SigLIP-2 / jina-clip-v2). Used by scripts/embed_images.py and scripts/extract_pdf_images.py. |
| torch | BSD-3-Clause | Tensor computation backend for the multimodal embedders. Already a transitive dep of sentence-transformers; listed explicitly because the multimodal path uses transformers.AutoModel directly. |
| transformers | Apache-2.0 | Model loading (AutoModel / AutoProcessor) for SigLIP-2 / jina-clip-v2. Already a transitive dep of sentence-transformers; listed explicitly because the multimodal path imports it directly. |

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


### jinaai/jina-clip-v2

- **Repository:** https://huggingface.co/jinaai/jina-clip-v2
- **License:** CC-BY-NC-4.0 (Creative Commons Attribution-NonCommercial 4.0)
- **Copyright:** Jina AI GmbH
- **Usage:** Vision Retrieval Feature — optional multimodal embedding model
  (image+text joint encoder). Multilingual (89 Sprachen incl. German), 1024
  dims (Matryoshka truncatable), 512×512 image input, ~3.5 GB download on
  first use. Selectable via
  `KH_MULTIMODAL_MODEL=jinaai/jina-clip-v2`.
  Runs via `transformers.AutoModel` + `AutoProcessor` (NOT via Ollama —
  Ollama has no multimodal-embedding API, Issue #5304 open since 2024-06).
  The default `google/siglip2-so400m-patch16-512` (Apache 2.0) is
  kommerziell sicher; jina-clip-v2 is the optional multilingual override,
  analog to the existing jina-reranker-v2 (CC-BY-NC-4.0).
- **License file:** https://huggingface.co/jinaai/jina-clip-v2/blob/main/LICENSE
- **Custom code:** The model ships an `auto_map` in `config.json`; we
  pass `trust_remote_code=True` to `AutoModel.from_pretrained()` in
  `scripts/model_manager.py::get_multimodal_embedder()`. The default
  SigLIP-2 has no `auto_map` and ignores this flag.

## Apache-2.0 Licensed Model Weights (Runtime, Configurable LLM)

These model weights are downloaded on demand at index-build time for
Phase 3.1 Contextual Retrieval. The default is `gemma4:12b-mlx`
(MLX-quantized, served via Ollama). Selectable via the
`KH_LLM_MODEL` environment variable.

### gemma4:12b-mlx (Gemma 4 12B)

- **Repository:** https://ollama.com/library/gemma4
- **License:** Apache-2.0
- **Copyright:** Google LLC
- **Usage:** Phase 3.1 default LLM for Contextual Retrieval
  (LLM-generated context prefix per chunk). 12B unified model,
  256K token context, 140+ languages (incl. German), ~7.7 GB
  MLX-quantized download via `ollama pull gemma4:12b-mlx`. Runs
  on-device via Ollama (localhost:11434, MLX/Metal native on Apple
  Silicon). Selectable via `KH_LLM_MODEL=gemma4:12b-mlx`.
  Gemma 4 12B is a reasoning model — see `docs/ai/best-practices.md`
  for the `num_predict=800` requirement (Thinking-Phase overhead).
- **License file:** https://www.apache.org/licenses/LICENSE-2.0
- **Additional terms:** Google's Gemma Terms of Use
  (https://ai.google.dev/gemma/terms) may apply in addition to
  Apache-2.0. Review before redistribution.
- **Custom code:** None. Ollama loads the model without
  HuggingFace `auto_map` custom code — no `trust_remote_code=True`
  needed (safer than the jina-reranker-v2 path).


### google/siglip2-so400m-patch16-512 (SigLIP-2)

- **Repository:** https://huggingface.co/google/siglip2-so400m-patch16-512
- **License:** Apache-2.0
- **Copyright:** Google LLC
- **Usage:** Vision Retrieval Feature — default multimodal embedding model
  (image+text joint encoder). 1152 dims, 512×512 image input, English-only,
  ~1.5 GB download on first use. Selectable via
  `KH_MULTIMODAL_MODEL=google/siglip2-so400m-patch16-512` (default).
  Loaded via `transformers.AutoModel` + `AutoProcessor` (NOT via Ollama —
  Ollama has no multimodal-embedding API, Issue #5304 open since 2024-06).
  Apache-2.0 license makes it kommerziell sicher, suitable as the default
  for the MIT-licensed Knowledge Hub.
- **License file:** https://www.apache.org/licenses/LICENSE-2.0
- **Custom code:** None. SigLIP-2 has no `auto_map` in config.json —
  `trust_remote_code=True` is passed to `AutoModel.from_pretrained()`
  for compatibility with the jina-clip-v2 path but is a no-op here.

### ollama (Python HTTP client)

- **Repository:** https://github.com/ollama/ollama-python
- **License:** MIT
- **Copyright:** Ollama
- **Usage:** Lightweight HTTP client (~10 MB) for the Ollama
  system service (localhost:11434). Phase 3.1 Contextual Retrieval.
  Pulls NO transformers / PyTorch — no dependency conflict with the
  BGE-M3 / jina stack. Installed via `pip install ollama` (listed in
  `requirements.txt`). Ollama itself must be installed as a system
  service (`brew install ollama`).
- **License file:** https://github.com/ollama/ollama-python/blob/main/LICENSE

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