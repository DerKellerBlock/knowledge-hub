# Security — Knowledge Hub

## Baseline

- No secrets, API keys or tokens in tracked files.
- Use environment variables for credentials.
- Do not index private data accidentally through `domains/*/sources/` or `personal/`.
- Treat external source ingestion as untrusted until reviewed.
- Avoid unsafe shell patterns and always quote paths.
- MCP server is stdio-oriented for local OpenCode use; do not expose it publicly without a separate security plan.

## Dependency and License Checks

- Review `requirements.txt`, `requirements-dev.txt`, `requirements-pdf.txt` and `THIRD_PARTY_LICENSES.md` when dependencies change.
- Keep the PyMuPDF4LLM AGPL process-boundary decision documented in `docs/decisions/2026-06-27-agpl-process-boundary.md`.

## Known Accepted Risk

BM25 indexes use Python pickle through `rank_bm25` serialization. This is accepted for Noahs personal local Hub where index files are generated locally and not consumed from untrusted sources. A shared or production Hub would need a safer serialization format.

`trust_remote_code=True` in `scripts/model_manager.py:get_reranker()` allows HuggingFace models to execute arbitrary Python code shipped in their repository (via `auto_map` in `config.json`). This is required for `jinaai/jina-reranker-v2-base-multilingual`, which ships custom code for its `JinaReranker` class. The legacy `cross-encoder/ms-marco-MiniLM-L-12-v2` has no `auto_map` and ignores the flag. Accepted for the personal Hub: the model comes from a known vendor (Jina AI), there is no multi-tenant access, and no untrusted external input feeds the reranker. For a production or shared Hub: pin the model to a known commit hash or audit the custom code before enabling `trust_remote_code`.

## Local LLM (Phase 3.1)

Contextual Retrieval nutzt ein lokales LLM (Gemma 4 12B MLX via Ollama) für Kontext-Generierung.
- **Keine Datenexfiltration:** LLM läuft on-device (Ollama + MLX/Metal), kein API-Key, kein externer Netzwerk-Call. Ollama hört auf localhost:11434.
- **Modell-Download:** Gemma 4 12B (~7.7 GB MLX-quantisiert) via `ollama pull gemma4:12b-mlx`. Apache 2.0 Lizenz. Zusätzlich können Google's Gemma Terms of Use gelten — dokumentiert in `THIRD_PARTY_LICENSES.md` (Sektion 'Apache-2.0 Licensed Model Weights').
- **Kein `trust_remote_code`:** Ollama lädt Modelle ohne HuggingFace-Custom-Code. Sicherer als jina-reranker (das `trust_remote_code=True` benötigt).
- **Ollama-Service:** Muss als System-Service laufen (`brew services start ollama`). localhost:11434 sollte nicht nach außen exponiert sein (macOS Firewall default blockt eingehende Verbindungen).
- **Loopback-Pinning (Phase 3.1a Security-Hardening):** `get_llm()` erzeugt `ollama.Client(host="http://localhost:11434")` per Default, um versehentliche Exfiltration lokaler Repo-/Personal-Notes-Inhalte an einen Remote-Ollama-Server zu verhindern. Die implizite `OLLAMA_HOST`-Default des ollama-Python-Clients wird absichtlich NICHT honoring. Ein non-loopback Host wird NUR akzeptiert bei explizitem `KH_OLLAMA_HOST`-Opt-in (siehe `best-practices.md`); dabei wird eine WARNING geloggt. Der LLM-Cache-Key ist `llm:<backend>:<model_name>` (inkl. Backend, verhindert stale cross-backend Reuse).
- **Ram-Budget:** BGE-M3 (~2.2 GB CPU) + Gemma 4 12B MLX (~7.7 GB Metal) + ChromaDB + BM25 = ~10.5 GB. Passt auf 16 GB Mac (knapp), sicher auf 32 GB.
- **Kein transformers-Konflikt:** Ollama Python package ist nur ein HTTP-Client (~10 MB), pulled keine transformers/PyTorch. BGE-M3/jina-Stack unbeeinflusst.

