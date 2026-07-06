# Improvement Roadmap Phase 3 — Advanced RAG & Content — Design Spec

> **Status:** Draft | **Datum:** 2026-06-30 | **Autor:** Orchestrator
>
> Abgeleitet aus: Interne Inventarisierung + externe Recherche (Stand 2026-06-30), 20 identifizierte Verbesserungspotentiale, Roadmap-Phasenplanung.
> Referenziert: `docs/superpowers/specs/2026-06-30-improvement-roadmap-phase2-embedding-upgrade-design.md`, `docs/superpowers/specs/2026-06-29-knowledge-hub-quality-evaluation-platform-design.md`

## Zusammenfassung

Phase 3 adressiert fortgeschrittene RAG-Techniken (Contextual Retrieval, RAGAS-Integration, BGE-M3 Sparse Retrieval), Content-Lücken (DaVinci Personal Notes + Scripts) und experimentelle Features (Multi-Modal Retrieval). Diese Phase setzt BGE-M3 aus Phase 2 voraus und erfordert lokale LLM-Integration. Aufwand und Risiko sind höher als in Phase 1+2 — einige Maßnahmen sind explizit experimentell.

## Hintergrund

Nachdem Phase 2 das Embedding-Modell modernisiert hat, kann Phase 3 die fortgeschrittenen Features angehen, die ein leistungsfähiges Embedding-Modell und ggf. ein lokales LLM voraussetzen. Die Inventarisierung hat gezeigt, dass DaVinci Resolve die schwächste Domain ist (null persönliches Wissen, keine Scripts, nur Fallback-Chunking). Contextual Retrieval und RAGAS sind State-of-the-Art-Techniken, die die Retrieval-Qualität weiter verbessern können. Multi-Modal Retrieval ist experimentell und nur für DaVinci relevant.

## Maßnahmen

### 3.1 Contextual Retrieval mit lokalem LLM

**Problem:** Chunks verlieren den Kontext ihres umgebenden Dokuments. Ein Chunk mit "Klicken Sie auf den Button" sagt nicht, welcher Button in welchem Panel gemeint ist. Anthropic (Sept 2024) berichtet 49–67% Retrieval-Fehlerraten-Reduktion mit Contextual Retrieval.

**Lösung:** Jeder Chunk bekommt einen LLM-generierten Kontext-Prefix (50–100 Tokens), der erklärt wo im Dokument der Chunk sitzt und was der umgebende Kontext ist. Einmaliges Preprocessing (nicht Query-Time). Lokales LLM (z.B. Qwen 2.5 7B auf Apple Silicon) für die Generierung.

**Aufwand:** 3–5 Tage. **Impact:** sehr hoch.

**Quelle:** https://www.anthropic.com/news/contextual-retrieval

**Betroffene Dateien:**
- `scripts/contextualize_chunks.py` (neu — Preprocessing-Script)
- `scripts/embed_index.py` (Kontext-Prefix vor Embedding)
- `requirements.txt` (`llama-cpp-python` oder `mlx-lm` für lokales LLM)

**Index-Rebuild:** Vollständiger Rebuild aller Domains (Kontext-Prefix ändert den Text, der embedded wird).

**Re-Evaluation:** Zwingend.

**Risiken:**
- LLM-Generierung für ~25.000 Chunks dauert (selbst mit 7B-Modell) mehrere Stunden
- Kontext-Qualität hängt vom LLM ab
- Speicherbedarf für Kontext-Prefixe (50–100 Tokens × 25.000 Chunks = ~2–5 MB Text)
- Re-Evaluation zwingend

**Offene Fragen für Noah:**
- Welches lokale LLM (Qwen 2.5 7B, Llama 3 8B, Mistral 7B)?
- Soll Kontext generiert werden für alle Chunks oder nur für Fallback/PDF-Chunks (strukturierte Godot-Chunks haben bereits `section_path`/`name`)?
- Soll Kontext in ChromaDB-Metadaten oder im `text`-Feld gespeichert werden?
- Soll Contextual Retrieval optional sein (CLI-Flag `--contextualize`)?

---

### 3.2 RAGAS-Integration für Answer-Quality

