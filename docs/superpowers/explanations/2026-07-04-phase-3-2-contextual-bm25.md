# Phase 3.2 Contextual BM25 — Wo die Dateien leben

> **Anfängerfreundliche Erklärung** | 2026-07-04 | BM25-Stichwortsuche bekommt LLM-Kontext — Ergebnis: GO

## 1. Was ist Contextual BM25?

### Kurzer Rückblick: Phase 3.1 (Contextual Retrieval)

In Phase 3.1 haben wir gelernt, dass ein LLM (großes Sprachmodell) für jeden
Wissens-Chunk einen kurzen Kontext-Präfix schreiben kann. Beispiel:

```
Kontext: "A rotation method within a Godot Node3D tutorial covering 3D
transforms and character controllers."

Chunk: "void rotate_y(angle: float)"
```

Dieser Kontext wurde in Phase 3.1 **nur für die semantische Suche** (Embeddings)
genutzt. Die Stichwortsuche (BM25) blieb unverändert — sie durchsuchte weiterhin
nur den reinen Chunk-Text ohne Kontext. Das war die bewusste Entscheidung **D1**:
„BM25 = nur text".

### Was Phase 3.2 ändert

Phase 3.2 hebt D1 **optional** auf: Wenn `--contextualize-bm25` gesetzt ist,
bekommt auch die BM25-Stichwortsuche den Kontext-Präfix. Der BM25-Corpus wird
dann aus `context_prefix + " " + text` gebaut statt nur aus `text`.

### Warum das hilft

BM25 ist eine reine Keyword-Suche. Sie zählt, wie oft Suchbegriffe in einem
Dokument vorkommen. Wenn der Kontext-Präfix zusätzliche Keywords enthält, erhöht
das die Treffer-Wahrscheinlichkeit:

