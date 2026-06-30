"""Unit tests for parser_base — Chunk dataclass and fallback_chunk."""

import json

import pytest

pytestmark = pytest.mark.unit

from parser_base import (
    Chunk,
    fallback_chunk,
    markdown_section_chunk,
    FALLBACK_CHUNK_CHARS,
    FALLBACK_OVERLAP_CHARS,
)


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
        assert FALLBACK_OVERLAP_CHARS == 1600


class TestMarkdownSectionChunk:
    """Tests for markdown_section_chunk() — per-section chunking for personal notes."""

    # ── Test 1: Basic section splitting ─────────────────────────────────
    def test_file_with_headers_produces_section_chunks(self):
        text = (
            "# Title\n"
            "\n"
            "Preamble paragraph that is long enough to be indexed.\n"
            "\n"
            "## First section\n"
            "Content of first section goes here and is long enough.\n"
            "\n"
            "## Second section\n"
            "Content of second section goes here and is also long enough.\n"
        )
        chunks = markdown_section_chunk(
            text, domain="test", source_type="personal",
            source_file="notes.md", category="notes",
        )
        # 1 preamble + 2 sections
        assert len(chunks) == 3
        assert chunks[0].chunk_type is None  # preamble
        assert chunks[1].chunk_type == "personal_section"
        assert chunks[2].chunk_type == "personal_section"

    # ── Test 2: Fallback if no `## ` header (Pflicht-Test Blind-Spot) ───
    def test_file_without_headers_falls_back(self):
        text = "Just a plain paragraph without any markdown headers at all.\n" * 20
        chunks = markdown_section_chunk(
            text, domain="test", source_type="personal",
            source_file="plain.md", category="plain",
        )
        # fallback_chunk is called → returns sliding-window chunks with
        # chunk_id prefix "test::fallback::..."
        assert len(chunks) >= 1
        assert all(c.chunk_id.startswith("test::fallback::") for c in chunks)
        # No personal_section chunk_type should be present
        assert all(c.chunk_type != "personal_section" for c in chunks)

    # ── Test 3: Empty preamble is skipped (Pflicht-Test Blind-Spot) ─────
    def test_preamble_empty_is_skipped(self):
        # File starts directly with `## ` → no preamble
        text = (
            "## Section One\n"
            "Content of section one that is definitely long enough.\n"
        )
        chunks = markdown_section_chunk(
            text, domain="test", source_type="personal",
            source_file="notes.md", category="notes",
        )
        assert len(chunks) == 1
        assert chunks[0].chunk_type == "personal_section"
        assert chunks[0].name == "Section One"

    # ── Test 4: Short preamble is skipped (defensive Skip) ──────────────
    def test_preamble_short_is_skipped(self):
        text = (
            "# Title\n"
            "short\n"  # < 50 chars after strip
            "## First section\n"
            "Content of first section that is definitely long enough.\n"
        )
        chunks = markdown_section_chunk(
            text, domain="test", source_type="personal",
            source_file="notes.md", category="notes",
        )
        # preamble skipped (too short), only 1 section
        assert len(chunks) == 1
        assert chunks[0].chunk_type == "personal_section"
        assert chunks[0].name == "First section"

    # ── Test 5: Short section is skipped (defensive Skip) ──────────────
    def test_section_short_is_skipped(self):
        text = (
            "## Good section\n"
            "This section has enough content to be indexed properly.\n"
            "\n"
            "## TODO\n"  # very short, only contains a placeholder
            "TODO\n"
            "\n"
            "## Another good section\n"
            "Another section with enough content for the index.\n"
        )
        chunks = markdown_section_chunk(
            text, domain="test", source_type="personal",
            source_file="notes.md", category="notes",
        )
        # Middle "## TODO" section skipped (< 50 chars after strip)
        names = [c.name for c in chunks]
        assert "Good section" in names
        assert "Another good section" in names
        assert "TODO" not in names
        assert len(chunks) == 2

    # ── Test 6: Section name extracted (without `## ` prefix) ──────────
    def test_section_name_extracted(self):
        text = (
            "## Jolt Physics + CharacterBody3D\n"
            "Body text that is long enough to be indexed properly.\n"
        )
        chunks = markdown_section_chunk(
            text, domain="test", source_type="personal",
            source_file="gotchas.md", category="gotchas",
        )
        assert len(chunks) == 1
        assert chunks[0].name == "Jolt Physics + CharacterBody3D"

    # ── Test 7: chunk_type is "personal_section" ────────────────────────
    def test_chunk_type_is_personal_section(self):
        text = (
            "## Heading\n"
            "Body content that is long enough to be indexed properly.\n"
        )
        chunks = markdown_section_chunk(
            text, domain="test", source_type="personal",
            source_file="notes.md", category="notes",
        )
        assert chunks[0].chunk_type == "personal_section"

    # ── Test 8: line_start / line_end correct ───────────────────────────
    def test_line_numbers_correct(self):
        # Note: section bodies must be >= 50 chars after .strip() or the
        # defensive skip kicks in. Build sections deliberately long.
        text = (
            "# Title\n"                            # line 1
            "\n"                                   # line 2
            "Preamble paragraph that is long enough to be kept by the indexer.\n"  # line 3
            "\n"                                   # line 4
            "## Section A\n"                       # line 5
            "Body A content that is long enough to be indexed properly.\n"  # line 6
            "More body A content spread over multiple lines.\n"  # line 7
            "\n"                                   # line 8
            "## Section B\n"                       # line 9
            "Body B content that is long enough to be indexed properly.\n"  # line 10
            "More body B content spread over multiple lines.\n"  # line 11
        )
        chunks = markdown_section_chunk(
            text, domain="test", source_type="personal",
            source_file="notes.md", category="notes",
        )
        assert len(chunks) == 3
        # Preamble: lines 1-4
        assert chunks[0].line_start == 1
        # Section A starts at line 5
        assert chunks[1].line_start == 5
        assert chunks[1].line_end >= chunks[1].line_start
        # Section B starts at line 9
        assert chunks[2].line_start == 9
        assert chunks[2].line_end >= chunks[2].line_start

    # ── Test 9: Large section falls back to fallback_chunk ─────────────
    def test_large_section_falls_back_to_sliding_window(self):
        # Build a single `## ` section that exceeds max_section_chars
        big_body = "x" * 200
        text = (
            "## Huge section\n"
            + big_body + "\n"
            + "## Small section\n"
            + "Small section content that is long enough.\n"
        )
        chunks = markdown_section_chunk(
            text, domain="test", source_type="personal",
            source_file="notes.md", category="notes",
            max_section_chars=100,  # tiny threshold to force sub-chunking
        )
        # The huge section is split into multiple sub-chunks by
        # fallback_chunk; the small section remains one chunk.
        assert len(chunks) >= 2
        # All chunks must preserve the chunk_id_in_file sequence
        for i, c in enumerate(chunks):
            assert c.chunk_id_in_file == i
            assert c.source_type == "personal"
        # At least one chunk must come from the huge section
        assert any(c.text.startswith("## Huge section") for c in chunks)

    # ── Test 10: source_type preserved as "personal" ────────────────────
    def test_source_type_preserved(self):
        text = (
            "## A\n"
            "Content of A that is long enough.\n"
            "\n"
            "## B\n"
            "Content of B that is also long enough.\n"
        )
        chunks = markdown_section_chunk(
            text, domain="test", source_type="personal",
            source_file="notes.md", category="notes",
        )
        assert all(c.source_type == "personal" for c in chunks)

    # ── Test 11: chunk_id_in_file increments from 0 ────────────────────
    def test_chunk_id_in_file_increments(self):
        # Note: section bodies must be >= 50 chars after .strip() or the
        # defensive skip kicks in.
        text = (
            "Preamble line one that is long enough to be kept by the indexer.\n"
            "\n"
            "## A\n"
            "Content of A that is long enough for the indexer to keep it.\n"
            "\n"
            "## B\n"
            "Content of B that is long enough for the indexer to keep it.\n"
            "\n"
            "## C\n"
            "Content of C that is long enough for the indexer to keep it.\n"
        )
        chunks = markdown_section_chunk(
            text, domain="test", source_type="personal",
            source_file="notes.md", category="notes",
        )
        # preamble + 3 sections = 4 chunks
        assert len(chunks) == 4
        for i, c in enumerate(chunks):
            assert c.chunk_id_in_file == i
            assert c.chunk_id == f"test::personal::notes::{i}"

    # ── Test 12: gotchas.md real content splits into sections ──────────
    def test_gotchas_md_real_content(self):
        from pathlib import Path
        gotchas_path = Path(__file__).resolve().parents[2] / "domains" / "godot" / "personal" / "gotchas.md"
        if not gotchas_path.exists():
            pytest.skip("gotchas.md not present in repo")
        text = gotchas_path.read_text(encoding="utf-8")
        chunks = markdown_section_chunk(
            text, domain="godot", source_type="personal",
            source_file="gotchas.md", category="gotchas",
        )
        # 1 preamble + 7 `## ` sections = 8 chunks
        assert len(chunks) == 8
        # The 7 sections should have their headings as `name`
        section_names = [c.name for c in chunks if c.chunk_type == "personal_section"]
        assert "GLB-Import Scale mit Meshy" in section_names
        assert "Jolt Physics + CharacterBody3D" in section_names
        # The preamble has chunk_type None and name None
        preamble = chunks[0]
        assert preamble.chunk_type is None
        assert preamble.name is None

    # ── Test 13: `### ` (level-3) is NOT treated as a split point ──────
    def test_h3_headers_not_split(self):
        text = (
            "## Top section\n"
            "Intro paragraph for the top section, long enough.\n"
            "\n"
            "### Sub heading\n"
            "Content under sub heading.\n"
            "\n"
            "More body content under sub heading, definitely long enough.\n"
            "\n"
            "## Next section\n"
            "Content of next section, definitely long enough.\n"
        )
        chunks = markdown_section_chunk(
            text, domain="test", source_type="personal",
            source_file="notes.md", category="notes",
        )
        # Only 2 chunks: `## Top section` (containing `### Sub heading`)
        # and `## Next section`. The `### Sub heading` does NOT split.
        assert len(chunks) == 2
        assert chunks[0].name == "Top section"
        assert chunks[1].name == "Next section"
        # The level-3 header text must still appear in the first chunk's text
        assert "### Sub heading" in chunks[0].text