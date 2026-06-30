# Real-World Source Evaluation — Design Spec

> **Status:** Draft | **Datum:** 2026-06-29 | **Autor:** plan-hub-change
>
> Abgeleitet aus: Nutzerwunsch "Real-World Source Evaluation", Recherche-Ergebnisse von research-knowledge-domain, bestehender Quality Evaluation Platform (Spec 2026-06-29-knowledge-hub-quality-evaluation-platform-design.md).

## Vision

Eine **systematische, semi-automatisierte Methodik** zur Bewertung, ob der Knowledge Hub die gleichen Quellen und Lösungen findet, die in echten Online-Community-Quellen (Foren, GitHub Issues, offizielle Docs, YouTube) als Antworten stehen. Die Platform liefert die Daten — der Mensch (Noah) macht die Bewertung.

Die Erweiterung ist:
- **Git-versioniert:** Real-World-Source-Daten leben im Golden Dataset YAML, sind diff-fähig und reviewbar.
- **Rückwärtskompatibel:** Bestehende Felder (`real_world_source_url` als String, `real_world_source_date` als Date) bleiben erhalten. Neue Felder werden additiv ergänzt.
- **Semi-automatisiert:** Die Platform validiert URLs, zeigt sie in Reports an und bereitet den Vergleich vor. Die eigentliche Bewertung (Source Coverage, Solution Alignment, Gap Detection) ist manuell.
- **Kein LLM:** Kein automatisches Solution-Alignment via LLM — das ist ein separates Folgefeature.

## Motivation

- **Qualitäts-Transparenz:** Der Knowledge Hub indexiert PDFs und Repo-Dokumentation, aber wie gut deckt er das ab, was die Community tatsächlich als Antworten nutzt? Ein hoher Composite Score im Golden Dataset sagt nichts darüber aus, ob der Hub die *richtigen* Lösungen findet.
- **Lücken-Erkennung:** GitHub Issues dokumentieren bekannte Bugs und Workarounds, die in offiziellen Docs nicht stehen. Wenn der Hub diese nicht kennt, ist das eine dokumentierte Lücke — kein "Fail" im Scoring, sondern eine Gap.
- **Kurations-Leitfaden:** Die Real-World-Source-Daten helfen Noah zu entscheiden, welche Quellen als nächstes in den Hub aufgenommen werden sollten (z.B. "GitHub Issues zu Jolt Physics sind relevant — sollten wir die indexieren?").

## Architektur-Übersicht

```
Golden Dataset YAML (erweitert)
  │
  ├── real_world_sources: [...]   ← NEU: Liste von Real-World-Quellen
  │     ├── url
  │     ├── date
  │     ├── type
  │     ├── solution_summary
  │     └── has_solution
  │
  ├── validate_dataset.py          ← ERWEITERT: --strict-urls validiert Listen
  ├── run_evaluation.py            ← ERWEITERT: gibt real_world_sources im Output aus
  ├── scorer.py                    ← ERWEITERT: load_golden_dataset parst neue Felder
  └── generate_report.py           ← ERWEITERT: Reports zeigen Real-World-Daten
```

**Architektur-Entscheidung: `real_world_source_url` wird zu `real_world_sources` (Liste)**

Das bestehende Feld `real_world_source_url` (string | null) wird **deprecated, aber nicht entfernt**. Ein neues Feld `real_world_sources` (Liste von Objekten) wird additiv ergänzt. `load_golden_dataset()` normalisiert alte Einzel-URLs automatisch in die neue Listen-Struktur, sodass bestehende YAMLs ohne Migration weiter funktionieren.

**Begründung:**
- Pro Frage gibt es oft 1–3 relevante Online-Quellen (z.B. offizielle Docs + GitHub Issue + Forum-Thread).
- Ein einzelner String kann das nicht abbilden.
- Die Listen-Struktur erlaubt `type`-Tagging, `solution_summary` und `has_solution` pro Quelle.
- Rückwärtskompatibilität: Alte YAMLs mit `real_world_source_url: "https://..."` werden beim Laden in eine 1-elementige `real_world_sources`-Liste konvertiert.

## Datenmodell: Erweiterte Golden-Dataset-Felder

### Bestehende Felder (unverändert)

