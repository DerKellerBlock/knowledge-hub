# Spec: Visual Question Answering via MCP (Image-Query Search)

**Task-ID:** visual-question-answering
**Datum:** 2026-07-07
**Status:** open
**Priorität:** high

## Problem

Aktuell kann ein OpenCode-Nutzer ein Bild hochladen ("was ist das recht
unten bei Scope?"), aber das OpenCode-LLM (gpt-5.5 / glm-5.2) kann keine
Bilder lesen → "this model does not support image input" Error.

Der Nutzer erwartet: das LLM gibt den Bild-Pfad an `search_knowledge` weiter,
der Knowledge Hub findet ähnliche DaVinci-Screenshots und gibt die Captions
zurück → "das ist ein Vectorscope, gefunden auf Seite X".

Das ist aktuell nicht möglich weil `search_knowledge` nur Text-Queries
akzeptiert, keine Bild-Pfade.

## Ziel

Erweitere `search_knowledge` um einen optionalen `image_path` Parameter.
Bei Setzung:
1. Bild mit SigLIP-2 embedden (gleicher Vektorraum wie indexierte Screenshots)
2. Semantische Bild-Suche in ChromaDB `<domain>_images` (image modality)
3. Ähnliche Screenshots finden → Top-K nach Cosine-Similarity
4. Captions der ähnlichen Screenshots zurückgeben
5. LLM bekommt die Captions + Bild-Pfade → "das ist ein Vectorscope, Seite X"

Der OpenCode-Agent muss instruiert werden: wenn ein Nutzer ein Bild
hochlädt und eine Frage dazu stellt, den Bild-Pfad als `image_path` an
`search_knowledge` weiterzugeben.

## Architektur

```
Nutzer lädt Bild hoch + Frage
       │
       ▼
OpenCode LLM (gpt-5.5 / glm-5.2 / MiniMax M3)
       │  extract image_path from upload
       │  call search_knowledge(domain, query, image_path=...)
       │
       ▼
search_knowledge MCP-Tool
       │  ┌─ image_path gesetzt?
       │  │   JA → image_similarity_search()
       │  │        1. Bild laden (PIL)
       │  │        2. SigLIP-2 image-embed → 1152-dim Vektor
       │  │        3. ChromaDB <domain>_images query (where modality=image)
       │  │        4. Top-K nach cosine similarity
       │  │        5. Captions aus Metadaten anreichern
       │  │
       │  └─ image_path NICHT gesetzt?
       │      → bestehende 4-Listen-RRF (Text + Bild + Caption)
       │
       ▼
Result JSON an LLM
       │  {results: [
       │    {modality: "image_match", score: 0.87,
       │     image_path: "...", caption: "The Vectorscope panel...",
       │     page: 1234, source_file: "reference-manual.md"}
       │  ]}
       │
       ▼
LLM generiert Antwort
       "Das ist ein Vectorscope. Du findest ihn in DaVinci Resolve
        auf der Color Seite rechts unten. Siehe Seite 1234 im
        Reference Manual."
```

## Anforderungen

### 1. `image_similarity_search()` in `hybrid_search.py`

Neue Funktion die ein Bild embeddet und ähnliche Screenshots findet:

```python
def image_similarity_search(
    domain: str,
    image_path: str,
    top_k: int = 10,
) -> list[dict]:
    """Find similar screenshots by image embedding.

    1. Load image via PIL
    2. Embed with SigLIP-2 (get_multimodal_embedder)
    3. Query ChromaDB <domain>_images (where modality="image")
    4. Return top-k with caption + page metadata
    """
```

**Cache:** Nutze `image_embedding_cache.py` — falls das Bild schon
mal embeddet wurde (content-hash), Cache-Hit.

**Pre-Flight:** Falls SigLIP-2 nicht verfügbar (Modell nicht geladen),
graceful fallback auf leere Results + Warning.

### 2. `search_knowledge` erweitern (MCP-Tool)

`mcp_servers/knowledge_hub/tools.py` + `server.py`:

Neuer optionaler Parameter `image_path`:

```python
def search_knowledge(
    domain: str,
    query: str,
    mode: str = "hybrid",
    max_results: int = 10,
    image_path: str | None = None,  # NEU
) -> dict:
    """Wenn image_path gesetzt: image_similarity_search zusätzlich zur
    Text-Suche. Ergebnisse werden gemischt."""
```

**Verhalten bei `image_path` gesetzt:**
- Text-Suche mit `query` läuft normal (4-Listen-RRF)
- ZUSÄTZLICH: `image_similarity_search(domain, image_path, top_k)`
- Beide Result-Listen werden gemischt (image_match hat eigene modality)
- Bild-Ähnlichkeits-Treffer bekommen `modality: "image_match"` + `similarity_score`

**Backward-kompatibel:** Ohne `image_path` → unverändertes Verhalten.

### 3. MCP-Tool Schema aktualisieren (`server.py`)

Der `search_knowledge` Tool-Input-Schema muss `image_path` als optionalen
Parameter deklarieren:

```json
{
  "name": "search_knowledge",
  "inputSchema": {
    "type": "object",
    "properties": {
      "domain": {"type": "string"},
      "query": {"type": "string"},
      "mode": {"type": "string", "default": "hybrid"},
      "max_results": {"type": "integer", "default": 10},
      "image_path": {"type": "string", "description": "Optional: path to an image file for visual similarity search"}
    }
  }
}
```

### 4. Orchestrator Instructions aktualisieren

Der `orchestrator-knowledge` Agent-Prompt muss instruiert werden:

```
Wenn ein Nutzer ein Bild hochlädt und eine Frage dazu stellt:
1. Extrahiere den Bild-Pfad aus dem Upload
2. Rufe search_knowledge(domain, query, image_path=<path>) auf
3. Die Ergebnisse enthalten "image_match" Treffer mit Captions ähnlicher
   Screenshots aus dem DaVinci-Handbuch
4. Nutze die Captions um zu erklären was auf dem Nutzer-Bild zu sehen ist
```

### 5. Optional: Vision-LLM Integration (MiniMax M3)

Als optionale Erweiterung könnte ein Vision-LLM (z.B. MiniMax M3) die
gefundenen ähnlichen Screenshots + das Nutzer-Bild direkt vergleichen:

```
Nutzer-Bild + Top-3 ähnliche DaVinci-Screenshots
       │
       ▼
Vision-LLM (MiniMax M3)
       "Das Nutzer-Bild zeigt einen Vectorscope. Ähnlich wie Screenshot
        X aus dem Reference Manual Seite 1234. Der Vectorscope befindet
        sich auf der Color Page rechts unten."
```

Dies ist **optional** — die Caption-basierte Antwort (Schritt 1-4) funktioniert
auch ohne Vision-LLM. Die Vision-LLM-Integration würde die Antwortqualität
verbessern indem sie das Nutzer-Bild direkt versteht, nicht nur über die
ähnlichen Captions schließt.

**MiniMax M3 Integration:**
- MiniMax M3 unterstützt Bild-Input (multimodal)
- Kann via OpenAI-compatible API aufgerufen werden
- Wäre ein separater MCP-Tool `analyze_image` oder integriert in `search_knowledge`
- Env-Var: `KH_VISION_QA_MODEL=minimax/m3` (optional, default off)

### 6. Error Handling

- `image_path` existiert nicht → graceful Error, Results ohne image_match
- `image_path` ist kein gültiges Bild → PIL Error, graceful
- SigLIP-2 nicht verfügbar → Warning, Results ohne image_match
- ChromaDB `<domain>_images` existiert nicht → Warning (Domain ohne Vision Feature)

## Akzeptanzkriterien

1. `image_similarity_search()` in `hybrid_search.py` implementiert
2. `search_knowledge` MCP-Tool akzeptiert optionalen `image_path` Parameter
3. Bei `image_path` gesetzt: Bild wird embeddet, ähnliche Screenshots gefunden
4. Ergebnisse enthalten `modality: "image_match"` mit `similarity_score`, `caption`, `page`, `source_file`
5. Backward-kompatibel: ohne `image_path` unverändertes Verhalten
6. MCP-Tool Schema in `server.py` deklariert `image_path` als optional
7. Orchestrator-Prompt instruiert Agent Bild-Pfade weiterzugeben
8. Error Handling: graceful bei fehlendem Bild / Modell / Collection
9. Alle 226 Unit-Tests bleiben grün
10. Optional: MiniMax M3 Vision-LLM Integration (separater Task)

## Nicht-Ziele

- Bild-Generierung (keine "generiere mir einen Screenshot")
- OCR (keine Text-Extraktion aus Bildern)
- Bildervergleich ohne DaVinci-Domain (nur DaVinci hat Bilder indexiert)
- Bild-Upload direkt an ChromaDB (Bild wird nur für Query embeddet, nicht indexiert)

## Forschungsquellen

- SigLIP-2 Model Card: https://huggingface.co/google/siglip2-so400m-patch16-512
- MiniMax M3: https://www.minimaxi.com/en (multimodal LLM)
- CLIP-based Image Retrieval: https://arxiv.org/abs/2103.00020
