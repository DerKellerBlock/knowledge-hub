# jina-Reranker Test — Wo die Dateien leben

> **Anfängerfreundliche Erklärung** | 2026-07-01 | Multilingualer Stage-2-Reranker (LIM-007/LIM-008)

## Übersicht

`jinaai/jina-reranker-v2-base-multilingual` ist als multilingualer Stage-2-Reranker
übernommen. Zusammen mit BGE-M3 (multilingual Embeddings) entsteht eine
konsistente Multilingual-Pipeline, die die DE↔EN-Sprachbarriere (LIM-008) auch im
Reranking schließt: godot-008 — deutsche `faq.md` auf Rang 1 trotz englischer Query.
jina wird BEHALTEN.

## Wo geänderte Dateien leben

| Bereich | Pfad | Was sich geändert hat |
|---------|------|----------------------|
| Doku | `docs/ai/best-practices.md` | `KH_RERANKER_MODEL`-Abschnitt erweitert (jina empfohlen, Setup-Hinweis, Score-Skala) |
| Doku | `docs/ai/security.md` | `trust_remote_code=True`-Risiko dokumentiert |
| Doku | `docs/ai/known-issues.md` | LIM-007, LIM-008 → resolved (KI-006, KI-007); LIM-009 bleibt offen |
| Doku | `docs/ai/changelog.md` | Neue `## 2026-07-01`-Sektion |
| CI | `.github/workflows/quality-gate.yml` | `KH_RERANKER_MODEL=jinaai/jina-reranker-v2-base-multilingual` als Job-Env |
| Baselines | `quality/baselines/godot-latest.json` | Überschrieben mit jina-Ergebnis (0.8594) |
| Baselines | `quality/baselines/davinci_resolve-latest.json` | Überschrieben mit jina-Ergebnis (0.7304) |
| Baselines | `quality/baselines/godot-msmarco-2026-06-30.json` | Neu (Backup der msmarco-Baseline) |
| Baselines | `quality/baselines/davinci_resolve-msmarco-2026-06-30.json` | Neu (Backup der msmarco-Baseline) |
| Baselines | `quality/baselines/README.md` | Hinweis: aktuelle Baselines sind BGE-M3+jina, msmarco archiviert |
| Reports | `quality/reports/godot_jina_2026-07-01.json` | jina-Evaluation (vorhanden, nicht geändert) |
| Reports | `quality/reports/davinci_resolve_jina_2026-07-01.json` | jina-Evaluation (vorhanden, nicht geändert) |
| Code | `scripts/model_manager.py` | **unverändert** — jina wird rein via Env-Var aktiviert |
| Tests | `tests/e2e/test_jina_reranker_integration.py` | Neu — Regressionsschutz für LIM-007 |

## Validierungsbefehle

```bash
# Quality Evaluation mit jina (lokal Env-Var setzen)
export KH_RERANKER_MODEL=jinaai/jina-reranker-v2-base-multilingual
.venv/bin/python scripts/quality/run_evaluation.py --domain godot --baseline quality/baselines/godot-latest.json

# CI Quality Gate (manuell)
gh workflow run quality-gate.yml
```

## Was ist neu

- **`KH_RERANKER_MODEL` CI-Default** — der Quality-Gate-Workflow setzt jina explizit
  als Job-Env. Lokal ohne Env-Var läuft weiterhin ms-marco (Rückwärtskompatibilität).
- **`quality/baselines/` jina** — `*-latest.json` sind jetzt die jina-Ergebnisse vom
  2026-07-01. msmarco-Baselines als `*-msmarco-2026-06-30.json` archiviert.

## Wo das Ergebnis sichtbar ist

- `quality/reports/godot_jina_2026-07-01.json` — godot avg_composite 0.8594,
  godot-008 mit `faq.md` auf Rang 1 (vorher msmarco: faq.md tiefer).
- `quality/reports/davinci_resolve_jina_2026-07-01.json` — davinci avg_composite
  0.7304 (+0.0058), PMA +0.0286 netto vs msmarco.

## Wichtige Hinweise

- **Lokaler Default:** `export KH_RERANKER_MODEL=jinaai/jina-reranker-v2-base-multilingual`
  in `~/.zshrc` oder `.env` setzen, damit lokale `hybrid_search`-Aufrufe jina nutzen.
  Ohne Env-Var fällt das System auf ms-marco zurück.
- **LIM-009 bleibt offen:** BGE-M3 long-context verändert das Chunking-Verhalten
  (Konfounder) — durch jina nicht gelöst.
- **Phase 2b offen:** Late Chunking, Golden Dataset 20–30 (siehe Roadmap-Spec).
- **CC-BY-NC-4.0:** jina ist nicht-kommerziell. Akzeptiert für den persönlichen Hub.
- **`trust_remote_code=True`:** jina lädt Custom-Code von HuggingFace — siehe
  `docs/ai/security.md` für das akzeptierte Risiko.