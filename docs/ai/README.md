# AI Documentation — Knowledge Hub

Strukturierte Dokumentation für AI-Agenten (OpenCode), die am Knowledge Hub arbeiten.

## Dateien

- `project-context.md` — Projektübersicht, Setup, Versionen, Tools
- `architecture.md` — Architektur, Datenfluss, Komponenten
- `domain-model.md` — Wie Domains funktionieren, Domain-Konventionen
- `best-practices.md` — Coding-Standards, Konventionen, Patterns
- `decisions.md` — Wichtige Architektur- und Design-Entscheidungen
- `known-issues.md` — Bekannte Bugs und technische Schulden
- `validation.md` — Verfügbare Checks, Testbefehle

Zusätzlich im übergeordneten `docs/`-Ordner:

- `README.md` — Zentrale Startseite für Menschen und AI-Agenten
- `domains/` — Domain-Dokumentation pro Tool (Godot, Blender, …)
- `superpowers/specs/` — Design-Specs
- `superpowers/plans/` — Implementierungspläne

## Lese-Reihenfolge für AI-Agenten

1. `docs/README.md` lesen, um die allgemeine Dokumentationsstruktur zu verstehen.
2. `docs/ai/project-context.md` und `docs/ai/architecture.md` lesen, um den aktuellen Stand zu kennen.
3. `docs/ai/domain-model.md` lesen, um die Domain-Struktur zu verstehen.
4. `docs/ai/best-practices.md` vor der ersten Implementierung lesen.
5. Bei neuen Domains: `docs/superpowers/specs/2026-06-09-knowledge-hub-design.md` für die vollständige Architektur-Spec.
6. Keine Architektur-, Domain- oder Technikdetails erfinden, wenn sie nicht dokumentiert oder vom Nutzer bestätigt sind.
