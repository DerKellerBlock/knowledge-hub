# Retrospective: Visual Question Answering via MCP

**Task-ID:** visual-question-answering
**Datum:** 2026-07-07
**Status:** done (Task 7 MiniMax M3 deferred)

## Was wurde gebaut

Visual Question Answering (VQA) als additives Feature über dem
Vision Retrieval Feature. Ein Nutzer kann ein Bild hochladen und eine
Frage dazu stellen („was ist das rechts unten?"). Das OpenCode-LLM
reicht den Bild-Pfad an `search_knowledge(image_path=...)` weiter. Der
Knowledge Hub embeddet das Bild mit SigLIP-2 (gleicher Vektorraum wie
die indexierten DaVinci-Screenshots), findet die ähnlichsten Screenshots
per Cosine-Similarity und gibt deren Captions + Seitenzahlen zurück.
Das LLM nutzt die Captions, um zu erklären was auf dem Nutzer-Bild zu
sehen ist.

## Tasks

| Task | Status | Anmerkung |
|------|--------|-----------|
| 1 — `image_similarity_search()` in `hybrid_search.py` | done | SigLIP-2 + ChromaDB query + content-hash cache (modality="query_image") |
| 2 — `search_knowledge` in `tools.py` erweitern | done | Optionaler `image_path` Parameter, additive prepend von image_match Treffern |
| 3 — MCP-Tool Schema in `server.py` aktualisieren | done | `image_path` als optionaler String-Parameter im inputSchema |
| 4 — Orchestrator-Prompt aktualisiert | done | VQA-Sektion in `.opencode/agents/orchestrator-knowledge.md` |
| 5 — Unit-Tests | done | 8 neue Tests in `tests/unit/test_image_similarity.py`, 234 total grün |
| 6 — Integration-Test (manuell) | done | Top-1 sim=1.0 (dasselbe Bild), Top-2/3 = ähnliche Color Wheels Panels (0.9994, 0.9973) |
| 7 — MiniMax M3 Vision-LLM (optional) | deferred | Kern-VQA funktioniert ohne; MiniMax würde Antwortqualität verbessern, erfordert API-Key |
| 8 — Doku + Retrospektive | done | architecture.md, best-practices.md, known-issues.md, diese Retrospektive, explanation.md, open-work.md |

## Was gut lief

- **Additives Design:** VQA ist rein additiv — die bestehende 4-Listen-RRF
  läuft unverändert. Ohne `image_path` ist das Verhalten byte-identisch
  zur Pre-VQA-Signatur (backward-kompatibel). Keine Migration nötig.
- **Cache-Design:** Query-Image-Embeddings nutzen `modality="query_image"`
  (nicht `"image"`), damit sie nicht mit indexierten Screenshot-Embeddings
  kollidieren. `image_id="query"` Placeholder macht den Cache-Key
  deterministisch (gleiche Bild-Bytes + gleiches Modell = Cache-Hit).
- **Graceful Fallback:** 4 Error-Pfade (File missing, PIL-Error,
  SigLIP-2 unavailable, Collection missing) returnieren `[]` — die
  Text-Suche bleibt unbeeinflusst. Integration-Test bestätigte das.
- **Integration-Test:** Echter DaVinci Color Wheels Screenshot als
  Query-Bild → Top-1 sim=1.0 (exakt dasselbe Bild), Top-2/3 = ähnliche
  Color Wheels Panels aus anderen Kapiteln. SigLIP-2 funktioniert auf
  MPS, ~18s Query-Zeit (inkl. Modell-Laden + 4-Listen-RRF).
- **Code-Struktur:** `image_similarity_search()` ist eine eigenständige
  Funktion in `hybrid_search.py` (vor `rrf_fusion_4list`), die
  `search()`-Funktion hat nur einen zusätzlichen `if image_path:` Block
  am Ende — minimal-invasiv.

## Was nicht so gut lief

- **MiniMax M3 deferred:** Die Caption-basierte Antwort funktioniert,
  ist aber bei niedriger Similarity (<0.7) irreführend — die Caption
  beschreibt den ähnlichen Screenshot, nicht das Nutzer-Bild. Ein
  Vision-LLM (MiniMax M3) würde das lösen, ist aber ohne API-Key nicht
  testbar. Status: deferred, in known-issues.md (VQA-004) dokumentiert.
- **Kein automatisierter E2E-Test:** Task 6 war manueller Integration-Test.
  Ein automatisierter E2E-Test (der echte SigLIP-2 + echte ChromaDB
  nutzt) wäre besser, würde aber ~18s pro Test laufen und
  Model-Download erfordern — nicht im Unit-Test-Layer machbar.
  Entscheidung: manueller Test + gemockte Unit-Tests sind ausreichend
  für den persönlichen Hub.

## Erkenntnisse

- **SigLIP-2 image-encode Pattern:** `processor(images=[img])` →
  `model.get_image_features(**inputs)` → `.cpu().float().numpy()` →
  L2-Normalize. Exakt derselbe Pattern wie in `embed_images.py:_embed_image_batch`,
  was die Konsistenz der Vektorräume garantiert (Query-Embedding und
  indexierte Embeddings nutzen denselben Encoder).
- **ChromaDB cosine distance:** ChromaDB returns cosine *distance*
  (0=identisch, 2=orthogonal). `similarity = 1 - distance`, geclamped
  auf [0, 1]. Wichtig für Consumer: `similarity_score` in Results ist
  similarity, nicht distance.
- **Modality-Namespace:** `modality="image_match"` ist neu und
  unterscheidet sich von `modality="image"` (4-Listen-RRF image_bm25
  Treffer) und `modality="caption"` (image_dense Treffer). Consumer
  können alle 4 Modalities unterscheiden.

## Nächste Schritte

- MiniMax M3 Vision-LLM Integration (Task 7, wenn API-Key verfügbar)
- E2E-Test mit mehreren Query-Bildern (verschiedene DaVinci UI-Panels)
- VQA für weitere Domains (wenn diese Screenshots indexieren)
