# Architecture — Knowledge Hub

## Überblick

```
┌─────────────────────────────────────────┐
│           Knowledge Hub                  │
│                                           │
│  domains/                                 │
│  ├── godot/  ──┐                         │
│  │   ├── sources/    (repomix output)     │
│  │   ├── personal/   (Noahs Wissen)       │
│  │   └── scripts/    (update, search)     │
│  ├── blender/ ──┤  (später)              │
│  └── freecad/  ──┘  (später)             │
│                                           │
│  scripts/                                 │
│  ├── embed_index.py   → ChromaDB         │
│  ├── embed_search.py  ← ChromaDB         │
│  └── hybrid_search.py ← BM25 + ChromaDB → Cross-Encoder │
│                                           │
│  mcp_servers/knowledge_hub/               │
│  └── OpenCode ← MCP-Tools                │
└─────────────────────────────────────────┘
```

## Datenfluss

1. **Quellen (Input):**
   - `domains/<name>/sources/*.md` — repomix-Output (Repo-Wissen)
   - `domains/<name>/personal/*.md` — Markdown-Notizen (persönliches Wissen)

2. **Indexierung:**
   - `scripts/embed_index.py --domain godot`
    - **Repo-Quellen (Godot/Repo-Domains):** `fallback_chunk()` (2000 Tokens / 8000 Zeichen, 400 Tokens Overlap / 1600 Zeichen, erhöht von 200 Tokens/800 Zeichen in Phase 1) → Embedding (MPNet, 768 dims) → ChromaDB Collection `<name>_knowledge`
   - **Personal Notes:** `markdown_section_chunk()` (Splittet an `##`-Headern in per-section Chunks, defensive Skip bei <50 Zeichen, Fallback auf `fallback_chunk()` bei Dateien ohne `##`-Header) → Embedding → ChromaDB
   - **PDF-Repo-Quellen (Phase 2.2, DaVinci):** Chapter-wise **Late Chunking** via `_LateChunkEncoder`: pro PDF-Chapter ein langer BGE-M3-Token-Stream → 512-Token-Fenster mit 128-Token-Overlap → Mean-Pooling pro Fenster. Chunks tragen `chunk_type="late_chunk"`, `page_start`/`page_end` aus Chapter-Grenzen. `precomputed_embeddings` werden als separates Dict (nicht Chunk-Attribut) durch die Pipeline gereicht, um BGE-M3-Long-Context (8192 Token) voll auszunutzen. DaVinci: 2.511 → 12.367 Chunks.
   - **Contextual Retrieval (Phase 3.1b):** Zwei-Phasig: (1) `contextualize_chunks.py` generiert LLM-basierte `context_prefix`-Strings für alle Path-A-Chunks (`chunk_type != "late_chunk"`) und persistiert sie im SQLite-Cache (`chromadb_data/<domain>/context_cache.db`). Resume-fähig via Cache-Lookup. (2) `embed_index.py --contextualize` liest den Cache und nutzt `context_prefix + "\n" + text` als Embedding-Input (D1). BM25 bleibt `text` only. Late-Chunk-Chunks (DaVinci) sind ausgenommen (D2 — haben bereits Chapter-Kontext).
   - **Cloud-Option (Phase 3.1c):** Statt lokalem Gemma 4 12B MLX (69h für 4580 Pfad-A-Chunks) kann `gemma4:cloud` (32.7B, Ollama-Cloud, Zero-Retention) genutzt werden (~3h). Setup: `ollama signin && ollama pull gemma4:cloud && export KH_LLM_MODEL=gemma4:cloud`. KH_OLLAMA_HOST bleibt localhost (lokaler Daemon routet Cloud). Usage-Limit-Handling: HTTP 429 → sofortiger Stopp, Resume via Cache. Account-Wechsel: `ollama signin`, neu starten, Cache bleibt gültig (Cache-Key domain-unabhängig). 3.1c-Ergebnis: +0.0105 avg_composite (NO-GO, < +0.02 Schwelle) — kein produktiver Rollout, Eval-Domains behalten.
   - **Contextual BM25 (Phase 3.2):** BM25-Corpus = context_prefix + " " + text (D1-Aufhebung E18, opt-in via --contextualize-bm25). A/B/C-Eval: +0.0209 avg_composite (GO). godot-008 (Sprachbarriere) gehoben. Default False = D1 gültig.
   - Collection wird komplett neu gebaut (kein inkrementelles Update)