**Problem:** Composite Score misst nur Retrieval-Qualität (Source Recall, PMA, TKR, EQ). Keine Metrik für Answer-Quality (Faithfulness, Hallucination, Response Relevancy). Der Hub ist ein Retrieval-System, aber in der Praxis werden die Ergebnisse von einem LLM (OpenCode) zu Antworten synthetisiert — die Qualität dieser Synthese wird nicht gemessen.

**Lösung:** RAGAS-Integration. LLM-basierte Metriken (Faithfulness, Response Relevancy, Factual Correctness) zusätzlich zu den bestehenden Retrieval-Metriken. Lokales LLM als Judge. Golden-Dataset-Erweiterung: `expected_answer` Feld pro Frage (Ground-Truth-Antwort für Factual Correctness).

**Aufwand:** 2–3 Tage. **Impact:** mittel.

**Quelle:** https://docs.ragas.io/

**Betroffene Dateien:**
- `scripts/quality/scorer.py` (neue Metriken: `score_faithfulness`, `score_response_relevancy`, `score_factual_correctness`)
- `scripts/quality/run_evaluation.py` (RAGAS-Aufruf)
- `requirements.txt` (`ragas`)
- `quality/golden/godot.yaml` (neues Feld `expected_answer` pro Frage)
- `quality/golden/davinci_resolve.yaml` (neues Feld `expected_answer` pro Frage)

**Risiken:**
- RAGAS benötigt LLM als Judge → lokales LLM nötig (selbes wie 3.1 oder kleiner?)
- Judge-Qualität hängt vom LLM ab
- Langsame Evaluation (LLM-Calls pro Frage)
- Golden Dataset muss um `expected_answer` erweitert werden (Kuratierungsaufwand)

**Offene Fragen für Noah:**
- Welches LLM als Judge (selbes wie 3.1 oder kleiner, z.B. Qwen 2.5 3B)?
- Soll RAGAS optional sein (Flag in `run_evaluation.py`) oder default?
- Wie wird `expected_answer` kuratiert (Noah schreibt Ground-Truth-Antworten)?
- Soll RAGAS nur für Quality-Reports oder auch für CI Quality Gate verwendet werden?

---

### 3.3 DaVinci Personal Notes + Scripts

**Problem:** DaVinci hat null persönliches Wissen (`ui-map.md` ist komplett TODO — 7 Sektionen, alle leer), keine Scripts (`update.sh`, `status.sh`, `search.sh` existieren nicht). `domain.md` listet `personal/beginner-questions.md`, `personal/gotchas.md`, `personal/workflow-notes.md` — aber diese Dateien existieren nicht. DaVinci ist die schwächste Domain im Hub.

**Lösung:** (a) DaVinci-Personal-Notes-Kuratierung durch Noah: `ui-map.md` mit echten UI-Locations, `gotchas.md` mit bekannten Resolve-Problemen, `workflow-notes.md` mit Color/Fusion-Workflows, `beginner-questions.md`. (b) Scripts erstellen: `update.sh` (PDF-Download+Konvertierung via PyMuPDF4LLM), `status.sh`, `search.sh`.

**Aufwand:** Large (Kuratierung mehrere Tage durch Noah + Scripts 1 Tag). **Impact:** kritisch für DaVinci-Domain.

**Betroffene Dateien:**
- `domains/davinci_resolve/personal/ui-map.md` (existiert, aber leer — füllen)
- `domains/davinci_resolve/personal/gotchas.md` (neu)
- `domains/davinci_resolve/personal/workflow-notes.md` (neu)
- `domains/davinci_resolve/personal/beginner-questions.md` (neu)
- `domains/davinci_resolve/scripts/update.sh` (neu)
- `domains/davinci_resolve/scripts/status.sh` (neu)
- `domains/davinci_resolve/scripts/search.sh` (neu)
- `quality/golden/davinci_resolve.yaml` (neue Fragen, die personal notes erwarten)

**Index-Rebuild:** Nötig (neue Chunks aus personal notes). **Re-Evaluation:** Nötig.

**Constraints:**
- Diese Maßnahme ist primär Kuratierung (Noahs Aufgabe), nicht Code
- Die Spec definiert nur Anforderungen (welche Notes, welches Format, welche Scripts)
- PyMuPDF4LLM AGPL Prozessgrenze beachten (bestehende Decision in `docs/decisions/2026-06-27-agpl-process-boundary.md`)
- `update.sh` muss PDFs aus `sources/raw/` konvertieren (falls neue PDFs hinzukommen)

