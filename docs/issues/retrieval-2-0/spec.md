# Retrieval 2.0 — Design Spec

> **Status:** Design abgeschlossen, wartet auf Planung | **Datum:** 2026-06-09 | **Autor:** Orchestrator + Noah
>
> Abgeleitet aus: Schwachstellen-Review der aktuellen Retrieval-Pipeline und Nutzer-Feedback.
> Referenziert: `docs/superpowers/specs/2026-06-09-knowledge-hub-design.md`

## Motivation

Das aktuelle Retrieval (Phase 1–3) hat drei strukturelle Schwächen:

1. **Fließtext-Chunking ohne Strukturwissen:** Godot-RST-Docs haben eine klare Klassen-Hierarchie (Klasse → Properties, Methoden, Signale, Enums, Vererbung), aber das Chunking (500-Token-Sliding-Window) weiß nichts davon. Chunks sind blinde Text-Slices ohne Wissen, ob sie eine Methode, Property oder Fließtext enthalten.
2. **Kein Relevanz-Score im Keyword-Retrieval:** ripgrep liefert binäre Match/No-Match-Ergebnisse. Die RRF-Fusion arbeitet mit Rang-Positionen, nicht mit Scores — das reduziert die Fusions-Qualität.
3. **Kein intelligentes Re-Ranking:** RRF ist ein simpler Positions-Merge. Ein Cross-Encoder kann Query-Dokument-Paare präzise bewerten und liefert signifikant bessere Top-10-Ergebnisse.

## Ziel

Ein **zweistufiges Retrieval-System**, das Keyword-Matching (BM25) und semantische Suche (ChromaDB/Dense) intelligent mit Cross-Encoder-Reranking kombiniert — plus strukturiertes Parsing der Quellen via Plugin-System.

Das System bleibt **domain-agnostisch**: Jede Domain kann optional einen Parser definieren. Ohne Parser fällt das System auf das bewährte Fließtext-Chunking zurück.

## Architektur-Übersicht

```
┌──────────────────────────────────────────────────────────────┐
│                    Knowledge Hub 2.0                          │
│                                                               │
│  domains/<name>/                                              │
│  ├── domain.md          (Quellen + optional: parser-Hinweis)  │
│  ├── parser.py          (optional, Plugin-System)            │
│  ├── sources/           (repomix Output)                     │
│  ├── personal/          (Noahs Wissen)                       │
│  └── scripts/           (update.sh, status.sh)               │
│                                                               │
│  scripts/                                                     │
│  ├── parser_base.py     ← Plugin-Interface + Chunk-Dataclass  │
│  ├── embed_index.py     → Chunks → ChromaDB + BM25-Index     │
│  ├── embed_search.py    ← ChromaDB (Dense)                   │
│  ├── bm25_search.py     ← BM25 (Sparse)              [NEU]   │
│  ├── reranker.py        ← Cross-Encoder               [NEU]  │
│  └── hybrid_search.py   ← BM25 + Dense → fusion → rerank     │
│                                                               │
│  mcp_servers/knowledge_hub/                                   │
│  ├── server.py          (Tools: aktualisierte Signaturen)    │
│  ├── tools.py           (Nutzung von hybrid_search.py)       │
│  └── config.py          (neue Pfade, Model-Config)           │
└──────────────────────────────────────────────────────────────┘
```

### Datenfluss einer Query

```
Query "wie rotiere ich Node3D um Y-Achse"
  │
  ├──► BM25 (rank_bm25)        ──► Top-100 Sparse
  ├──► ChromaDB (Dense)        ──► Top-100 Semantic
  │
  └──► RRF-Fusion (k=60)       ──► Top-20 Kandidaten
       │
       └──► Cross-Encoder       ──► Top-10 gerankt
            (ms-marco-MiniLM-L-12-v2)
```

### Gegenüberstellung: Aktuell vs Neu