## Akzeptierte Risiken (Phase 3.1a)

- **Prompt-Injection durch Chunk-Texte (MEDIUM):** `generate_context()` interpoliert `document_text` und `chunk_text` in den LLM-Prompt. Diese stammen aus `domains/*/sources/` und `domains/*/personal/` (Noahs trusted Content). Ein adversarialer Chunk könnte Instruktionen injectieren, die zu falschen `context_prefix`-Texten führen. Akzeptiert für den persönlichen Hub: keine Tool-/Code-Ausführung über das LLM, Impact begrenzt auf persistierte Retrieval-Manipulation. **Phase 3.1b Mitigation (M2):** Output-Validation `_validate_context()` implementiert (Länge 10–500 Zeichen, mehrzeilige Instruktionssprache-Regex, Injektions-Präfix `ignore`/`forget`/`system:`/`assistant:`). Verbleib-Risiko: keine perfekte Heuristik, persönlicher Hub mit trusted Sources.
- **Unbounded Prompt-Input (MEDIUM):** `generate_context()` begrenzt `document_text`/`chunk_text` nicht. Zusammen mit `num_predict=800` und `keep_alive="24h"` können sehr große/adversariale Dokumente lange Läufe oder RAM-Druck verursachen. **Phase 3.1b Mitigation (M3):** Token-Limits `_truncate()` implementiert (document 50K Zeichen, chunk 30K Zeichen). Warnung via `RuntimeWarning` bei Truncation.
- **Ollama-Crash-Retry (Phase 3.1b):** Exponentielles Backoff (30/60/120s, 3 Versuche) bei transienten Ollama-Connection-Errors via `_RetryClientProxy`. Nach 3 Fehlern → `RuntimeError`, Cache behält alle bereits geschriebenen Einträge für Resume.
- **`llama-cpp`-Backend (LOW):** `KH_LLM_BACKEND=llama-cpp` nutzt `KH_LLM_MODEL` direkt als `model_path` ohne Pfad-Validierung. Default ist `ollama`; `llama-cpp` ist experimenteller Cross-Platform-Fallback ohne Unit-Test. Akzeptiert: kein produktiver Einsatz geplant.

## Cloud-LLM (Phase 3.1c)

Contextual Retrieval kann via Ollama-Cloud (`gemma4:cloud`) statt lokalem Gemma 4 12B MLX laufen.
- **Datenexfiltration:** Chunk-Texte + Quelldokumente (Godot-Docs + Personal Notes) werden an Ollama-Cloud gesendet. KH_OLLAMA_HOST non-loopback Opt-in (3.1a Loopback-Pinning greift nicht bei Cloud — bewusst via Env-Var deaktiviert).
- **Zero-Retention-Policy:** Ollama-Cloud speichert/trained nicht auf Prompts/Outputs (ollama.com/privacy). Akzeptabel für trusted Sources (öffentliche Godot-Docs + technische Personal Notes). Nicht akzeptabel für sensitive Personal Notes — für diese wäre lokales Gemma fallback.
- **Usage-Limit-Handling:** HTTP 429 → sofortiger Stopp (kein Backoff-Verschwendung), Cache-Resume nach Account-Wechsel oder Limit-Reset.
- **Transienter Cloud-Ausfall:** HTTP 502 → 3× Backoff (30/60/120s), dann RuntimeError — Resume via Cache (kein Datenverlust, Cache wächst monoton).

## Review Commands

```bash
git status --short
python3 -m json.tool .opencode/opencode.json
find . -name "*.py" -not -path "*/__pycache__/*" -exec python3 -m py_compile {} \;
find . -name "*.sh" -exec bash -n {} \;
```

For changes touching `model_manager.py:get_reranker()` or any model loaded with `trust_remote_code=True`, additionally review the upstream model repository and confirm the commit hash matches the documented trusted source. `gitleaks`/`semgrep` are optional but recommended for security-sensitive changes.