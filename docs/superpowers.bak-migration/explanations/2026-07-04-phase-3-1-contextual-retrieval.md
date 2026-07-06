# Phase 3.1 Contextual Retrieval — Wo die Dateien leben

> **Anfängerfreundliche Erklärung** | 2026-07-04 | LLM-generierte Kontext-Präfixe für bessere Such-Chunks — Ergebnis: NO-GO

## 1. Was ist Contextual Retrieval?

### Das Problem

Wenn der Knowledge Hub eine Godot-Dokumentation in kleine Stücke („Chunks“) zerlegt,
entstehen Snippets wie:

```
void rotate_y(angle: float)
```

Dieser Chunk weiß nicht, dass er zu `Node3D` gehört und aus dem Tutorial
„3D Character Controller“ stammt. Eine Suche nach „how to rotate a 3D object“
findet ihn schlecht, weil der Chunk selbst keinen Kontext enthält.

### Die Lösung (Anthropic-Methode, Sept 2024)

Ein LLM (großes Sprachmodell) liest das **gesamte Quelldokument** und schreibt
für jeden Chunk einen kurzen 50–100 Token Kontext-Präfix, der den Chunk im
Dokument verortet. Beispiel:

```
Kontext: "A rotation method within a Godot Node3D tutorial covering 3D
transforms and character controllers."

Chunk: "void rotate_y(angle: float)"
```

Das Embedding (die semantische Vektordarstellung) wird dann aus
**„Kontext + Chunk-Text“** berechnet — der Chunk wird dadurch viel besser
auffindbar.

### Was bleibt unverändert?

- **BM25** (Stichwortsuche) sucht weiterhin nur im `text`-Feld — ohne Kontext.
- **Cross-Encoder** (Reranker) bewertet ebenfalls nur den `text`.
- **MCP-Server** liefert den `text` sauber und den `context_prefix` als
  separates Metadaten-Feld.

Diese Trennung (Entscheidung D1) stellt sicher, dass der Kontext nur das
Embedding verbessert, ohne die anderen Suchpfade zu verfälschen.

### Welche Chunks bekommen Kontext?

Nur Chunks mit `chunk_type != "late_chunk"` („Pfad A“). Das sind:
- Godot-Repo-Chunks (RST-API-Referenz)
- Personal Notes (faq.md, gotchas.md, tips.md, best-practices.md)

**Ausgenommen:** DaVinci-Resolve-Late-Chunks (haben bereits Chapter-Kontext
durch das Late-Chunking-Verfahren aus Phase 2.2).

---

## 2. Wo liegen die neuen Dateien?

### Neue Skripte

| Pfad | Beschreibung |
|------|-------------|
| `scripts/contextualize_chunks.py` | CLI-Skript für die Kontext-Generierung. Batch-Loop mit Ollama-Startup-Check, Cache-Lookup, LLM-Call mit Retry/Backoff (30s/60s/120s, 3 Versuche), Output-Validation, Resume via SQLite-Cache. Filtert automatisch nur Pfad-A-Chunks (`chunk_type != "late_chunk"`). |
| `scripts/context_cache.py` | SQLite-Cache-Modul für generierte Kontexte. WAL-Mode, `INSERT OR REPLACE`, domain-unabhängiger Cache-Key (`sha256(source_file + chunk_id_in_file + chunk_text_hash + model)`). Cache-Pfad: `chromadb_data/<domain>/context_cache.db`. |
| `scripts/quality/gate.py` | Spot-Check-Gate-Entscheidungslogik: `decide_gate(composite_delta)` → `"GO"`/`"NO-GO"` (Schwelle ≥ −0,02). Reines No-Go-Gate — verhindert nur deutliche Regressionen. |

### Neue Eval-Domains (E13-Isolation)

