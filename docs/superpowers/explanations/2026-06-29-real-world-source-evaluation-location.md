# Real-World Source Evaluation — Wo die Dateien leben

> **Anfängerfreundliche Erklärung** | 2026-06-29 | Real-World Source Evaluation

## Was wurde gemacht?

Das Golden Dataset wurde um **echte Online-Quellen** erweitert. Jede der 14 Testfragen (7 Godot, 7 DaVinci Resolve) hat jetzt eine `real_world_sources`-Liste mit URLs zu offiziellen Docs, GitHub Issues/PRs und Blackmagic-Produktseiten. Der Report zeigt diese Quellen neben den Hub-Suchergebnissen an, sodass Noah systematisch vergleichen kann: Findet der Hub die gleichen Antworten wie die Community?

## Datenmodell

Jede Frage im Golden Dataset hat jetzt ein neues Feld `real_world_sources` (Liste von Objekten):

| Feld | Typ | Beschreibung |
|------|-----|-------------|
| `url` | string | Vollständige URL der Online-Quelle |
| `date` | date \| null | Datum der Quelle |
| `type` | enum | `official-docs`, `github-issue`, `github-pr`, `forum`, `reddit`, `youtube`, `blog`, `stack-exchange`, `other` |
| `solution_summary` | string \| null | Kurze Zusammenfassung der Lösung (1–3 Sätze) |
| `has_solution` | boolean | Gibt es dort eine konkrete Lösung? |

Das alte Feld `real_world_source_url` (einzelner String) ist **deprecated** — es wird beim Laden automatisch in die neue Listen-Struktur konvertiert (backward-compat). Neue Fragen sollen nur noch `real_world_sources` verwenden.

## 3 Evaluations-Ebenen

Die Evaluation ist **semi-automatisiert**: Die Platform liefert die Daten, der Mensch (Noah) bewertet.

1. **Source Coverage** — Findet der Hub thematisch passende Quellen zu den Online-Quellen? (URL-Tabelle vs. `found_source_files`)
2. **Solution Alignment** — Kommt der Hub zur gleichen Lösung wie die Online-Quelle? (Vergleich `solution_summary` vs. Hub-Snippets)
3. **Gap Detection** — Welche Lücken zeigen die Online-Quellen auf, die der Hub nicht abdeckt? (insbesondere GitHub Issues)

## Wie man die Evaluation durchführt

```bash
# 1. Evaluation gegen den Live-Index ausführen
python scripts/quality/run_evaluation.py --domain godot --output /tmp/eval.json

# 2. Report generieren (Markdown + JSON)
python scripts/quality/generate_report.py --input /tmp/eval.json --output-dir /tmp/reports

# 3. Report öffnen und pro Frage durchgehen:
#    - "Real-World Source Comparison"-Sektion lesen
#    - URL-Tabelle mit Hub-Snippets vergleichen
#    - GFM-Checkboxen ankreuzen: Source Coverage, Solution Alignment, Gap Detection
```

## Report-Struktur

Der Markdown-Report enthält eine neue Sektion **"Real-World Source Comparison"** pro Frage:

- **URL-Tabelle:** Typ, URL, Solution Summary, Has Solution
- **Hub Top Snippets:** Top-3 Ergebnisse (200 Zeichen), mit Source-Filename
- **Found Sources:** Welche Hub-Quellen wurden gefunden
- **GFM-Checkboxen:** `- [ ] Source Coverage`, `- [ ] Solution Alignment`, `- [ ] Gap Detection`

## solution_summary TODO

Aktuell sind alle `solution_summary`-Werte `null` (TODO-Platzhalter, siehe LIM-005). Die manuelle Kuratierung durch Noah steht noch aus. Source Coverage (Ebene 1) und Gap Detection (Ebene 3) funktionieren bereits ohne Summaries — URLs und `has_solution` reichen dafür. Solution Alignment (Ebene 2) benötigt die Summaries für den vollständigen Vergleich.

## CLI-Befehle

```bash
# Dataset validieren (URL-Listen-Prüfung mit --strict-urls)
python scripts/quality/validate_dataset.py --domain godot --strict-urls

# Neue Frage mit Real-World-Quellen hinzufügen
python scripts/quality/add_question.py \
  --domain godot \
  --question "How do I ...?" \
  --expected-sources godot-docs-reference-packed.md \
  --difficulty easy \
  --tags rotation,node3d \
  --rws-url "https://docs.godotengine.org/..." \
  --rws-type official-docs
```

## Welche Dateien haben sich geändert?

| Pfad | Änderung |
|------|----------|
| `quality/golden/godot.yaml` | `real_world_sources` für alle 7 Fragen (Docs + GitHub Issues/PRs) |
| `quality/golden/davinci_resolve.yaml` | `real_world_sources` für alle 7 Fragen (Blackmagic-Produktseiten) |
| `scripts/quality/scorer.py` | `load_golden_dataset()`: Normalisierung alter Felder; `validate_question()`: neue Feld-Prüfung; `evaluate_question()`: `top_snippets`; `generate_markdown_report()`: Real-World-Sektion mit GFM-Checkboxen |
| `scripts/quality/validate_dataset.py` | `--strict-urls` validiert jetzt auch `real_world_sources`-Listen + type-Enum-Warnings + Deprecation-Warnung |
| `scripts/quality/run_evaluation.py` | `real_world_sources` und `top_snippets` im Output |
| `scripts/quality/add_question.py` | Neue `--rws-url`, `--rws-type`, `--rws-date`, `--rws-has-solution` Flags |
| `tests/quality/` | 18 neue Tests (Normalisierung, Validierung, Report-Sektion, top_snippets) |

## Weiterlesen

- **Spec:** `docs/superpowers/specs/2026-06-29-real-world-source-evaluation-design.md`
- **Known Issues:** `docs/ai/known-issues.md` (LIM-005: solution_summary null)
- **Changelog:** `docs/ai/changelog.md` (2026-06-29, letzter Eintrag)
