# Knowledge Hub Answer-Synthesis Design

**Date:** 2026-06-29  
**Status:** Approved for implementation  
**Owner:** Knowledge Hub  
**Pattern:** Single-Repo-Projekt, Orchestrator-Prompt-Erweiterung

## Ziel

Der Knowledge-Hub-Orchestrator (`orchestrator-knowledge`) soll Suchergebnisse aus dem MCP-Tool `search_knowledge` nicht nur weiterreichen, sondern aktiv zu quellenbelegten, ehrlichen Antworten synthetisieren. Die Synthese muss:

- **Quellenpriorisierung** korrekt anwenden (domain-agnostisch).
- **Seitenangaben** eindeutig als PDF-Seiten kommunizieren, nicht als gedruckte Buchseiten.
- **Truncation-Hinweise** beachten und nichts halluzinieren, was im abgeschnittenen Teil stehen könnte.
- **Bei fehlenden oder unzureichenden Quellen** ehrlich „keine ausreichenden Quellen gefunden" antworten, statt zu halluzinieren.

Die Spec definiert die Regeln und ein manuelles QA-Protokoll mit 6 konkreten Testfällen. Die konkrete Prompt-Formulierung gehört in `.opencode/agents/orchestrator-knowledge.md` (Abschnitt „Answer-Synthese"), nicht in diese Spec.

## Design-Entscheidungen

### 1. Prompt-basierte Synthese statt deterministischer Code-Logik

Die Synthese wird im Orchestrator-Prompt als explizite Anweisung verankert, nicht als zusätzliche Logik im MCP-Server oder in `hybrid_search.py`. Begründung:

- Das LLM im Orchestrator hat ohnehin die Aufgabe, aus Treffern Antworten zu formen.
- Deterministische Priorisierung in Python würde nur Reihenfolge sortieren, nicht inhaltlich gewichten (z.B. „Trainingsbuch > Manual" nur in der Antwort sichtbar machen).
- Kein neues Tool, keine neuen Felder, keine Pipeline-Änderung — kleines Diff, niedriges Risiko.

### 2. Domain-agnostische Quellenpriorisierung

Die Priorisierung verwendet eine **Heuristik**, die für alle Domains funktioniert:

```text
personal > guides/tutorials > reference/manual > general
```

Hinweise zur Erkennung kommen aus:

- `source_type` aus den ChromaDB-Metadaten (`"personal"` schlägt `"repo"`).
- Dateinamen-Keywords als Signal, nicht als harte Regel:
  - `personal`, `faq`, `gotcha`, `tip`, `best-practice` → persönliches Wissen.
  - `guide`, `tutorial`, `training`, `getting-started` → geführtes Lernmaterial.
  - `reference`, `manual`, `api`, `spec` → Nachschlagewerk.
  - sonstige Dateinamen → allgemeines Repo-Wissen.
- Cross-Encoder-Score als Tie-Breaker innerhalb einer Stufe.

Domain-spezifische Dateinamen (z.B. `davinci_resolve_primary_color_correction_training_guide-*.md`) werden **nicht** hardcodiert. Die Heuristik muss auch für Godot, Blender, FreeCAD oder künftige Domains greifen.

Beispiel-Priorisierung (DaVinci Resolve, illustrative Veranschaulichung, keine Regel):

1. `personal/gotchas.md` zu Planar Tracker → höchste Priorität.
2. `sources/davinci_resolve_planar_tracker_training_guide-*.md` → geführtes Material.
3. `sources/davinci_resolve_reference_manual-*.md` → Nachschlagewerk.
4. `sources/davinci_resolve_fusion_composting_manual-*.md` → allgemein.

### 3. PDF-Seiten vs. gedruckte Buchseiten

`page_start` und `page_end` in den ChromaDB-Metadaten sind **1-basierte PDF-Seiten**, nicht gedruckte Buchseiten. In Trainingsbüchern kann die TOC-Position (z.B. „(p.318)") von der PDF-Seitenzahl abweichen.

Regeln für den Orchestrator:

- Schreibweise: **„PDF-Seite N"** (nicht „Seite N" und nicht „S. N"), damit klar ist, dass es die Datei-Position ist.
- Wenn die Quelle selbst eine gedruckte Seitenzahl nennt (z.B. „see page 318 in the printed manual"), als **Hinweis** melden, nicht auflösen. Beispiel: „Laut Quelle wird auf der gedruckten Seite 318 verwiesen; in der PDF-Datei entspricht das PDF-Seite 412 (siehe Hinweis im Treffer)."
- Wenn `page_start`/`page_end` fehlen: **„[Seitenangabe nicht verfügbar]"** — keine erfundene Zahl.

### 4. Text-Truncation als bekannte Einschränkung

Das `text`-Feld in Suchergebnissen wird auf 5000 Zeichen trunciert (`hybrid_search.py:127`, `embed_search.py:69`). DaVinci-Fallback-Chunks können bis ~8000 Zeichen groß sein, daher kann ein DaVinci-Treffer deutlich gekürzt sein. Godot-Chunks sind kleiner und meist komplett im Treffer.

Regeln für den Orchestrator:

- Anzeichen für Truncation: Text bricht mitten im Satz/Wort ab, endet ohne Satzzeichen, oder endet mitten in einer Aufzählung.
- Nur das zitieren, was tatsächlich im `text`-Feld steht.
- Bei abgekürzten Stellen: „Der Treffer-Text zeigt … (möglicherweise unvollständig, truncated auf 5000 Zeichen)."
- Niemals den fehlenden Teil halluzinieren.

### 5. No-Results / unzureichende Quellen

Wenn die Suche keine oder keine relevanten Treffer liefert:

- Ehrliche Antwort: **„In den verfügbaren Quellen wurde zu <Thema> nichts Passendes gefunden."**
- Optional, aber empfohlen: Hinweis, welche Quelle vermutlich fehlt (z.B. „Wahrscheinlich wäre das Planar-Tracker-Kapitel im DaVinci-Resolve-Trainingsbuch relevant").
- Niemals antworten, als ob man eine Quelle hätte, wenn alle Treffer-Themen oder Score-Werte (< 0.1) zeigen, dass nichts passt.

## Out of Scope

- **Code-Änderungen an Pipeline, MCP-Server oder Index** — nicht erforderlich.
- **Index-Rebuilds** — keine Schema-Änderung, kein Migrations-Bedarf.
- **Deterministische Re-Ranking-Logik in Python** — Synthese bleibt im Prompt.
- **Automatisierte Test-Suite für Synthese-Qualität** — Golden-Dataset-Platform ist als separates Folgefeature geplant (siehe `docs/ai/known-issues.md` TD-002).
- **Domain-spezifische Prompt-Varianten** — eine domain-agnostische Heuristik reicht; spezielle Regeln würden die Prompt-Wartung erschweren.

## Felder, auf die der Orchestrator sich NICHT verlassen darf

- `section_path`: fehlt bei DaVinci-Resolve-Chunks (Fallback-Chunking, kein domain-spezifischer Parser) und in Teilen auch bei Godot-Chunks. Siehe `LIM-002`.
- `chunk_type`: fehlt bei DaVinci-Resolve-Chunks.

Diese Felder nur erwähnen, wenn sie im Treffer tatsächlich vorhanden sind. Andernfalls weglassen, nicht raten.

## Manuelles QA-Protokoll

Sechs konkrete Testfälle. Diese sind **manuell** durchzuspielen (vom Menschen oder mit Stichproben in OpenCode), nicht Teil der automatisierten Test-Suite. Ergebnis je Fall: PASS / FAIL / FINDING.

### Testfall 1 — DaVinci-Frage mit PDF-Seiten

- **Frage:** „Wie richte ich einen Planar Tracker in DaVinci Resolve ein?"
- **Erwartete Quellen (Top-3):** Mindestens ein Treffer aus einem Planar-Tracker-Trainingsguide mit `page_start`/`page_end`.
- **Erwartete Antwort:**
  - Antwort enthält Schritt-für-Schritt-Anleitung mit Quellenbeleg.
  - Zitierformat: „(Quelle: …training_guide…md, PDF-Seite 17, Score: 0.74)".
  - **Keine Verwechslung mit Point Tracker.** Wenn Point-Tracker-Inhalt in den Treffern steht, klar trennen („Das gilt für den Point Tracker; zum Planar Tracker siehe …").
- **PASS-Kriterium:** Synthese nutzt PDF-Seiten-Schreibweise, kein Point-Tracker-Inhalt fälschlich als Planar-Tracker-Antwort verkauft.

### Testfall 2 — Godot-Frage ohne PDF-Seiten

- **Frage:** „Wie bewege ich einen CharacterBody3D in Godot 4?"
- **Erwartete Quellen:** Repo-Wissen (rst-godot-Plugin), keine PDF-Quellen, keine `page_start`/`page_end`-Felder.
- **Erwartete Antwort:**
  - Antwort nutzt Code-Beispiele aus den Treffern.
  - Zitierformat: „(Quelle: godot-docs-packed.md, [Seitenangabe nicht verfügbar], Score: 0.68)".
  - **Keine erfundenen Seitenzahlen** wie „S. 142" oder „Seite 12".
- **PASS-Kriterium:** Korrekt „[Seitenangabe nicht verfügbar]" verwendet, keine halluzinierte Zahl.

### Testfall 3 — Frage ohne Treffer

- **Frage:** „Wie baue ich einen Flux-Kompensator in Blender?" (hypothetisch, existiert nicht).
- **Erwartete Quellen:** Leere Trefferliste oder alle Scores < 0.1.
- **Erwartete Antwort:**
  - „In den verfügbaren Quellen wurde zu einem Flux-Kompensator in Blender nichts Passendes gefunden."
  - Optional: Hinweis, dass das Konzept im Standardumfang von Blender nicht existiert.
  - **Keine Bastelanleitung** halluziniert.
- **PASS-Kriterium:** Ehrliche „keine Quellen"-Antwort, keine Halluzination.

### Testfall 4 — Tracker-Verwechslung vermeiden

- **Frage:** „Worin unterscheiden sich Point Tracker und Planar Tracker in DaVinci?"
- **Erwartete Quellen:** Treffer zu beiden Trackern.
- **Erwartete Antwort:**
  - Klare Trennung der beiden Tracker, jeweils mit Quellenbeleg.
  - Keine Vermischung der Eigenschaften.
  - Wenn ein Treffer nur einen Tracker behandelt, nicht die Eigenschaften des anderen dazudichten.
- **PASS-Kriterium:** Antwort zitiert für jeden Tracker nur das, was in den jeweiligen Quellen tatsächlich steht.

### Testfall 5 — Quellenpriorisierung Trainingsbuch vs. Manual

- **Frage:** „Wie nutze ich Primary Color Correction in DaVinci Resolve?"
- **Erwartete Quellen (Top-5):** Mehrere Treffer — z.B. `primary_color_correction_training_guide-*.md` und `reference_manual-*.md`.
- **Erwartete Antwort:**
  - Synthese nutzt Trainingsguide als Hauptquelle, Manual als Ergänzung.
  - Wenn das Trainingsbuch eine Schritt-für-Schritt-Anleitung bietet, steht diese zuerst; manuelle API-Spezifikationen danach.
  - Zitierformat spiegelt die Reihenfolge wider.
- **PASS-Kriterium:** Reihenfolge in der Antwort entspricht der Priorisierungs-Heuristik (`guides/tutorials > reference/manual`), nicht dem Rohtreffer-Ranking.

### Testfall 6 — Personal Notes Priorität

- **Frage:** „Welche Gotchas gibt es bei Godot CharacterBody3D?"
- **Erwartete Quellen:** Treffer aus `personal/gotchas.md` UND aus `sources/godot-docs-packed.md`.
- **Erwartete Antwort:**
  - Gotchas aus `personal/gotchas.md` zuerst, klar als persönliche Notizen markiert (z.B. „Aus meinen Notizen (personal/gotchas.md): …").
  - Repo-Wissen danach, als Hintergrund.
  - `source_type: personal` in den Treffer-Metadaten ist sichtbar berücksichtigt.
- **PASS-Kriterium:** Persönliche Notizen priorisiert, `source_type` in der Antwort erkennbar.

## Akzeptanzkriterien

Die Implementierung gilt als abgeschlossen, wenn:

1. `.opencode/agents/orchestrator-knowledge.md` einen neuen Abschnitt „Answer-Synthese" mit allen fünf Design-Entscheidungen (Priorisierung, PDF-Seiten, Truncation, No-Results, Zitierformat) enthält.
2. `docs/ai/known-issues.md` die neuen Einträge **LIM-002** und **LIM-003** enthält.
3. `docs/ai/changelog.md` einen Eintrag für 2026-06-29 mit Verweis auf diese Spec enthält.
4. `./scripts/workspace_check.sh` PASS (exit 0).
5. `python3 -m json.tool .opencode/opencode.json` OK.
6. Die 6 manuellen QA-Testfälle sind in dieser Spec dokumentiert (nicht automatisiert ausgeführt).