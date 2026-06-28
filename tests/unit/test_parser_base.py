"""Unit tests for parser_base — Chunk dataclass and fallback_chunk."""

import json

import pytest

pytestmark = pytest.mark.unit

from parser_base import Chunk, fallback_chunk, FALLBACK_CHUNK_CHARS, FALLBACK_OVERLAP_CHARS


class TestChunkToMetadata:
    def test_basic_fields_present(self):
        c = Chunk(
            chunk_id="test::1",
            domain="test",
            text="hello",
            source_type="repo",
            source_file="file.md",
            line_start=10,
            line_end=20,
        )
        meta = c.to_chromadb_metadata()
        assert meta["source_type"] == "repo"
        assert meta["domain"] == "test"
        assert meta["source_file"] == "file.md"
        assert meta["line_start"] == 10
        assert meta["line_end"] == 20
        assert meta["chunk_id_in_file"] == 0

    def test_none_fields_omitted(self):
        c = Chunk(
            chunk_id="test::1",
            domain="test",
            text="hello",
            source_type="repo",
        )
        meta = c.to_chromadb_metadata()
        assert "chunk_type" not in meta
        assert "class_name" not in meta
        assert "name" not in meta
        assert "signature" not in meta
        assert "inherits_from" not in meta
        assert "docstring" not in meta

    def test_inherits_from_serialized_as_json(self):
        c = Chunk(
            chunk_id="test::1",
            domain="test",
            text="hello",
            source_type="repo",
            inherits_from=["Node", "Node3D"],
        )
        meta = c.to_chromadb_metadata()
        assert meta["inherits_from"] == '["Node", "Node3D"]'
        assert isinstance(meta["inherits_from"], str)

    def test_docstring_truncated(self):
        long_doc = "x" * 1000
        c = Chunk(
            chunk_id="test::1",
            domain="test",
            text="hello",
            source_type="repo",
            docstring=long_doc,
        )
        meta = c.to_chromadb_metadata()
        assert len(meta["docstring"]) == 500


class TestChunkFromMetadata:
    def test_round_trip(self):
        c = Chunk(
            chunk_id="test::1",
            domain="test",
            text="hello world",
            source_type="repo",
            source_file="file.md",
            line_start=5,
            line_end=15,
            chunk_type="method",
            class_name="Node3D",
            name="rotate_y",
            signature="void rotate_y(angle: float)",
            inherits_from=["Node"],
            docstring="Rotates on Y axis",
        )
        meta = c.to_chromadb_metadata()
        restored = Chunk.from_chromadb_metadata("test::1", "hello world", meta)
        assert restored.chunk_id == "test::1"
        assert restored.text == "hello world"
        assert restored.source_type == "repo"
        assert restored.source_file == "file.md"
        assert restored.line_start == 5
        assert restored.line_end == 15
        assert restored.chunk_type == "method"
        assert restored.class_name == "Node3D"
        assert restored.name == "rotate_y"
        assert restored.signature == "void rotate_y(angle: float)"
        assert restored.inherits_from == ["Node"]
        assert restored.docstring == "Rotates on Y axis"

    def test_from_metadata_no_optional_fields(self):
        meta = {
            "source_type": "repo",
            "domain": "test",
            "source_file": "f.md",
            "line_start": 0,
            "line_end": 0,
            "chunk_id_in_file": 0,
        }
        c = Chunk.from_chromadb_metadata("id", "text", meta)
        assert c.chunk_type is None
        assert c.class_name is None
        assert c.name is None
        assert c.inherits_from is None


class TestFallbackChunk:
    def test_empty_text_returns_empty_list(self):
        result = fallback_chunk("", domain="test", source_type="repo", source_file="f.md")
        assert result == []

    def test_short_text_single_chunk(self):
        text = "short text"
        result = fallback_chunk(text, domain="test", source_type="repo", source_file="f.md")
        assert len(result) == 1
        assert result[0].text == text
        assert result[0].domain == "test"
        assert result[0].source_file == "f.md"
        assert result[0].chunk_id == "test::fallback::0"

    def test_long_text_multiple_chunks(self):
        # Use small chunk_size to produce multiple chunks without huge text
        text = "A" * 250
        result = fallback_chunk(
            text, domain="test", source_type="repo", source_file="f.md",
            chunk_size=100, overlap=20,
        )
        # step = chunk_size - overlap = 80; starts: 0, 80, 160, 240 (all < 250) → 4 chunks
        assert len(result) == 4
        assert result[0].chunk_id == "test::fallback::0"
        assert result[1].chunk_id == "test::fallback::1"
        assert result[2].chunk_id == "test::fallback::2"
        assert result[3].chunk_id == "test::fallback::3"

    def test_chunk_line_numbers_increment(self):
        text = "line1\nline2\nline3\nline4\nline5"
        result = fallback_chunk(
            text, domain="test", source_type="repo", source_file="f.md",
            chunk_size=100, overlap=20,
        )
        # each chunk should have line_start <= line_end
        for c in result:
            assert c.line_start >= 1
            assert c.line_end >= c.line_start

    def test_chunk_id_in_file_increments(self):
        text = "A" * 250
        result = fallback_chunk(
            text, domain="test", source_type="repo", source_file="f.md",
            chunk_size=100, overlap=20,
        )
        for i, c in enumerate(result):
            assert c.chunk_id_in_file == i

    def test_default_chunk_and_overlap_constants(self):
        assert FALLBACK_CHUNK_CHARS == 8000
        assert FALLBACK_OVERLAP_CHARS == 800