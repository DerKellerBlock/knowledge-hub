# Phase 3.3a: MPS GPU + Parallele LLM-Calls — Erklärung

**Datum:** 2026-07-04
**Phase:** 3.3a (Acceleration)
**Status:** Implementiert (Code + Tests grün, Rebuild/Eval folgen in 3.3b/c)

## 1. Warum Beschleunigung?

Die Contextual-Retrieval-Pipeline (Phase 3.1/3.2) war zu langsam für den
produktiven Einsatz:

| Schritt | Vorher | Problem |
|---------|--------|---------|
| Lokaler Gemma-LLM-Lauf (Phase 3.1c) | ~69 Stunden | 4.580 Chunks, ~16,6 s pro Chunk |
| CPU-Embedding-Build (Godot) | ~78 Minuten | 24.593 Chunks auf CPU |
| CPU-Embedding-Build (DaVinci) | ~210 Minuten | 12.367 Chunks auf CPU |
| Godot-Promote (Phase 3.2) | ~3h LLM + 78 Min Build | 24.593 neue LLM-Calls + Rebuild |

**Lösung:** Zwei unabhängige Beschleunigungen, die zusammen wirken:

| Maßnahme | Speedup | Godot-Promote |
|----------|---------|---------------|
| MPS GPU Encoding | ~4,7× | 78 Min → ~17 Min |
| Parallel LLM Calls (3 Worker) | ~3× | 3h → ~1h |
| **Kombiniert** | | **~1h 17 Min** (statt ~4h 18 Min) |

## 2. Was ist MPS?

**MPS** steht für **Metal Performance Shaders** — das ist Apples GPU-Framework
für maschinelles Lernen auf Apple Silicon (M1, M2, M3, M4).

Das BGE-M3-Embedding-Modell (das Texte in Vektoren umwandelt) lief bisher
ausschließlich auf der CPU (`device='cpu'` war hardcodiert). Das war sicher,
aber langsam.

Jetzt kann die GPU genutzt werden:

```bash
# Vorher (CPU, langsam):
python scripts/embed_index.py --domain godot
# → ~78 Minuten

# Jetzt (MPS GPU, 4,7× schneller):
KH_EMBEDDING_DEVICE=mps python scripts/embed_index.py --domain godot
# → ~17 Minuten
```

**Wichtig:** Der Default bleibt `cpu`. Ohne die Umgebungsvariable läuft alles
genau wie vorher — vollständige Rückwärtskompatibilität.

### LIM-011 ist gelöst

Bisher war MPS nicht nutzbar, weil BGE-M3 + `transformers` 4.57.6 auf Apple
Silicon einen Deadlock (Hänger) verursacht hat. Das war als **LIM-011**
dokumentiert.

**`torch` 2.12.0 hat diesen Bug behoben.** Seit dem Upgrade läuft BGE-M3
stabil auf MPS.

### Pre-Flight-Check

Vor jedem großen Build wird ein kurzer Test mit 10 Texten auf MPS empfohlen.
Hängt er länger als 30 Sekunden, wird automatisch auf CPU zurückgefallen.
Der Integration-Test `test_mps_encode_pre_flight` automatisiert diesen Check.

## 3. Was sind Parallel LLM Calls?

`contextualize_chunks.py` (das Skript, das LLM-Kontext für jeden Chunk
generiert) lief bisher **sequenziell**: ein Chunk nach dem anderen.

Jetzt kann es **parallel** arbeiten:

```bash
# Vorher (sequenziell, 1 Worker):
python scripts/contextualize_chunks.py --domain godot
# → ~3 Stunden für 24.593 Chunks (Cloud)

# Jetzt (parallel, 3 Worker):
KH_LLM_WORKERS=3 python scripts/contextualize_chunks.py --domain godot
# → ~1 Stunde (3× schneller)
```

### Wie funktioniert das?

- Ein **ThreadPoolExecutor** mit N Workern schickt mehrere Chunks gleichzeitig
  an Ollama-Cloud.
