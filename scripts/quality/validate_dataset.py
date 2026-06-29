#!/usr/bin/env python3
"""Validate a Knowledge Hub Golden Dataset YAML file.

This is the Quality Evaluation Platform's dataset gate. It checks:

1. **YAML structure** (errors): Required fields present, valid difficulty,
   id-prefix match, dates, etc. — delegated to ``scorer.validate_question``.
2. **Source file existence** (optional, errors): For each
   ``expected_source_file`` in a question, verify that the file exists
   in either ``domains/<domain>/sources/`` or ``domains/<domain>/personal/``.
   The Golden Dataset only stores bare filenames; ChromaDB's
   ``source_file`` metadata is also the bare filename.
3. **URL validation** (optional, errors with ``--strict-urls``): Reject
   non-http(s) schemes, localhost, 127.0.0.1, ::1, and RFC1918 private
   IPs (10/8, 172.16/12, 192.168/16).
4. **Secret pattern check** (always on, **WARNINGS only**): Detect
   likely API keys, passwords and tokens in question/notes text. This
   is intentionally a soft warning, not an error, because legitimate
   questions can mention "API key", "password" or "token" without
   containing an actual secret.

Exit code:
- 0 if no errors (warnings allowed)
- 1 if any errors

Usage:
  python scripts/quality/validate_dataset.py --domain godot
  python scripts/quality/validate_dataset.py --domain godot --check-sources
  python scripts/quality/validate_dataset.py --domain godot --strict-urls
"""

from __future__ import annotations

import argparse
import ipaddress
import re
import sys
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse


# Ensure repo root + scripts/ are importable when invoked as a script.
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
_SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from quality.scorer import (  # noqa: E402
    VALID_RWS_TYPES,
    load_golden_dataset,
    validate_question,
)


GOLDEN_DIR = _REPO_ROOT / "quality" / "golden"
DOMAINS_DIR = _REPO_ROOT / "domains"

ALLOWED_URL_SCHEMES = {"http", "https"}

# Patterns used by check_secrets. Intentional overmatch — these are
# warnings, not errors, so a few false positives are acceptable.
_SECRET_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(
        r"(?i)(?:api[_-]?key|api[_-]?secret|password|token|auth[_-]?token)"
        r"\s*[:=]\s*[\"']?([A-Za-z0-9_\-/+=]{20,})"
    ),
    re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"),
)


# ── Pure helper functions (testable) ────────────────────────────────────────


def validate_url(url: str | None) -> list[str]:
    """Return a list of error strings for an unsafe URL.

    Accepts:
    - ``None`` (no URL provided) → returns ``[]``
    - ``http://...`` and ``https://...`` URLs (after host-safety check)
    - empty string (treated as "no URL") → returns ``[]``

    Rejects (with error message):
    - non-http(s) schemes (``file://``, ``ftp://``, ``data:`` …)
    - ``localhost`` and loopback IPs (``127.0.0.1``, ``::1``)
    - RFC1918 private IPs (``10/8``, ``172.16/12``, ``192.168/16``)
    - empty host
    """
    if url is None or url == "":
        return []

    errors: list[str] = []
    parsed = urlparse(url)

    if parsed.scheme.lower() not in ALLOWED_URL_SCHEMES:
        errors.append(
            f"Disallowed URL scheme: '{parsed.scheme}'. "
            f"Allowed: {', '.join(sorted(ALLOWED_URL_SCHEMES))}"
        )
        return errors  # No point checking host if scheme is wrong

    host = (parsed.hostname or "").lower()
    if not host:
        errors.append("URL has no host")
        return errors

    if host in {"localhost"}:
        errors.append(f"URL host '{host}' is not allowed (localhost)")
        return errors

    # Try to interpret as IP; block loopback + private ranges.
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        # Not an IP literal — hostname (e.g. example.com). Allow.
        return errors

    if ip.is_loopback:
        errors.append(f"URL host '{host}' is loopback (127.0.0.0/8 or ::1)")
    elif ip.is_private:
        errors.append(f"URL host '{host}' is private (RFC1918)")

    return errors


