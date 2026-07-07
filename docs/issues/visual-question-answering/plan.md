# Plan: Visual Question Answering via MCP

**Task-ID:** visual-question-answering
**Datum:** 2026-07-07
**Spec:** docs/issues/visual-question-answering/spec.md

## Tasks

### Task 1: `image_similarity_search()` in `hybrid_search.py`
- Neue Funktion: Bild laden (PIL) → SigLIP-2 embedden → ChromaDB query
- Query ChromaDB `<domain>_images` (where modality="image"), cosine similarity
- Top-K Results anreichern mit caption/page/source_file Metadaten
- Content-Hash Cache via `image_embedding_cache.py`
- Graceful Error: Bild fehlt / PIL Error / SigLIP-2 nicht verfügbar / Collection fehlt
- **Verify:** Unit-Test mit Mock-ChromaDB (returns similar images), graceful error bei fehlendem Bild

### Task 2: `search_knowledge` MCP-Tool erweitern
- `tools.py`: `search_knowledge()` um `image_path: str | None = None` Parameter erweitern
- Bei `image_path` gesetzt: `image_similarity_search()` zusätzlich zur 4-Listen-RRF
- Results mischen: text/image/caption Treffer + `image_match` Treffer
- `image_match` Treffer: `modality: "image_match"`, `similarity_score`, `caption`, `page`, `source_file`
- Backward-kompatibel: ohne `image_path` unverändert
- **Verify:** Aufruf mit `image_path=None` → identisch mit alt; mit `image_path` → image_match in results

### Task 3: MCP-Tool Schema in `server.py` aktualisieren
- `inputSchema` für `search_knowledge` um `image_path` Property erweitern
- Description: "Optional: path to an image file for visual similarity search against indexed screenshots"
- **Verify:** MCP-Server startet, Tool-Liste zeigt `image_path` als optionalen Parameter

### Task 4: Orchestrator-Prompt aktualisieren
- `.opencode/agents/orchestrator-knowledge.md` (oder entsprechende Datei):
  - Instruktion: "Wenn Nutzer Bild hochlädt + Frage → image_path an search_knowledge weitergeben"
  - Beispiel-Prompt: "Was ist das rechts unten? [Image]" → `search_knowledge(domain, "Scope panel UI", image_path="/path/to/upload.jpg")`
- **Verify:** Prompt-Datei enthält VQA-Instruktion

### Task 5: Unit-Tests
- `tests/unit/test_image_similarity.py`:
  - Test `image_similarity_search()` mit Mock-ChromaDB
  - Test graceful error (Bild fehlt, PIL Error, Collection fehlt)
  - Test cache hit (content-hash bereits in `image_embedding_cache.db`)
  - Test `search_knowledge` mit `image_path` (image_match in results)
  - Test `search_knowledge` ohne `image_path` (backward-compat, kein image_match)
- **Verify:** `pytest -m unit -q` → alle grün

### Task 6: Integration-Test (optional, manuell)
- Echter Test: DaVinci-Screenshot hochladen → ähnliche Screenshots finden
- Test-Bild: `domains/davinci_resolve/images/davinci-resolve-20.3-reference-manual/DaVinci_Resolve_20.3_Reference_Manual.pdf-3084-0.png` (Color Wheels)
- Query: `search_knowledge("davinci_resolve", "Color Wheels", image_path="<pfad>")` → sollte dieses Bild (oder sehr ähnliche) finden
- **Verify:** Top-1 image_match hat similarity > 0.9 (es ist das gleiche Bild)

### Task 7: Optional — MiniMax M3 Vision-LLM Integration
- Neuer MCP-Tool `analyze_image(image_path, question, domain)`:
  1. `image_similarity_search()` → Top-3 ähnliche DaVinci-Screenshots
  2. Vision-LLM (MiniMax M3) bekommt: Nutzer-Bild + Top-3 Screenshots + Frage
  3. Vision-LLM vergleicht und antwortet
- Env-Var: `KH_VISION_QA_MODEL=minimax/m3` (default off)
- **Verify:** Optional — nur wenn MiniMax M3 API verfügbar

### Task 8: Doku + Retrospektive
- `architecture.md`: VQA Pipeline Sektion
- `best-practices.md`: `image_path` Parameter Usage
- `known-issues.md`: VQA Limitations (nur DaVinci, keine OCR, Caption-basiert)
- `retrospective.md` + `explanation.md`
- `open-work.md` aktualisieren
- **Verify:** Doku vollständig, `workspace_check.sh` OK

## Reihenfolge

```
Task 1 (image_similarity_search) ──┐
                                     ├── Task 2 (search_knowledge) ── Task 3 (server.py)
                                     │                                     │
                                     └── Task 5 (tests)                    Task 4 (prompt)
                                                                           │
                                                                           └── Task 6 (integration test)
                                                                                 │
                                                                                 └── Task 7 (MiniMax, optional)
                                                                                       │
                                                                                       └── Task 8 (doku)
```

## Validierung

```bash
.venv/bin/python -m py_compile scripts/*.py mcp_servers/knowledge_hub/*.py
.venv/bin/pytest -m unit -q
./scripts/workspace_check.sh
```

## Risiko

- **Niedrig:** Alle Änderungen sind additiv (neue Funktion + optionaler Parameter)
- **Backward-kompatibel:** Ohne `image_path` → unverändertes Verhalten
- **Dependencies:** PIL + SigLIP-2 + transformers bereits installiert
- **Performance:** 1 SigLIP-2 Embedding pro Query (~0.5s auf MPS, ~3s auf CPU)
