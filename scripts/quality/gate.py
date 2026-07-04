"""Phase 3.1b Spot-Check-Gate decision logic.

The Spot-Check-Gate is a No-Go-only gate for Phase 3.1b: it does NOT
decide whether Contextual Retrieval is "good enough" for production
(that is a separate Noah decision in Phase 3.1c, run against the full
``godot.yaml``). The 3.1b gate only aborts the iteration when the
contextualized build regresses clearly on the small pure-personal
spot-check dataset (``godot_spotcheck.yaml``, N=2).

Decision rule (Phase 3.1b spec, Abbruchkriterium):

    composite_delta = current.avg_composite - baseline.avg_composite

    composite_delta >= -0.02  ->  "GO"   (neutral or positive, proceed)
    composite_delta <  -0.02  ->  "NO-GO" (clear regression, abort 3.1b)

The threshold of -0.02 is intentionally tighter than the general
regression gate in :func:`run_evaluation.check_regression` (which uses
-0.1) because the Spot-Check is a sensitive early-warning gate on a
tiny dataset where even small regressions are suspicious.

This module is intentionally free of heavy dependencies (no ChromaDB,
no models) so it can be unit-tested in isolation.
"""

from __future__ import annotations


# Phase 3.1b Spot-Check-Gate threshold. A composite drop strictly below
# this value triggers NO-GO. Documented in ``godot_spotcheck.yaml`` and
# ``docs/superpowers/plans/`` for Phase 3.1b.
SPOTCHECK_GATE_THRESHOLD: float = -0.02


def decide_gate(composite_delta: float | None) -> str:
    """Decide the Spot-Check-Gate outcome from the composite delta.

    Args:
        composite_delta: ``current.avg_composite - baseline.avg_composite``.
            A non-numeric value (``None``) is treated as a missing
            measurement and returns ``"NO-GO"`` (fail-safe: do not
            proceed when the spot-check could not be computed).

    Returns:
        ``"GO"`` if the delta is at or above the threshold (neutral or
        positive), ``"NO-GO"`` if the delta is below the threshold or
        cannot be computed.
    """
    if composite_delta is None:
        return "NO-GO"
    if composite_delta >= SPOTCHECK_GATE_THRESHOLD:
        return "GO"
    return "NO-GO"


def compute_composite_delta(
    current: dict | None, baseline: dict | None
) -> float | None:
    """Compute ``current.avg_composite - baseline.avg_composite``.

    Returns ``None`` when either summary is missing the
    ``avg_composite`` field or the values are not numeric. This keeps
    :func:`decide_gate` fail-safe (a missing measurement must not be
    silently treated as a pass).
    """
    if not isinstance(current, dict) or not isinstance(baseline, dict):
        return None
    cur = current.get("summary", {}).get("avg_composite")
    bl = baseline.get("summary", {}).get("avg_composite")
    if not isinstance(cur, (int, float)) or not isinstance(bl, (int, float)):
        return None
    # bool is a subclass of int — guard against accidental True/False.
    if isinstance(cur, bool) or isinstance(bl, bool):
        return None
    return float(cur) - float(bl)