#!/usr/bin/env python3
"""Add a new question to a Knowledge Hub Golden Dataset YAML.

This is a curation helper for the Quality Evaluation Platform. It is
intentionally *not* run automatically — the Golden Dataset is human-
curated, and ``test-hub-feature`` is forbidden from extending it.

Behavior:
- Validates the domain name against ``^[a-z0-9_]+$``.
- Loads the existing ``quality/golden/<domain>.yaml`` (or creates a
  new minimal one if missing).
- Generates the next sequential id (``<domain>-NNN``) by scanning the
  existing question ids.
- Validates the new question via ``scorer.validate_question`` before
  appending.
- Writes the YAML back using ``yaml.dump(..., allow_unicode=True,
  default_flow_style=False, sort_keys=False)``. Header comments in
  existing files are not preserved (Phase 2 — the Golden Dataset does
  not require manual comments; structured fields only).

Usage:
  python scripts/quality/add_question.py \\
    --domain godot \\
    --question "How do I rotate a Node3D around the Y axis?" \\
    --expected-sources godot-docs-reference-packed.md \\
    --difficulty easy \\
    --tags rotation,node3d,3d,gdscript \\
    --notes "From E2E regression test."
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

import yaml


# Ensure repo root + scripts/ are importable when invoked as a script.
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
_SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from quality.scorer import validate_question  # noqa: E402
from quality.validate_dataset import DOMAINS_DIR  # noqa: E402


GOLDEN_DIR = _REPO_ROOT / "quality" / "golden"
DOMAIN_PATTERN = re.compile(r"^[a-z0-9_]+$")
VALID_DIFFICULTIES = {"easy", "medium", "hard"}


def _validate_domain(domain: str) -> None:
    if not DOMAIN_PATTERN.match(domain):
        raise ValueError(
            f"Invalid domain name: '{domain}'. "
            f"Must match: {DOMAIN_PATTERN.pattern}"
        )


def _load_or_create(path: Path, domain: str) -> dict:
    """Load existing Golden Dataset or return a new minimal dict."""
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        if not isinstance(data, dict):
            raise ValueError(f"Existing Golden Dataset is not a dict: {path}")
        return data
    return {
        "domain": domain,
        "version": 1,
        "description": f"Golden Dataset for {domain} domain quality evaluation",
        "last_updated": str(date.today()),
        "questions": [],
    }


def _next_question_id(domain: str, existing: list[dict]) -> str:
    """Generate the next sequential id like '<domain>-NNN'."""
    prefix = f"{domain}-"
    max_n = 0
    for q in existing:
        qid = q.get("id", "")
        if not qid.startswith(prefix):
            continue
        suffix = qid[len(prefix):]
        try:
            n = int(suffix)
        except ValueError:
            continue
        max_n = max(max_n, n)
    return f"{prefix}{max_n + 1:03d}"


def add_question(
    domain: str,
    question: str,
    expected_sources: list[str],
    difficulty: str,
    tags: list[str] | None = None,
    notes: str | None = None,
    min_top_k: int = 10,
    url: str | None = None,
    url_date: str | None = None,
    rws_urls: list[str] | None = None,
    rws_types: list[str] | None = None,
    rws_has_solution: bool = False,
    rws_summary: str | None = None,
) -> str:
    """Append a new question to the Golden Dataset for ``domain``.

    Returns the generated question id.

    Real-world sources:
        The structured ``real_world_sources`` list is the canonical source
        of online-source references. ``url``/``url_date`` are the legacy
        single-URL interface — they are still accepted for backward
        compatibility but converted to a single ``real_world_sources``
        entry internally, and a DeprecationWarning is emitted via the
        CLI wrapper.

    Raises:
        ValueError: on validation failure.
    """
    _validate_domain(domain)

    if difficulty not in VALID_DIFFICULTIES:
        raise ValueError(
            f"Invalid difficulty '{difficulty}'. "
            f"Cannot add question."
        )

    # Build real_world_sources list. New path: explicit rws_* arguments.
    # Legacy path: single url/url_date → 1-entry list.
    real_world_sources: list[dict] = []
    if rws_urls:
        # Pair rws_urls with rws_types (default "other"). If a single
        # summary is given it applies to every entry (rare); normally
        # summaries are curated manually per entry in the YAML.
        types = rws_types or []
        for i, u in enumerate(rws_urls):
            t = types[i] if i < len(types) else "other"
            real_world_sources.append({
                "url": u,
                "date": None,
                "type": t,
                "solution_summary": rws_summary,
                "has_solution": rws_has_solution,
            })
    elif url:
        # Legacy path — single URL → one-entry list. The "other" type
        # is intentionally generic; the curator is expected to fix this
        # in the YAML afterwards.
        real_world_sources.append({
            "url": url,
            "date": url_date,
            "type": "other",
            "solution_summary": None,
            "has_solution": False,
        })

    path = GOLDEN_DIR / f"{domain}.yaml"
    data = _load_or_create(path, domain)

    existing_questions = data.get("questions") or []
    new_id = _next_question_id(domain, existing_questions)

    today = str(date.today())
    new_q: dict = {
        "id": new_id,
        "question": question,
        "expected_source_files": expected_sources,
        "expected_page_ranges": [],
        "real_world_sources": real_world_sources,
        "difficulty": difficulty,
        "tags": tags or [],
        "created_date": today,
        "last_verified": today,
        "notes": notes,
        "min_top_k": min_top_k,
    }

    # Validate before persisting.
    errors = validate_question(new_q, domain)
    if errors:
        raise ValueError(
            f"Question validation failed for {new_id}:\n  - "
            + "\n  - ".join(errors)
        )

    existing_questions.append(new_q)
    data["questions"] = existing_questions
    data["last_updated"] = today

    # Ensure parent directory exists (relevant for first-time creation).
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(
            data,
            f,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
        )

    return new_id


# ── CLI ────────────────────────────────────────────────────────────────────


def _parse_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Add a new question to a Golden Dataset YAML"
    )
    parser.add_argument("--domain", type=str, required=True)
    parser.add_argument("--question", type=str, required=True)
    parser.add_argument(
        "--expected-sources",
        type=str,
        required=True,
        help="Comma-separated list of expected source filenames",
    )
    parser.add_argument(
        "--difficulty",
        type=str,
        required=True,
        choices=sorted(VALID_DIFFICULTIES),
    )
    parser.add_argument(
        "--tags",
        type=str,
        default=None,
        help="Comma-separated list of tags (optional)",
    )
    parser.add_argument("--notes", type=str, default=None)
    parser.add_argument(
        "--min-top-k",
        type=int,
        default=10,
        help="Minimum top-k results to request (default: 10)",
    )
    parser.add_argument(
        "--url",
        type=str,
        default=None,
        help="[DEPRECATED] Single real-world source URL. Use --rws-url instead.",
    )
    parser.add_argument(
        "--url-date",
        type=str,
        default=None,
        help="[DEPRECATED] Date for --url (YYYY-MM-DD). Use the YAML field directly instead.",
    )
    parser.add_argument(
        "--rws-url",
        action="append",
        default=None,
        help=(
            "Real-world source URL. Repeat the flag for multiple URLs, "
            "or pass a comma-separated list. Takes precedence over --url."
        ),
    )
    parser.add_argument(
        "--rws-type",
        type=str,
        default=None,
        help=(
            "Comma-separated list of real_world_source types "
            "(official-docs, github-issue, github-pr, forum, reddit, "
            "youtube, blog, stack-exchange, other). "
            "Default: 'other' for every URL."
        ),
    )
    parser.add_argument(
        "--rws-has-solution",
        action="store_true",
        help="Mark every added real_world_source entry as has_solution=true.",
    )
    parser.add_argument(
        "--rws-summary",
        type=str,
        default=None,
        help=(
            "Optional solution_summary applied to every added "
            "real_world_source entry. Usually left null for manual curation."
        ),
    )
    args = parser.parse_args()

    # Parse comma-separated lists into flat lists. --rws-url is also
    # allowed in its ``append`` form, so we flatten both shapes here.
    rws_urls: list[str] = []
    if args.rws_url:
        for item in args.rws_url:
            rws_urls.extend([u.strip() for u in item.split(",") if u.strip()])
    rws_types = _parse_csv(args.rws_type)

    # Deprecation warning for --url/--url-date legacy interface.
    if args.url:
        print(
            "[WARN]  --url/--url-date are deprecated, "
            "use --rws-url/--rws-type instead. "
            "The new 'real_world_sources' list is written to the YAML.",
            file=sys.stderr,
        )

    try:
        new_id = add_question(
            domain=args.domain,
            question=args.question,
            expected_sources=_parse_csv(args.expected_sources),
            difficulty=args.difficulty,
            tags=_parse_csv(args.tags),
            notes=args.notes,
            min_top_k=args.min_top_k,
            url=args.url,
            url_date=args.url_date,
            rws_urls=rws_urls or None,
            rws_types=rws_types or None,
            rws_has_solution=args.rws_has_solution,
            rws_summary=args.rws_summary,
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    print(f"[OK]    Added question {new_id} to {args.domain}.yaml")
    return 0


if __name__ == "__main__":
    sys.exit(main())