**Offene Fragen für Noah:**
- Soll DaVinci-Update GitHub-Action geben (wie Godot)?
- Welche DaVinci-Themen sind Noah wichtig (Color Page, Fusion, Edit, Audio)?
- Sollen die Scripts analog zu Godot-Scripts sein (gleiche Struktur, gleiche Konventionen)?
- Soll `beginner-questions.md` als FAQ-Äquivalent dienen (analog zu `godot/personal/faq.md`)?

---

### 3.4 BGE-M3 Sparse Retrieval (BM25 ersetzen) — experimentell

**Problem:** BM25 via `rank_bm25` mit Pickle-Serialisierung (akzeptiertes Risiko für persönlichen Hub, aber nicht für Shared/Multi-User). Zwei separate Indizes (ChromaDB + BM25) mit RRF-Fusion. Pickle ist ein Security-Risiko bei Shared-Nutzung.

**Lösung:** BGE-M3's integriertes Sparse-Retrieval (lexikalische Gewichte als Sparse-Vector) ersetzt BM25. ChromaDB nativer Sparse-Vector-Support (in Arbeit für 1.5.9+). Vereinfacht Pipeline (kein separater BM25-Index, kein Pickle).

**Aufwand:** 3–5 Tage. **Impact:** mittel.

**Quelle:** ChromaDB Releases: https://github.com/chroma-core/chroma/releases

**Betroffene Dateien:**
- `scripts/hybrid_search.py` (Sparse-Retrieval statt BM25)
- `scripts/bm25_search.py` (deprecated/entfernt)
- `scripts/embed_index.py` (Sparse-Embeddings indexieren)
- `scripts/model_manager.py` (BGE-M3 Sparse-Modus)
- `mcp_servers/knowledge_hub/config.py` (BM25_CACHE_MAX entfernt)

**Index-Rebuild:** Nötig (Sparse-Vectors müssen indexiert werden).

**Re-Evaluation:** Zwingend.

**Risiken:**
- ChromaDB Sparse-Vector-Support muss stabil sein (Phase 3 startet frühestens Sept 2026 — bis dahin sollte es stable sein)
- RRF-Fusion muss angepasst werden (Dense + Sparse statt BM25 + Dense)
- Eliminiert Pickle-Risiko (Security-Verbesserung)
- BGE-M3 Sparse-Lexikalische Gewichte könnten anders kalibriert sein als BM25-TF-IDF

**Offene Fragen für Noah:**
- Soll BM25 als Fallback erhalten bleiben (falls ChromaDB Sparse unstabil)?
- Wie wird RRF zwischen Dense und Sparse von BGE-M3 kalibriert (andere Score-Skala als BM25)?
- Soll diese Maßnahme vorgezogen werden, wenn ChromaDB 1.6 mit stable Sparse-Support released wird?

---

### 3.5 Multi-Modal Retrieval (Bilder aus PDFs) — experimentell

**Problem:** DaVinci-PDFs haben Screenshots/Diagramme (UI-Screenshots, Node-Graphen, Color-Wheels), die im Text-Chunking verloren gehen. Ein Bild sagt mehr als 1000 Worte — aber der Hub kann Bilder nicht retrieven.

**Lösung:** Multi-Modal Retrieval via ChromaDB (unterstützt Multi-Modal). Bilder aus PDFs extrahieren, mit CLIP/SigLIP embedden, als separate Chunks indexieren. Query-Time: Text-Query wird gegen Bild-Embeddings gematcht (CLIP cross-modal).

**Aufwand:** 1–2 Wochen. **Impact:** mittel (nur DaVinci relevant).

**Betroffene Dateien:**
- `scripts/embed_index.py` (Bild-Extraktion + Embedding)
- `scripts/parser_base.py` (Bild-Metadaten)
- `requirements.txt` (`transformers`, `PIL`/`Pillow`)

**Risiken:**
- Komplex (PDF-Bild-Extraktion, CLIP-Modell-Integration, ChromaDB Multi-Modal)
- Speicherbedarf (Bilder als Base64 oder Dateipfade)
- Query-Time: Text-Query muss gegen Bild-Embeddings matchen (CLIP cross-modal)
- Nur für DaVinci relevant — hoher Aufwand für eine Domain

