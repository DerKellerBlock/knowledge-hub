# Wie das Knowledge Retrieval funktioniert — eine einfache Erklärung

Wenn du den MCP-Server fragst „Wie rotiere ich einen Node3D um die Y-Achse in Godot?",
durchläuft deine Frage eine Pipeline aus vier Komponenten, die aus 24.593 Godot-Chunks
die 10 relevantesten heraussucht. Dieses Dokument erklärt jede Komponente — für Menschen
und AI-Agenten, die das System verstehen wollen, ohne Vektor-Search-Experten zu sein.

| Komponente | Typ | Aufgabe | Zeit |
|-----------|-----|---------|------|
| BGE-M3 | Embedding-Modell | Query in Vektor übersetzen | ~50 ms |
| ChromaDB + BM25 | Zwei parallele Indizes | Semantische + lexikalische Suche | ~100 ms |
| RRF-Fusion | Mathematisches Verfahren | Ergebnisse beider Indizes vereinen | ~1 ms |
| jina-reranker | Cross-Encoder | Query+Chunk-Paare bewerten, Top-10 | ~1–2 s |

---

## Setup-Beispiel

**Frage:** „Wie rotiere ich einen Node3D um die Y-Achse in Godot?"

**Aufgabe:** Aus 24.593 Godot-Chunks (API-Referenz, Tutorials, persönliche Notizen) die
relevantesten finden. Die Pipeline hat vier Stationen:

1. **BGE-M3** übersetzt die Frage in einen 1024-dimensionalen Vektor.
2. **ChromaDB** (semantisch) und **BM25** (lexikalisch) durchsuchen parallel alle Chunks.
3. **RRF-Fusion** vereint die beiden Ergebnislisten zu einer Top-100-Kandidatenliste.
4. **jina-Cross-Encoder** bewertet jedes Query+Chunk-Paar und liefert die finale Top-10.

---

## Komponente 1: BGE-M3 (Embedding-Modell)

### Was es ist

`BAAI/bge-m3` ist ein neuronales Netz (~2,2 GB Download, MIT-Lizenz), das Text in
einen 1024-dimensionalen Vektor übersetzt — eine Liste aus 1024 Zahlen, die die
semantische Bedeutung des Texts repräsentiert. Es versteht bis zu 8192 Token Kontext
und ist multilingual (Englisch, Deutsch, und viele weitere Sprachen).

### Was es macht

Stell dir vor, jeder Satz bekommt eine Zahlen-Signatur. Ähnliche Sätze haben ähnliche
Signaturen:

```
"Wie rotiere ich Node3D um Y?"     → [0.12, -0.45, 0.78, …, 0.33]  (1024 Zahlen)
"How to spin a 3D object on Y axis" → [0.11, -0.43, 0.76, …, 0.31]  (sehr ähnlich!)
"How to bake a pizza"              → [-0.67, 0.21, -0.05, …, -0.88] (ganz anders)
```

Die ersten beiden Vektoren liegen nah beieinander (ähnliche Bedeutung), der dritte
ist weit entfernt (anderes Thema). Genau das nutzt die Suche: Chunks, deren Vektor
dem Query-Vektor ähnlich ist, sind wahrscheinlich relevant.

### Warum multilingual?

Noahs persönliche Notizen (`faq.md`, `tips.md`) sind auf Deutsch, die Godot-Docs auf
Englisch. BGE-M3 versteht beide Sprachen im selben Vektorraum — eine deutsche Notiz
über „3D-Objekt drehen" liegt nah an einem englischen Chunk über „rotate Node3D".

### Wichtig

Bei jeder Suche wird **nur die Query** embeddet (~50 ms). Die 24.593 Chunk-Vektoren
liegen bereits fertig berechnet im ChromaDB-Index auf der Festplatte.

---

## Komponente 2: jina-reranker-v2 (Cross-Encoder)

### Was es ist

