# Domain: Godot Eval B

Phase 3.1b Eval-Domain — kontextualisiert. Kopie der Godot-Quellen via
relativer Symlinks auf `../../godot/sources/*.md` und
`../../godot/personal/*.md`. KEINE echten Quell-Daten hier (nur Symlinks).

Wichtig (NB-6): `Embedding-Model: BAAI/bge-m3` muss gesetzt bleiben, sonst
fiele `get_domain_config` auf `all-mpnet-base-v2` (384 Token) zurück und
`context_prefix + "\n" + text` würde truncieren — der Eval würde
Truncation-Artefakte statt Contextual-Retrieval-Nutzen messen.

## Zweck

E13-Isolation: Diese Domain hat einen eigenen ChromaDB-Index unter
`chromadb_data/godot_eval_b/` und einen eigenen BM25-Index
(`godot_eval_b_bm25.pkl`), sodass der produktive `chromadb_data/godot/`-Index
unberührt bleibt. Wird von `build_index("godot_eval_b", contextualize=True)`
als kontextualisierte Variante gebaut.

## Quellen (Repo-Wissen)

| Name | Repo URL | Include Pattern | Ignore Pattern |
|------|----------|-----------------|-----------------|
| godot-docs | https://github.com/godotengine/godot-docs | `classes/*.rst,getting_started/**/*.rst` | `**/*.png,**/*.jpg,**/*.gif,**/*.svg,**/_static/**,**/_extensions/**` |
| godot-docs-3d | https://github.com/godotengine/godot-docs | `tutorials/3d/**/*.rst` | `**/*.png,**/*.jpg,**/*.gif,**/*.svg` |
| godot-demo-projects | https://github.com/godotengine/godot-demo-projects | `3d/**/*.gd,viewport/**/*.gd,2d/**/*.gd,gui/**/*.gd,audio/**` | `**/*.png,**/*.jpg,**/*.import,**/*.uid` |

## Persönliches Wissen

| Datei | Beschreibung |
|-------|-------------|
| personal/faq.md | Häufige Godot-Fragen und Antworten |
| personal/gotchas.md | Fehler, Bugs und funktionierende Workarounds |
| personal/best-practices.md | Wiederholbare Patterns aus der Praxis |
| personal/tips.md | Kurze Tipps und Tricks |

## Metadaten

- Embedding-Model: BAAI/bge-m3 (1024 dims)
- Parser: rst-godot (structured parsing of RST class docs)
- ChromaDB-Collection: `godot_eval_b_knowledge`
- Source-Types: repo
- Letztes Update: 2026-07-02