| Feld | Typ | Status |
|------|-----|--------|
| `real_world_source_url` | string \| null | **Deprecated.** Wird beim Laden in `real_world_sources[0].url` konvertiert. Nicht mehr in neuen Fragen verwenden. |
| `real_world_source_date` | date \| null | **Deprecated.** Wird beim Laden in `real_world_sources[0].date` konvertiert. |

### Neue Felder

```yaml
questions:
  - id: godot-001
    # ... bestehende Felder ...
    real_world_sources:           # NEU: Liste von Real-World-Quellen
      - url: "https://docs.godotengine.org/en/stable/classes/class_node3d.html"
        date: "2025-01-15"        # Datum der Quelle (falls bekannt)
        type: "official-docs"     # Siehe Enum unten
        solution_summary: "Use rotate_y(angle) or rotate(Vector3.UP, angle) to rotate around Y axis. The rotation property (Euler angles in radians) is also available."
        has_solution: true
      - url: "https://docs.godotengine.org/en/stable/tutorials/3d/using_transforms.html"
        date: "2025-01-15"
        type: "official-docs"
        solution_summary: "Transforms tutorial covers rotation, basis vectors, and transform composition with practical examples."
        has_solution: true
```

> **Hinweis:** Alle `solution_summary`-Werte wurden in Commit 5a07b4b (2026-06-30) kuratiert — 29 von 29 ausgefüllt (15 godot + 14 davinci_resolve). Die Beispiele oben zeigen die tatsächliche Ziel-Struktur. Solution Alignment (Ebene 2) ist jetzt vollständig evaluierbar.

### Feld-Definitionen (neue Felder)

| Feld | Typ | Pflicht | Beschreibung |
|------|-----|---------|-------------|
| `real_world_sources` | list[object] | nein | Liste von Real-World-Quellen. Leere Liste oder fehlend = keine Real-World-Daten. |
| `real_world_sources[].url` | string | ja (wenn Objekt vorhanden) | Vollständige URL der Quelle. |
| `real_world_sources[].date` | date \| null | nein | Datum der Quelle (z.B. Erstellungsdatum eines GitHub Issues, Veröffentlichungsdatum eines Blogposts). |
| `real_world_sources[].type` | enum | ja (wenn Objekt vorhanden) | Typ der Quelle. Siehe Enum unten. |
| `real_world_sources[].solution_summary` | string \| null | nein | Kurze Zusammenfassung der Lösung/Antwort (1–3 Sätze). Was steht dort als Antwort? |
| `real_world_sources[].has_solution` | boolean | ja (wenn Objekt vorhanden) | Gibt es dort eine konkrete Lösung/Antwort? `true` = lösungsorientiert, `false` = reine Dokumentation/Referenz ohne spezifische Antwort. |

### `real_world_sources[].type` Enum

| Wert | Beschreibung | Beispiel |
|------|-------------|---------|
| `official-docs` | Offizielle Dokumentation/API-Referenz | docs.godotengine.org, blackmagicdesign.com/products |
| `github-issue` | GitHub Issue (Bug Report, Feature Request) | github.com/godotengine/godot/issues/112656 |
| `github-pr` | GitHub Pull Request | github.com/godotengine/godot/pull/114447 |
| `forum` | Community-Forum (Godot Forum, Blackmagic Forum) | forum.godotengine.org |
| `reddit` | Reddit-Thread | reddit.com/r/godot |
| `youtube` | YouTube-Video (Tutorial, Walkthrough) | youtube.com/watch?v=... |
| `blog` | Blog-Artikel, Devlog | Personal/Company Blog |
| `stack-exchange` | Stack Overflow, Stack Exchange | stackoverflow.com |
| `other` | Sonstige Quelle | — |

### Normalisierung beim Laden (Backward Compatibility)

`load_golden_dataset()` in `scorer.py` normalisiert alte Felder:

```python
# Pseudocode — tatsächliche Implementierung in scorer.py
for q in data["questions"]:
    # Neues Feld initialisieren
    q.setdefault("real_world_sources", [])

    # Altes Feld normalisieren, falls vorhanden und neues Feld leer
    if not q["real_world_sources"] and q.get("real_world_source_url"):
        source = {
            "url": q["real_world_source_url"],
            "date": q.get("real_world_source_date"),
            "type": "other",       # Default — alter Typ war nicht erfasst
            "solution_summary": None,
            "has_solution": False,  # Default — konservativ
        }
        q["real_world_sources"] = [source]
```