**Offene Fragen für Noah:**
- Welches Vision-Modell (CLIP, SigLIP, jina-clip-v2)?
- Soll Bild-Retrieval in den hybriden Search integriert oder separat sein?
- Wie werden Bild-Treffer im MCP-Tool dargestellt (Base64, Pfad, Beschreibung)?
- Ist der Aufwand gerechtfertigt (1–2 Wochen für eine Domain)?

---

## Abhängigkeiten zwischen Maßnahmen

```
Phase 2 (BGE-M3)
  ├── 3.1 Contextual Retrieval (setzt BGE-M3 nicht zwingend voraus, aber sinnvoll)
  ├── 3.2 RAGAS-Integration (unabhängig von BGE-M3, braucht lokales LLM)
  ├── 3.3 DaVinci Personal Notes (unabhängig)
  ├── 3.4 BGE-M3 Sparse Retrieval (setzt BGE-M3 aus Phase 2 voraus)
  └── 3.5 Multi-Modal Retrieval (unabhängig, aber experimentell)
```

Empfohlene Reihenfolge:
1. 3.3 DaVinci Personal Notes + Scripts (Content-Lücke zuerst schliessen)
2. 3.1 Contextual Retrieval (höchster Quality-Impact)
3. 3.4 BGE-M3 Sparse Retrieval (nachdem ChromaDB Sparse-Support stable ist)
4. 3.2 RAGAS-Integration (nachdem lokales LLM etabliert ist)
5. 3.5 Multi-Modal Retrieval (niedrigste Priorität, experimentell)

## Phase-Exit-Kriterien

- [ ] Contextual Retrieval für alle Fallback/PDF-Chunks implementiert
- [ ] RAGAS-Integration liefert Answer-Quality-Metriken
- [ ] DaVinci: ≥4 personal notes Dateien mit substanziellem Inhalt
- [ ] DaVinci: `update.sh`, `status.sh`, `search.sh` funktionsfähig
- [ ] BGE-M3 Sparse Retrieval ersetzt BM25 (oder BM25 als Fallback dokumentiert)
- [ ] Multi-Modal Retrieval: experimentelles Feature dokumentiert (auch wenn nicht aktiviert)
- [ ] Re-Evaluation bestätigt keine signifikanten Regressionen
- [ ] `docs/ai/changelog.md` aktualisiert

## Entscheidungen (Noah, 2026-06-30)

### Entscheidung 3.1: Lokales LLM für Contextual Retrieval
**Frage:** Welches lokale LLM (Qwen 2.5 7B, Llama 3 8B, Mistral 7B)? Soll Kontext generiert werden für alle Chunks oder nur für Fallback/PDF-Chunks? Soll Kontext in ChromaDB-Metadaten oder im text-Feld gespeichert werden?
**Entscheidung:** Qwen3-14B als primäres LLM, Qwen3-8B als Fallback (über KH_LLM_MODEL-Env-Var). Contextual Retrieval für ALLE Chunks (Godot-RST, DaVinci-PDF, Personal Notes), nicht nur Fallback/PDF. Kontext im text-Feld gespeichert (als Prefix vor dem Original-Chunk-Text), nicht in separaten Metadaten. MLX-Backend (mlx-lm) primär für Apple Silicon, llama-cpp-python als Cross-Platform-Fallback.
**Begründung:** Qwen3-Serie ist 2026 der Open-Source-Standard für multilingual (DE+EN+ZH+50 weitere), Apache 2.0, konstante Weiterentwicklung (Qwen3.5/3.6/3.7 in den letzten Monaten). 14B ist der Sweet-Spot auf Apple Silicon (M2/M3/M4, 16-32 GB RAM, ~8 GB quantisiert, 15-25 tokens/s). Einheitlichkeit: alle Chunks bekommen Kontext = einheitliche Architektur, keine Zwei-Klassen-Chunks (strukturiert vs. unstrukturiert). LLM kann Verbindungen sehen, die section_path allein nicht zeigt. Kontext im text-Feld bewahrt Semantik und wird von Embedding/Cross-Encoder mit verarbeitet. MLX nativ für Apple Silicon (2-3x schneller als llama.cpp auf M-Chips). NICHT Llama 3/4 (EN-fokussiert), NICHT Mistral (kleinere Modellfamilie), NICHT GLM (weniger Community-Ecosystem für lokale Deployment).

