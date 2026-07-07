# Plan: Quality Metrics v2

**Task-ID:** quality-metrics-v2
**Datum:** 2026-07-07
**Spec:** docs/issues/quality-metrics-v2/spec.md

## Tasks

### Task 1: NDCG@10 Metrik (scorer.py)
- Neue Funktion `score_ndcg(results, question)` mit 4-stufiger Relevanz
- Relevanz-Heuristik: rel=3 (source+page match), rel=2 (source match), rel=1 (keyword overlap), rel=0 (none)
- DCG/IDCG Berechnung mit `log2(i+1)` Diskontierung
- Ersetzt `score_top_k_relevance()` in `evaluate_question()`
- **Verify:** Unit-Test mit mock results (relevante Chunks auf Rang 1 vs Rang 5 → NDCG unterscheidet)

### Task 2: Jaccard Page Overlap (scorer.py)
- Neue Funktion `score_jaccard_page_overlap(results, expected_page_ranges, is_pdf_domain)`
- Berechnet Jaccard-Index pro expected_page_range, nimmt max
- Set-Operation: `|expected ∩ actual| / |expected ∪ actual|`
- Ersetzt `score_page_metadata_accuracy()` in `evaluate_question()`
- **Verify:** Unit-Test: expected[37-42] actual[36-40] → Jaccard=0.571; actual[37-42] → 1.0; actual[100-105] → 0.0

### Task 3: Weighted Source Recall (scorer.py + golden dataset)
- Erweitere `score_source_recall()` zu `score_weighted_source_recall(results, expected_source_files)`
- Parse optionales `weight`-Feld pro Source-Eintrag im Golden Dataset
- Backward-kompatibel: ohne weight → Default 1.0
- **Verify:** Unit-Test: 2 sources mit weights [2.0, 1.0], 1 found (weight 2.0) → WSR=0.667

### Task 4: Source Diversity (scorer.py)
- Neue Funktion `score_source_diversity(results)` — Shannon-Entropie normalisiert
- Berechnet Anteil jeder Quelle in Top-10, dann `-Σ(p × log2(p)) / log2(n)`
- **Verify:** Unit-Test: 10 results aus 1 Quelle → 0.0; 10 aus 5 Quellen (je 2) → ~0.93

### Task 5: Config + Weights aktualisieren (config.py + golden dataset)
- `DEFAULT_WEIGHTS` aktualisieren: NDCG=0.20, Jaccard=0.15, WSR=0.30, EQ=0.10, IP=0.20, Diversity=0.05
- `davinci_resolve.yaml` weights-Block aktualisieren
- `godot.yaml` — keine Änderung (IP=None → auto-umverteilt)
- **Verify:** `validate_dataset.py` für beide Domains OK

### Task 6: Report-Generierung aktualisieren (scorer.py)
- `generate_markdown_report()`: 6 Metriken in Tabelle (SR, PMA→Jaccard, NDCG, EQ, IP, Diversity)
- `aggregate_domain_scores()`: avg_source_diversity hinzufügen
- Per-Question-Tabelle: neue Spalten NDCG, Jaccard, Div
- **Verify:** Report zeigt alle Metriken, Bild-Fragen haben IP+Div, Text-Fragen haben N/A

### Task 7: Unit-Tests (tests/unit/test_scorer.py)
- Tests für alle 4 neuen Metrik-Funktionen (NDCG, Jaccard, WSR, Diversity)
- Tests für backward-compat (ohne weight-Feld, ohne page_ranges, ohne modality)
- Tests für edge cases (leere results, einzelne result, alle relevant, alle irrelevant)
- **Verify:** `pytest -m unit -q` → alle grün

### Task 8: Eval + Vergleich (run_evaluation.py)
- Eval mit neuen Metriken für davinci_resolve laufen lassen
- Vergleich: alt (0.7234, 15 pass) vs neu
- Report generieren und prüfen: höhere Varianz zwischen pass/weak?
- godot eval läuft ebenfalls (backward-compat check)
- **Verify:** Eval komplett, Report zeigt diskriminativere Scores

## Reihenfolge

Task 1-4 können parallel entwickelt werden (unabhängige Metrik-Funktionen).
Task 5 braucht Task 1-4. Task 6 braucht Task 5. Task 7 braucht Task 1-4. Task 8 braucht alles.

```
Task 1 (NDCG) ──┐
Task 2 (Jaccard)┤
Task 3 (WSR) ───┼── Task 5 (Config) ── Task 6 (Report) ── Task 8 (Eval)
Task 4 (Div) ───┤
                 └── Task 7 (Tests)
```

## Validierung

```bash
.venv/bin/python -m py_compile scripts/quality/*.py
.venv/bin/pytest -m unit -q
./scripts/workspace_check.sh
.venv/bin/python scripts/quality/validate_dataset.py --domain davinci_resolve
.venv/bin/python scripts/quality/validate_dataset.py --domain godot
```

## Risiko

- **Niedrig:** Alle Änderungen sind im Scorer (Pure Functions), kein Re-Build nötig
- **Backward-compat:** Godot ohne PDF-Metadaten → PMA=None → Jaccard=None → Gewichts-Umverteilung
- **Golden Dataset:** Optionale `weight`-Felder → ohne Feld = Default 1.0 = aktuelle SR
