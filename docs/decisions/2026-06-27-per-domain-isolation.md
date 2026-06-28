# ADR: Per-Domain ChromaDB Isolation

**Date:** 2026-06-27
**Status:** Accepted

## Context
Der Knowledge Hub lief bisher mit einer einzigen ChromaDB-Instanz für alle
Domains. Bei Hinzufügen einer DaVinci-Resolve-Domain würden beide Domains
RAM verbrauchen, auch wenn nur eine genutzt wird. Auf einem MacBook Pro M1
Max (32 GB) muss DaVinci Resolve Studio + OBS + Knowledge Hub parallel laufen.

## Decision
Jede Domain bekommt eine eigene ChromaDB-Datenbank unter
`chromadb_data/<domain>/chroma/` mit eigenem `PersistentClient` und
eigenem `chroma_memory_limit_bytes` (2 GB). Der MCP-Server akzeptiert ein
`--domains` CLI-Flag, das nur die konfigurierten Domains sichtbar macht.

## Consequences
- RAM-Isolation: nur die aktive Domain belegt Speicher.
- Zwei MCP-Prozesse (Godot + DaVinci) können parallel laufen (~1,7 GB).
- Migration des bestehenden Godot-Index nötig (automatisch mit Backup).
- `nak-hopper-game` und `video-blog` bekommen jeweils ihr `--domains` Flag.
- Embedding-Modell kann künftig per-Domain konfiguriert werden (domain.md).