### Entscheidung 3.2: RAGAS Judge-LLM
**Frage:** Welches LLM als Judge (selbes wie 3.1 oder kleiner)? Soll RAGAS optional sein (Flag) oder default? Wie wird expected_answer kuratiert?
**Entscheidung:** Qwen3-14B als RAGAS-Judge (selbes Modell wie Contextual Retrieval, via KH_LLM_MODEL). KEIN separates Judge-LLM. RAGAS default-off via Flag `--with-answer-quality` in run_evaluation.py (optional, da langsam). expected_answer: Noah kuratiert Ground-Truth-Antworten für die Golden-Dataset-Fragen manuell (kein LLM-Generierung der Ground-Truth).
**Begründung:** Ein Modell für Contextual Retrieval + RAGAS = eine KH_LLM_MODEL-Env-Var, ein Model-Download (~8 GB quantisiert), eine Deployment-Pipeline. Qwen3-14B ist stark genug als Judge (RAGAS benötigt Reasoning, 14B reicht für Faithfulness). RAGAS default-off verhindert langsame CI-Läufe und erlaubt Noah, Answer-Quality bei Bedarf zu evaluieren. expected_answer manuell kuratiert (keine zirkuläre LLM-Evaluierung von LLM-Generiertem).

### Entscheidung 3.3: DaVinci-Themen-Priorität
**Frage:** Soll DaVinci-Update GitHub-Action geben (wie Godot)? Welche DaVinci-Themen sind Noah wichtig (Color Page, Fusion, Edit, Audio)?
**Entscheidung:** DaVinci-Personal-Notes in dieser Reihenfolge: (1) ui-map.md für alle 4 Pages parallel (UI-Locations, 30-60 Min), (2) Color Page (gotchas.md + workflow-notes.md) — höchste Nutzung, komplexeste UI, (3) Edit Page (workflow-notes.md) — häufigster Workflow, (4) Fusion (gotchas.md) — Nischen-Feature, (5) Audio/Fairlight (gotchas.md) — letzte Priorität. KEINE GitHub-Action für DaVinci (PDFs manuell von Blackmagic-Website).
**Begründung:** Color und Edit decken ~80% der realen DaVinci-Nutzung ab. ui-map.md zuerst weil mechanisch erfassbar (Screenshot + Page-Tab + Panel-Name). Reihenfolge nach Hub-Wert, nicht nach Lernkurve. Golden-Dataset-Fragen parallel zu Notes: pro Page 3-5 Fragen. DaVinci-PDFs sind statisch (Blackmagic-Website), kein automatisches Upstream-Update nötig im Gegensatz zu Godot (Open-Source-Repo).

### Entscheidung 3.4: BGE-M3 Sparse Retrieval (BM25-Ersatz) Fallback
**Frage:** Soll BM25 als Fallback erhalten bleiben (falls ChromaDB Sparse unstabil)? Wie wird RRF zwischen Dense und Sparse von BGE-M3 kalibriert?
**Entscheidung:** BM25 als Fallback erhalten (via KH_SPARSE_MODE: "bm25" | "bge-m3-sparse", default "bm25" bis ChromaDB Sparse stable). RRF-Kalibrierung: separater k-Wert für BGE-M3-Sparse vs. BM25 (weil Score-Skalen differieren), empirisch via Re-Evaluation bestimmt.
**Begründung:** BM25-Fallback sichert gegen instabile ChromaDB-Sparse-Vector-Implementierung. Modus-Umschaltung via Env-Var entspricht etabliertem Muster (KH_RERANKER_MODEL, KH_EMBEDDING_MODEL). RRF-k-Parameter pro Sparse-Quelle separiert, da BGE-M3-Sparse-Scores (normalisiert) andere Skala als BM25-Okapi-Scores (unbounded) haben.

