# Plan: Vision Retrieval Feature — Echtes Multimodal-Retrieval

> **Task-ID:** vision-retrieval-feature
> **Datum:** 2026-07-06
> **Spec:** docs/issues/vision-retrieval-feature/spec.md
> **Status:** draft (warte auf Noah-Freigabe nach Spec-Review)

## Überblick

Implementierung von echtem Multimodal-Retrieval (Architektur A) für PDF-
Domains. Bilder aus DaVinci-PDFs extrahieren, context-aware Captions via
Gemma 4 Cloud generieren, mit SigLIP-2 (Default) oder jina-clip-v2 (Optional)
embedden, 4-Listen-RRF-Fusion in hybrid_search.py, MCP-Server erweitern.

Build-Zeit Schätzung (DaVinci, ~8.000 Bilder, 512×512, MPS + Cloud):
~6-9h.

Der Plan ist in 9 Tasks gegliedert. Tasks 1-5 sind Build-Pipeline
(Skripte), Tasks 6-8 sind Runtime (Search + MCP), Task 9 ist Doku + Test.

## Tasks

### Task 1: Dependencies + Model Manager

- [ ] `requirements.txt`: `pillow` (PIL für Bild-Verarbeitung) ergänzen
- [ ] `requirements-pdf.txt`: prüfen ob pymupdf4llm `write_images=True`
  schon unterstützt (sollte schon da)
- [ ] `scripts/model_manager.py`: `get_multimodal_embedder(domain)` Funktion
  hinzufügen
  - Lädt SigLIP-2 oder jina-clip-v2 via `transformers` (NICHT Ollama)
  - `AutoProcessor.from_pretrained(KH_MULTIMODAL_MODEL)`
  - `AutoModel.from_pretrained(KH_MULTIMODAL_MODEL, trust_remote_code=True)`
  - Cache-Key: `multimodal:<model>:<device>`
  - Live-Lesung von `KH_MULTIMODAL_MODEL`, `KH_MULTIMODAL_DEVICE`,
    `KH_MULTIMODAL_BATCH_SIZE` auf jedem Cache-Miss (wie BGE-M3)
  - LRU-Eviction (B4-Migration angewendet)
  - `trust_remote_code=True` für jina-clip-v2 (Custom-Code via auto_map,
    analog jina-reranker; in security.md als akzeptiert dokumentiert)
- [ ] `mcp_servers/knowledge_hub/config.py`: neue Env-Vars ergänzen
- [ ] `THIRD_PARTY_LICENSES.md`:
  - Apache-2.0-Sektion: `google/siglip2-so400m-patch16-512`
  - CC-BY-NC-4.0-Sektion: `jinaai/jina-clip-v2` (analog jina-reranker-v2)
- **Verify:** `py_compile scripts/model_manager.py`, `get_multimodal_embedder`
  lädt Modell (Pre-Flight Test mit 1 Bild)

### Task 2: Bild-Extraktion (`extract_pdf_images.py`)

- [ ] `scripts/extract_pdf_images.py` (AGPL-Header, wie parse_pdf_to_markdown.py)
  - PyMuPDF4LLM mit `write_images=True`
  - Bilder speichern nach `domains/<domain>/images/<source-file>/<page>-<idx>.png`
  - Pro Bild: Seitennummer, Position, umgebender Text (±200 chars aus
    PDF-Markdown, context-aware)
  - Quality-Check: Vision-LLM bewertet „Good" vs „Poor" (logos, illegible
    aussortieren)
  - Output: JSON `chromadb_data/<domain>/image_manifest.json` mit
    `{image_path, page, position, context_before, context_after, quality}`
  - CLI: `--domain <name>`, `--quality-check` (optional, default on)
- [ ] `scripts/workspace_check.sh`: Image-Ordner-Check (optional, nicht
  blockierend)
- **Verify:** `python scripts/extract_pdf_images.py --domain davinci_resolve`
  extrahiert Bilder, JSON existiert, mind. 100 Bilder (Quality-Good)

### Task 3: Bild-Captioning (`caption_images.py`)

- [ ] `scripts/caption_images.py`
  - Liest `image_manifest.json`, pro „Good"-Bild: Vision-LLM generiert
    Beschreibung
  - Prompt: „Beschreibe dieses Bild aus einem DaVinci-Resolve-Handbuch.
    Kontext: [context_before + context_after]. Was zeigt es? Welche
    UI-Elemente sind sichtbar?"
  - Vision-LLM: `gemma4:cloud` via Ollama Cloud (KH_VISION_LLM_WORKERS=3),
    ThreadPoolExecutor, cancel_event bei 429
  - Caption = context_before + Vision-LLM-Beschreibung + context_after
    (context-aware, TowardsDataScience Best-Practice)
  - SQLite-Cache: `chromadb_data/<domain>/image_caption_cache.db`
    (content-hash als Key, Resume bei Abbruch, wie context_cache)
  - CLI: `--domain <name>`, `--workers N`, `--limit N` (für Testing)
