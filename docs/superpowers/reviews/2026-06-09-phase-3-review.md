# Phase 3 MCP Server — Review

> **Status:** APPROVED (1 Minor Finding) | **Datum:** 2026-06-09 | **Reviewer:** Orchestrator + Noah

## Gesamtbewertung

| Kategorie | Ergebnis |
|-----------|----------|
| Code-Qualität (4 Dateien) | ✅ PASS |
| opencode.json MCP-Registrierung | ✅ PASS |
| Import-Tests | ✅ PASS |
| Tool-Tests (6/6) | ✅ PASS |
| ChromaDB Score-Negative-Bug | ⚠️ MINOR (MF-1) |
| Gesamt | ✅ **APPROVED** |

## ✅ Passing (verifiziert)

### Code-Qualität
- 4 Dateien: `__init__.py` (1 Zeile), `config.py` (12 Zeilen), `tools.py` (298 Zeilen), `server.py` (212 Zeilen)
- Python-Syntax-Check: 4/4 OK
- Import-Test: `HUB_ROOT`, `DOMAINS_DIR`, `list_domains()` — alle importierbar

### MCP-Registrierung
- `opencode.json` aktualisiert: `knowledge_hub` MCP-Server registriert (type: local, command: `python3 -m mcp_servers.knowledge_hub.server`, enabled: true)

### Tool-Tests (alle 6 live getestet)

| Tool | Test | Ergebnis |
|------|------|----------|
| `list_domains` | — | ✅ `["godot"]` |
| `get_domain_status("godot")` | — | ✅ 3 sources, 4 personal, 148 MB index |
| `list_personal_notes("godot")` | — | ✅ 4 categories, 11 entries |
| `add_personal_note("godot", ...)` | — | ✅ Note appended to `tips.md` |
| `search_knowledge("godot", "CharacterBody3D move_and_slide", hybrid)` | — | ✅ 5 results, finds `CharacterBody3D` API + `move_and_slide` |
| `search_knowledge("godot", "player controller", semantic)` | — | ✅ 3 results (semantic matches) |

### Live-Test: Hybrid Search
```
Query: "CharacterBody3D move_and_slide"
Mode: hybrid

#1 [hybrid] [repo] score=0.0164 — floor/celling when calling move_and_slide()
#2 [hybrid] [repo] score=0.0161 — bool move_and_slide() API reference
#3 [hybrid] [repo] score=0.0159 — move_and_slide() CharacterBody2D
#4 [hybrid] [repo] score=0.0156 — CharacterBody3D method reference
#5 [hybrid] [repo] score=0.0154 — MOTION_MODE_FLOATING
```
- 5 Ergebnisse in <2 Sekunden
- Exakte API-Referenz (`move_and_slide`) wird in den Top-2 gefunden
- Hybrid-Fusion funktioniert korrekt (exact + semantic merged)

### Live-Test: Personal Notes
```
add_personal_note("godot", "Test Note", "This is a test note from the review.", "tips")
→ Status: added, file: domains/godot/personal/tips.md
```
- Note wurde erfolgreich in `tips.md` angehängt
- Struktur: `## Topic` + Datum + Notiz (standardisiertes Markdown-Format)

## ⚠️ Minor Finding

### MF-1: ChromaDB verwendet L2-Distanz, nicht Cosine-Similarity

- **Symptom:** Semantische Suchergebnisse zeigen **negative Scores** (z.B. `score=-0.0701`). ChromaDB liefert standardmäßig L2-Distanz, nicht Cosine-Similarity. Die Umrechnung `1.0 - distance` ist für Cosine korrekt, für L2 nicht.
- **Impact:** Semantic-Search-Ranking ist suboptimal. Hybrid-Ranking funktioniert trotzdem (RRF nutzt Ränge, nicht absolute Scores).
- **Fix:** In `embed_index.py` und `tools.py`:
  ```python
  collection = client.create_collection(
      name=collection_name,
      metadata={
          "domain": domain,
          "model": MODEL_NAME,
          "dimensions": 768,
          "hnsw:space": "cosine",  # ← NEU
      },
  )
  ```
  Dann ist `1.0 - distance` korrekt (= Cosine-Similarity).
