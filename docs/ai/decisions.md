# Decisions — Knowledge Hub

> Wichtige Architektur- und Design-Entscheidungen mit Begründung.

## Q1: Hub = Single Source of Truth

- **Entscheidung:** Skills leben im Hub-Repo (`.agents/skills/`), nicht in einzelnen Projekten. Andere Projekte installieren via `install.sh` oder konsumieren via MCP.
- **Begründung:** GitHub Public Release. Ein Update im Hub aktualisiert alle Projekte. Keine Duplizierung.
- **Datum:** 2026-06-09

## Q2: Persistente ChromaDB (on-disk)

- **Entscheidung:** ChromaDB-Index liegt persistent auf Disk (`chromadb_data/`, .gitignored).
- **Begründung:** Bei 15K+ Chunks ist in-memory zu langsam. Neuaufbau dauert ~5 Minuten — das passiert nur bei `embed_index.py`, nicht bei jeder Query.
- **Datum:** 2026-06-09

## Q3: MPNet statt MiniLM

- **Entscheidung:** `all-mpnet-base-v2` (420 MB, 768 dims) als Embedding-Model.
- **Begründung:** Höhere Genauigkeit (~85%+ vs ~80%) priorisiert. 420 MB Download und ~5 Min Index-Zeit akzeptabel für persönlichen Hub.
- **Datum:** 2026-06-09

## Q4: Markdown für persönliches Wissen

- **Entscheidung:** Noahs Notizen als Freitext-Markdown mit `##`-Headern, nicht als strukturiertes YAML.
- **Begründung:** Schreibfreundlicher. ChromaDB-Chunking macht Inhalte trotzdem präzise durchsuchbar.
- **Datum:** 2026-06-09

## Q5: Kompletter Index-Neuaufbau (nicht inkrementell)

- **Entscheidung:** Bei jedem `embed_index.py`-Aufruf wird die ChromaDB-Collection komplett gelöscht und neu gebaut.
- **Begründung:** Einfachste Implementierung. Keine Deduplizierungs-Bugs, keine inkrementellen Edge-Cases. Index-Zeit (~5 Min) ist akzeptabel für wöchentliche Updates.
- **Datum:** 2026-06-09

## Architecture Decisions

### AD-001: Ein MCP-Server für alle Domains

- **Entscheidung:** Ein MCP-Server bedient alle Domains (domain als Parameter), nicht pro Domain ein Server.
- **Begründung:** Kein Multi-Port-Overhead. Neue Domains werden automatisch erkannt (Scan von `domains/` beim Server-Start). 4 Domains × 1 Server = sauber. 4 Domains × 4 Server = Overkill.

### AD-002: CLI + MCP (nicht nur CLI)

- **Entscheidung:** Knowledge-Operationen sind sowohl via CLI (`scripts/*.py`) als auch via MCP-Server zugänglich.
- **Begründung:** CLI für Entwicklung/Debugging, MCP für OpenCode-Integration. Gleiche Codebase, zwei Interfaces.

### AD-003: repomix für Scraping (nicht eigene Crawler)

- **Entscheidung:** Externe Quellen werden via repomix (`--remote`) gescraped, nicht mit eigenen HTTP/HTML-Parsern.
- **Begründung:** repomix 1.14.1 ist battle-tested, handled Git-Logik, Token-Counting, Compression. Eigenbau wäre signifikant mehr Aufwand.

## Q6: BM25 ersetzt ripgrep

- **Entscheidung:** BM25 (`rank_bm25`) ersetzt ripgrep komplett als exakten Retrieval-Pfad in der hybriden Suche.
- **Begründung:** BM25 liefert Relevanz-Scores (kontinuierlich) statt binärer Treffer. Bessere Fusions-Qualität mit ChromaDB über RRF, da beide Pfade echte Scores liefern. Keine Shell-Subprocess-Latenz. `rank_bm25` läuft in-memory im gleichen Python-Prozess.
- **Datum:** 2026-06-10

## Q7: Cross-Encoder-Reranking

- **Entscheidung:** Stage-2-Reranking mit `ms-marco-MiniLM-L-12-v2` als Cross-Encoder nach der RRF-Fusion.
- **Begründung:** Cross-Encoder bewertet Query-Dokument-Paare direkt (nicht nur Embedding-Ähnlichkeit), was präzisere Top-10-Rankings liefert. ~140 MB Modell, ~50–100 ms pro Reranking-Durchlauf — akzeptabel für persönlichen Hub.
- **Datum:** 2026-06-10

## Phase 3.1b Decisions (2026-07-02)

### E6: `--contextualize` Flag von 3.1c nach 3.1b vorgezogen