- [ ] `scripts/image_caption_cache.py`: SQLite-Cache-Modul
  (analog context_cache.py: WAL-Mode, INSERT OR REPLACE, busy_timeout=5000,
  check_same_thread=False, domain-unabhängiger Key)
- **Verify:** `KH_LLM_MODEL=gemma4:cloud KH_OLLAMA_HOST=http://localhost:11434
  KH_LLM_WORKERS=3 python scripts/caption_images.py --domain davinci_resolve
  --limit 10` generiert 10 Captions, Cache hat 10 Einträge, context_prefix
  != None

### Task 4: Multimodal Embedding (`embed_images.py`)

- [ ] `scripts/embed_images.py`
  - Liest `image_manifest.json` + Caption-Cache
  - Pro „Good"-Bild: SigLIP-2/jina-clip-v2 image-embed (512×512, 1152/1024-dim)
  - Pro Caption: SigLIP-2/jina-clip-v2 text-embed (gleicher Vektorraum)
  - Device: `KH_MULTIMODAL_DEVICE` (default cpu, opt-in mps)
  - Batch-Size: `KH_MULTIMODAL_BATCH_SIZE` (default 32)
  - Warm-Up: 10-Bild-Encode als Pre-Flight (MPS-Check, bei Hang >30s → CPU)
  - Content-Hash Caching: `chromadb_data/<domain>/image_embedding_cache.db`
    (SQLite, unveränderte Bilder überspringen bei Re-Build)
  - Output: ChromaDB-Collection `<domain>_images`
    - Metadaten: source_file, image_path, page_start/page_end, modality
      (image/caption), caption, quality
  - CLI: `--domain <name>`, `--device mps`, `--batch-size 64`
- [ ] `scripts/image_embedding_cache.py`: SQLite-Cache-Modul
  (analog image_caption_cache.py)
- [ ] `scripts/embed_index.py`: `--embed-images` Flag ergänzen
  (ruft embed_images.py als subprocess auf oder integriert es)
- **Verify:** `KH_MULTIMODAL_DEVICE=mps python scripts/embed_images.py
  --domain davinci_resolve --limit 10` embeddet 10 Bilder, ChromaDB
  Collection davinci_resolve_images hat mind. 10 Einträge (5 image + 5
  caption), device=mps:0

### Task 5: Bild-BM25 + Domain.md-Erweiterung

- [ ] `scripts/embed_index.py`: Bild-BM25-Index-Erstellung ergänzen
  - BM25-Index über Bild-Captions (Tokenisierung mit bestehendem
    Unicode-aware Tokenizer)
  - Speicher: `<domain>_images_bm25.pkl`
  - `use_context_prefix` analog Contextual BM25 (Caption-Kontext im Corpus)
- [ ] `domains/davinci_resolve/domain.md`: Metadaten erweitern
  - `Multimodal-Model: google/siglip2-so400m-patch16-512 (1152 dims, text+image)`
  - `Vision-LLM: gemma4:cloud (Captioning)`
  - `Collection: davinci_resolve_images (images)`
  - `Image-Extraction: enabled (write_images=True)`
- **Verify:** Bild-BM25 existiert, domain.md hat neue Metadaten

### Task 6: Hybrid-Search-Erweiterung (4-Listen-RRF)

- [ ] `scripts/hybrid_search.py`: 4-Listen-RRF-Fusion
  - text-vector (bestehend, BGE-M3)
  - text-bm25 (bestehend)
  - image-vector (NEU: query → jina-clip-v2/SigLIP-2 text-embed → Suche in
    `<domain>_images` wo modality=image)
  - image-bm25 (NEU: query → BM25-Suche in Bild-Captions)
  - RRF-Fusion über 4 Listen (k-Konstanten pro Modality: k_text=60,
    k_image=30, Modality-Gap-Berücksichtigung)
  - jina-reranker: nur Text-Chunks (bestehend), Bilder nach RRF-Rang
  - Output: Top-10 gemischt, `modality`-Feld in Metadaten
- [ ] Modality-Gap-Berücksichtigung:
  - CLIP image/text embeddings clustern in verschiedenen Regionen
    (Spheron-Best-Practice)
  - Lösung: separate RRF-k-Konstanten oder Score-Normalisierung vor RRF
- [ ] Tests: Unit-Test für 4-Listen-RRF, Integration-Test für end-to-end
  Search mit Bildern
- **Verify:** `python scripts/hybrid_search.py --domain davinci_resolve
  --query "color wheel" --mode hybrid` gibt Top-10 mit mind. 1 Bild-Ergebnis

