# Phase 3.1 Contextual Retrieval — Design Spec

> **Status:** Draft | **Datum:** 2026-07-02 | **Autor:** Orchestrator
>
> Abgeleitet aus: Phase 3 Roadmap (`2026-06-30-improvement-roadmap-phase3-advanced-rag-design.md` Maßnahme 3.1), Gemma 4 12B MLX Recherche, Blind-Spot-Review (GO MIT HINWEISEN).
> Aktualisiert: Entscheidung 3.1 (Qwen3-14B → Gemma 4 12B MLX).

## 1. Zusammenfassung

Contextual Retrieval (Anthropic, Sept 2024): LLM-generierter 50–100 Token Kontext-Prefix pro Chunk, der den Chunk im Gesamtdokument verortet. Anthropic berichtet 35 % Fehlerraten-Reduktion (Embeddings allein), 49 % (+BM25), 67 % (+Reranking). Phase 3.1 integriert dies in die Knowledge Hub Build-Pipeline mit **Gemma 4 12B MLX** als lokalem LLM. Kontext wird als separates `context_prefix`-Feld gespeichert (Hybrid-Nutzung: Embedding sieht Kontext, BM25 + Reranker nicht). Late-Chunking (DaVinci) wird ausgenommen — nur Godot und Personal Notes werden kontextualisiert.

## 2. Hintergrund

- Chunks verlieren Dokument-Kontext beim Chunking.
- Godot-RST-Chunk `void rotate_y(angle: float)` weiß nicht, dass er zu `Node3D` im Tutorial „3D Character Controller" gehört.
- Anthropic Contextual Retrieval: LLM generiert Kontext-Prefix pro Chunk, der den Chunk im Gesamtdokument situiert.
- Original-Spec nannte Qwen3-14B — aktualisiert auf **Gemma 4 12B MLX** (Juni 2026, 256K Kontext, Apache 2.0, MLX-nativ).

## 3. Recherche-Grundlage

### 3.1 Gemma 4 12B

- Released Juni 2026, 12B Unified
- Apache 2.0 Lizenz (kommerziell nutzbar)
- 256K Token Kontext (vs. Qwen3-14B 32K) — ganze Godot-Dokumente passen in einen Prompt
- 140+ Sprachen, Deutsch abgedeckt
- MLX-Variante: `mlx-community/gemma-4-12B-it-4bit` (6,74 GB)
- MLX-LM direkt (nicht Ollama) für Batch-Use-Case

### 3.2 Contextual Retrieval (Anthropic)

- Quelle: https://www.anthropic.com/news/contextual-retrieval
- 35 % Fehlerraten-Reduktion (Embeddings allein), 49 % (+BM25), 67 % (+Reranking)
- Prompt-Template: `<document>{{WHOLE_DOCUMENT}}</document> Here is the chunk: <chunk>{{CHUNK}}</chunk> Please give a short succinct context…`
- Output: 50–100 Token Kontext
- Prompt Caching: Dokument-Prefix einmal prefilled, wiederverwendet

### 3.3 Bestehender Hub-Stand

- Pipeline: Sources → Chunking → Embedding → ChromaDB (kein Kontext-Schritt)
- Godot: RST-Parser + Personal Notes (~24.600 Chunks)
- DaVinci: Late Chunking + Personal Notes (~12.400 Chunks)
- BGE-M3 MPS-Deadlock (LIM-011): Embedding auf CPU
- jina-Reranker als CI-Default

## 4. Entscheidungen

| ID | Entscheidung | Begründung |
|----|-------------|-----------|
| D1 (OQ-1) | Separates `context_prefix`-Feld (Hybrid): Embedding = `context_prefix + "\n" + text`; BM25 = nur `text`; Cross-Encoder = nur `text`; MCP = `text` clean + `context_prefix` als Metadaten | Anthropic-Embedding-Benefit ohne BM25/Reranker-Verfälschung |
| D2 (B1) | Late-Chunking (DaVinci) AUSGENOMMEN — nur Pfad A (`chunk_type != "late_chunk"`) kontextualisiert | DaVinci hat bereits Chapter-Kontext; eliminiert Offset-Problem; 25h → 17h |
| D3 (W7) | Sub-Phasen 3.1a / 3.1b / 3.1c | Zu groß für eine Iteration |
| D4 (W3) | Small-Scale-Eval PFLICHT vor Voll-Batch (Abbruch bei Delta < +0,02) | Anthropic-Zahlen unverifiziert für lokales 12B |
| D5 (W4) | A/B-Test-Flag `--contextualize` / `--no-contextualize` | Isolierte Messung, LIM-009-Konfounder |
| D6 (W6) | SQLite `context_cache.db` statt JSON | Atomare Transactions, Skalierung |
| D7 (B3) | `KH_EMBEDDING_DEVICE` nicht implementiert, BGE-M3 hardcoded CPU | Korrigiert falsche Annahme |
| D8 (B4) | Dependency-Konflikt-Check ist Blocker-Bedingung für 3.1a | `mlx-lm` `transformers>=5.7.0` kann Stack gefährden |
| D9 (W1) | LLM: Gemma 4 12B (`mlx-community/gemma-4-12B-it-4bit`, 6,74 GB, Apache 2.0) | 256K Kontext, MLX-nativ, aktueller als Qwen3 |
| D10 (W2) | Prompt-Caching: `make_prompt_cache()` + `generate(prompt_cache=...)` | Korrekte mlx-lm API |

