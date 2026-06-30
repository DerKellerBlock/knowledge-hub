# Architecture — Knowledge Hub

## Überblick

```
┌─────────────────────────────────────────┐
│           Knowledge Hub                  │
│                                           │
│  domains/                                 │
│  ├── godot/  ──┐                         │
│  │   ├── sources/    (repomix output)     │
│  │   ├── personal/   (Noahs Wissen)       │
│  │   └── scripts/    (update, search)     │
│  ├── blender/ ──┤  (später)              │
│  └── freecad/  ──┘  (später)             │
│                                           │
│  scripts/                                 │
│  ├── embed_index.py   → ChromaDB         │
│  ├── embed_search.py  ← ChromaDB         │
│  └── hybrid_search.py ← BM25 + ChromaDB → Cross-Encoder │
│                                           │
│  mcp_servers/knowledge_hub/               │
│  └── OpenCode ← MCP-Tools                │
└─────────────────────────────────────────┘
```

## Datenfluss

1. **Quellen (Input):**
   - `domains/<name>/sources/*.md` — repomix-Output (Repo-Wissen)
   - `domains/<name>/personal/*.md` — Markdown-Notizen (persönliches Wissen)

2. **Indexierung:**
   - `scripts/embed_index.py --domain godot`
    - **Repo-Quellen:** `fallback_chunk()` (2000 Tokens / 8000 Zeichen, 400 Tokens Overlap / 1600 Zeichen, erhöht von 200 Tokens/800 Zeichen in Phase 1) → Embedding (MPNet, 768 dims) → ChromaDB Collection `<name>_knowledge`
   - **Personal Notes:** `markdown_section_chunk()` (Splittet an `##`-Headern in per-section Chunks, defensive Skip bei <50 Zeichen, Fallback auf `fallback_chunk()` bei Dateien ohne `##`-Header) → Embedding → ChromaDB
   - Collection wird komplett neu gebaut (kein inkrementelles Update)

3. **Suche (zweistufig):**
   - `scripts/hybrid_search.py --domain godot --query "..." --mode hybrid`
   - **Stage 1:** BM25 (exakt) + ChromaDB (semantisch) → RRF-Fusion (k=60) → Candidate-Pool
     - BM25-Tokenisierung: Unicode-aware mit CamelCase-Splitting (`CharacterBody3D` → `["character", "body", "3", "d"]`, `GPU` bleibt `["gpu"]`, deutsche Umlaute erhalten). Symmetrisch für Index und Query.
   - **Stage 2:** Cross-Encoder (ms-marco-MiniLM-L-12-v2, konfigurierbar via `KH_RERANKER_MODEL`) → Reranking → Top-10 Ranking

4. **MCP-Server:**
   - `mcp_servers/knowledge_hub/server.py` — stdio MCP-Server
   - Tools: search_knowledge, get_domain_status, update_domain, add_personal_note, list_domains

## Komponenten

| Komponente | Verantwortung | Eingabe | Ausgabe |
|-----------|--------------|---------|---------|
| `embed_index.py` | Index-Bau | Quell-Dateien (.md) | ChromaDB-Collection |
| `embed_search.py` | Semantische Query | Query-String | JSON-Result |
| `hybrid_search.py` | Fusion BM25 + Embeddings → Cross-Encoder-Rerank | Query-String | JSON-Result (geranked) |
| MCP-Server | OpenCode-Integration | MCP-Tool-Calls | JSON-Responses |

## Domain-Autonomie

Jede Domain unter `domains/<name>/` ist ein autarkes Modul:
- Eigenes `domain.md` (Konfiguration)
- Eigene `sources/` (Rohdaten)
- Eigene `personal/` (Wissen)
- Eigene `scripts/` (CLI)
- Eigene ChromaDB-Collection (`<name>_knowledge`)

Neue Domain hinzufügen:
1. `domains/<name>/` mit domain.md + Quellen anlegen
2. `python scripts/embed_index.py --domain <name>` — Index bauen
3. MCP-Server erkennt neue Domain automatisch (scannt `domains/` beim Start)

## Per-Domain Isolation (2026-06-27)

```
chromadb_data/
  godot/
    chroma/                 # eigene DB
    godot_bm25.pkl
  davinci_resolve/
    chroma/
    davinci_resolve_bm25.pkl
```

Model Manager (`scripts/model_manager.py`) ist die einzige Stelle, die
Embedding- und Reranker-Modelle lädt. Lazy-Loading, Per-Domain-Caching,
LRU-Eviction.

Domain-Scoping: `--domains` CLI-Flag auf dem MCP-Server begrenzt sichtbare
Domains. Default (ohne Flag): alle sichtbar (rückwärtskompatibel).
