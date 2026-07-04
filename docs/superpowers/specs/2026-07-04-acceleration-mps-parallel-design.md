# Acceleration: MPS GPU + Parallel LLM Calls — Design

**Spec-Datei:** `docs/superpowers/specs/2026-07-04-acceleration-mps-parallel-design.md`
**Phase:** 3.3a
**Status:** Implementiert (Code + Tests grün). Rebuild / Eval folgen in 3.3b/c.

## Ziel

- Beschleunigung des Contextual-Retrieval-Workflows (Embedding + LLM)
  so dass ein Godot-Promote (~24.593 Pfad-A-Chunks) und ein DaVinci
  Smoke-Test in praktikabler Zeit durchführbar werden.
- DaVinci Smoke-Test (Infrastruktur-Validierung, **kein** +0.02 Gate).
- Godot-Promote (produktive Contextual Retrieval + BM25, ~24.593
  Chunks, ~5.7h parallel).

Die Beschleunigung ersetzt nicht die finale Qualitätsentscheidung
(`+0.02` avg_composite Schwelle), sondern macht die Läufe erst
wirtschaftlich. Es werden **keine** Evaluations-Ergebnisse erfunden —
3.3b/c führen die echten Läufe durch.

## Maßnahme 1: MPS GPU Encoding

- `KH_EMBEDDING_DEVICE` env var (default `cpu`, opt-in `mps`).
- `model_manager.py:get_embedder()` nutzt die env var statt des
  bisher hard-codierten `device="cpu"`. Der Cache-Key wird um das
  Device ergänzt (`embedder:<model>:<device>`), sodass ein
  Runtime-Switch keine falsch-Device-Instanz zurückliefert.
- **LIM-011 RESOLVED** (2026-07-04): `torch` 2.12.0 behebt den
  BGE-M3 + `transformers` 4.57.6 MPS-Deadlock. Auf Apple Silicon
  ergibt sich ein ~4.7× Speedup beim Encoding.
- **Pre-Flight-Mitigation (R1.1):** Vor jedem großen Build wird ein
  10-Texte MPS-Encode empfohlen; bei einem Hang (Timeout > 30 s)
  wird auf CPU zurückgefallen. Der Integration-Test
  `test_mps_encode_pre_flight` automatisiert diesen Check (10 Texte,
  < 30 s, kein Hang).
- Default bleibt `cpu` → vollständige Backward-Compat für Operatoren,
  die MPS nicht opt-in aktivieren.

## Maßnahme 2: Parallel LLM Calls

- `KH_LLM_WORKERS` env var (default `1` = sequenziell, Cloud Pro: `3`).
- `--workers N` CLI-Flag an `contextualize_chunks.py` (default aus env
  var, sonst `_DEFAULT_LLM_WORKERS = 1`).
- `contextualize_chunks()` Signatur erhält einen `workers: int = 1`
  Parameter. Bei `workers == 1` läuft der ursprüngliche sequenzielle
  Loop (factored-out `_contextualize_sequential`, identisches
  Verhalten, backward-compat). Bei `workers > 1` wird ein
  `ThreadPoolExecutor(max_workers=workers)` verwendet.
- Cache-Lookup bleibt sequenziell (vor Pool-Submit); nur die teuren
  LLM-Calls für Cache-Misses werden parallelisiert.
- Pro Worker ein eigener `_RetryClientProxy` (bereits so — wird pro
  `_generate_with_retry`-Call neu konstruiert).
- `get_llm()` wird vor ThreadPool-Start pre-warm aufgerufen, um eine
  Race im `_model_cache`-Dict zu vermeiden (B2).
- **SQLite-Safety:**
  - `open_cache()` setzt `check_same_thread=False` (Connection-Sharing
    über ThreadPool-Worker erlaubt).
  - `PRAGMA busy_timeout=5000` absorbiert residuale Write-Races (WAL
    Checkpoint contention).
  - Ein `threading.Lock` (`write_lock`) serialisiert die
    `put_cached`-Aufrufe im Main-Thread (Results werden gesammelt und
    sequenziell nach Batch geschrieben).
  - `threading.Lock` (`stats_lock`) schützt die Stats-Counter.
- **cancel_event bei HTTP 429 (Usage-Limit):** Ein
  `threading.Event` wird geteilt. Sobald ein Worker eine
  Usage-Limit-`RuntimeError` sieht, setzt der Main-Thread das Event,
  cancelt alle noch nicht gestarteten Futures und beendet das
  Draining. Worker, die das gesetzte Event beobachten, raisen eine
  "Usage limit reached — worker cancelled"-RuntimeError, die vom
  Main-Thread geschluckt wird (kein Crash, kein Datenverlust — der
  Cache bleibt für Resume intakt).
- Results sammeln, sequenziell nach Batch schreiben → kein
  nebenläufiger SQLite-Write nötig.

## Maßnahme 3: Inkrementelles Update (NICHT implementiert)

