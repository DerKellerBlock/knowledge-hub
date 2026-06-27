# DaVinci Resolve Knowledge Domain — Design Spec

> **Status:** Design abgeschlossen, wartet auf Planung | **Datum:** 2026-06-27 | **Autor:** Orchestrator + Noah
>
> Abgeleitet aus: Bedarf an DaVinci-Resolve-Lernwissen für den Video-Blog-Workspace (`video-blog/meta/`) und dem Wunsch nach RAM-effizientem, domain-scoped Knowledge-Hub-Betrieb.
> Referenziert: `docs/superpowers/specs/2026-06-09-knowledge-hub-design.md`, `docs/superpowers/specs/2026-06-09-retrieval-2-0-design.md`

## Cross-References

- Video-Blog-Workspace: `/Users/noahk/Documents/work/video-blog/meta/`
- Nak-Hopper-Game (bestehender Knowledge-Hub-Konsument): `/Users/noahk/Documents/work/nak-hopper-game/`
- Knowledge-Hub-Repo (dieses Repo): `/Users/noahk/Documents/work/knowledge-hub/`
- PyMuPDF: https://github.com/pymupdf/PyMuPDF (AGPL-3.0)
- PyMuPDF4LLM: https://github.com/pymupdf/pymupdf4llm (AGPL-3.0)
- DaVinci-Resolve-MCP (separates Projekt, nicht Teil dieses Specs): https://github.com/samuelgursky/davinci-resolve-mcp

## Motivation

Zwei Treiber führen zu diesem Spec:

1. **Lernbedarf DaVinci Resolve.** Noah lernt Videoschnitt mit DaVinci Resolve Studio 21 und braucht eine Wissensquelle, die die Fragen beantwortet: "Wo finde ich Werkzeug X in der UI?" und "Wie produziere ich erfolgreich ein Reel?" Die offizielle Blackmagic-Dokumentation liegt primär als PDF vor (Resolve 20 Reference Manual, 4234 Seiten; Resolve 21 New Features Guide; Training Guides). Eine Hybridsuche über diese Dokumentation — kombiniert mit persönlichen Notizen — ist der ideale Lernbegleiter.

2. **RAM-effizienter Multi-Domain-Betrieb.** Der Knowledge-Hub läuft bereits für `nak-hopper-game` (Godot-Domain). Eine zweite Domain (DaVinci) würde den RAM-Verbrauch erhöhen, wenn alle Domains immer geladen bleiben. Auf einem MacBook Pro M1 Max mit 32 GB RAM müssen DaVinci Resolve Studio, OBS, OpenCode und der Knowledge-Hub parallel funktionieren. Daher braucht der MCP-Server ein Domain-Scoping: nur die Domain, die das aufrufende Projekt braucht, wird geladen/durchsucht.

## Ziel

Ein **Per-Domain-isolierter, RAM-bewusster Knowledge-Hub** mit drei Eigenschaften:

1. **Per-Domain ChromaDB-Isolation:** Jede Domain hat ihre eigene ChromaDB-Datenbank, ihren eigenen BM25-Index und ihr eigenes RAM-Budget. Eine Domain kann gelöscht/rebuilded werden, ohne andere zu berühren.
2. **Domain-Scoped MCP-Server:** Der Server akzeptiert ein `--domains` CLI-Flag (oder `KNOWLEDGE_HUB_DOMAINS` Env-Var) und macht nur die konfigurierten Domains sichtbar/suchbar. Andere Domains werden nicht geladen.
3. **DaVinci-Resolve-Domain:** Eine neue Domain `davinci_resolve` mit PDF-konvertiertem Wissen aus 7 Blackmagic-Quellen plus persönlichen Lernnotizen, eingebunden in den Video-Blog-Workspace.

Zusätzlich: saubere **Lizenz-Trennung** zwischen MIT-lizenziertem Runtime-Code und AGPL-lizenziertem PDF-Build-Tool (siehe Abschnitt Lizenz-Thematik).

