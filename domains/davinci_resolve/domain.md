# Domain: davinci_resolve

## Zweck
Wissen für Videoschnitt-Produktion mit DaVinci Resolve Studio 21.
Fokus: Wo finde ich Werkzeuge in der UI, wie produziere ich erfolgreich Videos.
Deckt: Cut, Edit, Color, Fairlight, Fusion, Deliver, Photo (ab Resolve 21).

## Quellen (Repo-Wissen)
| Name | Datei | Ursprung | Konvertiert am |
|------|-------|----------|---------------|
| Resolve 20.3 Reference Manual | sources/davinci-resolve-20.3-reference-manual.md | Blackmagic PDF | 2026-06-28 |
| Resolve 21 New Features Guide | sources/davinci-resolve-21-new-features-guide.md | Blackmagic PDF | 2026-06-28 |
| Resolve 20 Beginner's Guide | sources/davinci-resolve-20-beginners-guide.md | Blackmagic PDF | 2026-06-28 |
| Resolve 20 Advanced Visual Effects | sources/davinci-resolve-20-advanced-visual-effects.md | Blackmagic PDF | 2026-06-28 |
| Resolve 20 Colorist Guide | sources/davinci-resolve-20-colorist-guide.md | Blackmagic PDF | 2026-06-28 |
| Resolve 20 Editor's Guide | sources/davinci-resolve-20-editors-guide.md | Blackmagic PDF | 2026-06-28 |
| Resolve 20 Fairlight Audio Post | sources/davinci-resolve-20-fairlight-audio-post.md | Blackmagic PDF | 2026-06-28 |
| Resolve 20 Fusion Visual Effects | sources/davinci-resolve-20-fusion-visual-effects.md | Blackmagic PDF | 2026-06-28 |
| Fairlight Live User Manual | sources/fairlight-live-user-manual.md | Blackmagic PDF | 2026-06-28 |
| Fusion 20.3 Manual | sources/fusion-20.3-manual.md | Blackmagic PDF | 2026-06-28 |

## Bezugsquellen (PDF-Downloads)
- Training: https://www.blackmagicdesign.com/products/davinciresolve/training
- Support & Manuals: https://www.blackmagicdesign.com/support/family/davinci-resolve-and-fusion

## Persönliches Wissen
| Datei | Beschreibung |
|-------|-------------|
| personal/ui-map.md | UI-Lernkarte: Page → Panel → Aktion |
| personal/beginner-questions.md | Anfängerfragen und Antworten |
| personal/gotchas.md | Fallen, Bugs, Workarounds |
| personal/workflow-notes.md | Eigene Reel-Produktions-Workflows |

## Metadaten
- Embedding-Model: BAAI/bge-m3 (1024 dims)
- Collection: davinci_resolve_knowledge
- ChromaDB-Path: chromadb_data/davinci_resolve/chroma/
- BM25-Path: chromadb_data/davinci_resolve/davinci_resolve_bm25.pkl
- Source-Types: pdf
- Letztes Update: 2026-06-30
- Multimodal-Model: google/siglip2-so400m-patch16-512 (1152 dims, text+image joint encoder, Apache 2.0)
- Vision-LLM: gemma4:cloud (Ollama Cloud, Zero-Retention, 3 parallele Worker)
- Image-Collection: davinci_resolve_images (ChromaDB, modality=image|caption)
- Image-BM25-Path: chromadb_data/davinci_resolve/davinci_resolve_images_bm25.pkl
- Image-Manifest: chromadb_data/davinci_resolve/image_manifest.json
- Image-Extraction: enabled (PyMuPDF4LLM write_images=True, AGPL build tool)
- Image-Caption-Cache: chromadb_data/davinci_resolve/image_caption_cache.db (SQLite WAL)
- Image-Embedding-Cache: chromadb_data/davinci_resolve/image_embedding_cache.db (SQLite WAL)

## Lizenz-Hinweis
Quelldokumente © Blackmagic Design. Ursprüngliche PDFs in sources/raw/ (gitignored).
Konvertierte Markdown-Dateien sind interne Arbeitsprodukte, nicht zur Weitergabe.
PyMuPDF/PyMuPDF4LLM (AGPL-3.0) wird nur im Build-Script verwendet, nicht im Runtime-Code.
Siehe THIRD_PARTY_LICENSES.md und docs/decisions/.