### Entscheidung 3.5: Multi-Modal Retrieval (experimentell)
**Frage:** Welches Vision-Modell (CLIP, SigLIP, jina-clip-v2)? Soll Bild-Retrieval in den hybriden Search integriert oder separat sein? Aufwand gerechtfertigt?
**Entscheidung:** Multi-Modal Retrieval DEFERRED (nicht in Phase 3 implementiert). Bleibt als experimenteller Plan in der Spec dokumentiert, aber kein Implementierungsziel. Falls DaVinci-Bild-Retrieval später relevant wird, separate Spec schreiben.
**Begründung:** Aufwand (1-2 Wochen) steht nicht im Verhältnis zum Nutzen für einen persönlichen Hub mit primär Text-Queries. DaVinci-PDFs haben Screenshots, aber Text-Chunking deckt die meisten Such-Queries ab. Multi-Modal fügt komplexe Dependencies (CLIP-Modell, PIL, Base64-Handling, Cross-Modal-Scoring) hinzu. Lieber Contextual Retrieval (Phase 3.1) zuerst, das alle Domains verbessert, statt DaVinci-spezifisches Bild-Retrieval.

### Entscheidung 3.6: Konfigurierbarkeit via Env-Vars (Querschnitt)
**Frage:** Wie werden Modelle, Reranker und LLMs konfiguriert, um Modellwechsel ohne Code-Änderung zu erlauben?
**Entscheidung:** Drei zentrale Env-Vars einführen: `KH_EMBEDDING_MODEL` (default all-mpnet-base-v2, BGE-M3 in Phase 2), `KH_RERANKER_MODEL` (default ms-marco-MiniLM-L-12-v2, jina-reranker-v2 in Phase 1), `KH_LLM_MODEL` (default Qwen3-14B, Fallback Qwen3-8B in Phase 3). Optional `KH_JUDGE_MODEL` (default = KH_LLM_MODEL) und `KH_SPARSE_MODE` (default "bm25"). Alle in config.py zentral verwaltet, in docs/ai/best-practices.md dokumentiert.
**Begründung:** Konfigurierbarkeit via Env-Vars ist der höchste Nachhaltigkeits-Hebel: danach kann jedes Modell getestet/gewechselt werden ohne Code-Änderung. Einmal gebaut (Phase 1), trägt es für Phase 2 (Embedding-Wechsel), Phase 3 (LLM, Sparse-Mode) und alle zukünftigen Modellwechsel. Defaults sichern Rückwärtskompatibilität (ohne Env-Var = aktuelles Verhalten). Dokumentation in best-practices.md macht es für zukünftige Agenten sichtbar.

## Offene Fragen für Noah (zusammengefasst)

> Siehe Entscheidungen (Noah, 2026-06-30) oben für die Antworten.

1. Contextual Retrieval: Welches LLM? Alle Chunks oder nur Fallback/PDF? Kontext in Metadaten oder Text? Optional?
2. RAGAS: Welches Judge-LLM? Optional oder default? `expected_answer`-Kuratierung? Auch in CI?
3. DaVinci: GitHub-Action? Welche Themen? Script-Struktur analog Godot? FAQ-Äquivalent?
4. Sparse Retrieval: BM25-Fallback? RRF-Kalibrierung? Vorziehen bei ChromaDB 1.6?
5. Multi-Modal: Welches Vision-Modell? Integration oder separat? Darstellung im MCP? Aufwand gerechtfertigt?

## Referenzen

- Contextual Retrieval: https://www.anthropic.com/news/contextual-retrieval
- RAGAS: https://docs.ragas.io/
- BGE-M3: https://huggingface.co/BAAI/bge-m3
- ChromaDB Releases: https://github.com/chroma-core/chroma/releases
- DaVinci-Domain-Spec: `docs/superpowers/specs/2026-06-27-davinci-resolve-knowledge-domain-design.md`
- Quality-Platform-Spec: `docs/superpowers/specs/2026-06-29-knowledge-hub-quality-evaluation-platform-design.md`
- Phase-2-Spec: `docs/superpowers/specs/2026-06-30-improvement-roadmap-phase2-embedding-upgrade-design.md`
- AGPL Process Boundary: `docs/decisions/2026-06-27-agpl-process-boundary.md`
- Bestehender BM25: `scripts/bm25_search.py`
- Bestehendes Hybrid Search: `scripts/hybrid_search.py`
- Bestehendes DaVinci UI-Map: `domains/davinci_resolve/personal/ui-map.md`
- Bestehendes DaVinci domain.md: `domains/davinci_resolve/domain.md`
