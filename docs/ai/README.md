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
- `fixes.md` — completed fixes for future agents
- `security.md` — security review baseline
- `changelog.md` — AI-visible project changes
- `handoffs/` — handoff notes for future sessions
- `open-work.md` — Index der offenen Tasks (welche Issues anstehen)

Zusätzlich im übergeordneten `docs/`-Ordner:

- `README.md` — Zentrale Startseite für Menschen und AI-Agenten
- `domains/` — Domain-Dokumentation pro Tool (Godot, Blender, …)
- `issues/` — Issue-zentrierte SDD-Struktur (pro Task ein Ordner mit spec.md, plan.md, context/, retrospective.md, explanation.md)

## Lese-Reihenfolge für AI-Agenten

1. `docs/README.md` lesen, um die allgemeine Dokumentationsstruktur zu verstehen.
2. `docs/ai/open-work.md` lesen — welche Tasks sind offen? Task wählen.
3. `docs/ai/project-context.md` und `docs/ai/architecture.md` lesen, um den aktuellen Stand zu kennen.
4. `docs/ai/domain-model.md` lesen, um die Domain-Struktur zu verstehen.
5. `docs/ai/best-practices.md` vor der ersten Implementierung lesen.
6. Bei neuen Domains: `docs/issues/knowledge-hub/spec.md` für die vollständige Architektur-Spec.
7. Bei Feature-Arbeit: `docs/issues/<task-id>/`-Ordner laden (nur den ausgewählten Task, nicht alle Issues).
8. Keine Architektur-, Domain- oder Technikdetails erfinden, wenn sie nicht dokumentiert oder vom Nutzer bestätigt sind.

## Context-Loading-Rules

- **Onboarding:** Lade `AGENTS.md` → `docs/ai/README.md` → `docs/ai/open-work.md` → `docs/ai/project-context.md`. Wähle dann einen Task aus `open-work.md`.
- **Task-Bearbeitung:** Lade NUR den `docs/issues/<task-id>/`-Ordner des ausgewählten Tasks (spec.md + plan.md + context/). Lade NICHT alle `docs/issues/`-Ordner oder alle `docs/ai/`-Dateien gleichzeitig.
- **Bei Bedarf:** Lade spezifische `docs/ai/<file>.md` nur wenn der Task sie benötigt (z.B. `validation.md` für Validierung, `security.md` für Security-Review).