- **Entscheidung:** Das `--contextualize` Flag in `embed_index.py` wurde von Phase 3.1c nach 3.1b vorgezogen, damit das Small-Scale-Eval den echten Pipeline-Pfad testet (nicht nur Mock-Ergebnisse).
- **Begründung:** Ohne das Flag hätte 3.1b nur den Kontext-Generierungs-Mechanismus getestet, aber nicht den Embedding-Pfad (`context_prefix + "\n" + text`). Das wäre ein unvollständiger Mechanismus-Test gewesen. Spec-Abweichung dokumentiert.
- **Datum:** 2026-07-02

### E11: Spot-Check-Gate Option (a) — personal-only, No-Go-Gate

- **Entscheidung:** Spot-Check-Gate mit 2 pure-personal-Fragen (24 Chunks, ~7 Min LLM), nur No-Go-Gate bei composite-Delta < −0,02. Misst NICHT echte Quality (N=2 ist schwaches Signal).
- **Begründung:** Ehrlich, billig, dokumentiert-limitiert. Echte Quality-Entscheidung folgt in 3.1c (Voll-Lauf gegen `godot.yaml`). 3.1c-Go ist separate Noah-Entscheidung.
- **Datum:** 2026-07-02

### E12: `--dataset-path` Flag in `run_evaluation.py`

- **Entscheidung:** `run_evaluation.py` akzeptiert `--dataset-path` für explizite Golden-Dataset-Pfade (C2-Blocker gelöst). Default `None` → backward-kompatibel (automatische Auflösung aus Domain-Namen).
- **Begründung:** Spot-Check-Gate braucht `godot_spotcheck.yaml` statt `godot.yaml`. Ohne dieses Flag wäre der Spot-Check nicht evaluierbar gewesen.
- **Datum:** 2026-07-02

### E13: Separate Eval-Domains statt Backup/Restore

- **Entscheidung:** `godot_eval_a` (Baseline) und `godot_eval_b` (kontextualisiert) als separate Domains mit Symlinks auf `godot/sources/` und `godot/personal/`. Eigene ChromaDB-Indizes unter `chromadb_data/godot_eval_{a,b}/`.
- **Begründung:** Produktiver `godot`-Index bleibt unangetastet. Kein Backup/Restore-Risiko. BM25-Isolation automatisch über Domain-Namen (E14 gestrichen).
- **Datum:** 2026-07-02

### E14: BM25-Override gestrichen

- **Entscheidung:** E14 (separater BM25-Override für Eval-Domains) wurde gestrichen.
- **Begründung:** BM25-Isolation funktioniert automatisch über Domain-Namen — jede Domain hat ihren eigenen `chromadb_data/<domain>/<domain>_bm25.pkl`. Kein zusätzlicher Mechanismus nötig.
- **Datum:** 2026-07-02

### E15: Pfad-A pure chunk_type-basiert (Spec N1)

- **Entscheidung:** Pfad-A-Filter für Contextual Retrieval ist pure `chunk_type != "late_chunk"` — kein Domain-/source_types-Check.
- **Begründung:** Spec N1 sagt domänenübergreifend alle Chunks mit `chunk_type != "late_chunk"`. DaVinci-Fallback-Chunks (`chunk_type=None` bei late_chunk-Fehler) werden kontextualisiert (korrekt — kein Chapter-Kontext). Mixed-Domain: repo-Chunks kontextualisiert, pdf late_chunk nicht.
- **Datum:** 2026-07-02

### E16 (2026-07-04): Cloud-gemma4 statt lokal für 3.1c, NO-GO result
Entschieden: Cloud-gemma4 (gemma4:cloud, 32.7B) statt lokalem Gemma 4 12B MLX für den 3.1c-Voll-Lauf. Begründung: 69h lokal → ~3h Cloud (Risiko-Reduktion HÖCHSTE → NIEDRIG). Zero-Retention-Policy akzeptiert für trusted Sources. Ergebnis: composite_delta +0.0105 < +0.02 Schwelle → NO-GO, kein Promote. Kontextqualität ist real (godot-012 gehoben), aber zu klein für produktiven Rollout. Konfounder: 32.7B ≠ 12B — Kontextqualität könnte mit lokalem 12B abweichen.

### E17 (2026-07-04): OQ-3 Cache-Promote via domain-unabhängigem Key — bestätigt
Cache-Key = sha256(source_file + chunk_id_in_file + chunk_text_hash + model) — domain-unabhängig (OQ-3 Option b). Beim Promote würde `cp context_cache.db` von eval_b → godot Cache-Reuse ermöglichen (~50 Min statt 3h). Bei NO-GO nicht angewendet, aber Design bestätigt: 2731 Cache-Hits beim Resume nach 502-Crash beweisen, dass der Cache-Key korrekt domain-übergreifend funktioniert.
