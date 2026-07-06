# Improvement Roadmap Phase 1 — Low-Hanging Fruit — Design Spec

> **Status:** Draft | **Datum:** 2026-06-30 | **Autor:** Orchestrator
>
> Abgeleitet aus: Interne Inventarisierung + externe Recherche (Stand 2026-06-30), 20 identifizierte Verbesserungspotentiale, Roadmap-Phasenplanung.
> Referenziert: `docs/superpowers/specs/2026-06-29-knowledge-hub-quality-evaluation-platform-design.md`, `docs/superpowers/specs/2026-06-30-gap-closing-godot-gotchas-design.md`

## Zusammenfassung

Phase 1 adressiert 5 Maßnahmen mit hohem Impact bei geringem Aufwand (1–4h pro Maßnahme). Keine Architektur-Änderungen, keine neuen Abhängigkeiten, keine langen Rebuilds. Ziel: Schnelle Qualitätsgewinne, die unabhängig von den grösseren Phasen 2+3 umgesetzt werden können.

## Hintergrund

Die Inventarisierung vom 2026-06-30 hat 20 Verbesserungspotentiale identifiziert. Fünf davon sind "Low-Hanging Fruit": Sie erfordern keine neuen Modelle, keine Architektur-Änderungen und keinen mehrstündigen Index-Rebuild. Sie können einzeln und in beliebiger Reihenfolge implementiert werden.

## Maßnahmen

### 1.1 CI Test Workflow

**Problem:** Kein GitHub-Action-Workflow für push/pull_request. 28 Testdateien (unit, integration, mcp, quality) laufen nur lokal. PRs können mit broken Tests mergen. `pytest` ist in der aktuellen Python-Umgebung nicht installiert — Tests existieren, aber es gibt keine automatisierte Ausführung.

**Lösung:** `.github/workflows/test.yml` mit `on: [push, pull_request]`, führt die schnellen Test-Layer aus:
- `pytest -m unit` (pure functions, keine Modelle/DB)
- `pytest -m integration` (temporäre ChromaDB + Dummy-Daten)
- `pytest -m mcp` (MCP-Contract-Tests)

Quality-Tests (`pytest -m quality`) und E2E-Tests (`pytest -m e2e`) erfordern einen vorgebauten Index und werden separat gehandhabt (siehe Phase 2 Quality Gate).

**Aufwand:** 2–3h. **Impact:** kritisch (keine CI = keine Regression-Detection).

**Betroffene Dateien:**
- `.github/workflows/test.yml` (neu)

**Constraints:**
- Kein Index-Rebuild in CI (zu langsam für push-Trigger)
- Python 3.11+, dependencies via `requirements.txt`
- Keine Secrets
- Keine Model-Downloads in Unit/Integration/MCP-Layern (nur Dummy-Daten)

**Risiken:** Niedrig. Reines Infrastruktur-Add-on, keine Code-Änderungen.

**Offene Fragen für Noah:**
- Soll eine Python-Versions-Matrix (3.11, 3.12, 3.13) laufen?
- Soll macOS getestet werden (Entwicklung ist macOS, GitHub macOS-Runner sind teurer)?
- Soll der Workflow auch `pytest -m quality` mit gecachtem Index ausführen (weekly scheduled)?

---

### 1.2 Reranker-Upgrade: jina-reranker-v2-base-multilingual

**Problem:** Aktueller Reranker `cross-encoder/ms-marco-MiniLM-L-12-v2` (2021, English-only, 512 Token Kontext) definiert in `mcp_servers/knowledge_hub/config.py:13`. Sprachbarriere DE↔EN, speziell für Cross-Encoder. Deutsche Queries gegen englische Chunks werden schlechter gerankt als englische Queries.

**Lösung:** Wechsel zu `jinaai/jina-reranker-v2-base-multilingual` (278M params, ~1.1 GB, multilingual, 1024 Token Kontext, Flash Attention, CodeSearchNet MRR@10: 71.36 vs. 62.86 für bge-reranker-v2-m3 — besser für Code/Technik-Doku).

