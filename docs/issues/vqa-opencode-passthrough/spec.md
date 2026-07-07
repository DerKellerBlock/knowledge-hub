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
