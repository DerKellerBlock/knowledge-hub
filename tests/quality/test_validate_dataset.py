"""Unit tests for the Golden Dataset validation CLI.

Covers pure functions ``validate_url`` and ``check_secrets``, plus the
high-level ``validate_dataset`` integration. Tests do NOT require a
real ChromaDB/BM25 index — they use tempfiles for fixtures.
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Iterator

import pytest

from quality.validate_dataset import (
    check_secrets,
    validate_dataset,
    validate_url,
)


# ── Fixtures ──────────────────────────────────────────────────────────────


@pytest.fixture
def tmp_yaml_path() -> Iterator[Path]:
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".yaml", delete=False, encoding="utf-8"
    )
    tmp.close()
    path = Path(tmp.name)
    try:
        yield path
    finally:
        if path.exists():
            path.unlink()


VALID_GODOT_YAML = """\
domain: godot
version: 1
description: "Test"
last_updated: 2026-06-29
questions:
  - id: godot-001
    question: "How do I rotate a Node3D?"
    expected_source_files:
      - "godot-docs-reference-packed.md"
    expected_page_ranges: []
    real_world_source_url: null
    real_world_source_date: null
    difficulty: easy
    tags: [rotation]
    created_date: 2026-06-29
    last_verified: 2026-06-29
    notes: "Test"
    min_top_k: 10
"""


@pytest.fixture
def write_godot_golden(tmp_yaml_path) -> Path:
    """Write a valid Godot Golden Dataset and yield the path.

    Uses tmp_yaml_path fixture (a real tempfile outside the repo) so
    we don't touch quality/golden/godot.yaml.
    """
    tmp_yaml_path.write_text(VALID_GODOT_YAML, encoding="utf-8")
    return tmp_yaml_path


# ── validate_url ──────────────────────────────────────────────────────────


class TestValidateUrl:
    def test_accepts_https(self):
        assert validate_url("https://example.com/article") == []

    def test_accepts_http(self):
        assert validate_url("http://example.com/article") == []

    def test_accepts_https_with_query(self):
        assert validate_url("https://example.com/?q=test&page=2") == []

    def test_rejects_file_scheme(self):
        errors = validate_url("file:///etc/passwd")
        assert len(errors) == 1
        assert "scheme" in errors[0].lower()

    def test_rejects_ftp_scheme(self):
        errors = validate_url("ftp://example.com/file")
        assert any("scheme" in e.lower() for e in errors)

    def test_rejects_data_scheme(self):
        errors = validate_url("data:text/plain,hello")
        assert any("scheme" in e.lower() for e in errors)

    def test_rejects_localhost(self):
        errors = validate_url("http://localhost:8080/x")
        assert any("localhost" in e for e in errors)

    def test_rejects_127_0_0_1(self):
        errors = validate_url("http://127.0.0.1/x")
        assert any("loopback" in e.lower() or "127" in e for e in errors)

    def test_rejects_ipv6_loopback(self):
        errors = validate_url("http://[::1]/x")
        assert any("loopback" in e.lower() or "::1" in e for e in errors)

    def test_rejects_private_10_dot(self):
        errors = validate_url("http://10.0.0.1/x")
        assert any("private" in e.lower() for e in errors)

    def test_rejects_private_192_168(self):
        errors = validate_url("http://192.168.1.1/x")
        assert any("private" in e.lower() for e in errors)

    def test_rejects_private_172_16(self):
        errors = validate_url("http://172.16.0.1/x")
        assert any("private" in e.lower() for e in errors)

    def test_rejects_private_172_31(self):
        errors = validate_url("http://172.31.255.255/x")
        assert any("private" in e.lower() for e in errors)

    def test_accepts_none(self):
        assert validate_url(None) == []

    def test_accepts_empty_string(self):
        assert validate_url("") == []

    def test_rejects_empty_host(self):
        errors = validate_url("http:///path")
        # Either no-host error or scheme error acceptable
        assert len(errors) >= 1


# ── check_secrets ─────────────────────────────────────────────────────────


class TestCheckSecrets:
    def test_detects_api_key_assignment(self):
        text = "Use api_key=abcdefghijklmnopqrstuvwxyz123456 in your config"
        warnings = check_secrets(text)
        assert len(warnings) >= 1

    def test_detects_password_assignment(self):
        text = "password=thisismyverystrongpassword123"
        warnings = check_secrets(text)
        assert len(warnings) >= 1

    def test_detects_token_assignment(self):
        text = "auth_token=ABCDEFGHIJKLMNOPQRSTUVWXYZ123456"
        warnings = check_secrets(text)
        assert len(warnings) >= 1

    def test_detects_openai_sk_prefix(self):
        text = "OPENAI_KEY=sk-abcdefghijklmnopqrstuvwxyz1234"
        warnings = check_secrets(text)
        assert len(warnings) >= 1

    def test_detects_github_ghp_prefix(self):
        text = "Set GITHUB_TOKEN=ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ1234"
        warnings = check_secrets(text)
        assert len(warnings) >= 1

    def test_no_false_positive_on_normal_text(self):
        text = "How do I rotate a Node3D around the Y axis in GDScript?"
        assert check_secrets(text) == []

    def test_no_false_positive_on_question_about_api_keys(self):
        # Mentions "API key" but has no actual key value following.
        text = "How do I configure an API key in my project settings?"
        # This is a legitimate question; should be safe.
        assert check_secrets(text) == []

    def test_accepts_none(self):
        assert check_secrets(None) == []

    def test_accepts_empty_string(self):
        assert check_secrets("") == []


# ── validate_dataset integration ─────────────────────────────────────────


class TestValidateDataset:
    def test_valid_dataset_no_errors(self, write_godot_golden, monkeypatch):
        # We need to patch GOLDEN_DIR in validate_dataset to point at
        # our tempfile. Importing here to avoid collection-time import.
        from quality import validate_dataset as vd

        monkeypatch.setattr(vd, "GOLDEN_DIR", write_godot_golden.parent)
        # Also rename the file in that tempdir to godot.yaml
        target = write_godot_golden.parent / "godot.yaml"
        target.write_text(write_godot_golden.read_text(encoding="utf-8"), encoding="utf-8")
        try:
            errors, warnings = vd.validate_dataset("godot")
            assert errors == [], f"Unexpected errors: {errors}"
        finally:
            if target.exists():
                target.unlink()

    def test_invalid_question_missing_field_reports_error(
        self, write_godot_golden, monkeypatch
    ):
        from quality import validate_dataset as vd

        # Write a YAML with a question that is missing 'difficulty'.
        bad_yaml = """\