## 5. Architektur

```
Sources → Chunking → [Contextualize (LLM)] → Embedding → ChromaDB
                          ↑
                    gemma-4-12b-mlx
                    + Prompt-Caching
```

**Zwei Pfade:**

- **Pfad A (Godot/Repo, Personal Notes):** Kontext NACH Chunking, VOR `_encode_robust()`. Ganzes Quelldokument als LLM-Input.
- **Pfad B (DaVinci/Late-Chunk):** AUSGENOMMEN (D2). Late-Chunking hat bereits Chapter-Kontext.

**Kontext-Speicherung (D1):**

- `Chunk.context_prefix: str | None = None` (neues Feld)
- Embedding-Input: `context_prefix + "\n" + text`
- BM25-Index: nur `text` (unverändert)
- Cross-Encoder: nur `text` (unverändert)
- MCP-Ausgabe: `text` (clean) + `context_prefix` als Metadaten-Feld
- ChromaDB: `context_prefix` als Metadatum (`from_chromadb_metadata` None-tolerant für Backward-Compat)

## 6. Sub-Phasen

### Phase 3.1a — LLM-Infrastruktur (KEIN Rebuild)

- `model_manager.get_llm()` mit `KH_LLM_MODEL` / `KH_LLM_BACKEND` Env-Vars
- `Chunk.context_prefix`-Feld in `parser_base.py`
- Dependency-Kompatibilitätstest (B4): `mlx-lm` + `sentence-transformers` + BGE-M3 + jina
- Mock-LLM-Tests (`FakeLLM.generate()`)
- MCP-Server: `context_prefix` als Metadaten-Feld
- Doku: `best-practices.md`, `security.md`
- **Freigabekriterium:** B4 geklärt, Mock-Tests grün, `context_prefix`-Feld existiert

### Phase 3.1b — Kontext-Generierung + Small-Scale-Eval (PFLICHT)

- `scripts/contextualize_chunks.py`: Prompt-Template, Prompt-Caching
- SQLite `context_cache.db`
- Resume-Atomizität (Cache-Write vor Embedding-Write)
- `llama-cpp-python` Fallback implementieren
- Small-Scale-Eval: 100–500 Godot Chunks mit/ohne Kontext, A/B gegen Golden Dataset
- **Abbruchkriterium:** falls Composite-Delta < +0,02 → 3.1c nicht starten
- Integration-Test `@skipif(not mlx_available)`
- **Freigabekriterium:** Small-Scale-Eval positiv, Cache funktioniert, Resume getestet

### Phase 3.1c — Rebuild & Evaluation (nur Godot)

- `--contextualize` / `--no-contextualize` Flag in `embed_index.py`
- Vollständiger Rebuild nur Godot
- A/B-Vergleich: `no-contextualize`-Baseline vs. `contextualize`-Index
- Doku-Update: `changelog`, `known-issues`, `domain-model`
- **Freigabekriterium:** keine Regressionen, Composite-Delta bestätigt Small-Scale-Eval

## 7. Prompt-Template

Anthropic-Template (angepasst für Gemma 4):

```text
<document>
{document_text}
</document>
Here is the chunk we want to situate within the whole document:
<chunk>
{chunk_content}
</chunk>
Please give a short succinct context to situate this chunk within the overall document for the purposes of improving search retrieval of the chunk. Answer only with the succinct context and nothing else.
```

Output: 50–100 Token, gestripped, in `context_prefix` gespeichert.

## 8. Caching & Resume

- SQLite `context_cache.db` pro Domain (gitignored)
- Schema: `(chunk_id_hash TEXT PK, model TEXT, chunk_text_hash TEXT, context TEXT, created_at TEXT)`
- Cache-Key: `sha256(chunk_id + model_name + chunk_text_hash)`
- Resume: nur Cache-Miss Chunks ans LLM, dann vollständiger ChromaDB-Rebuild
- Atomizität: Cache-Write vor Embedding-Write

## 9. Durchsatz-Schätzung