**Aufwand:** 2–4h. **Impact:** hoch.

**Quelle:** https://huggingface.co/jinaai/jina-reranker-v2-base-multilingual

**Betroffene Dateien:**
- `mcp_servers/knowledge_hub/config.py` (Zeile 13: `CROSS_ENCODER_MODEL`)
- `scripts/model_manager.py` (`get_reranker()` in Zeile 140–144)
- `scripts/reranker.py` (falls Score-Normalisierung anders)
- `THIRD_PARTY_LICENSES.md` (neue Lizenz dokumentieren)

**Index-Rebuild:** NICHT nötig (Reranker ist Query-Time, nicht Index-Time).

**Re-Evaluation:** Zwingend. Alle 14 Golden-Dataset-Fragen (7 godot + 7 davinci_resolve) müssen mit dem neuen Reranker evaluiert werden, um Regressionen zu erkennen.

**Constraints:**
- CC-BY-NC-4.0 Lizenz (für persönlichen Hub akzeptabel, dokumentieren in `THIRD_PARTY_LICENSES.md`)
- ~1.1 GB Download bei erstem Use
- Flash Attention erfordert ggf. Hardware-Support (Apple Silicon OK)

**Risiken:**
- Score-Skala unterscheidet sich von ms-marco (Logit-Differenz vs. anderes Format) — prüfen ob Score-Kompatibilität mit bestehenden Tests/Heuristiken nötig
- Re-Evaluation aller 14 godot+davinci Fragen, um Regressionen zu erkennen
- CC-BY-NC-4.0 schränkt kommerzielle Nutzung ein (für Noahs persönlichen Hub irrelevant, aber dokumentieren)

**Offene Fragen für Noah:**
- Soll der Reranker per-domain konfigurierbar sein (in `domain.md`) oder global in `config.py`?
- Soll ein Benchmark jina vs. ms-marco vs. bge-reranker-v2-m3 vor dem Wechsel laufen?
- Soll der alte Reranker als Fallback erhalten bleiben (z.B. via CLI-Flag `--reranker legacy`)?

---

### 1.3 BM25 CamelCase-Splitting

**Problem:** BM25-Tokenizer in `scripts/bm25_search.py:29` (`re.findall(r"\w+", text.lower())`) splittet nicht an CamelCase. `CharacterBody3D` → `characterbody3d` (1 Token) statt `["character", "body", "3d"]` (3 Tokens). Query-Keyword `character` matcht nicht. Das war eine Wurzelursache von godot-007 (Stair Stepping — `CharacterBody3D` war nicht als `character` tokenisiert).

**Lösung:** CamelCase-Splitting im Tokenizer. Beispiel-Regex: `re.findall(r"[a-z]+|[A-Z][a-z]*|\d+", text)` oder ähnlich. Zusätzlich: Lowercase nach Split. Optional: Stopwort-Entfernung, Porter-Stemmer (als separate Maßnahmen bewerten).

**Aufwand:** 1–2h. **Impact:** mittel (generischer Fix für eine ganze Klasse von Cross-Lingual/Keyword-Mismatch-Problemen).

**Betroffene Dateien:**
- `scripts/bm25_search.py` (`tokenize()`-Funktion in Zeile 27–29)

**Index-Rebuild:** Nötig (BM25-Index wird neu gebaut). ChromaDB-Index unverändert.

**Re-Evaluation:** Nötig. BM25-Token-Änderungen können Ranking verschieben.

**Risiken:**
- CamelCase-Splitting kann bei nicht-CamelCase-Tokens zu Over-Splitting führen (z.B. "GPU" → "G", "P", "U"? Nein — Regex muss Grossbuchstaben-Sequenzen erhalten)
- API-Methoden wie `move_and_slide` (snake_case) werden bereits korrekt gesplittet
- Test: `tests/unit/test_bm25_tokenizer.py` muss erweitert werden

