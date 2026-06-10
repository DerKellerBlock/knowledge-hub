# Project Context — Knowledge Hub

## Projekt

- **Name:** Knowledge Hub
- **Beschreibung:** Persönlicher, domain-agnostischer Knowledge Hub für Noahs technisches Wissen. Vereinigt Repo-Wissen (automatisch gescraped via repomix) mit persönlichem Erfahrungswissen (FAQs, Gotchas, Best Practices).
- **Repository:** `~/Documents/work/knowledge-hub`
- **Ziel:** Single Source of Truth für alle technischen Wissensdomains. Installierbar als OpenCode-Skill in andere Projekte.

## Technologie-Stack

- **Sprachen:** Bash (CLI-Skripte), Python 3.11+ (Embedding-Pipeline, MCP-Server)
- **Embedding-Model:** all-mpnet-base-v2 (768 dims, ~420 MB)
- **Cross-Encoder:** ms-marco-MiniLM-L-12-v2 (384 dims, ~140 MB)
- **Vector-DB:** ChromaDB (persistent, on-disk)
- **BM25-Tokenizer:** rank-bm25 (Python, in-memory)
- **Scraping:** repomix 1.14.1 (via Homebrew)
- **Suche:** BM25 (exakt) + ChromaDB (semantisch) + RRF-Fusion + Cross-Encoder-Reranking (hybrid)
- **MCP-Server:** Python MCP SDK (stdio transport)
- **OpenCode:** `.opencode/opencode.json` (orchestrator-knowledge)

## Ordnerstruktur

- `domains/` — Wissensdomains (autarke Module)
- `scripts/` — Generische Infrastruktur (embed_index.py, embed_search.py, hybrid_search.py)
- `mcp_servers/` — MCP-Server für OpenCode-Integration
- `.agents/skills/` — OpenCode-Skills (Single Source of Truth)
- `chromadb_data/` — ChromaDB-Index (.gitignored, ~80-120 MB)
- `personal/` — Domain-übergreifende Notizen
- `docs/` — Projektdokumentation

## Setup (neue Maschine)

```bash
# 1. Repo klonen
git clone <url> knowledge-hub
cd knowledge-hub

# 2. Abhängigkeiten installieren
brew install repomix
pip install -r requirements.txt

# 3. Ersten Index bauen
python scripts/embed_index.py --domain godot

# 4. MCP-Server testen
python -m mcp_servers.knowledge_hub.server --help
```

## Team / Kontakt

- **Verantwortlich:** Noah
- **Status:** Phase 2 (Retrieval 2.0)