domain: godot
version: 1
questions:
  - id: godot-001
    question: "Q"
    expected_source_files: []
    created_date: 2026-06-29
    last_verified: 2026-06-29
"""
        target = write_godot_golden.parent / "godot.yaml"
        target.write_text(bad_yaml, encoding="utf-8")
        monkeypatch.setattr(vd, "GOLDEN_DIR", write_godot_golden.parent)
        try:
            errors, warnings = vd.validate_dataset("godot")
            assert any("difficulty" in e for e in errors)
        finally:
            if target.exists():
                target.unlink()

    def test_secret_in_question_text_is_warning_not_error(
        self, write_godot_golden, monkeypatch
    ):
        from quality import validate_dataset as vd

        # Question text contains a fake secret.
        bad_yaml = """\
domain: godot
version: 1
questions:
  - id: godot-001
    question: "I set api_key=abcdefghijklmnopqrstuvwxyz1234 but it doesn't work"
    expected_source_files: []
    difficulty: easy
    created_date: 2026-06-29
    last_verified: 2026-06-29
"""
        target = write_godot_golden.parent / "godot.yaml"
        target.write_text(bad_yaml, encoding="utf-8")
        monkeypatch.setattr(vd, "GOLDEN_DIR", write_godot_golden.parent)
        try:
            errors, warnings = vd.validate_dataset("godot")
            # No structure errors (all required fields present)
            assert errors == [], f"Unexpected errors: {errors}"
            # But we should have at least one warning
            assert any("secret" in w.lower() for w in warnings)
        finally:
            if target.exists():
                target.unlink()

    def test_check_sources_finds_existing_files(
        self, write_godot_golden, monkeypatch
    ):
        """When --check-sources is enabled, existing files in sources/
        or personal/ should NOT produce errors."""
        from quality import validate_dataset as vd

        # Patch the domain directories to point at a tmp tree.
        import tempfile as _tf
        with _tf.TemporaryDirectory() as tmp_domains_str:
            tmp_domains = Path(tmp_domains_str)
            (tmp_domains / "godot" / "sources").mkdir(parents=True)
            (tmp_domains / "godot" / "sources" / "godot-docs-reference-packed.md").write_text(
                "fake", encoding="utf-8"
            )
            monkeypatch.setattr(vd, "DOMAINS_DIR", tmp_domains)

            target = write_godot_golden.parent / "godot.yaml"
            target.write_text(write_godot_golden.read_text(encoding="utf-8"), encoding="utf-8")
            monkeypatch.setattr(vd, "GOLDEN_DIR", write_godot_golden.parent)
            try:
                errors, warnings = vd.validate_dataset(
                    "godot", check_sources=True
                )
                assert errors == [], f"Unexpected errors: {errors}"
            finally:
                if target.exists():
                    target.unlink()

    def test_check_sources_flags_missing_file(
        self, write_godot_golden, monkeypatch
    ):
        """When --check-sources is enabled and a file is missing, error."""
        from quality import validate_dataset as vd

        import tempfile as _tf
        with _tf.TemporaryDirectory() as tmp_domains_str:
            tmp_domains = Path(tmp_domains_str)
            (tmp_domains / "godot" / "sources").mkdir(parents=True)
            # No files inside sources/ — godot-docs-reference-packed.md is missing
            monkeypatch.setattr(vd, "DOMAINS_DIR", tmp_domains)

            target = write_godot_golden.parent / "godot.yaml"
            target.write_text(write_godot_golden.read_text(encoding="utf-8"), encoding="utf-8")
            monkeypatch.setattr(vd, "GOLDEN_DIR", write_godot_golden.parent)
            try:
                errors, warnings = vd.validate_dataset(
                    "godot", check_sources=True
                )
                assert any("not found" in e for e in errors)
            finally:
                if target.exists():
                    target.unlink()

    def test_strict_urls_promotes_warnings_to_errors(
        self, write_godot_golden, monkeypatch
    ):
        from quality import validate_dataset as vd

        bad_yaml = """\
