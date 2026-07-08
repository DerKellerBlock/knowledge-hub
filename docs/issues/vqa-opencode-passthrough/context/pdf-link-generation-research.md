# PDF Source-Page Link Generation — Recherche-Kontext

**Task-ID:** vqa-opencode-passthrough (Sub-Feature: PDF Link Generation)
**Datum:** 2026-07-07
**Status:** research-notes (für Task D1, D2, D3)

## Hintergrund

Nach einer erfolgreichen VQA-Query (`@/Users/noahk/Downloads/davinci-resolve-19-2.png`)
lieferte der Knowledge Hub 5 `image_match`-Treffer (Similarity 0.80–0.81)
plus Text-Treffer mit `page_start`/`page_end`-Metadaten. Der Nutzer fragte
daraufhin: „can you tell me where I can find the similar images, i.e.
which PDF, and/or can you give me a command that opens the exact page
where the image and text are in the PDF?"

## Fehlgeschlagener Ansatz: `osascript` keystroke in Preview

Der erste Versuch des Orchestrators nutzte:

```bash
open -a Preview "/pfad/zum/pdf.pdf"
osascript -e 'tell application "Preview" to activate' \
          -e 'tell application "System Events" to keystroke "168" & return'
```

**Warum das fehlschlägt:**

1. **Accessibility-Permissions:** AppleScript GUI-Scripting benötigt
   System-Events-Berechtigung (Systemeinstellungen → Datenschutz →
   Bedienungshilfen). Diese ist nicht immer erteilt.
2. **„Go to Page"-Bar nicht offen:** die Tastatureingabe `168 + return`
   trifft nur die „Go to Page"-Suchleiste, wenn sie bereits offen ist.
   Wenn Preview stattdessen die Thumbnail-Sidebar zeigt, landet die
   Eingabe im falschen Feld.
3. **Timing fragil:** zwischen `open` und `keystroke` vergeht Zeit
   (PDF-Laden), und der keystroke feuert bevor die UI bereit ist.

**Fazit:** dieser Ansatz ist für eine reliable Copy-Paste-Anweisung an
den Nutzer ungeeignet.

## Verifizierte funktionierende Ansätze (macOS Darwin)

### 1. Direkter Browser-Binary mit `#page=N`-Anchor (primärer Ansatz)

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" "file:///abs/path/to/file.pdf#page=168"
```

- Chrome und Firefox nutzen PDF.js (oder nativen PDF-Viewer) mit
  Unterstützung für `#page=N`-Fragment-Anchor.
- **Keine Permissions nötig** — direkter Browser-Binary-Aufruf.
- Springt direkt zur Seite N (1-basiert).
- **Wichtig:** `open -a "Google Chrome" "file://...#page=N"` ist
  verworfen. Live-Debugging zeigte, dass macOS `open` das Fragment bei
  lokalen PDF-URLs nicht zuverlässig an die Ziel-App weiterreicht:
  Chrome/Safari sahen per AppleScript nur `file://...pdf` ohne
  `#page=168`. Der direkte Chrome-Binary-Aufruf bewahrte das Fragment
  und wurde vom Nutzer als funktionierend bestätigt.

**Getestete Browser:**

- ✅ Google Chrome — direkter Binary mit `#page=N` funktioniert
  zuverlässig.
- ✅ Firefox — direkter Binary mit `#page=N` soll analog funktionieren
  (Fallback; noch nicht so stark verifiziert wie Chrome).
- ❌ `open -a` — strippt/ignoriert `#page=N` bei lokalen PDFs.
- ⚠️ Safari — kein verlässlicher Page-Anchor-Fallback; nutze `open`
  ohne Anchor + Warnung „manuell zu Seite N navigieren".

### 2. Quick Look auf extrahierten Screenshot

```bash
qlmanage -p "domains/davinci_resolve/images/<source>/<file>.pdf-<page>-<idx>.png"
```

- Zeigt den indexierten Screenshot direkt (kein PDF-Öffnen nötig).
- Nutzt das `image_path`-Feld, das bereits im `image_match`-Result
  steht.
- Schnellster Weg, um zu sehen, was SigLIP-2 gematcht hat.

### 3. Direkter Screenshot-Open in Preview

```bash
open "domains/davinci_resolve/images/<source>/<file>.pdf-<page>-<idx>.png"
```

- Öffnet die PNG in Preview (Default-App für Bilder).
- Alternative zu Quick Look, falls der Nutzer das Bild länger
  betrachten oder zoomen will.

## Page-Numbering-Ambiguität

### `image_match.page` — geklärt (VRF-001)

- `page` in `image_match`-Resultaten und `image_manifest.json` ist
  **0-basiert** (PyMuPDF4LLM-Konvention).
- 1-basierte PDF-Seite für Browser = `page + 1`.

### `page_start`/`page_end` in text `late_chunk`-Chunks — geklärt

- `docs/ai/known-issues.md` LIM-004 referenziert `page_start`/
  `page_end` als „PDF-Seitennummern" mit ±2 Toleranz; die Basis war
  vor Task D2 unklar.
- Beobachteter Treffer: `page_start: 521, page_end: 522` für
  „The Cut page Timeline controls" (Reference Manual).
- **Verifikation in Task D2:** `pdftotext -f 521 -l 521` fand den Text
  nicht, `pdftotext -f 522 -l 522` fand ihn. Damit ist
  `page_start=521` → PDF-Seite 522 und `page_start` ist 0-basiert.