| Pfad | Beschreibung |
|------|-------------|
| `domains/godot_eval_a/` | Baseline-Eval-Domain. Symlinks auf `../../godot/sources/*.md` und `../../godot/personal/*.md`. Eigener ChromaDB-Index unter `chromadb_data/godot_eval_a/`. Wird **ohne** Kontext gebaut (`contextualize=False`). |
| `domains/godot_eval_b/` | Kontextualisierte Eval-Domain. Gleiche Symlinks wie `godot_eval_a`. Eigener Index unter `chromadb_data/godot_eval_b/`. Wird **mit** Kontext gebaut (`contextualize=True`). |
| `domains/godot_spotcheck/` | Spot-Check-Domain. Nur Symlinks auf `../../godot/personal/*.md` (keine `sources/`). 24 personal section-Chunks. BGE-M3 als Embedding-Modell (NB-6). |

### Golden Dataset für Spot-Check

| Pfad | Beschreibung |
|------|-------------|
| `quality/golden/godot_spotcheck.yaml` | 5 personal-only Fragen für das Spot-Check-Gate. Misst **nicht** echte Quality (N=5 ist schwaches Signal), sondern dient als Mechanismus-Validierung: „Läuft die Pipeline? Gibt es negative Signale?“ |

### A/B-Eval-Reports

| Pfad | Beschreibung |
|------|-------------|
| `results/3-1c/godot_eval_a_2026-07-04.md` | Baseline-Report: 21 Fragen, avg_composite 0.8281, 18 pass / 3 weak |
| `results/3-1c/godot_eval_a_2026-07-04.json` | Baseline-Rohdaten |
| `results/3-1c/godot_eval_b_2026-07-04.md` | Kontextualisiert-Report: 21 Fragen, avg_composite 0.8386, 19 pass / 2 weak |
| `results/3-1c/godot_eval_b_2026-07-04.json` | Kontextualisiert-Rohdaten |

### Tests

| Pfad | Beschreibung |
|------|-------------|
| `tests/unit/test_contextualize_infra.py` | 15 Tests: `get_llm()` Cache/Env-Var, `Chunk.context_prefix` Feld + N5 None-Toleranz, `generate_context()` mit FakeOllamaClient |
| `tests/unit/test_contextualize_chunks.py` | Unit-Tests für `contextualize_chunks.py` (Batch-Loop, Cache-Integration, Retry-Logik) |
| `tests/unit/test_context_cache.py` | Unit-Tests für `context_cache.py` (SQLite-Operationen, Cache-Key, Invalidation) |
| `tests/integration/test_contextualize_build.py` | Integration-Test: vollständiger Build mit Kontext |
| `tests/integration/test_eval_domains.py` | Integration-Test: Eval-Domain-Isolation (E13) |

### Geänderte Skripte

| Pfad | Was sich geändert hat |
|------|----------------------|
| `scripts/embed_index.py` | `build_index(domain, contextualize=False, contextualize_bm25=False)`. `--contextualize` Flag. Embedding-Input = `context_prefix + "\n" + text` wenn contextualize. ChromaDB documents bleiben `c.text` (D1). BM25 bleibt `c.text`. |
| `scripts/model_manager.py` | `get_llm()` (Lazy-Load, Cache-Key `llm:<model_name>`, liest `KH_LLM_MODEL`/`KH_LLM_BACKEND` LIVE). `generate_context()` (Anthropic-Prompt-Template, `keep_alive="24h"`, `temperature=0`, `num_predict=800`). Output-Validation `_validate_context()`, Token-Limits `_truncate()`. |
| `scripts/quality/run_evaluation.py` | `--dataset-path` Flag (E12). `_resolve_dataset_path()` Hilfsfunktion. Default `None` → backward-kompatibel. |
| `scripts/parser_base.py` | `Chunk.context_prefix: str \| None = None` (neues Feld). `to_chromadb_metadata()` serialisiert es, `from_chromadb_metadata()` liest es None-tolerant (N5). |
| `scripts/hybrid_search.py` | `context_prefix` als Metadaten-Feld in Suchergebnissen |
| `scripts/bm25_search.py` | BM25 ignoriert `context_prefix` (D1) |
| `mcp_servers/knowledge_hub/server.py` | `context_prefix` in Tool-Responses |
| `mcp_servers/knowledge_hub/config.py` | `DEFAULT_LLM_MODEL`, `DEFAULT_LLM_BACKEND` Konstanten |
| `requirements.txt` | `ollama>=0.4.0,<1.0.0` hinzugefügt |