| Aspekt | Aktuell (Phase 1-3) | Neu (Retrieval 2.0) |
|--------|---------------------|---------------------|
| Keyword-Retrieval | ripgrep (binär) | BM25 (Relevanz-Score) |
| Semantische Suche | ChromaDB + MPNet | Unverändert |
| Fusion | RRF (k=60) | RRF (k=60) |
| Re-Ranking | Keins | Cross-Encoder (MiniLM-L-12-v2) |
| Chunking | Zeichenbasiert (500/100) | Plugin-System + Fallback |
| Query-Preprocessing | Keins | Eingebaut via BM25-Field-Boosting |
| Code-Duplizierung | tools.py dupliziert RRF | tools.py delegiert an hybrid_search.py |

## Komponenten im Detail

### 1. Plugin-System (`scripts/parser_base.py`)

Jede Domain **kann** optional einen Parser definieren: `domains/<name>/parser.py`. Kein Parser → Fallback auf bestehendes Fließtext-Chunking.

**Chunk-Dataclass (erweitertes Schema):**

```python
@dataclass
class Chunk:
    # Pflichtfelder (immer)
    chunk_id: str           # Eindeutig, z.B. "godot::Node3D::method::rotate_y"
    domain: str             # "godot"
    text: str               # Chunk-Text (für Embedding + BM25 + Cross-Encoder)
    source_type: str        # "repo" | "personal"

    # Struktur-Felder (optional, None bei Fallback-Chunking)
    chunk_type: str | None = None     # "class" | "method" | "property" | "signal" | "enum" | "section"
    class_name: str | None = None     # Z.B. "Node3D"
    name: str | None = None           # Methoden-/Property-Name, z.B. "rotate_y"
    signature: str | None = None      # "void rotate_y(angle: float)"
    inherits_from: list[str] | None = None  # ["Node"]
    docstring: str | None = None      # Beschreibungstext

    # Position (immer)
    source_file: str = ""   # Original-Datei
    line_start: int = 0     # Zeilennummer im Original
    line_end: int = 0
```

**Parser-Interface:**

```python
class DomainParser(ABC):
    """Base class for domain-specific parsers."""

    @abstractmethod
    def parse(self, file_path: str, content: str) -> list[Chunk]:
        """Parse source content into structured chunks."""
        ...

    @property
    @abstractmethod
    def source_type_name(self) -> str:
        """Identifier, e.g. 'rst-godot'."""
        ...
```

**Discovery-Mechanismus (in `embed_index.py`):**

```python
def get_parser(domain: str) -> DomainParser | None:
    parser_path = REPO_ROOT / "domains" / domain / "parser.py"
    if parser_path.exists():
        spec = importlib.util.spec_from_file_location(f"{domain}_parser", parser_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.Parser()  # Konvention: Klasse heißt Parser
    return None
```

**Fallback-Chunking:** Wenn kein Parser existiert, wird das bestehende `chunk_text()` (Sliding-Window, 500 Tokens / 100 Overlap) verwendet und produziert `Chunk`-Objekte mit `chunk_type=None`, `class_name=None`, etc.

**`domain.md`-Erweiterung (optionales Dokumentationsfeld):**

```markdown
## Metadaten
- Parser: rst-godot    # Signalisiert menschlichen Lesern, welcher Parser läuft
```

### 2. Godot-Parser (`domains/godot/parser.py`) — Referenz-Implementierung

Der erste konkrete Parser. Dient als Referenz für alle zukünftigen Domain-Parser.

**Geparste Strukturen:**

| Chunk-Typ | Muster | Beispiel chunk_id |
|-----------|--------|-------------------|
| `class` | `.. class:: ClassName` | `godot::Node3D::class` |
| `method` | Member mit Signatur in Klasse | `godot::Node3D::method::rotate_y` |
| `property` | Member mit Typ + Getter/Setter | `godot::Node3D::property::global_position` |
| `signal` | `.. signal::` | `godot::Node3D::signal::visibility_changed` |
| `enum` | `enum EnumName` in Klasse | `godot::Node3D::enum::RotationEditMode` |
| `section` | Fließtext (Tutorials, Getting-Started) | Fallback-Chunking |

**Vererbung im Chunk-Text:** Jeder Methoden-/Property-Chunk enthält den Vererbungspfad im Text, z.B. `Node3D extends Node extends Object`. Das stellt sicher, dass eine semantische Query nach „Node Methoden“ auch `Node3D`-Methoden findet.

