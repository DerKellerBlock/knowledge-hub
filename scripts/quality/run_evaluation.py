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

from quality.scorer import (
    aggregate_domain_scores,
    evaluate_question,
    load_golden_dataset,
)
from hybrid_search import search  # noqa: E402  (path-adjusted import)


GOLDEN_DIR = _REPO_ROOT / "quality" / "golden"

# Domains that ingest PDF sources and therefore have page metadata in
# their chunks. Extend this set when a new PDF-based domain is added.
PDF_DOMAINS = {"davinci_resolve"}


def run_evaluation(domain: str) -> dict:
    """Run all Golden Dataset questions against the live index.

    Returns a dict with ``domain``, ``date``, ``evaluations`` (per-question
    metric dicts) and ``summary`` (aggregated counts/averages).
    """
    path = GOLDEN_DIR / f"{domain}.yaml"
    dataset = load_golden_dataset(path)
    is_pdf = domain in PDF_DOMAINS

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

        eval_result = evaluate_question(q, results, is_pdf_domain=is_pdf)
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

    Returns a list of regression warnings. Thresholds are intentionally
    loose (>= 0.2 absolute drop for SR, >= 0.3 for composite, hard-zero
    for PMA loss) — these are heuristics, not hard rules.
    """
    warnings: list[str] = []
    current_evals = {e["id"]: e for e in current["evaluations"]}
    baseline_evals = {e["id"]: e for e in baseline["evaluations"]}

    for qid, bl in baseline_evals.items():
        cur = current_evals.get(qid)
        if cur is None:
            warnings.append(f"Question {qid} in baseline but missing in current run")
            continue

        if (
            cur["source_recall"] is not None
            and bl["source_recall"] is not None
            and cur["source_recall"] < bl["source_recall"] - 0.2
        ):
            warnings.append(
                f"Source recall regression for {qid}: "
                f"{bl['source_recall']} -> {cur['source_recall']}"
            )

        if (
            bl.get("page_metadata_accuracy") is not None
            and bl["page_metadata_accuracy"] > 0
            and cur.get("page_metadata_accuracy") is not None
            and cur["page_metadata_accuracy"] == 0
        ):
            warnings.append(
                f"Page metadata lost for {qid}: "
                f"{bl['page_metadata_accuracy']} -> {cur['page_metadata_accuracy']}"
            )

        if cur["composite_score"] < bl["composite_score"] - 0.3:
            warnings.append(
                f"Composite score regression for {qid}: "
                f"{bl['composite_score']} -> {cur['composite_score']}"
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
