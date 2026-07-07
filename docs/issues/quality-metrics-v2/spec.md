# Spec: Quality Metrics v2 — Diskriminative Eval-Metriken

**Task-ID:** quality-metrics-v2
**Datum:** 2026-07-07
**Status:** open
**Priorität:** high

## Problem

Die aktuelle Quality Evaluation Platform hat 2 Metriken die **konstante Werte** liefern und damit 40% des Composite-Scores zu Noise machen:

| Metrik | Weight | Wert | Signal? | Beitrag |
|--------|--------|------|---------|---------|
| TKR (Top-K Relevance) | 0.20 | **0.55 (immer)** | ❌ Konstante | 0.11 |
| EQ (Evidence Quality) | 0.15 | **1.0 (fast immer)** | ❌ Konstante | 0.15 |
| **Konstant gesamt** | **0.35** | | | **0.26 von 1.0** |

**Auswirkung:** Bei pass-Schwelle 0.7 müssen die verbleibenden 30% diskriminativer Metriken (SR + PMA + IP) ~1.47 erreichen — praktisch SR=1.0 + PMA=1.0. Unrealistisch.

**Aktuelles Eval-Ergebnis (davinci_resolve, 2026-07-07):**
- 26 Fragen: 15 pass, 11 weak, 0 fail
- Avg Composite: 0.7234
- 5/11 weak wegen SR=0.5 (binär, nur 1 von 2 expected sources gefunden)
- 7/11 weak wegen PMA<0.5 (±2 Toleranz zu starr für Late Chunking)

## Ziel

Ersetze Konstanten und binäre Metriken durch **diskriminative, kontinuierliche Metriken** die echte Relevanz erfassen. Die Metriken sollten:
- Zwischen pass und weak unterscheiden können
- Kontinuierlich 0.0–1.0 sein (nicht nur 0.0/0.5/1.0)
- Industriestandards folgen (Ragas, NDCG, Jaccard)
- Backward-kompatibel sein (Godot ohne PDF-Metadaten nicht bestrafen)

## Anforderungen

### 1. NDCG@10 statt TKR (Top-K Relevance)

**Aktuell:** `score_top_k_relevance()` = `1.0 - (i/total)` → für 10 Results immer 0.55.

**Neu:** NDCG@10 mit 4-stufiger Relevanzskala:

```
Relevanz-Levels:
  0 = Chunk enthält nichts zur Frage
  1 = Chunk erwähnt Thema am Rande
  2 = Chunk enthält relevante Information
  3 = Chunk enthält die exakte Antwort/Code-Snippet
```

**Formel:**
```
DCG@10  = Σ(i=1..10) (2^rel_i - 1) / log2(i + 1)
IDCG@10 = DCG der idealen Sortierung (absteigend nach rel)
NDCG@10 = DCG@10 / IDCG@10
```

**Relevanz-Bestimmung:** Da kein manuelles Relevance-Judgment pro Chunk verfügbar ist, wird Relevanz heuristisch aus den vorhandenen Metadaten abgeleitet:
- `rel=3`: chunk ist aus einem `expected_source_file` UND `page_start` in `expected_page_ranges` ±2
- `rel=2`: chunk ist aus einem `expected_source_file` (ohne Page-Match)
- `rel=1`: chunk text enthält Query-Keywords (BM25-Token-Overlap > 0)
- `rel=0`: kein Match

**Gewicht:** Ersetzt TKR weight (0.20 → bleibt 0.20, oder neu verteilen).

### 2. Jaccard Page Overlap statt PMA ±2

**Aktuell:** `score_page_metadata_accuracy()` prüft ob `page_start/page_end` innerhalb `expected_page_ranges ±2` liegt → binär 0/1 pro Range, gemittelt.

**Neu:** Jaccard Page Overlap — natürlich kontinuierlich, keine willkürliche Toleranz:

```
expected_pages = Menge der Seiten in expected_page_ranges
actual_pages   = Menge der Seiten von page_start bis page_end
Jaccard = |expected_pages ∩ actual_pages| / |expected_pages ∪ actual_pages|
```

**Beispiel:** expected [37,42], actual [36,40] → overlap={37,38,39,40}=4, union={36,37,38,39,40,41,42}=7 → Jaccard=0.571

**Multi-Range:** Bei mehreren `expected_page_ranges` wird der beste Jaccard genommen (max).

**Gewicht:** Ersetzt PMA weight (0.15 → bleibt 0.15).

### 3. Weighted Source Recall statt binärer SR

**Aktuell:** `score_source_recall()` = `|found ∩ expected| / |expected|` → bei 2 expected und 1 found = 0.5 (binär-stufig).