### Dokumentation

| Pfad | Was sich geändert hat |
|------|----------------------|
| `docs/ai/architecture.md` | Contextualize-Schritt im Datenfluss, `context_prefix`-Feld |
| `docs/ai/best-practices.md` | `KH_LLM_MODEL`, `KH_LLM_BACKEND`, N4 BGE-M3-Voraussetzung, Gemma-4-Reasoning-Hinweis, Contextual Retrieval CLI, Cloud-Setup |
| `docs/ai/decisions.md` | E6, E11–E17 (Phase 3.1b/c Entscheidungen) |
| `docs/ai/known-issues.md` | LIM-012 (Ollama-Version + Gemma-Reasoning), LIM-013 (DaVinci-Fallback-Truncation), Phase 3.1c Ergebnis, Spot-Check-Gate-Limitation |
| `docs/ai/security.md` | Local LLM Sektion, Cloud-LLM Sektion, M2/M3-Mitigations, Retry/Backoff |
| `docs/ai/changelog.md` | 2026-07-02 (3.1a), 2026-07-02 (3.1b), 2026-07-04 (3.1c) |
| `docs/ai/domain-model.md` | Context Prefix Feld, Pfad-A-Filter, SQLite-Cache |
| `docs/superpowers/specs/2026-07-02-phase-3-1-contextual-retrieval-design.md` | Vollständige Design-Spec (Sektion 14: Cloud-Option) |
| `docs/superpowers/retrospectives/2026-07-04-phase-3-1-contextual-retrieval-no-go.md` | Retrospektive (Lessons Learned, Next Steps) |

### Index-Daten (nicht committet, `.gitignored`)

- `chromadb_data/godot_eval_a/` — Baseline-Index (nicht-kontextualisiert)
- `chromadb_data/godot_eval_b/` — Kontextualisierter Index + `context_cache.db` (4580/4580 Einträge)
- `chromadb_data/godot_spotcheck/` — Spot-Check-Index (nur personal)
- `chromadb_data/godot/` — **unverändert** (produktiver Index, E13-Isolation)

---

## 3. OpenCode-Konfiguration

`.opencode/opencode.json` wurde in Phase 3.1 **nicht verändert**. Es gibt keine
neuen Agenten, keine neuen Permissions und keine neuen MCP-Server.

Die vorhandenen Agenten unter `.opencode/agents/` bleiben:

- `orchestrator-knowledge.md` — primärer Agent
- `implement-hub-change.md`
- `plan-hub-change.md`
- `review-hub-plan-blindspots.md`
- `validate-hub-project.md`
- `test-hub-feature.md`
- `review-hub-diff.md`
- `review-hub-security.md`
- `update-hub-docs.md`
- `retrospect-iteration.md`
- `explain-location.md`

Task-Permissions in `opencode.json` matchen die Agent-Dateinamen (ohne `.md`).

---

## 4. Validierungsbefehle

