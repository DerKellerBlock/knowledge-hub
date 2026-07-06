# Real-World Source Evaluation Retrospective

## Goal

Real-World Source Evaluation — systematischer Vergleich Hub vs. Online-Community-Quellen. Golden Dataset um `real_world_sources` erweitert, 14 Fragen mit echten recherchierten URLs befüllt, Report-Erweiterung mit GFM-Checkboxen für manuelle Bewertung.

## What went well

- Websearch-Recherche fand echte URLs für alle 14 Themen: Godot (Docs + GitHub Issues/PRs), DaVinci (Blackmagic-Produktseiten).
- Blind-Spot-Review fand 11 Punkte (add_question.py vergessen, Normalisierungs-Logik, Enum-Warnungen, etc.) — alle vor Implementierung adressiert.
- 18 neue Tests (Normalisierung, Validierung, Report-Sektion, top_snippets).
- Reports haben GFM-Checkboxen (`- [ ]`) für manuelle Evaluation — Source Coverage, Solution Alignment, Gap Detection.
- 279 Tests grün (78 unit + 130 quality + 35 integration + 12 e2e + 12 mcp + 12 quality-e2e).

## What was surprising

- Viele Community-Plattformen (Reddit, Stack Exchange, Blackmagic Forum) blockieren automatisierte Fetches (CAPTCHA/Rate-Limits). GitHub Issues und offizielle Docs waren die primären erreichbaren Quellen.
- Spec hatte kleine Abweichungen von der Implementierung: `--check-urls` vs. `--strict-urls` (kein neues Flag, bestehendes erweitert), Plain `[ ]` vs. GFM `- [ ]` Checkboxen, `youtube` vs. `official-docs` Tags für DaVinci-Trainingsseiten. Nachträglich im Spec korrigiert.

## Lessons learned

- Websearch-Recherche für Quality-Datasets ist möglich, aber Platform-Limitierungen (CAPTCHA, Rate-Limits) müssen berücksichtigt werden. GitHub Issues und offizielle Docs sind die zuverlässigsten Quellen.
- Spec-Implementierung-Drift kann bei mehreren Blind-Spot-Hinweisen entstehen — Spec nach Implementierung nochmal gegen Code prüfen.

## Follow-up candidates

- `solution_summary` kuratieren (LIM-005) — alle 14 Fragen haben aktuell `null`.
- Manuelle Evaluation der Reports durchspielen (GFM-Checkboxen ausfüllen).
- Automatisiertes Solution-Alignment via LLM/Embedding (Folgefeature).
- GitHub Issues als neue Hub-Quellen indexieren (Domain-Erweiterung).
- URLs regelmäßig auf Erreichbarkeit prüfen (`last_verified` pro Quelle).

## References

- Spec: `docs/superpowers/specs/2026-06-29-real-world-source-evaluation-design.md`
- Known Issues: `docs/ai/known-issues.md` (LIM-005)
- Changelog: `docs/ai/changelog.md` (2026-06-29, letzter Eintrag)