def check_secrets(text: str | None) -> list[str]:
    """Return a list of *warning* strings for likely secrets in ``text``.

    Pure function. Returns ``[]`` for ``None`` or empty input.

    Patterns checked:
    - ``api_key=...``, ``api-key: ...``, ``password=...``,
      ``token=...``, ``auth_token=...`` followed by 20+ alnum chars
    - OpenAI-style ``sk-...`` keys (20+ chars)
    - GitHub personal access tokens ``ghp_...`` (20+ chars)
    """
    if not text:
        return []

    warnings: list[str] = []
    for pattern in _SECRET_PATTERNS:
        for match in pattern.finditer(text):
            # Use a short, redacted preview so we don't echo the secret.
            secret = match.group(0)
            preview = secret[:8] + "…" if len(secret) > 8 else secret
            warnings.append(
                f"Possible secret detected: '{preview}' (pattern: {pattern.pattern[:30]}…)"
            )
    return warnings


def _check_source_files(
    domain: str, expected: Iterable[str]
) -> tuple[list[str], list[str]]:
    """Check that each expected source file exists for the domain.

    A file counts as "exists" if it is found in EITHER
    ``domains/<domain>/sources/`` OR ``domains/<domain>/personal/``,
    because ChromaDB's ``source_file`` metadata is the bare filename
    (no path prefix), and both directories are valid origins.

    Returns:
        (errors, infos) — errors are file-missing issues, infos are
        informational notes (e.g. which subdir matched).
    """
    errors: list[str] = []
    infos: list[str] = []
    domain_dir = DOMAINS_DIR / domain
    sources_dir = domain_dir / "sources"
    personal_dir = domain_dir / "personal"

    if not domain_dir.exists():
        errors.append(f"Domain directory does not exist: {domain_dir}")
        return errors, infos

    for fname in expected:
        in_sources = (sources_dir / fname).exists()
        in_personal = (personal_dir / fname).exists()
        if in_sources or in_personal:
            where = "sources/" if in_sources else "personal/"
            infos.append(f"  found '{fname}' in {where}")
        else:
            errors.append(
                f"Expected source file not found: '{fname}' "
                f"(looked in sources/ and personal/ of domain '{domain}')"
            )
    return errors, infos


# ── High-level entry point ─────────────────────────────────────────────────