**Wichtig:** Die alten Felder `real_world_source_url` und `real_world_source_date` werden **nicht** aus den YAMLs entfernt (Git-Historie erhalten). Neue Fragen sollen nur noch `real_world_sources` verwenden. Die Doku (`domain-model.md`, Specs) wird entsprechend aktualisiert.

## Evaluationsmethodik: Drei Ebenen

Die Evaluation ist **semi-automatisiert**: Die Platform liefert die Daten (Real-World-Sources im Report, Hub-Suchergebnisse), der Mensch macht die Bewertung.

### Ebene 1: Source Coverage (automatisiert vorbereitet, manuell bewertet)

**Frage:** Findet der Hub Quellen, die thematisch zu den Online-Quellen passen?

**Was die Platform liefert:**
- Pro Frage: Liste der `real_world_sources` mit URL, Typ und Solution-Summary.
- Pro Frage: `found_source_files` aus den Hub-Suchergebnissen.
- Pro Frage: Top-3 Ergebnis-Snippets (Text-Anfang, 200 Zeichen).

**Was der Mensch bewertet:**
- Deckt der Hub die gleichen Themen ab wie die Online-Quelle?
- Ist die `source_file`-Abdeckung ausreichend?
- Bewertung: **pass** (Hub deckt Thema ab), **weak** (teilweise), **fail** (Lücke).

**Beispiel:**
- Frage: godot-001 (Node3D rotation)
- Online-Quelle: docs.godotengine.org/classes/class_node3d (rotate_y, rotation)
- Hub-Ergebnis: `godot-docs-reference-packed.md` in found_sources → **pass** (Thema abgedeckt)

### Ebene 2: Solution Alignment (manuell)

**Frage:** Kommt der Hub zur gleichen Lösung wie die Online-Quelle?

**Was die Platform liefert:**
- Pro Frage: `real_world_sources[].solution_summary` (die Online-Lösung in 1–3 Sätzen).
- Pro Frage: Top-5 Ergebnis-Snippets (Text-Anfang, 500 Zeichen).

**Was der Mensch bewertet:**
- Enthalten die Hub-Ergebnisse die gleiche Lösung/API/Methode wie die Online-Quelle?
- Ist die Lösung in den Top-Ergebnissen sichtbar (Rank 1–3) oder erst weiter unten?
- Bewertung: **pass** (gleiche Lösung gefunden), **weak** (ähnlich aber nicht exakt), **fail** (andere/falsche Lösung).

**Beispiel:**
- Frage: godot-001 (Node3D rotation)
- Online-Lösung: "Use `rotate_y(angle)` or `rotate(Vector3.UP, angle)`"
- Hub-Ergebnis: Chunks erwähnen `rotate_y()` und `rotation` → **pass** (Lösung gefunden)

### Ebene 3: Gap Detection (manuell)

**Frage:** Wo hat der Hub Lücken, die die Online-Quellen aufdecken?

**Was die Platform liefert:**
- Pro Frage: `real_world_sources` mit `type` (z.B. `github-issue`).
- Pro Frage: `found_source_files` (welche Hub-Quellen wurden gefunden).

**Was der Mensch bewertet:**
- Gibt es Online-Quellen (insbesondere GitHub Issues), deren Wissen im Hub fehlt?
- Sind das kritische Lücken (bekannte Bugs ohne Workaround im Hub)?
- Bewertung: **gap** (Lücke dokumentiert) mit Begründung.

**Beispiel:**
- Frage: godot-003 (Jolt Physics gotchas)
- Online-Quelle: github.com/godotengine/godot/issues/112656 (get_gravity ignoriert Area3D-Overrides)
- Hub: `gotchas.md` + `godot-docs-reference-packed.md` gefunden, aber der spezifische Bug #112656 ist nicht im Hub → **gap** (dokumentiert)

### Manueller Evaluations-Workflow (Schritt-für-Schritt)

1. **Evaluation ausführen:**
   ```bash
   python scripts/quality/run_evaluation.py --domain godot --output quality/reports/godot_$(date +%Y-%m-%d).json
   ```