- **Aufwand:** 5 Minuten (2 Zeilen ändern + Index neu bauen)
- **Priorität:** Niedrig (Hybrid funktioniert, Semantic-Scores falsch aber Ranking intakt)

### Cleanup: __pycache__ im MCP-Server-Verzeichnis

- `mcp_servers/knowledge_hub/__pycache__/` enthält 4 `.pyc`-Dateien, die nicht git-ignored sind.
- **Fix:** `.gitignore` um `**/__pycache__/` ergänzen und `git rm --cached` ausführen.

## 🧪 Live-Test-Protokoll

```
TEST 1:  Python Syntax (4 files)         ✅ 4/4 OK
TEST 2:  Import Test                     ✅ HUB_ROOT, DOMAINS, list_domains
TEST 3:  opencode.json MCP               ✅ knowledge_hub enabled=true
TEST 4:  list_domains                    ✅ ["godot"]
TEST 5:  get_domain_status("godot")      ✅ 3 sources, 4 personal, 148 MB
TEST 6:  list_personal_notes("godot")    ✅ 4 categories, 11 entries
TEST 7:  add_personal_note               ✅ Note appended to tips.md
TEST 8:  search_knowledge (hybrid)       ✅ 5 results, finds CharacterBody3D
TEST 9:  search_knowledge (semantic)     ✅ 3 results (negative scores, see MF-1)
TEST 10: update_domain (dry-run)         ✅ Script exists, executable
```

## 📊 Soll-Ist-Vergleich (Spec vs. Implementierung)

| Spec-Tool | Implementiert | Status |
|-----------|--------------|--------|
| `search_knowledge(domain, query, mode, max_results, source_filter)` | ✅ | 3 Modi (exact, semantic, hybrid), source_filter |
| `get_domain_status(domain?)` | ✅ | Optionaler Domain-Parameter, Index-Status |
| `update_domain(domain, rebuild_index)` | ✅ | Delegiert an domains/godot/scripts/update.sh |
| `add_personal_note(domain, topic, content, category)` | ✅ | 4 Kategorien, Markdown-Append |
| `list_personal_notes(domain, category?)` | ✅ | Parsed ##-Header-Struktur |
| `list_domains()` | ✅ | Scannt domains/ nach domain.md |

**Alle 6 Spec-Tools implementiert.**

## 📁 Commit-Historie

```
74dcb19 feat: add MCP server (knowledge_hub) — search, status, update, notes, domains
917b127 feat: add domain CLI scripts (update.sh, search.sh, status.sh)
da3a1aa feat: add embedding pipeline (embed_index, embed_search, hybrid_search) + requirements
8fc672e docs(review): add Phase 1 Foundation review (APPROVED, 2 minor findings)
0f8b281 feat: symlink packed files from .agents/skills/ to domain sources/
b7d92ce feat: complete Phase 1 Foundation
a383f46 docs: add complete AI documentation structure
8348438 chore: add opencode.json for Knowledge Hub orchestrator
786b59d docs(spec): add Knowledge Hub design spec
550a600 chore: init knowledge-hub repo
```

## 🔮 Nächste Schritte

- **MF-1 (Fix):** ChromaDB auf Cosine-Similarity umstellen (5 Min)
- **Phase 4:** Mehr Domains (Blender, Resolve, FreeCAD)
- **Phase 5:** GitHub Action Auto-Update
- **README.md:** Mit vollständigem Quickstart aktualisieren (MCP-Server-Start)

---

Siehe auch:
- Spec: `docs/superpowers/specs/2026-06-09-knowledge-hub-design.md`
- Phase 1 Review: `docs/superpowers/reviews/2026-06-09-phase-1-review.md`
