# Quality Evaluation Platform Phase 2 — Wo die Dateien leben

> **Anfängerfreundliche Erklärung** | 2026-06-29 | Phase 2 (Golden Datasets + CLIs + E2E)

## Was ist passiert?

Phase 2 der Quality Evaluation Platform ist fertig. Der Knowledge Hub hat jetzt **echte Testfragen** (Golden Datasets) für Godot und DaVinci Resolve, drei neue CLI-Werkzeuge zum Validieren, Hinzufügen und Reporten, E2E-Tests die gegen den echten Index laufen, und Security-Hardening gegen Path-Traversal und SSRF. Der `test-hub-feature`-Agent kann die Platform jetzt read-only nutzen.

## Welche Dateien haben sich geändert — und warum?

### Neue Dateien

| Pfad | Was es macht |
|---|---|
| `quality/golden/godot.yaml` | 7 kuratierte Testfragen für Godot (easy/medium/hard). Fragen stammen aus E2E-Tests und der Answer-Synthesis-Spec. |
| `quality/golden/davinci_resolve.yaml` | 7 kuratierte Testfragen für DaVinci Resolve (easy/medium/hard). |
| `scripts/quality/add_question.py` | CLI zum manuellen Hinzufügen neuer Fragen ans Golden Dataset. Generiert automatisch die nächste ID (`<domain>-NNN`). Nur für menschliche Kuratierung — `test-hub-feature` darf es nicht aufrufen. |
| `scripts/quality/validate_dataset.py` | CLI zum Prüfen der Golden-Dataset-YAML: Struktur, Quellen-Existenz, URL-Sicherheit, Secret-Patterns. |
| `scripts/quality/generate_report.py` | CLI zum Generieren von Markdown- und JSON-Reports aus einem `results.json`. |
| `tests/quality/test_validate_dataset.py` | 31 Unit-Tests für URL-Validierung, Secret-Check, Quellen-Prüfung und Strict-URL-Modus. |
| `tests/quality/test_godot_quality.py` | 3 E2E-Tests: Ergebnisse vorhanden, nicht alle fail, alle Felder vorhanden. Läuft gegen echten Godot-Index. |
| `tests/quality/test_davinci_quality.py` | 4 E2E-Tests: wie Godot, plus Page-Metadata-Prüfung (PMA > 0 für PDF-Domain). |

### Geänderte Dateien

| Datei | Änderung |
|---|---|
| `scripts/quality/run_evaluation.py` | Domain-Validierung (`^[a-z0-9_]+$`) als Path-Traversal-Schutz vor `run_evaluation()`. |
| `.opencode/agents/test-hub-feature.md` | Neuer Abschnitt „Quality Evaluation Platform": Agent darf `validate_dataset.py`, `run_evaluation.py` und `generate_report.py` read-only aufrufen. |
| `docs/ai/known-issues.md` | TD-002 als resolved markiert (Golden Dataset existiert jetzt). |
| `docs/ai/changelog.md` | Phase-2-Eintrag mit allen neuen Dateien und Security-Hardening. |
| `docs/ai/validation.md` | CLI-Befehle für `validate_dataset.py`, `add_question.py`, `run_evaluation.py`, `generate_report.py` ergänzt. |

## Golden Dataset Konzept

Ein **Golden Dataset** ist eine YAML-Datei pro Domain unter `quality/golden/<domain>.yaml`. Jede Datei enthält Testfragen mit erwarteten Antworten:

```yaml
domain: godot
version: 1
questions:
  - id: godot-001
    question: "How do I rotate a Node3D around the Y axis in GDScript?"
    expected_source_files:
      - "godot-docs-reference-packed.md"
    expected_page_ranges: []      # leer = keine PDF-Seiten-Erwartung
    difficulty: easy
    tags: [rotation, node3d, 3d, gdscript]
    min_top_k: 10
```

**Wichtige Felder:**
- `expected_source_files` — welche Quell-Dateien sollten in den Top-Ergebnissen auftauchen. Die Namen sind **bare filenames** (so wie ChromaDB sie in `source_file` speichert), z. B. `"godot-docs-reference-packed.md"`. Sie können in `domains/<domain>/sources/` ODER `domains/<domain>/personal/` liegen.
- `expected_page_ranges` — für PDF-Domains wie DaVinci Resolve: erwartete Seitenbereiche. Aktuell bei allen Fragen `[]` (noch nicht verifiziert).
- `real_world_source_url` — Link zur realen Quelle (Forum, GitHub Issue). Aktuell bei allen Fragen `null` (noch nicht kuratiert).

