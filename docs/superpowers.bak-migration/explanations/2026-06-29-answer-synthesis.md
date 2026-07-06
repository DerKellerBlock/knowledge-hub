# Answer-Synthese — Location Guide

**Datum:** 2026-06-29 | **Zielgruppe:** Anfänger im Knowledge Hub

---

## 1. Welche Dateien sich geändert haben und warum

| Datei | Was sie tut | Warum geändert |
|---|---|---|
| `docs/superpowers/specs/2026-06-29-answer-synthesis-design.md` | **NEU** — Design-Spec mit 5 Entscheidungen und 6 manuellen QA-Testfällen | Definiert, wie der Orchestrator Suchergebnisse zu ehrlichen, quellenbelegten Antworten synthetisieren soll |
| `docs/ai/known-issues.md` | Liste bekannter Einschränkungen | **LIM-002** (fehlende `section_path`/`chunk_type` bei DaVinci) und **LIM-003** (Text-Truncation auf 5000 Zeichen) |
| `docs/ai/changelog.md` | Chronik aller Projektänderungen | Eintrag für 2026-06-29 mit Verweis auf Spec und Orchestrator-Prompt-Erweiterung |
| `.opencode/agents/orchestrator-knowledge.md` | Prompt des primären Agenten | Neuer Abschnitt „Answer-Synthese": Quellenpriorisierung, PDF-Seiten, Truncation, No-Results, Zitierformat, Prompt-Injection-Schutz |

---

## 2. OpenCode-Konfiguration

- **`.opencode/opencode.json`** — Projektkonfiguration: Modell, Standard-Agent (`orchestrator-knowledge`), MCP-Server, Berechtigungen.
- **`.opencode/agents/*.md`** — 14 Agent-Prompts als Markdown mit YAML-Frontmatter (Modus, Modell, Berechtigungen). Der Markdown-Text ist der Prompt, den das LLM bei jedem Aufruf erhält.
- **Orchestrator** ist der primäre Agent. Er delegiert an Subagenten, darf selbst keine Dateien ändern. Der neue Abschnitt „Answer-Synthese" steuert, wie er `search_knowledge`-Treffer zu Antworten formt.

---

## 3. Agenten-Rollen (Übersicht)

14 Agenten arbeiten in einer festen Feedback-Schleife:

| Agent | Rolle |
|---|---|
| `orchestrator-knowledge` | Primärer Agent — koordiniert, synthetisiert Antworten |
| `read-hub-docs` | Liest Projektdokumentation |
| `inspect-hub-project` | Erkundet das Repo (lesend) |
| `research-knowledge-domain` | Recherchiert externe Quellen |
| `plan-hub-change` | Plant Änderungen (Dateien, Risiken, Doku-Bedarf) |
| `review-hub-plan-blindspots` | Prüft Pläne auf übersehene Risiken |
| `implement-hub-change` | Führt Änderungen aus |
| `validate-hub-project` | Validiert Repo (Syntax, Struktur, Index) |
| `test-hub-feature` | pytest + report-only Knowledge-QA |
| `review-hub-security` | Security-Review |
| `review-hub-diff` | Prüft Diffs auf Fehler/Regressionen |
| `update-hub-docs` | Aktualisiert Dokumentation |
| `retrospect-iteration` | Schreibt Retrospektive |
| `explain-location` | Erstellt anfängerfreundliche Erklärungen |

---

## 4. Validierungsbefehle

```bash
./scripts/workspace_check.sh                          # Strukturprüfung (muss exit 0)
./scripts/workspace_status.sh                         # Status-Übersicht
python3 -m json.tool .opencode/opencode.json          # JSON-Syntax
bash -n scripts/workspace_check.sh scripts/workspace_status.sh  # Bash-Syntax
.venv/bin/python -m pytest -m unit                    # Unit-Tests (schnell)
.venv/bin/python -m pytest -m integration             # Integrationstests
.venv/bin/python -m pytest -m e2e                     # End-to-End-Tests
.venv/bin/python -m pytest -m mcp                      # MCP-Server-Tests
```

`workspace_check.sh` prüft: erforderliche Dateien/Ordner, JSON-Syntax, Bash-Syntax, keine inline-Agenten in `opencode.json`, Task-Berechtigungen stimmen mit Agent-Dateinamen überein.

---

## 5. Knowledge-QA-Ablauf

### test-hub-feature (automatisiert)

Führt pytest-Läufe aus und prüft Retrieval-Qualität (report-only):
- realistische Nutzerfragen aus geänderten Quellen
- websearch-basierte Real-World-Problemfragen (bei Domain-/Quellenänderungen)
- `source_file` in Treffern, `page_start`/`page_end` bei PDF-Quellen
- Evidenz-Snippets, dokumentierte Lücken als Findings

### Manuelle QA (6 Testfälle aus der Spec)

Die Live-Synthese im Chat kann nur manuell geprüft werden:

| # | Testfall | Was geprüft wird |
|---|---|---|
| 1 | DaVinci mit PDF-Seiten | „PDF-Seite N"-Schreibweise, keine Point/Planar-Verwechslung |
| 2 | Godot ohne PDF-Seiten | „[Seitenangabe nicht verfügbar]", keine halluzinierten Zahlen |
| 3 | Frage ohne Treffer | Ehrliche „keine Quellen"-Antwort |
| 4 | Tracker-Verwechslung | Klare Trennung Point vs. Planar Tracker |
| 5 | Trainingsbuch vs. Manual | Priorisierung `guides > reference` in der Antwort |
| 6 | Personal Notes Priorität | `source_type: personal` zuerst, Repo-Wissen danach |

Ergebnis je Fall: PASS / FAIL / FINDING.

---

## 6. Wo man weiterliest

| Dokument | Inhalt |
|---|---|
| `docs/ai/README.md` | Einstieg für AI-Agenten, Lese-Reihenfolge |
| `docs/ai/architecture.md` | Architektur, Datenfluss, Komponenten |
| `docs/ai/domain-model.md` | Domain-Struktur und -Konventionen |
| `docs/superpowers/specs/2026-06-29-answer-synthesis-design.md` | Vollständige Design-Spec (5 Entscheidungen, 6 QA-Testfälle) |
| `docs/ai/known-issues.md` | LIM-002 und LIM-003 im Detail |
| `docs/ai/validation.md` | Alle Checks und Testbefehle |
| `.opencode/agents/orchestrator-knowledge.md` | Vollständiger Orchestrator-Prompt |

---

## Geprüfte Fakten

- `./scripts/workspace_check.sh`: PASS (exit 0)
- `python3 -m json.tool .opencode/opencode.json`: OK
- 14 Agent-Dateien unter `.opencode/agents/`
- Orchestrator-Prompt enthält Abschnitt „Answer-Synthese" mit allen 5 Design-Entscheidungen

## [unverified]

- Die 6 manuellen QA-Testfälle wurden in dieser Session nicht durchgespielt
- Integration/e2e/mcp-Tests wurden in dieser Session nicht ausgeführt

## Nächste Schritte für Noah

1. Die 6 manuellen QA-Testfälle aus der Spec im OpenCode-Chat durchspielen
2. Bei Bedarf den Orchestrator-Prompt nachjustieren
3. Integration/e2e/mcp-Tests nach OpenCode-Neustart ausführen
