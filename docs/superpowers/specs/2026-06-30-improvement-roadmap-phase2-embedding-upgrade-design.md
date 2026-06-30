# Improvement Roadmap Phase 2 — Embedding-Modell-Wechsel & Quality Gate — Design Spec

> **Status:** Draft | **Datum:** 2026-06-30 | **Autor:** Orchestrator
>
> Abgeleitet aus: Interne Inventarisierung + externe Recherche (Stand 2026-06-30), 20 identifizierte Verbesserungspotentiale, Roadmap-Phasenplanung.
> Referenziert: `docs/superpowers/specs/2026-06-29-knowledge-hub-quality-evaluation-platform-design.md`, `docs/superpowers/specs/2026-06-30-improvement-roadmap-phase1-low-hanging-fruit-design.md`

## Zusammenfassung

Phase 2 adressiert den Kern der Retrieval-Qualität: Wechsel des Embedding-Modells von `all-mpnet-base-v2` (English-only, 768d) zu `BAAI/bge-m3` (multilingual, 1024d, 8192 Token Kontext), Late Chunking für PDF-Domains, ein CI Quality Regression Gate und die Erweiterung des Golden Dataset auf 20–30 Fragen pro Domain. Diese Phase erfordert vollständige Index-Rebuilds und ist die Voraussetzung für Phase 3 (Advanced RAG).

## Hintergrund

Die Inventarisierung hat gezeigt, dass die grösste Qualitäts-Barriere die Sprachbarriere DE↔EN ist. `all-mpnet-base-v2` (2021) ist English-only und versteht deutsche Queries nur über Token-Overlap (via BM25). Der godot-007-Fix (Stair Stepping) war ein Workaround — die eigentliche Lösung ist ein multilinguales Embedding-Modell. BGE-M3 (2024) ist der aktuelle State-of-the-Art für multilinguale Dense-Retrieval-Modelle und bietet zusätzlich Sparse-Retrieval (für Phase 3) und Long-Context-Support (8192 Token, für Late Chunking).

## Maßnahmen

### 2.1 BGE-M3 als Embedding-Modell

**Problem:** `all-mpnet-base-v2` (2021, English-only, 768d, 384 Token Kontext) definiert in `mcp_servers/knowledge_hub/config.py:16`. Sprachbarriere DE↔EN. Deutsche Queries ("Wie speichere ich Spielstände?") matchen englische Chunks ("save game data") nur über BM25-Token-Overlap, nicht über semantische Ähnlichkeit. godot-007-Fix war Workaround, nicht Lösung.

**Lösung:** Wechsel zu `BAAI/bge-m3` (568M params, ~2.2 GB, multilingual 100+ Sprachen, 1024d, 8192 Token Kontext, MIT-Lizenz). Integriertes Sparse-Retrieval (kann BM25 ersetzen — aber das ist Phase 3, hier nur Dense-Embedding). Matryoshka-Training: unterstützt dimensionality reduction (1024→768→512) mit Qualitätsverlust — könnte genutzt werden um ChromaDB-Grösse zu kontrollieren.

**Aufwand:** 1–2 Tage. **Impact:** sehr hoch.

**Quelle:** https://huggingface.co/BAAI/bge-m3 — Chen et al., arXiv 2402.03216

**Betroffene Dateien:**
- `mcp_servers/knowledge_hub/config.py` (Zeile 16: `DEFAULT_MODEL_NAME`, neue Konstante für dims)
- `scripts/model_manager.py` (`get_embedder()`, `_EMBEDDING_MODEL_RE` in Zeile 68)
- `scripts/embed_index.py` (Collection-Dimension 768→1024)
- `scripts/embed_search.py` (Query-Embedding)
- `requirements.txt` (ggf. `FlagEmbedding` Package für BGE-M3)
- `THIRD_PARTY_LICENSES.md` (MIT-Lizenz dokumentieren)

**Index-Rebuild:** Vollständiger Rebuild ALLER Domains (godot + davinci_resolve + dummy). ChromaDB-Collections müssen neu erstellt werden (andere Dimension: 1024d statt 768d). Keine Migration möglich — kompletter Neuaufbau.

**Re-Evaluation:** Zwingend. Alle 14 Golden-Dataset-Fragen (7 godot + 7 davinci_resolve) müssen mit BGE-M3 evaluiert werden.

**Constraints:**
- ~2.2 GB Download bei erstem Use
- 1024d statt 768d → ChromaDB-Collections neu (keine Migration, kompletter Rebuild)
- BGE-M3 benötigt ggf. `FlagEmbedding` Package (`pip install FlagEmbedding`)
- MIT-Lizenz (keine Einschränkungen, besser als CC-BY-NC-4.0 des Rerankers)

