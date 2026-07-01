# Known Issues — Knowledge Hub

## Behobene Probleme

- **KI-001:** Phase 1+2 abgeschlossen (2026-06-09) — Alle Kern-Komponenten implementiert
- **KI-002:** Godot-Skills ins Hub migriert — Skills sind Single Source of Truth
- **TD-001:** ChromaDB-Integration getestet — 265 MB Index, 18.222 Chunks, Cosine-Metrik
- **KI-003:** Retrieval 2.0 implementiert (2026-06-10) — BM25 ersetzt ripgrep, Cross-Encoder-Reranking, Plugin-basiertes strukturiertes Parsing
- **KI-004:** godot-007 (3D character controller) Retrieval-Lücke geschlossen (2026-06-30) — `tips.md`/CharacterBody3D Stair Stepping-Sektion um GDScript-Code-Snippet erweitert (Godot-4-Stable-APIs + PR-#114447-APIs klar gekennzeichnet). Composite 0.7136 → 0.8594, SR 0.6667 → 1.0, `tips.md` Top-2 statt Rank 32. Cross-Encoder-Score -8.53 → +0.71. Behebt BM25-Token-Overlap (Query-Keywords velocity/gravity/jump/move_and_slide jetzt als Tokens vorhanden) und Cross-Encoder-Kontext (Sektion liest sich jetzt als vollständiger Character-Controller).
- **KI-005:** LIM-005 resolved (2026-06-30) — Alle 29 `solution_summary`-Felder in `real_world_sources` kuratiert (15 godot + 14 davinci_resolve, Commit 5a07b4b). Solution Alignment (Ebene 2) der Real-World-Evaluation ist jetzt vollständig evaluierbar.
- **KI-006:** LIM-007 resolved (2026-07-01) — jina-reranker-v2-base-multilingual tested with BGE-M3 embeddings. godot avg_composite 0.8594 (identisch), davinci 0.7304 (+0.0058), keine Regression. godot-008 multilingual gain: deutsche faq.md auf Rang 1 trotz englischer Query. Adopted via `KH_RERANKER_MODEL` env var; CI quality-gate default seit 2026-07-01. CC-BY-NC-4.0 akzeptiert für persönlichen nicht-kommerziellen Hub.
- **KI-007:** LIM-008 resolved (2026-07-01) — BGE-M3 multilingual embeddings + jina multilingual reranker = konsistente Multilingual-Pipeline. CI quality-gate nutzt jina default. Lokal via `KH_RERANKER_MODEL` env var aktivierbar (Shell-Profile/`.env` setup siehe `docs/ai/best-practices.md`). Ohne Env-Var fällt System auf ms-marco zurück (Übergangskonfiguration bleibt funktionsfähig, ist aber nicht mehr der empfohlene Pfad).

## Technische Schulden

- **TD-002 (resolved 2026-06-29):** Quality Evaluation Platform Phase 1+2 implementiert — Golden Dataset für `godot` und `davinci_resolve`, Bewertungsrubrik, CLI-Skripte (`run_evaluation.py`, `add_question.py`, `validate_dataset.py`, `generate_report.py`), E2E Quality Tests. Siehe `docs/superpowers/specs/2026-06-29-knowledge-hub-quality-evaluation-platform-design.md`.

## Einschränkungen

- **LIM-001:** MCP-Server nur stdio (kein HTTP/SSE) — akzeptabel für persönlichen Hub
- **LIM-002:** `section_path` und `chunk_type` fehlen bei DaVinci-Resolve-Fallback-Chunks (Repo-Quellen) und bei Preamble-Chunks aus `markdown_section_chunk()`. Sektions-Chunks aus `markdown_section_chunk()` haben jetzt `chunk_type="personal_section"` und `name=<Sektionsüberschrift>`, aber `section_path=None`. Godot-Repo-Chunks haben diese Felder via rst-godot-Parser. Agenten dürfen sich nicht auf `section_path` als zuverlässiges Feld verlassen.
- **LIM-003:** `text`-Feld in Suchergebnissen wird auf 5000 Zeichen trunciert (`hybrid_search.py:127`, `embed_search.py:69`). DaVinci-Fallback-Chunks können bis ~8000 Zeichen groß sein. Der Orchestrator-Prompt instruiert Agenten, Truncation zu erkennen und nicht zu halluzinieren.
- **LIM-004:** `expected_page_ranges` in `quality/golden/davinci_resolve.yaml` enthalten ±2 Seitentoleranz (Chunking-Variance), nicht die exakten Seitenzahlen. Die PMA-Bewertung (`score_page_metadata_accuracy`) prüft, ob die tatsächlichen `page_start`/`page_end`-Werte innerhalb der erwarteten Range ±2 liegen.
- **LIM-005 (resolved 2026-06-30):** `solution_summary` in `real_world_sources` war `null` für alle 14 Golden-Dataset-Fragen (TODO-Platzhalter). Kuratiert in Commit 5a07b4b: 15 godot-Summaries + 14 davinci_resolve-Summaries (29 total, alle ausgefüllt). Solution Alignment (Ebene 2) der Real-World-Evaluation ist jetzt vollständig evaluierbar.
- **LIM-006:** `line_end` in `markdown_section_chunk()` und `fallback_chunk()` kann 1 Zeile über den tatsächlichen Inhalt hinausgehen (konsistente Konvention, aber semantisch ungenau). Risiko niedrig, da Orchestrator den `text`-Inhalt zeigt, nicht Zeilennummern.
- **LIM-007 (resolved 2026-07-01):** `jinaai/jina-reranker-v2-base-multilingual` getestet mit BGE-M3-Embeddings. godot avg_composite 0.8594 (identisch), davinci 0.7304 (+0.0058), keine Regression. godot-008 multilingual gain (deutsche faq.md auf Rang 1). Adopted via `KH_RERANKER_MODEL` env var; CI quality-gate default. Siehe KI-006.
- **LIM-008 (resolved 2026-07-01):** BGE-M3 multilingual embeddings + jina multilingual reranker = konsistente Multilingual-Pipeline. CI quality-gate nutzt jina default. Lokal via `KH_RERANKER_MODEL` env var aktivierbar. Ohne Env-Var fällt System auf ms-marco zurück. Siehe KI-007.
- **LIM-009 (B10):** BGE-M3 long-context verändert das effektive Chunking-Verhalten. BGE-M3 `max_seq_length=8192` vs all-mpnet 384. DaVinci-Fallback-Chunks bis ~8000 Zeichen (~2000 Token) werden jetzt VOLLSTÄNDIG verarbeitet (vorher auf 384 Token trunciert). Das ist ein Konfounder in der Phase-2a-Re-Evaluation: Embedding-Modell und effektive Chunk-Länge ändern sich gleichzeitig. Eine isolierte Messung des Chunking-Effekts wäre nur mit einem 384-Token-BGE-M3-Setup möglich, das nicht geplant ist.

## Bekannte Retrieval-Lücken

- **godot-008 (3D model visibility, weak):** Composite 0.6406, SR 0.5 (`godot-docs-reference-packed.md` gefunden, `faq.md` fehlt Top-10). Wurzelursache ist die Sprachbarriere: die englische Query („Why is my 3D model not visible") matcht semantisch schlecht gegen die deutsche `faq.md`-Sektion, da `all-mpnet-base-v2` English-only ist. Phase-1-Content-Maßnahmen (neue FAQ-Sektion) können das nicht beheben. Eine deutsche Variante `godot-008-de` testet `faq.md` direkt ohne Sprachbarriere. Die echte Lösung ist (b) BGE-M3 multilingual in Phase 2. Weitere Optionen: (a) FAQ-Visibility-Abschnitt mit englischen Suchankern verstärken, (c) Frage spezifischer formulieren.

- **godot-009/011/012/017/019 (Phase 2.4 weak, composite 0.6406):** Fünf neue weak-Fragen aus der Phase-2.4-Golden-Dataset-Erweiterung (Animation, UI, Navigation, Performance, Custom Resources). Alle testen Themen ohne dedizierte `personal/`-Notizen, die Multi-Page-Synthese über `godot-docs-reference-packed.md` und `godot-docs-3d-packed.md` erfordern. BM25-Token-Overlap ist niedrig, weil die Themen breit gestreut sind. Diese Fragen sind die Baseline für Phase 2.2 Late Chunking Vergleich — Verbesserung wird erwartet, wenn Late Chunking Cross-Section-Kontext in DaVinci-PDFs erhält (nur DaVinci betroffen, Godot-weak-Fragen sind nur Referenz).

- **DaVinci Phase-1-Baseline-Verlust:** DaVinci avg_composite 0.7218 / PMA 0.1714 ist die erste Messung nach Phase 1 (Chunk-Overlap 200→400, +283 Chunks). Keine Pre-Phase-1-Baseline vorhanden (Backups entfernt). PMA 0.1714 ist niedrig (±2 Seitentoleranz, PDF-Chunking-Varianz) — ob Phase 1 die PMA verschlechtert oder verbessert hat, ist nicht ermittelbar. Phase 2 sollte eine neue DaVinci-Baseline etablieren und den Chunk-Overlap-Effekt auf PMA isoliert messen.

