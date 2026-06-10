# Known Issues — Knowledge Hub

## Behobene Probleme

- **KI-001:** Phase 1+2 abgeschlossen (2026-06-09) — Alle Kern-Komponenten implementiert
- **KI-002:** Godot-Skills ins Hub migriert — Skills sind Single Source of Truth
- **TD-001:** ChromaDB-Integration getestet — 265 MB Index, 18.222 Chunks, Cosine-Metrik
- **KI-003:** Retrieval 2.0 implementiert (2026-06-10) — BM25 ersetzt ripgrep, Cross-Encoder-Reranking, Plugin-basiertes strukturiertes Parsing

## Technische Schulden

- **TD-002:** Keine Test-Suite (pytest/bats) — optional, geringe Prio

## Einschränkungen

- **LIM-001:** MCP-Server nur stdio (kein HTTP/SSE) — akzeptabel für persönlichen Hub
- **LIM-002:** Godot-Parser produziert aktuell 0 strukturierte Chunks (Regex muss auf echtes RST angepasst werden) — Fallback-Chunking greift korrekt
