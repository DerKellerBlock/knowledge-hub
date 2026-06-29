"""Unit tests for scorer.load_golden_dataset and scorer.validate_question.

These tests cover the YAML parsing/validation layer of the Quality
Evaluation Platform. They use ``tempfile`` for hermetic fixture files
and do NOT require a real ChromaDB/BM25 index.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterator
import tempfile

import pytest

from quality.scorer import load_golden_dataset, validate_question


# ── Fixtures ──────────────────────────────────────────────────────────────


@pytest.fixture
def tmp_yaml_path() -> Iterator[Path]:
    """Yield a fresh tempfile path; clean up the file after the test."""
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


VALID_YAML = """\
domain: godot
version: 1
description: "Golden Dataset for Godot"
last_updated: 2026-06-29
questions:
  - id: godot-001
    question: "How do I rotate a Node3D?"
    expected_source_files:
      - "godot-docs-packed.md"
    expected_page_ranges: []
    real_world_source_url: "https://forum.godotengine.org/t/12345"
    real_world_source_date: 2025-03-15
    difficulty: easy
    tags: [rotation, node3d]
    created_date: 2026-06-29
    last_verified: 2026-06-29
    notes: "Beginner question"
    min_top_k: 5
"""


# ── load_golden_dataset ───────────────────────────────────────────────────


def test_load_valid_yaml_returns_expected_keys(tmp_yaml_path):
    tmp_yaml_path.write_text(VALID_YAML, encoding="utf-8")
    data = load_golden_dataset(tmp_yaml_path)
    assert data["domain"] == "godot"
    assert data["version"] == 1
    assert isinstance(data["questions"], list)
    assert len(data["questions"]) == 1
    q = data["questions"][0]
    assert q["id"] == "godot-001"
    assert q["difficulty"] == "easy"


def test_load_missing_file_raises_filenotfound(tmp_path):
    missing = tmp_path / "does-not-exist.yaml"
    with pytest.raises(FileNotFoundError):
        load_golden_dataset(missing)


def test_load_invalid_yaml_raises_value_error_with_yaml_message(tmp_yaml_path):
    tmp_yaml_path.write_text("domain: godot\n  bad-indent: [unclosed\n", encoding="utf-8")
    with pytest.raises(ValueError, match=r"Invalid YAML"):
        load_golden_dataset(tmp_yaml_path)


def test_load_missing_domain_field_raises_value_error(tmp_yaml_path):
    tmp_yaml_path.write_text(
        "version: 1\nquestions: []\n", encoding="utf-8"
    )
    with pytest.raises(ValueError, match=r"domain"):
        load_golden_dataset(tmp_yaml_path)


def test_load_empty_yaml_file_raises_value_error(tmp_yaml_path):
    # YAML file with comments only — yaml.safe_load returns None
    tmp_yaml_path.write_text("# only a comment\n", encoding="utf-8")
    with pytest.raises(ValueError, match=r"Empty YAML file"):
        load_golden_dataset(tmp_yaml_path)


def test_load_missing_questions_defaults_to_empty_list(tmp_yaml_path):
    tmp_yaml_path.write_text("domain: godot\nversion: 1\n", encoding="utf-8")
    data = load_golden_dataset(tmp_yaml_path)
    assert data["questions"] == []


def test_load_applies_default_values(tmp_yaml_path):
    minimal = """\
domain: godot
version: 1
questions:
  - id: godot-002
    question: "Minimal question"
    expected_source_files: []
    difficulty: medium
    created_date: 2026-06-29
    last_verified: 2026-06-29
"""
    tmp_yaml_path.write_text(minimal, encoding="utf-8")
    data = load_golden_dataset(tmp_yaml_path)
    q = data["questions"][0]
    assert q["min_top_k"] == 10
    assert q["expected_page_ranges"] == []
    assert q["real_world_source_url"] is None
    assert q["real_world_source_date"] is None
    assert q["tags"] == []
    assert q["notes"] is None


# ── validate_question ─────────────────────────────────────────────────────


def test_validate_question_accepts_valid_question():
    q = {
        "id": "godot-001",
        "question": "How do I rotate a Node3D?",
        "expected_source_files": ["foo.md"],
        "difficulty": "easy",
        "created_date": "2026-06-29",
        "last_verified": "2026-06-29",
    }
    assert validate_question(q, "godot") == []


def test_validate_question_missing_id():
    q = {
        "question": "How do I rotate a Node3D?",
        "expected_source_files": ["foo.md"],
        "difficulty": "easy",
        "created_date": "2026-06-29",
        "last_verified": "2026-06-29",
    }
    errors = validate_question(q, "godot")
    assert any("id" in e for e in errors)


def test_validate_question_missing_question_text():
    q = {
        "id": "godot-001",
        "expected_source_files": ["foo.md"],
        "difficulty": "easy",
        "created_date": "2026-06-29",
        "last_verified": "2026-06-29",
    }
    errors = validate_question(q, "godot")
    assert any("question" in e for e in errors)


def test_validate_question_empty_question_text():
    q = {
        "id": "godot-001",
        "question": "",
        "expected_source_files": ["foo.md"],
        "difficulty": "easy",
        "created_date": "2026-06-29",
        "last_verified": "2026-06-29",
    }
    errors = validate_question(q, "godot")
    assert any("question" in e for e in errors)


def test_validate_question_invalid_difficulty():
    q = {
        "id": "godot-001",
        "question": "q",
        "expected_source_files": ["foo.md"],
        "difficulty": "super-easy",
        "created_date": "2026-06-29",
        "last_verified": "2026-06-29",
    }
    errors = validate_question(q, "godot")
    assert any("difficulty" in e.lower() for e in errors)


def test_validate_question_id_wrong_prefix():
    q = {
        "id": "unreal-001",
        "question": "q",
        "expected_source_files": ["foo.md"],
        "difficulty": "easy",
        "created_date": "2026-06-29",
        "last_verified": "2026-06-29",
    }
    errors = validate_question(q, "godot")
    assert any("unreal-001" in e and "godot-" in e for e in errors)


def test_validate_question_missing_expected_source_files():
    q = {
        "id": "godot-001",
        "question": "q",
        "difficulty": "easy",
        "created_date": "2026-06-29",
        "last_verified": "2026-06-29",
    }
    errors = validate_question(q, "godot")
    assert any("expected_source_files" in e for e in errors)


def test_validate_question_empty_expected_source_files_is_ok():
    q = {
        "id": "godot-001",
        "question": "q",
        "expected_source_files": [],
        "difficulty": "easy",
        "created_date": "2026-06-29",
        "last_verified": "2026-06-29",
    }
    # Empty expected_source_files is allowed (SR becomes N/A at scoring time)
    assert validate_question(q, "godot") == []


def test_validate_question_missing_dates():
    q = {
        "id": "godot-001",
        "question": "q",
        "expected_source_files": ["foo.md"],
        "difficulty": "easy",
    }
    errors = validate_question(q, "godot")
    assert any("created_date" in e for e in errors)
    assert any("last_verified" in e for e in errors)