**Offene Fragen für Noah:**
- Soll Stemming (Porter) zusätzlich aktiviert werden?
- Soll eine Stopwort-Liste verwendet werden (welche: Englisch, Deutsch, beide)?
- Soll CamelCase-Splitting per-domain konfigurierbar sein?

---

### 1.4 Chunk-Overlap erhöhen (200 → 400 Tokens)

**Problem:** `FALLBACK_CHUNK_OVERLAP = 200` in `scripts/parser_base.py:127` entspricht 200 Tokens Overlap (800 chars bei 4 chars/token). Overlap von 200 Tokens kann "lost context" an Chunk-Grenzen verursachen — ein Satz, der über die Chunk-Grenze läuft, wird in keinem Chunk vollständig erfasst.

**Lösung:** `FALLBACK_CHUNK_OVERLAP = 400` (entspricht 400 Tokens, 1600 chars). Trivial in `parser_base.py:127`.

**Aufwand:** 1h. **Impact:** mittel.

**Betroffene Dateien:**
- `scripts/parser_base.py` (Zeile 127: `FALLBACK_CHUNK_OVERLAP`)

**Index-Rebuild:** Nötig (Chunk-Grenzen ändern sich → neue Chunks → neuer Index).

**Re-Evaluation:** Nötig.

**Risiken:**
- Grösserer Overlap = mehr Chunks = grösserer Index
- Bei aktuell ~24.500 Chunks mit 200-Token-Overlap → mit 400-Token-Overlap könnten es ~25.000–30.000 Chunks werden
- Speicherbedarf steigt (ChromaDB + BM25)
- Quality-Tests prüfen

**Offene Fragen für Noah:**
- Soll Overlap per-domain konfigurierbar sein (in `domain.md`)?
- Soll `markdown_section_chunk()` auch Overlap bekommen (aktuell kein Overlap zwischen Sektionen — bewusst, da Sektionen semantisch unabhängig sind)?

---

### 1.5 Godot faq.md füllen

**Problem:** `domains/godot/personal/faq.md` hat 3 `##`-Sektionen, alle mit Inhalt "TODO" (<50 Zeichen). Defensive Skip bei `markdown_section_chunk()` filtert sie → 0 Chunks. Häufige Anfängerfragen (Lifecycle, Data Saving, 3D Visibility) sind nicht beantwortet.

**Lösung:** Noah kuratiert echte FAQ-Einträge. Diese Spec definiert nur die Anforderungen (welche Themen, Format), nicht den Inhalt selbst (das ist Noahs Aufgabe).

**Aufwand:** 1–2h (Spec) + Noahs Kuratierung. **Impact:** mittel.

**Themen (laut TODO-Platzhaltern):**
1. **Node Lifecycle** (`_ready`, `_enter_tree`, `_exit_tree`, `_process`, `_physics_process`) — Wann wird was aufgerufen?
2. **Data Saving** (`save_game`, JSON, `ConfigFile`, `ResourceSaver`) — Wie speichert man Spielstände?
3. **3D Visibility** (`visible`, `process_mode`, `cull_mask`, `layers`) — Warum sehe ich mein 3D-Modell nicht?

**Format:** `##`-Header pro Frage, Antwort in 2–5 Sätzen, ggf. Code-Snippet. Deutsch Prosa + englische Code-Kommentare (wie `gotchas.md`/`tips.md`).

**Betroffene Dateien:**
- `domains/godot/personal/faq.md`

**Index-Rebuild:** Nötig. **Re-Evaluation:** Nötig (falls eine godot-Frage `faq.md` erwartet — aktuell keine, aber neue Golden-Dataset-Fragen könnten hinzukommen).

**Constraints:**
- Keine erfundenen Godot-APIs
- Nur dokumentierte Godot-4-Stable-APIs
- Konsistentes Format mit bestehenden personal notes

**Offene Fragen für Noah:**
- Soll `faq.md` auch deutsche Übersetzungen der Fragen enthalten (für BM25-Cross-Lingual)?
- Soll eine neue Golden-Dataset-Frage hinzugefügt werden, die `faq.md` erwartet?
- Welche weiteren FAQ-Themen sind relevant (Signals, Input Handling, Scene Management)?

