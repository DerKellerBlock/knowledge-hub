# Spec: Vision Retrieval Feature — Echtes Multimodal-Retrieval für PDF-Domains

> **Task-ID:** vision-retrieval-feature
> **Datum:** 2026-07-06
> **Autor:** Noah + Orchestrator
> **Status:** draft (warte auf Noah-Freigabe)
> **Plan:** docs/issues/vision-retrieval-feature/plan.md

## Vision

Der Knowledge Hub ist aktuell text-only — Bilder in PDFs (Screenshots,
Diagramme, UI-Abbildungen) gehen bei der PyMuPDF4LLM-Konvertierung verloren.
Diese Spec definiert echtes **Multimodal-Retrieval** (Architektur A): Bilder
werden aus PDFs extrahiert, mit einem multimodalen Embedding-Modell (jina-
clip-v2) in einen gemeinsamen Vektorraum mit Text embeddet, und bei der
Suche werden Text- und Bild-Ergebnisse gemischt zurückgegeben.

Das Ziel: wenn jemand „wie sieht der Color-Wheel-Dialog aus" fragt, findet
der Hub den Screenshot des Dialogs — nicht nur den Text-Chunk der ihn
beschreibt.

## Architektur

```
BUILD (einmalig, offline):

PDF → PyMuPDF4LLM (write_images=True)
    │
    ├── Text-Chunks (bestehend, BGE-M3, 1024-dim)
    │       → ChromaDB: <domain>_knowledge (bestehend)
    │       → BM25 text (bestehend)
    │
    ├── Bild-Dateien (PNGs, neu)
    │       → domains/<domain>/images/<source>/<page>-<idx>.png
    │
    ├── Context-Aware Captions (neu)
    │       │ Text ±200 chars um Bild + Vision-LLM Beschreibung
    │       │ → Caption-Text
    │       ↓
    │   jina-clip-v2 text-embeddet (1024-dim)
    │       → ChromaDB: <domain>_images (NEU)
    │       → BM25 captions (NEU)
    │
    └── Bild-Embeddings (neu)
            jina-clip-v2 image-embeddet (1024-dim)
            → ChromaDB: <domain>_images (gleiche Collection, modality=image)


SEARCH (runtime, lokal):

Text-Query
    │
    ├── BGE-M3 text-embed (1024-dim, bestehend)
    │       → ChromaDB: <domain>_knowledge (text)
    │       → BM25 text (bestehend)
    │
    └── jina-clip-v2 text-embed (1024-dim, NEU)
            → ChromaDB: <domain>_images (image vectors)
            → BM25 captions (NEU)

    ┌────────────────┬────────────────┬──────────────────┬────────────────┐
    │ text-vector    │ text-bm25      │ image-vector      │ image-bm25      │
    │ (bestehend)    │ (bestehend)    │ (NEU: query vs    │ (NEU: query vs  │
    │                │               │  Bild-Vektoren)   │  Caption-Tokens)│
    └────────┬───────┴────────┬──────┴─────────┬────────┴────────┬────────┘
             │                │                │                 │
             └────────┬───────┴────────┬───────┘                 │
                      ↓                ↓                         │
               RRF-Fusion (4 Listen) ←───────────────────────────┘
                      │
                      ↓
               jina-reranker-v2 (nur Text-Chunks, bestehend)
                      │
                      ↓
               Top-10 Ergebnisse (Text + Bild gemischt)
                      │
                      ↓
               MCP search_knowledge Antwort
               (text + image_path + caption + page + modality)
```

## Komponenten

### 1. Bild-Extraktion (Build-Skript, neu)

**Datei:** `scripts/extract_pdf_images.py`

- PyMuPDF4LLM mit `write_images=True` (PNGs speichern in
  `domains/<domain>/images/<source-file>/<page>-<idx>.png`)
- Pro Bild: Seitennummer, Position, umgebender Text (±200 chars aus
  PDF-Markdown, context-aware nach TowardsDataScience-Best-Practice)
