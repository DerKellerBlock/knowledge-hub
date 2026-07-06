# Knowledge Hub OpenCode Standard Migration Design

**Date:** 2026-06-29  
**Status:** Approved for migration planning  
**Owner:** Knowledge Hub  
**Pattern:** Single-Repo-Projekt, kein Meta/Sibling-Workspace

## Ziel

`knowledge-hub` soll auf Noahs aktuellen agentenfreundlichen Standard migriert werden, ohne die bestehende Single-Repo-Struktur aufzugeben. Der wichtigste fehlende Teil ist die nachvollziehbare OpenCode-Konfiguration: Agenten sollen nicht mehr als lange Inline-Blöcke in `.opencode/opencode.json` versteckt sein, sondern als einzelne `.opencode/agents/*.md` Dateien versioniert, reviewbar und dokumentiert werden.

Zusätzlich soll der Workflow vom reinen Struktur-/Syntax-Check auf einen Knowledge-Hub-spezifischen Qualitätsprozess erweitert werden. Der neue `test-hub-feature` Agent prüft nicht nur Python-/MCP-Tests, sondern bewertet auch, ob der Hub qualitative Mehrwerte liefert: richtige Quellen, nachvollziehbare Seitenzahlen, sinnvolle Antworten auf realistische Probleme und klare Findings, wenn Quellen- oder Seitenmetadaten fehlen.

## Entscheidung

Wir verwenden Ansatz B: **Single-Repo-Standard-Migration + Knowledge-QA**.

Ansatz C, eine dauerhafte Qualitätsplattform mit Golden Dataset, Scoring, Reports und gespeicherten Real-World-Testfragen, wird bewusst als späteres eigenes Feature behandelt. Diese Migration schafft nur die Struktur, Agenten und Regeln, damit solche Qualitätsprüfungen report-only durchgeführt und später sauber produktisiert werden können.

## Bestehender Zustand

Stand der Inspektion am 2026-06-29:

- `knowledge-hub` ist ein bestehendes Git-Repo unter `/Users/noahk/Documents/work/knowledge-hub`.
- Es gibt bereits `.opencode/opencode.json` mit `default_agent: orchestrator-knowledge`.
- Die Agenten sind aktuell inline unter `.opencode/opencode.json#/agent` definiert.
- Es gibt kein `AGENTS.md` im Repo-Root.
- Es gibt keine `.opencode/agents/*.md` Agent-Dateien.
- `docs/ai/` existiert, ist aber nicht vollständig auf dem aktuellen Standard:
  - vorhanden: `README.md`, `project-context.md`, `architecture.md`, `domain-model.md`, `best-practices.md`, `decisions.md`, `known-issues.md`, `validation.md`, `changelog.md`
  - fehlt: `security.md`, `fixes.md`, `handoffs/.gitkeep`
- `docs/superpowers/` enthält `specs/`, `plans/`, `reviews/`; es fehlen `explanations/` und `retrospectives/`.
- Eine Test-Suite existiert bereits (`tests/unit`, `tests/integration`, `tests/e2e`, `tests/mcp`), aber `docs/ai/known-issues.md` enthält noch eine veraltete Aussage über fehlende Tests.
- Der aktuelle Git-Status enthält uncommitted Änderungen an `domains/davinci_resolve/sources/*.md` und untracked `.coverage*` Dateien. Die Migration darf diese Dateien nicht verändern.

## Zielstruktur