2. **Report generieren:**
   ```bash
   python scripts/quality/generate_report.py --input quality/reports/godot_$(date +%Y-%m-%d).json
   ```

3. **Report öffnen** (Markdown) und pro Frage durchgehen:
   - Real-World-Sources-Tabelle lesen (URL, Typ, Solution-Summary)
   - Hub-Ergebnisse (found_source_files, Top-Snippets) mit Online-Quellen vergleichen
   - Bewertung in einer separaten Spalte/Notiz dokumentieren

4. **Findings dokumentieren:**
   - In `notes`-Feld der Frage oder in einem separaten Evaluation-Log.
   - Format: `[real-world-eval 2026-06-29] Ebene 1: pass, Ebene 2: pass, Ebene 3: gap (Bug #112656 nicht im Hub)`

5. **Gaps als Issues/ TODOs tracken:**
   - Kritische Lücken → neue Golden-Dataset-Frage oder Source-Erweiterung planen.
   - Nicht-kritische Lücken → in `notes` dokumentieren.

## CLI-Erweiterung

### `validate_dataset.py --strict-urls` (erweitert)

Das bestehende `--strict-urls`-Flag wird erweitert, um die neuen `real_world_sources`-Listen zu validieren:

- **Ohne `--strict-urls`:** URL-Validierung ist ein Warning (wie bisher).
- **Mit `--strict-urls`:** URL-Validierung ist ein Error (wie bisher).
- **Neu:** Jede URL in `real_world_sources[].url` wird einzeln validiert.
- **Neu:** `real_world_sources[].type` wird gegen das Enum geprüft (Warning bei unbekanntem Typ).
- **Neu:** `real_world_sources[].has_solution` muss ein Boolean sein (Error wenn fehlt).

```bash
# Validiert alle URLs in real_world_sources (Warnings)
python scripts/quality/validate_dataset.py --domain godot

# Validiert alle URLs in real_world_sources (Errors)
python scripts/quality/validate_dataset.py --domain godot --strict-urls
```

### `run_evaluation.py` (erweitert)

Der Output von `run_evaluation.py` enthält jetzt pro Frage die `real_world_sources`:

```json
{
  "evaluations": [
    {
      "id": "godot-001",
      "question": "How do I rotate a Node3D around the Y axis in GDScript?",
      "real_world_sources": [
        {
          "url": "https://docs.godotengine.org/en/stable/classes/class_node3d.html",
          "date": "2025-01-15",
          "type": "official-docs",
          "solution_summary": "Use rotate_y(angle) or rotate(Vector3.UP, angle)...",
          "has_solution": true
        }
      ],
      "source_recall": 1.0,
      "found_source_files": ["godot-docs-reference-packed.md"],
      "top_snippets": [
        "void rotate_y(float angle) rotates the node around the Y axis...",
        "..."
      ],
      ...
    }
  ]
}
```

> **Hinweis:** Alle `solution_summary`-Werte wurden in Commit 5a07b4b (2026-06-30) kuratiert — 29 von 29 ausgefüllt. Das Beispiel oben zeigt die tatsächliche Struktur.

**Neues Feld `top_snippets`:** Die ersten 200 Zeichen des `text`-Felds der Top-3 Ergebnisse, damit der Mensch im Report schnell vergleichen kann, ohne die Rohdaten zu öffnen.

### `generate_report.py` (erweitert)

Der Markdown-Report enthält eine neue Sektion **"Real-World Source Comparison"** pro Frage:

```markdown
## Real-World Source Comparison

### godot-001 (pass, 0.85)
**Question:** How do I rotate a Node3D around the Y axis in GDScript?

| # | Type | URL | Solution Summary | Has Solution |
|---|------|-----|-----------------|-------------|
| 1 | official-docs | [class_node3d](https://docs.godotengine.org/...) | Use rotate_y(angle) or rotate(Vector3.UP, angle)... | ✅ |
| 2 | official-docs | [using_transforms](https://docs.godotengine.org/...) | Transforms tutorial covers rotation, basis vectors... | ✅ |

**Hub Top Snippets:**
1. `void rotate_y(float angle) rotates the node around the Y axis...` (godot-docs-reference-packed.md)
2. `The rotation property is a Vector3 of Euler angles in radians...` (godot-docs-reference-packed.md)
3. `transform.basis = Basis(Vector3.UP, angle)...` (godot-docs-reference-packed.md)

**Found Sources:** godot-docs-reference-packed.md

---
*Manual evaluation:*
- [ ] Source Coverage: Hub findet thematisch passende Quellen?
- [ ] Solution Alignment: Hub kommt zur gleichen Lösung?
- [ ] Gap Detection: Lücken die Online-Quellen aufdecken?
```

