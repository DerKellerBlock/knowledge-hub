# Known Issues — Knowledge Hub

## Aktive Probleme

- **KI-001:** Phase 1 (Foundation) noch nicht abgeschlossen
  - **Beschreibung:** Basis-Struktur existiert, aber keine der Kern-Komponenten (embed_index.py, MCP-Server) ist implementiert.
  - **Betroffene Dateien:** Alle
  - **Status:** Offen

- **KI-002:** Godot-Skills liegen noch im Spiel-Projekt
  - **Beschreibung:** Die `.agents/skills/godot/` existieren nur in `nak-hopper-game/`, nicht im Hub. Migration steht aus.
  - **Betroffene Dateien:** `.agents/skills/`, `install.sh`
  - **Status:** Offen

## Technische Schulden

- **TD-001:** ChromaDB-Integration nicht getestet
  - **Beschreibung:** `scripts/embed_index.py` ist noch nicht implementiert. Theoretische Architektur steht, praktische Validierung fehlt.
  - **Empfohlene Lösung:** Phase 2 (Embeddings) abarbeiten.

- **TD-002:** Keine Test-Suite
  - **Beschreibung:** Keine Unit-Tests für Python-Skripte oder Shell-Skripte.
  - **Empfohlene Lösung:** pytest für Python, bats oder shunit2 für Shell (optional, geringe Prio).

## Einschränkungen

- **LIM-001:** Kein Remote-Zugriff (Phase 1)
  - MCP-Server läuft nur lokal via stdio. Kein HTTP/SSE-Transport für Remote-Zugriff.
  - Akzeptabel für persönlichen Hub.
