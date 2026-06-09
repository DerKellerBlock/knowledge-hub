# Best Practices — Knowledge Hub

## Shell-Skripte

- Jedes Skript beginnt mit `#!/usr/bin/env bash` und `set -euo pipefail`
- Farben via ANSI-Escape-Codes: `GREEN`, `YELLOW`, `RED`, `CYAN`, `BOLD`, `NC`
- Hilfsfunktionen: `log_info()`, `log_warn()`, `log_error()`
- Hilfe via `show_help()` oder `--help`/`-h` Flag
- Pfade relativ zum Repository-Root: `REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"`
- Variablen in Strings immer mit `"${VAR}"` quoten (nicht nackt)
- Arrays mit `"${ARR[@]}"` expandieren
- Kein `eval`, kein `curl | bash`, keine ungeprüften externen Inputs in Shell-Commands

## Python-Skripte

- Python 3.11+
- `argparse` (CLI) oder `click` (komplexere CLIs)
- Docstrings für jedes Modul und jede Funktion
- Type-Hints wo sinnvoll (`def embed(texts: list[str]) -> np.ndarray:`)
- ChromaDB-Client als Singleton (nicht pro Request neu instanziieren)
- Embedding-Model einmal laden, dann wiederverwenden
- Fehler via Exceptions, nicht via Print+Exit
- `if __name__ == "__main__":` Guard

## Markdown-Dokumentation

- `##`-Header für Sektionen, `###` für Sub-Sektionen
- Tabellen für strukturierte Daten (Quellen, Metadaten, Zustände)
- Code-Blöcke mit Sprachangabe (\`\`\`bash, \`\`\`python, \`\`\`markdown)
- Links auf andere Docs/Dateien
- Status-Indikatoren: ✅ (erledigt), ⚠️ (Warnung), ❌ (Fehler/fehlt)

## Versionierung

- ChromaDB-Index ist `.gitignored`
- Packed-Files via Git LFS (`.gitattributes`)
- `requirements.txt` mit version-pinned Dependencies
- Semver-ähnliche Tags für Releases (später)

## Sicherheit

- Keine Secrets in Config-Dateien
- API-Keys nur via Environment-Variablen oder `.env` (gitignored)
- Keine harten `/Users/noahk/`-Pfade (außer in dieser Doku und opencode.json)
- Shell-Skripte prüfen Inputs (z.B. Domain-Namen validieren)
