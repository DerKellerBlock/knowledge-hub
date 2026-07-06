# Knowledge Hub Quality Evaluation Platform — Design Spec

> **Status:** Draft | **Datum:** 2026-06-29 | **Autor:** plan-hub-change
>
> Abgeleitet aus: TD-002 (known-issues.md), Nutzerwunsch "Ansatz C", Recherche zu RAGAS/DeepEval/TruLens

## Vision

Eine **schlanke, selbstgebaute Quality Evaluation Platform** für den Knowledge Hub, die ohne externe Frameworks (RAGAS, DeepEval, TruLens) auskommt. Sie bewertet die Retrieval-Qualität pro Domain anhand eines versionierten Golden Dataset, liefert menschenlesbare Reports und erkennt Regressionen nach Index-Rebuilds.

Die Platform ist:
- **Git-versioniert:** Golden Dataset und archivierte Reports leben im Repo, sind diff-fähig und reviewbar.
- **Domain-agnostisch:** Gleiche Metriken für Godot (RST-Repo-Quellen) und DaVinci Resolve (PDF-Quellen), mit domain-spezifischen Erwartungen (z.B. page_start nur für PDF-Domains).
- **Pytest-integriert:** Qualitäts-Tests laufen als pytest-Marker `quality`, nutzen die bestehende `hybrid_search.search()`-API.
- **CLI-gesteuert:** Skripte zum Hinzufügen von Fragen, Validieren des Datasets, Ausführen von Evaluationen und Generieren von Reports.
- **Kein LLM:** Alle Metriken sind rein retrieval-basiert (kein Faithfulness, keine Answer-Relevancy). Der Hub ist ein Retrieval-System, kein Generator.

## Motivation

- **TD-002:** Ein dauerhaftes Golden Dataset für Knowledge-QA fehlt. Der `test-hub-feature`-Agent macht ad-hoc Websearch-basierte QA, aber ohne persistente Fixtures gibt es keine reproduzierbaren Qualitätsmetriken über die Zeit.
- **Regressionen:** Nach jedem `embed_index.py --domain X` (Komplett-Neuaufbau des Index) gibt es keine automatisierte Prüfung, ob wichtige Quellen noch gefunden werden oder Seitenmetadaten verloren gehen.
- **Qualitäts-Transparenz:** Noah braucht einen schnellen Überblick, welche Domains gut abgedeckt sind und wo Lücken bestehen — ohne manuelles Durchsuchen.

## Architektur-Übersicht

```
knowledge-hub/
├── quality/                          # Quality Evaluation Platform (NEU)
│   ├── golden/                       # Golden Dataset pro Domain
│   │   ├── godot.yaml
│   │   └── davinci_resolve.yaml
│   └── reports/                      # Generierte Reports (.gitignored)
│       └── .gitkeep
├── scripts/
│   └── quality/                      # CLI-Skripte (NEU)
│       ├── __init__.py
│       ├── scorer.py                 # Pure functions: load_golden_dataset, validate_question, scoring, report generation
│       ├── add_question.py           # Frage zum Golden Dataset hinzufügen (Phase 2)
│       ├── validate_dataset.py       # YAML-Struktur + Quellen-Existenz prüfen (Phase 2)
│       ├── run_evaluation.py         # Evaluation gegen live Index ausführen (Phase 1)
│       └── generate_report.py        # Markdown + JSON Report generieren (Phase 2)
├── tests/
│   └── quality/                      # Pytest-basierte Qualitäts-Tests (NEU)
│       ├── __init__.py
│       ├── test_golden_dataset_loader.py   # TDD: Dataset-Loader (Phase 1)
│       ├── test_rubric_scorer.py           # TDD: Rubrik-Scorer (Phase 1)
│       └── test_report_generator.py        # TDD: Report-Generator (Phase 1)
└── docs/
    └── superpowers/
        └── quality-reports/          # Archivierte Quality Reports (NEU, versioniert)
            └── .gitkeep
```

**Architektur-Entscheidung: Trennung von Pure Functions und CLI-Wrapper**