**Risiken:**
- Index-Grösse wächst (1024d vs 768d ~33% mehr Speicher pro Vector)
- Rebuild-Zeit länger (grösseres Modell, mehr Dimensionen)
- Re-Evaluation ALLER 14 Fragen zwingend
- Backup ALLER Indizes vor Rebuild
- Falls BGE-M3 schlechter performt als all-mpnet (unwahrscheinlich aber möglich), Rollback nötig

**Offene Fragen für Noah:**
- Soll BGE-M3 mit vollen 1024d oder mit Matryoshka auf 768d/512d verwendet werden?
- Soll das Sparse-Retrieval-Feature von BGE-M3 direkt aktiviert werden (Phase 3) oder erst später?
- Wie wird der Modellaustausch in `model_manager.py` atomic (rollback-safe)?
- Benchmark BGE-M3 vs. all-mpnet vor dem Wechsel?

---

### 2.2 Late Chunking für PDF-Domains (DaVinci)

**Problem:** DaVinci-PDFs werden mit `fallback_chunk()` (2000 Tokens, 200 Overlap) vorge-chunkt. Querverweise innerhalb eines Kapitels gehen verloren. Ein Satz wie "Wie in Kapitel 3 beschrieben..." hat keinen Zugriff auf Kapitel 3, wenn es in einem anderen Chunk liegt.

**Lösung:** Late Chunking (Jina AI 2024): Gesamtes Dokument durch den Transformer schicken, dann Token-Embeddings zu Chunk-Embeddings poolen. Behält Dokument-Kontext. Setzt Long-Context Embedding Model voraus (BGE-M3 mit 8192 Token). Abhängigkeit von 2.1.

**Aufwand:** 2–3 Tage. **Impact:** mittel-hoch.

**Quelle:** https://jina.ai/news/late-chunking-in-long-context-embedding-models/

**Betroffene Dateien:**
- `scripts/embed_index.py` (neue Chunking-Strategie für PDFs)
- `scripts/parser_base.py` (neue Funktion `late_chunk()`)

**Index-Rebuild:** Nur DaVinci betroffen (Godot hat strukturierten Parser, personal notes haben `markdown_section_chunk()`).

**Re-Evaluation:** DaVinci-Fragen (7 Stück).

**Risiken:**
- Implementierung komplex (Token-Level-Pooling)
- BGE-M3 muss Long-Context effizient verarbeiten (8192 Token können langsam sein)
- DaVinci-PDFs sind 50–200 Seiten — evtl. müssen sie kapitelweise verarbeitet werden (8192 Token ≈ 6–8 Seiten)
- Re-Evaluation DaVinci-Fragen

**Offene Fragen für Noah:**
- Kapitelweises Late Chunking (an PDF-Page-Markern) statt dokumentenweites?
- Wie wird Chunk-Granularität nach dem Pooling kontrolliert?
- Soll Late Chunking auch für Godot-Repo-Sources angewendet werden?

---

### 2.3 CI Quality Regression Gate

**Problem:** Quality Platform hat 28 Testdateien und `run_evaluation.py`, aber nichts läuft in CI. Composite-Scores werden nie automatisch geprüft. Nach einem Index-Rebuild gibt es keine automatisierte Regression-Detection.

**Lösung:** Scheduled GitHub Action (weekly, z.B. jeden Montag): baut Index, führt `run_evaluation.py --domain godot` und `--domain davinci_resolve` aus, vergleicht Composite-Score mit gespeicherter Baseline (z.B. `quality/baselines/godot-latest.json`), blockt bei Regression (avg_composite < baseline − 0.1 oder eine Frage von pass → weak/fail). Erzeugt Report als Artifact.

**Aufwand:** 1 Tag. **Impact:** hoch.

**Betroffene Dateien:**
- `.github/workflows/quality-gate.yml` (neu)
- `quality/baselines/` (neues Verzeichnis)
- `scripts/quality/run_evaluation.py` (Baseline-Vergleich-Funktion ggf. verbessern)

**Constraints:**
- Index-Rebuild in CI dauert ~10–20 Min pro Domain → scheduled (nicht push)
- GitHub-Action-Runner hat begrenzten Speicher (ChromaDB + Modelle ~3–4 GB — ggf. large runner nötig)
- Models müssen gecacht werden (`actions/cache`)

**Risiken:**
- CI-Umgebung unterscheidet sich von lokal (andere Python-Version, andere ChromaDB-Version) → Scores können abweichen
- Baseline muss regelmässig aktualisiert werden (wer macht das?)

**Offene Fragen für Noah:**
- Soll der Quality Gate auch DaVinci prüfen (DaVinci-PDFs sind via LFS — CI muss LFS pullen)?
- Wie wird die Baseline aktualisiert (manuell nach jeder erfolgreichen Iteration, oder automatisch wenn Score besser als Baseline)?
- Soll es ein separates Issue geben wenn der Gate blockt?