| Metrik | Wert |
|--------|------|
| Godot Pfad-A-Chunks | ~15.000–18.000 |
| Output pro Chunk | ~100 Token |
| MLX Gemma 4 12B Q4 | ~20–40 tokens/s auf Apple Silicon |
| Geschätzte Dauer (Worst-Case) | 18–22 Stunden |
| Mit Prompt-Caching | Prefill nur ~3 Godot-Quelldateien (statt 18.000×) |
| Small-Scale-Eval (500 Chunks) | ~42 Min LLM + Rebuild |

## 10. Risiken

| Prio | Risiko | Mitigation |
|------|--------|-----------|
| HÖCHSTE | B4 `transformers`-Konflikt | Vorab-Test, Subprozess-Grenze bei Bedarf |
| HOCH | 17–22h Batch für null Gewinn | Small-Scale-Eval PFLICHT, Abbruch bei Delta < +0,02 |
| MITTEL | Gemma-Lizenz/Terms | `security.md`, `trust_remote_code` prüfen |
| MITTEL | Cache-Korruption | SQLite-Transactions, Write-vor-Embedding |
| NIEDRIG | godot-009/012/017 bleiben weak | Nicht als Erfolgskriterium |

## 11. Betroffene Dateien

**Neu:**
- `scripts/contextualize_chunks.py`
- `tests/unit/test_contextualize_chunks.py`
- `tests/integration/test_contextualize_build.py`
- `scripts/context_cache.db` (gitignored)
- `requirements-llm.txt` (falls B4-Konflikt)

**Geändert (Code):**
- `scripts/model_manager.py` — `get_llm()`
- `scripts/embed_index.py` — `--contextualize` Flag, Kontext-Prefix vor Embedding
- `scripts/parser_base.py` — `Chunk.context_prefix` Feld
- `scripts/hybrid_search.py` — `context_prefix` als Metadaten
- `scripts/bm25_search.py` — BM25 ignoriert `context_prefix`
- `mcp_servers/knowledge_hub/server.py` — `context_prefix` in Tool-Responses
- `mcp_servers/knowledge_hub/config.py` — `KH_LLM_MODEL`, `KH_LLM_BACKEND`
- `requirements.txt` — `mlx-lm` (oder `requirements-llm.txt`)

**Geändert (Doku):**
- `docs/ai/architecture.md`
- `docs/ai/best-practices.md`
- `docs/ai/domain-model.md`
- `docs/ai/known-issues.md`
- `docs/ai/security.md`
- `docs/ai/decisions.md`
- `docs/ai/changelog.md`
- `THIRD_PARTY_LICENSES.md`

## 12. Phase-Exit-Kriterien

- [ ] `get_llm()` lädt Gemma 4 12B MLX lazy, cached per `KH_LLM_MODEL`
- [ ] `context_prefix`-Feld existiert, Embedding nutzt es, BM25/Reranker nicht
- [ ] `contextualize_chunks.py` generiert 50–100 Token Kontext, mit Prompt-Caching
- [ ] `context_cache.db` persistiert, Resume funktioniert
- [ ] Small-Scale-Eval zeigt positiven Composite-Delta (>+0,02)
- [ ] `--contextualize` Flag funktioniert
- [ ] Vollständiger Godot-Rebuild erfolgreich (Backup → Rebuild → Verify)
- [ ] Re-Evaluation: keine Regressionen, Composite-Delta bestätigt
- [ ] `pytest -m unit/integration/quality` grün
- [ ] Doku aktualisiert

## 13. Hinweise aus Blind-Spot-Review (N1–N6)

- **N1:** Pfad-A = alle `chunk_type != "late_chunk"` Chunks (domänenübergreifend)
- **N2:** Subprozess-IPC bei B4-Konflikt spezifizieren (analog PyMuPDF4LLM)
- **N3:** mlx-lm Prompt-Caching-API vorab verifizieren
- **N4:** BGE-M3-Voraussetzung für Contextual Retrieval dokumentieren
- **N5:** `from_chromadb_metadata` None-tolerant für `context_prefix`
- **N6:** Durchsatz-Schätzung 18–22h (Worst-Case)

## 14. Referenzen

- Anthropic Contextual Retrieval: https://www.anthropic.com/news/contextual-retrieval
- Gemma 4: https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/
- Ollama Gemma 4 MLX: https://ollama.com/library/gemma4
- MLX-LM: https://github.com/ml-explore/mlx-lm
- Phase 3 Roadmap: `docs/superpowers/specs/2026-06-30-improvement-roadmap-phase3-advanced-rag-design.md`
- Phase 2 Spec: `docs/superpowers/specs/2026-06-30-improvement-roadmap-phase2-embedding-upgrade-design.md`
- AGPL Process Boundary: `docs/decisions/2026-06-27-agpl-process-boundary.md`