3. **Suche (zweistufig):**
   - `scripts/hybrid_search.py --domain godot --query "..." --mode hybrid`
   - **Stage 1:** BM25 (exakt) + ChromaDB (semantisch) → RRF-Fusion (k=60) → Candidate-Pool
     - BM25-Tokenisierung: Unicode-aware mit CamelCase-Splitting (`CharacterBody3D` → `["character", "body", "3", "d"]`, `GPU` bleibt `["gpu"]`, deutsche Umlaute erhalten). Symmetrisch für Index und Query.
   - **Stage 2:** Cross-Encoder (ms-marco-MiniLM-L-12-v2, konfigurierbar via `KH_RERANKER_MODEL`) → Reranking → Top-10 Ranking

4. **MCP-Server:**
   - `mcp_servers/knowledge_hub/server.py` — stdio MCP-Server
   - Tools: search_knowledge, get_domain_status, update_domain, add_personal_note, list_domains

## Komponenten

| Komponente | Verantwortung | Eingabe | Ausgabe |
|-----------|--------------|---------|---------|
| `embed_index.py` | Index-Bau | Quell-Dateien (.md) | ChromaDB-Collection |
| `embed_search.py` | Semantische Query | Query-String | JSON-Result |
| `hybrid_search.py` | Fusion BM25 + Embeddings → Cross-Encoder-Rerank | Query-String | JSON-Result (geranked) |
| MCP-Server | OpenCode-Integration | MCP-Tool-Calls | JSON-Responses |

## Domain-Autonomie

Jede Domain unter `domains/<name>/` ist ein autarkes Modul:
- Eigenes `domain.md` (Konfiguration)
- Eigene `sources/` (Rohdaten)
- Eigene `personal/` (Wissen)
- Eigene `scripts/` (CLI)
- Eigene ChromaDB-Collection (`<name>_knowledge`)

Neue Domain hinzufügen:
1. `domains/<name>/` mit domain.md + Quellen anlegen
2. `python scripts/embed_index.py --domain <name>` — Index bauen
3. MCP-Server erkennt neue Domain automatisch (scannt `domains/` beim Start)

## Per-Domain Isolation (2026-06-27)

```
chromadb_data/
  godot/
    chroma/                 # eigene DB
    godot_bm25.pkl
  davinci_resolve/
    chroma/
    davinci_resolve_bm25.pkl
```

Model Manager (`scripts/model_manager.py`) ist die einzige Stelle, die
Embedding- und Reranker-Modelle lädt. Lazy-Loading, Per-Domain-Caching,
LRU-Eviction (BM25-Cache hat LRU; `_model_cache` ist aktuell plain dict —
LRU-Migration für Embedder in Phase 2b, siehe B4).

Embedding-Modell-Auswahl (Phase 2a, Decision 2.7):
- Precedence: `KH_EMBEDDING_MODEL` Env-Var > `domain.md` Metadaten >
  `config.DEFAULT_MODEL_NAME` (`all-mpnet-base-v2`).
- Live-Lesung der Env-Var auf jedem Cache-Miss in `get_embedder()`
  (analog `get_reranker()`).
- Aktive Modelle: `all-mpnet-base-v2` (768 dims, 384 Token, English-only)
  als Fallback; `BAAI/bge-m3` (1024 dims, 8192 Token, multilingual, MIT)
  als Phase-2a-Default über Env-Var + domain.md.

Embedding-Device-Auswahl (Phase 3.3a, LIM-011 RESOLVED):
- `KH_EMBEDDING_DEVICE` Env-Var steuert das Compute-Device (Default
  `cpu`, opt-in `mps` auf Apple Silicon).
- `torch` 2.12.0 hat den BGE-M3 + `transformers` 4.57.6 MPS-Deadlock
  behoben, der zuvor `device='cpu'` erzwungen hat (~4.7× Speedup).
- Cache-Key ist `embedder:<model>:<device>` (Runtime-Switch lädt eine
  frische Instanz statt eine falsch-Device Cache-Instanz zurückzugeben).
- Pre-Flight-Mitigation (R1.1): 100-Chunk MPS-Encode vor jedem großen
  Build; bei Hang (>30 s) auf CPU zurückfallen. Integration-Test
  `test_mps_encode_pre_flight` automatisiert den Check.

Parallel LLM-Calls (Phase 3.3a, Contextual Retrieval):
- `KH_LLM_WORKERS` Env-Var (Default `1` = sequenziell, opt-in `>1`
  für Ollama-Cloud Pro Concurrency). CLI-Flag `--workers N` an
  `contextualize_chunks.py` überschreibt die env var.
- Bei `workers > 1` dispatcht `contextualize_chunks()` Cache-Misses an
  einen `ThreadPoolExecutor`. Cache-Lookup bleibt sequenziell (vor
  Pool-Submit); SQLite-Writes werden im Main-Thread über einen
  `threading.Lock` serialisiert.
