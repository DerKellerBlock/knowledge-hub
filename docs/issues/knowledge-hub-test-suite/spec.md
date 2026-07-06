# Knowledge Hub — Test Suite Design Spec

**Date:** 2026-06-28
**Status:** Draft
**Owner:** Knowledge Hub

## Ziel

Aufbau eines vierschichtigen, automatisierten Test-Suites für den Knowledge Hub,
der verifiziert, dass Information Retrieval (Suchen + Wiedergabe) tatsächlich
funktioniert — nicht nur dass Code kompiliert oder dass irgendwelche Ergebnisse
zurückkommen, sondern dass die **gefundenen Inhalte inhaltlich korrekt und
vollständig** sind.

Der Knowledge Hub hatte bisher nur ein manuelles `validate_search.py`-Script,
das zwar Latenz und Mindestanzahl prüft, aber NICHT ob die Ergebnisse relevant
sind, ob Texte vollständig sind, ob BM25 exakte Treffer findet, ob Reranking
korrekt sortiert, ob Personal Notes korrekt gespeichert werden, oder ob
Domain-Scoping fehlerhafte Zugriffe blockt.

## Architektur-Ansatz

Vier Test-Schichten mit klarer Trennung, abgestuft nach Laufzeit und Abhängigkeiten:

```
Schicht 1: Unit-Tests         → pytest, schnell, isoliert, keine Modelle/DB
Schicht 2: Integration-Tests   → pytest, mit temporärer ChromaDB + Dummy-Daten
Schicht 3: E2E-Regression     → pytest, mit echtem Godot/DaVinci-Index
Schicht 4: MCP-Contract-Tests  → pytest-asyncio, MCP-Tool-Aufrufe
```

## Schicht 1: Unit-Tests (schnell, isoliert)

**Ziel:** Pure Logik testen, ohne Modelle zu laden oder eine ChromaDB zu starten.
Laufzeit: < 5 Sekunden. Keine Netzwerk-/Model-Downloads.

### Module unter Test
- `mcp_servers/knowledge_hub/config.py`: Path-Helper
- `scripts/model_manager.py`: Regex-Parsing, BM25-Cache-LRU, Domain-Config-Reader
- `mcp_servers/knowledge_hub/tools.py`: Domain-Scoping, Category-Validierung, Note-Parsing
- `scripts/bm25_search.py`: Tokenizer (pure Funktion)
- `scripts/hybrid_search.py`: RRF-Fusion (pure Funktion)
- `scripts/parser_base.py`: `fallback_chunk`, `Chunk.to_chromadb_metadata` / `from_chromadb_metadata`

### Test-Dateien
- `tests/unit/test_config.py`
- `tests/unit/test_model_manager.py`
- `tests/unit/test_tools.py`
- `tests/unit/test_bm25_tokenizer.py`
- `tests/unit/test_rrf_fusion.py`
- `tests/unit/test_parser_base.py`

### Beispiel-Tests (inhaltlich)

**config.py:**
- `domain_chroma_path("godot")` → `…/chromadb_data/godot/chroma`
- `domain_bm25_path("davinci_resolve")` → `…/chromadb_data/davinci_resolve/davinci_resolve_bm25.pkl`
- `legacy_bm25_path("godot")` → `…/chromadb_data/godot_bm25.pkl`
- `legacy_collection_path("godot")` → `…/chromadb_data/godot_knowledge`

**model_manager.py:**
- `_DOMAIN_META_RE` matched auf einer echten `domain.md` (godot, davinci_resolve)
- `_DOMAIN_META_RE` matched NICHT, wenn keine `## Metadaten`-Sektion existiert
- `_EMBEDDING_MODEL_RE` extrahiert `all-mpnet-base-v2` aus `- Embedding-Model: all-mpnet-base-v2 (768 dims)`
- `_EMBEDDING_MODEL_RE` extrahiert `all-MiniLM-L6-v2` aus `- Embedding-Model: all-MiniLM-L6-v2`
- `get_domain_config("nonexistent")` → Fallback-Dict mit `DEFAULT_MODEL_NAME` und `nonexistent_knowledge`
- BM25-Cache: `bm25_cache_set("d1", {})` + `bm25_cache_set("d2", {})` + … + `bm25_cache_set("d4", {})` → `d1` evicted (BM25_CACHE_MAX=3)
- BM25-Cache: `bm25_cache_get("d2")` nach LRU-Update → ist noch da
- BM25-Cache: `bm25_cache_invalidate("d2")` → `bm25_cache_get("d2")` ist None

