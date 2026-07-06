# jina-Reranker Test Retrospective

## Goal

Test `jinaai/jina-reranker-v2-base-multilingual` als multilingualen Stage-2-Reranker
mit BGE-M3-Embeddings und entscheiden, ob jina dauerhaft übernommen wird. Damit
sollen LIM-007 (jina ungetestet) und LIM-008 (BGE-M3 + ms-marco Übergangskonfiguration)
geschlossen werden.

## What went well

- **MPS-Pre-Check funktionierte.** jina-Download + Laden + `predict()`-Probe
  verlief ohne Überraschungen, `trust_remote_code=True` griff wie dokumentiert.
- **godot-008 multilingual gain bestätigt.** Deutsche `faq.md` rückt trotz
  englischer Query auf Rang 1 — der systematische Sprachbarriere-Fix wirkt jetzt
  auch im Stage-2-Reranking, nicht nur im Embedding.
- **Keine Regression.** godot avg_composite 0.8594 (identisch), davinci
  0.7304 (+0.0058), PMA davinci +0.0286 netto. Alle 16 Fragen bleiben pass.
- **Score-Skala kompatibel wie recherchiert.** jina sigmoid (0–1) vs ms-marco
  logits (−10..+10) — `hybrid_search.py` und `scorer.py` benötigen keine
  Anpassung, da das Ranking rein rangbasiert (kein Threshold) ist.

## What was surprising or difficult

- **Composite maskiert den Reranker-Effekt für godot fast vollständig.**
  SR/TKR/Evidence sind alle am Deck, Composite bleibt 0.8594. Der jina-Gewinn
  zeigt sich nur über die Reihenfolge (faq.md auf Rang 1) und die Snippets —
  Metriken auf Komponenten-Ebene wären aufschlussreicher.
- **`generate_report.py` überschrieb datumsbasierte Reports ohne `_jina`-Suffix.**
  Die Ausgabe nach `godot_2026-07-01.json` kollidierte mit der msmarco-Datei vom
  gleichen Tag; explizite Suffix-Übergabe war nötig, um beide Läufe trennbar zu
  halten.

## Lessons learned

- **MPS-Pre-Check ist unverzichtbar.** Vor jedem Modellwechsel Download + Load +
  `predict()`-Probe laufen lassen — vermeidet teure Fehlschläge mitten im
  Evaluation-Lauf.
- **Rank-basierte Metriken sind reranker-agnostisch** — das ist Stärke (keine
  Code-Anpassung nötig) und Schwäche (Composite reagiert kaum auf
  Reranker-Verbesserungen). Für künftige Reranker-Vergleiche sollten
  Reihenfolge-/Snippet-basierte Vergleiche ergänzt werden.

## Follow-up candidates

1. **Phase 2b: Late Chunking (2.2) + Golden Dataset 20–30 (2.4)**
2. **jina Sparse / BGE-M3 Sparse** — Sparse-Modalitäten zusätzlich zum Dense-Embedding
3. **Contextual Retrieval + RAGAS** — Phase 3

## References

- LIM-007, LIM-008 in `docs/ai/known-issues.md` (beide resolved)
- Spec: `docs/superpowers/specs/2026-06-30-improvement-roadmap-phase2-embedding-upgrade-design.md`
- Reports: `quality/reports/godot_jina_2026-07-01.json`, `quality/reports/davinci_resolve_jina_2026-07-01.json`
- Baselines: `quality/baselines/godot-latest.json`, `quality/baselines/davinci_resolve-latest.json`
- CI: `.github/workflows/quality-gate.yml`