- `scripts/quality/scorer.py` enthält **pure functions** (`load_golden_dataset`, `validate_question`, `score_*`, `evaluate_question`, `aggregate_domain_scores`, `generate_markdown_report`, `generate_json_report`). Diese nehmen Suchergebnisse als Argumente und rufen NICHT `hybrid_search.search()` auf. Das macht sie in Unit-Tests mit Mock-Results schnell testbar (keine echten Indizes nötig).
- `scripts/quality/run_evaluation.py` ist der **CLI-Wrapper**, der `hybrid_search.search()` aufruft und die Ergebnisse an scorer-Funktionen übergibt. Er ist nicht direkt in Unit-Tests getestet (stattdessen manueller Smoke-Test gegen echte Indizes).

## Datenmodell: Golden Dataset

### Speicherort

`quality/golden/<domain>.yaml` — eine YAML-Datei pro Domain.

**Begründung:**
- `quality/` als Top-Level-Namespace trennt die Quality-Plattform klar von `tests/` (Test-Infrastruktur) und `domains/` (Wissensinhalte).
- Eine Datei pro Domain hält die Dateien klein und reviewbar.
- YAML ist menschenlesbar, git-diff-fähig und benötigt nur `pyyaml` als Dependency.

### Schema

```yaml
# quality/golden/<domain>.yaml
domain: godot
version: 1
description: "Golden Dataset for Godot domain quality evaluation"
last_updated: 2026-06-29
questions:
  - id: godot-001                # Eindeutige ID: <domain>-<nnn>
    question: "How do I rotate a Node3D around the Y axis in GDScript?"
    expected_source_files:        # Quellen, die in Top-K erwartet werden
      - "godot-docs-packed.md"
    expected_page_ranges: []      # Leer für nicht-PDF-Domains
    real_world_source_url: "https://forum.godotengine.org/t/how-to-rotate-node3d/12345"
    real_world_source_date: "2025-03-15"
    difficulty: easy              # easy | medium | hard
    tags: [rotation, node3d, 3d, gdscript]
    created_date: 2026-06-29
    last_verified: 2026-06-29
    notes: "Common beginner question from Godot forums"
    min_top_k: 5                  # Wie viele Top-Results werden mindestens geprüft
```

### Feld-Definitionen

| Feld | Typ | Pflicht | Beschreibung |
|------|-----|---------|-------------|
| `id` | string | ja | Eindeutige ID, Format `<domain>-<nnn>` |
| `question` | string | ja | Natürlichsprachliche Frage |
| `expected_source_files` | list[string] | ja | Erwartete `source_file`-Werte in Top-K. Leere Liste = keine Quellen-Erwartung (SR-Metrik wird N/A). |
| `expected_page_ranges` | list[{start, end}] | nein | Für PDF-Domains: erwartete Seitenbereiche. `[]` = keine Seiten-Erwartung. |
| `real_world_source_url` | string | nein | URL der realen Quelle (Forum, GitHub Issue, YouTube). |
| `real_world_source_date` | date | nein | Datum der realen Quelle. |
| `difficulty` | enum | ja | `easy`, `medium`, `hard` |
| `tags` | list[string] | nein | Freie Tags zur Kategorisierung |
| `created_date` | date | ja | Erstellungsdatum der Frage im Dataset |
| `last_verified` | date | ja | Letzte manuelle Verifikation |
| `notes` | string | nein | Kontext, Erwartungen, bekannte Einschränkungen |
| `min_top_k` | int | nein | Mindestanzahl Top-Results für Evaluation (Default: 10) |

## Bewertungsrubrik

### Metriken (0–1, höher = besser; oder N/A wenn nicht anwendbar)

#### 1. Source Recall (SR)

Anteil der `expected_source_files`, die in den Top-K-Ergebnissen gefunden wurden.

```
SR = |expected_source_files ∩ found_source_files| / |expected_source_files|
```

**N/A-Fall:** Wenn `expected_source_files` leer ist, wird SR=N/A (keine Quellen-Erwartung → keine Abwertung, kein Division-by-Zero). Das Gewicht von SR (0.35) wird auf die übrigen Metriken umverteilt.

#### 2. Page Metadata Accuracy (PMA)

Für PDF-Domains: Anteil der Top-K-Ergebnisse mit `page_start` ≠ None, die im erwarteten Bereich liegen.

```
PMA = count(results with page_start in expected_range) / count(results with page_start != None)
```

Falls keine `expected_page_ranges` definiert sind: PMA prüft nur, ob `page_start` überhaupt vorhanden ist:
```
PMA = count(results with page_start != None) / min(K, total_results)
```

