"""Unit tests for parser_base — Chunk dataclass, fallback_chunk,
markdown_section_chunk, and late_chunk (Phase 2.2)."""

import json
from unittest.mock import MagicMock

import numpy as np
import pytest

pytestmark = pytest.mark.unit

from parser_base import (
    Chunk,
    fallback_chunk,
    markdown_section_chunk,
    late_chunk,
    _split_into_chapters,
    _token_windows_from_offsets,
    _clean_chunk_text,
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


# ── Mock tokenizers for late-chunk tests (no real BGE-M3 download) ───────

class _OffsetSequence:
    """Mock for a single-sequence (batch-stripped) offset_mapping.

    The real BGE-M3 tokenizer's ``enc["offset_mapping"][0]`` returns a
    torch.Tensor of shape ``(seq_len, 2)`` whose ``.tolist()`` gives a
    list of ``[start, end]`` pairs. Our mock needs the same surface for
    ``late_chunk`` to call ``.tolist()`` on it.
    """

    def __init__(self, data):
        # data: list of [start, end] pairs (seq_len, 2)
        self._data = data

    def tolist(self):
        return self._data

    def __getitem__(self, idx):
        return self._data[idx]

    def to(self, device):  # for ``.to(device)`` no-op
        return self

    def __len__(self):
        return len(self._data)


class _OffsetTensor:
    """Mock for the batched ``offset_mapping`` returned by tokenizer.

    The real tokenizer returns shape ``(batch=1, seq_len, 2)``. Our mock
    supports ``[0]`` to drop the batch dim (returns ``_OffsetSequence``).
    ``.tolist()`` on the batched tensor returns ``[[seq1], [seq2], ...]``;
    we provide the same surface in case late_chunk calls it.
    """

    def __init__(self, sequences):
        # sequences: list of per-sequence offset lists
        self._sequences = sequences

    def tolist(self):
        return self._sequences

    def __getitem__(self, idx):
        return _OffsetSequence(self._sequences[idx])

    def to(self, device):
        return self

    def __len__(self):
        return len(self._sequences)


class _InputIdsTensor:
    """Mock for input_ids tensor: list of token ids, supports .to() and shape."""

    def __init__(self, ids):
        # ids: list of ints, batch=1 → 2D nested list [[id, id, ...]]
        self._data = [list(ids)]
        self.shape = (1, len(ids))

    def to(self, device):
        return self

    def __getitem__(self, idx):
        return self._data[idx]


class _WhitespaceTokenizer:
    """Tiny whitespace tokenizer that returns char-level offset_mapping.

    This mimics the structure of ``transformers.AutoTokenizer`` for
    `return_offsets_mapping=True`: returns a list of ``(start, end)``
    tuples aligned with each whitespace-separated token. Used to unit-test
    ``_token_windows_from_offsets`` and ``late_chunk`` without
    downloading a real model.
    """

    def __call__(self, text, return_offsets_mapping=True, **kw):
        tokens = text.split()
        offsets = []
        pos = 0
        # Whitespace split (preserves order, drops the whitespace).
        for tok in tokens:
            start = text.find(tok, pos)
            if start == -1:
                # Should not happen for our test inputs.
                continue
            end = start + len(tok)
            offsets.append((start, end))
            pos = end
        # Wrap in a structure that mimics tokenizer output. Real
        # tokenizers also return ``input_ids`` and ``attention_mask``;
        # late_chunk reads them in ``_LateChunkEncoder._encode_raw``
        # and calls ``.to(device)`` on them, so we provide compatible
        # mocks.
        class _Enc(dict):
            pass
        enc = _Enc()
        enc["offset_mapping"] = _OffsetTensor([offsets])  # batch dim
        enc["input_ids"] = _InputIdsTensor(range(len(tokens)))
        enc["attention_mask"] = _InputIdsTensor([1] * len(tokens))
        return enc


class _MockAutoModelOutput:
    """Mock for ``transformers.BaseModelOutputWithPooling``-like outputs.

    We only need ``last_hidden_state`` to have shape ``(batch, seq, dim)``
    and be indexable so ``outputs.last_hidden_state[0]`` gives a
    2-D tensor. We provide a numpy-backed array so the late_chunk
    mean-pooling works without torch.
    """

    def __init__(self, last_hidden_state):
        self.last_hidden_state = last_hidden_state


def _build_mock_model(vocab_size: int = 100, hidden_dim: int = 4):
    """Build a MagicMock that mimics ``SentenceTransformer`` for late_chunk.

    The mock is shaped just enough for ``_LateChunkEncoder._warmup`` and
    ``_encode_chapter_with_hidden_states`` to succeed:

    - ``model[0]`` is a Transformer-like module with ``tokenizer`` and
      ``auto_model`` attributes.
    - ``model[0].tokenizer(...)`` returns a dict with ``offset_mapping``,
      ``input_ids``, ``attention_mask`` (mocked tensors with the right
      surface).
    - ``model[0].auto_model(...)`` returns an object whose
      ``last_hidden_state`` is a torch.Tensor of shape
      ``(1, seq_len, hidden_dim)`` (constant value 1.0) so
      ``late_chunk`` can mean-pool and convert to numpy.
    - ``next(model[0].auto_model.parameters()).device`` is a string.

    This is a SMOKE test of the pipeline (chunk emission, metadata
    propagation, embedding dict shape) — not a semantic test of the
    embeddings themselves.
    """
    import torch

    model = MagicMock()
    # Make model[...] return a Transformer-like sub-mock.
    transformer = MagicMock()
    model.__getitem__ = MagicMock(return_value=transformer)

    # Tokenizer: whitespace-based, char-level offsets, plus mock
    # input_ids/attention_mask for ``model_in = {k: v.to(device) ...}``.
    transformer.tokenizer = _WhitespaceTokenizer()

    # auto_model.parameters() needs to return an iterator over objects
    # with a ``.device`` attribute (string). MagicMock handles this by
    # returning a MagicMock for ``.device``; we explicitly set it to a
    # plain string "cpu" so PyTorch code in _LateChunkEncoder accepts it.
    param_mock = MagicMock()
    param_mock.device = "cpu"
    transformer.auto_model.parameters.return_value = iter([param_mock])

    # auto_model(...) needs to return an object with last_hidden_state
    # as a torch.Tensor. We use side_effect to build a constant tensor
    # shaped (1, seq_len, hidden_dim).
    def _forward(**kwargs):
        input_ids = kwargs.get("input_ids")
        if hasattr(input_ids, "shape"):
            seq_len = int(input_ids.shape[-1])
        elif input_ids is not None and len(input_ids) > 0:
            seq_len = len(input_ids[0])
        else:
            seq_len = 1
        # torch.Tensor of shape (1, seq_len, hidden_dim), value 1.0
        arr = torch.ones((1, seq_len, hidden_dim), dtype=torch.float32)
        return _MockAutoModelOutput(arr)

    transformer.auto_model.side_effect = _forward

    return model


# ── TestLateChunk: Phase 2.2 Late Chunking ────────────────────────────────

class TestLateChunk:
    """Tests for late_chunk() and its helpers (Phase 2.2)."""

    # ── _split_into_chapters ─────────────────────────────────────────────

    # Test 1: empty text → empty list
    def test_split_into_chapters_empty(self):
        assert _split_into_chapters("") == []
        assert _split_into_chapters("   \n\n  ") == []

    # Test 2: no separators → 1 chapter
    def test_split_into_chapters_no_separators(self):
        text = "Just a long paragraph of text without any page separators."
        chapters = _split_into_chapters(text)
        assert len(chapters) == 1
        assert chapters[0][0] == text
        # No separators → pages default to (0, 0)
        assert chapters[0][1] == 0
        assert chapters[0][2] == 0

    # Test 3: single separator → 2 chapters
    def test_split_into_chapters_single_separator(self):
        text = "Page 1 content here.\n--- end of page=0 ---\nPage 2 content."
        chapters = _split_into_chapters(text)
        assert len(chapters) == 2
        # First chapter: the "Page 1" content, page 0 (0-based).
        assert chapters[0][1] == 0
        # Second chapter: starts with the page=0 separator (page 0) and
        # continues with "Page 2" content (page 1).
        assert chapters[1][1] == 0
        assert chapters[1][2] == 1

    # Test 4: multiple separators → N+1 chapters
    def test_split_into_chapters_multiple_separators(self):
        text = (
            "P0.\n--- end of page=0 ---\n"
            "P1.\n--- end of page=1 ---\n"
            "P2.\n--- end of page=2 ---\n"
            "P3.\n--- end of page=3 ---\n"
            "P4.\n--- end of page=4 ---\n"
            "P5."
        )
        chapters = _split_into_chapters(text)
        assert len(chapters) == 6
        # Chapter pages (0-based): each chapter spans from its content's
        # first page to the last page present in the chapter text.
        expected_pages = [(0, 0), (0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]
        for chapter, (exp_start, exp_end) in zip(chapters, expected_pages):
            assert (chapter[1], chapter[2]) == (exp_start, exp_end), (
                f"Expected pages {exp_start}-{exp_end} for chapter "
                f"starting with {chapter[0][:30]!r}, got {chapter[1]}-{chapter[2]}"
            )

    # Test 5: separator at start of text
    def test_split_into_chapters_separator_at_start(self):
        # Separator at position 0 → no "leading" chapter (it's empty).
        # First chapter begins at the separator and contains it.
        text = "--- end of page=0 ---\nPage 1 content here."
        chapters = _split_into_chapters(text)
        # The leading empty text before the first separator is skipped
        # (chapter_text.strip() is empty).
        assert len(chapters) == 1
        # The first real chapter starts with the page=0 separator, so
        # its page_start is 0 (the separator's page).
        assert chapters[0][1] == 0
        assert chapters[0][2] == 1

    # Test 6: consecutive separators → empty chapter skipped
    def test_split_into_chapters_consecutive_separators(self):
        text = (
            "P0.\n"
            "--- end of page=0 ---\n"
            "--- end of page=1 ---\n"   # empty chapter between sep 0 and sep 1
            "P2 content."
        )
        chapters = _split_into_chapters(text)
        # Should be 2 chapters: "P0." and "--- end of page=1 ---\nP2 content."
        # (The empty chapter between the two consecutive separators is skipped.)
        assert len(chapters) == 2
        assert "P0" in chapters[0][0]
        assert "P2" in chapters[1][0]
        # Second chapter: starts with the page=1 separator, contains
        # P2 (page 2). Page range: 1-2.
        assert chapters[1][1] == 1
        assert chapters[1][2] == 2

    # ── _token_windows_from_offsets: lossless property ───────────────────

    # Test 7: ASCII text — windows slice the original text losslessly
    def test_token_windows_lossless_ascii(self):
        # 9 whitespace-separated tokens. The whitespace tokenizer
        # returns one offset pair per token, so 9 offsets.
        text = "The quick brown fox jumps over the lazy dog"
        tok = _WhitespaceTokenizer()
        enc = tok(text, return_offsets_mapping=True)
        offsets = enc["offset_mapping"].tolist()[0]
        assert len(offsets) == 9  # 9 whitespace-separated tokens

        # No overlap → every token is in exactly one window.
        windows = _token_windows_from_offsets(
            text, offsets, window_size=4, overlap=0
        )
        # 9 tokens / 4 per window = 3 windows (4 + 4 + 1).
        assert len(windows) == 3

        # Each window's slice must equal the original text slice
        # (this is the lossless property at the per-window level).
        for w_text, c_start, c_end in windows:
            assert w_text == text[c_start:c_end], (
                f"Window {w_text!r} does not match text[{c_start}:{c_end}] "
                f"= {text[c_start:c_end]!r}"
            )

        # Union of window char ranges covers the full text length
        # (the whitespace gaps are not covered, which is expected).
        char_offsets = set()
        for _, s, e in windows:
            char_offsets.update(range(s, e))
        # Every character in any token's range must be covered.
        for s, e in offsets:
            for i in range(s, e):
                assert i in char_offsets, (
                    f"Character at position {i} not in any window"
                )

        # The last window must end at the last token's end.
        assert windows[-1][2] == offsets[-1][1]

    # Test 8: UTF-8 special characters — lossless with byte-slicing fallback
    def test_token_windows_lossless_utf8(self):
        # German umlauts, eszett, em-dash, curly quotes.
        # Use escape sequences for inner double quotes to keep the
        # outer string literal well-formed.
        text = (
            "Größe und übermäßige Höhe — äöü ß. "
            "\u201eAnführungszeichen\u201c und Em-Dashes — für Tests."
        )
        tok = _WhitespaceTokenizer()
        enc = tok(text, return_offsets_mapping=True)
        offsets = enc["offset_mapping"].tolist()[0]
        # Use overlap=0 for a clean round-trip of the JOINED windows.
        windows = _token_windows_from_offsets(
            text, offsets, window_size=4, overlap=0
        )
        assert len(windows) >= 1
        # Each window's slice must be the ORIGINAL text slice (char-based,
        # not byte-based) — verify by reading the text back.
        for w_text, c_start, c_end in windows:
            assert w_text == text[c_start:c_end], (
                f"Window text {w_text!r} does not match text[{c_start}:{c_end}] "
                f"= {text[c_start:c_end]!r} (UTF-8 char slicing broken?)"
            )
        # Union of window char ranges must cover the full text (modulo
        # whitespace gaps, which is expected because the tokenizer
        # skips whitespace tokens).
        covered_ranges = [(w[1], w[2]) for w in windows]
        # No window should be empty.
        for s, e in covered_ranges:
            assert s < e
        # The last window should reach the end of the text.
        assert covered_ranges[-1][1] == len(text)

    # ── _clean_chunk_text ────────────────────────────────────────────────

    # Test 9: page separators are removed
    def test_clean_chunk_text_removes_separators(self):
        text = (
            "Page 1 content.\n"
            "--- end of page=0 ---\n"
            "Page 2 content.\n"
            "--- end of page=1 ---\n"
            "Page 3 content."
        )
        cleaned = _clean_chunk_text(text)
        assert "--- end of page=" not in cleaned
        assert "Page 1 content." in cleaned
        assert "Page 2 content." in cleaned
        assert "Page 3 content." in cleaned
        # Whitespace is collapsed but newlines between paragraphs are kept.
        assert "\n\n" in cleaned or " " in cleaned

    # ── late_chunk: pipeline shape ───────────────────────────────────────

    # Test 10: late_chunk returns (chunks, embeddings_dict) — separate dict
    def test_late_chunk_returns_tuple(self):
        # Build a mock model that pretends to encode 4 tokens per call.
        model = _build_mock_model(hidden_dim=8)
        text = (
            "--- end of page=0 ---\n"
            "This is page 1 content about DaVinci Resolve video editing. "
            "It covers basic concepts and some advanced topics."
        )
        chunks, precomputed = late_chunk(
            text,
            domain="davinci_resolve",
            source_file="test.md",
            model=model,
            window_size=4,
            overlap=0,
        )
        # Must be a tuple
        assert isinstance(chunks, list)
        assert isinstance(precomputed, dict)
        # All chunks have a corresponding embedding (Hinweis 2: separate dict)
        for c in chunks:
            assert c.chunk_id in precomputed, (
                f"Chunk {c.chunk_id} has no precomputed embedding"
            )
            emb = precomputed[c.chunk_id]
            assert isinstance(emb, np.ndarray)
            # Hidden_dim from mock is 8.
            assert emb.shape == (8,)
        # Chunk has NO `.embedding` attribute — precomputed is a separate dict.
        for c in chunks:
            assert not hasattr(c, "embedding") or c.embedding is None

    # Test 11: chunk_type is "late_chunk"
    def test_late_chunk_type_is_late_chunk(self):
        model = _build_mock_model(hidden_dim=4)
        text = (
            "--- end of page=0 ---\n"
            "Some content about color grading in DaVinci Resolve Studio."
        )
        chunks, _ = late_chunk(
            text,
            domain="davinci_resolve",
            source_file="test.md",
            model=model,
            window_size=3,
            overlap=0,
        )
        assert len(chunks) >= 1
        for c in chunks:
            assert c.chunk_type == "late_chunk", (
                f"Expected chunk_type='late_chunk', got {c.chunk_type!r}"
            )

    # Test 12: source_type is "repo" (PDF sources live in sources/, not personal/)
    def test_late_chunk_source_type_is_repo(self):
        model = _build_mock_model(hidden_dim=4)
        text = (
            "--- end of page=0 ---\n"
            "Fusion is the compositing module in DaVinci Resolve."
        )
        chunks, _ = late_chunk(
            text,
            domain="davinci_resolve",
            source_file="fusion.md",
            model=model,
            window_size=3,
            overlap=0,
        )
        assert len(chunks) >= 1
        for c in chunks:
            assert c.source_type == "repo", (
                f"Expected source_type='repo', got {c.source_type!r}"
            )

    # Test 13: page_start / page_end populated from chapter (extracted BEFORE
    # page-separator cleanup)
    def test_late_chunk_page_metadata_before_cleanup(self):
        model = _build_mock_model(hidden_dim=4)
        # The text has a page separator at the START of chapter 1; the
        # cleaned chunk text should NOT contain "--- end of page=" but the
        # page_start/page_end metadata should still be set.
        text = (
            "--- end of page=0 ---\n"
            "Page 1 content that talks about video editing basics."
        )
        chunks, _ = late_chunk(
            text,
            domain="davinci_resolve",
            source_file="test.md",
            model=model,
            window_size=3,
            overlap=0,
        )
        assert len(chunks) >= 1
        for c in chunks:
            # Page metadata must be present (1-based, matching fallback_chunk)
            assert c.page_start is not None, "page_start missing"
            assert c.page_end is not None, "page_end missing"
            # The chunk text should be CLEANED (no separator present).
            assert "--- end of page=" not in c.text, (
                f"Chunk text still contains page separator: {c.text!r}"
            )
            # The page metadata is non-trivial (page 1 or higher in
            # 1-based convention for content after a page=0 separator).
            assert c.page_start >= 1
            assert c.page_end >= c.page_start

    # ── Additional structural tests ──────────────────────────────────────

    def test_late_chunk_empty_text_returns_empty(self):
        model = _build_mock_model()
        chunks, precomputed = late_chunk(
            "", domain="davinci_resolve", source_file="empty.md", model=model
        )
        assert chunks == []
        assert precomputed == {}

    def test_late_chunk_chunk_id_format(self):
        model = _build_mock_model(hidden_dim=4)
        text = (
            "--- end of page=0 ---\n"
            "Some meaningful content that produces at least one chunk."
        )
        chunks, _ = late_chunk(
            text,
            domain="davinci_resolve",
            source_file="manual.md",
            model=model,
            window_size=3,
            overlap=0,
        )
        assert len(chunks) >= 1
        for i, c in enumerate(chunks):
            # Format: <domain>::late_chunk::<filename>::<index>
            assert c.chunk_id == f"davinci_resolve::late_chunk::manual.md::{i}"
            assert c.chunk_id_in_file == i

    def test_late_chunk_source_file_set(self):
        model = _build_mock_model(hidden_dim=4)
        text = (
            "--- end of page=0 ---\n"
            "DaVinci Resolve content here for testing the source_file field."
        )
        chunks, _ = late_chunk(
            text,
            domain="davinci_resolve",
            source_file="davinci-resolve-20-beginners-guide.md",
            model=model,
            window_size=3,
            overlap=0,
        )
        assert len(chunks) >= 1
        for c in chunks:
            assert c.source_file == "davinci-resolve-20-beginners-guide.md"

    def test_late_chunk_domain_set(self):
        model = _build_mock_model(hidden_dim=4)
        text = (
            "--- end of page=0 ---\n"
            "Domain test content for verifying the domain field."
        )
        chunks, _ = late_chunk(
            text,
            domain="my_domain",
            source_file="x.md",
            model=model,
            window_size=3,
            overlap=0,
        )
        assert len(chunks) >= 1
        for c in chunks:
            assert c.domain == "my_domain"