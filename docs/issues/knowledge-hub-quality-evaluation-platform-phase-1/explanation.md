# Quality Evaluation Platform Phase 1 — Wo die Dateien leben

> **Anfängerfreundliche Erklärung** | 2026-06-29 | Phase 1 (MVP)

## Was ist passiert?

Der Knowledge Hub hat eine **Quality Evaluation Platform** bekommen — ein System, das automatisch prüft, wie gut die Suche funktioniert. Phase 1 liefert die Grundbausteine: Scoring-Funktionen, einen CLI-Runner und TDD-Tests. Das eigentliche Golden Dataset (die Testfragen) kommt in Phase 2.

## Welche Dateien haben sich geändert — und warum?

### Neue Dateien und Verzeichnisse

| Pfad | Typ | Was es macht |
|---|---|---|
| `quality/golden/` | Verzeichnis | YAML-Dateien mit Testfragen pro Domain (aktuell nur `.gitkeep`). |
| `quality/reports/` | Verzeichnis | Generierte Reports (`.gitignore`-d, außer `.gitkeep`). |
| `scripts/quality/` | Verzeichnis | Python-Code: `scorer.py` + `run_evaluation.py`. |
| `tests/quality/` | Verzeichnis | 68 TDD-Tests (Loader, Scorer, Report-Generator). |
| `docs/superpowers/quality-reports/` | Verzeichnis | Archivierte Reports (aktuell nur `.gitkeep`). |
| `scripts/quality/scorer.py` | Datei | **Pure functions** — 4 Metriken (SR, PMA, TKR, EQ), Reports. Kein `hybrid_search`-Import → testbar mit Mock-Daten. |
| `scripts/quality/run_evaluation.py` | Datei | **CLI-Wrapper** — ruft `hybrid_search.search()` auf, optionaler Regression-Check gegen Baseline. |
| `docs/superpowers/specs/2026-06-29-knowledge-hub-quality-evaluation-platform-design.md` | Datei | Vollständige Design-Spec. |

### Geänderte Dateien

| Datei | Änderung |
|---|---|
| `pyproject.toml` | Neuer pytest-Marker `quality`. |
| `requirements-dev.txt` | `pyyaml>=6.0.0,<7.0.0` hinzugefügt. |
| `.gitignore` | `quality/reports/*.md`/`*.json` ignoriert, `.gitkeep` ausgenommen. |
| `scripts/workspace_check.sh` | Neue `required_dirs` für Quality-Verzeichnisse. |
| `THIRD_PARTY_LICENSES.md` | Neue Sektion für `pyyaml` (MIT, Dev-Abhängigkeit). |
| `docs/ai/changelog.md` | Phase-1-Eintrag. |
| `docs/ai/validation.md` | `pytest -m quality` ergänzt. |

## Architektur: Pure Functions vs. CLI-Wrapper

Das ist der wichtigste Design-Trick der Platform:

```
┌──────────────────────────────┐
│  run_evaluation.py (CLI)     │  ← ruft hybrid_search.search() auf
│  import hybrid_search        │     (braucht echten Index)
└──────────┬───────────────────┘
           │ übergibt Suchergebnisse
           ▼
┌──────────────────────────────┐
│  scorer.py (pure functions)  │  ← KEIN hybrid_search-Import
│  load_golden_dataset()       │     (testbar mit Mock-Daten,
│  score_source_recall()       │      kein echter Index nötig)
│  evaluate_question()         │
│  generate_markdown_report()  │
└──────────────────────────────┘
```

- **`scorer.py`** enthält nur Funktionen, die Suchergebnisse als Argumente bekommen. Sie rufen nie selbst die Suche auf. Deshalb kannst du sie mit `pytest -m quality` testen, ohne dass ein Index existieren muss — die Tests schieben einfach Fake-Ergebnisse rein.
- **`run_evaluation.py`** ist der einzige Ort, der `hybrid_search.search()` aufruft. Es lädt das Golden Dataset, sucht jede Frage, reicht die Ergebnisse an `scorer.py` weiter und gibt das Ergebnis aus.

## Die Bewertungsrubrik (4 Metriken)

Jede Frage im Golden Dataset wird mit 4 Metriken bewertet (alle Werte 0–1, höher = besser):

