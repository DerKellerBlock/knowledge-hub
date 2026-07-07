# Root-Cause Investigation: OpenCode Image Path Loss

**Datum:** 2026-07-07
**Zweck:** Verifizierte Befunde, warum `search_knowledge(image_path=...)`
heute nicht über Drag-Drop / Clipboard-Paste in OpenCode v1.17.15
ausgelöst werden kann. Kopie der Recherchenotes, damit der Task
self-contained ist (die URLs sind verifizierte OpenCode-Repo-Quellen,
keine erfundenen Fakten).

## Ausgangslage

Das VQA-Feature (`docs/issues/visual-question-answering/spec.md`) setzt
voraus, dass der OpenCode-Orchestrator den absoluten Pfad eines
hochgeladenen Bildes an `search_knowledge(image_path=...)` weitergibt.
Die spec nennt beispielhaft `/tmp/opencode/uploads/img-xyz.png` als
Pfad, den OpenCode „liefert". Die Verifikation in v1.17.15 zeigt:
**diese Annahme ist falsch** — OpenCode kodiert Drag-Drop-Bilder als
`data:image/png;base64,...` in der User-Message und verliert den
ursprünglichen Datei-Pfad, bevor die Nachricht den Orchestrator-Agent
erreicht.

## Verifizierte Befunde

### B1: OpenCode v1.17.15 kodiert Drag-Drop als base64

- Drag-Drop eines Bildes in den OpenCode-TUI erzeugt ein
  `data:image/png;base64,...` Part in der User-Message.
- Der ursprüngliche macOS-Datei-Pfad geht verloren, bevor die Nachricht
  an den Orchestrator-Agent weitergereicht wird.
- `Image.normalize()` in OpenCode akzeptiert ausschließlich
  `data:...;base64,...` URLs und gibt dieselbe Form zurück — es erzeugt
  **nie** Datei-Pfade.

### B2: Die relevanten OpenCode-PRs sind NICHT gemerged

Stand 2026-07-07 sind folgende PRs im OpenCode-Repo geprüft (alle
unmerged oder abandoned):

| PR | Status | Bezeichnung |
|----|--------|-------------|
| #21633 | open seit Apr 2026 | fix(tui): save clipboard-pasted images to temp files for MCP tool access |
| #30153 | closed (abandoned) | feat: save file attachments to disk before model processing |
| #32680 | closed | feat: save unsupported image to temp file for vision MCP tools |
| #22218 | closed | fix: persist clipboard images as temp files with file:// URLs |

PR #21633 würde bei Merge `/tmp/opencode-paste-<timestamp>.png`
erzeugen und wäre der sauberste Fix auf OpenCode-Seite. Bis dahin
bleibt die Drag-Drop-Pfad-Erhaltung beim Knowledge Hub-Consumer
hängen.

### B3: `@/abs/path.png` funktioniert, aber nur via Text-Part

- Ein `@/Users/noahk/.../image.png` Mention in der TUI triggert
  `resolvePromptParts()` und erzeugt ein `file://` URL Part.
- Die Read-Pipeline re-encodiert die Datei jedoch zu `data:` für das
  Modell — der Pfad geht im Modell-Input verloren.
- **Aber:** der Plain-Text der User-Message enthält weiterhin die
  `@/...`-Zeichenkette, die der Orchestrator-Prompt per Regex
  extrahieren kann. Das ist der Hebel für Approach A.

### B4: Knowledge Hub-Seite ist vollständig

- `search_knowledge(domain, query, ..., image_path=None)` in
  `mcp_servers/knowledge_hub/tools.py:86` ist implementiert und
  propagiert `image_path` an `hybrid_search.search()` (line 596).
- `image_similarity_search(domain, image_path, top_k=10)` in
  `scripts/hybrid_search.py:232` ist implementiert (PIL → SigLIP-2 →
  ChromaDB cosine query → `image_match` Treffer).
- Tests in `tests/unit/test_image_similarity.py` decken den Pfad ab:
  `test_search_with_image_path_prepends_image_match`,
  `test_returns_image_match_results_sorted_by_similarity`,
  `test_invalid_image_file_returns_empty_list`,
  `test_collection_missing_returns_empty_list`.
- **Die Lücke liegt ausschließlich auf der OpenCode→MCP-Grenze**, nicht
  im Knowledge Hub selbst.

## Folgerung

Drei unabhängige Lösungsansätze sind möglich (siehe `spec.md`):

- **Approach A (low effort):** `@`-Mention-Passthrough — Orchestrator
  parst `@/abs/path.png` aus der User-Message und reicht den Pfad an
  `search_knowledge(image_path=...)` weiter. Funktioniert heute, ohne
  OpenCode-Änderung, erfordert aber dass der Nutzer den Pfad manuell
  referenziert.
- **Approach B (medium effort):** Neues MCP-Tool
  `get_recent_image_path()` — scannt Desktop / Downloads /
  Pictures/Screenshots / macOS-Clipboard nach dem jüngsten Bild und
  liefert den Pfad an den Orchestrator. Löst den Drag-Drop-Fall, ist
  aber macOS-spezifisch.
- **Approach C (high effort):** Lokales OpenCode-Plugin/Plugin-Loader —
  patcht die Message-Pipeline, sodass Drag-Drop-Bilder nach
  `/tmp/knowledge-hub-attachments/...` gespeichert und der Pfad als
  Text-Part injiziert wird. Löst die Wurzel, erfordert aber eine
  OpenCode-Plugin-API, die in v1.17.15 nicht formal für diesen Use-Case
  existiert — Research-Spike zur Bestätigung nötig.

## Quellen

- OpenCode PR #21633 (open, Apr 2026) — Clipboard-Image-to-Temp-File
- OpenCode PR #30153 (closed/abandoned) — File-Attachments-to-Disk
- OpenCode PR #32680 (closed) — Unsupported-Image-to-Temp-File
- OpenCode PR #22218 (closed) — Clipboard-Images-as-Temp-Files
- Lokale Verifikation v1.17.15: `Image.normalize()` akzeptiert nur
  `data:` URLs
- Knowledge Hub-Code: `mcp_servers/knowledge_hub/tools.py:86`,
  `scripts/hybrid_search.py:232`,
  `tests/unit/test_image_similarity.py`
