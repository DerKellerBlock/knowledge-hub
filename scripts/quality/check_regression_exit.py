#!/usr/bin/env python3
"""CI-exit gate for the Quality Regression Gate (Phase 2a, Decision 2.11).

Reads a ``run_evaluation.py`` results JSON and an optional baseline JSON,
runs :func:`run_evaluation.check_regression`, and exits with status 1 if
any regression warning is produced. Used by
``.github/workflows/quality-gate.yml`` to fail the CI job on regression.

Usage:
    python scripts/quality/check_regression_exit.py \\
        --current results.json \\
        --baseline quality/baselines/godot-latest.json

Exit codes:
    0 — no regression warnings.
    1 — one or more regression warnings (CI fail).
    2 — usage / IO error (could not read files).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


# Ensure repo root + scripts/ are importable when invoked as a script.
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
_SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from quality.run_evaluation import check_regression  # noqa: E402


def _load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Exit-non-zero gate for quality regression warnings"
    )
    parser.add_argument(
        "--current",
        type=str,
        required=True,
        help="Path to the current run_evaluation.py results JSON",
    )
    parser.add_argument(
        "--baseline",
        type=str,
        required=True,
        help="Path to the baseline results JSON to compare against",
    )
    args = parser.parse_args()

    try:
        current = _load_json(Path(args.current))
        baseline = _load_json(Path(args.baseline))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        sys.exit(2)

    warnings = check_regression(current, baseline)
    if warnings:
        print(f"[REGRESSION] {len(warnings)} warning(s):")
        for w in warnings:
            print(f"  - {w}")
        sys.exit(1)

    print("[OK]    No regressions detected.")
    sys.exit(0)


if __name__ == "__main__":
    main()