- Quality-Check: Vision-LLM bewertet „Good" vs „Poor" (logos, illegible
  aussortieren, nach TowardsDataScience-Pattern)
- Output: JSON mit `{image_path, page, position, context_before, context_after,
  quality}` pro Bild
- **Best-Practice Rule 1:** Dokumentstruktur erhalten (parent_id, Position,
  Kontext)

### 2. Bild-Captioning (Build-Skript, neu)

**Datei:** `scripts/caption_images.py`

- Pro Bild (nur „Good"-qualifizierte): Vision-LLM generiert Beschreibung
- Prompt: „Beschreibe dieses Bild aus einem <Domain>-Handbuch. Kontext:
  [context_before + context_after]. Was zeigt es? Welche UI-Elemente sind
  sichtbar?"
- Vision-LLM: Gemma 3 via Ollama (`gemma3:4b`, lokal, ~4 GB) oder
  `gemma4:cloud` (Ollama Cloud, wie Contextual-Retrieval)
- Parallel: `KH_LLM_WORKERS=3` für Cloud-Captioning (ThreadPoolExecutor,
  cancel_event bei 429, SQLite-Cache für Resume)
- Caption = context_before + Vision-LLM-Beschreibung + context_after
  (context-aware nach TowardsDataScience)
- Cache: `chromadb_data/<domain>/image_caption_cache.db` (SQLite, wie
  context_cache, content-hash als Key für Resume bei Abbruch)
- **Best-Practice aus TowardsDataScience:** context-aware image summaries
  statt isolierte Captions

### 3. Multimodal Embedding (Build-Skript, neu)

**Datei:** `scripts/embed_images.py`

Zwei Modelle wählbar via `KH_MULTIMODAL_MODEL` env var (analog zum
`KH_RERANKER_MODEL`-Pattern beim Reranker):

| Modell | Lizenz | Sprachen | Dims | Input | Default? |
|---|---|---|---|---|---|
| `google/siglip2-so400m-patch16-512` | Apache 2.0 | English-only | 1152 | 512×512 | **Ja** |
| `jinaai/jina-clip-v2` | CC-BY-NC-4.0 | 89 Sprachen (multilingual) | 1024 | 512×512 | Optional |

- Via `transformers` (NICHT Ollama, Issue #5304 offen)
- `from transformers import AutoProcessor, AutoModel`
- `model = AutoModel.from_pretrained(KH_MULTIMODAL_MODEL, trust_remote_code=True)`
- `processor = AutoProcessor.from_pretrained(KH_MULTIMODAL_MODEL)`
  (zwingend — hardcoded normalization = falsche results, Spheron-Best-
  Practice)
- **SigLIP-2:** 1152-dim, mean [0.5, 0.5, 0.5], std [0.5, 0.5, 0.5]
- **jina-clip-v2:** 1024-dim (Matryoshka truncatable), mean [0.485, 0.456,
  0.406], std [0.229, 0.224, 0.225]
- Caption-Text-Embeddings: gleicher Vektorraum, gleicher Encoder (joint)
- Device: `KH_MULTIMODAL_DEVICE` env var (default `cpu`, opt-in `mps`)
  - Cache-Key: `multimodal:<model>:<device>` (Runtime-Switch lädt frische
    Instanz, wie BGE-M3)
  - Pre-Flight-Mitigation: 10-Bild MPS-Encode vor Build; bei Hang >30s → CPU
- Batch-Size: `KH_MULTIMODAL_BATCH_SIZE` env var (default 32, MPS RAM-limitiert)
  - Offline-Indexing: 64-128 (Spheron empfiehlt 256-512, aber M1 Max RAM
    limitiert)
- Warm-Up: Dummy-Request vor Build-Loop (2-5s cold start, Spheron)
- Output: ChromaDB-Collection `<domain>_images`
  - Metadaten: `source_file`, `image_path`, `page_start/page_end`,
    `modality` (image/caption), `caption`, `quality`
- **Best-Practice Rule 2:** Joint-Encoder, gemeinsamer Vektorraum
- **Best-Practice Rule 3:** Bild-Pfad in Metadaten (für späteres Abrufen)
- **Lizenz-Doku:** SigLIP-2 → Apache-2.0-Sektion in THIRD_PARTY_LICENSES.md;
  jina-clip-v2 → CC-BY-NC-4.0-Sektion (analog jina-reranker-v2)

### 4. Bild-BM25 (Index, neu)

- BM25-Index über Bild-Captions (für lexikalische Bild-Suche)
- Tokenisierung der Captions (bestehender Unicode-aware Tokenizer)
- Speicher: `<domain>_images_bm25.pkl` (wie text BM25)
- `use_context_prefix` analog zu Contextual BM25 — Caption-Kontext im
  BM25-Corpus

### 5. Hybrid-Search-Erweiterung (bestehend, erweitert)

**Datei:** `scripts/hybrid_search.py` erweitert

- **4 Listen statt 2:** text-vector, text-bm25, image-vector, image-bm25
- **RRF-Fusion über 4 Listen** (statt 2)
  - Modality-Gap-Berücksichtigung: image-vector und image-bm25 haben andere
    Score-Skalen als text (CLIP modality gap, Spheron-Best-Practice)
  - Lösung: separate RRF-k-Konstanten pro Modality (z.B. k_text=60,
    k_image=30) oder Normalisierung vor RRF
- **jina-Cross-Encoder** rerankt nur Text-Chunks (bestehend, Bilder können
  nicht als Query-Chunk-Paare bewertet werden)
- **Bild-Ergebnisse:** nach RRF-Rang, kein Cross-Encoder
- **Output:** Top-10 gemischt (Text + Bilder), mit `modality`-Feld in
  Metadaten, `image_path` für Bilder

### 6. MCP-Server-Erweiterung (bestehend, erweitert)

**Datei:** `mcp_servers/knowledge_hub/server.py` erweitert

- `search_knowledge` gibt optional `image_path` + `caption` in Ergebnissen
  zurück
- Neue Metadaten-Felder in Ergebnis-JSON: `modality` (text/image),
  `image_path`, `caption`
- `get_domain_status` erweitert: Image-Count pro Domain, Bild-Index vorhanden?
- `update_domain` könnte Bild-Extraktion + Embedding auslösen (optional,
  später)

### 7. Model Manager Erweiterung (bestehend, erweitert)

**Datei:** `scripts/model_manager.py` erweitert

- Neue Funktion `get_multimodal_embedder(domain)` — lädt jina-clip-v2
  (analog `get_embedder()` für BGE-M3)
- Cache-Key: `multimodal:<model>:<device>`
- LRU-Eviction (wie embedder, B4-Migration angewendet)
- `KH_MULTIMODAL_MODEL` env var (default `google/siglip2-so400m-patch16-512`,
  optional `jinaai/jina-clip-v2` für multilingual)
- `KH_MULTIMODAL_DEVICE` env var (default `cpu`, opt-in `mps`)
- `KH_MULTIMODAL_BATCH_SIZE` env var (default 32)
- Live-Lesung der Env-Vars auf jedem Cache-Miss (wie BGE-M3)

## Performance-Strategien (M1 Max)

### MPS GPU Acceleration
- `KH_MULTIMODAL_DEVICE=mps` (wie BGE-M3, LIM-011 resolved)
- Pre-Flight-Test: 10-Bild MPS-Encode; bei Hang >30s → CPU-Fallback
- Geschätzt bei 512×512: ~1.500-4.000 pairs/hr (M1 Max MPS, ~5-10× langsamer
  als A100 bei 4× mehr pixel throughput als 224×224)
- Bei ~8.000 DaVinci-Bildern: ~2-5h (MPS), 5-10h (CPU)

### Batch-Size Optimierung
- `KH_MULTIMODAL_BATCH_SIZE=64` (start, MPS RAM-limitiert)
- Steigern auf 128 bei genug RAM, bei OOM zurückfallen
- Offline-Indexing: 64-128 empfohlen (Spheron: 256-512 für Server-GPUs)

### Parallel Captioning (Vision-LLM)
- `KH_LLM_WORKERS=3` + Ollama Cloud (wie Contextual-Retrieval)
- Bild-Captioning ist der langsamste Schritt (~2.5s/Bild)
- Bei 8.000 Bildern + 3 Workern: ~2h effektive Cloud-Zeit
- Resume via SQLite-Cache bei Usage-Limit (cancel_event, wie contextualize)

### ONNX-Export (optional, testen)
- `optimum-cli export onnx --model jinaai/jina-clip-v2`
- Spheron: 20-40% speedup auf Ampere/Hopper
- Auf MPS möglicherweise weniger Vorteil — testen, ggf. fallback auf PyTorch

### Content-Hash Caching
- Embedding-Cache für Bilder (content-hash als Key, wie context_cache)
- Bei Re-Builds werden unveränderte Bilder übersprungen (AugmentCode Rule 8)
- SQLite: `chromadb_data/<domain>/image_embedding_cache.db`

### Warm-Up
- Dummy-Request vor Build-Loop (2-5s cold start, Spheron)
- 10-Bild-Encode als Pre-Flight (gleichzeitig MPS-Check)

## Build-Zeit Schätzung (DaVinci, ~8.000 Bilder, 512×512 Input)

| Phase | M1 Max MPS | Mit Cloud (Captioning) |
|---|---|---|
| Bild-Extraktion (PyMuPDF4LLM) | 10-30 min | 10-30 min |
| Bild-Embedding (SigLIP-2/jina-clip-v2, 512×512) | 2-5h | 2-5h |
| Bild-Captioning (Gemma 4, 3 Worker Cloud) | ~5.5h lokal | **~2h (Cloud)** |
| Caption-Text-Embedding | 15-30 min | 15-30 min |
| ChromaDB + BM25 | 15-30 min | 15-30 min |
| **Total** | ~10-14h | **~6-9h** |

Hinweis: 512×512 Input ist 4× mehr pixel throughput als 224×224. MPS ist
der Flaschenhals beim Bild-Embedding. Vision-LLM-Captioning wird durch
Cloud-Parallelisierung (3 Worker) beschleunigt.

## Konfiguration (neue Env-Vars)

- `KH_MULTIMODAL_MODEL` — default `google/siglip2-so400m-patch16-512`
  (Apache 2.0, kommerziell sicher), optional `jinaai/jina-clip-v2`
  (CC-BY-NC-4.0, multilingual)
- `KH_MULTIMODAL_DEVICE` — default `cpu`, opt-in `mps`
- `KH_MULTIMODAL_BATCH_SIZE` — default 32 (MPS RAM-limitiert)
- `KH_VISION_LLM_MODEL` — default `gemma4:cloud` (Ollama Cloud, parallel)
- `KH_VISION_LLM_WORKERS` — default 1, opt-in 3 für Cloud (parallel)

## Neue Dateien

| Datei | Zweck |
|---|---|
| `scripts/extract_pdf_images.py` | Bild-Extraktion aus PDFs (AGPL, wie parse_pdf_to_markdown.py) |
| `scripts/caption_images.py` | Bild-Captioning mit Vision-LLM |
| `scripts/embed_images.py` | Multimodal-Embedding (jina-clip-v2) |
| `scripts/image_caption_cache.py` | SQLite-Cache für Caption-Resume |
| `scripts/image_embedding_cache.py` | SQLite-Cache für Embedding-Resume |

## Erweiterte Dateien

| Datei | Änderung |
|---|---|
| `scripts/model_manager.py` | `get_multimodal_embedder()`, neue Env-Vars |
| `scripts/hybrid_search.py` | 4-Listen-RRF, modality-gap-Berücksichtigung |
| `scripts/embed_index.py` | `--embed-images` Flag für Bild-Indexing |
| `mcp_servers/knowledge_hub/server.py` | `image_path`, `caption`, `modality` in Ergebnissen |
| `mcp_servers/knowledge_hub/config.py` | Multimodal-Config |
| `scripts/workspace_check.sh` | Image-Collection-Check (optional) |
| `requirements.txt` | `pillow` (PIL für Bild-Verarbeitung) |
| `requirements-pdf.txt` | bereits pymupdf (für write_images=True) |
| `THIRD_PARTY_LICENSES.md` | SigLIP-2 (Apache 2.0) + jina-clip-v2 (CC-BY-NC-4.0) |

## Neue Ordner

| Ordner | Zweck |
|---|---|
| `domains/<domain>/images/` | Extrahierte PNGs pro Domain |
| `chromadb_data/<domain>/<domain>_images/` | Bild-ChromaDB-Collection |

## domain.md Erweiterung

```markdown
## Metadaten
- Embedding-Model: BAAI/bge-m3 (1024 dims, text)
- Multimodal-Model: jinaai/jina-clip-v2 (1024 dims, text+image)
- Vision-LLM: gemma3:4b (lokal) oder gemma4:cloud (Captioning)
- Collection: <name>_knowledge (text), <name>_images (images)
- Source-Types: pdf, repo
- Image-Extraction: enabled (write_images=True)
- Letztes Update: YYYY-MM-DD
```

## Akzeptanzkriterien

- [ ] `scripts/extract_pdf_images.py` extrahiert Bilder aus PDFs mit Kontext
- [ ] `scripts/caption_images.py` generiert context-aware Captions via
  Vision-LLM
- [ ] `scripts/embed_images.py` embeddet Bilder + Captions mit jina-clip-v2
- [ ] `model_manager.py` hat `get_multimodal_embedder()` mit MPS-Support
- [ ] `hybrid_search.py` macht 4-Listen-RRF-Fusion (text+image, vector+bm25)
- [ ] MCP `search_knowledge` gibt `image_path` + `caption` + `modality` zurück
- [ ] MPS Pre-Flight-Test funktioniert (10-Bild-Encode, Hang-Detection)
- [ ] Build-Zeit < 10h für DaVinci (8.000 Bilder, MPS + Cloud-Captioning)
- [ ] SQLite-Cache für Caption-Resume bei Usage-Limit
- [ ] Quality-Check filtert logos/illegible Bilder
- [ ] AutoProcessor wird verwendet (keine hardcodierte normalization)
- [ ] Modality-Gap in RRF-Fusion berücksichtigt
- [ ] `requirements.txt` enthält `pillow`
- [ ] `THIRD_PARTY_LICENSES.md` enthält jina-clip-v2 (Apache 2.0)
- [ ] Tests: Unit-Tests für extract/caption/embed, Integration-Test für
  end-to-end Pipeline
- [ ] Doku: `docs/ai/architecture.md` + `docs/ai/best-practices.md` + 
  `docs/ai/how-retrieval-works.md` aktualisiert

## Nicht-Ziele

- **KEINE Bild-Query** (Bild als Query hochladen) — folgt in separater
  Iteration, falls gewünscht
- **KEINE OCR** — Bilder werden als Bilder embeddet, nicht via OCR zu Text
  konvertiert
- **KEINE Bild-Generierung** — der Hub retrieves Bilder, erzeugt keine
- **KEINE Video/Audio** — nur Bilder (PDF-Screenshots)
- **KEINE Migration** bestehender Indizes — neue Bild-Indizes werden
  parallel zu Text-Indizes gebaut, bestehende Text-Suche bleibt unverändert
- **KEINE Änderung an BGE-M3 / jina-reranker / Contextual Retrieval** —
  Text-Pipeline bleibt unverändert, Bild-Pipeline ist additiv

## Risiken

1. **jina-clip-v2 MPS Hang** — möglich (wie BGE-M3 vor LIM-011-fix).
   Mitigation: Pre-Flight-Test, CPU-Fallback.
2. **8.000 Bilder Speicherplatz** — PNGs können ~500 MB-2 GB pro Domain
   werden. ChromaDB-Collection wächst um ~100-200 MB.
3. **Usage-Limit bei Cloud-Captioning** — 8.000 Bilder × ~2.5s = ~5.5h
   Cloud-Zeit. Mehrere Account-Wechsel möglich (wie Contextual-Retrieval).
4. **Modality-Gap Degradation** — CLIP image-text accuracy 10-20% unter
   benchmark bei domain-shift (Spheron). DaVinci-Screenshots sind domain-
   shift vs. CLIP training data. Mitigation: RRF-Gewichtung anpassen,
   evaluiert via Golden Dataset.
5. **Ollama keine multimodalen Embeddings** — jina-clip-v2 muss via
   transformers laufen, nicht Ollama. Zweites großes Modell im RAM
   (~3.5 GB zusätzlich zu BGE-M3 + jina-reranker).
6. **PyMuPDF4LLM AGPL Process Boundary** — `extract_pdf_images.py` braucht
   AGPL-Header (wie `parse_pdf_to_markdown.py`), wird via subprocess
   aufgerufen.

## Entscheidungen (Noah, 2026-07-06)

1. **Domains:** Nur `davinci_resolve` (PDFs mit Screenshots). Godot hat keine
   Bilder in den repomix-Packed-Files.
2. **Vision-LLM:** Gemma 4 via Ollama Cloud mit 3 parallelen Workern
  (`KH_LLM_WORKERS=3`), wie Contextual-Retrieval. Lokal als Fallback.
3. **search_knowledge:** Bestehende Funktion erweitern (backward-kompatibel,
   `modality`-Feld in Metadaten, `image_path` + `caption` optional).
4. **Multimodal-Modell:** **Option 3 — Beide unterstützen:**
   - **Default:** `google/siglip2-so400m-patch16-512` (Apache 2.0,
     kommerziell sicher, English-only, 512×512)
   - **Optional:** `jinaai/jina-clip-v2` (CC-BY-NC-4.0, multilingual, 512×512)
   - **Env-Var:** `KH_MULTIMODAL_MODEL` (Default: siglip2, wie
     `KH_RERANKER_MODEL`-Pattern beim Reranker)
   - **Lizenz-Doku:** in `THIRD_PARTY_LICENSES.md` analog zum Reranker-Pattern
     (Default = kommerziell sicher, Optional = CC-BY-NC-4.0 akzeptiert für
     persönlichen Hub)
   - **Begründung:** Knowledge Hub ist MIT-lizenziert (Open Source). Default
     bleibt kommerziell sicher (Apache 2.0). Optional für multilingual
     (CC-BY-NC-4.0, analog zum bereits akzeptierten jina-reranker-v2).
5. **Bild-Auflösung:** 512×512 (beide Modelle unterstützen 512×512). Kein
   Downsampling — volle Qualität für UI-Screenshot-Erkennung.

## Referenzen

- Context-Dateien: `docs/issues/vision-retrieval-feature/context/` (4 Quellen)
  - `research-multimodal-rag.md` (TowardsDataScience, Context-Aware Captions)
  - `research-augmentcode-best-practices.md` (12 Production Best-Practices)
  - `research-spheron-benchmarks.md` (GPU Benchmarks, M1 Max Schätzung,
    Modality Gap)
  - `research-ollama-multimodal-limitation.md` (Ollama Limitation,
    transformers-Pfad)