### Task 7: MCP-Server-Erweiterung

- [ ] `mcp_servers/knowledge_hub/server.py`: `search_knowledge` erweitern
  - Neue Metadaten-Felder in Ergebnis-JSON: `modality` (text/image),
    `image_path`, `caption`
  - Backward-kompatibel: falls keine Bild-Collection existiert, verhält
    sich search_knowledge wie bisher (nur Text)
  - `get_domain_status`: Image-Count pro Domain, Bild-Index vorhanden?
- [ ] Tests: MCP-Integration-Test für multimodal search
- **Verify:** MCP-Server quicktest zeigt modality/image_path in Ergebnissen

### Task 8: Doku-Aktualisierung

- [ ] `docs/ai/architecture.md`: Multimodal-Pipeline ergänzen
  - Bild-Extraktion, Captioning, Embedding, 4-Listen-RRF
  - Neue Collections, neue BM25-Indizes
- [ ] `docs/ai/best-practices.md`: neue Env-Vars ergänzen
  - KH_MULTIMODAL_MODEL, KH_MULTIMODAL_DEVICE, KH_MULTIMODAL_BATCH_SIZE
  - KH_VISION_LLM_MODEL, KH_VISION_LLM_WORKERS
  - SigLIP-2 vs jina-clip-v2 Lizenz-Hinweis
- [ ] `docs/ai/how-retrieval-works.md`: Multimodal-Sektion ergänzen
  - Neue Komponente „5. SigLIP-2/jina-clip-v2 (Multimodal-Embedding)"
  - 4-Listen-RRF-Diagramm erweitern
  - Context-Aware Captions erklären
- [ ] `docs/ai/security.md`: trust_remote_code für jina-clip-v2 (analog
  jina-reranker)
- [ ] `docs/ai/known-issues.md`: Modality-Gap als bekannte Limitierung
- **Verify:** Alle Doku-Dateien referenzieren SigLIP-2 + jina-clip-v2

### Task 9: Vollständiger Build + Eval + Retrospektive

- [ ] **Vollständiger Build (DaVinci):**
  ```bash
  # 1. Bilder extrahieren
  python scripts/extract_pdf_images.py --domain davinci_resolve
  # 2. Captions generieren (Cloud, parallel)
  KH_LLM_MODEL=gemma4:cloud KH_OLLAMA_HOST=http://localhost:11434 \
    KH_LLM_WORKERS=3 python scripts/caption_images.py --domain davinci_resolve
  # 3. Bilder + Captions embedden (MPS)
  KH_MULTIMODAL_DEVICE=mps KH_MULTIMODAL_MODEL=google/siglip2-so400m-patch16-512 \
    python scripts/embed_images.py --domain davinci_resolve
  # 4. BM25 + ChromaDB finalisieren
  python scripts/embed_index.py --domain davinci_resolve --embed-images
  ```
- [ ] **Eval:** Golden Dataset erweitern mit Bild-Fragen (mindestens 3
  neue Fragen die Bild-Antworten erwarten, z.B. „wie sieht der Color-Wheel
  aus", „Planar Tracker UI", „Fusion Page Layout")
- [ ] `scripts/quality/run_evaluation.py --domain davinci_resolve`:
  Bild-Treffer in Ergebnissen verifizieren
- [ ] **Validierung:** py_compile, pytest -m unit, pytest -m integration,
  workspace_check.sh
- [ ] `docs/issues/vision-retrieval-feature/retrospective.md` schreiben
- [ ] `docs/issues/vision-retrieval-feature/explanation.md` schreiben
- [ ] `docs/ai/open-work.md`: Task als done markieren
- [ ] Git commit
- **Verify:** Build läuft ohne Crash, Eval zeigt Bild-Treffer, alle Tests
  grün, Doku aktuell

## Validierung

- [ ] `py_compile scripts/*.py` — Syntax OK
- [ ] `pytest -m unit -q` — alle Unit-Tests grün
- [ ] `pytest -m integration -q` — alle Integration-Tests grün
- [ ] `./scripts/workspace_check.sh` — All checks passed
- [ ] `KH_MULTIMODAL_DEVICE=mps` Pre-Flight funktioniert (10-Bild-Encode)
- [ ] 4-Listen-RRF gibt gemischte Text+Bild Ergebnisse
- [ ] MCP-Server gibt `image_path` + `caption` in Ergebnissen
- [ ] `THIRD_PARTY_LICENSES.md` hat SigLIP-2 + jina-clip-v2

## Open Questions für Noah

(keine — alle 5 Entscheidungen getroffen: DaVinci only, Gemma 4 Cloud 3
Worker, search_knowledge erweitern, Option 3 SigLIP-2 Default + jina-clip-v2
Optional, 512×512 Input)