- `context_cache.open_cache()` setzt `check_same_thread=False` und
  `PRAGMA busy_timeout=5000` für Connection-Sharing über Worker +
  Resilienz gegen residuale Write-Races.
- Ein geteiltes `threading.Event` propagiert HTTP 429 Usage-Limit-
  Abbrüche an alle in-flight Worker (Cache bleibt für Resume intakt).
- `get_llm()` wird vor ThreadPool-Start pre-warm aufgerufen, um eine
  Race im `_model_cache`-Dict zu vermeiden.

Domain-Scoping: `--domains` CLI-Flag auf dem MCP-Server begrenzt sichtbare
Domains. Default (ohne Flag): alle sichtbar (rückwärtskompatibel).

## Vision Retrieval Feature (2026-07-07)

Multimodal-RAG für PDF-Domains mit Screenshots (aktuell: `davinci_resolve`).
Additive Pipeline — bestehende Text-Suche bleibt unverändert, Bild-Pipeline
ist ein zusätzliches Retrieval-Signal.

### Pipeline-Übersicht

```
PDFs (sources/raw/*.pdf)
   │
   ▼ extract_pdf_images.py (PyMuPDF4LLM write_images=True, AGPL build tool)
   │
   ├─ domains/<domain>/images/<source-stem>/<pdf>-<page>-<idx>.png
   └─ chromadb_data/<domain>/image_manifest.json
         │
         ▼ caption_images.py (Gemma 4 Cloud, 3 parallele Worker)
         │
         └─ chromadb_data/<domain>/image_caption_cache.db (SQLite WAL)
               │
               ▼ embed_images.py (SigLIP-2 / jina-clip-v2, MPS)
               │
               ├─ chromadb_data/<domain>/image_embedding_cache.db (SQLite WAL)
               └─ ChromaDB <domain>_images collection (modality=image|caption)
                     │
                     ▼ embed_index.py --embed-images
                     │
                     └─ chromadb_data/<domain>/<domain>_images_bm25.pkl
                           │
                           ▼ hybrid_search.py (4-Listen-RRF)
                           │
                           └─ Top-K gemischt (text + image + caption)
```

### 4-Listen-RRF (Modality-Gap-Berücksichtigung)

```
Stage 1 (parallel):
  text_bm25    → BM25 über Text-Chunks (k=60)
  text_dense   → BGE-M3 ChromaDB (k=60)
  image_bm25   → BM25 über Bild-Captions (k=30, kleiner → stärkere Gewichtung)
  image_dense  → SigLIP-2 Caption-Embeddings (k=30)

Stage 2 (Reranking):
  text_entries   → jina-reranker-v2 Cross-Encoder
  image_entries  → kein Reranking (Modality-Gap: Text-Cross-Encoder
                   würde Bild-Captions falsch scoreran)
  Merge: 2/3 Text + 1/3 Bild (min 1 Bild wenn im RRF-Pool)
```

### Neue Env-Vars

- `KH_MULTIMODAL_MODEL` — Default `google/siglip2-so400m-patch16-512`
  (Apache 2.0, 1152 dims, English-only). Optional: `jinaai/jina-clip-v2`
  (CC-BY-NC-4.0, multilingual, 1024 dims, `trust_remote_code=True`).
- `KH_MULTIMODAL_DEVICE` — Default `cpu`, opt-in `mps` (Apple Silicon).
- `KH_MULTIMODAL_BATCH_SIZE` — Default `32`.
- `KH_VISION_LLM_MODEL` — Default folgt `KH_LLM_MODEL` (`gemma4:cloud`).
- `KH_VISION_LLM_WORKERS` — Default `1`, opt-in `3` für Cloud-Concurrency.

### Neue Skripte

| Skript | Verantwortung | AGPL? |
|--------|---------------|-------|
| `extract_pdf_images.py` | PDF → PNG + Manifest | Ja (PyMuPDF) |
| `caption_images.py` | Bild → Caption (Gemma 4 Cloud) | Nein (MIT) |
| `embed_images.py` | Bild/Caption → ChromaDB images | Nein (MIT) |
| `image_caption_cache.py` | SQLite-Cache für Captions | Nein (MIT) |
| `image_embedding_cache.py` | SQLite-Cache für Embeddings | Nein (MIT) |

### Neue Collections / Indizes

- ChromaDB `<domain>_images` — modality=image|caption, cosine, 1152 dims (SigLIP-2)
- BM25 `<domain>_images_bm25.pkl` — über Bild-Captions
- SQLite `image_caption_cache.db` — WAL, content-hash Key, domain-unabhängig
- SQLite `image_embedding_cache.db` — WAL, base64 float32, domain-unabhängig

