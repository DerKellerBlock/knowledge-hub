# Best Practices — Knowledge Hub

## Shell-Skripte

- Jedes Skript beginnt mit `#!/usr/bin/env bash` und `set -euo pipefail`
- Farben via ANSI-Escape-Codes: `GREEN`, `YELLOW`, `RED`, `CYAN`, `BOLD`, `NC`
- Hilfsfunktionen: `log_info()`, `log_warn()`, `log_error()`
- Hilfe via `show_help()` oder `--help`/`-h` Flag
- Pfade relativ zum Repository-Root: `REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"`
- Variablen in Strings immer mit `"${VAR}"` quoten (nicht nackt)
- Arrays mit `"${ARR[@]}"` expandieren
- Kein `eval`, kein `curl | bash`, keine ungeprüften externen Inputs in Shell-Commands

## Python-Skripte

- Python 3.11+
- `argparse` (CLI) oder `click` (komplexere CLIs)
- Docstrings für jedes Modul und jede Funktion
- Type-Hints wo sinnvoll (`def embed(texts: list[str]) -> np.ndarray:`)
- ChromaDB-Client als Singleton (nicht pro Request neu instanziieren)
- Embedding-Model einmal laden, dann wiederverwenden
- Fehler via Exceptions, nicht via Print+Exit
- `if __name__ == "__main__":` Guard

## Late Chunking (Phase 2.2, PDF-Domains)

Für PDF-basierte Domains (z.B. DaVinci Resolve) wird seit Phase 2.2 chapter-weises
Late Chunking verwendet. Statt jeden Chunk einzeln zu embedden, wird der gesamte
Chapter als ein langer Token-Stream an das BGE-M3-Modell gefüttert (long-context
8192 Token) und das Modell erzeugt kontext-sensitive Token-Embeddings. Anschließend
werden 512-Token-Fenster mit 128-Token-Overlap über die Token-Embeddings gelegt
und pro Fenster gemittelt (mean pooling).

Konventionen:

- **`_LateChunkEncoder` MPS-Pre-Flight-Pattern:** Vor dem Encoding-Loop ein
  Warmup-Token-Batch laufen lassen, um die tatsächliche Compute-Device (CPU,
  CUDA, MPS) zu erkennen. Bei MPS-OOM einmal pro Session auf CPU zurückfallen
  (nicht pro Chunk). Verhindert wiederholte Crashes auf Apple Silicon.
- **BGE-M3 MPS Hang (transformers 4.57.6, RESOLVED 2026-07-04):** `torch`
  2.12.0 behebt den BGE-M3 + `transformers` 4.57.6 MPS-Deadlock, der zuvor
  `device='cpu'` erzwungen hat. `model_manager.get_embedder()` nutzt jetzt
  die `KH_EMBEDDING_DEVICE` env var (Default `cpu`, opt-in `mps`, ~4,7×
  Speedup auf Apple Silicon). Siehe LIM-011 (resolved) und die
  `KH_EMBEDDING_DEVICE`-Sektion unten.
- **`precomputed_embeddings` als separates Dict:** Die BGE-M3-Token-Embeddings
  werden in einem separaten Dict `{chunk_id: np.ndarray}` durch die Pipeline
  gereicht, nicht als Chunk-Attribut gespeichert. Das hält die Chunk-Daten klein
  (Token-Embeddings sind 1024-dim Vektoren pro Token) und ermöglicht das
  Window-Mean-Pooling außerhalb der Embedding-Funktion.
- **`_token_windows_from_offsets` lossless via offset mapping:** Die
  Original-zu-Token-Offsets werden mitgeführt, damit Window-Mean-Pooling
  verlustfrei auf den exakten Token-Regionen operieren kann. Niemals auf
  String-Substring-Operationen zurückfallen (würde mit BGE-M3-Tokenizer
  divergieren).

## Markdown-Dokumentation