**tools.py:**
- `set_domain_scope(["godot"])` → `_check_domain_scope("godot")` ist None, `_check_domain_scope("davinci_resolve")` liefert Error-Dict
- `set_domain_scope(["nonexistent"])` → `ValueError`
- `set_domain_scope(None)` → alle Domains sichtbar, `_check_domain_scope` immer None
- `set_domain_scope([])` → alle Domains sichtbar
- `_CATEGORY_RE` matched auf `gotchas`, `tips`, `best-practices`, `faq`; matched NICHT auf `Gotchas`, `up/per`, `` (leer)
- `list_personal_notes` Parser: Test mit einer Dummy-Datei, die 2 Einträge enthält → beide Einträge als Dicts zurück

**bm25_search.py:**
- `tokenize("Node3D rotate_y")` → `["node3d", "rotate_y"]`
- `tokenize("  multiple   spaces  ")` → `["multiple", "spaces"]`
- `tokenize("")` → `[]`
- `tokenize("CamelCaseString")` → `["camelcasestring"]`

**hybrid_search.py (RRF):**
- `rrf_fusion([], [])` → `[]`
- `rrf_fusion(sparse=[chunk_id="A"], dense=[chunk_id="A"])` → 1 Ergebnis, `stage1_sources=["bm25", "semantic"]`, score > 0
- `rrf_fusion(sparse=[chunk_id="A"], dense=[chunk_id="B"])` → 2 Ergebnisse, Rang 1 hat höheren Score (wenn BM25 + Dense zusammen)
- Top-N-Limit: `rrf_fusion(sparse=[…10 Chunks…], dense=[…10 Chunks…], top_n=5)` → genau 5 Ergebnisse

**parser_base.py:**
- `fallback_chunk` mit `chunk_size=100, overlap=20` und 250 chars Text → 3 Chunks (Start: 0, 80, 160)
- `fallback_chunk` mit leerem Text → `[]`
- `Chunk.to_chromadb_metadata()` enthält `source_type`, `domain`, `source_file`, `line_start`, `line_end`
- `Chunk.to_chromadb_metadata()` mit `inherits_from=["Node"]` → `meta["inherits_from"]` ist JSON-String `'["Node"]'`
- `Chunk.from_chromadb_metadata` round-trip: `Chunk(...)` → `to_chromadb_metadata()` → `from_chromadb_metadata()` → gleiche Felder
- `Chunk.to_chromadb_metadata()` mit `None`-Feldern → diese Keys fehlen im Dict (werden nicht als `None` gespeichert)

## Schicht 2: Integration-Tests (mit temporärer ChromaDB)

**Ziel:** Die Such- und Indexierungs-Pipeline mit einer **echten temporären
ChromaDB-Instanz** und kleinen Dummy-Quellen testen. Keine echten 24.552 Chunks
laden — nur 3-5 Dummy-Markdown-Dateien. Laufzeit: ~30-60 Sekunden (Embedding-
Modell laden + kleine Indexierung).

### Module unter Test
- `scripts/embed_index.py`: `build_index` mit Dummy-Domain
- `scripts/bm25_search.py`: `bm25_search`, `build_bm25_index` mit echtem Index
- `scripts/embed_search.py`: `semantic_search` mit echtem Index
- `scripts/hybrid_search.py`: `search` mit mode=exact/semantic/hybrid
- `scripts/migration.py`: `migrate_legacy_layout` Idempotenz + Backup
- `mcp_servers/knowledge_hub/tools.py`: `add_personal_note`, `list_personal_notes`

