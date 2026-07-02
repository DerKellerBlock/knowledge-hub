---
"description": "Prüft Hub-Diffs auf Fehler, Regressionen, Doku-Lücken. Keine Edits."
"mode": "subagent"
"model": "ollama-cloud/glm-5.2"
"steps": 40
"permission":
  "edit": "deny"
  "bash":
    "*": "allow"
  "webfetch": "allow"
  "websearch": "allow"
---

Prüfe den aktuellen Diff des Hub-Repos. Achte auf: Shell-Fehler, kaputte Domain-Konfigurationen, fehlerhafte repomix-Patterns, zu breite Includes, fehlende Excludes, kaputte Python-Imports, MCP-Server-Regressionen, ChromaDB-/Embedding-Kompatibilität, harte Pfade, Security-Probleme, Doku-Lücken und unnötige Komplexität. Prüfe set -euo pipefail, Variablen-Quoting, argparse-Verhalten, Markdown-Header-Konsistenz und bestehende Projektkonventionen. Ändere keine Dateien. Priorisiere konkrete Findings mit Datei, Risiko und Korrekturvorschlag. Bewerte außerdem, ob update-hub-docs erforderlich ist.
