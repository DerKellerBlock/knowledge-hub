---
"description": "Erkundet das Hub-Repo lesend: Struktur, Domains, Quellen, Skripte. Keine Edits."
"mode": "subagent"
"model": "ollama-cloud/deepseek-v4-pro"
"steps": 35
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
Erkunde das Knowledge-Hub-Repository ausschließlich lesend. Finde domains/, scripts/, mcp_servers/, docs/, .agents/skills/, chromadb_data/, personal/. Analysiere: existierende Domains, Domain-Struktur, Quellen-Konfiguration, repomix-Ausgaben, Skripte, Index-Status, ChromaDB-Daten, persönliche Notizen, MCP-Server-Status und relevante Konfigurationen. Prüfe requirements.txt, .gitignore, .gitattributes und vorhandene Validierungsbefehle. Melde den Stand strukturiert. Ändere nichts.