- **Sprachbarriere-Beispiel:** Eine englische Query („Why is my 3D model not
  visible") sucht nach Keywords wie `3d`, `model`, `visible`. Die deutsche
  `faq.md` enthält diese Keywords nicht — aber der LLM-generierte Kontext-Präfix
  (auf Englisch) tut es. Dadurch findet BM25 den deutschen Chunk, obwohl die
  Query und der Chunk-Text in verschiedenen Sprachen sind.

- **Allgemein:** Der Kontext fügt Keywords hinzu, die den Chunk im Gesamtdokument
  verorten (z. B. „Godot 3D tutorial", „Node3D rotation method"). Das verbessert
  die BM25-Recall für verwandte Queries.

### Was unverändert bleibt

- **Default ist aus** (`contextualize_bm25=False`). Ohne das Flag verhält sich
  BM25 wie vorher (D1 gültig, Backward-Compat).
- **Cross-Encoder** (Reranker) bewertet weiterhin nur den `text`.
- **MCP-Server** liefert den `text` sauber und `context_prefix` als separates
  Metadaten-Feld.
- **Embeddings** nutzen den Kontext weiterhin (wie in Phase 3.1).

---

## 2. Wo liegen die neuen/geänderten Dateien?

### Geänderte Skripte

| Pfad | Was hat sich geändert? |
|------|----------------------|
| `scripts/bm25_search.py` | `build_bm25_index()` hat einen neuen Parameter `use_context_prefix: bool = False`. Wenn `True`, wird der BM25-Corpus aus `context_prefix + " " + text` tokenisiert (Zeile 80–81). Chunks ohne `context_prefix` fallen auf `tokenize(text)` zurück. Die Field-Boosts (`name * 2`, `signature * 3`) bleiben in beiden Modi unverändert. |
| `scripts/embed_index.py` | Das `--contextualize-bm25` Flag ist jetzt **funktional** (vorher wurde es akzeptiert aber ignoriert). Es impliziert `--contextualize` (Zeile 460). `build_index()` ruft `build_bm25_index(domain, chunks, use_context_prefix=contextualize_bm25)` auf (Zeile 423). |

### Neue Eval-Domain

| Pfad | Beschreibung |
|------|-------------|
| `domains/godot_eval_c/` | Phase-3.2-Eval-Domain für Contextual BM25. Symlinks auf `../../godot/sources/*.md` und `../../godot/personal/*.md`. Eigener ChromaDB-Index unter `chromadb_data/godot_eval_c/`. Wird mit `contextualize=True, contextualize_bm25=True` gebaut. Nutzt **bewusst keinen RST-Parser** (BS-8), sondern `fallback_chunk`, um den Contextual-BM25-Effekt isoliert zu messen — ohne RST-Strukturierungs-Boosts als Konfounder. |

### A/B/C-Eval-Ergebnisse

| Pfad | Beschreibung |
|------|-------------|
| `results/3-2/godot-eval-a.json` | **A = Baseline** (keine Kontexte). 18 pass / 3 weak, avg_composite 0.8281. |
| `results/3-2/godot-eval-b.json` | **B = Embeddings-only** (Phase 3.1, nur Embeddings kontextualisiert). 19 pass / 2 weak, avg_composite 0.8386. |
| `results/3-2/godot-eval-c.json` | **C = Embeddings + Contextual BM25** (Phase 3.2). 20 pass / 1 weak, avg_composite 0.8490. |

### Neue/geänderte Tests

| Pfad | Was wurde getestet? |
|------|-------------------|
| `tests/integration/test_bm25_search.py` | 5 neue Tests für `use_context_prefix`: Default `False` → BM25-Corpus = nur `text`; `True` → Corpus enthält `context_prefix`-Tokens; Chunk ohne `context_prefix` → Fallback auf `text`; Backward-Compat ohne Kwarg; BS-4: `context_prefix`-Keywords erhöhen BM25-Score für Query. |
| `tests/integration/test_contextualize_build.py` | `test_contextualize_bm25_flag_enables_contextual_bm25` (ersetzt den alten No-Op-Test): prüft, dass `contextualize_bm25=True` den BM25-Corpus mit Kontext baut. `test_contextualize_bm25_false_keeps_clean_bm25`: prüft, dass `False` den BM25-Corpus sauber hält (D1). |
| `tests/integration/test_eval_domains.py` | `godot_eval_c` zur `EVAL_DOMAINS`-Liste hinzugefügt. Neuer Test `test_godot_eval_c_symlinks_resolve`: prüft, dass alle 3 Source- und 4 Personal-Symlinks existieren. Parametrisierte Collection-Name-Tests um `godot_eval_c` erweitert. |

### Aktualisierte Dokumentation

| Pfad | Was wurde ergänzt? |
|------|-------------------|
| `docs/ai/changelog.md` | Phase-3.2-Eintrag (Zeilen 135–148): A/B/C-Ergebnisse, GO-Entscheidung, godot-008/012 gehoben, Promote ausstehend (R4). |
| `docs/ai/decisions.md` | **E18** (D1-Aufhebung für Contextual BM25, opt-in) und **E19** (Cache-Reuse für godot_eval_c, 4580 Hits, 0 LLM-Calls). |
| `docs/ai/known-issues.md` | Phase-3.2-Ergebnis-Eintrag (Zeile 35): GO, 20 pass / 1 weak, R4-Parser-Konfounder. |
| `docs/ai/best-practices.md` | Contextual-BM25-Setup-Block (Zeilen 186–192): CLI-Befehl, Default-Verhalten, Cache-Reuse-Anleitung. |
| `docs/ai/architecture.md` | Contextual-BM25-Zeile im Datenfluss (Zeile 40): D1-Aufhebung E18, A/B/C-Eval, GO. |
| `docs/ai/domain-model.md` | Contextual-BM25-Absatz (E18) im Context-Prefix-Block. |
| `docs/ai/security.md` | Contextual-BM25-Sektion: keine neuen Security-Risiken, lokale Token-Variation. |

---

## 3. A/B/C-Vergleich (vereinfacht)

Wir haben drei Varianten des Godot-Index gebaut und mit denselben 21 Golden-Dataset-Fragen evaluiert:

| Variante | Embeddings | BM25 | Ergebnis |
|----------|-----------|------|----------|
| **A** (Baseline) | ohne Kontext | ohne Kontext | 18 pass / 3 weak, avg 0.8281 |
| **B** (Phase 3.1) | mit Kontext | ohne Kontext | 19 pass / 2 weak, avg 0.8386 |
| **C** (Phase 3.2) | mit Kontext | **mit Kontext** | 20 pass / 1 weak, avg 0.8490 |

**Delta C − A = +0.0209** — das liegt über der +0.02-Schwelle → **GO**.

### Was wurde besser?

- **godot-008** („Why is my 3D model not visible"): weak → pass. Die
  Sprachbarriere (englische Query, deutsche `faq.md`) wurde durch Contextual
  BM25 überwunden — der englische Kontext-Präfix im BM25-Corpus liefert die
  Keywords, die BM25 zum Matchen braucht.

- **godot-012** (NavigationAgent3D Enemy Chase): weak → pass (schon in B
  gehoben, C bestätigt).

### Was bleibt weak?

- **godot-009** (AnimationTree + BlendSpace2D, breite Animation): Die einzige
  verbleibende weak-Frage. Das Thema ist zu breit gestreut, als dass Contextual
  Retrieval allein es lösen könnte.

### Cache-Reuse

C hat den Cache von `godot_eval_b` wiederverwendet: 4580 Cache-Hits, **0
LLM-Calls**. Der domain-unabhängige Cache-Key (Entscheidung E17) funktioniert
— der Cache-Eintrag aus `godot_eval_b` ist identisch mit dem, den
`godot_eval_c` brauchen würde.

---

## 4. Validierungsbefehle

```bash
# Unit-Tests (216 passed)
.venv/bin/pytest -m unit -q

# Integration-Tests (106 passed)
.venv/bin/pytest -m integration -q

# Workspace-Struktur prüfen
./scripts/workspace_check.sh
```

---

## 5. Was ist das Ergebnis?

**GO** — Contextual BM25 wird für den produktiven Rollout freigegeben.

- **+0.0209 avg_composite** (C − A), über der +0.02-Schwelle
- **20 von 21 Fragen pass**, nur noch 1 weak (godot-009)
- **godot-008** (Sprachbarriere) und **godot-012** (NavigationAgent3D) gehoben
- **Keine Regressionen** bei den anderen 19 Fragen

### Promote ausstehend: R4-Parser-Konfounder

Der Eval (`godot_eval_c`) nutzt `fallback_chunk` (kein RST-Parser), aber der
produktive `godot`-Index nutzt den `rst-godot`-Parser. Der RST-Parser fügt
Struktur-Boosts hinzu (`name * 2`, `signature * 3`), die im Eval nicht
gemessen wurden.

Für den Promote muss ein separater Cloud-Lauf mit dem produktiven `godot`-Index
durchgeführt werden:

```bash
# 1. Cache von eval_b nach godot kopieren
cp chromadb_data/godot_eval_b/context_cache.db chromadb_data/godot/context_cache.db

# 2. Produktiven Index mit Contextual BM25 bauen
KH_LLM_MODEL=gemma4:cloud python scripts/embed_index.py \
  --domain godot --contextualize --contextualize-bm25

# 3. Gegen godot.yaml evaluieren
python scripts/quality/run_evaluation.py --domain godot
```

---

## 6. Nächste Schritte für Noah

1. **Promote durchführen:** Cache kopieren, produktiven `godot`-Index mit
   `--contextualize --contextualize-bm25` neu bauen (~3h Cloud), gegen
   `godot.yaml` evaluieren.
2. **godot-009 angehen:** Die letzte weak-Frage (AnimationTree + BlendSpace2D)
   braucht wahrscheinlich Content-Maßnahmen — breitere Animation-Themen in
   `tips.md` oder `best-practices.md`.
3. **DaVinci evaluieren:** Contextual BM25 auch für `davinci_resolve` testen
   (nur Pfad-A-Chunks, Late-Chunks sind ausgenommen). Cache müsste neu generiert
   werden (DaVinci hat keinen bestehenden Cache).
4. **Default-Entscheidung:** Überlegen, ob `contextualize_bm25=True` zum Default
   werden soll (aktuell opt-in). Dafür braucht es einen erfolgreichen Promote
   und eine DaVinci-Evaluation ohne Regressionen.
