# Spec: VQA OpenCode-Passthrough (Drag-Drop / Clipboard / @-Mention)

**Task-ID:** vqa-opencode-passthrough
**Datum:** 2026-07-07
**Status:** open
**Priorität:** high

## Problem

Das VQA-Feature (`docs/issues/visual-question-answering/`) erwartet,
dass der OpenCode-Orchestrator den absoluten Pfad eines hochgeladenen
Bildes an `search_knowledge(image_path=...)` weitergibt. Die
Original-Spec nennt beispielhaft `/tmp/opencode/uploads/img-xyz.png`
als Pfad, den „OpenCode liefert".

Verifikation in **OpenCode v1.17.15** (siehe
`context/root-cause-investigation.md`): diese Annahme ist **falsch**.
OpenCode kodiert Drag-Drop-Bilder als `data:image/png;base64,...` in
der User-Message und verliert den ursprünglichen macOS-Datei-Pfad,
bevor die Nachricht den Orchestrator-Agent erreicht. Die relevanten
OpenCode-PRs (#21633, #30153, #32680, #22218) sind unmerged/abandoned.

Das VQA-Feature funktioniert also **nur, wenn der Nutzer den Pfad
manuell tippt** — ein daily-workflow-Blocker für den Mac-Nutzer, der
häufig DaVinci-Resolve-Screenshots zieht und „was ist das rechts
unten bei Scope?" fragt.

Knowledge Hub-seitig ist alles implementiert und getestet:
- `search_knowledge(..., image_path=None)` (`tools.py:86`)
- `image_similarity_search(domain, image_path, top_k=10)`
  (`hybrid_search.py:232`)
- Tests in `tests/unit/test_image_similarity.py`

**Die Lücke liegt ausschließlich auf der OpenCode→MCP-Grenze**, nicht
im Knowledge Hub.

## Ziel

Biete drei **unabhängige** Lösungsansätze, die der Nutzer einzeln oder
kombiniert umsetzen kann. Jeder Ansatz schließt die Lücke auf einem
anderen Weg:

1. **Approach A — `@`-Mention Passthrough:** Orchestrator-Prompt
   instruiert den Agent, `@/abs/path.png` aus der User-Message zu
   extrahieren und an `search_knowledge(image_path=...)` weiterzugeben.
2. **Approach B — `get_recent_image_path()` MCP-Tool:** Neues MCP-Tool
   scannt Desktop/Downloads/Pictures/Clipboard nach dem jüngsten Bild
   und liefert den Pfad. Löst Drag-Drop/Clipboard-Paste ohne
   `@`-Mention.
3. **Approach C — Lokales OpenCode-Plugin:** Patcht die
   Message-Pipeline, sodass Drag-Drop-Bilder nach
   `/tmp/knowledge-hub-attachments/...` gespeichert und der Pfad als
   Text-Part injiziert wird. Löst die Wurzel, erfordert aber eine
   OpenCode-Plugin-API, die in v1.17.15 nicht formal existiert.

Die drei Ansätze sind bewusst unabhängig, damit der Nutzer nach
Aufwand/Verlässlichkeit wählen kann (A=sofort, B=robust für Mac,
C=langfristig generisch).

## Architektur

### Heutiger (gebrochener) Flow

```
Nutzer drag-drop Bild ─┐
                       ▼
OpenCode TUI (v1.17.15) ─ data:image/png;base64,... ─┐
                                                      ▼
Orchestrator-Agent ─ sieht base64, KEIN Pfad ─ kann image_path NICHT setzen
                                                      │
                                                      ▼
search_knowledge(domain, query, image_path=None) ─ Text-Suche only
```

### Approach A — @-Mention Passthrough (fixiert den Text-Pfad)

```
Nutzer tippt: "was ist das rechts unten? @/Users/noahk/Desktop/shot.png"
                       │
                       ▼
Orchestrator-Prompt (NEU: parse @-Mentions) ─ extrahiert /Users/noahk/Desktop/shot.png
                       │
                       ▼
search_knowledge(domain="davinci_resolve", query="Scope panel UI",
                 image_path="/Users/noahk/Desktop/shot.png", mode="hybrid")
                       │
                       ▼
image_similarity_search ─ Top-K image_match ─ Captions → Antwort
```

### Approach B — `get_recent_image_path()` MCP-Tool

```
Nutzer paste screenshot ─ kein Pfad sichtbar
                       │
Nutzer fragt: "was ist das in der UI?"
                       │
                       ▼
Orchestrator ruft: get_recent_image_path(max_age_minutes=5,
                                         include_clipboard=True)
                       │
                       ▼
MCP-Tool scannt:
  ~/Desktop        (mtime ≤ 5min, *.png|*.jpg)
  ~/Downloads      (mtime ≤ 5min, *.png|*.jpg)
  ~/Pictures/Screenshots (mtime ≤ 5min)
  macOS-Clipboard  (osascript: «class furl»)
                       │
                       ▼
Return: "/Users/noahk/Desktop/Screenshot 2026-07-07 at 21.43.png"
                       │
                       ▼
search_knowledge(domain="davinci_resolve", query="...",
                 image_path="<path>", mode="hybrid")
```

### Approach C — Lokales OpenCode-Plugin

```
Nutzer drag-drop Bild ─┐
                       ▼
OpenCode-Plugin-Hook (chat.message, pre-LLM) ─ NEU
  ├─ decode base64 → PNG bytes
  ├─ write /tmp/knowledge-hub-attachments/<sessionID>/<timestamp>.png
  └─ inject TEXT-PART: "[attachment: /tmp/.../<ts>.png]"
                       │
                       ▼
Orchestrator-Agent ─ sieht Text-Part mit Pfad ─ reicht an search_knowledge
                       │
                       ▼
search_knowledge(image_path="/tmp/.../<ts>.png")
```

## Anforderungen

### 1. Approach A: Orchestrator-Prompt `@`-Mention-Passthrough

**Datei:** `.opencode/agents/orchestrator-knowledge.md` (existierend,
206 Zeilen, hat bereits `### Visual Question Answering`-Sektion bei
Line 158).

- Erweitere die bestehende VQA-Sektion um eine **`@`-Mention-Detection**
  -Subsektion. Der Prompt instruiert den Agent:
  1. Scanne die User-Message-Text-Parts nach
     `@(/[^)\s]+\.(?:png|jpg|jpeg|webp))` (case-insensitive).
  2. Bei Treffer: extrahiere den Pfad (ohne `@`), validiere dass er
     absolut ist (Start mit `/`), und rufe `search_knowledge` mit
     `image_path=<pfad>` auf.
  3. Bei mehreren `@`-Mentions: nutze den ersten Bild-Pfad (oder frag
     den Nutzer nach Bestätigung).
  4. Falls kein `@`-Mention, aber eine Bild-Referenz als `data:`-URL:
     informiere den Nutzer, dass Drag-Drop aktuell nicht unterstützt
     wird und schlage `@/pfad/zum/bild.png` oder Approach B/C vor.
- Kein Python-Code — das ist eine reine Prompt-Instruktion.
- **Backward-kompatibel:** der bestehende `image_path`-Passthrough-Text
  (Lines 163–170) bleibt erhalten; die `@`-Mention-Logik ergänzt sie.

**Code-Referenz:** die Regex-Extraktion passiert im LLM-Head, nicht im
Knowledge Hub-Code. Der Knowledge Hub-Code ist unverändert.

### 2. Approach B: Neues MCP-Tool `get_recent_image_path()`

**Datei:** `mcp_servers/knowledge_hub/tools.py` (285 Zeilen) +
`mcp_servers/knowledge_hub/server.py` (203 Zeilen).

- Neue Funktion in `tools.py`:
  ```python
  def get_recent_image_path(
      max_age_minutes: int = 5,
      scan_dirs: list[str] | None = None,
      include_clipboard: bool = True,
  ) -> dict:
      """
      Finde den jüngsten Bild-Pfad für VQA-Passthrough.

      Scannt Desktop, Downloads, Pictures/Screenshots und (optional)
      die macOS-Zwischenablage nach Bilddateien (png/jpg/jpeg/webp),
      die in den letzten `max_age_minutes` Minuten erstellt/modifiziert
      wurden. Gibt den Pfad der jüngsten Datei zurück, oder None.

      Returns: {"image_path": str | None, "source": str,
                 "mtime": str | None}
        - source: "desktop" | "downloads" | "screenshots" | "clipboard"
        - mtime: ISO-8601 oder None
      """
  ```
- Default `scan_dirs = ["~/Desktop", "~/Downloads",
  "~/Pictures/Screenshots"]` (expandiert via `os.path.expanduser`).
- Filesystem-Scan via `os.walk` (nicht `subprocess.run(["find", ...])`,
  um Portabilität zu wahren; `find` wäre schneller, aber `os.walk`
  reicht für ~3 Verzeichnisse).
- Clipboard via `subprocess.run(["osascript", "-e",
  'get the clipboard as «class furl»'])` → parse POSIX-Pfad aus
  `«class furl»:`-Resultat. Graceful fallback: bei nicht-macOS oder
  keinem Bild im Clipboard → `source="clipboard", image_path=None`.
- **Security:** validiere, dass jeder Treffer-Pfad **unter** einem der
  `scan_dirs` liegt (`os.path.realpath` + Prefix-Check). Kein
  Symlink-Following außerhalb der Scan-Dirs (`os.path.realpath` statt
  `os.path.abspath`, `os.path.islink`-Check). Rejiziere Pfade mit
  `..`-Traversal oder absolute Pfade außerhalb der Allowlist.
- **MCP-Registrierung:** in `server.py`:
  1. Import `get_recent_image_path` (Line ~38).
  2. Neues `Tool(...)`-Entry in `list_tools_handler` (Lines 67–142)
     mit Schema:
     ```json
     {
       "name": "get_recent_image_path",
       "description": "Finde den jüngsten Bild-Pfad (Desktop/Downloads/Screenshots/Clipboard) für VQA-Passthrough. Mac-spezifisch.",
       "inputSchema": {
         "type": "object",
         "properties": {
           "max_age_minutes": {"type": "integer", "default": 5},
           "include_clipboard": {"type": "boolean", "default": true}
         }
       }
     }
     ```
  3. `elif name == "get_recent_image_path":` Branch in
     `call_tool_handler` (Lines 145–182).
- **Orchestrator-Prompt:** erweitere die VQA-Sektion um die Instruktion,
  dass der Agent bei einer Bild-Frage ohne sichtbaren Pfad proaktiv
  `get_recent_image_path()` aufrufen soll, um den Pfad zu beschaffen.

### 3. Approach C: Lokales OpenCode-Plugin (Research-Spike first)

- **Schritt 1 (Research-Spike):** verifiziere, ob OpenCode v1.17.15 eine
  Plugin-API für `chat.message`-Hooks (pre-LLM) unterstützt. Lese
  `packages/opencode/src/plugin/` und `packages/plugin/` im
  OpenCode-Source (lokaler Clone oder GitHub). Dokumentiere:
  - existiert ein Hook-Typ, der Message-Parts **vor** dem LLM-Call
    modifizieren kann?
  - ist der Hook stabil dokumentiert oder undokumentiert?
  - gibt es ein Plugin-Loader-Mechanismus (Config-Eintrag in
    `opencode.json`, `~/.config/opencode/plugins/`, ...)?
- **Schritt 2 (falls API existiert):** schreibe ein Plugin
  (`plugins/knowledge-hub-image-passthrough/` in diesem Repo oder als
  separater Skill) das:
  1. Bei `chat.message` (pre-LLM) alle `data:image/...;base64,...` Parts
     findet.
  2. PNG-Bytes dekodiert → schreibt nach
     `/tmp/knowledge-hub-attachments/<sessionID>/<timestamp>.png`.
  3. Einen synthetischen Text-Part `[attachment:
     /tmp/.../<ts>.png]` **vor** dem Bild-Part injiziert.
  4. Optional: den `data:`-Part durch eine `file://`-Referenz ersetzt
     (falls das Modell das unterstützt — sonst Text-Part als Fallback).
- **Schritt 3 (falls API NICHT existiert):** Approach C ist blockiert
  bis OpenCode PR #21633 merged. Dokumentiere als `blocked` im Plan
  und verweise auf Approach A/B als Workaround.

**Skill-Distribution:** falls das Plugin als OpenCode-Skill
distributiert werden soll, lege es unter
`.agents/skills/knowledge-hub-image-passthrough/SKILL.md` ab (analog
der bestehenden Skills-Struktur).

### 4. PDF Source-Page Link Generation (cross-cutting, gilt für alle 3 Approaches)

**Konzept:** Wenn der Orchestrator VQA-Results (`image_match`-Treffer)
oder Text-Such-Treffer mit PDF-Seiten-Metadaten zurückgibt, soll er
copy-paste-fertige CLI-Kommandos generieren, die den Nutzer die exakte
PDF-Seite in einem Browser öffnen lassen (Chrome/Firefox-Binary direkt
mit `file://...#page=N`) oder den extrahierten Screenshot direkt per
Quick Look anzeigen.

**Hintergrund:** Der Nutzer fragt nach einer VQA-Query typischerweise
„wo finde ich das im Handbuch?" — aktuell liefert der Knowledge Hub
nur `page`/`page_start`/`page_end` als Zahlen und `source_file` als
Markdown-Basename. Der Nutzer müsste selbst die PDF finden, die Seite
umrechnen und das PDF-Programm bedienen. Diese Sub-Feature schließt
diese Lücke durch Prompt-Instruktion (kein Code-Change am Knowledge Hub).

**Anforderungen:**

- Für jeden `image_match`-Treffer mit `page`- und `source_file`-Feld:
  - Berechne 1-basierte PDF-Seite = `page + 1` (da `page` 0-basiert
    ist, siehe VRF-001).
  - Finde die tatsächliche PDF-Datei: mappe `source_file` (z.B.
    `davinci-resolve-20-beginners-guide.md`) auf den Roh-PDF-Pfad
    `domains/<domain>/sources/raw/<pdf-filename>.pdf` — eine
    Helper-Funktion oder Lookup-Tabelle ist nötig (der `source_file`-
    Basename ohne `.md`-Endung entspricht ungefähr dem PDF-Filename,
    aber verifiziere das exakte Mapping in der Implementierung).
  - Generiere zwei Kommandos:
    1. **PDF an Seite öffnen (Browser):**
       `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" "file://<abs_path_to_pdf>#page=<N>"`
       (mit Fallback auf den Firefox-Binary, falls Chrome nicht installiert).
    2. **Quick Look extrahierter Screenshot:**
       `qlmanage -p "<abs_path_to_extracted_png>"` — nutzt das
       `image_path`-Feld, das bereits im Result steht.
- Für jeden Text-Treffer (`modality: text`) mit `page_start`/`page_end`
  und `source_type: repo` mit `chunk_type: late_chunk`:
  - Berechne PDF-Seite (1-basiert) = `page_start + 1` (0-basiert,
    verifiziert in Task D2; siehe `context/page-offset-verification.md`).
  - Generiere: `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" "file://<abs_path_to_pdf>#page=<N>"`.
- **Browser-Erkennung:** bevorzugt Chrome, Fallback Firefox, Fallback
  `open` (Default-App, kein Page-Anchor) mit gedruckter Warnung, dass
  der Nutzer manuell navigieren muss.
- **Wichtig:** `open -a "Google Chrome" "file://...#page=N"` ist
  **nicht** zulässig. Live-Verifikation zeigte, dass macOS `open` das
  URL-Fragment bei lokalen PDF-URLs nicht zuverlässig an die Ziel-App
  weiterreicht; Chrome/Safari sahen nur `file://...pdf` ohne `#page=N`.
  Der direkte Browser-Binary-Aufruf erhält das Fragment und springt zur
  korrekten Seite.
- **Pfad-Handling:** alle generierten Pfade müssen absolut sein (auflösen
  via `os.path.abspath` relativ zum Knowledge-Hub-Repo-Root, da der
  Orchestrator von dort läuft).
- **Keine Code-Änderung an den Knowledge Hub Tools** — das ist reine
  Orchestrator-Prompt-Arbeit, analog Approach A. Der Orchestrator
  konstruiert die Kommandos im Antwort-Text, indem er die `image_path`-,
  `page`- und `source_file`-Felder aus den Suchergebnissen liest.

**Browser-Fallback-Chain:**

```
1. Try: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" "file://...#page=N"
2. Falls Chrome nicht installiert: "/Applications/Firefox.app/Contents/MacOS/firefox" "file://...#page=N"
3. Falls beide fehlen: open "file://..." (kein Page-Anchor, Warnung ausgeben)
```

**PDF-Pfad-Auflösung:**

Der Orchestrator muss `source_file` (z.B.
`davinci-resolve-20-beginners-guide.md`) auf den tatsächlichen PDF-
Filename mappen. Die Konvention ist:

- `source_file` stript `.md` → `davinci-resolve-20-beginners-guide`.
- Ersetze Bindestriche/Unterstriche basierend auf den tatsächlichen
  PDF-Filenames in `domains/<domain>/sources/raw/`.
- Für DaVinci: `davinci-resolve-20-beginners-guide.md` →
  `DaVinci-Resolve-20_Beginners-Guide.pdf` (Case- + Unterstrich-
  Unterschiede).

Da das Mapping nicht 1:1 durch einfache String-Manipulation möglich
ist (Case-Unterschiede, Unterstrich-Platzierung), sollte der
Orchestrator `glob` oder `bash` mit `ls domains/<domain>/sources/raw/`
nutzen, um die tatsächliche PDF-Datei zur Antwort-Zeit zu finden. Das
ist zuverlässig und braucht keine Helper-Funktion.

**Quellen-Verifikation (in dieser Session durchgeführt):**

- `domains/davinci_resolve/sources/raw/` enthält 10 PDFs (siehe
  `context/pdf-link-generation-research.md` für die vollständige Liste).
- Das Mapping `*.md` → `*.pdf` ist case-insensitive-basierbar, aber
  nicht trivial (z.B. `davinci-resolve-20.3-reference-manual.md` →
  `DaVinci_Resolve_20.3_Reference_Manual.pdf`).
- Beispielpfade: `davinci-resolve-20-beginners-guide.md` →
  `DaVinci-Resolve-20_Beginners-Guide.pdf`.

**Page-Numbering-Konvention (siehe VRF-001):**

- `page` in `image_match`-Resultaten und `image_manifest.json` ist
  **0-basiert** (PyMuPDF4LLM-Konvention).
- `page_start`/`page_end` in Text-Chunks (`late_chunk`-Typ) sind
  ebenfalls **0-basiert**. Task D2 verifizierte das via `pdftotext`:
  Treffer `page_start=521` enthält „The Cut page Timeline controls" auf
  PDF-Seite 522.

Für die Nutzer-Anfrage ist die sicherste Konvention:

- Für `image_match`-Treffer: PDF-Seite (1-basiert) = `page + 1`.
- Für Text-`late_chunk`-Treffer: PDF-Seite (1-basiert) = `page_start + 1`.


## Akzeptanzkriterien

### Approach A (alle erfüllt → A done)

1. `.opencode/agents/orchestrator-knowledge.md` enthält eine
   `@`-Mention-Detection-Instruktion mit Regex-Beispiel und
   Bild-Dateiendungs-Whitelist (png/jpg/jpeg/webp).
2. Integration-Test in `tests/mcp/test_orchestrator_image_passthrough.py`
   mocked eine User-Message mit `@/tmp/test.png` und verifiziert, dass
   die simulierte Tool-Call-Argument-Extraktion den Pfad korrekt liefert
   (Test des Prompt-Verhaltens via Prompt-Text-Assertion, nicht via
   echtem LLM-Call — siehe Plan Task A2).
3. Manueller Smoke-Test: Nutzer tippt
   `was ist das rechts unten? @/Users/noahk/Desktop/shot.png` →
   Orchestrator ruft `search_knowledge` mit korrektem `image_path` auf.
4. `pytest -m unit -q` bleibt grün.
5. `pytest -m mcp -q` bleibt grün.

### Approach B (alle erfüllt → B done)

6. `get_recent_image_path()` in `tools.py` implementiert mit
   Signatur `(max_age_minutes=5, scan_dirs=None, include_clipboard=True)
   -> dict`.
7. Security-Validierung: alle Treffer-Pfade liegen unter einem
   `scan_dir` (realpath + prefix-check); Unit-Test mit Path-Traversal-
   und Symlink-Escape-Versuchen.
8. `server.py` registriert das Tool (Schema + handler branch).
9. Unit-Tests in `tests/unit/test_get_recent_image_path.py`:
   - mocked filesystem (tmp_path) → jüngste Datei gefunden
   - leeres Dir → `image_path=None`
   - Datei älter als `max_age_minutes` → `None`
   - clipboard-osascript mocked → Pfad zurück
   - clipboard ohne Bild → `None`
   - path-traversal-Versuch → rejected (security)
   - symlink-escape außerhalb scan_dir → rejected
10. MCP-Contract-Test in `tests/mcp/test_get_recent_image_path.py`
    ruft die Tool-Funktion über den `call_tool_handler` auf.
11. Orchestrator-Prompt erweitert: proaktiver
    `get_recent_image_path()`-Call bei Bild-Fragen ohne Pfad.
12. `pytest -m unit -q` und `pytest -m mcp -q` grün.

### Approach C (alle erfüllt → C done ODER blocked dokumentiert)

13. Research-Spike-Dokument `docs/issues/vqa-opencode-passthrough/
    context/opencode-plugin-api-research.md` existiert und
    dokumentiert, ob v1.17.15 einen `chat.message` pre-LLM Hook hat.
14. Falls API existiert: Plugin implementiert, Smoke-Test in
    `/tmp/knowledge-hub-attachments/...` schreibt PNG + injiziert
    Text-Part.
15. Falls API nicht existiert: Plan markiert Approach C als `blocked`,
    verweist auf PR #21633, und der Nutzer kann Approach A/B als
    Workaround nutzen.

### Übergreifend

16. `docs/ai/open-work.md` Eintrag für `vqa-opencode-passthrough`
    bleibt `open`, bis mindestens ein Approach done ist.
17. `docs/issues/vqa-opencode-passthrough/retrospective.md` +
    `explanation.md` werden bei Abschluss geschrieben (Standard-Workflow).
18. Keine bestehende Funktionalität regrediert
   (`tests/unit/test_image_similarity.py` bleibt grün).
19. Orchestrator-Prompt (`.opencode/agents/orchestrator-knowledge.md`)
    instruiert den Agent, bei `image_match`- und `late_chunk`-Text-
    Treffern mit `page`-/`page_start`-Metadaten copy-paste-fertige
    CLI-Kommandos zu generieren (direkter Chrome-Binary mit `#page=N`,
    Fallback direkter Firefox-Binary, Fallback `open` ohne Page-Anchor).
20. Generierte Pfade sind absolut (via `os.path.abspath` oder
    repo-root-aware).
21. Page-Offset ist korrekt: `image_match.page + 1` für 1-basierte
    PDF-Seite; für Text-`late_chunk` ist der Offset in Task D2 verifiziert
    und im Prompt dokumentiert.
22. PDF-Dateiname wird zur Laufzeit via `ls`/`glob` aufgelöst (kein
    hardcodiertes Mapping).
23. Manuelles Smoke-Test: VQA-Query mit `@/pfad/zum/bild.png` liefert
    Ergebnisse + copy-paste-fähige direkte Browser-Binary-Kommandos
    (`.../Google Chrome` oder `.../firefox` mit `#page=N`), die den
    Nutzer auf der richtigen PDF-Seite landen lassen.
24. `pytest -m unit -q` und `pytest -m mcp -q` bleiben grün.

## Nicht-Ziele

- Keine Änderung an `search_knowledge`-Signatur oder
  `image_similarity_search` (Knowledge Hub-seitig ist fertig).
- Keine OCR-Texterkennung (SigLIP-2 bleibt visuell — siehe VQA-002).
- Keine Cross-Platform-Version von Approach B (macOS-spezifisch via
  `osascript`; Linux/Windows-Clipboard-Support wäre ein Folgetask).
- Keine generische OpenCode-Plugin-Fix-PR (das wäre Aufgabe für die
  OpenCode-Contributors; Approach C patcht nur lokal für den
  Knowledge-Hub-Nutzer).
- Kein Bild-Upload direkt an ChromaDB (Bild bleibt Query-only).
- Keine Lösung für das OpenCode-Bug-PR-#21633 selbst (das liegt
  außerhalb des Knowledge Hub-Repo).