Die GFM-Checkboxen `- [ ]` sind Platzhalter für die manuelle Bewertung. Der Mensch kann sie im Markdown-Report ankreuzen und das Ergebnis committen.

## Report-Struktur (vollständig, erweitert)

```
# Quality Report: godot — 2026-06-29

## Summary
(Unverändert)

## Metric Averages
(Unverändert)

## Per-Question Results
(Unverändert, aber mit zusätzlicher Spalte "RWS" = Anzahl Real-World-Sources)

## Real-World Source Comparison  ← NEU
(Für jede Frage mit real_world_sources: Tabelle + Snippets + Checkboxen)

## Weak / Fail Details
(Unverändert)

## Truncation Warnings
(Unverändert)

## Gaps & Recommendations
(Erweitert: Hinweis auf dokumentierte Gaps aus Ebene 3)
```

## Out of Scope

- **Automatisches LLM-basiertes Solution-Alignment (Ebene 2 automatisiert):** Die Platform vergleicht nicht automatisch Hub-Snippets mit `solution_summary`. Das erfordert ein LLM oder Cross-Encoder-Vergleich und ist ein separates Folgefeature.
- **Neue Such-Quellen indexieren:** GitHub Issues, Foren oder YouTube-Transkripte werden nicht als neue Hub-Quellen indexiert. Das wäre eine Domain-Erweiterung (z.B. `godot_community` mit GitHub-Issue-Scraper).
- **Automated webfetch der Online-Quellen beim Eval-Run:** Keine Live-Abhängigkeit zu externen URLs. Zu langsam, zu fragil (Rate-Limits, Änderungen).
- **CI-Integration:** Keine automatischen Evaluationen in CI.
- **Automatische Gap-Bewertung:** Die Platform erkennt nicht automatisch, ob eine Lücke kritisch ist. Das ist eine manuelle Entscheidung.
- **`real_world_sources` als Scoring-Metrik:** Die Real-World-Daten fließen **nicht** in den Composite Score ein. Sie sind rein informativ für die manuelle Evaluation. Eine automatische Metrik (z.B. "Solution Alignment Score") wäre ein Folgefeature.

## Erfolgskriterien

1. Spec existiert unter `docs/superpowers/specs/2026-06-29-real-world-source-evaluation-design.md`.
2. `godot.yaml` und `davinci_resolve.yaml` enthalten `real_world_sources` für alle 14 Fragen mit den recherchierten URLs.
3. `load_golden_dataset()` normalisiert alte `real_world_source_url`-Felder in `real_world_sources` (backward compat).
4. `validate_question()` prüft neue Felder (`type`-Enum, `has_solution`-Boolean, `url`-Pflicht).
5. `validate_dataset.py --strict-urls` validiert alle URLs in `real_world_sources`-Listen.
6. `run_evaluation.py` gibt `real_world_sources` und `top_snippets` im Output aus.
7. `generate_report.py` zeigt die "Real-World Source Comparison"-Sektion im Markdown-Report.
8. Bestehende Tests (`pytest -m quality`) bleiben grün.
9. Neue Tests für Normalisierung, Listen-Validierung und Report-Erweiterung.
10. `workspace_check.sh` erkennt keine neuen Issues.

## Bekannte Einschränkungen

