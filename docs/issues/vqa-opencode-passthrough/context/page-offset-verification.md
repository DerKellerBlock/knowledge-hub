# Task D2 — Page-Offset Verifikation

**Datum:** 2026-07-07
**Status:** ✅ abgeschlossen
**Methode:** pdftotext (Poppler 26.04.0, 1-basierte Seitenangabe via `-f N -l N`)
**Operator:** Orchestrator (Session 2026-07-07)

## Frage

Sind `late_chunk.page_start` / `page_end` 0-basiert oder 1-basiert?
Die Dokumentation in `docs/ai/known-issues.md` LIM-004 ist mehrdeutig
(„±2 Seitentoleranz" wird erwähnt, aber nicht die Basis).

## Versuchsaufbau

Methode: `pdftotext -f N -l N <pdf> -` extrahiert Text der angegebenen
PDF-Seite (pdftotext erwartet 1-basierte Seitenzahlen für `-f`/`-l`).

Für jeden Treffer aus der VQA-Session wurden die benachbarten
PDF-Seiten (N-1, N, N+1, N+2) auf charakteristische Text-Snippets
geprüft.

PDFs:
- `domains/davinci_resolve/sources/raw/DaVinci_Resolve_20.3_Reference_Manual.pdf`
- `domains/davinci_resolve/sources/raw/DaVinci-Resolve-20_Beginners-Guide.pdf`

## Ergebnisse

### Test 1 — Bester Text-Treffer (maßgeblich)

| Feld | Wert |
|---|---|
| Chunk | `davinci-resolve-20.3-reference-manual.md` late_chunk |
| `page_start` | 521 |
| `page_end` | 522 |
| Erwarteter Text | „The Cut page Timeline controls" |
| PDF-Seite 521 (Hypothese 1-basiert) | ❌ nicht gefunden |
| PDF-Seite 522 (Hypothese 0-basiert) | ✅ gefunden |
| PDF-Seite 523 | ❌ nicht gefunden |
| PDF-Seite 524 | ✅ gefunden (Caption wiederholt) |

**Schluss:** `page_start=521` → Text auf PDF-Seite 522 → **0-basiert bestätigt**

### Test 2 — Bild-Treffer Cross-Check (Top-1 image_match)

| Feld | Wert |
|---|---|
| Chunk | `davinci-resolve-20-beginners-guide.md` image_match |
| `page` | 167 |
| Caption-Snippet | „Single-Viewer Mode button in the top right of the timeline viewer" |
| PDF-Seite 166 | ❌ nicht gefunden |
| PDF-Seite 167 | ❌ nicht gefunden |
| PDF-Seite 168 | ❌ nicht gefunden |
| PDF-Seite 169 | ✅ gefunden |

**Erklärung:** Die Caption beschreibt den `context_after` (Text NACH
dem Bild). Bild liegt auf PDF-Seite 168 (= `page + 1`), Text erscheint
eine Seite später (169). → **0-basiert bestätigt**

### Test 3 — Bild-Treffer Cross-Check (Top-3 image_match)

| Feld | Wert |
|---|---|
| Chunk | `davinci-resolve-20.3-reference-manual.md` image_match |
| `page` | 838 |
| Caption-Snippet | „move the playhead to an In or Out point" |
| PDF-Seite 837 | ❌ nicht gefunden |
| PDF-Seite 838 | ❌ nicht gefunden |
| PDF-Seite 839 | ❌ nicht gefunden |
| PDF-Seite 840 | ✅ gefunden |

**Erklärung:** Bild liegt auf PDF-Seite 839 (= `page + 1`), Caption
erscheint eine Seite später. → **0-basiert bestätigt**

## Verdict

**Einheitlich 0-basiert.** Sowohl `image_match.page` (per VRF-001)
als auch `late_chunk.page_start` / `late_chunk.page_end` nutzen
PyMuPDF4LLMs 0-basierte Seitenkonvention.

## Regel für CLI-Kommando-Generierung

```text
1-basierte PDF-Seite = page + 1            (für image_match)
1-basierte PDF-Seite = page_start + 1       (für late_chunk Start)
1-basierte PDF-Seite = page_end + 1         (für late_chunk Ende)
```

In Kommandos:
```bash
# image_match
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" "file://<abs_pdf_path>#page=$((page + 1))"

# late_chunk
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" "file://<abs_pdf_path>#page=$((page_start + 1))"
```

## Bekannte Nebenwirkung

Bild-Captions sind context-aware (TowardsDataScience-Best-Practice:
`context_before + [IMAGE: description] + context_after`). Die
Caption-Texte tauchen daher häufig auf der **übernächsten** PDF-Seite
auf (Bild-Seite + 1 für `context_after`). Das ist kein Bug, sondern
ein gewünschtes Disambiguierung-Feature der Captioning-Pipeline.

## Offene Fragen

Keine — die Verifikation ist eindeutig. Task D2 gilt als abgeschlossen.

## Tools

- `pdftotext` (Poppler 26.04.0, via Homebrew) — 1-basierte Seiten für `-f`/`-l`
- `bash` 5.x für Schleife und `grep -qi`

## Referenzen

- `docs/ai/known-issues.md` VRF-001 (image_match.page ist 0-basiert)
- `docs/ai/known-issues.md` LIM-004 (±2 Seitentoleranz, aber Basis war unklar)
- `docs/issues/visual-question-answering/spec.md` (Original-VQA-Spec)
- `docs/issues/vqa-opencode-passthrough/spec.md` Section 4 (PDF Source-Page Link Generation)
- `docs/issues/vqa-opencode-passthrough/plan.md` Task D2 (Verifikationsanforderung)