---

## Abhängigkeiten zwischen Maßnahmen

Keine. Alle 5 Maßnahmen sind unabhängig voneinander implementierbar. Empfohlene Reihenfolge (nach Impact):
1. 1.1 CI Test Workflow (Infrastruktur zuerst)
2. 1.2 Reranker-Upgrade (höchster Quality-Impact)
3. 1.3 BM25 CamelCase-Splitting
4. 1.4 Chunk-Overlap erhöhen
5. 1.5 Godot faq.md füllen (erfordert Noahs Kuratierung)

## Phase-Exit-Kriterien

- [ ] Alle 5 Maßnahmen implementiert
- [ ] CI Workflow läuft erfolgreich auf push/pull_request
- [ ] Re-Evaluation nach 1.2, 1.3, 1.4 bestätigt keine signifikanten Regressionen (avg_composite ≥ baseline − 0.05)
- [ ] `faq.md` enthält mindestens 3 substanzielle Einträge (>50 Zeichen pro Sektion)
- [ ] `THIRD_PARTY_LICENSES.md` aktualisiert (jina-reranker CC-BY-NC-4.0)
- [ ] `docs/ai/changelog.md` aktualisiert

## Entscheidungen (Noah, 2026-06-30)

### Entscheidung 1.1: CI Python-Version und Runner
**Frage:** Soll eine Python-Versions-Matrix (3.11, 3.12, 3.13) laufen? Soll macOS getestet werden?
**Entscheidung:** Python 3.11 only auf ubuntu-latest. Keine Versions-Matrix, kein macOS-Runner.
**Begründung:** 3.11 ist die requirements.txt-Vorgabe. Multi-Version-Matrix bringt false positives bei Versionsdrift (ChromaDB-Verhalten) und 50% mehr CI-Laufzeit für eine Solo-Entwicklung. macOS-Runner sind 10x teurer und lokal läuft macOS bereits. Wartungsarm: ein Job, eine Version, ein Setup. Falls später multiple contributors: Matrix auf 3.11+3.12 erweitern.

### Entscheidung 1.2: Reranker-Wechsel-Strategie
**Frage:** Soll ein Benchmark jina vs. ms-marco vor dem Wechsel laufen? Soll der Reranker per-domain oder global konfigurierbar sein?
**Entscheidung:** Direkter Wechsel zu jina-reranker-v2-base-multilingual OHNE Vorab-Benchmark. Reranker global konfigurierbar via Umgebungsvariable `KH_RERANKER_MODEL` mit ms-marco als dokumentierten Fallback. Kein per-domain-Reranker.
**Begründung:** Ein Vorab-Benchmark über 14 Golden-Dataset-Fragen ist statistisch nicht aussagekräftig (n=14). Stattdessen nach dem Wechsel Re-Evaluation aller 14 Fragen; bei Regression Rollback via Env-Var in 30 Sekunden (Reranker ist Query-Time, kein Rebuild nötig). Konfigurierbarkeit via Env-Var ist der nachhaltige Hebel: danach kann ANY Reranker getestet werden ohne Code-Änderung (z.B. bge-reranker-v2-m3 in Phase 3).

### Entscheidung 1.3: BM25-Tokenisierung
**Frage:** Soll Stemming (Porter) zusätzlich aktiviert werden? Soll eine Stopwort-Liste verwendet werden (welche: Englisch, Deutsch, beide)? Soll CamelCase-Splitting per-domain konfigurierbar sein?
**Entscheidung:** Nur CamelCase-Splitting implementieren. Kein Porter-Stemmer, keine Stopwort-Liste. Global für alle Domains, nicht per-domain.
**Begründung:** CamelCase-Splitting ist universell für Code/API-Dokumentation (Godot, DaVinci, Blender, FreeCAD nutzen alle CamelCase) — einmal gebaut, trägt es für jede zukünftige Domain. Porter-Stemmer ist sprachspezifisch (EN vs. DE) und würde Sprach-Erkennung pro Chunk erfordern — Komplexität ohne Gewinn bei CamelCase-API-Namen. Stopwörter: BM25-Okapi hat IDF-basierte Stopwort-Abschwächung bereits eingebaut. Minimalismus ist nachhaltiger als ein Stemming-Framework, das in 2 Jahren debugged werden muss.

