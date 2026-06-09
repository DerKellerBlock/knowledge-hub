# Knowledge Hub — Design Spec

> **Status:** Entscheidungen getroffen (Q1-Q5) | **Datum:** 2026-06-09 | **Autor:** Orchestrator + Noah
>
> Abgeleitet aus: `docs/ai/knowledge-skills-review-2026-06-09.md` und Nutzer-Feedback

## Vision

Ein **domain-agnostischer, persönlicher Knowledge Hub**, der mehrere Wissensdomains (Godot, Blender, DaVinci Resolve, FreeCAD, …) unter einem Dach vereint. Er kombiniert **Repo-Wissen** (automatisch aus Dokumentationen und Code-Repos gescraped via repomix) mit **persönlichem Erfahrungswissen** (FAQs, Best Practices, „hat funktioniert / hat nicht funktioniert") des Nutzers Noah.

Der Hub ist:
- **Single Source of Truth:** Alles Wissen lebt hier. Andere Projekte (z.B. `nak-hopper-game`) konsumieren via MCP oder installieren Skills via `install.sh`.
- **Modular:** Jede Domain ist ein Plug-in — neue Domains werden ohne Refactor hinzugefügt.
- **Agent-wartbar:** OpenCode + Subagents können das Hub-Repo selbstständig pflegen, erweitern und aktualisieren.
- **Selbstdokumentierend:** Das gleiche `docs/`-Pattern wie `nak-hopper-game` — mit AI-Readme, Specs, Plans, Architecture-Docs.
- **Suchbar:** Exakte Suche (ripgrep) + semantische Suche (ChromaDB-Embeddings) + Hybrid-Fusion, querybar via MCP-Server oder CLI.
- **Installierbar:** Andere Projekte können die Skills via `./install.sh <project-path>` oder `skill install` einbinden. Ziel: GitHub Public Repo.

## Motivation

- **Bisher:** Godot-Wissen lebt nur im Spiel-Projekt (`nak-hopper-game/.agents/skills/`). Für Blender, Resolve oder FreeCAD müsste alles dupliziert werden.
- **Problem:** Kein zentraler Ort für Noahs persönliches Wissen („In Godot 4.6 hatte ich Bug X, Workaround Y"). Das Wissen existiert nur im Kopf oder verstreut in Chat-Verläufen.
- **Ziel:** Ein Repo, das Noahs **komplettes technisches Wissen** bündelt — strukturiert, durchsuchbar, versioniert, von AI-Agenten nutzbar, als Open-Source-Skill installierbar.

## Architektur-Übersicht

```
┌─────────────────────────────────────────────────────────────┐
│                     Knowledge Hub                            │
│                                                               │
│  .agents/skills/     ← OpenCode Skills (Single Source)       │
│  └── godot/          ← Godot-Knowledge-Skills               │
│      ├── SKILL.md                                          │
│      └── references/*-packed.md                            │
│                                                               │
│  domains/                                                     │
│  ├── godot/           ← erste Domain (live)                  │
│  │   ├── sources/     ← repomix-packed files (Rohdaten)     │
│  │   ├── personal/    ← Noahs FAQs, Gotchas, Tips           │
│  │   ├── domain.md    ← Domain-Konfiguration                │
│  │   └── scripts/     ← Domain-CLI (update, search)         │
│  ├── blender/         ← später                               │
│  ├── resolve/         ← später                               │
│  └── freecad/         ← später                               │
│                                                               │
│  scripts/             ← Generische Infrastruktur              │
│  ├── embed_index.py   ← Chunking + Embedding → ChromaDB     │
│  ├── embed_search.py  ← Semantische Query                   │
│  └── hybrid_search.py ← Fusion ripgrep + Embeddings         │
│                                                               │
│  mcp_servers/                                               │
│  └── knowledge_hub/    ← MCP-Server (ein Server, alle Domains)│
│      ├── server.py                                          │
│      └── tools.py                                           │
│                                                               │
│  install.sh            ← Installiert Hub-Skills in Projekte   │
│  chromadb_data/        ← Index (.gitignored, ~80-120 MB)     │
│  personal/             ← Domain-übergreifende Notizen        │
│                                                               │
│  docs/                 ← Agent-Doku (Pattern: nak-hopper-game)│
│  ├── ai/                                                     │
│  ├── domains/          ← Pro Domain: Quellen, Patterns       │
│  └── superpowers/      ← Specs, Plans                        │
│                                                               │
│  requirements.txt      ← Python-Dependencies                 │
│  README.md             ← Einstieg für Menschen + AI-Agenten   │
└─────────────────────────────────────────────────────────────┘
```

### Wie andere Projekte den Hub konsumieren

```
knowledge-hub/                     (Single Source of Truth)
    │
    ├── MCP-Server ────────────────→ nak-hopper-game/ (via OpenCode MCP-Tools)
    │
    └── install.sh ────────────────→ blender-project/  (kopiert .agents/skills/)
                   ────────────────→ new-godot-game/   (kopiert .agents/skills/)
```

**`install.sh` Konzept:**
```bash
#!/usr/bin/env bash
# Installiert die Knowledge-Hub-Skills in ein anderes Projekt.
#
# Usage:
#   ./install.sh /path/to/project           # alle Domains
#   ./install.sh /path/to/project godot      # nur godot
#   ./install.sh /path/to/project --symlink  # Symlinks statt Kopien (dev)
```

## Domain-Modell

Jede Domain ist ein **autarkes Modul** mit eigener Konfiguration:

```
domains/<name>/
├── domain.md              # Konfiguration (siehe unten)
├── sources/               # Repomix-Packed-Files (*-packed.md)
├── personal/              # Noahs persönliches Wissen (*.md)
│   ├── faq.md             # Häufige Fragen + Antworten
│   ├── gotchas.md         # "Hat nicht funktioniert" + Workarounds
│   ├── best-practices.md  # Bewährte Patterns
│   └── tips.md            # Kurze Tipps & Tricks
└── scripts/               # Domain-spezifische CLI
    ├── update.sh           # Repomix-Update für diese Domain
    ├── search.sh           # ripgrep-Suche in dieser Domain
    └── status.sh           # Status dieser Domain
```

**`domain.md` Konfiguration:**
```markdown
# Domain: godot

## Quellen (Repo-Wissen)
| Name | Repo URL | Include Pattern | Ignore Pattern | Update |
|------|----------|-----------------|-----------------|--------|
| godot-docs | https://github.com/godotengine/godot-docs | `classes/*.rst,getting_started/**/*.rst` | `**/*.png,**/*.jpg` | wöchentlich |
| godot-demo-projects | https://github.com/godotengine/godot-demo-projects | `**/*.gd` | `**/*.import` | wöchentlich |

## Persönliches Wissen
| Datei | Beschreibung | Gepflegt von |
|-------|-------------|-------------|
| personal/faq.md | Häufige Godot-Fragen | Noah |
| personal/gotchas.md | Fehler + Workarounds | Noah + Agent |
| personal/best-practices.md | Bewährte Patterns | Noah |

## Aktueller Stand
- Letztes Update: 2026-06-09
- Embedding-Model: all-mpnet-base-v2 (768 dims)
- ChromaDB-Collection: `godot_knowledge` (~15.000 Chunks, ~80 MB)
```

## Datenquellen: Zwei Wissenstypen

### Typ A: Repo-Wissen (automatisch)

| Eigenschaft | Wert |
|-------------|------|
| **Quelle** | Git-Repos (godot-docs, godot-demo-projects, …) |
| **Format** | Generiert via `repomix --remote` → `sources/<name>-packed.md` |
| **Update** | Wöchentlich per Script (später: GitHub Action) |
| **Metadaten** | `source_type: "repo"`, `domain`, `source_name`, `commit_hash`, `updated_at` |
| **Lebenszyklus** | Wird bei jedem Update **komplett überschrieben** |

### Typ B: Persönliches Wissen (kumulativ)

| Eigenschaft | Wert |
|-------------|------|
| **Quelle** | Noahs Markdown-Dateien (`personal/*.md`) |
| **Format** | Strukturierte Markdown mit `##`-Headern pro Topic |
| **Update** | Manuell (Noah) oder per Agent („Füge diesen Workaround zu gotchas.md hinzu") |
| **Metadaten** | `source_type: "personal"`, `domain`, `author: "noah"`, `created_at` |
| **Lebenszyklus** | **Wächst kumulativ** — nichts wird überschrieben |

**Beispiel `personal/gotchas.md`:**
```markdown
# Godot Gotchas — Was nicht funktioniert hat

## Jolt Physics + CharacterBody3D
- **Problem:** CharacterBody3D fällt durch den Boden bei Jolt Physics in Godot 4.6
- **Ursache:** `move_and_slide()` ruft `PhysicsServer3D.body_test_motion()` auf, Jolt interpretiert `safe_margin` anders
- **Workaround:** `safe_margin = 0.001` setzen, oder GodotPhysics statt Jolt nutzen
- **Datum:** 2026-06-03
- **Status:** Workaround funktioniert, Bug report offen (GH-12345)

## GLB-Import mit Meshy
- **Problem:** Meshy GLB hat scale 0.01, Modell unsichtbar
- **Workaround:** `auto_size: true` + `origin_at: bottom` in Meshy API-Call
- **Datum:** 2026-06-08
```

## Datenfluss

```
┌──────────────────┐     ┌──────────────────┐
│  Repo-Wissen      │     │  Persönliches     │
│  (repomix)        │     │  Wissen (.md)     │
└────────┬─────────┘     └────────┬─────────┘
         │                        │
         ▼                        ▼
┌──────────────────────────────────────────────┐
│           scripts/embed_index.py              │
│                                                │
│  1. Lies alle sources/*.md + personal/*.md    │
│  2. Chunking: 500 Tokens, 100 Token Overlap   │
│  3. Embedding: all-mpnet-base-v2 (768 dims)   │
│  4. Speichere in ChromaDB                      │
│     - Collection: "<domain>_knowledge"         │
│     - Metadata: source_type, domain, source,   │
│       chunk_id, line_offset                    │
│  5. Collection komplett neu (inkrementell N/A) │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│              chromadb_data/                    │
│  godot_knowledge/ (~15K Chunks, ~80 MB)       │
│  blender_knowledge/ (später)                  │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│         mcp_servers/knowledge_hub/             │
│                                                │
│  Tools:                                        │
│  • search_knowledge(domain, query, mode)       │
│  • get_status(domain?)                         │
│  • update_domain(domain)                       │
│  • add_personal_note(domain, topic, content)   │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
              OpenCode Agent
         „Wie macht man Schwerkraft?"
```

## Sucharchitektur

Drei Modi, ein Interface:

### Modus 1: Exakt (`mode: "exact"`)
- Nutzt **ripgrep** auf den rohen Packed-Files
- Schnell (<100ms), findet nur exakte String-Matches
- Gut für: API-Namen, Klassennamen, exakte Code-Snippets

### Modus 2: Semantisch (`mode: "semantic"`)
- Nutzt **ChromaDB + all-mpnet-base-v2** (768-dim Embeddings)
- Findet konzeptionell ähnliche Inhalte
- Gut für: umschreibende Fragen, „Wie macht man X?", konzeptionelle Suche

### Modus 3: Hybrid (`mode: "hybrid"`, Default)
- Parallele Query: ripgrep + ChromaDB
- Fusion: Reciprocal Rank Fusion (RRF, k=60)
- Deduplizierung: gleiche Chunks mergen, Score addieren
- Ranking: Top-10 Treffer, sortiert nach kombiniertem Score

**API (MCP-Tool):**
```json
{
  "tool": "search_knowledge",
  "params": {
    "domain": "godot",
    "query": "Wie erstelle ich einen 3D-Character-Controller?",
    "mode": "hybrid",
    "max_results": 10,
    "source_filter": ["repo", "personal"]
  }
}
```

**Response:**
```json
{
  "results": [
    {
      "rank": 1,
      "score": 0.94,
      "source_type": "repo",
      "source": "godot-demo-projects",
      "domain": "godot",
      "text": "extends CharacterBody3D\n\nvar speed = 5.0\n...",
      "chunk_id": "godot_demos_3d_character_chunk_0042",
      "match_type": "hybrid"
    },
    {
      "rank": 2,
      "score": 0.87,
      "source_type": "personal",
      "source": "gotchas.md",
      "domain": "godot",
      "text": "## Jolt Physics + CharacterBody3D\n...",
      "chunk_id": "godot_personal_gotchas_chunk_0003",
      "match_type": "semantic"
    }
  ],
  "total_found": 47,
  "query_time_ms": 234
}
```

## Verzeichnisstruktur (vollständig)

```
~/Documents/work/
├── nak-hopper-game/                   # Godot-Spiel (existiert, konsumiert via MCP)
│
└── knowledge-hub/                     # NEU: Single Source of Truth
    │
    ├── README.md                      # Einstieg für Menschen + AI-Agenten
    ├── install.sh                     # Installiert Hub-Skills in andere Projekte
    │
    ├── .agents/skills/                # OpenCode Skills (Single Source of Truth)
    │   └── godot/
    │       ├── SKILL.md
    │       └── references/
    │           ├── godot-docs-reference-packed.md
    │           ├── godot-docs-3d-packed.md
    │           └── godot-demos-packed.md
    │
    ├── docs/                          # Agent-Dokumentation
    │   ├── ai/
    │   │   ├── README.md              # Lese-Reihenfolge für AI-Agenten
    │   │   ├── project-context.md     # Projekt-Übersicht, Setup, Versionen
    │   │   ├── architecture.md        # Architektur, Datenfluss, Komponenten
    │   │   ├── domain-model.md        # Wie Domains funktionieren
    │   │   ├── best-practices.md      # Coding-Standards, Konventionen
    │   │   ├── validation.md          # Verfügbare Checks, Tests
    │   │   └── known-issues.md        # Bekannte Bugs, technische Schulden
    │   ├── domains/
    │   │   ├── godot.md               # Domain-Doku: Quellen, Patterns
    │   │   ├── blender.md             # (später)
    │   │   └── resolve.md             # (später)
    │   └── superpowers/
    │       ├── specs/                 # Design-Specs
    │       └── plans/                 # Implementierungspläne
    │
    ├── domains/                       # Domain-Module (autark)
    │   └── godot/
    │       ├── domain.md              # Konfiguration (Quellen, Patterns)
    │       ├── sources/               # Repomix-Packed-Files (Rohdaten)
    │       │   ├── godot-docs-packed.md
    │       │   ├── godot-demos-packed.md
    │       │   └── .gitkeep
    │       ├── personal/              # Noahs persönliches Wissen
    │       │   ├── faq.md
    │       │   ├── gotchas.md
    │       │   ├── best-practices.md
    │       │   └── tips.md
    │       └── scripts/               # Domain-CLI
    │           ├── update.sh
    │           ├── search.sh
    │           └── status.sh
    │
    ├── scripts/                       # Generische Infrastruktur
    │   ├── embed_index.py             # Chunking + Embedding → ChromaDB
    │   ├── embed_search.py            # Semantische Query
    │   └── hybrid_search.py           # Fusion ripgrep + Embeddings
    │
    ├── mcp_servers/                   # MCP-Server
    │   └── knowledge_hub/
    │       ├── __init__.py
    │       ├── server.py              # MCP-Server (stdio)
    │       ├── tools.py               # Tool-Definitionen
    │       └── config.py              # Konfiguration (Domains, Pfade)
    │
    ├── chromadb_data/                 # ChromaDB-Index (.gitignored)
    │   └── .gitkeep
    │
    ├── personal/                      # Domain-übergreifende Notizen
    │   └── workflow-ideas.md
    │
    ├── requirements.txt               # Python-Dependencies (s.u.)
    ├── .gitignore                     # chromadb_data/, __pycache__, .env
    └── .gitattributes                 # LFS für Packed-Files
```

### Hinweis: `sources/` vs `.agents/skills/`

Die `sources/` enthalten die **Rohdaten** (reine repomix-Outputs). Die `.agents/skills/` enthalten die **Skills** (SKILL.md + references/*-packed.md Kopien). Der Workflow:

1. `domains/godot/scripts/update.sh` → erzeugt `sources/*.md`
2. `domains/godot/scripts/update.sh` → kopiert nach `.agents/skills/godot/references/`
3. `scripts/embed_index.py` → liest `sources/` + `personal/` → indexiert

## Kern-Komponenten

### `scripts/embed_index.py`

```python
"""
Baut ChromaDB-Index aus allen Domain-Quellen.

Usage:
  python scripts/embed_index.py --domain godot
  python scripts/embed_index.py --all

Workflow:
  1. Scan domains/<domain>/sources/*.md + personal/*.md
  2. Chunking: 500 Tokens, 100 Token Overlap
  3. Embedding: all-mpnet-base-v2 (768-dim) via sentence-transformers
  4. Speichern in ChromaDB Collection "<domain>_knowledge"
  5. Alte Collection löschen, neue erstellen (kein inkrementelles Update)

Modell-Hinweis:
  - all-mpnet-base-v2: ~420 MB Download beim ersten pip install
  - Höhere Genauigkeit als MiniLM (~85% vs ~80% semantic search benchmark)
  - Index-Größe: ~80 MB pro Domain (15K Chunks)
  - Index-Zeit: ~5 Min pro Domain (CPU), ~1 Min (GPU/MPS)
"""
```

### `scripts/embed_search.py`

```python
"""
Semantische Query gegen ChromaDB-Index.

Usage:
  python scripts/embed_search.py --domain godot --query "Schwerkraft" --top 5

Returns JSON:
  [
    {"rank": 1, "score": 0.94, "text": "...", "source_type": "repo", ...},
    ...
  ]
"""
```

### `scripts/hybrid_search.py`

```python
"""
Fusion aus ripgrep (exakt) + ChromaDB (semantisch).

Usage:
  python scripts/hybrid_search.py --domain godot --query "CharacterBody3D" --top 10

Algorithm:
  1. Parallele Queries: ripgrep + ChromaDB
  2. RRF-Fusion (Reciprocal Rank Fusion, k=60)
  3. Deduplizierung (gleiche Chunks mergen)
  4. Ranking nach kombiniertem Score
"""
```

### MCP-Server (`mcp_servers/knowledge_hub/`)

**Tools:**

| Tool | Parameter | Beschreibung |
|------|-----------|-------------|
| `search_knowledge` | `domain`, `query`, `mode?`, `max_results?`, `source_filter?` | Hybride Suche (exakt + semantisch) |
| `get_domain_status` | `domain?` | Status einer/aller Domains |
| `update_domain` | `domain` | Repo-Wissen aktualisieren + Index neu bauen |
| `add_personal_note` | `domain`, `topic`, `content`, `category?` | Persönliche Notiz hinzufügen (hängt an `personal/<category>.md` an) |
| `list_personal_notes` | `domain`, `category?` | Persönliche Notizen auflisten |
| `list_domains` | — | Alle verfügbaren Domains + deren Status |

### `install.sh`

```bash
#!/usr/bin/env bash
# Installiert Knowledge-Hub-Skills in ein anderes OpenCode-Projekt.
#
# Usage:
#   ./install.sh /path/to/project                    # alle Domains
#   ./install.sh /path/to/project godot              # nur godot
#   ./install.sh /path/to/project godot blender       # mehrere
#   ./install.sh /path/to/project --symlink godot     # Symlinks (dev)
#
# Example:
#   cd ~/Documents/work/knowledge-hub
#   ./install.sh ~/Documents/work/nak-hopper-game godot
```

### `requirements.txt`

```
# Knowledge Hub — Python Dependencies
#
# Hinweis: sentence-transformers mit all-mpnet-base-v2 lädt ~420 MB
# beim ersten pip install herunter (one-time Model-Download).

chromadb>=0.5.0
sentence-transformers>=3.0.0
```

## Phasen-Plan

### Phase 1: Foundation (aktuell)
- [x] ~~3 Godot-Skills im `nak-hopper-game`~~ (existiert, wird nach Hub migriert)
- [x] ~~4 CLI-Skripte (update, search, status, pack)~~ (existiert, wird nach Hub migriert)
- [x] ~~Git LFS~~ (existiert)
- [x] ~~Prio 1 Verbesserungen (Header, ripgrep, status, local mode)~~ (erledigt)
- [ ] **Knowledge-Hub-Repo anlegen** ← NÄCHSTER SCHRITT
- [ ] Basis-Struktur (README, docs/, domains/godot/, .agents/skills/, mcp_servers/)
- [ ] `domain.md` für Godot schreiben
- [ ] Skills + Skripte aus `nak-hopper-game` ins Hub-Repo migrieren
- [ ] `install.sh` implementieren (Symlink/Copy für Skills)
- [ ] `requirements.txt` anlegen

### Phase 2: Embeddings (Prio 2.6)
- [ ] `pip install -r requirements.txt` (chromadb, sentence-transformers + all-mpnet-base-v2 ~420 MB)
- [ ] `scripts/embed_index.py` implementieren (MPNet, 768 dims, komplett neu)
- [ ] `scripts/embed_search.py` implementieren
- [ ] `scripts/hybrid_search.py` implementieren
- [ ] Index für Godot-Domain bauen + testen

### Phase 3: MCP-Server (Prio 3.7)
- [ ] `mcp_servers/knowledge_hub/server.py` implementieren
- [ ] `mcp_servers/knowledge_hub/tools.py` implementieren
- [ ] Server in OpenCode registrieren
- [ ] Test: `search_knowledge(domain="godot", query="CharacterBody3D")`

### Phase 4: Mehr Domains
- [ ] `blender/` Domain anlegen (Quellen: Blender Python API docs, Blender StackExchange)
- [ ] `resolve/` Domain anlegen
- [ ] `freecad/` Domain anlegen

### Phase 5: Automation (Prio 2.5)
- [ ] GitHub Action für wöchentliches Update
- [ ] Auto-Index-Rebuild nach Update
- [ ] GitHub Public Release (inkl. `install.sh`-Doku)

## Erfolgskriterien

- [ ] Knowledge-Hub-Repo existiert mit docs/ai/README.md (Agent findet sich zurecht)
- [ ] `./install.sh ~/Documents/work/nak-hopper-game godot` funktioniert
- [ ] Godot-Domain ist funktional: `python scripts/embed_search.py --domain godot --query "Schwerkraft"` liefert relevante Treffer
- [ ] MCP-Server ist in OpenCode registriert und Tools sind aufrufbar
- [ ] Persönliches Wissen (gotchas.md, faq.md) ist in ChromaDB indexiert und durchsuchbar
- [ ] `source_type: "personal"` und `source_type: "repo"` sind in Suchergebnissen unterscheidbar
- [ ] Neue Domain hinzufügen = 3 Dateien anlegen + `embed_index.py --domain <name>` ausführen (kein Code-Refactor)
- [ ] Repo ist bereit für GitHub Public (LFS, .gitignore, README, MIT License)

## Entscheidungen (Q1-Q5)

| # | Frage | Entscheidung | Begründung |
|---|-------|-------------|------------|
| Q1 | Skills in beiden Repos oder Hub als Single Source? | **Hub = Single Source of Truth** | Andere Projekte installieren Skills via `install.sh`. GitHub Public. |
| Q2 | ChromaDB persistent oder in-memory? | **Persistent** (Disk, .gitignored) | 15K+ Chunks in-memory zu langsam |
| Q3 | MiniLM (80 MB) oder MPNet (420 MB)? | **all-mpnet-base-v2** (MPNet, 768 dims) | Höhere Accuracy (85%+) priorisiert. 420 MB Download akzeptabel, Index-Zeit ~5 Min |
| Q4 | Freitext-Markdown oder strukturiertes YAML? | **Markdown** mit `##`-Headern | Schreibfreundlicher, ChromaDB-Chunking macht durchsuchbar |
| Q5 | Inkrementell oder komplett neu? | **Komplett neu** bei jedem `embed_index.py` | Einfachste Implementierung, keine Deduplizierungs-Bugs |

---

Siehe auch:
- Phase 1 Spec: `docs/superpowers/specs/2026-06-09-godot-knowledge-skills-design.md`
- Phase 2 Spec: `docs/superpowers/specs/2026-06-09-godot-knowledge-skills-phase-2-design.md`
- Review: `docs/ai/knowledge-skills-review-2026-06-09.md`
- Workflow: `docs/ai/knowledge-skills-workflow.md`