## Forschungsquellen

- `docs/issues/visual-question-answering/spec.md` — Original VQA-Spec
- `context/root-cause-investigation.md` — Verifikation v1.17.15 + PR-Status
- `mcp_servers/knowledge_hub/tools.py:86` — `search_knowledge`-Signatur
- `mcp_servers/knowledge_hub/server.py:67-182` — Tool-Registrierung
- `scripts/hybrid_search.py:232` — `image_similarity_search`
- `tests/unit/test_image_similarity.py` — bestehende VQA-Tests
- `.opencode/agents/orchestrator-knowledge.md:158-200` — bestehende
  VQA-Prompt-Sektion
- OpenCode PRs #21633, #30153, #32680, #22218 (unmerged/abandoned)
- `context/pdf-link-generation-research.md` — PDF-Link-Generierung
  Recherche (osascript-Failure, `open -a` Fragment-Stripping,
  direkter Browser-Binary mit `#page=`, qlmanage,
  Page-Offset-Ambiguität, Beispielpfade für die 5 VQA-Hits)
- `docs/ai/known-issues.md` VRF-001 — `page`-Feld ist 0-basiert
- `docs/ai/known-issues.md` LIM-004 — `page_start`/`page_end` ±2-Toleranz
- `domains/davinci_resolve/sources/raw/` — 10 Quell-PDFs (Mapping-Tabelle
  in `context/pdf-link-generation-research.md`)
