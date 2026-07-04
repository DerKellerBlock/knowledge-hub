# Domain: Godot Spot-Check

Phase 3.1b Spot-Check-Gate-Domain. Nutzt NUR die 24 personal section-Chunks
aus `../../godot/personal/*.md` (KEINE `sources/`-Verzeichnis). Zweck ist
der schnelle Mechanismus-Gate: Pipeline läuft + kein negatives Signal auf
personal. KEINE echte Quality-Entscheidung (N=2 ist schwaches Signal — echte
Quality folgt in 3.1c gegen das volle `godot.yaml`).

Wichtig (NB-6 — kritisch für Spot-Check): `Embedding-Model: BAAI/bge-m3` MUSS
gesetzt bleiben. Ohne BGE-M3 fällt `get_domain_config` auf
`all-mpnet-base-v2` (384 Token) zurück. Das `context_prefix + "\n" + text`
würde dann truncieren und der Spot-Check würde Truncation-Artefakte statt
Contextual-Retrieval-Nutzen messen — das Gate-Resultat wäre wertlos.

## Zweck

E13-Isolation: Eigener ChromaDB-Index unter `chromadb_data/godot_spotcheck/`
und eigener BM25-Index (`godot_spotcheck_bm25.pkl`), sodass der produktive
`chromadb_data/godot/`-Index unberührt bleibt.

## Persönliches Wissen

| Datei | Beschreibung |
|-------|-------------|
| personal/faq.md | Häufige Godot-Fragen und Antworten |
| personal/gotchas.md | Fehler, Bugs und funktionierende Workarounds |
| personal/best-practices.md | Wiederholbare Patterns aus der Praxis |
| personal/tips.md | Kurze Tipps und Tricks |

## Metadaten

- Embedding-Model: BAAI/bge-m3 (1024 dims)
- ChromaDB-Collection: `godot_spotcheck_knowledge`
- Source-Types: repo
- Letztes Update: 2026-07-02