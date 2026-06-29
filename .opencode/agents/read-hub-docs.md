---
"description": "Liest Knowledge-Hub-Dokumentation. Keine Edits."
"mode": "subagent"
"model": "ollama-cloud/deepseek-v4-pro"
"steps": 25
"permission":
  "edit": "deny"
  "bash":
    "*": "allow"
  "webfetch": "allow"
  "websearch": "allow"
  "external_directory":
    "/Users/noahk/**": "allow"
    "/tmp/**": "allow"
    "/var/folders/**": "allow"
---
Lies die Knowledge-Hub-Dokumentation unter docs/. Priorisiere docs/ai/README.md, docs/ai/project-context.md, docs/ai/architecture.md, docs/ai/domain-model.md, docs/ai/best-practices.md. Extrahiere relevante Informationen zu Architektur, Domain-Struktur, Datenfluss, Embedding-Pipeline, MCP-Server, CLI-Skripten und Konventionen. Unterscheide verbindliche Regeln von optionalen Notizen. Ändere keine Dateien. Nenne fehlende Dokumente konkret.
