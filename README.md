# Knowledge Hub

Noah's persönlicher, domain-agnostischer Knowledge Hub für technisches Wissen über mehrere Tools: Godot, Blender, DaVinci Resolve, FreeCAD und mehr.

## Quick Start

```bash
# Abhängigkeiten
brew install repomix ripgrep
pip install -r requirements.txt

# Godot-Skills in ein Projekt installieren
./install.sh ~/my-godot-project godot

# Status prüfen
./domains/godot/scripts/status.sh
```

## Was ist hier?

- **Repo-Wissen** — Automatisch aus Dokumentationen und Code-Repos gescraped (via repomix)
- **Persönliches Wissen** — FAQs, Gotchas, Best Practices aus Noahs Erfahrung
- **Embedding-Index** — Semantische Suche via ChromaDB + MPNet
- **MCP-Server** — Native OpenCode-Integration

## Struktur

| Ordner | Inhalt |
|--------|--------|
| `domains/` | Wissensdomains (Godot, Blender, …) |
| `scripts/` | Infrastruktur: Index, Suche |
| `mcp_servers/` | MCP-Server für OpenCode |
| `.agents/skills/` | OpenCode-Skills (Single Source of Truth) |
| `docs/` | Dokumentation (für Menschen + AI-Agenten) |

## Für AI-Agenten

Starte mit `AGENTS.md`. Danach liest du `docs/ai/README.md`, `docs/ai/project-context.md`, `docs/ai/architecture.md`, `docs/ai/domain-model.md`, `docs/ai/validation.md` und `docs/ai/security.md`.

OpenCode-Projektkonfiguration liegt in `.opencode/opencode.json`; Agentenprompts liegen in `.opencode/agents/*.md`.
