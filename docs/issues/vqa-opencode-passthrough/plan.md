# Plan: VQA OpenCode-Passthrough (Drag-Drop / Clipboard / @-Mention)

**Task-ID:** vqa-opencode-passthrough
**Datum:** 2026-07-07
**Spec:** docs/issues/vqa-opencode-passthrough/spec.md

Die drei Approaches sind **unabhängig** — der Nutzer kann einen,
zwei oder alle drei umsetzen. Empfohlene Start-Reihenfolge: A → B → C
(A sofort verfügbar, B robust für Mac, C langfristig generisch).

## Tasks

### Task A1: Approach A — Orchestrator-Prompt `@`-Mention-Passthrough

- Datei: `.opencode/agents/orchestrator-knowledge.md` (206 Zeilen,
  VQA-Sektion bei Line 158).
- Erweitere die Sektion `### Visual Question Answering` um eine
  Subsektion **`@`-Mention-Passthrough (Workaround für OpenCode
  v1.17.15)** mit folgenden Instruktionen:
  1. Regex-Beispiel: `@(/[^)\s]+\.(?:png|jpg|jpeg|webp))` (case-
     insensitive).
  2. Extrahiere den absoluten Pfad (ohne `@`), validiere Start mit `/`.
  3. Rufe `search_knowledge(domain="davinci_resolve", query="<frage
     als text>", image_path="<pfad>", mode="hybrid", max_results=10)`.
  4. Bei mehreren `@`-Mentions: erstes Bild verwenden, oder Nutzer
     bestätigen lassen.
  5. Fallback-Hinweis: falls nur `data:`-URL sichtbar (Drag-Drop ohne
     `@`), Nutzer informieren, dass Drag-Drop in v1.17.15 nicht
     automatisch weitergereicht wird, und `@/pfad.png` vorschlagen.
- Keine Code-Änderung — reine Prompt-Instruktion.
- **Verify:** `grep -n "@-Mention-Passthrough" .opencode/agents/
  orchestrator-knowledge.md` liefert Treffer; Prompt-Datei bleibt
  gültiges Markdown.

### Task A2: Approach A — Integration-Test für Prompt-Verhalten

- Datei: `tests/mcp/test_orchestrator_image_passthrough.py` (neu).
- Test-Strategie: **kein echter LLM-Call** — der Test parst die
  Prompt-Datei und verifiziert, dass die Instruktion
  `image_path=<extrahierter pfad>` im Prompt-Text steht. Dann testet
  der Test die **Extraktionslogik** an synthetischen User-Message-
  Strings (Python-Regex analog zur Prompt-Instruktion) und
  verifiziert, dass `@/Users/noahk/Desktop/shot.png` →
  `/Users/noahk/Desktop/shot.png` extrahiert wird.
- Test-Fälle:
  - `test_prompt_contains_at_mention_instruction` — liest
    `.opencode/agents/orchestrator-knowledge.md` und assert, dass
    `image_path` und `@`-Mention-Detection erwähnt werden.
  - `test_extract_image_path_from_at_mention_png` — synthetische
    Message `"... @/tmp/shot.png ..."` → extrahiert `/tmp/shot.png`.
  - `test_extract_image_path_rejects_relative_path` —
    `@relative/shot.png` → kein Treffer (muss absolut sein).
  - `test_extract_image_path_multiple_mentions_picks_first` —
    zwei `@`-Mentions → erster Pfad.
  - `test_extract_image_path_rejects_non_image_extension` —
    `@/tmp/notes.txt` → kein Treffer.
- Marker: `@pytest.mark.mcp` (Prompt-Datei ist MCP-Server-Kontext)
  oder `@pytest.mark.unit` (reine String-Extraktion) — siehe Plan
  Validierung.
- **Verify:** `pytest -m mcp tests/mcp/test_orchestrator_image_passthrough.py -q`
  → grün.

### Task B1: Approach B — `get_recent_image_path()` in `tools.py`

