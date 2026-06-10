# Decisions — Knowledge Hub

> Wichtige Architektur- und Design-Entscheidungen mit Begründung.

## Q1: Hub = Single Source of Truth

- **Entscheidung:** Skills leben im Hub-Repo (`.agents/skills/`), nicht in einzelnen Projekten. Andere Projekte installieren via `install.sh` oder konsumieren via MCP.
- **Begründung:** GitHub Public Release. Ein Update im Hub aktualisiert alle Projekte. Keine Duplizierung.
- **Datum:** 2026-06-09

## Q2: Persistente ChromaDB (on-disk)

- **Entscheidung:** ChromaDB-Index liegt persistent auf Disk (`chromadb_data/`, .gitignored).
- **Begründung:** Bei 15K+ Chunks ist in-memory zu langsam. Neuaufbau dauert ~5 Minuten — das passiert nur bei `embed_index.py`, nicht bei jeder Query.
- **Datum:** 2026-06-09

## Q3: MPNet statt MiniLM

- **Entscheidung:** `all-mpnet-base-v2` (420 MB, 768 dims) als Embedding-Model.
- **Begründung:** Höhere Genauigkeit (~85%+ vs ~80%) priorisiert. 420 MB Download und ~5 Min Index-Zeit akzeptabel für persönlichen Hub.
- **Datum:** 2026-06-09

## Q4: Markdown für persönliches Wissen

- **Entscheidung:** Noahs Notizen als Freitext-Markdown mit `##`-Headern, nicht als strukturiertes YAML.
- **Begründung:** Schreibfreundlicher. ChromaDB-Chunking macht Inhalte trotzdem präzise durchsuchbar.
- **Datum:** 2026-06-09

## Q5: Kompletter Index-Neuaufbau (nicht inkrementell)

- **Entscheidung:** Bei jedem `embed_index.py`-Aufruf wird die ChromaDB-Collection komplett gelöscht und neu gebaut.
- **Begründung:** Einfachste Implementierung. Keine Deduplizierungs-Bugs, keine inkrementellen Edge-Cases. Index-Zeit (~5 Min) ist akzeptabel für wöchentliche Updates.
- **Datum:** 2026-06-09

## Architecture Decisions

### AD-001: Ein MCP-Server für alle Domains

- **Entscheidung:** Ein MCP-Server bedient alle Domains (domain als Parameter), nicht pro Domain ein Server.
- **Begründung:** Kein Multi-Port-Overhead. Neue Domains werden automatisch erkannt (Scan von `domains/` beim Server-Start). 4 Domains × 1 Server = sauber. 4 Domains × 4 Server = Overkill.

### AD-002: CLI + MCP (nicht nur CLI)

- **Entscheidung:** Knowledge-Operationen sind sowohl via CLI (`scripts/*.py`) als auch via MCP-Server zugänglich.
- **Begründung:** CLI für Entwicklung/Debugging, MCP für OpenCode-Integration. Gleiche Codebase, zwei Interfaces.

### AD-003: repomix für Scraping (nicht eigene Crawler)

- **Entscheidung:** Externe Quellen werden via repomix (`--remote`) gescraped, nicht mit eigenen HTTP/HTML-Parsern.
- **Begründung:** repomix 1.14.1 ist battle-tested, handled Git-Logik, Token-Counting, Compression. Eigenbau wäre signifikant mehr Aufwand.

## Q6: BM25 ersetzt ripgrep

- **Entscheidung:** BM25 (`rank_bm25`) ersetzt ripgrep komplett als exakten Retrieval-Pfad in der hybriden Suche.
- **Begründung:** BM25 liefert Relevanz-Scores (kontinuierlich) statt binärer Treffer. Bessere Fusions-Qualität mit ChromaDB über RRF, da beide Pfade echte Scores liefern. Keine Shell-Subprocess-Latenz. `rank_bm25` läuft in-memory im gleichen Python-Prozess.
- **Datum:** 2026-06-10

## Q7: Cross-Encoder-Reranking

- **Entscheidung:** Stage-2-Reranking mit `ms-marco-MiniLM-L-12-v2` als Cross-Encoder nach der RRF-Fusion.
- **Begründung:** Cross-Encoder bewertet Query-Dokument-Paare direkt (nicht nur Embedding-Ähnlichkeit), was präzisere Top-10-Rankings liefert. ~140 MB Modell, ~50–100 ms pro Reranking-Durchlauf — akzeptabel für persönlichen Hub.
- **Datum:** 2026-06-10
