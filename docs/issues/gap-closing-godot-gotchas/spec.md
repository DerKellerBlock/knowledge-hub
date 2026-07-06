# Gap-Closing: GitHub-Issue-basierte Gotchas kuratieren — Design Spec

> **Status:** Approved (implementiert 2026-06-30) | **Datum:** 2026-06-30 | **Autor:** plan-hub-change
>
> Abgeleitet aus: Manuelle Real-World Evaluation vom 2026-06-30 (archiviert unter `docs/superpowers/quality-reports/2026-06-30-godot-real-world-eval.md`), bestehender Quality Evaluation Platform.

## Vision

Die erste manuelle Real-World Evaluation hat 4 inhaltliche Gaps in der Godot-Domain aufgedeckt — allesamt GitHub Issues/PRs mit Bug-Workarounds, die im Hub nicht dokumentiert waren. Diese Spec schließt diese Gaps durch Kuratierung neuer `personal/gotchas.md`- und `personal/tips.md`-Einträge, gefolgt von einem Index-Rebuild und Re-Evaluation.

## Die 4 Gaps

1. **Gap 1 (godot-002):** Area3D Gravity Bug #112656 — `get_gravity()` ignoriert Area3D-Overrides
2. **Gap 2 (godot-003):** 3 Jolt Physics Bugs — #117857 (move_and_collide null collision), #112315 (apply_floor_snap catapulting), #113058 (Reparenting Area3D trigger)
3. **Gap 3 (godot-005):** GLB Mesh Origin Bug #111653 — Mesh origin verschiebt sich beim Skalieren
4. **Gap 4 (godot-007):** Native Stair Stepping PR #114447 — step_enabled, step_height für CharacterBody3D

## Architektur

Keine neuen Komponenten — nutzt ausschließlich bestehende Infrastruktur:
- `domains/godot/personal/gotchas.md` ← 5 neue Einträge (Gaps 1-3)
- `domains/godot/personal/tips.md` ← 1 neuer Eintrag (Gap 4)
- `quality/golden/godot.yaml` ← expected_source_files erweitert (gotchas.md für godot-002, tips.md für godot-007)
- `domains/godot/domain.md` ← Letztes Update aktualisiert
- `scripts/embed_index.py --domain godot` ← Rebuild (ChromaDB + BM25)
- `scripts/quality/run_evaluation.py` + `generate_report.py` ← Re-Evaluation + Report

## Implementierung

- 5 neue `##`-Abschnitte in gotchas.md (jeder Bug eigener Abschnitt, bestehende Einträge unverändert)
- 1 neuer Tipp in tips.md (Stair Stepping, im kurzen Tipps-Format)
- Golden Dataset: gotchas.md zu godot-002 expected_source_files hinzugefügt; tips.md zu godot-007
- Index neu gebaut (24552 Chunks, ChromaDB ~373 MB, BM25 11 MB)
- Backup vor Rebuild erstellt und nach Erfolg entfernt

## Re-Evaluation Ergebnisse

| Frage | Vorher (Composite) | Nachher (Composite) | Änderung |
|-------|-------------------|---------------------|----------|
| godot-001 | 0.8594 pass | 0.8594 pass | unverändert |
| godot-002 | 0.8594 pass | 0.8594 pass | gotchas.md in found_sources |
| godot-003 | 0.8594 pass | 0.8594 pass | gotchas.md in found_sources |
| godot-004 | 0.8594 pass | 0.8594 pass | unverändert |
| godot-005 | 0.8594 pass | **0.4219 weak** | Regression — gotchas.md nicht in Top-10 (Ranking-Schwäche) |
| godot-006 | 0.8594 pass | 0.8594 pass | unverändert |
| godot-007 | 0.8594 pass | 0.7136 pass | tips.md in found_sources |

**Avg Composite: 0.8594 → 0.7761**

## Bekanntes Finding: godot-005 Regression

godot-005 fiel von pass (0.86) auf weak (0.42), weil `gotchas.md` nicht in den Top-10 Suchergebnissen für "How do I fix GLB model import scale issues from Meshy" erscheint. Stattdessen rankt `best-practices.md` (Score 1.03) und `godot-docs-reference-packed.md` (GLTFDocument-Methoden) höher. Der neue GLB-Mesh-Origin-Gotcha-Eintrag ist indexiert, aber die hybride Suche rankt ihn für diese generische Frage nicht hoch genug.

Das ist eine **Ranking-Schwäche**, kein Implementierungsfehler. Bei spezifischen Queries ("Mesh Origin Bug Generate LODs") taucht gotchas.md ebenfalls nicht auf — das legt nahe dass das Cross-Encoder-Reranking die API-Referenz-Methoden (generate_lods, ImporterMesh) stärker gewichtet als die personal notes für diese Frage.

**Follow-up:** Entweder (a) die Frage spezifischer formulieren, (b) Ranking-Tuning (Cross-Encoder-Gewichtung für personal notes), oder (c) Chunk-Splitting für gotchas.md damit einzelne Einträge besser ranken können.

## Out of Scope

- Andere Domains (DaVinci hatte 0 Gaps)
- Automatisches GitHub-Issue-Scraping
- Ranking-Optimierung
- Golden Dataset real_world_sources (bereits vollständig kuratiert)

## Erfolgskriterien

1. ✅ 5 neue Gotcha-Einträge + 1 Tip-Eintrag im konsistenten Format
2. ✅ Index neu gebaut ohne Fehler
3. ⚠️ Re-Evaluation: 6/7 pass, 1 weak (godot-005 Regression — dokumentiertes Finding)
4. ✅ Neuer Report archiviert
5. ✅ Gotcha-Format konsistent (Problem → Ursache → Workaround → Datum → Status)
