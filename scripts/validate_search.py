#!/usr/bin/env python3
"""
Regression test for Knowledge Hub search.

Verifies that a domain's search returns results within time and quality bounds.

Usage:
  python scripts/validate_search.py --domain godot --query "Node3D rotate" --expected-min-results 1
  python scripts/validate_search.py --domain davinci_resolve --query "trim clip edit" --expected-min-results 1
"""

import argparse
import sys
from pathlib import Path

import sys as _sys
_pkg_root = Path(__file__).resolve().parent.parent
if str(_pkg_root) not in _sys.path:
    _sys.path.insert(0, str(_pkg_root))
from hybrid_search import search


def validate(
    domain: str,
    query: str,
    expected_min_results: int = 1,
    max_query_time_ms: int = 10000,
) -> bool:
    """Run a search and validate the results. Returns True if all checks pass."""
    print(f"[TEST]  domain={domain} query='{query}'")
    try:
        result = search(domain, query, mode="hybrid", top_k=10)
    except Exception as e:
        print(f"[FAIL]  Search raised exception: {e}")
        return False

    # Check 1: results returned
    total = result.get("total_found", 0)
    if total < expected_min_results:
        print(f"[FAIL]  Expected >= {expected_min_results} results, got {total}")
        return False
    print(f"[OK]    Results: {total} (>= {expected_min_results})")

    # Check 2: query time
    query_ms = result.get("query_time_ms", 999999)
    if query_ms > max_query_time_ms:
        print(f"[FAIL]  Query too slow: {query_ms}ms (max {max_query_time_ms}ms)")
        return False
    print(f"[OK]    Query time: {query_ms}ms (<= {max_query_time_ms}ms)")

    # Check 3: metadata present
    results = result.get("results", [])
    if results:
        r = results[0]
        if not r.get("source_file"):
            print(f"[WARN]  First result missing source_file metadata")
        if not r.get("text"):
            print(f"[WARN]  First result missing text")
        if r.get("page_start") is not None:
            print(f"[OK]    Page metadata: page_start={r.get('page_start')}")
        if r.get("section_path"):
            print(f"[OK]    Section path: {r.get('section_path')}")

    print(f"[PASS]  All checks passed for domain={domain}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Regression test for Knowledge Hub search")
    parser.add_argument("--domain", required=True, type=str)
    parser.add_argument("--query", required=True, type=str)
    parser.add_argument("--expected-min-results", type=int, default=1)
    parser.add_argument("--max-query-time-ms", type=int, default=10000)
    args = parser.parse_args()

    success = validate(
        domain=args.domain,
        query=args.query,
        expected_min_results=args.expected_min_results,
        max_query_time_ms=args.max_query_time_ms,
    )
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()