**Parsing-Strategie:**
1. `.. class:: ClassName` → Neue Klasse beginnt, extrahiere Vererbung (`inherits`)
2. Innerhalb einer Klasse: Member-Definitionen erkennen (Methoden mit `(`, Properties mit Typ-Annotation, Signale via `signal`)
3. Alles außerhalb von Klassen-Definitionen → Fallback-Chunking als `section`
4. Docstring-Extraktion: Text zwischen Member-Definition und nächstem Member

### 3. BM25-Indexierung

**Bibliothek:** `rank_bm25` (Python, in-memory, ~5-10 MB pro Domain mit ~20K Chunks)

**Einbindung in `embed_index.py`:**

Nach dem Chunking (egal ob via Parser oder Fallback) werden alle `Chunk`-Objekte sowohl in ChromaDB als auch in einen BM25-Index geschrieben:

```python
from rank_bm25 import BM25Okapi
import pickle

# Nach ChromaDB-Insert:
corpus = []
bm25_chunk_ids = []
for chunk in all_chunks:
    tokens = tokenize(chunk.text)
    # Field-Boosting: name + signature erhalten höheres Gewicht
    if chunk.name:
        tokens.extend(tokenize(chunk.name) * 2)       # 2x boost
    if chunk.signature:
        tokens.extend(tokenize(chunk.signature) * 3)   # 3x boost
    corpus.append(tokens)
    bm25_chunk_ids.append(chunk.chunk_id)

bm25 = BM25Okapi(corpus)
bm25_path = CHROMA_DIR / f"{domain}_bm25.pkl"
with open(bm25_path, "wb") as f:
    pickle.dump({"index": bm25, "chunk_ids": bm25_chunk_ids}, f)
```

**Persistenz:** Serialisiert per `pickle` nach `chromadb_data/<domain>_bm25.pkl`. Wird bei jeder Query geladen und im Memory gecached. Passt zum „kompletter Neuaufbau"-Modell (kein inkrementelles Update nötig).

**Speicher:** ~5-10 MB pro Domain.

### 4. BM25-Suche (`scripts/bm25_search.py`)

```python
def bm25_search(domain: str, query: str, top_k: int = 100) -> list[dict]:
    """BM25 sparse retrieval mit Field-Boosting.

    Returns:
        [
            {"chunk_id": "godot::Node3D::method::rotate_y",
             "score": 12.45,
             "match_type": "bm25"},
            ...
        ]
    """
    bm25_data = load_bm25_index(domain)  # cached
    tokens = tokenize(query)
    scores = bm25_data["index"].get_scores(tokens)
    top_indices = np.argsort(scores)[::-1][:top_k]
    return [
        {
            "chunk_id": bm25_data["chunk_ids"][i],
            "score": float(scores[i]),
            "match_type": "bm25"
        }
        for i in top_indices if scores[i] > 0
    ]
```

### 5. Cross-Encoder-Reranking (`scripts/reranker.py`)

**Modell:** `cross-encoder/ms-marco-MiniLM-L-12-v2` (12-Layer, ~130 MB Download)

```python
from sentence_transformers import CrossEncoder

_model: CrossEncoder | None = None

def get_reranker() -> CrossEncoder:
    global _model
    if _model is None:
        _model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-12-v2")
    return _model

def rerank(
    query: str,
    candidates: list[dict],
    top_k: int = 10
) -> list[dict]:
    """Cross-Encoder re-ranks Stage-1 candidates."""
    model = get_reranker()
    pairs = [(query, c["text"]) for c in candidates]
    scores = model.predict(pairs)

    for c, score in zip(candidates, scores):
        c["rerank_score"] = float(score)
        c["stage1_score"] = c.pop("score", None)
        c["score"] = float(score)

    candidates.sort(key=lambda c: c["score"], reverse=True)
    return candidates[:top_k]
```

**Latenz:** ~200ms für 20-50 Kandidaten-Paare (CPU).
**Fallback:** Wenn das Cross-Encoder-Modell nicht geladen werden kann (erste Installation, kein Internet), fällt `hybrid_search` auf RRF-only zurück mit Warning-Log.