- MPS ersetzt den Bedarf an inkrementellen Updates: ein Vollrebuild
  dauert ~17 Min (Godot) bzw. ~45 Min (DaVinci) — schnell genug, um
  nach jedem repomix-Update einen Clean-Rebuild zu fahren.
- Inkrementelle Cache-Invalidation bleibt über
  `bulk_invalidate_by_source_file()` verfügbar, wird aber in 3.3a
  nicht weiter ausgebaut.

## Plan A: DaVinci Smoke-Test

- 1 Pfad-A-Chunk (`ui-map.md`), 1 LLM-Call (~5 s).
- MPS-Build ~45 Min (12.367 Chunks).
- **KEIN** `+0.02` Gate — nur Infrastruktur-Check:
  - Build läuft ohne Crash.
  - 1 Cache-Eintrag geschrieben, `context_prefix` nicht `None`.
  - Contextual BM25 aktiv (`--contextualize --contextualize-bm25`).
  - Keine Exception.
- Statt PMA (sinnlos bei unveränderten `late_chunk`-Metadaten) wird
  der Smoke-Test auf Infrastruktur-Indikatoren geprüft (Fix 6):
  Cache-Eintrag geschrieben, `context_prefix != None`, keine
  Exception, Build läuft.
- Direkte Produktivsetzung (R4: `late_chunk` folgt dem gleichen
  Parser-Pfad → Cache-Hits bei nachfolgenden Läufen).

## Plan B: Godot-Promote

- 24.593 Pfad-A-Chunks (alle — Godot hat keine `late_chunk`-Chunks).
- **R5:** 0 Cache-Hits (`rst-godot` ≠ `eval_b` `fallback_chunk` →
  `chunk_text_hash` divergiert). ~24.593 neue LLM-Calls.
- ~5.7h parallel (3 Workers, `gemma4:cloud`, ~2.5 s/Call).
- MPS-Build ~17 Min.
- Backup: `chromadb_data/godot.bak-pre-3-2`.
- Eval-Verifikation: `avg_composite` (keine Regression vs.
  Pre-Promote-Baseline, `godot-008`/`godot-012` pass erwartet).
- **B-R2-3 Fix:** `godot/context_cache.db` Schema-Initialisierung
  vor dem Promote. `contextualize_chunks.py:main()` öffnet den Cache
  jetzt immer (auch im Dry-Run) ganz am Anfang, sodass
  `init_schema()` läuft und eine leere/stale DB-Datei ein gültiges
  Schema bekommt (Fix 5).

## Risiken

- **R1.1 MPS-Hang → Pre-Flight 10 Texte, CPU-Fallback.**
  Integration-Test `test_mps_encode_pre_flight` automatisiert den
  Pre-Flight (10 Texte, < 30 s).
- **R1.2 MPS float32 → irrelevant** (produktiver Build, kein A/B).
- **R3 SQLite-Lock → `busy_timeout=5000` + `check_same_thread=False`
  + `write_lock`.** Integration-Test
  `test_parallel_cache_write_no_lock` verifiziert 3 konkurrierende
  `put_cached`-Aufrufe ohne `database is locked`.
- **B2 Thread-Safety → pre-warm `get_llm()`, pro Worker eigener
  `_RetryClientProxy`, `write_lock` um SQLite-Writes.**
- **B-R2-4 Cloud Concurrency → Spike-Test 3 parallele Calls vor dem
  5.7h-Lauf** (empfohlen, nicht in 3.3a implementiert).
- **R5 Cache-Miss → 24.593 neue LLM-Calls**, dokumentiert.
- **B-R2-5 Eval-Erwartung → Pre-Promote-Baseline** auf produktivem
  `godot` nötig (wird in 3.3c erhoben, nicht hier).

## Validierung

- **Unit** (`tests/unit/test_acceleration.py`, 10 Tests grün):
  - `test_kh_embedding_device_default_cpu`
  - `test_kh_embedding_device_mps`
  - `test_device_is_part_of_cache_key`
  - `test_busy_timeout_set`
  - `test_check_same_thread_false`
  - `test_workers_default_1_sequential`
  - `test_workers_3_uses_threadpool`
  - `test_cancel_event_on_usage_limit`
  - `test_workers_clamped_to_1_when_below`
  - `test_default_llm_workers_constant_is_1`
- **Integration** (`tests/integration/test_acceleration.py`, 2 Tests
  grün):
  - `test_parallel_cache_write_no_lock`
  - `test_mps_encode_pre_flight` (skipped auf Nicht-Apple-Silicon)
- **Smoke-Test:** DaVinci (folgt in 3.3b).
- **Eval:** Godot (folgt in 3.3c, keine Regression, `godot-008`/`012`
  pass erwartet).

## Constraints (Phase 3.3a)

- Kein Rebuild (folgt in 3.3b/c).
- Keine Eval (folgt in 3.3b/c).
- Keine Änderung an `embed_index.py`, `hybrid_search.py`,
  `bm25_search.py`, `parser_base.py`.
- Default `KH_EMBEDDING_DEVICE=cpu`, `KH_LLM_WORKERS=1` →
  vollständige Backward-Compat.
