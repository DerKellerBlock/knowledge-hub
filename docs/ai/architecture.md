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
│  └── hybrid_search.py ← rg + ChromaDB    │
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
   - Chunking (500 Tokens, 100 Overlap) → Embedding (MPNet, 768 dims) → ChromaDB Collection `<name>_knowledge`
   - Collection wird komplett neu gebaut (kein inkrementelles Update)

3. **Suche:**
   - `scripts/hybrid_search.py --domain godot --query "..." --mode hybrid`
   - Parallel: ripgrep (exakt) + ChromaDB (semantisch) → RRF-Fusion (k=60) → Top-10 Ranking

4. **MCP-Server:**
   - `mcp_servers/knowledge_hub/server.py` — stdio MCP-Server
   - Tools: search_knowledge, get_domain_status, update_domain, add_personal_note, list_domains

## Komponenten

| Komponente | Verantwortung | Eingabe | Ausgabe |
|-----------|--------------|---------|---------|
| `embed_index.py` | Index-Bau | Quell-Dateien (.md) | ChromaDB-Collection |
| `embed_search.py` | Semantische Query | Query-String | JSON-Result |
| `hybrid_search.py` | Fusion rg + Embeddings | Query-String | JSON-Result (geranked) |
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
