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
| Late Chunk (PDF) | `"repo"` | `"late_chunk"` | `sources/*.md` (PDF) | Komplett neu |

Personal Notes mit `##`-Headern werden via `markdown_section_chunk()` in semantisch unabhängige Sektions-Chunks zerlegt (`chunk_type="personal_section"`, `name=Sektionsüberschrift`, `source_file`, `line_start`/`line_end`, `page_start`/`page_end=None`). Preamble-Chunks (Inhalt vor dem ersten `##`-Header) haben `chunk_type=None`, `name=None`. Dateien ohne `##`-Header oder mit ausschließlich <50-Zeichen-Sektionen fallen auf `fallback_chunk()` zurück (1 Chunk pro Datei).

Late Chunks (Phase 2.2) stammen aus PDF-Quellen (DaVinci) und werden via `_LateChunkEncoder` chapter-weise erzeugt. Jeder Chunk trägt `chunk_type="late_chunk"`, `name=<Chapter-Titel>`, `source_file`, `page_start`/`page_end` (Chapter-Grenzen ±2 Toleranz), `line_start=0`/`line_end=0` (PDF-Chapter haben keine Zeilennummern — siehe LIM-010).

**Context Prefix (Phase 3.1):** Jeder Chunk hat ein optionales Feld `context_prefix: str | None = None` (Phase 3.1, Contextual Retrieval). Es enthält einen LLM-generierten 50–100 Token Kontext, der den Chunk im Gesamtdokument verortet. Hybrid-Nutzung (D1): Embedding-Input = `context_prefix + "\n" + text`; BM25- und Cross-Encoder-Input bleiben unverändert (`text` only). MCP-Ausgabe liefert `text` clean und `context_prefix` als separates Metadaten-Feld. `from_chromadb_metadata` liest das Feld None-tolerant (N5 — alte Collections vor Phase 3.1 haben das Feld nicht → `None`).

**Pfad-A-Filter (Phase 3.1b, E15):** Der Geltungsbereich für Contextual Retrieval ist pure `chunk_type != "late_chunk"` (Spec N1, kein Domain-/source_types-Check). DaVinci-Fallback-Chunks (`chunk_type=None` bei late_chunk-Fehler) werden kontextualisiert (korrekt — kein Chapter-Kontext). Mixed-Domain: repo-Chunks kontextualisiert, pdf late_chunk nicht. Contextual Retrieval setzt BGE-M3 voraus (N4 — 8192-Token-Kontext für `context_prefix + "\n" + text`; all-mpnet 384 Token würde truncieren).

**SQLite-Cache (Phase 3.1b):** Kontext-Generierung persistiert in `chromadb_data/<domain>/context_cache.db` (WAL-Mode, `INSERT OR REPLACE`). Der Cache-Key ist domain-unabhängig (OQ-3 Option b: `sha256(source_file | chunk_id_in_file | chunk_text_hash | model)`), sodass ein Cache-Eintrag aus `godot_eval_a` beim Promote nach `godot` wiederverwendet werden kann. `bulk_invalidate_by_source_file()` löscht alle Einträge einer Quelldatei (z.B. nach repomix-Update).

**Contextual BM25 (Phase 3.2, E18):** Bei `contextualize_bm25=True` wird der BM25-Corpus auf `context_prefix + " " + text` erweitert (D1-Aufhebung, opt-in). Default `False` = D1 gültig (BM25 = nur text). Query-Tokenisierung bleibt symmetrisch — der Kontext steckt im Index, nicht in der Query.

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