**N/A-Fall:** Für nicht-PDF-Domains (Godot, keine `page_start`-Metadaten) wird PMA=N/A. Das Gewicht von PMA (0.20) wird auf die übrigen Metriken umverteilt.

#### 3. Top-K Relevance (TKR)

Rang-basierter normalisierter Score der Top-K-Ergebnisse. RRF/Cross-Encoder-Scores aus `hybrid_search` sind nicht im [0,1]-Bereich (~0.017), daher wird **rang-basiert** normalisiert:

```
normalized_score_i = 1.0 - (rank_index_i / total_results)
```

wobei `rank_index` 0-basiert ist (Rank 1 → index 0 → höchster Score). TKR ist der Durchschnitt der `normalized_scores`.

**Begründung:** Rang-basiert statt raw-Score-basiert, weil RRF/Cross-Encoder-Scores nicht vergleichbar zwischen Domains und Runs sind. Der Rang ist deterministisch und aussagekräftig genug für Quality-Tracking.

#### 4. Evidence Quality (EQ)

Anteil der Top-K-Ergebnisse mit nicht-leerem `text`-Feld.

```
EQ = count(results with non-empty text) / K
```

Zusätzlich: Wenn `text`-Feld >= 5000 Zeichen lang ist (Truncation-Heuristik, LIM-003), wird ein `truncation_warning` im Report vermerkt. **Achtung:** `len(text) >= 5000` ist eine Heuristik — False Positives möglich bei natürlich 5000-Zeichen-Chunks. Der Score wird dadurch nicht reduziert (Truncation ist systembedingt), aber der Report weist darauf hin.

#### Composite Score (Gewichte mit N/A-Umverteilung)

Default-Gewichte: SR=0.35, PMA=0.20, TKR=0.25, EQ=0.20.

Wenn eine Metrik N/A ist, wird ihr Gewicht proportional auf die übrigen Metriken umverteilt:

- Alle Metriken vorhanden: `composite = 0.35*SR + 0.20*PMA + 0.25*TKR + 0.20*EQ`
- SR=N/A: `composite = (0.20*PMA + 0.25*TKR + 0.20*EQ) / 0.65`
- PMA=N/A: `composite = (0.35*SR + 0.25*TKR + 0.20*EQ) / 0.80`
- SR=N/A und PMA=N/A: `composite = (0.25*TKR + 0.20*EQ) / 0.45`

Wenn SR und PMA beide N/A sind, fließen nur TKR und EQ ein; wenn alle Metriken N/A sind, ist Composite = 0.0.

### Thresholds

| Score-Bereich | Label | Bedeutung |
|---------------|-------|-----------|
| ≥ 0.7 | **pass** | Retrieval-Qualität ausreichend |
| 0.4 – 0.7 | **weak** | Verbesserungspotential, Lücken dokumentieren |
| < 0.4 | **fail** | Kritische Lücke, Index oder Quellen prüfen |

Thresholds werden pro Frage und aggregiert pro Domain angewendet.

### Aggregation pro Domain

- **Domain Composite Score:** Mittelwert aller Frage-Composite-Scores.
- **Pass/Weak/Fail-Verteilung:** Anzahl und Prozent der Fragen in jeder Kategorie.
- **Metrik-Durchschnitte:** SR, PMA, TKR, EQ als Mittelwerte über alle Fragen (N/A-Metriken überspringen im Mittelwert).
- **Lücken-Report:** Fragen mit `fail` oder `weak` + konkrete Empfehlung.

## Reports

### Formate

- **Markdown** (`.md`): Menschenlesbar, mit Tabellen.
- **JSON** (`.json`): Maschinenlesbar, für weitere Verarbeitung.

### Speicherort

- `quality/reports/` — Arbeitsordner für generierte Reports (.gitignored, generierte Artefakte).
- `docs/superpowers/quality-reports/` — Archivierte/versionierte Reports (manuell kuratierte Report-Historie).

### Report-Struktur (Markdown)

```
# Quality Report: godot — 2026-06-29

## Summary
- Domain, Date, Questions evaluated, Composite Score, Pass/Weak/Fail-Verteilung

## Metric Averages
| Metric | Average |
(alle 4 Metriken, N/A markiert wenn nicht anwendbar)

## Per-Question Results
| ID | Question | Score | Label | SR | PMA | TKR | EQ |
(Tabelle aller Fragen)

## Weak / Fail Details
(Details für Fragen mit weak/fail, mit Empfehlung)

## Truncation Warnings
(Fragen mit truncation_warning > 0)

## Gaps & Recommendations
(Generelle Empfehlungen)
```