**Neu:** Weighted Source Recall — kontinuierlich, mit optionalem Gewicht pro Quelle:

```yaml
# Golden Dataset kann Gewichte pro Source definieren:
expected_source_files:
  - file: "davinci-resolve-20.3-reference-manual.md"
    weight: 2.0  # Hauptreferenz
  - file: "davinci-resolve-20-colorist-guide.md"
    weight: 1.0  # Nebenquelle
```

**Formel:**
```
WSR = Σ(w_s × found_s) / Σ(w_s)  für s ∈ expected_sources
```

**Backward-kompatibel:** Ohne `weight`-Feld → Default weight 1.0 (identisch mit aktueller SR).

**Gewicht:** Ersetzt SR weight (0.30 → bleibt 0.30).

### 4. Source Diversity (neue Metrik)

**Neu:** Shannon-Entropie der Quell-Verteilung in Top-10, normalisiert:

```
p_i = Anteil der Quelle i in Top-10 (count_i / 10)
Diversity = -Σ(p_i × log2(p_i)) / log2(num_unique_sources)
```

**Beispiel:** 10 Results aus 1 Quelle → Diversity=0.0. 10 Results aus 5 Quellen (je 2) → Diversity=0.93.

**Warum:** Belohnt Retrieval das über multiple Quellen streut (wichtig bei 10+ PDF-Handbüchern). Verhindert dass ein einzelnes Handbuch alle Slots dominiert.

**Gewicht:** Neu, 0.05 (genommen von EQ das auf 0.10 reduziert wird).

### 5. EQ (Evidence Quality) reduzieren oder entfernen

**Aktuell:** EQ=1.0 fast immer (jedes Result hat text). Konstante ohne Signal.

**Option A:** EQ weight auf 0.10 reduzieren (statt 0.15), Diversity bekommt 0.05.
**Option B:** EQ entfernen und weight auf Diversity (0.15) geben.

**Empfehlung:** Option A (EQ behalten aber reduzieren — falls zukünftig mal leere Text-Felder auftauchen).

### 6. Neue Gewichtsverteilung (Ziel)

```
source_recall:          0.30  (Weighted SR, diskriminativ)
page_metadata_accuracy: 0.15  (Jaccard, diskriminativ)
top_k_relevance:        0.20  (NDCG@10, diskriminativ)
evidence_quality:       0.10  (EQ, reduziert — fast konstant)
image_presence:         0.20  (bestehend, nur Bild-Fragen)
source_diversity:       0.05  (neu, Shannon-Entropie)
─────────────────────────────
Summe:                  1.00
```

**Nicht-Bild-Domains (Godot):** IP=None → Gewicht umverteilt. Diversity+EQ = 0.15.
**Diskriminative Metriken:** SR+PMA+NDCG+Diversity = 0.70 (vorher 0.60).

## Akzeptanzkriterien

1. `score_top_k_relevance()` ersetzt durch `score_ndcg()` — NDCG@10 mit 4-stufiger Relevanz
2. `score_page_metadata_accuracy()` ersetzt durch `score_jaccard_page_overlap()` — Jaccard statt ±2
3. `score_source_recall()` erweitert zu `score_weighted_source_recall()` — mit optionalem weight-Feld
4. `score_source_diversity()` neu — Shannon-Entropie normalisiert
5. `DEFAULT_WEIGHTS` aktualisiert mit neuen Metriken + Gewichten
6. Golden Dataset YAML kann optionale `weight`-Felder pro `expected_source_files`-Eintrag haben
7. Report (Markdown) zeigt alle 6 Metriken in Tabelle
8. Backward-kompatibel: Godot ohne PDF-Metadaten und ohne `weight`-Felder funktioniert unverändert
9. Alle 226 Unit-Tests bleiben grün
10. Eval mit neuen Metriken: avg_composite sollte diskriminativer sein (höhere Varianz zwischen pass/weak)

## Nicht-Ziele

- Retrieval-Verbesserungen (HyDE, Query Decomposition) — separates Issue
- LLM-as-Reranker — separates Issue
- Small-to-Big Retrieval — separates Issue
- Re-Indexing oder Re-Build — nicht nötig, nur Scorer ändert sich

## Forschungsquellen

- Ragas (RAG-Eval-Standard): https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/
- Ragas Paper: https://arxiv.org/abs/2309.15217
- NDCG@K: https://arxiv.org/abs/2312.10997 (RAG Survey)
- RAG Best Practices: https://arxiv.org/abs/2407.01219
- Seven Failure Points: https://arxiv.org/abs/2401.05856