- Datei: `mcp_servers/knowledge_hub/tools.py` (285 Zeilen).
- Neue Funktion `get_recent_image_path(max_age_minutes=5,
  scan_dirs=None, include_clipboard=True) -> dict` am Ende der Datei.
- Default `scan_dirs = ["~/Desktop", "~/Downloads",
  "~/Pictures/Screenshots"]`, via `os.path.expanduser` expandiert.
- Filesystem-Scan: `os.walk` pro Dir, sammle Dateien mit Endung
  `.png|.jpg|.jpeg|.webp` und `mtime` innerhalb
  `max_age_minutes`. Sortiere nach `mtime` absteigend, returniere
  jüngste.
- Clipboard (`include_clipboard=True`): `subprocess.run(["osascript",
  "-e", 'get the clipboard as «class furl»'])` → parse
  `«class furl»:<hex>` → POSIX-Pfad via `struct.unpack` oder
  alternativ `osascript -e 'get the clipboard as POSIX file as text'`
  (verifiziere welche Form in v1.17.15/macOS-Current zuverlässig
  funktioniert — der Test nutzt einen Mock).
- **Security-Validierung (zwingend):**
  - `os.path.realpath(path)` für jeden Treffer, dann Prefix-Check
    gegen `realpath(scan_dir)`. Rejiziere, falls Treffer nicht mit
    `realpath(scan_dir) + os.sep` beginnt.
  - `os.path.islink(path)`-Check: falls Symlink, folge ihm nur, wenn
    das Target unter `scan_dir` liegt (sonst reject — Symlink-Escape).
  - Explizit rejiziere Pfade mit `..`-Komponenten (vor realpath-Check
    als erste Verteidigungslinie).
- Return-Dict: `{"image_path": str | None, "source": str, "mtime":
  str | None}`. `source` ∈ `{"desktop", "downloads", "screenshots",
  "clipboard"}`.
- Graceful fallback: bei `OSError`/`subprocess.SubprocessError` →
  `image_path=None` (kein Crash, log warning).
- **Verify:** `python -c "from mcp_servers.knowledge_hub.tools import
  get_recent_image_path; print(get_recent_image_path(max_age_minutes=1))"
  ` läuft ohne Crash (liefert Dict, `image_path` kann None sein).

### Task B2: Approach B — MCP-Tool-Registrierung in `server.py`

- Datei: `mcp_servers/knowledge_hub/server.py` (203 Zeilen).
- Import `get_recent_image_path` in Line ~38 (zusammen mit den
  anderen Tool-Funktionen).
- Neues `Tool(...)`-Entry in `list_tools_handler` (Lines 67–142),
  positioniert nach `search_knowledge`:
  ```json
  {
    "name": "get_recent_image_path",
    "description": "Finde den jüngsten Bild-Pfad (Desktop/Downloads/Pictures/Screenshots/Clipboard) für VQA-Passthrough. Mac-spezifisch. Gibt {image_path, source, mtime} zurück.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "max_age_minutes": {"type": "integer", "default": 5,
          "description": "Maximales Alter der Datei in Minuten"},
        "include_clipboard": {"type": "boolean", "default": true,
          "description": "macOS-Clipboard via osascript prüfen"}
      }
    }
  }
  ```
- `elif name == "get_recent_image_path":` Branch in
  `call_tool_handler` (Lines 145–182), extrahiere Argumente mit
  `.get("max_age_minutes", 5)` und `.get("include_clipboard", True)`,
  rufe Funktion, returniere JSON.
- **Verify:** `python -c "from mcp_servers.knowledge_hub.server import
  list_tools_handler"` startet ohne Fehler; MCP-Server-Quicktest
  (siehe `docs/ai/validation.md`) zeigt das neue Tool.

### Task B3: Approach B — Unit-Tests für `get_recent_image_path`