| Metrik | Kürzel | Was sie misst | Gewicht |
|---|---|---|---|
| **Source Recall** | SR | Wie viele der erwarteten Quellen wurden in den Top-Ergebnissen gefunden? | 0.35 |
| **Page Metadata Accuracy** | PMA | Haben die Ergebnisse `page_start`-Metadaten (nur für PDF-Domains wie DaVinci Resolve)? | 0.20 |
| **Top-K Relevance** | TKR | Rang-basierter Score: Ergebnisse auf Rang 1 zählen mehr als auf Rang 10. | 0.25 |
| **Evidence Quality** | EQ | Haben die Ergebnisse ein nicht-leeres `text`-Feld (damit man die Antwort nachlesen kann)? | 0.20 |

### N/A-Logik: Wenn eine Metrik nicht anwendbar ist

- **SR = N/A**, wenn `expected_source_files` leer ist (keine Quellen-Erwartung).
- **PMA = N/A** für nicht-PDF-Domains wie Godot (keine `page_start`-Metadaten).
- Wenn eine Metrik N/A ist, wird ihr Gewicht auf die übrigen Metriken umverteilt. Beispiel: Bei Godot ist PMA=N/A, also zählen SR, TKR und EQ zusammen 100 % (statt 80 %).

### Thresholds

| Composite Score | Label | Bedeutung |
|---|---|---|
| ≥ 0.7 | **pass** | Retrieval-Qualität ausreichend |
| 0.4 – 0.7 | **weak** | Verbesserungspotential |
| < 0.4 | **fail** | Kritische Lücke |

## Validierungsbefehle

```bash
pytest -m quality                    # 68 Tests, Mock-Daten, kein Index nötig
pytest -m unit                       # Bestehende Test-Stufen
pytest -m integration
pytest -m e2e
pytest -m mcp
./scripts/workspace_check.sh         # Struktur-Check (neue Verzeichnisse)
python3 -m py_compile scripts/quality/scorer.py
python3 -m py_compile scripts/quality/run_evaluation.py

# Evaluation gegen echten Index (braucht Golden Dataset YAML)
python scripts/quality/run_evaluation.py --domain godot --output results.json
python scripts/quality/run_evaluation.py --domain godot --baseline previous.json
```

## Golden Dataset Konzept

Ein **Golden Dataset** ist eine YAML-Datei pro Domain (z. B. `quality/golden/godot.yaml`), die Testfragen mit erwarteten Antworten enthält:

```yaml
domain: godot
version: 1
questions:
  - id: godot-001
    question: "How do I rotate a Node3D around the Y axis in GDScript?"
    expected_source_files:
      - "godot-docs-packed.md"
    expected_page_ranges: []      # leer = keine PDF-Seiten
    difficulty: easy
    tags: [rotation, node3d, 3d]
    min_top_k: 5
```

- **Phase 1:** Die Infrastruktur steht, aber die YAML-Dateien sind noch leer (nur `.gitkeep`).
- **Phase 2:** Echte Fragen werden hinzugefügt — aus Foren, GitHub Issues, YouTube-Kommentaren und Noahs eigener Erfahrung.

## Reports: generiert vs. archiviert

- `quality/reports/` — Arbeitsordner, `.gitignore`-d. Hier landen Ergebnisse von `--output results.json`.
- `docs/superpowers/quality-reports/` — Versioniert. Reports, die du behalten willst, kopierst du hierher und committest sie.

## Wo man weiterliest

- **Design-Spec:** `docs/superpowers/specs/2026-06-29-knowledge-hub-quality-evaluation-platform-design.md` — vollständige Architektur, alle Metriken im Detail, Regression-Tests, Out of Scope.
- **Validierung:** `docs/ai/validation.md` — alle Test-Befehle und die Knowledge-QA-Checklist.
- **Architektur:** `docs/ai/architecture.md` — wie der Knowledge Hub insgesamt aufgebaut ist.
- **Bekannte Einschränkungen:** `docs/ai/known-issues.md` — TD-002 (Golden Dataset fehlt noch), LIM-002 (kein `section_path` bei DaVinci), LIM-003 (`text`-Feld auf 5000 Zeichen trunciert).
- **Changelog:** `docs/ai/changelog.md` — der Phase-1-Eintrag unter 2026-06-29.

## Nächste Schritte (Phase 2)

- Echte Golden-Dataset-YAML-Dateien mit Fragen befüllen (`quality/golden/godot.yaml`, `davinci_resolve.yaml`).
- CLI-Skripte `add_question.py`, `validate_dataset.py`, `generate_report.py` bauen.
- `test-hub-feature`-Agent mit der Quality Platform integrieren.
- Gewichte und Thresholds nach ersten echten Evaluationsergebnissen kalibrieren.