### Fixtures
- `tests/conftest.py`: 
  - `tmp_hub` Fixture: erstellt ein temporäres `HUB_ROOT`-Verzeichnis mit `domains/`, `chromadb_data/`, `scripts/`, `mcp_servers/` und monkeypatched die Modul-Pfade
  - `dummy_domain` Fixture: erstellt `domains/dummy/sources/dummy-source.md` (3 kurze Abschnitte über "Node3D rotation", "Camera follow", "Audio bus") + `domains/dummy/personal/gotchas.md` (1 Eintrag)
  - `indexed_dummy` Fixture: baut den Index für `dummy_domain` (nutzt `tmp_hub`)
  - Skip-Marker wenn ChromaDB/embedding-Model nicht verfügbar

### Test-Dateien
- `tests/integration/test_embed_index.py`
- `tests/integration/test_bm25_search.py`
- `tests/integration/test_embed_search.py`
- `tests/integration/test_hybrid_search.py`
- `tests/integration/test_migration.py`
- `tests/integration/test_personal_notes.py`

### Beispiel-Tests (inhaltlich)

**embed_index.py:**
- `build_index("dummy")` → Collection `dummy_knowledge` existiert, `coll.count()` == Anzahl Chunks aus Dummy-Quellen
- `build_index("dummy")` 2× aufgerufen → 2. Lauf ersetzt die Collection (keine Duplikate)
- BM25-Pickle existiert nach `build_index`
- Chunks haben korrekte Metadaten (`source_type="repo"`, `source_file="dummy-source.md"`, `domain="dummy"`)

**bm25_search.py:**
- `bm25_search("dummy", "Node3D rotate")` → mind. 1 Ergebnis mit `chunk_id` aus der "Node3D rotation"-Section
- `bm25_search("dummy", "nonexistentword12345")` → `[]` (score 0 wird gefiltert)
- `bm25_search("dummy", "Node3D rotate", top_k=1)` → genau 1 Ergebnis

**embed_search.py:**
- `semantic_search("dummy", "How to rotate a 3D node")` → mind. 1 Ergebnis, `source_file` ist gesetzt, `text` ist nicht leer
- `semantic_search("dummy", "nonexistentword12345")` → Liste mit 0 oder wenigen Einträgen (ChromaDB liefert immer n_results, auch bei schlechter Query)

**hybrid_search.py:**
- `search("dummy", "Node3D rotate", mode="exact")` → BM25-only, `match_type="bm25"` in Ergebnissen
- `search("dummy", "Node3D rotate", mode="semantic")` → `match_type="semantic"` in Ergebnissen
- `search("dummy", "Node3D rotate", mode="hybrid")` → `match_type="hybrid"` in Ergebnissen
- `search("dummy", "Node3D rotate")` → `total_found >= 1`, `query_time_ms` vorhanden, `results[0]["text"]` nicht leer
- `source_filter=["personal"]` → alle Ergebnisse haben `source_type == "personal"`
- `source_filter=["repo"]` → alle Ergebnisse haben `source_type == "repo"`
- Return-Dict-Struktur: enthält `results`, `total_found`, `mode`, `query_time_ms`

**migration.py:**
- Idempotenz: `migrate_legacy_layout()` mit leerem `chromadb_data/` → `False` (nichts migriert)
- Idempotenz: 2× aufrufen → 2. Aufruf `False`
- Legacy-Layout simulieren: erstelle `chromadb_data/dummy_knowledge/` + `chromadb_data/dummy_bm25.pkl` → `migrate_legacy_layout()` → `True`, neue Pfade existieren, alte nicht mehr
- Orphaned-BM25: nur `chromadb_data/dummy_bm25.pkl` + `chromadb_data/dummy/` (bereits migriert collection) → Second-Pass migriert BM25, `True`
- Backup: `_legacy_backup/` existiert nach Migration, enthält Kopien