### 6. Hybride Suche (`scripts/hybrid_search.py`) — Überarbeitet

```python
def hybrid_search(domain: str, query: str, top_k: int = 10) -> list[dict]:
    """Zweistufiges Retrieval: BM25 + Dense → RRF → Cross-Encoder."""
    # Stage 1: Parallele Breitensuche
    bm25_results = bm25_search(domain, query, top_k=100)
    dense_results = semantic_search(domain, query, top_k=100)

    # RRF-Fusion → ~20-50 Kandidaten
    fused = rrf_fuse(bm25_results, dense_results, k=60)

    # Stage 2: Cross-Encoder-Rerank → Top-10
    try:
        reranked = rerank(query, fused, top_k=top_k)
    except Exception as e:
        log_warning(f"Cross-encoder unavailable: {e}. Falling back to RRF-only.")
        reranked = fused[:top_k]

    return reranked
```

**Drei Modi erhalten:**
- `exact` → Nur BM25
- `semantic` → Nur ChromaDB/Dense
- `hybrid` → BM25 + ChromaDB + Cross-Encoder (Default)

### 7. MCP-Server-Änderungen

**Code-Deduplizierung:** `tools.py` nutzt `hybrid_search.py` direkt (keine eigene RRF-Implementierung mehr). Die gesamte Suchlogik lebt in `scripts/`.

**Tool-Signaturen bleiben kompatibel:**
- `search_knowledge` behält `domain`, `query`, `mode`, `max_results`, `source_filter`
- `mode="exact"` ruft jetzt BM25 statt ripgrep — gleiches Interface, bessere Qualität
- `update_domain` baut nach `update.sh` automatisch ChromaDB + BM25-Index
- `get_domain_status` zeigt zusätzlich: `has_parser: bool`, `bm25_index_size_mb: float`

**Erweiterte Response-Struktur:**

```json
{
  "chunk_id": "godot::Node3D::method::rotate_y",
  "text": "void rotate_y(angle: float)\n\nRotates this node around the Y axis...",
  "score": 0.97,
  "match_type": "hybrid",
  "source_type": "repo",
  "source_file": "godot-docs-reference-packed.md",
  "chunk_type": "method",
  "class_name": "Node3D",
  "name": "rotate_y",
  "signature": "void rotate_y(angle: float)",
  "inherits_from": ["Node"],
  "line_start": 1420,
  "line_end": 1445
}
```

Die neuen Struktur-Felder sind `None`, wenn der Chunk unstrukturiert ist (Fallback-Chunking).

## Technische Anforderungen

| Anforderung | Wert |
|-------------|------|
| Python | 3.11+ |
| Neue Dependencies | `rank-bm25` (zu `requirements.txt` hinzufügen) |
| Bestehende Dependencies | `chromadb>=0.5.0`, `sentence-transformers>=3.0.0`, `mcp>=1.0.0` |
| Cross-Encoder-Modell | `cross-encoder/ms-marco-MiniLM-L-12-v2` (~130 MB, auto-download via sentence-transformers) |
| Speicher (gesamt) | ~500-600 MB (ChromaDB ~350 MB + BM25 ~10 MB + Cross-Encoder ~130 MB) |
| Index-Zeit | ~5-7 Min pro Domain (CPU), inkl. BM25-Bau |
| Query-Latenz (hybrid) | Stage 1 ~50ms + Stage 2 ~200ms = ~250ms gesamt |
| Query-Latenz (exact/semantic) | ~50ms |

## Betroffene Dateien

### Neue Dateien
| Datei | Zweck |
|-------|-------|
| `scripts/parser_base.py` | Plugin-Interface + Chunk-Dataclass |
| `scripts/bm25_search.py` | BM25 Sparse Retrieval |
| `scripts/reranker.py` | Cross-Encoder-Reranking |
| `domains/godot/parser.py` | Godot RST-Parser (Referenz-Implementierung) |

