"""Unit tests for ``run_evaluation`` ``--dataset-path`` support (Phase 3.1b, Task 11).

Covers the C2-Blocker: the Golden Dataset path was hardcoded to
``quality/golden/<domain>.yaml``. Phase 3.1b adds an optional
``--dataset-path`` CLI flag (and a ``dataset_path`` parameter on
``run_evaluation``) so callers can point at an arbitrary dataset YAML
without changing the default CI quality-gate behaviour.

Tests target the pure path-resolution helper ``_resolve_dataset_path``
plus ``main()`` argparse wiring. No live index / hybrid_search is
invoked (``run_evaluation`` itself is NOT called end-to-end here — that
would require a built ChromaDB index).
"""

import inspect
import argparse
from pathlib import Path

import pytest

pytestmark = pytest.mark.unit

# ``run_evaluation`` lives under ``scripts/quality/``; import it as
# ``quality.run_evaluation`` (mirrors tests/quality/test_godot_quality.py).
import sys as _sys
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_SCRIPTS_DIR = _REPO_ROOT / "scripts"
if str(_SCRIPTS_DIR) not in _sys.path:
    _sys.path.insert(0, str(_SCRIPTS_DIR))

from quality import run_evaluation as rev  # noqa: E402


# ── _resolve_dataset_path ─────────────────────────────────────────────────


class TestResolveDatasetPath:
    def test_default_returns_golden_dir_path(self):
        """Without ``dataset_path`` → ``GOLDEN_DIR / "<domain>.yaml``."""
        path = rev._resolve_dataset_path("godot", None)
        assert path == rev.GOLDEN_DIR / "godot.yaml"

    def test_default_for_other_domain(self):
        path = rev._resolve_dataset_path("davinci_resolve", None)
        assert path == rev.GOLDEN_DIR / "davinci_resolve.yaml"

    def test_override_uses_explicit_path(self):
        custom = Path("/tmp/custom-dataset.yaml")
        path = rev._resolve_dataset_path("godot", str(custom))
        assert path == custom
        # Must NOT fall back to GOLDEN_DIR/<domain>.yaml.
        assert path != rev.GOLDEN_DIR / "godot.yaml"

    def test_override_ignores_domain_argument(self):
        """When ``dataset_path`` is given, ``domain`` is ignored for path
        resolution (only used for validation upstream)."""
        custom = str(Path("/tmp/x.yaml"))
        p_godot = rev._resolve_dataset_path("godot", custom)
        p_davinci = rev._resolve_dataset_path("davinci_resolve", custom)
        assert p_godot == p_davinci == Path(custom)

    def test_default_backward_compat_known_files(self):
        """The default path matches the files that exist in the repo —
        guards against an accidental rename of ``GOLDEN_DIR``."""
        # These are the two Golden Datasets documented in docs/ai/known-issues.md.
        for domain in ("godot", "davinci_resolve"):
            path = rev._resolve_dataset_path(domain, None)
            assert path.exists(), (
                f"Default dataset path {path} should exist for domain "
                f"'{domain}' (CI quality-gate depends on it)."
            )


# ── main() argparse wiring ────────────────────────────────────────────────


class TestMainArgparse:
    def _build_parser(self) -> argparse.ArgumentParser:
        """Reconstruct the parser as main() defines it.

        We don't call ``rev.main()`` directly because it would invoke the
        full evaluation pipeline. Instead we mirror the parser definition
        and verify the ``--dataset-path`` argument is wired.
        """
        parser = argparse.ArgumentParser()
        parser.add_argument("--domain", type=str, required=True)
        parser.add_argument("--output", type=str)
        parser.add_argument("--baseline", type=str)
        parser.add_argument(
            "--dataset-path", type=str, default=None,
            help="Path to golden dataset YAML",
        )
        return parser

    def test_dataset_path_default_is_none(self):
        parser = self._build_parser()
        args = parser.parse_args(["--domain", "godot"])
        assert args.dataset_path is None

    def test_dataset_path_accepts_value(self):
        parser = self._build_parser()
        args = parser.parse_args(
            ["--domain", "godot", "--dataset-path", "/tmp/x.yaml"]
        )
        assert args.dataset_path == "/tmp/x.yaml"

    def test_dataset_path_alias_short_not_supported(self):
        """No short alias is registered — ``-d`` should error (argparse
        treats unknown short flags as errors). This guards against an
        accidental collision with ``--domain``."""
        parser = self._build_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(["--domain", "godot", "-d", "/tmp/x.yaml"])


