# Explanation — Quality Metrics v2

**Datum:** 2026-07-07
**Status:** Abgeschlossen
**Commit:** 2afdc8d, 1ce7838

## Was gebaut wurde

Die Quality Evaluation Platform hatte 2 Metriken die **konstante Werte** lieferten und 40% des Composite-Scores zu Noise machten. Ersetzt durch 4 diskriminative Metriken aus RAG-Evaluation-Forschung (Ragas, NDCG).

### Problem
- TKR = 0.55 (immer, für 10 Results) — 20% Gewicht, kein Signal
- EQ = 1.0 (fast immer) — 15% Gewicht, kein Signal
- Zusammen 35% Gewicht = 0.26 Punkte Noise pro Frage

### Lösung

| Alt | Neu | Forschung |
|-----|-----|-----------|
| TKR (konstant 0.55) | **NDCG@10** (4-stufige Relevanz, 0.67–0.99) | NDCG aus IR-Standard |
| PMA ±2 (binär) | **Jaccard Page Overlap** (kontinuierlich 0.03–1.0) | Jaccard-Index |
| SR (binär 0/0.5/1) | **Weighted Source Recall** (mit Gewichten) | Ragas Context Recall |
| — | **Source Diversity** (Shannon-Entropie, neu) | Information Theory |

### Neue Gewichte
```
source_recall:          0.25  (Weighted SR)
page_metadata_accuracy: 0.15  (Jaccard)
top_k_relevance:        0.20  (NDCG@10)
evidence_quality:       0.10  (EQ, reduziert von 0.20)
image_presence:         0.20  (Vision Retrieval)
source_diversity:       0.10  (neu)
```
70% diskriminativ (war 60%).

### HyDE
`scripts/hyde.py`: LLM generiert hypothetisches Dokument → besseres semantisches Embedding. Optional via `KH_HYDE_ENABLED=1`.

### Geänderte Dateien
| Datei | Änderung |
|------|----------|
| `scripts/quality/scorer.py` | 4 neue Metrik-Funktionen + Report-Update |
| `scripts/quality/config.py` | Neue DEFAULT_WEIGHTS |
| `scripts/hyde.py` | Neues Modul (HyDE) |
| `scripts/hybrid_search.py` | HyDE-Integration |
| `quality/golden/davinci_resolve.yaml` | Neue weights + page ranges |
| `docs/issues/quality-metrics-v2/` | SDD Issue (spec + plan + retro) |

### Eval-Ergebnis
- **davinci_resolve:** 0.7234 → 0.8017 (+0.0783), 15 → 21 pass
- **godot (backward-compat):** 0.9153 unverändert, 19 pass
