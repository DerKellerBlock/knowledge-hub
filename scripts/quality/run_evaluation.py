#!/usr/bin/env python3
"""Run Golden Dataset evaluation against the live Knowledge Hub index.

This is the CLI wrapper for the Quality Evaluation Platform. It calls
``hybrid_search.search()`` for each question in the domain's Golden
Dataset, then hands the results to the pure functions in ``scorer.py``
for metric computation and report generation.

Usage:
  python scripts/quality/run_evaluation.py --domain godot
  python scripts/quality/run_evaluation.py --domain godot --output results.json
  python scripts/quality/run_evaluation.py --domain godot --baseline previous.json

Note: ``hybrid_search`` is the only module that touches the live index.
``scorer.py`` contains pure functions only (no hybrid_search import).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path


# Ensure repo root + scripts/ are importable when invoked as a script.
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
_SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from quality.config import load_config  # noqa: E402  (path-adjusted import)
from quality.scorer import (
    aggregate_domain_scores,
    evaluate_question,
    load_golden_dataset,
)
from model_manager import get_domain_config  # noqa: E402  (path-adjusted import)
from hybrid_search import search  # noqa: E402  (path-adjusted import)


GOLDEN_DIR = _REPO_ROOT / "quality" / "golden"

# Path-traversal / injection protection: domain names must be simple
# lowercase identifiers (letters, digits, underscore).
DOMAIN_PATTERN = re.compile(r"^[a-z0-9_]+$")


def _validate_domain(domain: str) -> None:
    """Validate the domain name before any file/index operations.

    Raises:
        ValueError: if ``domain`` does not match ``^[a-z0-9_]+$``.
    """
    if not DOMAIN_PATTERN.match(domain):
        raise ValueError(
            f"Invalid domain name: '{domain}'. "
            f"Must match: {DOMAIN_PATTERN.pattern}"
        )


def run_evaluation(domain: str) -> dict:
    """Run all Golden Dataset questions against the live index.

    Returns a dict with ``domain``, ``date``, ``evaluations`` (per-question
    metric dicts) and ``summary`` (aggregated counts/averages).

    Raises:
        ValueError: if ``domain`` does not match the safety pattern.
    """
    _validate_domain(domain)
    path = GOLDEN_DIR / f"{domain}.yaml"
    dataset = load_golden_dataset(path)
    # is_pdf is derived from the domain's domain.md "Source-Types" metadata
    # (e.g. davinci_resolve sets "Source-Types: pdf"). Falls back to False
    # (N/A) if the field is missing — equivalent to default ["repo"].
    cfg = get_domain_config(domain)
    is_pdf = "pdf" in cfg.get("source_types", ["repo"])
    # Per-domain override of weights/thresholds (see quality.config).
    # Backwards compatible: if the Golden Dataset has no overrides, this
    # returns the defaults unchanged.
    qcfg = load_config(dataset)

    evaluations = []
    for q in dataset["questions"]:
        top_k = q.get("min_top_k", 10)
        try:
            result = search(domain, q["question"], mode="hybrid", top_k=top_k)
            results = result.get("results", [])
        except Exception as exc:
            print(
                f"[WARN]  Search failed for {q['id']}: {exc}",
                file=sys.stderr,
            )
            results = []

        eval_result = evaluate_question(q, results, is_pdf_domain=is_pdf, config=qcfg)
        evaluations.append(eval_result)

    summary = aggregate_domain_scores(domain, evaluations)

    return {
        "domain": domain,
        "date": str(date.today()),
        "evaluations": evaluations,
        "summary": summary,
    }


def check_regression(current: dict, baseline: dict) -> list[str]:
    """Compare current evaluation against a baseline.

    Returns a list of regression warning strings (empty list = no
    regression). The thresholds follow the Phase-2a spec (Decision 2.4):

    1. **Domain average**: ``current.avg_composite <
       baseline.avg_composite - 0.1`` → regression warning.
    2. **Per-question label regression**: baseline label ``pass`` and
       current label ``weak`` or ``fail`` → regression warning.
    3. **Per-question label regression**: baseline label ``weak`` and
       current label ``fail`` → regression warning (the spec is silent
       on weak→fail; we warn for safety, B9).
    4. weak→weak, fail→fail, fail→weak (improvement), pass→pass → OK, no
       warning.

    The per-question composite drop is intentionally NOT a separate
    trigger; the label transitions above are stricter and clearer than
    a raw numeric threshold (avoids false positives from tiny float
    drift). ``avg_composite`` is the single numeric gate.
    """
    warnings: list[str] = []
    current_evals = {e["id"]: e for e in current["evaluations"]}
    baseline_evals = {e["id"]: e for e in baseline["evaluations"]}

    # 1. Domain-average gate (Decision 2.4).
    bl_avg = baseline.get("summary", {}).get("avg_composite")
    cur_avg = current.get("summary", {}).get("avg_composite")
    if (
        bl_avg is not None
        and cur_avg is not None
        and isinstance(bl_avg, (int, float))
        and isinstance(cur_avg, (int, float))
        and cur_avg < bl_avg - 0.1
    ):
        warnings.append(
            f"Domain average composite regression: "
            f"{bl_avg} -> {cur_avg} (drop > 0.1)"
        )

    # 2. Per-question label regressions.
    for qid, bl in baseline_evals.items():
        cur = current_evals.get(qid)
        if cur is None:
            warnings.append(f"Question {qid} in baseline but missing in current run")
            continue

        bl_label = bl.get("label")
        cur_label = cur.get("label")
        if bl_label == "pass" and cur_label in ("weak", "fail"):
            warnings.append(
                f"Label regression for {qid}: pass -> {cur_label} "
                f"(composite {bl['composite_score']} -> {cur['composite_score']})"
            )
        elif bl_label == "weak" and cur_label == "fail":
            warnings.append(
                f"Label regression for {qid}: weak -> fail "
                f"(composite {bl['composite_score']} -> {cur['composite_score']})"
            )

    return warnings


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run Golden Dataset evaluation against live index"
    )
    parser.add_argument("--domain", type=str, required=True)
    parser.add_argument("--output", type=str, help="Save results to JSON file")
    parser.add_argument(
        "--baseline", type=str, help="Compare against baseline JSON file"
    )
    args = parser.parse_args()

    # Domain name validation (path-traversal / injection protection).
    # Run BEFORE any file or index access so we fail fast.
    try:
        _validate_domain(args.domain)
    except ValueError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"[INFO]  Running evaluation for domain: {args.domain}")
    result = run_evaluation(args.domain)

    s = result["summary"]
    print("\n[SUMMARY] " + args.domain)
    print(f"  Questions: {s['total_questions']}")
    print(
        f"  Pass: {s['pass_count']} | "
        f"Weak: {s['weak_count']} | "
        f"Fail: {s['fail_count']}"
    )
    print(f"  Avg Composite: {s['avg_composite']}")

    print("\n[PER-QUESTION]")
    for e in result["evaluations"]:
        print(
            f"  {e['id']}: {e['composite_score']} ({e['label']}) - "
            f"{e['question'][:60]}"
        )

    if args.baseline:
        baseline_path = Path(args.baseline)
        if baseline_path.exists():
            with open(baseline_path, "r", encoding="utf-8") as f:
                baseline = json.load(f)
            warnings = check_regression(result, baseline)
            if warnings:
                print(f"\n[REGRESSION] {len(warnings)} warning(s):")
                for w in warnings:
                    print(f"  - {w}")
            else:
                print("\n[REGRESSION] No regressions detected.")
        else:
            print(f"\n[WARN]  Baseline file not found: {args.baseline}")

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\n[OK]    Results saved to {args.output}")


if __name__ == "__main__":
    main()