- **Regel:** 1-basierte PDF-Seite = `page_start + 1`.

## Browser-Detection-Logik

```bash
test -x "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
test -x "/Applications/Firefox.app/Contents/MacOS/firefox"
```

**Fallback-Chain:**

1. Chrome-Binary gefunden → `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" "file://...#page=N"`.
2. Firefox-Binary (kein Chrome) → `"/Applications/Firefox.app/Contents/MacOS/firefox" "file://...#page=N"`.
3. Kein Chrome/Firefox → `open "file://..."` (kein Page-Anchor) +
   Warnung ausgeben: „Kein Chrome/Firefox-Binary gefunden — bitte
   manuell zu Seite N navigieren."

## PDF-Pfad-Mapping (DaVinci-Quellen)

Verifiziertes Mapping `source_file` (.md) → PDF (.pdf) anhand
`domains/davinci_resolve/sources/` und `domains/davinci_resolve/
sources/raw/`:

| source_file (.md) | PDF (.pdf) |
|---|---|
| davinci-resolve-20-advanced-visual-effects.md | DaVinci-Resolve-20-Advanced-Visual-Effects.pdf |
| davinci-resolve-20-beginners-guide.md | DaVinci-Resolve-20_Beginners-Guide.pdf |
| davinci-resolve-20-colorist-guide.md | DaVinci-Resolve-20-Colorist-Guide.pdf |
| davinci-resolve-20-editors-guide.md | DaVinci-Resolve-20-Editors-Guide.pdf |
| davinci-resolve-20-fairlight-audio-post.md | DaVinci-Resolve-20-Fairlight-Audio-Post.pdf |
| davinci-resolve-20-fusion-visual-effects.md | DaVinci-Resolve-20-Fusion-Visual-Effects.pdf |
| davinci-resolve-20.3-reference-manual.md | DaVinci_Resolve_20.3_Reference_Manual.pdf |
| davinci-resolve-21-new-features-guide.md | DaVinci_Resolve_21_New_Features_Guide.pdf |
| fairlight-live-user-manual.md | FairlightLiveUserManual.pdf |
| fusion-20.3-manual.md | Fusion20.3_Manual.pdf |

**Konvention:** Case-Unterschiede (DaVinci vs davinci), Unterstrich-
vs Bindestrich-Platzierung variieren. Daher ist ein case-insensitive
Lookup via `ls domains/<domain>/sources/raw/ | grep -i "<basename>"`
robust als ein hardcodiertes Mapping.

## Beispielpfade für die 5 VQA-Hits des Nutzer-Tests

(Die exakten Seitenzahlen hängen von der konkreten VQA-Query ab; diese
Tabelle zeigt das generierte Kommando-Format. Beispielseiten aus dem
Nutzer-Test, sim/0.80–0.81.)

| Treffer | source_file | page (0-basiert) | PDF-Seite (1-basiert) | Browser-Kommando |
|---|---|---|---|---|
| Beginners Guide p.168 | davinci-resolve-20-beginners-guide.md | 167 | 168 | `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" "file://$REPO/domains/davinci_resolve/sources/raw/DaVinci-Resolve-20_Beginners-Guide.pdf#page=168"` |
| Beginners Guide p.170 | davinci-resolve-20-beginners-guide.md | 169 | 170 | `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" "file://$REPO/domains/davinci_resolve/sources/raw/DaVinci-Resolve-20_Beginners-Guide.pdf#page=170"` |
| Reference Manual p.839 | davinci-resolve-20.3-reference-manual.md | 838 | 839 | `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" "file://$REPO/domains/davinci_resolve/sources/raw/DaVinci_Resolve_20.3_Reference_Manual.pdf#page=839"` |
| Reference Manual p.955 | davinci-resolve-20.3-reference-manual.md | 954 | 955 | `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" "file://$REPO/domains/davinci_resolve/sources/raw/DaVinci_Resolve_20.3_Reference_Manual.pdf#page=955"` |
| Reference Manual p.60 | davinci-resolve-20.3-reference-manual.md | 59 | 60 | `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" "file://$REPO/domains/davinci_resolve/sources/raw/DaVinci_Resolve_20.3_Reference_Manual.pdf#page=60"` |

`$REPO` ist der Knowledge-Hub-Repo-Root (für den Orchestrator das
aktuelle Working Directory, via `os.path.abspath` auflösbar).

Für jeden `image_match`-Treffer wird zusätzlich generiert:

```bash
qlmanage -p "<abs_path_to_extracted_png_aus_image_path_feld>"
```

## Quellen

- `docs/ai/known-issues.md` VRF-001 — `page` ist 0-basiert.
- `docs/ai/known-issues.md` LIM-004 — `page_start`/`page_end` ±2.
- `domains/davinci_resolve/sources/raw/` — 10 PDFs (siehe Mapping-Tabelle).
- `domains/davinci_resolve/sources/*.md` — 10 packed Markdown-Quellen.
- Live-Verifikation des Nutzers in dieser Session (direkter Chrome-
  Binary mit `#page=` funktioniert; `open -a ... #page=` failt,
  weil das Fragment nicht bei der App ankommt; qlmanage und
  `open <png>` funktionieren; `osascript keystroke` failt).