```bash
# Struktur-Check (37 Checks)
./scripts/workspace_check.sh

# Unit-Tests (216 Tests)
.venv/bin/pytest -m unit -q

# Integration-Tests (90 Tests)
.venv/bin/pytest -m integration -q

# Quality-Tests (145 Tests)
.venv/bin/pytest -m quality -q

# Spot-Check-Dataset validieren
.venv/bin/python scripts/quality/validate_dataset.py --domain godot_spotcheck --check-sources

# Eval für eine Domain laufen lassen (mit explizitem Dataset-Pfad)
.venv/bin/python scripts/quality/run_evaluation.py --domain godot_eval_a --dataset-path quality/golden/godot.yaml

# Eval für die kontextualisierte Variante
.venv/bin/python scripts/quality/run_evaluation.py --domain godot_eval_b --dataset-path quality/golden/godot.yaml

# Kontext-Generierung (nur wenn Ollama-Cloud verfügbar)
.venv/bin/python scripts/contextualize_chunks.py --domain godot_eval_b --limit 50 --dry-run
```

---

## 5. Knowledge-QA-Abläufe (vereinfacht)

### A/B-Test

Der Kern der Phase 3.1 ist ein kontrollierter A/B-Vergleich:

1. **Baue zwei Indizes** aus denselben Quellen:
   - **A (Baseline):** `build_index("godot_eval_a", contextualize=False)` — ohne Kontext
   - **B (Kontextualisiert):** `build_index("godot_eval_b", contextualize=True)` — mit Kontext
2. **Evaluiere beide** gegen dasselbe Golden Dataset (`quality/golden/godot.yaml`, 21 Fragen)
3. **Vergleiche das Composite-Delta:** `B.avg_composite − A.avg_composite`
4. **Entscheide:** ≥ +0.02 → GO (produktiver Rollout), < +0.02 → NO-GO

### Spot-Check-Gate (Phase 3.1b)

Vor dem teuren Voll-Lauf (~3h Cloud) läuft ein kleiner Vorab-Test:

- **Domain:** `godot_spotcheck` (nur 24 personal section-Chunks)
- **Dataset:** `quality/golden/godot_spotcheck.yaml` (5 personal-only Fragen)
- **Gate:** `decide_gate(composite_delta)` → `"GO"`/`"NO-GO"` (Schwelle ≥ −0,02)
- **Zweck:** Reines No-Go-Gate — verhindert nur, dass ein kaputter Mechanismus
  einen teuren Voll-Lauf verschwendet. Misst **nicht** echte Quality.

### Eval-Domain-Isolation (E13)

Statt den produktiven `godot`-Index zu backupen/restoren, nutzt Phase 3.1
**separate Eval-Domains** mit Symlinks:

```
domains/godot_eval_a/sources/ → ../../godot/sources/  (Symlink)
domains/godot_eval_a/personal/ → ../../godot/personal/ (Symlink)
domains/godot_eval_b/sources/ → ../../godot/sources/  (Symlink)
domains/godot_eval_b/personal/ → ../../godot/personal/ (Symlink)
```

Jede Domain hat ihren eigenen ChromaDB-Index unter `chromadb_data/godot_eval_{a,b}/`
und ihren eigenen BM25-Index. Der produktive `chromadb_data/godot/`-Index bleibt
**komplett unangetastet**.

### Real-World-Source-Comparison

Die Eval-Reports (`results/3-1c/*.md`) enthalten eine „Real-World Source
Comparison“-Sektion, die Hub-Suchergebnisse mit Online-Quellen (GitHub Issues,
offizielle Docs) vergleicht. Drei Bewertungsebenen:

1. **Source Coverage** — Deckt der Hub die gleichen Quellen ab?
2. **Solution Alignment** — Stimmen die Hub-Antworten mit den Online-Lösungen überein?
3. **Gap Detection** — Fehlen wichtige Lösungen im Hub?

---

## 6. Was ist das Ergebnis? (NO-GO)

### Die Zahlen

| Metrik | Baseline (A) | Kontextualisiert (B) | Delta |
|--------|-------------|---------------------|-------|
| avg_composite | 0.8281 | 0.8386 | **+0.0105** |
| Pass | 18/21 (85.7%) | 19/21 (90.5%) | +1 |
| Weak | 3/21 (14.3%) | 2/21 (9.5%) | −1 |
| Fail | 0 | 0 | 0 |