`jinaai/jina-reranker-v2-base-multilingual` ist ein neuronales Netz (~548 MB Download,
CC-BY-NC-4.0), das Query und Chunk **gemeinsam** liest und einen Relevanz-Score ausgibt.
Anders als BGE-M3 (ein „Bi-Encoder", der Query und Chunk getrennt embeddet) ist jina
ein „Cross-Encoder": Er kreuzt beide Seiten und versteht den Zusammenhang.

### Was es macht

jina bekommt Paare aus Query + Chunk und bewertet, wie gut sie zusammenpassen:

```
Query + "Node3D.rotate_y() dreht das Objekt um die Y-Achse"  → Score +0,71  (relevant!)
Query + "Die Kamera folgt dem Spieler mit SmoothDamp"        → Score -8,3   (irrelevant)
```

Die Scores sind sigmoid-skaliert (0–1), wobei höhere Werte bessere Relevanz bedeuten.

### Warum ein 2-Stufen-Prozess?

- **Stufe 1 (BGE-M3 + BM25 → RRF):** Liefert 100 Kandidaten — schnell, grob, aber
  mit hoher Recall (die relevanten Chunks sind wahrscheinlich dabei).
- **Stufe 2 (jina):** Bewertet diese 100 Paare — langsam (~1–2 s für 100 Paare),
  aber präzise. Die Top-10 nach jina-Score sind die finale Antwort.

Ein Cross-Encoder über alle 24.593 Chunks laufen zu lassen wäre viel zu langsam.
Die 2-Stufen-Architektur kombiniert Geschwindigkeit mit Genauigkeit.

### Warum multilingual?

Wie BGE-M3 versteht jina mehrere Sprachen. Eine deutsche Notiz und eine englische
Query werden korrekt als zusammengehörig erkannt — das war der Durchbruch für
godot-008 („Why is my 3D model not visible" fand endlich die deutsche `faq.md`).

---

## Komponente 3: ChromaDB + BM25-Index (zwei parallele Speicher)

Zwei völlig unterschiedliche Such-Strategien laufen parallel — sie ergänzen sich.

### ChromaDB (semantisch)

Eine Vektor-Datenbank auf der Festplatte (`chromadb_data/godot/chroma/`, ~1,7 GB).
Pro Chunk speichert sie: ID, Text, 1024-dimensionalen Vektor und Metadaten
(`source_file`, `chunk_type`, `context_prefix`, …).

**Suche:** Vektor-Ähnlichkeit (Cosine Similarity). ChromaDB findet den Chunk, dessen
Vektor dem Query-Vektor am nächsten liegt.

**Stärke:** Findet semantisch Verwandtes ohne Wortüberlappung — „rotate" findet
„drehen", „velocity" findet „Geschwindigkeit".

**Schwäche:** Kann semantisch verwandte, aber thematisch falsche Chunks liefern —
„3D-Objekt drehen" könnte „3D-Kamera bewegen" finden.

### BM25-Index (lexikalisch)

Ein klassischer Suchindex als Pickle-Datei (`chromadb_data/godot/godot_bm25.pkl`,
~14 MB). Pro Chunk speichert er eine tokenisierte Wortliste mit TF-IDF-Gewichtung.
Tokens werden Unicode-aware mit CamelCase-Splitting erzeugt: `CharacterBody3D` wird
zu `["character", "body", "3", "d"]`.

**Suche:** Wort-Überlappung — welche Chunks enthalten die Tokens `rotate`, `node3d`, `y`?

**Stärke:** Präzise bei exakten Begriffen — API-Namen wie `CharacterBody3D`,
`move_and_slide` werden zuverlässig gefunden.

**Schwäche:** Versteht keine Synonyme — „drehen" findet nicht „rotate", „Geschwindigkeit"
findet nicht „velocity".

### Warum beide?

Sie ergänzen sich perfekt. ChromaDB findet das semantisch Passende, BM25 findet das
exakt Benannte. Zusammen sind sie stärker als jede Komponente allein.

---

## Komponente 4: RRF-Fusion (Zusammenführung)

### Das Problem

ChromaDB liefert Cosine-Scores (0–1), BM25 liefert TF-IDF-Scores (0–50). Die Skalen
sind nicht vergleichbar — man kann nicht einfach addieren.

### Die Lösung: Reciprocal Rank Fusion

RRF ist ein mathematisches Verfahren (kein LLM, kein neuronales Netz), das absolute
Scores ignoriert und nur auf **Ränge** (Position in der Liste) schaut:

```
RRF_Score = 1/(k + Rang_in_ChromaDB) + 1/(k + Rang_in_BM25)
```

`k=60` ist eine Glättungskonstante, die verhindert, dass Rang 1 zu dominant wird.

### Konkretes Beispiel

Drei Chunks A, B, C nach der Query „Wie rotiere ich Node3D um Y?":

| Chunk | Rang ChromaDB | Rang BM25 | RRF-Berechnung | RRF-Score |
|-------|---------------|-----------|----------------|-----------|
| A | 3 | 1 | 1/63 + 1/61 | **0,0322** |
| B | 1 | 50 | 1/61 + 1/110 | 0,0255 |
| C | 5 | — (nicht in Top-100) | 1/65 + 0 | 0,0154 |

**Chunk A gewinnt**, weil er in **beiden** Indizes gut rankt — das ist genau das,
was RRF belohnt. Chunk B ist zwar in ChromaDB auf Rang 1, aber BM25 findet ihn kaum.
Chunk C ist nur in einem Index vertreten.

### Output

Eine vereinigte Top-100-Kandidatenliste, sortiert nach RRF-Score — bereit für den
jina-Cross-Encoder.

---

## Die komplette Pipeline

```
Deine Frage: "Wie rotiere ich Node3D um Y?"
                    │
                    ▼
        ┌───────────────────────┐
        │ BGE-M3 embeddet Query │  ~50 ms
        │ → Query-Vektor (1024d)│
        └───────────────────────┘
                    │
        ┌──────────┴──────────┐
        ▼                     ▼
┌──────────────┐      ┌──────────────┐
│  ChromaDB    │      │  BM25-Index  │
│  Vektor-     │      │  Token-      │
│  ähnlichkeit │      │  überlappung │
│  Top-100     │      │  Top-100     │
└──────────────┘      └──────────────┘
        │                     │
        └──────────┬──────────┘
                   ▼
         ┌─────────────────┐
         │ RRF-Fusion      │  ~1 ms (Mathematik)
         │ vereinigt Ränge │
         │ Top-100         │
         └─────────────────┘
                   │
                   ▼
         ┌─────────────────┐
         │ jina Cross-     │  ~1–2 s (100 Paare bewerten)
         │ Encoder bewertet│
         │ Query+Chunk als │
         │ Paare, Top-10   │
         └─────────────────┘
                   │
                   ▼
         Antwort an MCP-Client
         (Top-10 Treffer mit
          source_file, text,
          context_prefix, score)
```

**Gesamtzeit:** ~1–3 Sekunden pro Suche. Komplett lokal, keine Cloud, kein LLM-Call
während der Suche. Die Chunk-Vektoren liegen fertig im Index, nur die Query wird
live embeddet.

---

## Wichtig: context_prefix (Contextual Retrieval)

Jeder Chunk im Index hat ein optionales Feld `context_prefix` — ein 50–100 Token
langer Vorspann, der den Chunk im Gesamtdokument verortet. Dieser wurde **beim
Index-Build** mit `gemma4:cloud` (Ollama-Cloud, 32.7B Parameter) generiert und
in ChromaDB gespeichert.

**Bei der Suche** wird `context_prefix` als Metadaten-Feld zurückgegeben. Es hilft
dem OpenCode-Agent zu verstehen, woher der Chunk stammt — z. B. „Dieser Abschnitt
stammt aus dem Kapitel '3D Transforms' der Godot-Dokumentation und beschreibt die
Rotation von Node3D-Objekten."

**Produktiver Godot-Index (24.593 Chunks):** Contextual BM25 ist aktiviert — das
`context_prefix` fließt in den BM25-Corpus ein. Das hat die Sprachbarriere bei
godot-008 gehoben (deutsche `faq.md` wird jetzt gefunden), aber eine leichte
Regression bei godot-017 verursacht (Performance/LOD-Chunks in `best-practices.md`
sind schlechter auffindbar).

**Produktiver DaVinci-Index (12.561 Chunks):** Contextual BM25 ist aktiviert, aber
nur 6 Chunks sind kontextualisiert. Die restlichen 12.555 sind `late_chunk`-Chunks
aus PDFs — diese sind von Contextual Retrieval ausgenommen (D2), da sie bereits
Chapter-Kontext aus dem Late-Chunking besitzen.

Technische Details zu Contextual Retrieval, Env-Vars und CLI-Skripten siehe
`docs/ai/architecture.md` und `docs/ai/best-practices.md`.

---

## Referenzen

- `docs/ai/architecture.md` — Technische Architektur (referenz-orientiert)
- `docs/ai/best-practices.md` — Env-Vars, CLI-Skripte, Contextual Retrieval CLI
- `docs/ai/known-issues.md` — Bekannte Retrieval-Lücken (godot-017, godot-009, godot-012)
- `docs/superpowers/specs/2026-07-04-acceleration-mps-parallel-design.md` — MPS/Parallel-Spec