### Entscheidung 1.4: Chunk-Overlap
**Frage:** Soll Overlap per-domain konfigurierbar sein (in domain.md)? Soll markdown_section_chunk auch Overlap bekommen (aktuell kein Overlap zwischen Sektionen — bewusst)?
**Entscheidung:** Erhöhung global auf 400 Tokens (FALLBACK_OVERLAP_CHARS 800 → 1600), nicht per-domain. markdown_section_chunk bleibt ohne Overlap (bewusst — Sektionen sind semantisch unabhängig).
**Begründung:** Per-domain-Konfiguration pro Parameter führt zu Konfigurations-Explosion. Globale Werte sind wartungsärmer und konsistent über alle Domains. markdown_section_chunk ohne Overlap ist bewusst: Sektionen sind semantisch unabhängige Einheiten (z.B. ein Gotcha pro Sektion), Overlap würde Code-Snippets überschneiden lassen.

### Entscheidung 1.5: Godot faq.md
**Frage:** Soll faq.md deutsche Übersetzungen der Fragen enthalten (für BM25-Cross-Lingual)? Soll eine neue Golden-Dataset-Frage hinzugefügt werden, die faq.md erwartet? Weitere Themen über die 3 TODOs hinaus?
**Entscheidung:** faq.md in deutscher Prosa mit englischen Code-Snippets (wie gotchas.md/tips.md), KEINE separaten deutschen Frage-Übersetzungen. EINE neue Golden-Dataset-Frage (godot-008) hinzufügen, die faq.md als expected_source_file erwartet. Nur die 3 bestehenden TODO-Themen (Lifecycle, Data Saving, 3D Visibility) füllen — keine zusätzlichen Themen.
**Begründung:** Code-Snippets liefern englische BM25-Tokens (velocity, save, visible) — das reicht für Cross-Lingual-Matching, ohne manuelle Übersetzungen pflegen zu müssen. Eine neue Golden-Dataset-Frage (godot-008) sichert, dass faq.md nach dem Füllen in der Evaluation geprüft wird. Drei Themen sind fokussiert und decken häufige Anfängerfragen ab; weitere Themen folgen organisch.

## Offene Fragen für Noah (zusammengefasst)

> Siehe Entscheidungen (Noah, 2026-06-30) oben für die Antworten.

1. CI: Python-Versions-Matrix? macOS-Runner?
2. Reranker: Per-domain oder global? Benchmark vor Wechsel? Fallback erhalten?
3. BM25: Stemming? Stopwörter? Per-domain?
4. Overlap: Per-domain? Auch für markdown_section_chunk?
5. FAQ: Deutsche Übersetzungen? Neue Golden-Dataset-Fragen? Weitere Themen?

## Referenzen

- Bestehender Reranker: `mcp_servers/knowledge_hub/config.py:13`
- Bestehender Tokenizer: `scripts/bm25_search.py:27-29`
- Bestehender Overlap: `scripts/parser_base.py:127`
- Bestehendes FAQ: `domains/godot/personal/faq.md`
- Jina Reranker: https://huggingface.co/jinaai/jina-reranker-v2-base-multilingual
- Test-Suite-Spec: `docs/superpowers/specs/2026-06-28-knowledge-hub-test-suite-design.md`
- Quality-Platform-Spec: `docs/superpowers/specs/2026-06-29-knowledge-hub-quality-evaluation-platform-design.md`
- godot-007-Fix: `docs/superpowers/specs/2026-06-30-gap-closing-godot-gotchas-design.md`