- Datei: `tests/unit/test_get_recent_image_path.py` (neu).
- Marker: `@pytest.mark.unit`.
- Test-Fälle (mit `tmp_path`-Fixture und mocked `os.walk`/`osascript`):
  - `test_finds_youngest_image_in_scan_dir` — drei PNGs mit
    unterschiedlicher mtime → jüngster wird zurückgegeben.
  - `test_returns_none_for_empty_dir` — leeres `scan_dir` →
    `image_path=None`.
  - `test_returns_none_when_all_older_than_max_age` — Datei mit
    mtime > `max_age_minutes` → None.
  - `test_filters_non_image_extensions` — `.txt`-Datei wird ignoriert.
  - `test_clipboard_returns_path_when_image_present` —
    `subprocess.run` mocken, liefert `«class furl»:<hex>`,
    `image_path` gesetzt, `source="clipboard"`.
  - `test_clipboard_returns_none_when_no_image` — Mock liefert
    leeres/Text-Clipboard → `image_path=None`.
  - `test_path_traversal_rejected` — synthetischer Treffer-Pfad
    `/etc/passwd` (nicht unter scan_dir) → reject,
    `image_path=None`.
  - `test_symlink_escape_rejected` — Symlink in scan_dir zeigt auf
    `/etc/passwd` → reject.
  - `test_oserror_graceful_fallback` — `os.walk` raise `OSError` →
    `image_path=None`, kein Crash.
  - `test_default_scan_dirs_expand_home` — `~/Desktop` wird zu
    `/Users/<user>/Desktop` expandiert (mock `os.path.expanduser`).
- **Verify:** `pytest -m unit tests/unit/test_get_recent_image_path.py -q`
  → grün.

### Task B4: Approach B — MCP-Contract-Test

- Datei: `tests/mcp/test_get_recent_image_path.py` (neu).
- Marker: `@pytest.mark.mcp`.
- Test-Fälle:
  - `test_tool_registered_in_list_tools` — `list_tools_handler()`
    enthält Tool mit `name="get_recent_image_path"`.
  - `test_call_tool_handler_dispatches_to_function` — mock
    `tools.get_recent_image_path`, rufe `call_tool_handler` mit
    `name="get_recent_image_path"`, args `{"max_age_minutes": 1}`,
    verifiziere Mock wurde mit richtigen Argumenten aufgerufen.
  - `test_tool_returns_json_serializable` — return-Wert ist
    JSON-serialisierbar (MCP-Transport).
- **Verify:** `pytest -m mcp tests/mcp/test_get_recent_image_path.py -q`
  → grün.

### Task B5: Approach B — Orchestrator-Prompt proaktiver Aufruf

- Datei: `.opencode/agents/orchestrator-knowledge.md`.
- Erweitere VQA-Sektion um: „Falls der Nutzer eine Bild-Frage stellt
  OHNE `@`-Mention und OHNE sichtbaren Pfad, rufe proaktiv
  `get_recent_image_path(max_age_minutes=5, include_clipboard=True)`
  auf, um den Pfad des jüngsten Screenshots zu finden. Verwende das
  Resultat als `image_path` für `search_knowledge`."
- **Verify:** `grep -n "get_recent_image_path" .opencode/agents/
  orchestrator-knowledge.md` liefert Treffer.

### Task C1: Approach C — Research-Spike OpenCode-Plugin-API

- Datei: `docs/issues/vqa-opencode-passthrough/context/
  opencode-plugin-api-research.md` (neu, im context/-Ordner).
- Aufgabe: klone/lade OpenCode-Source, lese `packages/opencode/src/
  plugin/` und `packages/plugin/` (falls vorhanden). Dokumentiere:
  1. OpenCode-Version im Clone (sicherstellen, dass es v1.17.15 oder
     kompatibel ist).
  2. Liste aller Hook-Typen (z.B. `chat.message`, `chat.part`,
     `tool.pre`, ...).
  3. Für jeden Hook: Signatur, kann er Message-Parts **vor** dem
     LLM-Call modifizieren? (pre-LLM).
  4. Plugin-Loader-Mechanismus: Config-Eintrag in `opencode.json`?
     `~/.config/opencode/plugins/`? npm-Package?
  5. TypeScript-Typdefinitionen für die Plugin-API.