- `##`-Header für Sektionen, `###` für Sub-Sektionen
- Tabellen für strukturierte Daten (Quellen, Metadaten, Zustände)
- Code-Blöcke mit Sprachangabe (\`\`\`bash, \`\`\`python, \`\`\`markdown)
- Links auf andere Docs/Dateien
- Status-Indikatoren: ✅ (erledigt), ⚠️ (Warnung), ❌ (Fehler/fehlt)

## Versionierung

- ChromaDB-Index ist `.gitignored`
- Packed-Files via Git LFS (`.gitattributes`)
- `requirements.txt` mit version-pinned Dependencies
- Semver-ähnliche Tags für Releases (später)

## Umgebungsvariablen

- `KH_RERANKER_MODEL` — Überschreibt das Cross-Encoder-Modell für Stage-2-Reranking.
  Default: `cross-encoder/ms-marco-MiniLM-L-12-v2`.
  Empfohlene Alternative (multilinguale Domains, BGE-M3-Embeddings):
  `jinaai/jina-reranker-v2-base-multilingual` (multilingual, 1024 Token Kontext,
  CC-BY-NC-4.0). BGE-M3 (multilingual Embeddings) + jina (multilingual Reranker)
  bilden eine konsistente Multilingual-Pipeline und lösen LIM-008 (Sprachbarriere).
  Setup für lokalen Default: `export KH_RERANKER_MODEL=jinaai/jina-reranker-v2-base-multilingual`
  in `~/.zshrc` oder `.env` setzen. Der CI quality-gate nutzt jina als Default seit
  2026-07-01. Score-Skala-Hinweis: jina nutzt sigmoid (0–1), ms-marco nutzt logits
  (−10..+10) — beide sind sort-kompatibel (rank-basiert, kein Threshold), sodass
  `hybrid_search.py` und `scorer.py` ohne Anpassung funktionieren.
  Wird in `mcp_servers/knowledge_hub/config.py` ausgewertet. `trust_remote_code=True`
  in `model_manager.py` aktiviert HuggingFace-Custom-Code-Ladung für jina-Modelle
  (siehe `docs/ai/security.md` für das akzeptierte Risiko).
- `KH_EMBEDDING_MODEL` — Überschreibt das Embedding-Modell (Phase 2a, Decision 2.2).
  Default: `all-mpnet-base-v2` (768 dims, English-only, ~420 MB).
  Alternative: `BAAI/bge-m3` (1024 dims, multilingual, 8192 Token Kontext, MIT, ~2.2 GB Download).
  Wird LIVE in `model_manager.get_embedder()` auf jedem Cache-Miss gelesen.
  Precedence (Decision 2.7): Env-Var > `domain.md` (`## Metadaten → Embedding-Model`) > `config.DEFAULT_MODEL_NAME`.
  Hinweis: Gleichzeitiges Laden beider Modelle kostet ~2.6 GB RAM (`_model_cache` ist aktuell plain dict ohne LRU — LRU-Migration in Phase 2b, B4).
- `KNOWLEDGE_HUB_DOMAINS` — Komma-separierte Domain-Liste für MCP-Server-Scoping.
  Wird in `mcp_servers/knowledge_hub/server.py` ausgewertet.
- `KH_LLM_MODEL` — Überschreibt das LLM-Modell für Contextual Retrieval (Phase 3.1).
  Default: `gemma4:12b-mlx` (Gemma 4 12B, 7.7 GB MLX-quantisiert, Apache 2.0,
  256K Token Kontext, 140+ Sprachen). Wird LIVE in `model_manager.get_llm()`
  auf jedem Cache-Miss gelesen. System-Setup: `brew install ollama &&
  ollama pull gemma4:12b-mlx`. Ollama nutzt MLX nativ auf Apple Silicon
  (seit v0.19, optimiert für Gemma 4 in v0.31.1 mit 90 % MTP-Speedup).
  ACHTUNG: Ollama v0.31.1+ ist für Gemma 4 erforderlich; ältere Versionen
  lehnen den Pull mit HTTP 412 ab ("requires a newer version of Ollama").
- `KH_LLM_BACKEND` — Überschreibt das LLM-Backend (Phase 3.1).
  Default: `ollama` (HTTP-API, MLX-native). Alternative: `llama-cpp`
  (Cross-Platform-Fallback, benötigt `llama-cpp-python`).
  Ollama muss als System-Service laufen (`ollama serve` oder
  `brew services start ollama`). Das `ollama` Python-Package ist nur ein
  HTTP-Client (~10 MB) und pulled keine transformers/PyTorch — kein
  Dependency-Konflikt mit dem BGE-M3/jina-Stack (B4 ist bei Ollama kein
  Blocker).
- `KH_OLLAMA_HOST` — Überschreibt den Ollama-HTTP-Host (Phase 3.1a
  Security-Hardening). Default: `http://localhost:11434` (Loopback,
  keine Datenexfiltration). Ein non-loopback Host (z.B.
  `http://remote.example:11434`) wird NUR akzeptiert, wenn diese Env-Var
  explizit gesetzt ist (Opt-in) — die implizite `OLLAMA_HOST`-Default des
  ollama-Python-Clients wird absichtlich NICHT honoring, um versehentliche
  Exfiltration lokaler Repo-/Personal-Notes-Inhalte zu verhindern. Bei
  non-loopback Host wird eine WARNING geloggt. Der LLM-Cache-Key ist
  `llm:<backend>:<model_name>` (inkl. Backend, verhindert stale
  cross-backend Reuse).
- `KH_EMBEDDING_DEVICE` — Überschreibt das Compute-Device des
  Embedders (Phase 3.3a, LIM-011 RESOLVED). Default: `cpu`
  (backward-compat, sicher auf jeder Plattform). Opt-in MPS GPU
  Beschleunigung via `KH_EMBEDDING_DEVICE=mps` — `torch` 2.12.0 hat
  den BGE-M3 + `transformers` 4.57.6 MPS-Deadlock behoben, der zuvor
  `device='cpu'` erzwungen hat (~4.7× Speedup auf Apple Silicon).
  Der Embedder-Cache-Key ist `embedder:<model>:<device>` — ein
  Runtime-Switch lädt eine frische Instanz statt eine falsch-Device
  Cache-Instanz zurückzugeben. **Pre-Flight-Mitigation (R1.1):** vor
  jedem großen Build wird ein 100-Chunk MPS-Encode empfohlen; bei
  Hang (>30 s) auf CPU zurückfallen. Integration-Test
  `test_mps_encode_pre_flight` automatisiert den Check.
- `KH_LLM_WORKERS` — Überschreibt die Anzahl paralleler LLM-Worker
  für Contextual Retrieval (Phase 3.3a). Default: `1` (sequenziell,
  backward-compat). `>1` dispatcht Cache-Misses an einen
  `ThreadPoolExecutor` (z.B. `3` für Ollama-Cloud Pro Concurrency).
  CLI-Flag `--workers N` an `contextualize_chunks.py` überschreibt die
  env var. SQLite-Writes werden über einen `threading.Lock` und
  `PRAGMA busy_timeout=5000` serialisiert; ein geteiltes
  `threading.Event` propagiert HTTP 429 Usage-Limit-Abbrüche an alle
  in-flight Worker (Cache bleibt für Resume intakt).

**Contextual Retrieval setzt BGE-M3 voraus (N4):** Das LLM-generierte
`context_prefix` (50–100 Token) wird vor dem Embedding an den Chunk-Text
gehängt (`context_prefix + "\n" + text`). Bei all-mpnet-base-v2 (384 Token
Kontext) würde dieser Zusatz den Chunk truncieren. BGE-M3 (8192 Token
Kontext) ist daher die Voraussetzung für Phase 3.1 und über
`KH_EMBEDDING_MODEL=BAAI/bge-m3` bzw. `domain.md` aktiviert. Der Pfad-A-
Geltungsbereich (N1) umfasst domänenübergreifend alle Chunks mit
`chunk_type != "late_chunk"`; Late-Chunking (DaVinci) ist ausgenommen (D2),
da es bereits Chapter-Kontext besitzt.

**Gemma 4 12B ist ein Reasoning-Modell (Phase 3.1a Erkenntnis):** Gemma 4
12B MLX generiert vor der finalen Antwort eine interne Thinking-Phase
(`message.thinking`-Feld in der Ollama-Antwort). Mit dem Anthropic-Default
von `num_predict=100` reicht das Token-Budget oft nur für die Thinking-
Phase — `content` bleibt leer (`done_reason='length'`). Empirisch braucht
der Contextual-Retrieval-Prompt ~256 eval-Tokens (949 Zeichen Thinking +
~15 Token Antwort). `generate_context()` nutzt daher `num_predict=800`
als Default (mit headroom für längere Dokumente). Bei ~16.6s pro Chunk
skaliert das auf ~15.000 Godot-Chunks = ~69 Stunden (reiner LLM-Teil) —
länger als die ursprüngliche 15–20h Schätzung der Spec, weil das
Reasoning-Modell mehr Tokens generiert. Die Durchsatz-Planung in Phase
3.1b/c muss das berücksichtigen (ggf. später `num_predict` tunen oder
ein Non-Reasoning-Modell evaluiert).

## Contextual Retrieval CLI (Phase 3.1b)

- **`contextualize_chunks.py`** — CLI-Skript für Kontext-Generierung:
  ```bash
  python scripts/contextualize_chunks.py --domain godot
  python scripts/contextualize_chunks.py --domain godot --limit 50 --dry-run
  python scripts/contextualize_chunks.py --domain godot --source-file foo-packed.md
  python scripts/contextualize_chunks.py --domain godot --batch-size 100
  python scripts/contextualize_chunks.py --domain godot --workers 3  # Phase 3.3a
  ```
  Batch-Loop mit Ollama-Startup-Check, Cache-Lookup, LLM-Call mit Retry/Backoff
  (exponentiell 30s/60s/120s, 3 Versuche), Output-Validation, Resume via SQLite-Cache.
  Pfad-A-Filter: pure `chunk_type != "late_chunk"` (Spec N1, kein Domain-/source_types-Check).
  Phase 3.3a: `--workers N` (oder `KH_LLM_WORKERS` env var) dispatcht Cache-Misses
  an einen `ThreadPoolExecutor`. SQLite-Writes werden über einen `threading.Lock`
  und `PRAGMA busy_timeout=5000` serialisiert; HTTP 429 bricht alle Worker über
  ein geteiltes `threading.Event` ab (Cache bleibt für Resume intakt).

- **`embed_index.py --contextualize`** — Liest `context_prefix` aus dem SQLite-Cache
  und nutzt `context_prefix + "\n" + text` als Embedding-Input (D1). BM25 bleibt
  `text` only. `--contextualize-bm25` Flag akzeptiert aber noch nicht genutzt.

- **`run_evaluation.py --dataset-path`** — Expliziter Golden-Dataset-Pfad für
  Spot-Check-Gate (z.B. `quality/golden/godot_spotcheck.yaml`). Default `None` →
  backward-kompatibel.

- **Spot-Check-Gate (Phase 3.1b):** `quality/golden/godot_spotcheck.yaml` (2 Fragen),
  `scripts/quality/gate.py` mit `decide_gate(composite_delta)` → `"GO"`/`"NO-GO"`
  (Schwelle ≥ −0,02). Nur No-Go-Gate — echte Quality-Entscheidung in 3.1c.

- **Retry/Backoff:** Exponentielles Backoff (30/60/120s, 3 Versuche) bei transienten
  Ollama-Connection-Errors. Nach 3 Fehlern → `RuntimeError`, Cache behält alle
  bereits geschriebenen Einträge für Resume.

**Cloud-Setup (Phase 3.1c, ~3h für 4580 Pfad-A-Chunks):**
```bash
ollama signin && ollama pull gemma4:cloud
export KH_LLM_MODEL=gemma4:cloud
# KH_OLLAMA_HOST bleibt localhost (lokaler Daemon routet Cloud)
# Alternative: gpt-oss:20b-cloud (Usage Level 1, günstiger)
# Usage-Limit: contextualize_chunks.py stoppt bei HTTP 429, Resume via Cache
# Account-Wechsel: ollama signin, neu starten, Cache bleibt gültig
# Transienter Cloud-Ausfall (502): 3× Backoff, dann RuntimeError — neu starten für Resume
```

**Contextual BM25 (Phase 3.2, GO):**
```bash
# C-Variante: Embeddings + BM25 kontextualisiert
KH_LLM_MODEL=gemma4:cloud python scripts/embed_index.py --domain <domain> --contextualize --contextualize-bm25
# Default (ohne --contextualize-bm25): BM25 bleibt clean (D1, Backward-Compat)
# Cache-Reuse: cp context_cache.db von eval-Domain nach Ziel-Domain (vorher PRAGMA wal_checkpoint)
```

## Sicherheit

- Keine Secrets in Config-Dateien
- API-Keys nur via Environment-Variablen oder `.env` (gitignored)
- Keine harten `/Users/noahk/`-Pfade (außer in dieser Doku und opencode.json)
- Shell-Skripte prüfen Inputs (z.B. Domain-Namen validieren)
- **Pickle-Sicherheit:** `rank_bm25` serialisiert/deserialisiert BM25-Indizes via Python `pickle`. Für den persönlichen Hub akzeptabel (alle Dateien unter eigener Kontrolle, kein externer Input). Produktion/Shared-Hub wäre problematisch — dann auf JSON oder safetensors migrieren.

## Vision Retrieval Feature (2026-07-07)

### Neue Env-Vars

- `KH_MULTIMODAL_MODEL` — Überschreibt das Multimodal-Embedding-Modell
  (SigLIP-2 / jina-clip-v2). Default: `google/siglip2-so400m-patch16-512`
  (Apache 2.0, 1152 dims, 512×512, English-only, kommerziell sicher).
  Optional: `jinaai/jina-clip-v2` (CC-BY-NC-4.0, multilingual, 1024 dims,
  `trust_remote_code=True`, analog jina-reranker-v2).
  Wird LIVE in `model_manager.get_multimodal_embedder()` auf jedem Cache-Miss
  gelesen. Precedence: Env-Var > `DEFAULT_MULTIMODAL_MODEL`.
- `KH_MULTIMODAL_DEVICE` — Überschreibt das Compute-Device des Multimodal-
  Embedders. Default `cpu`, opt-in `mps` (Apple Silicon, ~4.7× Speedup).
  Cache-Key: `multimodal:<model>:<device>` (Runtime-Switch lädt frische
  Instanz). Pre-Flight-Mitigation: 10-Bild MPS-Encode vor jedem Build;
  bei Hang (>30s) auf CPU zurückfallen (`embed_images.py` automatisiert).
- `KH_MULTIMODAL_BATCH_SIZE` — Default `32`. MPS RAM-limitiert (Spheron
  empfiehlt 256-512 für Server-GPUs; auf M1 Max ist 32-128 sicher).
- `KH_VISION_LLM_MODEL` — Überschreibt das Vision-LLM für Bild-Captioning.
  Default folgt `KH_LLM_MODEL` (`gemma4:cloud`). Wird in `caption_images.py`
  genutzt.
- `KH_VISION_LLM_WORKERS` — Default `1` (sequenziell), opt-in `3` für
  Ollama-Cloud Pro Concurrency. CLI-Flag `--workers N` an `caption_images.py`
  überschreibt die env var. ThreadPoolExecutor + `cancel_event` bei HTTP 429.

### CLI-Skripte

```bash
# 1. Bilder extrahieren (AGPL build tool, PyMuPDF4LLM)
python scripts/extract_pdf_images.py --domain davinci_resolve
python scripts/extract_pdf_images.py --domain davinci_resolve --quality-check

# 2. Captions generieren (Gemma 4 Cloud, 3 Worker)
KH_LLM_MODEL=gemma4:cloud KH_VISION_LLM_WORKERS=3 \
    python scripts/caption_images.py --domain davinci_resolve --workers 3

# 3. Bild-Embeddings bauen (SigLIP-2, MPS)
KH_MULTIMODAL_DEVICE=mps KH_MULTIMODAL_BATCH_SIZE=64 \
    python scripts/embed_images.py --domain davinci_resolve

# 4. Bild-BM25 + Text-Index (additiv)
python scripts/embed_index.py --domain davinci_resolve --embed-images
```

### Pre-Flight MPS-Check (SigLIP-2)

`embed_images.py` führt vor jedem Build einen 10-Bild MPS-Encode durch.
Bei Hang (>30s) oder OOM fällt es automatisch auf CPU zurück und lädt
das Modell neu. Der Check ist auch standalone verfügbar:

```bash
KH_MULTIMODAL_DEVICE=mps python scripts/embed_images.py --domain davinci_resolve --pre-flight-only
```

### Context-Aware Captions (TowardsDataScience Best-Practice)

Captions sind context-aware: `context_before + [IMAGE: description] + context_after`.
Der Vision-LLM bekommt den umgebenden Handbuch-Text (±200 chars, bereinigt
um Bild-Referenzen) als Disambiguierungshilfe. Ähnlich aussehende
Screenshots (verschiedene Color-Page-Dialoge) bekommen so unterscheidbare
Captions.

### Content-Hash Caching (AugmentCode Rule 8)

`image_caption_cache.db` und `image_embedding_cache.db` verwenden
content-hash Keys (SHA-256 der Bild-Bytes + Modell + Modality). Bei
Re-Builds werden unveränderte Bilder/Captions übersprungen. Cache-Resume
nach Abbruch: alle bereits verarbeiteten Bilder bleiben im Cache.

## Visual Question Answering (image_path, 2026-07-07)

### search_knowledge mit image_path

```python
# Über MCP-Tool (OpenCode Agent):
search_knowledge(
    domain="davinci_resolve",
    query="Color Wheels panel",         # Frage als Text zusammengefasst
    image_path="/tmp/uploads/img.png",  # absoluter Pfad zum Nutzer-Bild
    mode="hybrid",
    max_results=10,
)
```

**Verhalten:**
- 4-Listen-RRF läuft unverändert (text + image_bm25 + caption).
- ZUSÄTZlich wird `image_similarity_search()` aufgerufen: das Query-Bild
  wird mit SigLIP-2 embeddet und gegen `<domain>_images` (modality=image)
  per Cosine-Similarity gesucht.
- `image_match` Treffer werden vorangestellt (additiv, bis top_k).
- `image_match_count` im Return-Dict gibt die Anzahl der Bild-Treffer.

**Backward-Kompatibel:** Ohne `image_path` läuft die Text-Suche
unverändert. Kein `image_match` in Results, `image_match_count = 0`.

### Cache-Verhalten

Query-Image-Embeddings werden in `image_embedding_cache.db` gecacht:

- `modality = "query_image"` (NICHT `"image"` — das sind indexierte
  Screenshots; Kollision würde zu falschen Cache-Hits führen).
- `image_id = "query"` (stabilen Placeholder, damit gleiche Bild-Bytes
  + gleiches Modell denselben Cache-Key ergeben).
- Cache-Key: `sha256("query" | <content_hash> | <model> | "query_image")`.
- Bei wiederholter Query desselben Bildes: Cache-Hit (~0ms Embedding).

### Graceful Fallback

`image_similarity_search()` returniert `[]` bei:

- Bild-Datei existiert nicht
- PIL kann Bild nicht dekodieren (kein gültiges PNG/JPG)
- SigLIP-2 nicht verfügbar (Modell nicht geladen / nicht heruntergeladen)
- `<domain>_images` Collection existiert nicht (Domain ohne Vision Feature)

Die `search()`-Funktion fängt zusätzlich alle Exceptions ab und setzt
`image_match_count = 0` — die Text-Suche bleibt unbeeinflusst.

### Einschränkungen

- Nur `davinci_resolve` hat indexierte Screenshots. Andere Domains
  liefern keine `image_match` Treffer.
- Keine OCR-Texterkennung — SigLIP-2 findet *ähnliche* Screenshots,
  keine Text-Inhalte. Wenn das Nutzer-Bild Text enthält, der nicht in
  DaVinci-Screenshots vorkommt, kann die Suche schwach sein.
- Captions sind kontext-aware ( TowardsDataScience Best-Practice:
  `context_before + [IMAGE: description] + context_after`), aber
  gelegentlich leicht verrauscht (VRF-002).
