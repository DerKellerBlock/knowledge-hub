# Knowledge Hub — Dokumentation

Zentrale Anlaufstelle für Menschen und AI-Agenten (OpenCode), die am persönlichen Knowledge Hub arbeiten. Der Hub bündelt Noahs technisches Wissen über mehrere Tools (Godot, Blender, DaVinci Resolve, FreeCAD, …) — strukturiert, durchsuchbar und versioniert.

## Wie diese Doku gelesen werden soll

- Neue Mitwirkende starten hier und lesen danach die Bereichsdokumente.
- AI-Agenten lesen zusätzlich `docs/ai/README.md`.
- Entscheidungen werden mit Kontext, Begründung und Konsequenzen dokumentiert.
- Unbekanntes bleibt als offene Frage markiert. Keine Details erfinden.

## Bereiche

| Bereich | Zweck |
|--------|-------|
| `domains/` | Wissensdomains (Godot, Blender, …) — autarke Module mit Quellen, persönlichem Wissen und CLI |
| `scripts/` | Generische Infrastruktur: Embedding-Index, semantische Suche, Hybrid-Search |
| `mcp_servers/` | MCP-Server für OpenCode-Integration (ein Server, alle Domains) |
| `.agents/skills/` | OpenCode-Skills (Single Source of Truth) |
| `docs/ai/` | Projektkontext, Architektur und Regeln für AI-Agenten |
| `docs/superpowers/` | Design-Specs und Implementierungspläne |

## Wichtige Startdateien

- `docs/ai/project-context.md` — Projektübersicht, Setup, Versionen
- `docs/ai/architecture.md` — Architektur, Datenfluss, Komponenten
- `docs/ai/domain-model.md` — Wie Domains funktionieren und konfiguriert werden
- `docs/ai/best-practices.md` — Coding-Standards, Konventionen
- `docs/superpowers/specs/2026-06-09-knowledge-hub-design.md` — Vollständige Design-Spec (Q1-Q5 entschieden)

## Dokumentationsprinzipien

- **Kurz und auffindbar:** Jede Datei beantwortet eine klare Frage.
- **Lebendig:** Doku wird aktualisiert, wenn sich Architektur oder Konventionen ändern.
- **Entscheidungsorientiert:** Warum etwas entschieden wurde ist genauso wichtig wie die Entscheidung selbst.
- **Agentenfreundlich:** Dateien enthalten klare Zustandsangaben, offene Fragen und Links auf verwandte Dokumente.