domain: godot
version: 1
questions:
  - id: godot-001
    question: "Q"
    expected_source_files: []
    difficulty: easy
    real_world_source_url: "http://localhost:8080/x"
    created_date: 2026-06-29
    last_verified: 2026-06-29
"""
        target = write_godot_golden.parent / "godot.yaml"
        target.write_text(bad_yaml, encoding="utf-8")
        monkeypatch.setattr(vd, "GOLDEN_DIR", write_godot_golden.parent)
        try:
            # Non-strict: localhost URL is only a warning
            errors_loose, warnings_loose = vd.validate_dataset("godot", strict_urls=False)
            assert errors_loose == []
            assert any("localhost" in w for w in warnings_loose)

            # Strict: localhost URL is an error
            errors_strict, warnings_strict = vd.validate_dataset("godot", strict_urls=True)
            assert any("localhost" in e for e in errors_strict)
        finally:
            if target.exists():
                target.unlink()


# ── Real-World Sources validation ──────────────────────────────────────────


class TestRealWorldSourcesValidation:
    def test_validate_dataset_warns_unknown_rws_type(
        self, write_godot_golden, monkeypatch
    ):
        """Blind-Spot-Fix #3: unknown ``type`` is a warning, not an error —
        validate_question's signature stays unchanged."""
        from quality import validate_dataset as vd

        bad_yaml = """\
domain: godot
version: 1
questions:
  - id: godot-001
    question: "Q"
    expected_source_files: []
    difficulty: easy
    created_date: 2026-06-29
    last_verified: 2026-06-29
    real_world_sources:
      - url: "https://example.com/a"
        date: null
        type: "invalid-type"
        solution_summary: null
        has_solution: true
"""
        target = write_godot_golden.parent / "godot.yaml"
        target.write_text(bad_yaml, encoding="utf-8")
        monkeypatch.setattr(vd, "GOLDEN_DIR", write_godot_golden.parent)
        try:
            errors, warnings = vd.validate_dataset("godot")
            assert errors == [], f"Unexpected errors: {errors}"
            assert any("invalid-type" in w and "type" in w.lower() for w in warnings)
        finally:
            if target.exists():
                target.unlink()

    def test_validate_dataset_deprecated_real_world_source_url_warning(
        self, write_godot_golden, monkeypatch
    ):
        """Blind-Spot-Fix #11: using the legacy ``real_world_source_url``
        field produces a deprecation warning."""
        from quality import validate_dataset as vd

        yaml_text = """\
domain: godot
version: 1
questions:
  - id: godot-001
    question: "Q"
    expected_source_files: []
    difficulty: easy
    created_date: 2026-06-29
    last_verified: 2026-06-29
    real_world_source_url: "https://example.com/legacy"
    real_world_source_date: null
"""
        target = write_godot_golden.parent / "godot.yaml"
        target.write_text(yaml_text, encoding="utf-8")
        monkeypatch.setattr(vd, "GOLDEN_DIR", write_godot_golden.parent)
        try:
            errors, warnings = vd.validate_dataset("godot")
            assert errors == [], f"Unexpected errors: {errors}"
            assert any("deprecated" in w and "real_world_sources" in w for w in warnings)
        finally:
            if target.exists():
                target.unlink()

    def test_validate_dataset_validates_rws_urls_with_strict(
        self, write_godot_golden, monkeypatch
    ):
        """Blind-Spot-Fix #4: each URL inside ``real_world_sources`` is
        validated through the existing ``--strict-urls`` path. A
        ``file://`` URL in the list is fatal under ``--strict-urls``."""
        from quality import validate_dataset as vd

        bad_yaml = """\
domain: godot
version: 1
questions:
  - id: godot-001
    question: "Q"
    expected_source_files: []
    difficulty: easy
    created_date: 2026-06-29
    last_verified: 2026-06-29
    real_world_sources:
      - url: "file:///etc/passwd"
        date: null
        type: "other"
        solution_summary: null
        has_solution: false
"""
        target = write_godot_golden.parent / "godot.yaml"
        target.write_text(bad_yaml, encoding="utf-8")
        monkeypatch.setattr(vd, "GOLDEN_DIR", write_godot_golden.parent)
        try:
            # Non-strict: warning
            errors_loose, warnings_loose = vd.validate_dataset(
                "godot", strict_urls=False
            )
            assert errors_loose == []
            assert any("real_world_sources URL" in w and "scheme" in w for w in warnings_loose)

            # Strict: error
            errors_strict, _ = vd.validate_dataset("godot", strict_urls=True)
            assert any("real_world_sources URL" in e and "scheme" in e for e in errors_strict)
        finally:
            if target.exists():
                target.unlink()