- Falls kein `chat.message` pre-LLM Hook existiert: dokumentiere
  Approach C als `blocked`, verweise auf OpenCode PR #21633.
- **Verify:** Datei existiert, dokumentiert klar ob API existiert
  (ja/nein) mit Zitat der relevanten Source-Datei.

### Task C2: Approach C — Plugin implementieren (falls API existiert)

- NUR auszuführen, falls Task C1 bestätigt, dass ein `chat.message`
  pre-LLM Hook existiert.
- Datei: `plugins/knowledge-hub-image-passthrough/` (neuer Ordner im
  Repo) oder `.agents/skills/knowledge-hub-image-passthrough/SKILL.md`
  (Skill-Distribution).
- Plugin-Hook: bei `chat.message` pre-LLM:
  1. Finde alle `data:image/...;base64,...` Parts in der Message.
  2. Dekodiere PNG-Bytes → schreibe nach
     `/tmp/knowledge-hub-attachments/<sessionID>/<timestamp>.png`.
  3. Injiziere synthetischen Text-Part `[attachment: /tmp/.../<ts>.png]`
     **vor** dem Bild-Part.
  4. Optional: ersetze `data:`-Part durch `file://`-Referenz (falls
     Modell `file://` unterstützt — sonst Text-Part als Fallback).
- Smoke-Test: manuelles Drag-Drop im OpenCode-TUI → verifiziere, dass
  `/tmp/knowledge-hub-attachments/.../*.png` existiert und der
  Orchestrator-Prompt den Pfad sieht.
- **Verify:** `/tmp/knowledge-hub-attachments/<sessionID>/` enthält
  PNG-Datei mit mtime ≤ 30s; Orchestrator-Log zeigt
  `image_path=/tmp/...`.

### Task D1: Doku + open-work.md + Retrospektive

- Datei: `docs/ai/open-work.md` — Status des Tasks auf `done` setzen,
  sobald mindestens ein Approach abgeschlossen ist (A reicht für
  `done` mit Vermerk, dass B/C optional folgen).
- Datei: `docs/issues/vqa-opencode-passthrough/retrospective.md`
  (bei Abschluss) — Was gebaut wurde, was gut/lief nicht gut,
  Erkenntnisse.
- Datei: `docs/issues/vqa-opencode-passthrough/explanation.md`
  (bei Abschluss) — Anfängerfreundliche Erklärung der genutzten
  Approach(es).
- Datei: `docs/ai/known-issues.md` — falls Approach A umgesetzt wird,
  neuen Eintrag unter „Bekannte Retrieval-Lücken" oder
 „Einschränkungen", dass Drag-Drop ohne `@`-Mention in v1.17.15 nicht
  weitergereicht wird (und Approach B/C als Lösung).
- **Verify:** `./scripts/workspace_check.sh` OK; open-work.md hat
  konsistenten Eintrag.

## Reihenfolge

```
Approach A (unabhängig):
  Task A1 (Prompt) ── Task A2 (Test) ──┐
                                       └── Task D1 (Doku)

Approach B (unabhängig, parallel zu A möglich):
  Task B1 (tools.py) ──┬── Task B2 (server.py)
                       │                     │
                       └── Task B3 (unit)     └── Task B4 (mcp)
                                               │
                                               └── Task B5 (Prompt)
                                                     │
                                                     └── Task D1 (Doku)

Approach C (blockiert bis C1 Research):
  Task C1 (Research-Spike) ─┬── [API existiert] ── Task C2 (Plugin) ── Task D1
                             │
                             └── [API fehlt] ── blocked, dokumentiert, D1
```

Die drei Approaches sind unabhängig — der Nutzer kann A sofort
umsetzen, B nachreichen, C erforschen.