- **URL-Verfügbarkeit:** Online-Quellen können sich ändern, verschwinden oder ihre Inhalte aktualisieren. Die URLs im Golden Dataset sind eine Momentaufnahme. `last_verified` sollte regelmäßig aktualisiert werden.
- **GitHub Issues können geschlossen werden:** Ein Issue, das heute "open" ist, kann morgen "closed" oder "fixed" sein. Der `date`-Eintrag hilft, den historischen Kontext zu verstehen.
- **YouTube-Videos sind nicht durchsuchbar:** Der Hub kann Video-Inhalte nicht indexieren (kein Transkript). YouTube-Quellen im Golden Dataset dienen als Referenz für das, was die Community nutzt — nicht als Quelle, die der Hub finden soll.
- **Solution-Summaries sind subjektiv:** Die Zusammenfassung der Online-Lösung in 1–3 Sätzen ist eine manuelle Kuratierung und kann unvollständig sein.
- **Kein automatisches Solution-Alignment:** Ebene 2 (Solution Alignment) ist rein manuell. Die Platform zeigt Snippets und Summaries nebeneinander, aber der Vergleich erfordert menschliches Urteilsvermögen.
- **`top_snippets`-Länge:** 200 Zeichen sind ein Kompromiss zwischen Lesbarkeit und Informationsgehalt. Bei stark strukturierten Chunks (z.B. RST-Tabellen) können die ersten 200 Zeichen nicht repräsentativ sein.

---

## Implementierungsplan (Task-Liste)

### Phase 1: Datenmodell + Normalisierung

- [ ] **Task 1.1:** `scorer.py` — `load_golden_dataset()` erweitern
  - `q.setdefault("real_world_sources", [])` hinzufügen
  - Normalisierungslogik: altes `real_world_source_url` → `real_world_sources[0]`
  - Defaults für neue Felder: `type: "other"`, `has_solution: false`, `solution_summary: null`
  - Betroffene Datei: `scripts/quality/scorer.py` (Funktion `load_golden_dataset`)

- [ ] **Task 1.2:** `scorer.py` — `validate_question()` erweitern
  - Prüfung: Wenn `real_world_sources` nicht leer, dann jedes Objekt validieren
  - `url` muss nicht-leer sein (Error)
  - `type` muss im Enum sein (Warning bei unbekanntem Typ, kein Error)
  - `has_solution` muss Boolean sein (Error wenn fehlt)
  - Betroffene Datei: `scripts/quality/scorer.py` (Funktion `validate_question`)

- [ ] **Task 1.3:** `scorer.py` — `evaluate_question()` erweitern
  - `real_world_sources` aus der Question in den Eval-Output übernehmen
  - `top_snippets` generieren: erste 200 Zeichen des `text`-Felds der Top-3 Ergebnisse
  - Betroffene Datei: `scripts/quality/scorer.py` (Funktion `evaluate_question`)

### Phase 2: Golden Dataset YAMLs befüllen

