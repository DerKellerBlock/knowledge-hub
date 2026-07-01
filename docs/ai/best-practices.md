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

## Umgebungsvariablen

- `KH_RERANKER_MODEL` — Überschreibt das Cross-Encoder-Modell für Stage-2-Reranking.
  Default: `cross-encoder/ms-marco-MiniLM-L-12-v2`.
  Alternative: `jinaai/jina-reranker-v2-base-multilingual` (multilingual, 1024 Token Kontext, CC-BY-NC-4.0).
  Wird in `mcp_servers/knowledge_hub/config.py` ausgewertet. `trust_remote_code=True` in `model_manager.py` aktiviert Custom-Code-Ladung für jina-Modelle.
- `KH_EMBEDDING_MODEL` — Überschreibt das Embedding-Modell (Phase 2a, Decision 2.2).
  Default: `all-mpnet-base-v2` (768 dims, English-only, ~420 MB).
  Alternative: `BAAI/bge-m3` (1024 dims, multilingual, 8192 Token Kontext, MIT, ~2.2 GB Download).
  Wird LIVE in `model_manager.get_embedder()` auf jedem Cache-Miss gelesen.
  Precedence (Decision 2.7): Env-Var > `domain.md` (`## Metadaten → Embedding-Model`) > `config.DEFAULT_MODEL_NAME`.
  Hinweis: Gleichzeitiges Laden beider Modelle kostet ~2.6 GB RAM (`_model_cache` ist aktuell plain dict ohne LRU — LRU-Migration in Phase 2b, B4).
- `KNOWLEDGE_HUB_DOMAINS` — Komma-separierte Domain-Liste für MCP-Server-Scoping.
  Wird in `mcp_servers/knowledge_hub/server.py` ausgewertet.

## Sicherheit

- Keine Secrets in Config-Dateien
- API-Keys nur via Environment-Variablen oder `.env` (gitignored)
- Keine harten `/Users/noahk/`-Pfade (außer in dieser Doku und opencode.json)
- Shell-Skripte prüfen Inputs (z.B. Domain-Namen validieren)
- **Pickle-Sicherheit:** `rank_bm25` serialisiert/deserialisiert BM25-Indizes via Python `pickle`. Für den persönlichen Hub akzeptabel (alle Dateien unter eigener Kontrolle, kein externer Input). Produktion/Shared-Hub wäre problematisch — dann auf JSON oder safetensors migrieren.