**tools.py (personal notes):**
- `add_personal_note("dummy", "Test topic", "Test content", "gotchas")` → `status: "added"`, Datei existiert
- `list_personal_notes("dummy")` → enthält `"gotchas"`-Key mit mind. 1 Eintrag
- `add_personal_note("dummy", "Topic", "Content", "Invalid/Category")` → `error`-Key im Return (Category-Regex)
- `add_personal_note("dummy", "Topic", "Content", "UPPERCASE")` → `error`-Key (nur lowercase erlaubt)

## Schicht 3: E2E-Regression (mit echtem Index)

**Ziel:** Verifiziert, dass die **realen** Godot- und DaVinci-Indizes korrekte,
inhaltlich relevante Ergebnisse liefern. Ersetzt das manuelle `validate_search.py`
durch automatisierte Assertions mit Relevanz-Checks. Laufzeit: ~10-30 Sekunden
pro Domain (Index bereits gebaut, Suche läuft).

### Voraussetzung
- `chromadb_data/godot/` und `chromadb_data/davinci_resolve/` existieren (vorab gebaut)
- Tests werden übersprungen (skip), wenn Index fehlt — kein automatischer Build im Test

### Test-Datei
- `tests/e2e/test_godot_regression.py`
- `tests/e2e/test_davinci_regression.py`

### Beispiel-Tests (inhaltlich)

**Godot:**
- `test_godot_node3d_search_finds_relevant_results`: `search("godot", "Node3D rotate")` → `total_found >= 1`, kombinierte Texte der Top-3-Ergebnisse enthalten "Node3D" oder "Spatial" oder "rotate"
- `test_godot_search_returns_metadata`: erstes Ergebnis hat `source_file`, `text` nicht leer, `chunk_id` startet mit `"godot::"`
- `test_godot_search_modes_all_work`: exact, semantic, hybrid liefern alle `total_found >= 1`
- `test_godot_hybrid_is_not_slower_than_10s`: `query_time_ms <= 10000`

**DaVinci:**
- `test_davinci_trim_clip_search_finds_relevant_results`: `search("davinci_resolve", "trim clip edit")` → `total_found >= 1`, Top-3-Texte enthalten "trim" oder "edit" (case-insensitive)
- `test_davinci_color_grading_search`: `search("davinci_resolve", "color grading primary correction")` → `total_found >= 1`, Top-3-Texte enthalten "color" oder "primary"
- `test_davinci_render_deliver_search`: `search("davinci_resolve", "render deliver settings")` → `total_found >= 1`, Top-3-Texte enthalten "deliver" oder "render"
- `test_davinci_search_returns_pdf_metadata`: mind. 1 Ergebnis hat `page_start` gesetzt (PDF-Seitennummer)
- `test_davinci_hybrid_is_not_slower_than_10s`: `query_time_ms <= 10000`

## Schicht 4: MCP-Contract-Tests

**Ziel:** Die 6 MCP-Tools über ihre tatsächlichen Funktionen aufrufen (nicht
über stdio-Transport) und den Return-Contract verifizieren. Verwendet
pytest-asyncio für die `@server.call_tool()`-Handler.

### Module unter Test
- `mcp_servers/knowledge_hub/server.py`: `call_tool_handler`, `list_tools_handler`
- `mcp_servers/knowledge_hub/tools.py`: alle 6 Tool-Funktionen

### Test-Datei
- `tests/mcp/test_mcp_contract.py`

### Beispiel-Tests (inhaltlich)

**list_domains (scoped):**
- Vor `set_domain_scope`: `list_scoped_domains()` == `list_domains()` (alle sichtbar)
- Nach `set_domain_scope(["godot"])`: `list_scoped_domains()` == `["godot"]`
- Tool-Handler `list_domains` liefert `{"domains": [...], "count": N}`

