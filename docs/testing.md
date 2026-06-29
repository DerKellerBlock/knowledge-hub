# Testing

The Knowledge Hub has a four-layer test suite that verifies information
retrieval actually works — content relevance, not just structure.

## Installation

```bash
pip install -r requirements-dev.txt
```

## Running Tests

```bash
# Run all tests (~15s)
pytest

# Run only fast unit tests (< 5s) — no models loaded
pytest -m unit

# Run integration tests with temporary ChromaDB + dummy data (~8s)
pytest -m integration

# Run E2E regression against real prebuilt indexes (~13s)
# Requires: chromadb_data/godot/ and chromadb_data/davinci_resolve/
pytest -m e2e

# Run MCP contract tests (~8s) — calls actual tool functions
pytest -m mcp

# Run with coverage report
pytest --cov=scripts --cov=mcp_servers/knowledge_hub --cov-report=term-missing
```

## Test Layers

| Layer | Marker | What it tests | Runtime | Dependencies |
|-------|--------|---------------|---------|--------------|
| Unit | `@pytest.mark.unit` | Pure logic (regex, cache, tokenizer, RRF fusion, Chunk dataclass) | ~4s | None (no models, no DB) |
| Integration | `@pytest.mark.integration` | Search/index pipeline with temp ChromaDB + 3 dummy markdown sources | ~8s | sentence-transformers model (cached after first run) |
| E2E | `@pytest.mark.e2e` | Real indexes return content-relevant results (godot + davinci) | ~13s | Prebuilt indexes at `chromadb_data/<domain>/` |
| MCP | `@pytest.mark.mcp` | 6 MCP tool functions return correct contracts, scope enforcement | ~8s | At least one built index for search_knowledge test |

## Building Indexes (required for E2E)

E2E tests require prebuilt indexes. Build them with:

```bash
python scripts/embed_index.py --domain godot
python scripts/embed_index.py --domain davinci_resolve
```

E2E tests automatically skip if the index directory doesn't exist.

## Known Gaps

None currently. The `page_start`/`page_end` metadata gap was fixed by
enabling `page_separators=True` in `parse_pdf_to_markdown.py` and
extending `fallback_chunk()` to extract page numbers from the
`--- end of page=N ---` markers.

## Coverage

Run `pytest --cov=scripts --cov=mcp_servers/knowledge_hub --cov-report=term-missing`
to see coverage. Core search/cache modules have 78-100% coverage. CLI scripts
(`server.py`, `embed_index.py`, `validate_search.py`, `parse_pdf_to_markdown.py`)
show 0% direct coverage because they're exercised indirectly via fixtures and
E2E tests rather than direct unit-test calls.

## Test File Structure

```
tests/
├── conftest.py                        # shared fixtures: tmp_hub, dummy_domain, indexed_dummy
├── unit/                              # fast, no models
│   ├── test_config.py
│   ├── test_model_manager.py
│   ├── test_tools.py
│   ├── test_bm25_tokenizer.py
│   ├── test_rrf_fusion.py
│   └── test_parser_base.py
├── integration/                       # temp ChromaDB + dummy data
│   ├── test_embed_index.py
│   ├── test_bm25_search.py
│   ├── test_embed_search.py
│   ├── test_hybrid_search.py
│   ├── test_personal_notes.py
│   └── test_migration.py
├── e2e/                                # real prebuilt indexes
│   ├── test_godot_regression.py
│   └── test_davinci_regression.py
└── mcp/                                # MCP tool contract tests
    └── test_mcp_contract.py
```