## Regression-Tests

### Quellenanker-Regression

Prüft, ob nach einem Index-Rebuild die gleichen `source_file`-Werte für Golden-Dataset-Fragen gefunden werden. Vergleich: vorher/nachher `source_file`-Sets. Implementiert via `run_evaluation.py --baseline <previous.json>`.

### Seitenzahlen-Regression (PDF-Domains)

Prüft, ob `page_start`-Werte nach Rebuild erhalten bleiben. Toleranz: ±2 Seiten (Chunking kann Seitengrenzen verschieben). Heuristisch — nicht als harre Regel zu verstehen.

## CLI-Skripte (Phase 1)

### `run_evaluation.py`

```
python scripts/quality/run_evaluation.py --domain godot
python scripts/quality/run_evaluation.py --domain godot --output results.json
python scripts/quality/run_evaluation.py --domain godot --baseline previous.json
```

Führt alle Fragen des Golden Dataset gegen `hybrid_search.search()` aus, berechnet Scores via scorer.py, gibt JSON aus. Vergleicht optional gegen Baseline für Regression-Detection.

## Integration mit test-hub-feature (Phase 2)

Der `test-hub-feature`-Agent bleibt report-only. Er kann `run_evaluation.py` aufrufen (read-only), schreibt keine neuen Golden-Dataset-Fragen. Detail-Integration in Phase 2.

## Bekannte Einschränkungen (Design-Entscheidungen)

- **LIM-002:** `section_path` und `chunk_type` fehlen bei DaVinci-Resolve-Chunks. Die Rubrik bewertet diese Felder nicht. PMA prüft nur `page_start`/`page_end`.
- **LIM-003:** `text`-Feld auf 5000 Zeichen trunciert. EQ prüft auf nicht-leeres Text-Feld, vermerkt Truncation als Warning (Heuristik, kein Score-Abzug).
- **Pickle-Sicherheit:** BM25-Indizes nutzen `pickle`. Die Quality Platform erzeugt keine neuen Pickle-Dateien. Bestehende Pickle-Dateien werden nur gelesen (via `bm25_search`).
- **Keine automatischen Index-Rebuilds:** Die Platform baut keine Indexes neu. Regression-Tests vergleichen gegen eine gespeicherte Baseline.
- **Keine LLM-Metriken:** Faithfulness, Answer-Relevancy, Context-Precision (im RAGAS-Sinne) sind out of scope, da der Hub kein Generator ist.
- **Gewichte/Thresholds hardcoded in Phase 1:** 0.35/0.20/0.25/0.20 und 0.7/0.4 sind im Code hardcoded. Konfigurierbarkeit (via YAML-Header oder quality/config.py) ist Phase 2 / Follow-up, nach ersten Evaluationsergebnissen.

## Out of Scope

- UI / Dashboard
- Datenbank-Backend
- Automatische Index-Rebuilds in Tests
- LLM-basierte Metriken (Faithfulness, Answer-Relevancy)
- Cloud-Plattform / Confident AI
- Automatische Generierung von Testfragen
- RAGAS / DeepEval / TruLens als Dependency
- Slack/Email-Benachrichtigungen
- CI/CD-Integration (kann später ergänzt werden)
- Phase 2: add_question.py, validate_dataset.py CLI, initiales Golden Dataset, test-hub-feature Integration, vollständige Doku-Updates

## Erfolgskriterien (Phase 1)

1. Spec existiert unter `docs/superpowers/specs/2026-06-29-knowledge-hub-quality-evaluation-platform-design.md`.
2. `pytest -m quality` läuft mit TDD-Tests (Mock-Results) für Loader, Scorer, Report-Generator.
3. `run_evaluation.py` ist funktionsfähig (manueller Smoke-Test gegen echten Index möglich, wenn Golden Dataset existiert — Golden Dataset selbst ist Phase 2).
4. Bestehende Test-Suite (`pytest -m unit/integration/e2e/mcp`) bleibt unverändert grün.
5. `pyyaml` ist in `requirements-dev.txt` und `THIRD_PARTY_LICENSES.md` dokumentiert.
6. `quality` Marker ist in `pyproject.toml` registriert.
7. `workspace_check.sh` prüft die neuen Verzeichnisse.