---

### 2.4 Golden Dataset erweitern (20–30 pro Domain)

**Problem:** 7 Fragen pro Domain ist minimal. Regression-Detection ist schwach (eine Frage kann den Avg zu stark beeinflussen — siehe godot-005 Regression in der Gap-Closing-Spec, wo eine Frage von pass auf weak fiel und den Avg von 0.86 auf 0.78 senkte).

**Lösung:** Pro Domain auf 20–30 Fragen ausbauen. Verschiedene Schwierigkeitsgrade (easy/medium/hard), verschiedene Themen (API, Workflow, Gotchas, Best Practices, Troubleshooting). `add_question.py` CLI existiert bereits.

**Aufwand:** Kuratierung durch Noah, mehrere Stunden. **Impact:** mittel.

**Betroffene Dateien:**
- `quality/golden/godot.yaml`
- `quality/golden/davinci_resolve.yaml`

**Constraints:**
- Fragen müssen realistisch sein (keine erfundenen Use-Cases)
- `expected_source_files` müssen existieren
- `real_world_sources` sollten kuratiert werden (URLs, `has_solution`, `solution_summary`)
- LIM-005 resolved — `solution_summary`-Felder müssen ausgefüllt sein

**Offene Fragen für Noah:**
- Soll es ein Template/CLI für Bulk-Import geben?
- Soll die Difficulty-Verteilung festgelegt sein (z.B. 30% easy, 50% medium, 20% hard)?
- Welche Themen fehlen aktuell in beiden Domains?

---

## Abhängigkeiten zwischen Maßnahmen

```
2.1 BGE-M3 (keine Abhängigkeiten)
  └── 2.2 Late Chunking (setzt BGE-M3 voraus — braucht Long-Context-Embedding)
2.3 CI Quality Gate (unabhängig, aber sinnvoll nach 2.1/2.2 für Regression-Detection)
2.4 Golden Dataset erweitern (unabhängig, aber sinnvoll vor 2.3 für bessere Baseline)
```

Empfohlene Reihenfolge:
1. 2.4 Golden Dataset erweitern (Kuratierung zuerst, damit Baseline breiter ist)
2. 2.1 BGE-M3 (Kern-Änderung)
3. 2.2 Late Chunking (nach BGE-M3)
4. 2.3 CI Quality Gate (nachdem neue Baseline etabliert ist)

## Phase-Exit-Kriterien

- [ ] BGE-M3 ist als Embedding-Modell aktiv (alle Domains)
- [ ] Late Chunking für DaVinci-PDFs implementiert
- [ ] CI Quality Gate läuft weekly und blockt bei Regressionen
- [ ] Golden Dataset: ≥20 Fragen pro Domain
- [ ] Re-Evaluation bestätigt keine signifikanten Regressionen (avg_composite ≥ baseline − 0.05)
- [ ] Backup-Strategie für Index-Rollback dokumentiert
- [ ] `THIRD_PARTY_LICENSES.md` aktualisiert (BGE-M3 MIT)
- [ ] `docs/ai/changelog.md` aktualisiert

## Entscheidungen (Noah, 2026-06-30)

### Entscheidung 2.1: BGE-M3 Dimensionalität
**Frage:** Soll BGE-M3 mit vollen 1024d oder mit Matryoshka auf 768d/512d verwendet werden?
**Entscheidung:** Volle 1024 Dimensionen. Keine Matryoshka-Reduktion.
**Begründung:** ~25k Chunks → ChromaDB 700 MB ist unkritisch lokal, selbst bei 100k Chunks wären 2-3 GB ok. Volle 1024d = volle Qualität; Matryoshka verliert 2-5% Retrieval-Qualität. Architektur-Entscheidung: einmal auf 1024d festgelegt, ChromaDB so dimensioniert. Später reduzieren würde weiteren Rebuild erfordern. Lieber einmal richtig bauen.

### Entscheidung 2.2: BGE-M3 Sparse-Retrieval Aktivierung
**Frage:** Soll das Sparse-Retrieval-Feature von BGE-M3 direkt aktiviert werden (Phase 3) oder erst später? Wie wird der Modellaustausch in model_manager.py atomic (rollback-safe)?
**Entscheidung:** Sparse-Retrieval erst in Phase 3 (wie ursprünglich geplant), nicht vorzeitig. Modellaustausch atomic via `KH_EMBEDDING_MODEL`-Env-Var mit all-mpnet-base-v2 als Fallback. Vor dem Rebuild Backup ALLER Indizes; bei Re-Evaluations-Regression Rollback auf Backup.
**Begründung:** Sparse-Retrieval erfordert ChromaDB nativen Sparse-Vector-Support (stabil ab ~1.6), der in Phase 2 noch nicht garantiert ist. Phasen-Trennung hält Phase 2 fokussiert auf Dense-Embedding-Wechsel. Atomic-Rollback via Env-Var + Backup entspricht dem etablierten Muster aus Entscheidung 1.2.

