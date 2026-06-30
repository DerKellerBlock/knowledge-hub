# Domain Model — Knowledge Hub

## Konzept

Jede Domain repräsentiert ein Tool/eine Technologie in Noahs Wissensbasis (Godot, Blender, Resolve, FreeCAD, …). Domains sind **autarke Module** — sie können unabhängig voneinander existieren, haben eigene Quellen, eigenes Wissen und eigene CLI-Skripte.

## Domain-Struktur

```
domains/<name>/
├── domain.md              # Konfiguration (Quellen, Metadaten)
├── sources/               # Repomix-Packed-Files (*.md)
│   ├── <source1>-packed.md
│   └── <source2>-packed.md
├── personal/              # Noahs persönliches Wissen (*.md)
│   ├── faq.md             # Häufige Fragen + Antworten
│   ├── gotchas.md         # Fehler + Workarounds
│   ├── best-practices.md  # Bewährte Patterns
│   └── tips.md            # Kurze Tipps
└── scripts/               # Domain-CLI
    ├── update.sh           # Quellen aktualisieren (repomix)
    ├── search.sh           # BM25-Suche
    └── status.sh           # Domain-Status
```

## domain.md Format

```markdown
# Domain: <name>

## Quellen (Repo-Wissen)
| Name | Repo URL | Include Pattern | Ignore Pattern |
|------|----------|-----------------|-----------------|
| ... | ... | ... | ... |

## Persönliches Wissen
| Datei | Beschreibung |
|-------|-------------|
| ... | ... |

## Metadaten
- Embedding-Model: all-mpnet-base-v2 (768 dims)
- Collection: <name>_knowledge
- Source-Types: pdf|repo     (kommagetrennt, z.B. "pdf" oder "repo" oder "pdf, repo"; Default "repo")
- Letztes Update: YYYY-MM-DD
```

`source_types` wird vom `model_manager.get_domain_config()` aus dem
`## Metadaten`-Block geparst (Regex `r"- Source-Types:\s*(.+?)\s*$"` mit
`re.MULTILINE`). Wird das Feld weggelassen, fällt der Wert auf
`["repo"]` zurück. Die Quality Evaluation Platform leitet daraus ab, ob
eine Domain PDF-Metadaten (`page_start`/`page_end`) in den Suchergebnissen
erwarten lässt (siehe `scripts/quality/run_evaluation.py`).

## Wissenstypen (ChromaDB-Metadaten)

| Typ | source_type | chunk_type | Quelle | Update-Strategie |
|-----|-------------|------------|--------|-----------------|
| Repo-Wissen | `"repo"` | (domain-spezifisch) | `sources/*.md` | Komplett neu bei jedem Update |
| Persönliches Wissen (Sektion) | `"personal"` | `"personal_section"` | `personal/*.md` | Kumulativ (wächst) |
| Persönliches Wissen (Preamble) | `"personal"` | `None` | `personal/*.md` | Kumulativ (wächst) |

Personal Notes mit `##`-Headern werden via `markdown_section_chunk()` in semantisch unabhängige Sektions-Chunks zerlegt (`chunk_type="personal_section"`, `name=Sektionsüberschrift`, `source_file`, `line_start`/`line_end`, `page_start`/`page_end=None`). Preamble-Chunks (Inhalt vor dem ersten `##`-Header) haben `chunk_type=None`, `name=None`. Dateien ohne `##`-Header oder mit ausschließlich <50-Zeichen-Sektionen fallen auf `fallback_chunk()` zurück (1 Chunk pro Datei).

## Indizes pro Domain

| Index | Technologie | Speicherort | Metrik |
|-------|-------------|-------------|--------|
| ChromaDB-Collection | ChromaDB (on-disk) | `chromadb_data/<name>_knowledge/` | Cosine (768d) |
| BM25-Index | rank_bm25 (in-memory) | Beim Laden aus Chunks gebaut | TF-IDF-basiert |
| Cross-Encoder | ms-marco-MiniLM-L-12-v2 | In-Memory beim Search-Lauf | Pairwise Score |

Der `bm25_index_size_mb` ist Teil des Domain-Status und wird in `domain.md` als Metadatum geführt.

## Eine neue Domain anlegen

```bash
# 1. Struktur anlegen
mkdir -p domains/blender/{sources,personal,scripts}
cp templates/domain.md domains/blender/domain.md  # anpassen

# 2. Quellen scrapen
cd domains/blender && ./scripts/update.sh

# 3. Index bauen
python scripts/embed_index.py --domain blender

# 4. In MCP-Server sichtbar (automatisch beim nächsten Server-Start)
```