```text
knowledge-hub/
├── AGENTS.md
├── .opencode/
│   ├── opencode.json
│   └── agents/
│       ├── orchestrator-knowledge.md
│       ├── read-hub-docs.md
│       ├── inspect-hub-project.md
│       ├── research-knowledge-domain.md
│       ├── plan-hub-change.md
│       ├── review-hub-plan-blindspots.md
│       ├── implement-hub-change.md
│       ├── validate-hub-project.md
│       ├── test-hub-feature.md
│       ├── review-hub-security.md
│       ├── review-hub-diff.md
│       ├── update-hub-docs.md
│       ├── retrospect-iteration.md
│       └── explain-location.md
├── scripts/
│   ├── workspace_check.sh
│   └── workspace_status.sh
└── docs/
    ├── ai/
    │   ├── security.md
    │   ├── fixes.md
    │   └── handoffs/.gitkeep
    └── superpowers/
        ├── explanations/.gitkeep
        └── retrospectives/.gitkeep
```

## OpenCode-Konfigurationsdesign

`.opencode/opencode.json` wird schlank gehalten und bleibt die zentrale Projektkonfiguration für:

- `$schema`
- `default_agent`
- `model`
- `small_model`
- `compaction`
- `instructions`
- globale `permission`
- `mcp`

Die Agentendefinitionen werden aus dem JSON herausgelöst. Jede Agent-Datei nutzt OpenCode-Frontmatter:

```markdown
---
description: Kurzbeschreibung
mode: primary|subagent
model: provider/model
steps: 30
permission:
  edit: deny
  bash:
    "*": ask
---

Agent prompt body.
```

Wichtig: Task-Permissions müssen echte Agent-Dateinamen verwenden. Abgekürzte Namen wie `plan`, `review` oder `docs` sind verboten, weil OpenCode-Pattern-Matching literal arbeitet und die letzte passende Regel gewinnt.

## Agenten-Workflow

Der Knowledge-Hub-Workflow wird:

```text
read-hub-docs
→ inspect-hub-project
→ research-knowledge-domain      # nur bei neuen/geänderten Wissensquellen oder Domains
→ plan-hub-change
→ review-hub-plan-blindspots
→ implement-hub-change
→ validate-hub-project           # Struktur, JSON, Bash, Python-Syntax
→ test-hub-feature               # pytest + Knowledge-QA report-only
→ review-hub-security            # Secrets, Dependencies, MCP-/Path-Risiken
→ review-hub-diff
→ update-hub-docs
→ retrospect-iteration
→ explain-location
```

`orchestrator-knowledge` bleibt der Primary-Agent und delegiert Schreibzugriffe an `implement-hub-change` beziehungsweise `update-hub-docs`. Der Orchestrator selbst bleibt edit-deny.

## `test-hub-feature` als Knowledge-QA-Agent

`test-hub-feature` hat zwei Ebenen.

### Ebene 1: Technische Tests

Der Agent liest zuerst:

- `docs/ai/validation.md`
- `docs/testing.md`
- relevante Specs und Plans

Dann führt er abhängig vom Diff aus:

```bash
pytest -m unit
pytest -m integration
pytest -m e2e
pytest -m mcp
```

Wenn ein Test nicht relevant ist oder Voraussetzungen fehlen, meldet der Agent `[skip: <reason>]` statt Ergebnisse zu erfinden.

### Ebene 2: Knowledge-QA

Für betroffene Domains prüft der Agent, ob der Knowledge Hub praktischen Nutzen erzeugt:

1. Betroffene Quellen identifizieren, etwa `domains/davinci_resolve/sources/*.md`.
2. Quellbasierte Testfragen ableiten, deren Antwort in den Quellen stehen muss.
3. Real-World-Fragen per Websearch finden und als Plausibilitäts-Check nutzen.
4. Den Hub mit `search_knowledge` oder den vorhandenen Suchskripten abfragen.
5. Ergebnisse bewerten:
   - Relevanz der Top-Treffer
   - vorhandene `source_file`
   - vorhandene `page_start` / `page_end` bei PDF-basierten Domains
   - nachvollziehbare Antwortanker im Text
   - Lücken, die als Verbesserung dokumentiert werden sollten

Der Agent schreibt keine neuen Testdaten und verändert keine Quellen. Er berichtet Findings im Format:

```text
[pass|weak|fail] <kurzer Titel>
Domain: <domain>
Question: <Frage>
Real-world source: <URL oder [not used]>
Hub source: <source_file>
Pages: <page_start-page_end oder [missing]>
Evidence: <kurzer Ausschnitt oder Ergebnisbeschreibung>
Human follow-up: <konkrete Empfehlung>
```

Für PDF-derived Domains gilt: Wenn Treffer keine Seitenmetadaten haben, meldet der Agent `[fail: missing page metadata]` für das betroffene Ergebnis. Das blockiert nicht automatisch jede Migration, ist aber ein Qualitätsfinding, das priorisiert werden muss.

## Dokumentationsdesign

`AGENTS.md` wird Root-Onboarding für AI-Agenten:

1. `docs/ai/README.md` lesen.
2. `docs/ai/project-context.md` lesen.
3. `docs/ai/architecture.md` und `docs/ai/domain-model.md` lesen.
4. Vor Änderungen `docs/ai/best-practices.md`, `docs/ai/validation.md`, `docs/ai/security.md` lesen.
5. Bei größeren Änderungen Plan in `docs/superpowers/plans/` erstellen.
6. Keine Projektfakten, Testergebnisse, Index-Läufe oder Quellen erfinden.

`docs/ai/validation.md` wird um die Trennung Struktur-Validation vs. Test/Knowledge-QA ergänzt.

`docs/ai/security.md` dokumentiert Baseline:

- keine Secrets
- keine ungeprüften externen Downloads
- keine private Daten versehentlich indexieren
- MCP-Server stdio-only
- Dependency-/Lizenzrisiken
- Pickle-Risiko für BM25-Indizes als bewusst akzeptierte persönliche-Hub-Grenze

## Schutzregeln für die Migration

- Keine Änderungen an `domains/davinci_resolve/sources/*.md`.
- Keine Änderungen an `chromadb_data/`.
- Keine Index-Rebuilds.
- Keine Löschung bestehender `.git/`-Daten.
- Keine Commits ohne explizite Nutzerfreigabe.
- `.coverage*` Dateien nicht inhaltlich anfassen; nur `.gitignore` darf sie künftig ignorieren, wenn das Teil des Plans bleibt.
- Bestehende Inline-Agent-Prompts müssen vollständig erhalten bleiben oder bewusst ersetzt und im Diff reviewbar gemacht werden.

## Erfolgskriterien

1. `.opencode/opencode.json` ist valides JSON und enthält keine Inline-Agenten mehr.
2. Alle Agenten liegen als `.opencode/agents/*.md` vor.
3. `default_agent` zeigt auf `orchestrator-knowledge`.
4. Task-Permissions des Orchestrators matchen echte Agent-Dateinamen.
5. `AGENTS.md` existiert und beschreibt das Onboarding.
6. `scripts/workspace_check.sh` läuft erfolgreich.
7. `scripts/workspace_status.sh` zeigt Projektstatus, OpenCode-Dateien, Docs und Git-Status nachvollziehbar an.
8. `docs/ai/validation.md` beschreibt technische Tests und Knowledge-QA.
9. `docs/ai/security.md` existiert.
10. `docs/ai/known-issues.md` enthält keine veraltete Aussage, dass es keine Test-Suite gibt.
11. Bestehende uncommitted Domain-Quellen bleiben unverändert.

## Folgefeature: Ansatz C

Nach dieser Migration kann ein eigenes Feature geplant werden:

**Knowledge Hub Quality Evaluation Platform**

Mögliche Inhalte:

- dauerhaftes Golden Dataset pro Domain
- gespeicherte Real-World-Testfragen mit Quellen
- Bewertungsrubrik für Retrieval-Qualität
- Reports pro Domain
- Regressionen für Seitenzahlen und Quellenanker
- Tooling zur halbautomatischen Pflege von Testfragen

Dieses Folgefeature ist nicht Teil der Standard-Migration.