## Validierung

```bash
# Syntax
.venv/bin/python -m py_compile scripts/*.py mcp_servers/knowledge_hub/*.py
find . -name "*.sh" -exec bash -n {} \;

# Unit-Tests
.venv/bin/pytest -m unit -q

# MCP-Contract-Tests
.venv/bin/pytest -m mcp -q

# Structure
./scripts/workspace_check.sh
./scripts/workspace_status.sh

# Manueller Smoke-Test Approach A (nach Task A1):
# Im OpenCode-TUI: "was ist das rechts unten? @/Users/noahk/Desktop/shot.png"
# → Orchestrator sollte search_knowledge mit image_path aufrufen.

# Manueller Smoke-Test Approach B (nach Task B5):
# Screenshot auf Desktop ziehen → in OpenCode: "was ist das in der UI?"
# → Orchestrator sollte get_recent_image_path() aufrufen, dann search_knowledge.

# Manueller Smoke-Test Approach C (nach Task C2):
# Bild in OpenCode drag-droppen → /tmp/knowledge-hub-attachments/... prüfen
# → Orchestrator sollte image_path im Prompt sehen.
```

## Risiko

- **Approach A — Niedrig:** reine Prompt-Instruktion, kein Code-
  Änderung am Knowledge Hub. Risiko: LLM folgt der Instruktion nicht
  zuverlässig (LLM-Adhäsion) — mitigierbar durch klare Regex-Beispiele
  und Fallback-Hinweis. Test A2 prüft nur die Prompt-Datei, nicht das
  LLM-Verhalten (echte LLM-Adhäsion ist manueller Smoke-Test).
- **Approach B — Mittel:** macOS-spezifisch (`osascript`). Risiko:
  osascript-Syntax variiert zwischen macOS-Versionen (verifiziere in
  Unit-Test mit Mock). Security-Risiko via Path-Traversal/Symlink-
  Escape → mitigierbar durch realpath+prefix-check (Unit-Tests B3).
  Risiko: `os.walk` ist langsam auf großen Dirs → `max_age_minutes`
  begrenzt die Treffer-Menge, aber der Walk selbst scannt alle Files;
  ggf. `find` als Performance-Optimierung falls `os.walk` zu langsam
  (separater Folgetask).
- **Approach C — Hoch:** OpenCode-Plugin-API in v1.17.15 nicht
  formal für `chat.message` pre-LLM dokumentiert. Wahrscheinlich
  `blocked` bis PR #21633 merged. Plugin-API kann sich ändern (nicht
  stabil). Risiko: Plugin bricht bei OpenCode-Update. Vertrieb als
  Skill erhöht Wartbarkeit, aber nicht Stabilität.
- **Übergreifend — Niedrig:** alle Ansätze sind additiv; keine
  Änderung an `search_knowledge`/`image_similarity_search`. Bestehende
  VQA-Tests (`tests/unit/test_image_similarity.py`) bleiben unberührt.
- **Backward-Kompatibilität:** Approach A verändert nur den Prompt;
  ohne `@`-Mention bleibt Verhalten unverändert. Approach B fügt ein
  neues Tool hinzu, ohne bestehende Tools zu ändern. Approach C
  patcht OpenCode lokal, ohne Knowledge-Hub-Code zu ändern.

## Aufwandsschätzung

| Approach | Aufwand | Verlässlichkeit | macOS-spezifisch? |
|----------|---------|-----------------|-------------------|
| A | ~1-2h | mittel (LLM-Adhäsion) | nein |
| B | ~3-4h | hoch (deterministisch) | ja (osascript) |
| C | ~1-2 Tage (falls API existiert) | unklar (Plugin-API instabil) | nein |

**Empfehlung:** A zuerst (sofort verfügbar, low risk), dann B (löst
den täglichen Mac-Screenshot-Workflow robust). C nur als
langfristige Forschung, falls PR #21633 nicht in absehbarer Zeit
mergt.