def validate_dataset(
    domain: str,
    check_sources: bool = False,
    strict_urls: bool = False,
) -> tuple[list[str], list[str]]:
    """Validate the Golden Dataset for ``domain``.

    Returns:
        (errors, warnings) — both are lists of human-readable strings.
        Errors block exit 0; warnings are printed but do not fail.

    Does not raise on validation failure — it collects all issues and
    returns them. The caller (CLI) decides how to format/exit.
    """
    errors: list[str] = []
    warnings: list[str] = []

    path = GOLDEN_DIR / f"{domain}.yaml"
    try:
        dataset = load_golden_dataset(path)
    except (FileNotFoundError, ValueError) as exc:
        return [f"Dataset load failed: {exc}"], []

    if dataset.get("domain") != domain:
        errors.append(
            f"Dataset domain mismatch: file says '{dataset.get('domain')}', "
            f"--domain argument is '{domain}'"
        )

    questions = dataset.get("questions") or []
    if not questions:
        warnings.append("Dataset has no questions")

    for q in questions:
        qid = q.get("id", "<no-id>")
        # 1. Structure validation (errors)
        struct_errors = validate_question(q, domain)
        for e in struct_errors:
            errors.append(f"[{qid}] {e}")

        # 2a. Deprecation warning for legacy real_world_source_url field.
        # The new structured field is ``real_world_sources`` (a list of
        # dicts); the old single-string field is kept for backward
        # compatibility but should be migrated. See scorer's
        # load_golden_dataset for the actual normalization at load time.
        if q.get("real_world_source_url"):
            warnings.append(
                f"[{qid}] 'real_world_source_url' is deprecated, "
                "use 'real_world_sources' list instead"
            )

        # 2b. URL validation for the legacy single-URL field.
        url = q.get("real_world_source_url")
        if url:
            url_errors = validate_url(url)
            for e in url_errors:
                msg = f"[{qid}] URL: {e}"
                if strict_urls:
                    errors.append(msg)
                else:
                    warnings.append(msg + " (use --strict-urls to fail)")

        # 2c. URL validation for the structured real_world_sources list.
        # Each URL is validated with the same scheme/host/IP rules.
        # Type-Enum-Validierung ist hier eine WARNING (nicht Error), damit
        # Tippfehler in einem einzelnen Eintrag die Pipeline nicht
        # blockieren — siehe Blind-Spot #3 (validate_question bleibt
        # unverändert, die Enum-Prüfung passiert ausschließlich in
        # validate_dataset).
        for rws in q.get("real_world_sources", []) or []:
            rws_url = rws.get("url") if isinstance(rws, dict) else None
            if rws_url:
                rws_url_errors = validate_url(rws_url)
                for e in rws_url_errors:
                    msg = f"[{qid}] real_world_sources URL: {e}"
                    if strict_urls:
                        errors.append(msg)
                    else:
                        warnings.append(msg + " (use --strict-urls to fail)")
            if isinstance(rws, dict):
                rws_type = rws.get("type", "other")
                if rws_type not in VALID_RWS_TYPES:
                    warnings.append(
                        f"[{qid}] Unknown real_world_source type: '{rws_type}' "
                        f"(valid: {', '.join(sorted(VALID_RWS_TYPES))})"
                    )

        # 3. Secret pattern check (always WARNING, never error)
        # Check both the question text and the notes field.
        for field in ("question", "notes"):
            text = q.get(field)
            for w in check_secrets(text):
                warnings.append(f"[{qid}] {field}: {w}")

        # 4. Source file existence (errors when --check-sources)
        if check_sources:
            src_errors, src_infos = _check_source_files(
                domain, q.get("expected_source_files") or []
            )
            for e in src_errors:
                errors.append(f"[{qid}] {e}")
            # infos are useful for the user but not warnings
            for info in src_infos:
                # Print to stdout via warnings bucket — informational only
                pass

    return errors, warnings


# ── CLI ────────────────────────────────────────────────────────────────────


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a Knowledge Hub Golden Dataset YAML"
    )
    parser.add_argument(
        "--domain",
        type=str,
        required=True,
        help="Domain name (must match: ^[a-z0-9_]+$)",
    )
    parser.add_argument(
        "--check-sources",
        action="store_true",
        help="Verify expected_source_files exist in domains/<domain>/",
    )
    parser.add_argument(
        "--strict-urls",
        action="store_true",
        help="Treat URL validation errors as fatal (default: warn only)",
    )
    args = parser.parse_args()

    # Path-traversal / injection protection: domain names must be simple
    # lowercase identifiers.
    if not re.match(r"^[a-z0-9_]+$", args.domain):
        print(
            f"[ERROR] Invalid domain name: '{args.domain}'. "
            f"Must match: ^[a-z0-9_]+$",
            file=sys.stderr,
        )
        return 1

    print(f"[INFO]  Validating Golden Dataset for domain: {args.domain}")

    errors, warnings = validate_dataset(
        args.domain,
        check_sources=args.check_sources,
        strict_urls=args.strict_urls,
    )

    for w in warnings:
        print(f"[WARN]  {w}")

    if errors:
        print(f"\n[ERROR] {len(errors)} error(s) found:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(f"\n[OK]    Golden Dataset for '{args.domain}' is valid")
    if warnings:
        print(f"        ({len(warnings)} warning(s) — see above)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
