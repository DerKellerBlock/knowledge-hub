# Known Issues — Knowledge Hub

## Behobene Probleme

- **KI-001:** Phase 1+2 abgeschlossen (2026-06-09) — Alle Kern-Komponenten implementiert
- **KI-002:** Godot-Skills ins Hub migriert — Skills sind Single Source of Truth
- **TD-001:** ChromaDB-Integration getestet — 265 MB Index, 18.222 Chunks, Cosine-Metrik
- **KI-003:** Retrieval 2.0 implementiert (2026-06-10) — BM25 ersetzt ripgrep, Cross-Encoder-Reranking, Plugin-basiertes strukturiertes Parsing

## Technische Schulden

- **TD-002 (resolved 2026-06-29):** Quality Evaluation Platform Phase 1+2 implementiert — Golden Dataset für `godot` und `davinci_resolve`, Bewertungsrubrik, CLI-Skripte (`run_evaluation.py`, `add_question.py`, `validate_dataset.py`, `generate_report.py`), E2E Quality Tests. Siehe `docs/superpowers/specs/2026-06-29-knowledge-hub-quality-evaluation-platform-design.md`.

## Einschränkungen

- **LIM-001:** MCP-Server nur stdio (kein HTTP/SSE) — akzeptabel für persönlichen Hub
- **LIM-002:** `section_path` und `chunk_type` fehlen bei DaVinci-Resolve-Chunks (Fallback-Chunking, kein domain-spezifischer Parser). Godot-Chunks haben diese Felder via rst-godot-Parser. Agenten dürfen sich nicht auf `section_path` als zuverlässiges Feld verlassen.
- **LIM-003:** `text`-Feld in Suchergebnissen wird auf 5000 Zeichen trunciert (`hybrid_search.py:127`, `embed_search.py:69`). DaVinci-Fallback-Chunks können bis ~8000 Zeichen groß sein. Der Orchestrator-Prompt instruiert Agenten, Truncation zu erkennen und nicht zu halluzinieren.
- **LIM-004:** `expected_page_ranges` in `quality/golden/davinci_resolve.yaml` enthalten ±2 Seitentoleranz (Chunking-Variance), nicht die exakten Seitenzahlen. Die PMA-Bewertung (`score_page_metadata_accuracy`) prüft, ob die tatsächlichen `page_start`/`page_end`-Werte innerhalb der erwarteten Range ±2 liegen.