- [ ] **Task 2.1:** `godot.yaml` — `real_world_sources` für alle 7 Fragen eintragen
  - godot-001: 2 URLs (class_node3d, using_transforms) — beide `official-docs`, `has_solution: true`
  - godot-002: 2 URLs (character_body_2d tutorial, issue #112656) — `official-docs` + `github-issue`
  - godot-003: 3 URLs (issue #117857, issue #112315, issue #113058) — alle `github-issue`
  - godot-004: 2 URLs (camera3d class, using_transforms) — beide `official-docs`
  - godot-005: 3 URLs (issue #111653, model_export_considerations, issue #97022) — `github-issue` + `official-docs` + `github-issue`
  - godot-006: 1 URL (signals tutorial) — `official-docs`
  - godot-007: 2 URLs (character_body_2d tutorial, PR #114447) — `official-docs` + `github-pr`
  - Betroffene Datei: `quality/golden/godot.yaml`

- [ ] **Task 2.2:** `davinci_resolve.yaml` — `real_world_sources` für alle 7 Fragen eintragen
  - davinci_resolve-001: 2 URLs (fusion page, fusion training) — beide `official-docs`
  - davinci_resolve-002: 2 URLs (edit page, editing training) — beide `official-docs`
  - davinci_resolve-003: 2 URLs (color page, color training) — beide `official-docs`
  - davinci_resolve-004: 2 URLs (fusion page, color page) — beide `official-docs`
  - davinci_resolve-005: 2 URLs (edit page, delivering training) — beide `official-docs`
  - davinci_resolve-006: 2 URLs (fairlight page, fairlight training) — beide `official-docs`
  - davinci_resolve-007: 2 URLs (whatsnew page, support page) — beide `official-docs`
  - Betroffene Datei: `quality/golden/davinci_resolve.yaml`

### Phase 3: CLI-Erweiterung

- [ ] **Task 3.1:** `validate_dataset.py` — `--strict-urls` für Listen erweitern
  - `validate_url()` für jede URL in `real_world_sources` aufrufen
  - `type`-Enum-Prüfung (Warning bei unbekanntem Typ)
  - `has_solution`-Boolean-Prüfung (Error wenn kein Boolean)
  - Betroffene Datei: `scripts/quality/validate_dataset.py`

- [ ] **Task 3.2:** `run_evaluation.py` — Output erweitern
  - `real_world_sources` und `top_snippets` aus `evaluate_question()` in den Output übernehmen
  - Keine Änderung an der Suchlogik — nur Daten durchreichen
  - Betroffene Datei: `scripts/quality/run_evaluation.py`

- [ ] **Task 3.3:** `generate_report.py` — "Real-World Source Comparison"-Sektion
  - `generate_markdown_report()`: Neue Sektion mit Tabelle pro Frage
  - `generate_json_report()`: `real_world_sources` und `top_snippets` in JSON ausgeben
  - Betroffene Datei: `scripts/quality/scorer.py` (Funktionen `generate_markdown_report`, `generate_json_report`)

### Phase 4: Tests

- [ ] **Task 4.1:** `test_golden_dataset_loader.py` — Normalisierung testen
  - Test: Altes `real_world_source_url` wird in `real_world_sources[0]` konvertiert
  - Test: Leeres `real_world_sources` wenn kein altes Feld vorhanden
  - Test: Alte Felder bleiben erhalten (nicht gelöscht)
  - Betroffene Datei: `tests/quality/test_golden_dataset_loader.py`

- [ ] **Task 4.2:** `test_golden_dataset_loader.py` — `validate_question` für neue Felder testen
  - Test: Valides `real_world_sources`-Objekt wird akzeptiert
  - Test: Fehlende `url` → Error
  - Test: Unbekannter `type` → Warning (nicht Error)
  - Test: Fehlendes `has_solution` → Error
  - Betroffene Datei: `tests/quality/test_golden_dataset_loader.py`

- [ ] **Task 4.3:** `test_validate_dataset.py` — URL-Listen-Validierung testen
  - Test: `--strict-urls` validiert alle URLs in `real_world_sources`
  - Test: Ohne `--strict-urls` sind URL-Fehler nur Warnings
  - Betroffene Datei: `tests/quality/test_validate_dataset.py`

- [ ] **Task 4.4:** `test_report_generator.py` — Real-World-Sektion testen
  - Test: Markdown-Report enthält "Real-World Source Comparison"-Sektion
  - Test: JSON-Report enthält `real_world_sources` und `top_snippets`
  - Test: Fragen ohne `real_world_sources` zeigen keine Sektion
  - Betroffene Datei: `tests/quality/test_report_generator.py`

- [ ] **Task 4.5:** `test_rubric_scorer.py` — `evaluate_question` mit neuen Feldern testen
  - Test: `evaluate_question` gibt `real_world_sources` im Output zurück
  - Test: `evaluate_question` gibt `top_snippets` im Output zurück
  - Test: `top_snippets` sind auf 200 Zeichen begrenzt
  - Betroffene Datei: `tests/quality/test_rubric_scorer.py`

### Phase 5: Doku + Validierung

- [ ] **Task 5.1:** `docs/ai/domain-model.md` — Golden-Dataset-Felder dokumentieren
  - Neue Felder in der Feld-Tabelle ergänzen
  - Hinweis auf Deprecation von `real_world_source_url`

- [ ] **Task 5.2:** `docs/ai/validation.md` — Neue CLI-Optionen dokumentieren
  - `--strict-urls` für `validate_dataset.py` (jetzt auch für `real_world_sources`-Listen)

- [ ] **Task 5.3:** `docs/ai/changelog.md` — Änderung eintragen

- [ ] **Task 5.4:** `workspace_check.sh` — Sicherstellen dass neue Dateien erkannt werden

- [ ] **Task 5.5:** `pytest -m quality` — Alle Tests müssen grün sein

- [ ] **Task 5.6:** `python scripts/quality/validate_dataset.py --domain godot --strict-urls` — Muss erfolgreich durchlaufen

- [ ] **Task 5.7:** `python scripts/quality/validate_dataset.py --domain davinci_resolve --strict-urls` — Muss erfolgreich durchlaufen