## Visual Question Answering (2026-07-07)

VQA erweitert das Vision Retrieval Feature um **Image-Query Search**:
Ein Nutzer lädt ein Bild hoch und stellt eine Frage dazu („was ist das
rechts unten?"). Das OpenCode-LLM kann keine Bilder lesen, aber es
reicht den Bild-Pfad an `search_knowledge(image_path=...)` weiter. Der
Knowledge Hub embeddet das Bild mit SigLIP-2 (gleicher Vektorraum wie
die indexierten Screenshots), findet die ähnlichsten DaVinci-Screenshots
per Cosine-Similarity und gibt deren Captions zurück. Das LLM nutzt die
Captions um zu erklären was auf dem Nutzer-Bild zu sehen ist.

### VQA Pipeline

```
Nutzer-Bild (PNG/JPG, beliebiger Pfad)
   │
   ▼ image_similarity_search() in hybrid_search.py
   │
   ├─ PIL Image.open(path).convert("RGB")
   ├─ Content-Hash (SHA-256) → image_embedding_cache.db Lookup
   │    modality="query_image" (NICHT "image" — das sind indexierte
   │    Screenshots; image_id="query" Placeholder)
   │
   ├─ [Cache Miss] SigLIP-2 image-encode (processor + get_image_features)
   │    → 1152-dim Vektor → L2-Normalize (CLIP convention)
   │    → Cache write (modality="query_image")
   │
   ├─ ChromaDB <domain>_images.query (where modality="image", cosine)
   │    → Top-K image entries nach similarity
   │
   └─ Result-Enrichment: caption, page, source_file aus image-Metadaten
      ( caption ist im image-Eintrag selbst gespeichert, kein separater
        caption-Lookup nötig — embed_images.py schreibt caption in beide
        modality-Entries )
      → sortiert nach similarity_score (1 - cosine_distance, 0..1)
      → modality="image_match", match_type="image_similarity"
```

### search_knowledge image_path Integration

```
search_knowledge(domain, query, image_path=<pfad>)
   │
   ├─ [1] 4-Listen-RRF läuft unverändert (text + image_bm25 + caption)
   │      → top_k text/image/caption Treffer
   │
   ├─ [2] image_similarity_search(domain, image_path, top_k)
   │      → top_k image_match Treffer (similarity_score, caption, page)
   │
   └─ [3] Merge: image_match Treffer werden PREPENDED
          ( additive, bis top_k — kombinierte Liste max 2*top_k )
          → Ranks 1..N neu zugewiesen
          → Return-Dict: image_match_count + results
```

### Backward-Kompatibilität

Ohne `image_path` (Default `None`):

- `image_similarity_search` wird NICHT aufgerufen
- Kein `image_match` in Results
- `image_match_count = 0`
- Verhalten identisch zur Pre-VQA-Signatur

### Modality-Werte in Results

| modality | Quelle | Bedeutung |
|----------|--------|-----------|
| `text` | 4-Listen-RRF (text_bm25 + text_semantic) | Text-Chunk aus Repo/Personal Notes |
| `image` | 4-Listen-RRF (image_bm25) | Screenshot gefunden via Caption-Keyword-Match |
| `caption` | 4-Listen-RRF (image_dense) | Screenshot gefunden via Caption-Semantic-Match |
| `image_match` | VQA: `image_similarity_search` | Screenshot gefunden via Query-Image-Ähnlichkeit (NEU) |

### Neue Env-Vars

Keine — VQA nutzt die bestehenden `KH_MULTIMODAL_MODEL` /
`KH_MULTIMODAL_DEVICE` Env-Vars des Vision Retrieval Features.

### Performance

- 1 SigLIP-2 Image-Embedding pro Query (~0.5s auf MPS, ~3s auf CPU)
- Cache-Hit bei wiederholter Query desselben Bildes (~0ms Embedding)
- ChromaDB cosine query über ~23k image-Entries: ~50ms

### Optional: MiniMax M3 Vision-LLM (deferred)

Die Caption-basierte Antwort (über `image_match` Captions) funktioniert
ohne Vision-LLM. Eine optionale Erweiterung würde das Nutzer-Bild + Top-3
ähnliche Screenshots an einen Vision-LLM (MiniMax M3) senden, der das
Bild direkt versteht statt über Captions zu schließen. Status: deferred
(keine API-Keys, externe Dependency). Siehe
`docs/issues/visual-question-answering/spec.md` Section 5.