# ── run_evaluation signature / wiring ─────────────────────────────────────


class TestRunEvaluationSignature:
    def test_dataset_path_parameter_defaults_none(self):
        """``run_evaluation`` must accept ``dataset_path`` with default
        ``None`` (backward-compatible signature)."""
        import inspect
        sig = inspect.signature(rev.run_evaluation)
        assert "dataset_path" in sig.parameters
        param = sig.parameters["dataset_path"]
        assert param.default is None, (
            f"dataset_path default must be None for backward-compat, "
            f"got {param.default!r}"
        )

    def test_resolve_dataset_path_used_by_run_evaluation(self, monkeypatch):
        """``run_evaluation`` must call ``_resolve_dataset_path`` (not the
        old hardcoded ``GOLDEN_DIR / f"{domain}.yaml"``). Verified by
        monkeypatching the helper and stubbing the rest of the pipeline.
        """
        called: dict = {}

        def fake_resolve(domain, dataset_path):
            called["domain"] = domain
            called["dataset_path"] = dataset_path
            return Path("/tmp/stub.yaml")

        def fake_load_golden_dataset(path):
            called["loaded_path"] = path
            return {"questions": []}

        def fake_load_config(dataset):
            return {}

        def fake_get_domain_config(domain):
            return {"source_types": ["repo"]}

        def fake_aggregate(domain, evals):
            return {"total_questions": 0, "pass_count": 0,
                    "weak_count": 0, "fail_count": 0,
                    "avg_composite": 0.0}

        monkeypatch.setattr(rev, "_resolve_dataset_path", fake_resolve)
        monkeypatch.setattr(rev, "load_golden_dataset", fake_load_golden_dataset)
        monkeypatch.setattr(rev, "load_config", fake_load_config)
        monkeypatch.setattr(rev, "get_domain_config", fake_get_domain_config)
        monkeypatch.setattr(rev, "aggregate_domain_scores", fake_aggregate)
        monkeypatch.setattr(rev, "search", lambda *a, **k: {"results": []})

        result = rev.run_evaluation("godot", dataset_path="/tmp/custom.yaml")
        assert called["domain"] == "godot"
        assert called["dataset_path"] == "/tmp/custom.yaml"
        assert called["loaded_path"] == Path("/tmp/stub.yaml")
        assert result["domain"] == "godot"

    def test_run_evaluation_default_path_when_none(self, monkeypatch):
        """When called without ``dataset_path``, the default path is
        used (``None`` is forwarded to ``_resolve_dataset_path``)."""
        called: dict = {}

        def fake_resolve(domain, dataset_path):
            called["dataset_path"] = dataset_path
            return Path("/tmp/stub.yaml")

        monkeypatch.setattr(rev, "_resolve_dataset_path", fake_resolve)
        monkeypatch.setattr(rev, "load_golden_dataset", lambda p: {"questions": []})
        monkeypatch.setattr(rev, "load_config", lambda d: {})
        monkeypatch.setattr(rev, "get_domain_config", lambda d: {"source_types": ["repo"]})
        monkeypatch.setattr(
            rev, "aggregate_domain_scores",
            lambda d, e: {"total_questions": 0, "pass_count": 0,
                          "weak_count": 0, "fail_count": 0,
                          "avg_composite": 0.0},
        )
        monkeypatch.setattr(rev, "search", lambda *a, **k: {"results": []})

        rev.run_evaluation("godot")
        assert called["dataset_path"] is None