**Wie Fragen kuratiert werden:**
1. **Manuell via `add_question.py`** — das ist der vorgesehene Weg. Das Skript validiert die Frage, generiert die nächste ID und hängt sie ans YAML an.
2. **Manuell im YAML-Editor** — du kannst die YAML-Datei auch direkt editieren. `validate_dataset.py` prüft dann die Struktur.
3. **NICHT automatisch** — `test-hub-feature` und andere Agenten dürfen keine neuen Fragen schreiben. Das Golden Dataset ist menschenkuratiert.

## CLI-Skripte

### `validate_dataset.py` — Golden Dataset prüfen

```bash
# Basis-Validierung (YAML-Struktur, IDs, Difficulty, Datum)
python scripts/quality/validate_dataset.py --domain godot

# Plus: prüfen ob expected_source_files in sources/ ODER personal/ existieren
python scripts/quality/validate_dataset.py --domain godot --check-sources

# Plus: URL-Warnings als Errors behandeln (file://, localhost, private IPs)
python scripts/quality/validate_dataset.py --domain godot --strict-urls
```

Was es prüft:
- YAML-Struktur (alle Pflichtfelder, gültige Difficulty, ID-Präfix, Datumsformat)
- Quellen-Existenz (`--check-sources`: sucht in `sources/` UND `personal/`)
- URL-Sicherheit (lehnt `file://`, `ftp://`, `data:`, localhost, 127.0.0.1, ::1, RFC1918 ab)
- Secret-Patterns (immer als **WARNING**, nie als Error — legitime Fragen können "API key" erwähnen)

### `add_question.py` — Frage hinzufügen (manuelle Kuratierung)

```bash
python scripts/quality/add_question.py \
  --domain godot \
  --question "How do I rotate a Node3D around the Y axis?" \
  --expected-sources godot-docs-reference-packed.md \
  --difficulty easy \
  --tags rotation,node3d,3d,gdscript \
  --notes "Beginner question"
```

- Generiert automatisch die nächste ID (z. B. `godot-008`).
- Validiert die Frage vor dem Anhängen.
- Schreibt mit `yaml.dump(allow_unicode=True, default_flow_style=False, sort_keys=False)`.

### `generate_report.py` — Reports aus results.json generieren

```bash
# Markdown + JSON Report im Default-Verzeichnis (quality/reports/)
python scripts/quality/generate_report.py --input results.json

# In eigenes Verzeichnis
python scripts/quality/generate_report.py --input results.json --output-dir my-reports/

# Ins Archiv (docs/superpowers/quality-reports/)
python scripts/quality/generate_report.py --input results.json --archive
```

### `run_evaluation.py` — Evaluation gegen echten Index

```bash
# Alle Golden-Dataset-Fragen gegen den Index laufen lassen
python scripts/quality/run_evaluation.py --domain godot

# Ergebnis als JSON speichern
python scripts/quality/run_evaluation.py --domain godot --output results.json

# Regression-Check gegen vorherigen Lauf
python scripts/quality/run_evaluation.py --domain godot --baseline previous.json
```

## Security-Hardening

Drei Schutzebenen wurden in Phase 2 eingebaut:

1. **Domain-Validierung (Path-Traversal-Schutz):** Bevor `run_evaluation.py` eine Datei öffnet oder den Index anspricht, prüft `_validate_domain()` mit Regex `^[a-z0-9_]+$`. Ein Domain-Name wie `../../etc/passwd` wird sofort abgelehnt.

2. **URL-Validierung (SSRF-Schutz):** `validate_dataset.py` prüft `real_world_source_url` auf gefährliche Schemas (`file://`, `ftp://`, `data:`) und blockiert localhost, Loopback-IPs (127.0.0.1, ::1) sowie private IPs (10/8, 172.16/12, 192.168/16). Standardmäßig sind das Warnings — mit `--strict-urls` werden sie zu Errors.