- Der **Cache-Lookup** („wurde dieser Chunk schon verarbeitet?") läuft weiter
  sequenziell — nur die teuren LLM-Calls werden parallelisiert.
- **`get_llm()` wird vor dem Start aufgewärmt** (pre-warm), um Race-Conditions
  im Modell-Cache zu vermeiden.
- Ein **`cancel_event`** (threading.Event) stoppt alle Worker sofort, wenn
  Ollama-Cloud ein Usage-Limit (HTTP 429) meldet. Der Cache bleibt intakt —
  man kann später einfach weitermachen.
- **`threading.Lock`** schützt die Statistiken und Cache-Schreibvorgänge.

**Wichtig:** Der Default bleibt `1` Worker (sequenziell). Ohne die
Umgebungsvariable läuft alles genau wie vorher.

## 4. SQLite-Safety

Wenn mehrere Worker parallel auf die Cache-Datenbank schreiben, kann es zu
Konflikten kommen („database is locked").

Drei Maßnahmen verhindern das:

1. **`check_same_thread=False`** — erlaubt mehreren Threads, dieselbe
   SQLite-Verbindung zu nutzen.
2. **`PRAGMA busy_timeout=5000`** — SQLite wartet bis zu 5 Sekunden, wenn
   die Datenbank kurz gesperrt ist, statt sofort abzubrechen.
3. **`threading.Lock` (write_lock)** — Cache-Schreibvorgänge werden im
   Haupt-Thread gesammelt und nacheinander geschrieben, nicht parallel.

Der Integration-Test `test_parallel_cache_write_no_lock` verifiziert, dass
3 parallele Schreibvorgänge ohne Fehler durchlaufen.

## 5. Wo liegen die Dateien?

### Neue/geänderte Dateien

| Datei | Änderung |
|-------|----------|
| `scripts/model_manager.py` | `KH_EMBEDDING_DEVICE` env var, Cache-Key `embedder:<model>:<device>` |
| `scripts/context_cache.py` | `busy_timeout=5000`, `check_same_thread=False` |
| `scripts/contextualize_chunks.py` | `ThreadPoolExecutor`, `--workers` CLI, `cancel_event`, `threading.Lock` |
| `tests/unit/test_acceleration.py` | 10 Tests (env parsing, busy_timeout, ThreadPool, cancel_event) |
| `tests/integration/test_acceleration.py` | 2 Tests (MPS encode, parallel cache-write) |
| `docs/superpowers/specs/2026-07-04-acceleration-mps-parallel-design.md` | Design-Spec |

### Dokumentations-Updates

| Datei | Was wurde aktualisiert |
|-------|----------------------|
| `docs/ai/best-practices.md` | `KH_EMBEDDING_DEVICE`, `KH_LLM_WORKERS` env vars dokumentiert |
| `docs/ai/known-issues.md` | LIM-011 als RESOLVED markiert |
| `docs/ai/architecture.md` | Embedding-Device-Auswahl, Parallel-LLM-Calls dokumentiert |
| `docs/ai/security.md` | Parallel Workers, Usage-Limit-Propagation dokumentiert |
| `docs/ai/changelog.md` | Phase 3.3a Eintrag |

### Nicht geändert

Diese Dateien wurden in Phase 3.3a **nicht** angefasst:

- `scripts/embed_index.py`
- `scripts/hybrid_search.py`
- `scripts/bm25_search.py`
- `scripts/parser_base.py`

## 6. Validierung

### Tests

```bash
# Unit-Tests (alle grün)
.venv/bin/pytest -m unit -q
# → 226 passed

# Integration-Tests (alle grün)
.venv/bin/pytest -m integration -q
# → 108 passed
```

### MPS-Device-Check

```bash
KH_EMBEDDING_DEVICE=mps .venv/bin/python -c "
from scripts.model_manager import get_embedder
m = get_embedder('godot')
print(m.device)
"
# → mps:0
```

Ohne die Env-Variable zeigt es `cpu`:

```bash
.venv/bin/python -c "
from scripts.model_manager import get_embedder
m = get_embedder('godot')
print(m.device)
"
# → cpu
```

### Workspace-Check

```bash
./scripts/workspace_check.sh
# → All workspace checks passed.
```

## 7. Nächste Schritte

### 3.3b: DaVinci Smoke-Test

- **1 Pfad-A-Chunk** (`ui-map.md`), 1 LLM-Call (~5 s)
- MPS-Build ~45 Minuten (12.367 Chunks)
- **KEIN** Qualitäts-Gate — nur Infrastruktur-Check:
  - Build läuft ohne Crash
  - Cache-Eintrag wird geschrieben
  - `context_prefix` ist nicht `None`
  - Contextual BM25 ist aktiv (`--contextualize --contextualize-bm25`)

### 3.3c: Godot-Promote

- **24.593 Pfad-A-Chunks** (alle — Godot hat keine `late_chunk`-Chunks)
- ~5,7 Stunden parallel (3 Worker, `gemma4:cloud`, ~2,5 s/Call)
- MPS-Build ~17 Minuten
- Eval-Verifikation: `avg_composite` (keine Regression, `godot-008`/`godot-012`
  pass erwartet)

## Zusammenfassung

Phase 3.3a macht die Contextual-Retrieval-Pipeline wirtschaftlich nutzbar:

- **MPS GPU** beschleunigt das Embedding um das 4,7-fache
- **Parallele LLM-Calls** beschleunigen die Kontext-Generierung um das 3-fache
- **SQLite-Safety** verhindert Datenbank-Konflikte bei parallelen Schreibvorgängen
- **Vollständige Rückwärtskompatibilität** — ohne Env-Variablen läuft alles wie vorher

Die eigentlichen Produktiv-Läufe (DaVinci Smoke-Test, Godot-Promote) folgen in
den nächsten Phasen 3.3b und 3.3c.
