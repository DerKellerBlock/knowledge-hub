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
- **LIM-002:** `section_path` und `chunk_type` fehlen bei DaVinci-Resolve-Fallback-Chunks (Repo-Quellen) und bei Preamble-Chunks aus `markdown_section_chunk()`. Sektions-Chunks aus `markdown_section_chunk()` haben jetzt `chunk_type="personal_section"` und `name=<Sektionsüberschrift>`, aber `section_path=None`. Godot-Repo-Chunks haben diese Felder via rst-godot-Parser. Agenten dürfen sich nicht auf `section_path` als zuverlässiges Feld verlassen.
- **LIM-003:** `text`-Feld in Suchergebnissen wird auf 5000 Zeichen trunciert (`hybrid_search.py:127`, `embed_search.py:69`). DaVinci-Fallback-Chunks können bis ~8000 Zeichen groß sein. Der Orchestrator-Prompt instruiert Agenten, Truncation zu erkennen und nicht zu halluzinieren.
- **LIM-004:** `expected_page_ranges` in `quality/golden/davinci_resolve.yaml` enthalten ±2 Seitentoleranz (Chunking-Variance), nicht die exakten Seitenzahlen. Die PMA-Bewertung (`score_page_metadata_accuracy`) prüft, ob die tatsächlichen `page_start`/`page_end`-Werte innerhalb der erwarteten Range ±2 liegen.
- **LIM-005:** `solution_summary` in `real_world_sources` ist aktuell `null` für alle 14 Golden-Dataset-Fragen (TODO-Platzhalter). Manuelle Kuratierung durch Noah ausstehend. Die Evaluationsmethodik (Source Coverage, Solution Alignment, Gap Detection) funktioniert bereits mit null-Summaries (URLs + has_solution reichen für Ebene 1 und 3), aber Solution Alignment (Ebene 2) benötigt die Summaries für den vollständigen Vergleich.
- **LIM-006:** `line_end` in `markdown_section_chunk()` und `fallback_chunk()` kann 1 Zeile über den tatsächlichen Inhalt hinausgehen (konsistente Konvention, aber semantisch ungenau). Risiko niedrig, da Orchestrator den `text`-Inhalt zeigt, nicht Zeilennummern.

## Bekannte Retrieval-Lücken

- **godot-007 (3D character controller):** Composite 0.7136 (pass, aber niedrigste SR=0.6667). `tips.md`/CharacterBody3D Stair Stepping rankt nicht in Top-10 der breiten godot-007-Frage. Lücke stammt aus Commit f5be7e0 (Gap-Closing-Iteration), nicht aus der Fix-Iteration. Mögliche Folge-Lösungen: (a) `tips.md`-Stair-Stepping-Sektion mit konkreten Code-Snippets erweitern, (b) Golden Dataset `expected_source_files` anpassen, (c) Hybrid-Search Stage-1 top-K erhöhen.