3. **Secret-Pattern-Check:** `validate_dataset.py` scannt `question`- und `notes`-Felder auf Muster wie `api_key=...`, `sk-...` (OpenAI-Keys), `ghp_...` (GitHub-Tokens). Funde sind **immer Warnings**, nie Errors — legitime Fragen können "API key" oder "token" erwähnen, ohne ein echtes Secret zu enthalten.

## E2E Quality Tests

Die Dateien `tests/quality/test_godot_quality.py` und `tests/quality/test_davinci_quality.py` sind **echte End-to-End-Tests** — sie rufen `run_evaluation()` auf, das wiederum `hybrid_search.search()` gegen den live Index ausführt.

**Skipif-Logik:** Beide Testdateien haben `pytest.mark.skipif` auf Modulebene:
- Wenn `chromadb_data/<domain>/chroma/` nicht existiert → Test wird übersprungen mit Hinweis `"Run: python scripts/embed_index.py --domain <domain>"`.
- Wenn `quality/golden/<domain>.yaml` nicht existiert → Test wird übersprungen.

Das bedeutet: Auf einem frischen Checkout ohne gebauten Index laufen die E2E-Tests nicht — sie werden sauber geskippt. Auf Noahs Maschine mit gebautem Index laufen sie durch.

**Godot (3 Tests):** `test_godot_quality_has_results`, `test_godot_quality_not_all_fail`, `test_godot_quality_evaluations_have_expected_fields`.

**DaVinci (4 Tests):** Die gleichen drei plus `test_davinci_quality_page_metadata_present` — stellt sicher, dass mindestens eine Frage einen PMA-Wert > 0 hat (Page-Metadaten gehen nicht verloren).

## test-hub-feature Integration

Der `test-hub-feature`-Agent (`.opencode/agents/test-hub-feature.md`) hat einen neuen Abschnitt „Quality Evaluation Platform". Er darf:

- `validate_dataset.py --domain <domain>` aufrufen (Golden Dataset Struktur prüfen)
- `run_evaluation.py --domain <domain>` aufrufen (Evaluation gegen live Index, read-only)
- `generate_report.py --input <results.json>` aufrufen (Report generieren)

Er darf **nicht** `add_question.py` aufrufen — das ist ein manueller Kuratierungsschritt.

## Live-Ergebnisse (2026-06-29)

Smoke-Tests gegen die gebauten Indizes:

| Domain | Fragen | Pass | Weak | Fail | Avg Composite |
|---|---|---|---|---|---|
| Godot | 7 | 7 | 0 | 0 | 0.86 |
| DaVinci Resolve | 7 | 6 | 1 | 0 | 0.84 |

**dvr-002 (trim clip, weak 0.54):** Die Frage "How do I trim a clip on the Edit page in DaVinci Resolve?" erreicht nur 0.54. Das ist ein echtes Qualitäts-Finding — mögliche Ursache: Die Frage ist zu generisch formuliert, oder der Editors Guide (`davinci-resolve-20-editors-guide.md`) rankt nicht stark genug. Follow-up: Frage verfeinern oder personal note ergänzen.

## Wo man weiterliest

- **Design-Spec:** `docs/superpowers/specs/2026-06-29-knowledge-hub-quality-evaluation-platform-design.md` — vollständige Architektur, alle Metriken, Bewertungsrubrik, Regression-Tests.
- **Validierung:** `docs/ai/validation.md` — alle CLI-Befehle und Test-Stufen.
- **Bekannte Einschränkungen:** `docs/ai/known-issues.md` — TD-002 (resolved), LIM-002 (kein `section_path` bei DaVinci), LIM-003 (Truncation auf 5000 Zeichen).
- **Phase 1 Location:** `docs/superpowers/explanations/2026-06-29-knowledge-hub-quality-evaluation-platform-phase-1-location.md` — Grundbausteine aus Phase 1 (scorer.py, pure functions, TDD).
- **Phase 1 Retro:** `docs/superpowers/retrospectives/2026-06-29-knowledge-hub-quality-evaluation-platform-phase-1.md`
- **Changelog:** `docs/ai/changelog.md` — der Phase-2-Eintrag unter 2026-06-29.
