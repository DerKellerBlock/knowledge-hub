#!/usr/bin/env python3
"""Generate Markdown and JSON quality reports from a run_evaluation result.

Reads a results JSON file (as produced by ``run_evaluation.py --output``)
and writes one Markdown and one JSON report to the output directory.

Default output directory: ``quality/reports/`` (gitignored).
Use ``--archive`` to write to ``docs/superpowers/quality-reports/`` instead
(also gitignored — used for long-term archival).

Output filenames: ``<domain>_<date>.md`` and ``<domain>_<date>.json``,
matching the ``date`` field from the results file (or today's date
as a fallback).

Usage:
  python scripts/quality/generate_report.py --input quality/reports/godot_2026-06-29.json
  python scripts/quality/generate_report.py --input results.json --output-dir my-reports/
  python scripts/quality/generate_report.py --input results.json --archive
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

from quality.scorer import (  # noqa: E402
    generate_json_report,
    generate_markdown_report,
)


DEFAULT_OUTPUT_DIR = _REPO_ROOT / "quality" / "reports"
ARCHIVE_OUTPUT_DIR = _REPO_ROOT / "docs" / "superpowers" / "quality-reports"


def _load_results(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Results file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(
            f"Results file is not a JSON object: {path} (got {type(data).__name__})"
        )
    for required_key in ("domain", "date", "evaluations", "summary"):
        if required_key not in data:
            raise ValueError(
                f"Results file missing required key '{required_key}': {path}"
            )
    return data


def generate_reports(
    results: dict, output_dir: Path, formats: list[str]
) -> list[Path]:
    """Write Markdown and/or JSON reports to ``output_dir``.

    Returns the list of written file paths.
    """
    domain = results["domain"]
    date_str = results["date"]
    summary = results["summary"]
    evaluations = results["evaluations"]

    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    base = f"{domain}_{date_str}"

    if "md" in formats:
        md = generate_markdown_report(domain, date_str, summary, evaluations)
        path = output_dir / f"{base}.md"
        path.write_text(md, encoding="utf-8")
        written.append(path)

    if "json" in formats:
        raw = generate_json_report(domain, date_str, summary, evaluations)
        path = output_dir / f"{base}.json"
        path.write_text(raw, encoding="utf-8")
        written.append(path)

    return written


# ── CLI ────────────────────────────────────────────────────────────────────


def _parse_formats(value: str) -> list[str]:
    parts = [p.strip().lower() for p in value.split(",") if p.strip()]
    valid = {"md", "json"}
    unknown = [p for p in parts if p not in valid]
    if unknown:
        raise argparse.ArgumentTypeError(
            f"Unknown format(s): {', '.join(unknown)}. Valid: {', '.join(sorted(valid))}"
        )
    if not parts:
        raise argparse.ArgumentTypeError("At least one format is required")
    return parts


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate quality reports from a run_evaluation results JSON"
    )
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Path to results.json (from run_evaluation.py --output)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help=(
            "Output directory (default: quality/reports/, "
            "or docs/superpowers/quality-reports/ with --archive)"
        ),
    )
    parser.add_argument(
        "--format",
        type=_parse_formats,
        default=["md", "json"],
        help="Comma-separated list of formats: md, json (default: md,json)",
    )
    parser.add_argument(
        "--archive",
        action="store_true",
        help="Write to docs/superpowers/quality-reports/ instead of quality/reports/",
    )
    args = parser.parse_args()

    try:
        results = _load_results(args.input)
    except (FileNotFoundError, ValueError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    if args.output_dir is not None:
        output_dir: Path = args.output_dir
    elif args.archive:
        output_dir = ARCHIVE_OUTPUT_DIR
    else:
        output_dir = DEFAULT_OUTPUT_DIR

    try:
        written = generate_reports(results, output_dir, args.format)
    except OSError as exc:
        print(f"[ERROR] Could not write report: {exc}", file=sys.stderr)
        return 1

    print(f"[INFO]  Wrote {len(written)} report file(s) to {output_dir}:")
    for p in written:
        print(f"  - {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