### Geänderte Dateien
| Datei | Änderung |
|-------|---------|
| `scripts/embed_index.py` | Plugin-Discovery, strukturierte Chunks, BM25-Index-Bau |
| `scripts/hybrid_search.py` | BM25 statt ripgrep, Cross-Encoder-Reranking, neue RRF-Logik |
| `scripts/embed_search.py` | Angepasst an erweitertes Chunk-Schema (Rückgabe-Struktur) |
| `mcp_servers/knowledge_hub/tools.py` | Deduplizierung (delegiert an hybrid_search.py), erweiterte Response |
| `mcp_servers/knowledge_hub/config.py` | Neue Pfade (BM25-Index, Cross-Encoder-Cache) |
| `mcp_servers/knowledge_hub/server.py` | Aktualisierte Tool-Registrierung |
| `requirements.txt` | `rank-bm25` hinzufügen |
| `domains/godot/domain.md` | Parser-Hinweis, aktualisierte Metadaten |

### Entfernte Logik (nicht Dateien)
| Ort | Was |
|-----|-----|
| `scripts/hybrid_search.py` | ripgrep-Aufrufe |
| `mcp_servers/knowledge_hub/tools.py` | Eigene RRF-Implementierung, ripgrep-Aufrufe |

## Erfolgskriterien

- [ ] `domains/godot/parser.py` extrahiert strukturierte Chunks (class, method, property, signal, enum) aus Godot-RST-Docs
- [ ] Ohne Parser fällt `embed_index.py` auf bestehendes Fließtext-Chunking zurück (Rückwärtskompatibilität)
- [ ] `python scripts/hybrid_search.py --domain godot --query "wie rotiere ich Node3D um Y-Achse"` liefert `rotate_y` als Top-1
- [ ] BM25-Suche (`mode=exact`) liefert relevante Ergebnisse mit Scores (nicht nur binär)
- [ ] Cross-Encoder re-rankt Hybrid-Ergebnisse und verbessert die Top-10-Präzision
- [ ] `mcp_servers/knowledge_hub/tools.py` enthält keine eigene Suchlogik mehr
- [ ] MCP-Tool `search_knowledge` funktioniert mit allen drei Modi (exact/semantic/hybrid)
- [ ] `update_domain` baut BM25-Index parallel zu ChromaDB
- [ ] `get_domain_status` zeigt `has_parser` und `bm25_index_size_mb`
- [ ] Query-Latenz (hybrid) unter 500ms auf Consumer-Hardware (CPU)

## Entscheidungen

| # | Frage | Entscheidung | Begründung |
|---|-------|-------------|------------|
| D1 | Plugin- oder Konfigurations-basiertes Parsing? | **Plugin-basiert** (`parser.py` pro Domain) | Flexibel, erweiterbar, fällt sauber auf Fallback zurück |
| D2 | BM25 ersetzt oder ergänzt ripgrep? | **Ersetzt** ripgrep komplett | BM25+Ripgrep korrelieren stark; drei Signale machen RRF-Tuning unnötig komplex |
| D3 | BM25-Index: rank_bm25 (in-memory), Whoosh (on-disk), oder SQLite FTS5? | **rank_bm25 + pickle** | Minimal, schnell, passt zum „kompletter Neuaufbau"-Modell |
| D4 | Welches Cross-Encoder-Modell? | **ms-marco-MiniLM-L-12-v2** (~130 MB) | Höhere Genauigkeit als L-6, 12-Layer, akzeptabel für persönlichen Hub |
| D5 | MCP-Tool-Signaturen ändern oder kompatibel bleiben? | **Dürfen geändert werden** | Noch in Anfangsphase, keine externen Consumer. Skills werden mit aktualisiert. |
| D6 | Query-Preprocessing via BM25-Field-Boosting? | **Ja**, name (2x) + signature (3x) Boost im BM25-Index | Deckt Identifier-Matches ab, die ripgrep früher geliefert hat |

---

Siehe auch:
- Ursprüngliche Design-Spec: `docs/superpowers/specs/2026-06-09-knowledge-hub-design.md`
- Architektur-Doku: `docs/ai/architecture.md`
- Domain-Modell: `docs/ai/domain-model.md`
