# Domain: Godot Eval C

Phase 3.2 Eval-Domain — Contextual BM25. Kopie der Godot-Quellen via
relativer Symlinks auf `../../godot/sources/*.md` und
`../../godot/personal/*.md`. KEINE echten Quell-Daten hier (nur Symlinks).

Wichtig (NB-6): `Embedding-Model: BAAI/bge-m3` muss gesetzt bleiben, sonst
fiele `get_domain_config` auf `all-mpnet-base-v2` (384 Token) zurück und
`context_prefix + "\n" + text` würde truncieren — der Eval würde
Truncation-Artefakte statt Contextual-Retrieval-Nutzen messen.

Wichtig (BS-8): `Parser: none (fallback chunking, eval-domain)` —
godot_eval_c nutzt bewusst KEINEN RST-Parser, damit der BM25-Corpus
ausschließlich aus `fallback_chunk`-Chunks besteht und der
Contextual-BM25-Effekt (TF-Erhöhung durch `context_prefix`-Keyword-
Overlap) isoliert gemessen wird, ohne RST-Parser-Strukturierung
(name/signature-Boosts) als Konfounder.

## Zweck

E13-Isolation: Diese Domain hat einen eigenen ChromaDB-Index unter
`chromadb_data/godot_eval_c/` und einen eigenen BM25-Index
(`godot_eval_c_bm25.pkl`), sodass der produktive `chromadb_data/godot/`-Index
unberührt bleibt. Wird von `build_index("godot_eval_c", contextualize=True,
contextualize_bm25=True)` als Contextual-BM25-Variante gebaut.

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
- Parser: none (fallback chunking, eval-domain)
- ChromaDB-Collection: `godot_eval_c_knowledge`
- Source-Types: repo
- Letztes Update: 2026-07-04