### Entscheidung 2.3: Quality Gate Scope (DaVinci in CI)
**Frage:** Soll der Quality Gate auch DaVinci prüfen (DaVinci-PDFs sind via LFS — CI muss LFS pullen)?
**Entscheidung:** Ja, Quality Gate prüft BEIDE Domains (godot + davinci_resolve). LFS-Cache via actions/cache für die packed-files/PDFs.
**Begründung:** DaVinci ohne Quality Gate = blinde Hälfte des Hubs; Regressionen würden erst in realer Nutzung auffallen. LFS in CI ist gelöst (actions/cache mit ~/.git-lfs als Cache-Key; erster Run ~50 MB Download, danach cache-hit, keine Runtime-Strafe). Symmetrie: godot und davinci identisch behandelt; bei zukünftigen Domains (Blender/FreeCAD) wird der Workflow erweitert, kein DaVinci-Sonderkonstrukt.

### Entscheidung 2.4: Baseline-Update-Strategie für Quality Gate
**Frage:** Wie wird die Baseline aktualisiert (manuell nach jeder erfolgreichen Iteration, oder automatisch wenn Score besser als Baseline)?
**Entscheidung:** Manuell nach jeder erfolgreichen Iteration. Baseline-Datei (`quality/baselines/<domain>-latest.json`) wird von Noah committed, wenn eine Iteration die Scores verbessert oder stabilisiert hat. CI vergleicht nur gegen diese committed Baseline und blockt bei Regression (avg_composite < baseline − 0.1 ODER eine Frage von pass → weak/fail). Kein automatisches Baseline-Update (verhindert Score-Creep durch zufällige Verbesserungen).
**Begründung:** Automatisches Baseline-Update würde schleichende Verschlechterungen verdecken (einmal weak → neue Baseline → nächstes weak → neue Baseline). Manuelle Updates zwingen Noah, Score-Veränderungen bewusst zu reviewen. Schwellen 0.1 für avg_composite und pass→weak/fail für einzelne Fragen sind streng genug für Regression-Detection, locker genug für nicht-deterministische Reranker-Schwankungen.

### Entscheidung 2.5: Golden Dataset Erweiterung
**Frage:** Soll es ein Template/CLI für Bulk-Import geben? Soll die Difficulty-Verteilung festgelegt sein (z.B. 30% easy, 50% medium, 20% hard)?
**Entscheidung:** Kein Bulk-Import-CLI (add_question.py reicht). Difficulty-Verteilung: ~30% easy, 50% medium, 20% hard (orientiert an realer Nutzung). Pro Domain auf 20-30 Fragen ausbauen.
**Begründung:** Bulk-Import-CLI wäre Overengineering für ~25 manuell kuratierte Fragen pro Domain. Difficulty-Verteilung 30/50/20 spiegelt reale Query-Verteilung (mehr medium als hard). 20-30 Fragen geben statistische Power für Regression-Detection (bei n=14 ist eine Frage 7% — bei n=25 nur 4%).

## Offene Fragen für Noah (zusammengefasst)

> Siehe Entscheidungen (Noah, 2026-06-30) oben für die Antworten.

1. BGE-M3: Volle 1024d oder Matryoshka? Sparse-Retrieval jetzt oder Phase 3? Atomic-Rollback-Strategie? Benchmark vor Wechsel?
2. Late Chunking: Kapitelweise oder dokumentenweit? Chunk-Granularität? Auch für Godot?
3. Quality Gate: DaVinci in CI (LFS)? Baseline-Update-Strategie? Issue bei Block?
4. Golden Dataset: Bulk-Import-Template? Difficulty-Verteilung? Fehlende Themen?

## Referenzen

- Bestehendes Embedding-Modell: `mcp_servers/knowledge_hub/config.py:16`
- Bestehender Model Manager: `scripts/model_manager.py`
- BGE-M3: https://huggingface.co/BAAI/bge-m3
- Late Chunking: https://jina.ai/news/late-chunking-in-long-context-embedding-models/
- Quality-Platform-Spec: `docs/superpowers/specs/2026-06-29-knowledge-hub-quality-evaluation-platform-design.md`
- Test-Suite-Spec: `docs/superpowers/specs/2026-06-28-knowledge-hub-test-suite-design.md`
- Phase-1-Spec: `docs/superpowers/specs/2026-06-30-improvement-roadmap-phase1-low-hanging-fruit-design.md`