### Was hat sich verbessert?

**godot-012 (NavigationAgent3D Enemy Chase): weak → pass** (+0.2188 composite).
Contextual Retrieval hat die deutsche `tips.md`-Sektion besser auffindbar gemacht.

### Was hat sich nicht verbessert?

- **godot-008** (3D model visibility, englische Query) bleibt weak —
  Sprachbarriere zwischen englischer Query und deutscher `faq.md`.
- **godot-009** (AnimationTree + BlendSpace2D) bleibt weak —
  breites Thema, fragmentierte API-Referenz-Chunks.

### Warum NO-GO?

Das Composite-Delta von **+0.0105** liegt unter der **+0.02 Schwelle**.
Contextual Retrieval allein bringt einen realen, aber zu kleinen Nutzen
für einen produktiven Rollout. Es gab **keine Regressionen** — der
Mechanismus funktioniert korrekt, der Effekt ist nur zu klein.

### Was bleibt?

Die gesamte Infrastruktur bleibt für zukünftige Re-Läufe erhalten:

- **Eval-Domains** (`godot_eval_a`, `godot_eval_b`, `godot_spotcheck`) werden
  nicht gelöscht — sie können für spätere Experimente wiederverwendet werden.
- **SQLite-Cache** (`chromadb_data/godot_eval_b/context_cache.db`) enthält
  alle 4580 generierten Kontexte — kein erneuter Cloud-Lauf nötig.
- **`--contextualize-bm25` Flag** ist bereits im Code akzeptiert (aber noch
  nicht genutzt) — Anthropic berichtet +14% zusätzliche Reduktion durch
  Contextual BM25.

### Nächste Schritte (für Noah)

1. **Contextual BM25** — `--contextualize-bm25` aktivieren und A/B-Eval
   wiederholen. BM25-Input = `context_prefix + "\n" + text`. Geringer
   Aufwand (Flag existiert, Cache ist gefüllt).
2. **Prompt-Tuning** — Aktuelle Kontexte sind deskriptiv („This chunk
   contains…“). Kürzere, situativere Kontexte könnten das Embedding
   verbessern.
3. **Anderes Cloud-Modell** — `gpt-oss:20b-cloud` (Usage Level 1, günstiger)
   könnte andere Kontext-Stile produzieren. Cache ist modell-spezifisch,
   ein neuer Lauf wäre nötig.
4. **Lokales Gemma 4 12B** — Cloud-gemma4 (32.7B) ≠ lokales Gemma 12B.
   Ein Small-Sample-Vergleich würde den Konfounder auflösen.

---

## Zusammenfassung für Einsteiger

| Frage | Antwort |
|-------|---------|
| Was wurde gebaut? | Ein LLM schreibt für jeden Such-Chunk einen kurzen Kontext-Präfix, der den Chunk im Dokument verortet. Das Embedding nutzt „Kontext + Text“ für bessere Auffindbarkeit. |
| Wo liegt der Code? | `scripts/contextualize_chunks.py`, `scripts/context_cache.py`, `scripts/quality/gate.py` + Änderungen in `embed_index.py`, `model_manager.py`, `run_evaluation.py` |
| Wurde der produktive Index verändert? | **Nein.** Eval-Domains (`godot_eval_a`/`godot_eval_b`) mit Symlinks isolieren das Experiment komplett vom produktiven `godot`-Index. |
| Was ist das Ergebnis? | **NO-GO.** +0.0105 composite-Delta (1 Frage verbessert), unter der +0.02 Schwelle. Keine Regressionen. |
| Wurde etwas kaputt gemacht? | **Nein.** 0 Regressionen, alle 216 Unit-Tests + 90 Integration-Tests + 145 Quality-Tests grün. |
| Was passiert als nächstes? | Infrastruktur bleibt für Re-Läufe. Contextual BM25, Prompt-Tuning oder anderes Modell könnten den Effekt verstärken. |