## Architektur-Übersicht

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    Knowledge Hub 3.0 — Per-Domain Isolation                │
│                                                                           │
│  domains/<name>/                                                          │
│  ├── domain.md          (Quellen + Metadaten + Embedding-Model-Config)     │
│  ├── sources/           (Markdown, aus PDF konvertiert oder repomix)      │
│  │   └── raw/           (Original-PDFs, gitignored)                       │
│  └── personal/          (Noahs Wissen: ui-map.md, gotchas.md, ...)        │
│                                                                           │
│  chromadb_data/<domain>/                                                  │
│  ├── chroma/            (eigene PersistentClient-DB pro Domain)            │
│  └── <domain>_bm25.pkl  (eigener BM25-Index pro Domain)                   │
│                                                                           │
│  scripts/                                                                 │
│  ├── model_manager.py   [NEU] Zentraler Model-Cache (Lazy, LRU, unload)   │
│  ├── migration.py       [NEU] Legacy-Layout → Per-Domain-Layout           │
│  ├── parse_pdf_to_markdown.py [NEU, AGPL] PDF → Markdown (PyMuPDF4LLM)    │
│  ├── validate_search.py [NEU] Regressionstest-Skript                     │
│  ├── embed_index.py     [ANGEPASST] Per-Domain-ChromaDB-Pfade             │
│  ├── embed_search.py    [ANGEPASST] nutzt model_manager                   │
│  ├── bm25_search.py     [ANGEPASST] LRU-Cache, Per-Domain-Pfade           │
│  ├── hybrid_search.py   [ANGEPASST] nutzt model_manager, Per-Domain       │
│  ├── reranker.py        [ANGEPASST] nutzt model_manager                   │
│  └── parser_base.py     (bestehend, Plugin-Interface)                    │
│                                                                           │
│  mcp_servers/knowledge_hub/                                                │
│  ├── server.py          [ANGEPASST] --domains CLI-Flag, Scoping-Logik     │
│  ├── tools.py           [ANGEPASST] nutzt model_manager                   │
│  └── config.py         [ANGEPASST] Per-Domain-Konfiguration               │
│                                                                           │
│  requirements.txt        [ANGEPASST] kein pymupdf (MIT-Runtime)             │
│  requirements-pdf.txt    [NEU] pymupdf, pymupdf4llm (AGPL-Build-Tool)      │
│  THIRD_PARTY_LICENSES.md [NEU]                                            │
│  LICENSE                 (bleibt MIT)                                     │
└──────────────────────────────────────────────────────────────────────────┘
```

### Datenfluss — PDF-Konvertierung (Build-Zeit, einmalig)

```
PDF-Datei (sources/raw/*.pdf)
  │
  ├──► scripts/parse_pdf_to_markdown.py   (AGPL — importiert pymupdf4llm)
  │      │
  │      ├── pymupdf4llm.to_markdown()  → sauberes Markdown mit Headings
  │      └── pymupdf.get_toc()         → Kapitelhierarchie + Seitenzahlen
  │
  └──► sources/*.md   (fertiges Markdown, MIT-kompatibel, kein pymupdf nötig)
```

### Datenfluss — Index-Bau (laufend, bei Update)

```
domains/davinci_resolve/sources/*.md + personal/*.md
  │
  ├──► scripts/embed_index.py   (MIT — liest Markdown, kein pymupdf)
  │      │
  │      ├── Section-Aware Chunking (Markdown-Headings als Boundaries)
  │      ├── model_manager.get_embedder("davinci_resolve")  → Vektoren
  │      ├── chromadb_data/davinci_resolve/chroma/         → PersistentClient
  │      └── chromadb_data/davinci_resolve/davinci_resolve_bm25.pkl
  │
  └──► Index fertig
```

### Datenfluss — Query (Runtime, MCP-Server)

```
search_knowledge(domain="davinci_resolve", query="trim clip edit", mode="hybrid")
  │
  ├──► model_manager.get_embedder("davinci_resolve")   (Lazy-Singleton)
  ├──► BM25 (bm25_search, Per-Domain-Pfad)             ─► Top-100 Sparse
  ├──► ChromaDB (embed_search, Per-Domain-Client)      ─► Top-100 Dense
  ├──► RRF-Fusion                                       ─► Top-50 Kandidaten
  └──► model_manager.get_reranker() (Lazy-Singleton)   ─► Top-10 gerankt
```

## Abschnitt 1: Per-Domain ChromaDB-Isolation

### Bisheriges Layout

```
chromadb_data/
  godot_knowledge/        # eine Collection
  godot_bm25.pkl
```

### Neues Layout

```
chromadb_data/
  godot/
    chroma/                # eigene DB für Godot
      godot_knowledge/     # gleiche Collection, neuer Ort
    godot_bm25.pkl
  davinci_resolve/
    chroma/
      davinci_resolve_knowledge/
    davinci_resolve_bm25.pkl
```

Jede Domain bekommt ihren eigenen `chromadb.PersistentClient` auf ihren eigenen Unterordner.

### Eigenschaften

- Keine Collection-Collisionen mehr (auch nicht bei gleichen Collection-Namen in verschiedenen Domains).
- Eine Domain kann gelöscht/rebuilded werden ohne andere zu berühren.
- Speicher-Isolation: `chroma_memory_limit_bytes` wirkt pro Domain-DB.
- Migration des Godot-Index: bestehende Collection wird nach `chromadb_data/godot/chroma/` verschoben (siehe Abschnitt 5).

### Embedding-Modelle pro Domain konfigurierbar

`domain.md` bekommt ein neues Metadaten-Feld:

```markdown
## Metadaten
- Embedding-Model: all-mpnet-base-v2 (768 dims)
- Collection: knowledge
- ChromaDB-Path: chromadb_data/godot/chroma/
- Letztes Update: 2026-06-09
```

Jede Domain kann theoretisch ihr eigenes Embedding-Modell haben. Für den Moment nutzen Godot und DaVinci beide `all-mpnet-base-v2`, aber die Architektur erlaubt später z.B. ein Code-optimiertes Modell für eine Blender-API-Domain. Ein Modellwechsel bedeutet eine neue Collection und Re-Embedding — wird nicht in-place migriert.

## Abschnitt 2: Domain-Scoped MCP-Server

### Konfigurationswege

**Weg A — CLI-Flag:**

```bash
python3 -m mcp_servers.knowledge_hub.server --domains godot
python3 -m mcp_servers.knowledge_hub.server --domains davinci_resolve
python3 -m mcp_servers.knowledge_hub.server --domains godot,davinci_resolve
```

**Weg B — Environment Variable:**

```bash
KNOWLEDGE_HUB_DOMAINS=godot python3 -m mcp_servers.knowledge_hub.server
```

**Standardverhalten (ohne Flag/Env):** alle Domains sichtbar — rückwärtskompatibel mit dem bestehenden `nak-hopper-game`-Setup, das kein Scoping hat.

### Verhalten beim Server-Start

1. `list_domains()` scannt `domains/` wie bisher.
2. **Neu:** Filtert die Liste auf die konfigurierten Domains.
3. Nur die konfigurierten Domains sind in `search_knowledge`, `get_domain_status`, `update_domain`, `add_personal_note`, `list_personal_notes` sichtbar/aufrufbar.
4. Anfragen auf nicht konfigurierte Domains → Fehlerantwort: `"Domain 'X' not available in this server scope. Available: [godot]"`.

### Einbindung in den Projekten

`nak-hopper-game/.opencode/opencode.json`:

```json
"knowledge_hub": {
  "command": [
    "/Users/noahk/Documents/work/knowledge-hub/.venv/bin/python3",
    "-m", "mcp_servers.knowledge_hub.server",
    "--domains", "godot"
  ]
}
```

`video-blog/meta/.opencode/opencode.json` (neu):

```json
"knowledge_hub_davinci": {
  "command": [
    "/Users/noahk/Documents/work/knowledge-hub/.venv/bin/python3",
    "-m", "mcp_servers.knowledge_hub.server",
    "--domains", "davinci_resolve"
  ],
  "enabled": true,
  "environment": {
    "PYTHONPATH": "/Users/noahk/Documents/work/knowledge-hub"
  }
}
```

### RAM-Auswirkung

Wenn der Server nur `davinci_resolve` kennt:

- BM25-Cache lädt nur `davinci_resolve_bm25.pkl`.
- ChromaDB-Client öffnet nur `chromadb_data/davinci_resolve/chroma/`.
- Cross-Encoder bleibt lazy (lädt nur bei erster Hybrid-Suche).
- Godot-Domain wird gar nicht berührt.

Zwei MCP-Prozesse (einer pro Projekt) können gleichzeitig laufen, ohne dass einer das Wissen des anderen lädt.

### Rückwärtskompatibilität

Wenn `nak-hopper-game` sein `--domains godot` noch nicht gesetzt hat, verhält sich der Server wie vorher (alle sichtbar). Das bedeutet: kein Breaking Change bei bestehenden Setups, bis das Flag explizit gesetzt wird.

## Abschnitt 3: Memory Management & Lazy Loading

### Aktuelle RAM-Probleme

1. `hybrid_search.py` erstellt bei jedem Suchaufruf eine neue `SentenceTransformer`-Instanz (Memory-Leak).
2. BM25-Cache (`_bm25_cache`) wächst pro Domain und wird nie gelöscht.
3. Cross-Encoder wird beim ersten `is_reranker_available()`-Check geladen und bleibt für immer.

### Neue Architektur — drei Schichten

#### Schicht 1: Zentraler Model-Manager

Ein neues Modul `scripts/model_manager.py` wird die einzige Stelle, die Modelle lädt und cacht:

```python
# scripts/model_manager.py (vereinfacht)
_model_cache: dict[str, SentenceTransformer | CrossEncoder] = {}

def get_embedder(domain: str) -> SentenceTransformer:
    """Lazy-load embedding model for a domain. Cached per model_name."""
    model_name = get_domain_config(domain).embedding_model  # from domain.md
    key = f"embedder:{model_name}"
    if key not in _model_cache:
        _model_cache[key] = SentenceTransformer(model_name)
    return _model_cache[key]

def get_reranker() -> CrossEncoder:
    """Lazy-load cross-encoder. Only loads on first hybrid search."""
    if "reranker" not in _model_cache:
        _model_cache["reranker"] = CrossEncoder(CROSS_ENCODER_MODEL)
    return _model_cache["reranker"]

def unload_domain(domain: str) -> None:
    """Unload all resources tied to a domain: BM25 index, ChromaDB collection."""
    _bm25_cache.pop(domain, None)
    _chroma_clients.pop(domain, None)
    # Note: embedder/reranker are shared across domains, kept cached.
    gc.collect()
```

`hybrid_search.py`, `embed_search.py`, `reranker.py` und `tools.py` nutzen alle diesen Manager. Keine direkten `SentenceTransformer(...)`-Aufrufe mehr im Suchcode.

#### Schicht 2: ChromaDB LRU-Cache pro Domain

Jede Domain-DB nutzt LRU-Caching:

```python
def get_chroma_client(domain: str) -> chromadb.PersistentClient:
    """Get cached PersistentClient for a domain's isolated ChromaDB."""
    if domain not in _chroma_clients:
        db_path = CHROMA_DIR / domain / "chroma"
        _chroma_clients[domain] = chromadb.PersistentClient(
            path=str(db_path),
            settings=Settings(
                chroma_segment_cache_policy="LRU",
                chroma_memory_limit_bytes=2 * 1024 * 1024 * 1024,  # 2GB pro Domain
            )
        )
    return _chroma_clients[domain]
```

Auswirkung:

- Jede Domain hat maximal 2 GB RAM-Budget.
- Wenn eine Collection lange nicht genutzt wird, entlädt Chroma sie automatisch.
- Wenn der Server domain-scoped ist (Abschnitt 2), gibt es nur einen Client → nur eine Domain belegt RAM.

#### Schicht 3: BM25-Cache-Eviction

```python
# bm25_search.py — aktuell:
_bm25_cache: dict[str, dict] = {}  # wächst für immer

# Neu: mit Größenlimit und LRU
from collections import OrderedDict
_bm25_cache: OrderedDict[str, dict] = {}
_BM25_CACHE_MAX = 3  # max 3 Domains gleichzeitig im RAM

def _load_index(domain: str) -> dict:
    if domain in _bm25_cache:
        _bm25_cache.move_to_end(domain)  # LRU-Update
        return _bm25_cache[domain]
    # ... load from disk ...
    _bm25_cache[domain] = data
    if len(_bm25_cache) > _BM25_CACHE_MAX:
        _bm25_cache.popitem(last=False)  # evict oldest
    return data
```

Mit `model_manager.unload_domain(domain)` kann der MCP-Server gezielt eine Domain entladen.

### RAM-Bilanz (geschätzt, M1 Max 32 GB)

| Komponente | RAM wenn aktiv | RAM wenn entladen |
|---|---|---|
| Embedder (MPNet) | ~420 MB | 0 (del + gc) |
| Cross-Encoder | ~130 MB | 0 (del + gc) |
| BM25-Index (pro Domain) | ~5-10 MB | 0 |
| ChromaDB Collection (pro Domain) | ~200-500 MB | 0 (LRU-evicted) |
| MCP-Server-Prozess | ~50 MB | — |

- **Worst Case (1 Domain aktiv):** ~860 MB-1 GB
- **Zwei Server-Prozesse (Godot + DaVinci parallel):** ~1,7-2 GB
- **32 GB MacBook:** problemlos, genug Luft für DaVinci Resolve Studio, OBS, OpenCode etc.

### Was explizit NICHT gemacht wird

- Keine automatische Inaktivitäts-Erkennung mit Timern (zu komplex, YAGNI).
- Keine GPU-Offloading (M1 Max nutzt CPU für sentence-transformers standardmäßig).
- Keine Modell-Quantisierung (zu viel Engineering für ~420 MB Ersparnis).

## Abschnitt 4: PDF-Parser für DaVinci-Resolve-Dokumentation

> **WICHTIG — Lizenz-Thematik:** Dieser Abschnitt dokumentiert die Trennung zwischen AGPL-lizenziertem Build-Tool und MIT-lizenziertem Runtime-Code. Siehe separaten Abschnitt "Lizenz-Thematik" unten für die vollständige rechtliche Begründung.

### Quellen für die DaVinci-Domain

| Quelle | Typ | Geschätzte Größe |
|---|---|---|
| DaVinci Resolve 20 Reference Manual (4234 Seiten) | PDF | ~40-60 MB |
| DaVinci Resolve 21 New Features Guide | PDF | ~5-10 MB |
| DaVinci Resolve 20 Editor's Guide | PDF | ~20-30 MB |
| DaVinci Resolve 20 Colorist Guide | PDF | ~20-30 MB |
| DaVinci Resolve 20 Fairlight Audio Guide | PDF | ~20-30 MB |
| DaVinci Resolve 20 Visual Effects Guide (Fusion) | PDF | ~20-30 MB |
| DaVinci Resolve 20 Beginner's Guide | PDF | ~15-25 MB |

### Lizenz-Thematik (AGPL vs. MIT)

**Situation:**

- Knowledge-Hub: MIT-Lizenz, öffentlich auf GitHub (https://github.com/DerKellerBlock/knowledge-hub).
- PyMuPDF + PyMuPDF4LLM: AGPL-3.0 (oder kommerzielle Lizenz von Artifex).

**Problem:** AGPL-3.0 ist ein starkes Copyleft. Wenn `import pymupdf` im MIT-lizenzierten Code erfolgt, entsteht ein abgeleitetes Werk. Die gesamte kombinierte Software müsste unter AGPL-3.0 stehen, nicht MIT. Artifex sagt explizit: *"You cannot deploy our open-source as part of a server-based application or service, without disclosing your own application's full source code under AGPL."*

**Lösung: Process Boundary.** Wenn ein Programm via `subprocess` / separatem Script-Aufruf aufgerufen wird (nicht via `import`), gelten beide als separate Werke. Das ist der gleiche Grund, warum GCC (GPL-lizenziert) aus proprietären Build-Systemen aufgerufen werden darf.

**Konkret:**

```
Build-Zeit (manuell, selten):
  PDF-Datei
    ↓ python scripts/parse_pdf_to_markdown.py  ← importiert pymupdf4llm (AGPL)
    ↓ → domains/davinci_resolve/sources/<name>.md

Index-Zeit (embed_index.py):
  domains/davinci_resolve/sources/*.md          ← liest nur Markdown (MIT-kompatibel)
    ↓ embed_index.py                             ← importiert KEIN pymupdf
    ↓ → ChromaDB + BM25

Query-Zeit (MCP-Server):
  search_knowledge(domain="davinci_resolve")    ← importiert KEIN pymupdf
    ↓ hybrid_search.py
    ↓ → Ergebnisse
```

**Bedeutung:**

1. `scripts/parse_pdf_to_markdown.py` — ein eigenständiges Script, das PyMuPDF4LLM importiert. Dieses eine File steht unter AGPL-3.0. Es ist ein Build-Tool, kein Teil des MCP-Servers.
2. `embed_index.py`, `hybrid_search.py`, `mcp_servers/` — importieren niemals pymupdf. Sie lesen nur fertige `.md`-Dateien aus `sources/`. Bleiben MIT-lizenziert.
3. Die PDFs werden einmalig vor dem Index-Bau konvertiert und als Markdown abgelegt. Danach braucht niemand mehr PyMuPDF.
4. `requirements.txt` wird gesplittet:
   - `requirements.txt` (MIT-Runtime): chromadb, sentence-transformers, mcp, rank-bm25 — kein pymupdf.
   - `requirements-pdf.txt` (AGPL-Build-Tool): pymupdf, pymupdf4llm — nur für PDF-Konvertierung.

**Lizenz-Dateien im Repo:**

- `LICENSE` — bleibt MIT (für den Hauptcode).
- `scripts/parse_pdf_to_markdown.py` Header — AGPL-3.0 Notice für dieses File.
- `THIRD_PARTY_LICENSES.md` — listet PyMuPDF/PyMuPDF4LLM AGPL + Artifex Copyright auf.

**Dies ist im Spec und in der Projektdokumentation verbindlich festzuhalten. Keine Ausnahme.**

### Konvertierungs-Pipeline

```
PDF-Datei
  ↓ Phase 1: PyMuPDF4LLM.to_markdown()
  ↓   → Sauberes Markdown mit Headings, Tabellen, Lesereihenfolge
  ↓   → PyMuPDF.get_toc() für hierarchische Kapitelstruktur
  ↓ Phase 2: Section-Aware Chunking (im embed_index.py, analog Godot-RST-Parser)
  ↓   → Markdown-Headings als Section-Boundaries
  ↓   → Recursive Split falls Section zu lang (>1000 Tokens)
  ↓   → 100-Token Overlap zwischen Chunks
  ↓ Chunk-Objekte mit Metadaten
  ↓ embed_index.py → ChromaDB + BM25
```

### parse_pdf_to_markdown.py (AGPL-Build-Script)

```python
# scripts/parse_pdf_to_markdown.py
# SPDX-License-Identifier: AGPL-3.0-or-later
# This script imports PyMuPDF4LLM (AGPL-3.0, Artifex Software).
# It is a standalone build tool, NOT part of the MIT-licensed runtime.
# See THIRD_PARTY_LICENSES.md.

import argparse
from pathlib import Path
import pymupdf          # AGPL
import pymupdf4llm      # AGPL

def convert_pdf(pdf_path: Path, out_path: Path) -> None:
    """Convert a PDF to section-aware Markdown."""
    # Phase 1a: Markdown-Extraktion
    md_text = pymupdf4llm.to_markdown(str(pdf_path))

    # Phase 1b: TOC für Hierarchie (optional, für Metadaten)
    doc = pymupdf.open(str(pdf_path))
    toc = doc.get_toc()  # [[level, title, page], ...]

    # TODO: Markdown + TOC-Metadaten zusammenführen
    # → Output: saubere .md-Datei mit Heading-Struktur

    out_path.write_text(md_text, encoding="utf-8")
    print(f"[OK] {pdf_path.name} → {out_path.name} ({len(md_text)} chars)")

def main():
    parser = argparse.ArgumentParser(description="PDF → Markdown (AGPL build tool)")
    parser.add_argument("--pdf", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    convert_pdf(args.pdf, args.out)

if __name__ == "__main__":
    main()
```

### Chunk-Struktur mit Metadaten

Jeder Chunk bekommt:

```python
Chunk(
    chunk_id="davinci_resolve::edit::transform_clips::0",
    text="To transform clips on the Edit page, use the Inspector...",
    source_type="repo",
    source_file="davinci-resolve-20-reference-manual.md",
    chunk_type="section",
    class_name="Edit",          # Resolve-Page als "class"-Äquivalent
    name="Transform Clips",
    signature=None,             # keine Signature wie bei Godot
    inherits_from=["Edit", "Editing"],  # hierarchischer Pfad
    line_start=0,               # wird auf page_start gemappt
    line_end=0,
    page_start=423,             # PDF-Seite (aus TOC oder page_chunks)
    page_end=425,
    section_path="Part 5 > Edit > Transform Clips",  # menschenlesbarer Pfad
)
```

### Wichtige Designentscheidungen

1. **Section-basiert, nicht page-basiert:** Ein Abschnitt wie "Color > Primary Color Correction" kann 5 Seiten umfassen. Ein Chunk pro Abschnitt (mit Recursive-Split wenn >1000 Tokens), nicht ein Chunk pro Seite. So bleibt der semantische Kontext erhalten.
2. **Page-Number in Metadaten:** Jeder Chunk weiß, auf welchen PDF-Seiten er liegt. Das ist essenziell für das Lernziel — die KI kann antworten: *"Das findest du im Reference Manual auf Seite 423-425, Part 5 > Edit > Transform Clips."*
3. **PyMuPDF4LLM statt Font-Size-Heuristik:** PyMuPDF4LLM liefert sauberes Markdown mit `#`/`##`/`###`-Headings. Das ist robuster als eigene Font-Size-Heuristik und wird von den PyMuPDF-Experten gepflegt.
4. **TOC als zusätzliche Hierarchie-Quelle:** `doc.get_toc()` liefert die echte Blackmagic-Kapitelstruktur mit Seitenzahlen. Kombiniert mit Markdown-Headings für Fein-Struktur. Fallback auf reine Markdown-Heading-Erkennung falls TOC fehlt.

### Neue Abhängigkeiten

```
# requirements-pdf.txt (NEU — AGPL-Build-Tool)
PyMuPDF>=1.24.0,<2.0.0
pymupdf4llm>=0.0.17,<1.0.0
```

```
# requirements.txt (ANGEPASST — kein pymupdf!)
chromadb>=0.5.0
sentence-transformers>=2.7.0
mcp>=1.0.0
rank-bm25>=0.2.2
# WICHTIG: pymupdf/pymupdf4llm NICHT hier — siehe requirements-pdf.txt
```

### Workflow für eine neue DaVinci-Quelle

```bash
# 1. PDF herunterladen
cp ~/Downloads/davinci-resolve-20-reference-manual.pdf \
   domains/davinci_resolve/sources/raw/

# 2. PDF → Markdown konvertieren (AGPL-Tool, einmalig)
pip install -r requirements-pdf.txt  # falls noch nicht geschehen
python scripts/parse_pdf_to_markdown.py \
  --pdf domains/davinci_resolve/sources/raw/davinci-resolve-20-reference-manual.pdf \
  --out domains/davinci_resolve/sources/davinci-resolve-20-reference-manual.md

# 3. Index bauen (MIT-Code, liest .md)
python scripts/embed_index.py --domain davinci_resolve

# 4. Fertig — MCP-Server kann suchen
```

## Abschnitt 5: Migration der bestehenden Godot-Domain

### Was sich am Pfad ändert

```
Vorher:
  chromadb_data/
    godot_knowledge/          # Collection-Ordner
    godot_bm25.pkl            # BM25-Index

Nachher:
  chromadb_data/
    godot/
      chroma/                 # PersistentClient für Godot
        godot_knowledge/      # gleiche Collection, neuer Ort
      godot_bm25.pkl          # gleiche Datei, neuer Ort
    davinci_resolve/
      chroma/
        davinci_resolve_knowledge/
      davinci_resolve_bm25.pkl
```

### Migrations-Strategie — dreistufig

#### Stufe 1: Automatische Migration beim Start

`embed_index.py` und der MCP-Server erkennen beim Start den alten Pfad und migrieren automatisch:

```python
# scripts/migration.py (neu)
def migrate_legacy_layout():
    """Migrate chromadb_data/godot_knowledge → chromadb_data/godot/chroma/godot_knowledge."""
    legacy_collection = CHROMA_DIR / "godot_knowledge"
    legacy_bm25 = CHROMA_DIR / "godot_bm25.pkl"

    if not legacy_collection.exists():
        return  # nichts zu migrieren

    new_dir = CHROMA_DIR / "godot" / "chroma"
    new_dir.mkdir(parents=True, exist_ok=True)

    # Collection verschieben
    shutil.move(str(legacy_collection), str(new_dir / "godot_knowledge"))

    # BM25 verschieben
    if legacy_bm25.exists():
        shutil.move(str(legacy_bm25), str(CHROMA_DIR / "godot" / "godot_bm25.pkl"))

    print("[MIGRATION] Godot-Index nach chromadb_data/godot/chroma/ verschoben")
```

#### Stufe 2: Backup vor Migration

Bevor etwas verschoben wird, legt der Migrator ein Backup an:

```python
def migrate_legacy_layout():
    legacy_collection = CHROMA_DIR / "godot_knowledge"
    if not legacy_collection.exists():
        return

    # Backup
    backup = CHROMA_DIR / "_legacy_backup"
    backup.mkdir(exist_ok=True)
    shutil.copytree(str(legacy_collection), str(backup / "godot_knowledge"))
```

Falls etwas schiefgeht, kann der Nutzer zurückkehren.

#### Stufe 3: Idempotenz

Die Migration läuft nur, wenn das alte Layout existiert und das neue noch nicht. Wenn bereits `chromadb_data/godot/chroma/` existiert, passiert nichts.

### Was mit nak-hopper-game passiert

Da `nak-hopper-game` den MCP-Server aus `knowledge-hub/.venv` startet, läuft die Migration beim nächsten Server-Start automatisch. Danach ist der Godot-Index am neuen Ort und alles funktioniert weiter.

### Risiko-Minderung

- Migration ist reine Datei-Verschiebung, kein Re-Embedding.
- Backup wird angelegt.
- `nak-hopper-game` muss nicht angefasst werden — nur `knowledge-hub` aktualisieren.
- Falls die Migration fehlschlägt: Nutzer kann Backup zurückkopieren und alten Code verwenden.

## Abschnitt 6: DaVinci-Domain-Setup und Einbindung ins Video-Blog-Projekt

### Domain-Ordner-Struktur

```
domains/
  godot/                          # bestehend
    domain.md
    sources/
    personal/
  davinci_resolve/                # neu
    domain.md
    sources/
      davinci-resolve-20-reference-manual.md      # aus PDF konvertiert
      davinci-resolve-21-new-features-guide.md
      davinci-resolve-20-editors-guide.md
      davinci-resolve-20-colorist-guide.md
      davinci-resolve-20-fairlight-audio-guide.md
      davinci-resolve-20-fusion-visual-effects.md
      davinci-resolve-20-beginners-guide.md
      raw/                                          # gitignored, Original-PDFs
        davinci-resolve-20-reference-manual.pdf
        ...
    personal/
      ui-map.md                    # "Wo finde ich was" — Lernkarte
      beginner-questions.md         # Fragen und Antworten
      gotchas.md                    # Fallen und Workarounds
      workflow-notes.md             # Eigene Reel-Workflows
```

### domain.md für DaVinci

```markdown
# Domain: davinci_resolve

## Zweck
Wissen für Videoschnitt-Produktion mit DaVinci Resolve Studio 21.
Fokus: Wo finde ich Werkzeuge in der UI, wie produziere ich erfolgreich Videos.
Deckt: Cut, Edit, Color, Fairlight, Fusion, Deliver, Photo (ab Resolve 21).

## Quellen (Repo-Wissen)
| Name | Datei | Ursprung | Konvertiert am |
|------|-------|----------|---------------|
| Resolve 20 Reference Manual | sources/davinci-resolve-20-reference-manual.md | Blackmagic PDF | 2026-06-27 |
| Resolve 21 New Features Guide | sources/davinci-resolve-21-new-features-guide.md | Blackmagic PDF | 2026-06-27 |
| Resolve 20 Editor's Guide | sources/davinci-resolve-20-editors-guide.md | Blackmagic PDF | 2026-06-27 |
| Resolve 20 Colorist Guide | sources/davinci-resolve-20-colorist-guide.md | Blackmagic PDF | 2026-06-27 |
| Resolve 20 Fairlight Audio Guide | sources/davinci-resolve-20-fairlight-audio-guide.md | Blackmagic PDF | 2026-06-27 |
| Resolve 20 Visual Effects Guide | sources/davinci-resolve-20-fusion-visual-effects.md | Blackmagic PDF | 2026-06-27 |
| Resolve 20 Beginner's Guide | sources/davinci-resolve-20-beginners-guide.md | Blackmagic PDF | 2026-06-27 |

## Persönliches Wissen
| Datei | Beschreibung |
|-------|-------------|
| personal/ui-map.md | UI-Lernkarte: Page → Panel → Aktion |
| personal/beginner-questions.md | Anfängerfragen und Antworten |
| personal/gotchas.md | Fallen, Bugs, Workarounds |
| personal/workflow-notes.md | Eigene Reel-Produktions-Workflows |

## Metadaten
- Embedding-Model: all-mpnet-base-v2 (768 dims)
- Collection: davinci_resolve_knowledge
- ChromaDB-Path: chromadb_data/davinci_resolve/chroma/
- BM25-Path: chromadb_data/davinci_resolve/davinci_resolve_bm25.pkl
- Letztes Update: 2026-06-27

## Lizenz-Hinweis
Quelldokumente © Blackmagic Design. Ursprüngliche PDFs in sources/raw/ (gitignored).
Konvertierte Markdown-Dateien sind interne Arbeitsprodukte, nicht zur Weitergabe.
PyMuPDF/PyMuPDF4LLM (AGPL-3.0) wird nur im Build-Script verwendet, nicht im Runtime-Code.
Siehe THIRD_PARTY_LICENSES.md und docs/decisions/.
```

### .gitignore für sources/raw/

```
# domains/*/sources/raw/ — Original-PDFs, zu gross für Git
domains/*/sources/raw/
```

### Einbindung in den Video-Blog-Workspace

`video-blog/meta/.opencode/opencode.json` bekommt einen neuen MCP-Server-Eintrag (siehe Abschnitt 2).

### Aktualisierung von nak-hopper-game

`nak-hopper-game/.opencode/opencode.json` wird angepasst auf `--domains godot` (siehe Abschnitt 2).

### Beide parallel

Wenn beide Workspaces gleichzeitig offen sind, laufen zwei MCP-Prozesse:

```
Prozess 1 (nak-hopper-game): --domains godot        → ~860 MB RAM
Prozess 2 (video-blog):       --domains davinci_resolve → ~860 MB RAM
Gesamt:                                              → ~1,7 GB RAM
```

Mit 32 GB RAM kein Problem, selbst wenn DaVinci Resolve Studio und OBS gleichzeitig laufen.

### Wie das Lernen dann aussieht

Im Video-Blog-Workspace kann Noah fragen:

> *"Ich will einen Clip auf der Edit-Page trimmen. Wo finde ich das und wie mache ich es?"*

Der Agent nutzt `search_knowledge(domain="davinci_resolve", query="trim clip edit page", mode="hybrid")` und bekommt:

- Den relevanten Abschnitt aus dem Reference Manual
- Die Seitenzahl (z.B. "Reference Manual S. 423-425, Part 5 > Edit > Trimming Clips")
- Falls vorhanden: eigene Notizen aus `personal/ui-map.md`

Dann antwortet der Agent:

> *"Auf der Edit-Page findest du das Trim-Tool links in der Toolbar. ... Das steht im Reference Manual auf Seite 423-425. Du kannst auch [Shortcut] nutzen."*

## Abschnitt 7: Testing, Validierung, Fehlerbehandlung

### Testing-Strategie

Da der Knowledge-Hub keine Godot-GUT-Tests hat, nutzen wir eine eigene QA-Checkliste, die zum Workspace-Pattern passt.

#### Ebene 1 — Syntax & Struktur

```bash
# Bash-Syntax check
bash -n scripts/parse_pdf_to_markdown.sh

# Python-Syntax check
python3 -m py_compile scripts/model_manager.py
python3 -m py_compile scripts/migration.py
python3 -m py_compile scripts/parse_pdf_to_markdown.py
python3 -m py_compile mcp_servers/knowledge_hub/server.py

# JSON validierung
python3 -m json.tool video-blog/meta/.opencode/opencode.json
python3 -m json.tool nak-hopper-game/.opencode/opencode.json
```

#### Ebene 2 — Integrationstests (manuell, im Spec dokumentiert)

| Test | Was wird geprüft | Erfolgskriterium |
|---|---|---|
| Godot-Migration | Alte Struktur → neue Struktur | Index durchsuchbar, gleiche Ergebnisse |
| Domain-Scoping `--domains godot` | Server ignoriert davinci_resolve | `search(davinci_resolve)` → Fehler |
| Domain-Scoping `--domains davinci_resolve` | Server ignoriert godot | `search(godot)` → Fehler |
| Lazy Loading | RSS-Speicher vor/nach Suche | Modelle laden nur bei Suche |
| PDF-Konvertierung | PDF → Markdown | Section-Headings erkennbar, TOC korrekt |
| DaVinci-Index | Markdown → ChromaDB | `search("trim clip edit")` liefert Ergebnis mit Page-Number |
| Beide Server parallel | RAM-Messung | < 2,5 GB für beide Prozesse zusammen |

#### Ebene 3 — Regressionstests (Skript)

Ein neues Script `scripts/validate_search.py`, das nach jeder Änderung läuft:

```bash
python scripts/validate_search.py --domain godot --query "Node3D rotate" --expected-min-results 1
python scripts/validate_search.py --domain davinci_resolve --query "trim clip edit" --expected-min-results 1
```

Es prüft:

- Suchergebnisse kommen zurück
- `total_found > 0`
- Query-Zeit < 5 Sekunden
- Metadaten vorhanden (source_file, page_start, section_path)

### Fehlerbehandlung

**PDF-Konvertierung schlägt fehl:**

- `parse_pdf_to_markdown.py` fängt `pymupdf`-Exceptions ab.
- Gibt klare Fehlermeldung: "PDF konnte nicht konvertiert werden: <Grund>".
- Bricht ab, ohne partielle Markdown-Datei zu hinterlassen.
- Exit-Code 1, damit CI/Build-Skripte es bemerken.

**Migration schlägt fehl:**

- Backup bleibt erhalten.
- Alte Struktur wird nicht gelöscht bis Migration bestätigt.
- Fehlermeldung sagt explizit: "Backup in chromadb_data/_legacy_backup/, alte Struktur intakt".

**Domain-Scoping — ungültige Domain:**

- Server startet nicht, wenn `--domains foobar` angegeben wird und `domains/foobar/` nicht existiert.
- Klare Fehlermeldung: "Domain 'foobar' nicht gefunden. Verfügbare Domains: godot, davinci_resolve".

**Modell-Laden schlägt fehl:**

- `model_manager.get_embedder()` fängt Exceptions ab.
- Gibt klare Meldung: "Embedding-Modell konnte nicht geladen werden. Prüfe requirements.txt und Modell-Cache."
- Suche schlägt graceful fehl, statt den MCP-Server zum Absturz zu bringen.

**ChromaDB-LRU-Eviction:**

- Wenn RAM-Limit erreicht wird, entlädt ChromaDB automatisch die am wenigsten genutzte Collection.
- Das ist transparent — die nächste Suche lädt die Collection wieder.
- Kein Fehler, nur leicht erhöhte Latenz bei Wiederladung.

### Datei- und Code-Organisation

```
knowledge-hub/
  scripts/
    parse_pdf_to_markdown.py    # NEU (AGPL — importiert pymupdf4llm)
    migration.py                # NEU (MIT — Datei-Verschiebung)
    model_manager.py            # NEU (MIT — zentraler Model-Cache)
    validate_search.py          # NEU (MIT — Regressionstest)
    embed_search.py             # ANGEPASST (nutzt model_manager)
    bm25_search.py              # ANGEPASST (LRU-Cache, Per-Domain-Pfade)
    hybrid_search.py            # ANGEPASST (nutzt model_manager, Per-Domain-Clients)
    reranker.py                 # ANGEPASST (nutzt model_manager)
    embed_index.py              # ANGEPASST (Per-Domain-ChromaDB-Pfade)
  mcp_servers/knowledge_hub/
    server.py                   # ANGEPASST (--domains CLI-Flag, Scoping-Logik)
    config.py                   # ANGEPASST (Per-Domain-Konfiguration)
    tools.py                    # ANGEPASST (nutzt model_manager)
  domains/
    godot/                      # bestehend
    davinci_resolve/            # NEU
  chromadb_data/
    godot/                      # NEU (migriert aus alter Struktur)
    davinci_resolve/            # NEU
  requirements.txt              # ANGEPASST (kein pymupdf)
  requirements-pdf.txt          # NEU (pymupdf, pymupdf4llm — AGPL-Build-Tool)
  THIRD_PARTY_LICENSES.md        # NEU
  LICENSE                       # bleibt MIT
```

### Was bewusst NICHT gemacht wird

- Keine automatischen CI-Tests in GitHub Actions (YAGNI für aktuelle Phase).
- Keine Performance-Benchmarks mit festen Schwellwerten (zu variabel).
- Keine automatische Inaktivitäts-Erkennung mit Timern.
- Keine Modell-Quantisierung.
- Keine GPU-Offloading.
- Keine Web-UI für den Knowledge-Hub.

## Entscheidungs-Tabelle

| # | Abschnitt | Kern-Entscheidung |
|---|---|---|
| 1 | Per-Domain ChromaDB-Isolation | Jede Domain bekommt eigene DB + eigenen PersistentClient |
| 2 | Domain-Scoped MCP-Server | `--domains` CLI-Flag / Env-Var begrenzt sichtbare Domains |
| 3 | Memory Management | Zentraler Model-Manager, LRU-Cache, BM25-Cache-Eviction |
| 4 | PDF-Parser | PyMuPDF4LLM im separaten Build-Script (AGPL Process Boundary) |
| 5 | Migration | Automatische Godot-Index-Migration mit Backup |
| 6 | DaVinci-Domain | 7 Quellen, domain.md, Video-Blog-Einbindung |
| 7 | Testing & Fehler | QA-Checkliste, Regression-Script, graceful Errors |

## Offene Punkte / TODOs

- [ ] Prüfen, ob das Indexieren und interne Nutzen der Blackmagic-PDFs zulässig ist (Lizenz der Quelldokumente). Aktuelle Annahme: interne Nutzung okay, keine Weitergabe der konvertierten Markdowns. Vor dem Index-Bau klären.
- [ ] DaVinci Resolve 21 Reference Manual: aktuell nur "New Features Guide" verfügbar. Vollständiges Reference Manual kommt laut Blackmagic "nach dem Public Beta". Nachtrag indexieren, sobald verfügbar.
- [ ] `parse_pdf_to_markdown.py`: detaillierte Implementierung von TOC + Markdown-Heading-Zusammenführung. Im Spec nur skizziert.
- [ ] Domain-Config-Leser für `domain.md` Metadaten-Felder (`get_domain_config(domain)` in model_manager.py). Im Spec nur skizziert.

## Referenzen

- Knowledge-Hub bestehend: `docs/superpowers/specs/2026-06-09-knowledge-hub-design.md`
- Retrieval 2.0: `docs/superpowers/specs/2026-06-09-retrieval-2-0-design.md`
- Video-Blog Workspace: `/Users/noahk/Documents/work/video-blog/meta/AGENTS.md`
- PyMuPDF: https://github.com/pymupdf/PyMuPDF (AGPL-3.0)
- PyMuPDF4LLM: https://github.com/pymupdf/pymupdf4llm (AGPL-3.0)
- Artifex Licensing: https://artifex.com/licensing
- ChromaDB Memory Management: https://cookbook.chromadb.dev/strategies/memory-management/
- ChromaDB Chunking Guide: https://docs.trychroma.com/guides/build/chunking
- DaVinci Resolve 21 New Features Guide: https://documents.blackmagicdesign.com/SupportNotes/DaVinci_Resolve_21_New_Features_Guide.pdf
- DaVinci Resolve 20 Reference Manual (via elements.tv Zusammenfassung): https://elements.tv/blog/davinci-resolve-20-reference-manual/
