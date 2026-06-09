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
    ├── search.sh           # ripgrep-Suche
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
- Letztes Update: YYYY-MM-DD
```

## Wissenstypen (ChromaDB-Metadaten)

| Typ | source_type | Quelle | Update-Strategie |
|-----|-------------|--------|-----------------|
| Repo-Wissen | `"repo"` | `sources/*.md` | Komplett neu bei jedem Update |
| Persönliches Wissen | `"personal"` | `personal/*.md` | Kumulativ (wächst) |

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