**search_knowledge:**
- `search_knowledge(domain="godot", query="Node3D")` → Dict mit `results`, `total_found`, `mode`, `query_time_ms`
- `search_knowledge(domain="nonexistent", query="test")` → Exception oder Error-Dict (je nach Implementierung)
- Mit `set_domain_scope(["godot"])`: `search_knowledge(domain="davinci_resolve", query="test")` → `{"error": "Domain 'davinci_resolve' not available in this server scope. Available: ['godot']"}`

**get_domain_status:**
- `get_domain_status("godot")` → Dict mit `sources`, `personal_notes`, `index_exists`, `index_size_mb`, `bm25_index_size_mb`
- `get_domain_status()` (ohne Argument) → Dict mit allen scoped Domains als Keys
- Mit Scope `["godot"]`: `get_domain_status("davinci_resolve")` → Error-Dict

**add_personal_note / list_personal_notes:**
- `add_personal_note(domain="dummy", topic="Test", content="Content")` → `status: "added"`
- `list_personal_notes(domain="dummy")` → Dict mit Notes
- `add_personal_note(domain="dummy", topic="T", content="C", category="bad/cat")` → Error-Dict

**update_domain:**
- `update_domain(domain="nonexistent")` → Error-Dict (`No update.sh found`)

**list_tools_handler:**
- Liefert 6 Tools mit korrekten `name`, `description`, `inputSchema` (JSON-Schema)

## Test-Infrastruktur

### pytest-Konfiguration
- `pyproject.toml` mit `[tool.pytest.ini_options]`:
  - `testpaths = ["tests"]`
  - `markers = ["unit: fast isolated tests", "integration: with tmp ChromaDB", "e2e: with real index", "mcp: MCP contract tests"]`
  - `addopts = "--strict-markers"`
- `tests/conftest.py` mit gemeinsamen Fixtures

### Requirements
- `requirements-dev.txt` (neu): `pytest>=8.0`, `pytest-asyncio>=0.23`, `pytest-cov>=4.0`
- Runtime-Requirements (`requirements.txt`) bleiben unverändert

### CI-Integration (vorbereitet, nicht aktiv)
- `.github/workflows/tests.yml` (Stub für später): führt `pytest -m unit` (schnell, bei jedem PR) und `pytest -m "integration or e2e"` (nur bei Änderungen an scripts/ oder domains/) aus
- Aktuell: Tests laufen lokal manuell

### Test-Ausführung
```bash
# Alle Tests
pytest

# Nur Unit (schnell, < 5s)
pytest -m unit

# Nur Integration (~60s)
pytest -m integration

# E2E mit echtem Index (~30s)
pytest -m e2e

# MCP-Contract
pytest -m mcp

# Mit Coverage
pytest --cov=scripts --cov=mcp_servers/knowledge_hub --cov-report=term-missing
```

## Out of Scope

- **Keine** Mock-Tests für SentenceTransformer (zu komplex, Modell-Download ist Teil des Integration-Tests)
- **Keine** Performance-Benchmarks (Latenz wird in E2E-Tests geprüft, aber keine Microbenchmarks)
- **Keine** UI-Tests (kein UI vorhanden)
- **Keine** Lasttests (Single-User-MCP-Server)
- **Keine** automatische Index-Rebuilds im Test (E2E erwartet vorgebauten Index)
- **Keine** GitHub-Actions-CI-Activation in diesem Spec (nur Stub-Vorbereitung)

## Erfolgskriterien

1. `pytest -m unit` läuft in < 10 Sekunden und ist zu 100% grün
2. `pytest -m integration` läuft in < 120 Sekunden und ist zu 100% grün
3. `pytest -m e2e` läuft in < 60 Sekunden und ist zu 100% grün (vorausgesetzt Indizes existieren)
4. `pytest -m mcp` läuft in < 30 Sekunden und ist zu 100% grün
5. `pytest --cov` zeigt Coverage > 60% für `scripts/` und `mcp_servers/knowledge_hub/`
6. Tests verifizieren **inhaltliche Korrektheit** (Relevanz der Ergebnisse), nicht nur Struktur
7. Tests sind idempotent und hinterlassen keine Reste (tmp_path für Integration)
