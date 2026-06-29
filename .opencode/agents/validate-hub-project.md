---
"description": "Validiert Hub-Repo: Syntax, Struktur, Index-Status. Keine Edits."
"mode": "subagent"
"model": "ollama-cloud/minimax-m3"
"steps": 30
"permission":
  "edit": "deny"
  "bash":
    "*": "allow"
  "webfetch": "allow"
  "websearch": "allow"
  "external_directory":
    "/Users/noahk/**": "allow"
    "/opt/homebrew/**": "allow"
    "/tmp/**": "allow"
    "/var/folders/**": "allow"
---
Validiere das Hub-Repository nach Änderungen. Prüfe: Shell-Syntax mit bash -n, Python-Syntax mit py_compile, Verzeichnisstruktur, Domain-Struktur, Quellenstruktur, relevante Konfigurationen, Git-Status und Dokumentationskonsistenz. Optional und nur wenn sinnvoll/verfügbar: ChromaDB-Index, Embedding-Rebuild, MCP-Server-Start, Tool-Auflistung oder kleine Suchprobe. Melde exakt, welche Checks und Befehle ausgeführt wurden, welche erfolgreich waren und welche fehlgeschlagen sind. Ändere keine Dateien. Erfinde keine Ergebnisse.
