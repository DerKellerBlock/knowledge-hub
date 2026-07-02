#!/usr/bin/env python3
"""
Plugin system for domain-specific structured parsing.

Defines the Chunk dataclass (unified schema for all chunks) and the
DomainParser abstract base class. Domains MAY provide a parser.py that
subclasses DomainParser. If no parser exists, fallback_chunk() is used.

Phase 2.2: late_chunk() implements chapter-wise late chunking for PDF
sources (DaVinci Resolve), producing token-level embeddings that span
chapter boundaries instead of arbitrary character positions.
"""

import json
import re
import warnings
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Chunk:
    """Unified chunk schema for indexing, search, and reranking.

    Pflichtfelder (immer befüllt):
        chunk_id, domain, text, source_type, source_file, line_start, line_end

    Struktur-Felder (None bei Fallback-Chunking):
        chunk_type, class_name, name, signature, inherits_from, docstring
    """

    # Pflichtfelder
    chunk_id: str
    domain: str
    text: str
    source_type: str  # "repo" | "personal"

    # Struktur-Felder (optional)
    chunk_type: str | None = None       # "class" | "method" | "operator" | "constructor" | "property" | "signal" | "enum" | "constant" | "annotation" | "theme_property" | "section"
    class_name: str | None = None       # z.B. "Node3D"
    name: str | None = None             # Methoden-/Property-Name, z.B. "rotate_y"
    signature: str | None = None        # "void rotate_y(angle: float)"
    inherits_from: list[str] | None = None  # ["Node"]
    docstring: str | None = None        # Beschreibungstext

    # Position
    source_file: str = ""
    line_start: int = 0
    line_end: int = 0
    page_start: int | None = None      # PDF page number (1-based), set by fallback_chunk if page separators present
    page_end: int | None = None        # PDF page number (1-based), set by fallback_chunk if page separators present

    # Intern (wird von embed_index.py gesetzt)
    chunk_id_in_file: int = 0

    def to_chromadb_metadata(self) -> dict:
        """Convert to ChromaDB-compatible metadata dict.

        ChromaDB metadata only supports str, int, float, bool — no lists or None.
        """
        meta = {
            "source_type": self.source_type,
            "domain": self.domain,
            "source_file": self.source_file,
            "line_start": self.line_start,
            "line_end": self.line_end,
            "chunk_id_in_file": self.chunk_id_in_file,
        }
        if self.chunk_type:
            meta["chunk_type"] = self.chunk_type
        if self.class_name:
            meta["class_name"] = self.class_name
        if self.name:
            meta["name"] = self.name
        if self.signature:
            meta["signature"] = self.signature
        if self.inherits_from:
            meta["inherits_from"] = json.dumps(self.inherits_from)
        if self.docstring:
            meta["docstring"] = self.docstring[:500]
        if self.page_start is not None:
            meta["page_start"] = self.page_start
        if self.page_end is not None:
            meta["page_end"] = self.page_end
        return meta

    @staticmethod
    def from_chromadb_metadata(chunk_id: str, text: str, meta: dict) -> "Chunk":
        """Reconstruct a Chunk from ChromaDB metadata (used in search results)."""
        inherits = None
        if meta.get("inherits_from"):
            inherits = json.loads(meta["inherits_from"])
        return Chunk(
            chunk_id=chunk_id,
            domain=meta.get("domain", ""),
            text=text,
            source_type=meta.get("source_type", "unknown"),
            chunk_type=meta.get("chunk_type"),
            class_name=meta.get("class_name"),
            name=meta.get("name"),
            signature=meta.get("signature"),
            inherits_from=inherits,
            docstring=meta.get("docstring"),
            source_file=meta.get("source_file", ""),
            line_start=meta.get("line_start", 0),
            line_end=meta.get("line_end", 0),
            chunk_id_in_file=meta.get("chunk_id_in_file", 0),
        )


class DomainParser(ABC):
    """Base class for domain-specific parsers.

    Subclass this in domains/<name>/parser.py and name the class 'Parser'.
    """

    @abstractmethod
    def parse(self, file_path: str, content: str) -> list[Chunk]:
        """Parse source content into structured Chunk objects."""
        ...

    @property
    @abstractmethod
    def source_type_name(self) -> str:
        """Identifier, e.g. 'rst-godot'."""
        ...


# ── Fallback chunking ─────────────────────────────────────────────────────

FALLBACK_CHUNK_SIZE = 2000  # approximate tokens
FALLBACK_CHUNK_OVERLAP = 400
CHARS_PER_TOKEN = 4
FALLBACK_CHUNK_CHARS = FALLBACK_CHUNK_SIZE * CHARS_PER_TOKEN       # 2000
FALLBACK_OVERLAP_CHARS = FALLBACK_CHUNK_OVERLAP * CHARS_PER_TOKEN  # 1600


# Regex to detect PDF page separators inserted by parse_pdf_to_markdown.py
# Format: "--- end of page=N ---" where N is 0-based.
# parse_pdf_to_markdown.py uses page_separators=True in pymupdf4llm.to_markdown().
_PAGE_SEPARATOR_RE = re.compile(r'--- end of page=(\d+) ---')


def _extract_page_numbers(text_slice: str, full_text: str, slice_start: int) -> tuple[int | None, int | None]:
    """Extract page_start and page_end from page separators in a text slice.

    Page separators ("--- end of page=N ---") are inserted by
    parse_pdf_to_markdown.py. A chunk may span multiple pages, so we find
    the first page number before or within the slice, and the last page
    number within or just after the slice.

    Returns (page_start, page_end) — both are 1-based (matching PDF
    convention), or (None, None) if no separators are present.
    """
    # Find all page separators in the FULL text (not just the slice) so we
    # can determine which page the chunk starts on.
    all_seps = list(_PAGE_SEPARATOR_RE.finditer(full_text))
    if not all_seps:
        return None, None

    # Find page separators WITHIN the slice
    seps_in_slice = list(_PAGE_SEPARATOR_RE.finditer(text_slice))

    # page_start: the page number of the last separator BEFORE the slice
    # starts, or 0 (first page) if no separator precedes the slice.
    page_start_num = 0  # default: first page (0-based from separator)
    for sep in all_seps:
        if sep.start() < slice_start:
            page_start_num = int(sep.group(1))
        else:
            break

    # page_end: the page number of the last separator WITHIN the slice
    if seps_in_slice:
        page_end_num = int(seps_in_slice[-1].group(1))
    else:
        # No separator in slice → chunk is entirely within page_start_num
        page_end_num = page_start_num

    # Convert to 1-based page numbers (PDF convention)
    return page_start_num + 1, page_end_num + 1


def fallback_chunk(
    text: str,
    domain: str,
    source_type: str,
    source_file: str,
    chunk_size: int = FALLBACK_CHUNK_CHARS,
    overlap: int = FALLBACK_OVERLAP_CHARS,
) -> list[Chunk]:
    """Sliding-window chunking (fallback when no parser exists).

    If the text contains "--- end of page=N ---" separators (inserted by
    parse_pdf_to_markdown.py), each Chunk's page_start/page_end is set
    to the PDF page number(s) it spans. Otherwise page_start/page_end
    remain None.
    """
    chunks = []
    start = 0
    chunk_idx = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk_text_slice = text[start:end]
        line_offset = text[:start].count("\n") + 1
        line_end = text[:end].count("\n") + 1

        # Extract PDF page numbers if page separators are present
        page_start, page_end = _extract_page_numbers(chunk_text_slice, text, start)

        chunks.append(Chunk(
            chunk_id=f"{domain}::fallback::{chunk_idx}",
            domain=domain,
            text=chunk_text_slice,
            source_type=source_type,
            source_file=source_file,
            line_start=line_offset,
            line_end=line_end,
            chunk_id_in_file=chunk_idx,
            page_start=page_start,
            page_end=page_end,
        ))

        chunk_idx += 1
        start += (chunk_size - overlap)

    return chunks


# ── Markdown section chunking (personal notes) ────────────────────────────

# Split Markdown at level-2 headers. The look-ahead (?=^## ) splits before
# each `## ` at line start without consuming the delimiter. The trailing
# space after the hashes is required, so `### ` (level-3) is NOT treated
# as a split point and stays inside its parent `## ` section.
_SECTION_SPLIT_RE = re.compile(r"(?=^## )", re.MULTILINE)
_HEADER_PREFIX_RE = re.compile(r"^##\s+")


def markdown_section_chunk(
    text: str,
    domain: str,
    source_type: str,
    source_file: str,
    category: str,
    max_section_chars: int = FALLBACK_CHUNK_CHARS,
    min_section_chars: int = 50,
) -> list[Chunk]:
    """Split Markdown at `## ` headers into per-section chunks.

    Intended for personal notes where each `## ` section is a
    semantically independent entry (e.g. one gotcha, one tip). Without
    splitting, a long file like ``gotchas.md`` would be indexed as a
    single chunk and dilute cross-encoder semantics.

    Behavior:
        * Files without any `## ` header fall back to ``fallback_chunk``.
        * Text before the first `## ` becomes a preamble chunk (only if
          its stripped length is >= ``min_section_chars``).
        * Each `## ` section becomes its own Chunk with
          ``chunk_type="personal_section"`` and ``name`` set to the
          section heading (without the ``## `` prefix).
        * Sections whose stripped length is < ``min_section_chars`` are
          skipped (defensive: avoids indexing TODO placeholders).
        * Sections larger than ``max_section_chars`` are sub-chunked
          via ``fallback_chunk`` (defensive: doesn't happen for personal
          notes, but keeps the function robust).
        * No overlap between sections (semantically independent).

    Args:
        text: Markdown source content.
        domain: Domain name (used for chunk_id prefix).
        source_type: Source type (``"personal"`` or ``"repo"``).
        source_file: Filename (for metadata traceability).
        category: File stem (e.g. ``"gotchas"``); used in chunk_id.
        max_section_chars: Threshold above which a single section is
            sub-chunked via ``fallback_chunk``.
        min_section_chars: Minimum stripped length to keep a chunk.
            Shorter sections are skipped.
    """
    if not text:
        return []

    # Fallback if no `## ` header is present.
    if not _SECTION_SPLIT_RE.search(text):
        return fallback_chunk(
            text,
            domain=domain,
            source_type=source_type,
            source_file=source_file,
        )

    # Split with look-ahead: each part begins with `## ` except the first
    # (the preamble, which may be empty).
    parts = _SECTION_SPLIT_RE.split(text)
    chunks: list[Chunk] = []
    section_idx = 0  # counts only sections + preamble, mirrors chunk_id_in_file

    for part in parts:
        if not part:
            continue

        # Detect whether this part is a section (starts with `## `) or
        # the preamble (everything before the first `## `).
        header_match = _HEADER_PREFIX_RE.match(part)
        is_section = header_match is not None

        # Defensive skip: skip sections/preambles whose stripped content
        # is below the minimum threshold (e.g. TODO placeholders).
        if len(part.strip()) < min_section_chars:
            continue

        # Large section → sub-chunk via fallback_chunk. This keeps the
        # function robust for future content growth.
        if len(part) > max_section_chars:
            sub_chunks = fallback_chunk(
                part,
                domain=domain,
                source_type=source_type,
                source_file=source_file,
            )
            for sub in sub_chunks:
                # Override the chunk_id / chunk_id_in_file to embed the
                # section index from the parent file.
                sub.chunk_id = f"{domain}::personal::{category}::{section_idx}"
                sub.chunk_id_in_file = section_idx
                if is_section:
                    heading = part[header_match.end():].split("\n", 1)[0].strip()
                    sub.name = heading
                    sub.chunk_type = "personal_section"
                else:
                    sub.name = None
                chunks.append(sub)
                section_idx += 1
            continue

        # Normal-sized section or preamble.
        line_start = text[: text.find(part)].count("\n") + 1
        line_end = line_start + part.count("\n")

        if is_section:
            heading = part[header_match.end():].split("\n", 1)[0].strip()
            name = heading
            chunk_type = "personal_section"
        else:
            name = None
            chunk_type = None

        chunks.append(
            Chunk(
                chunk_id=f"{domain}::personal::{category}::{section_idx}",
                domain=domain,
                text=part,
                source_type=source_type,
                source_file=source_file,
                line_start=line_start,
                line_end=line_end,
                chunk_id_in_file=section_idx,
                chunk_type=chunk_type,
                name=name,
            )
        )
        section_idx += 1

    return chunks


# ── Late Chunking (Phase 2.2) ─────────────────────────────────────────────
#
# Late chunking encodes the FULL chapter at once (BGE-M3 long context, up
# to LATE_CHUNK_MAX_CHAPTER_TOKENS tokens), captures the resulting
# token-level hidden states, and then POOLS them into 512-token windows
# with 128-token overlap. The advantage over fallback_chunk() is that
# each window's embedding is aware of the surrounding chapter context
# (cross-section semantics), which is what we want for PDF chapters
# (DaVinci Resolve manuals) where the same topic is discussed across
# pages.
#
# Reference: Günther et al. "Late Chunking: Contextual Chunk Embeddings
# Using Long-Context Embedding Models" (2024). Implementation adapted
# for HuggingFace transformer models with `output_hidden_states=True`.

LATE_CHUNK_WINDOW_TOKENS = 512
LATE_CHUNK_MAX_CHAPTER_TOKENS = 8192  # BGE-M3 max sequence length
LATE_CHUNK_POOLING_OVERLAP = 128

# Page-separator regex (shared with fallback_chunk's _PAGE_SEPARATOR_RE,
# duplicated here to keep late_chunk self-contained for unit tests).
_PAGE_SEP_RE = _PAGE_SEPARATOR_RE

# Heading regex: lines starting with `# ` or `## ` at line start.
_HEADING_RE = re.compile(r"(?m)^#{1,2} ")


def _split_into_chapters(
    text: str,
    max_tokens: int = LATE_CHUNK_MAX_CHAPTER_TOKENS,
) -> list[tuple[str, int, int]]:
    """Split PDF text into chapters at page boundaries and markdown headings.

    Split points (in priority order):
        1. ``--- end of page=N ---`` separators (inserted by
           ``parse_pdf_to_markdown.py``). Each page boundary becomes a
           chapter break.
        2. Markdown headings ``# Heading`` and ``## Heading`` at line
           start (level 1 and 2 only; level 3+ is kept inside the
           enclosing level-2 chapter).

    Returns:
        list of ``(chapter_text, page_start_0based, page_end_0based)``
        tuples. Pages are 0-based (the format used by the page
        separator). Empty chapters are skipped. Chapters whose text
        exceeds ``max_tokens`` characters are sub-split with a warning.

    Note:
        The max_tokens parameter is interpreted in CHARACTERS here (not
        tokenizer tokens), as a defensive upper bound to avoid feeding
        pathologically long chapters to the tokenizer. The tokenizer's
        own ``max_length`` truncates at the actual token level.
    """
    if not text or not text.strip():
        return []

    # Collect split positions: each split is (position_in_text, page_num).
    # We walk the text left-to-right and break on the first split point
    # we encounter (heading or page separator) — page separators take
    # precedence because they encode the natural PDF page boundary.
    split_positions: list[tuple[int, int]] = []  # (char_pos, page_num_0based)
    current_page = 0  # page counter

    last_pos = 0
    for sep_match in _PAGE_SEP_RE.finditer(text):
        # Pages 0..N-1 are determined by the separator number.
        # Anything BEFORE the first separator is page 0.
        sep_pos = sep_match.start()
        sep_page = int(sep_match.group(1))
        # A heading between the last position and the next separator
        # is also a chapter boundary, but the page separator itself
        # is the more important boundary — we use it directly.
        split_positions.append((sep_pos, sep_page))
        last_pos = sep_match.end()

    # If the text has NO page separators but has headings, split at headings.
    if not split_positions:
        for h_match in _HEADING_RE.finditer(text):
            # Skip the first heading if it's at position 0 (file starts
            # with a heading — no need to split there).
            if h_match.start() == 0:
                continue
            split_positions.append((h_match.start(), 0))
    else:
        # Even with page separators, also consider heading splits
        # BETWEEN separators. Only keep heading splits that don't
        # coincide with a separator.
        sep_positions = {p for p, _ in split_positions}
        for h_match in _HEADING_RE.finditer(text):
            if h_match.start() in sep_positions:
                continue
            if h_match.start() == 0:
                continue
            split_positions.append((h_match.start(), -1))  # -1 = use default

    # Sort by position
    split_positions.sort(key=lambda x: x[0])

    # Build chapter slices.
    chapters: list[tuple[str, int, int]] = []
    boundaries = [p for p, _ in split_positions] + [len(text)]
    # The page number recorded at each split position.
    sep_pages = [p for _, p in split_positions]

    def _page_at_position(pos: int) -> int:
        """Return the 0-based page number of the character at ``pos``.

        Page boundary rule: a separator at position S with page=N
        means content at positions (prev_sep, S] is on page N, and
        content at positions (S, next_sep] is on page N+1. The
        separator itself is on page N.

        Heading splits are NOT real page boundaries — they are only
        position markers, registered with ``page=-1`` ("use default").
        They must be skipped here so they don't reset the page counter
        (which would produce ``page_start=-1`` chunks in the late-chunk
        pipeline, and ``w_page_start=0`` after the +1 conversion —
        breaking the 1-based page convention).
        """
        page = 0
        for sep_pos, sep_page in split_positions:
            if pos < sep_pos:
                break
            # Heading splits carry sep_page=-1 ("use default"); they
            # are not real page boundaries and must not overwrite the
            # current ``page`` value.
            if sep_page < 0:
                continue
            # pos >= sep_pos: we are AT or AFTER the separator.
            # If pos == sep_pos, we're on page sep_page.
            # If pos > sep_pos, we're on page sep_page + 1.
            if pos == sep_pos:
                page = sep_page
            else:
                page = sep_page + 1
        return page

    for i, start in enumerate([0] + boundaries[:-1]):
        end = boundaries[i]
        # chapter_page_start: page at position ``start`` (inclusive).
        # chapter_page_end: page at position ``end - 1`` (last char in chapter).
        chapter_page_start = _page_at_position(start)
        chapter_page_end = _page_at_position(max(end - 1, start))

        chapter_text = text[start:end]
        # Skip empty chapters (e.g. leading whitespace before the first
        # separator). Also skip chapters whose content is ONLY page
        # separators and whitespace — these appear between consecutive
        # page separators and have no useful text to index.
        if not chapter_text.strip():
            continue
        if not re.sub(_PAGE_SEP_RE, "", chapter_text).strip():
            continue

        # Defensive: chapters larger than max_tokens characters get
        # sub-split at paragraph boundaries. If a single paragraph
        # itself exceeds max_tokens AND has no internal \n\n boundaries
        # (e.g. a very long line of unbroken text), we fall back to
        # fixed-size character splits with overlap. We do not warn at
        # the warning level for every chapter — instead we just log the
        # count once at the late_chunk() entry point.
        if len(chapter_text) > max_tokens:
            sub_chunks: list[tuple[str, int, int]] = []
            # Split on double-newline (paragraph boundary)
            paragraphs = re.split(r"\n\s*\n", chapter_text)
            sub_text = ""
            for p in paragraphs:
                if len(sub_text) + len(p) > max_tokens and sub_text:
                    sub_chunks.append((sub_text, chapter_page_start, chapter_page_end))
                    sub_text = p
                else:
                    sub_text = (sub_text + "\n\n" + p) if sub_text else p
            if sub_text.strip():
                sub_chunks.append((sub_text, chapter_page_start, chapter_page_end))
            for sub in sub_chunks:
                # MEDIUM-2 fix: if a single sub-chunk still exceeds
                # max_tokens (e.g. a paragraph with no \n\n boundaries
                # that is longer than max_tokens), split it into
                # fixed-size character chunks with a small overlap.
                # This is a defensive last-resort path; the resulting
                # chunks will be re-encoded with BGE-M3's max_length
                # truncation, but at least the indexer doesn't blow up
                # with a 100k-character chunk.
                if len(sub[0]) > max_tokens:
                    chunk_size_chars = 8000
                    overlap_chars = 200
                    text_part = sub[0]
                    pos = 0
                    while pos < len(text_part):
                        end_pos = min(pos + chunk_size_chars, len(text_part))
                        sub_chunks.append((
                            text_part[pos:end_pos],
                            sub[1],
                            sub[2],
                        ))
                        if end_pos >= len(text_part):
                            break
                        pos += chunk_size_chars - overlap_chars
                    warnings.warn(
                        f"Chapter exceeds {max_tokens} chars with no "
                        f"\\n\\n boundaries; fixed-size splitting at "
                        f"{chunk_size_chars} chars.",
                        RuntimeWarning,
                        stacklevel=2,
                    )
                if sub[0].strip():
                    chapters.append(sub)
        else:
            chapters.append((chapter_text, chapter_page_start, chapter_page_end))

    return chapters


def _token_windows_from_offsets(
    text: str,
    offset_mapping: list[tuple[int, int]],
    window_size: int = LATE_CHUNK_WINDOW_TOKENS,
    overlap: int = LATE_CHUNK_POOLING_OVERLAP,
) -> list[tuple[str, int, int]]:
    """Slice text into ``window_size``-token windows via token offset mapping.

    Uses the token-level ``offset_mapping`` (returned by
    ``tokenizer(..., return_offsets_mapping=True)``) to slice the
    ORIGINAL text — NOT ``tokenizer.decode()``, which would lose
    whitespace and normalization. Each window covers ``window_size``
    tokens with ``overlap``-token overlap to the next window.

    Special tokens (offset ``(0, 0)`` at the start/end) are skipped.
    Tokens whose offset is ``(0, 0)`` in the middle (BPE wordboundary
    markers, etc.) are also skipped.

    The result is lossless: ``"".join(w[0] for w in windows) == text``
    after stripping the leading/trailing whitespace of the join
    (modulo separator gaps in the original text). For BGE-M3
    (XLM-RoBERTa) the offsets are CHARACTER-based, so
    ``text[start:end]`` is the correct slice. For tokenizers that
    return BYTE offsets (e.g. some SentencePiece configurations with
    multi-byte UTF-8), this function falls back to
    ``text.encode('utf-8')[start:end].decode('utf-8')`` automatically.

    Returns:
        list of ``(window_text, char_start, char_end)`` tuples.
    """
    if not offset_mapping:
        return []

    # Build a list of (char_start, char_end) for REAL (non-special) tokens.
    # Special tokens have offset (0, 0). We detect byte-vs-char offsets by
    # checking whether ANY non-special token offset is out of range for
    # char-slicing (i.e. > len(text) characters means byte offsets).
    real_offsets: list[tuple[int, int]] = []
    n_text = len(text)
    n_bytes = len(text.encode("utf-8"))
    for s, e in offset_mapping:
        if s == 0 and e == 0:
            continue
        if s < 0 or e < 0:
            continue
        real_offsets.append((s, e))

    if not real_offsets:
        return []

    # Detect byte vs char offsets. If the maximum end-offset exceeds
    # the text length in characters but not in bytes, we have byte
    # offsets. (This is conservative: a very long text on a tokenizer
    # that returns char offsets but happens to exceed n_text would not
    # be byte offsets; the max-offset test is the discriminant.)
    max_end = max(e for _, e in real_offsets)
    use_byte_offsets = max_end > n_text and max_end <= n_bytes

    def _slice(s: int, e: int) -> str:
        if use_byte_offsets:
            return text.encode("utf-8")[s:e].decode("utf-8", errors="replace")
        return text[s:e]

    # Step size in tokens. If overlap >= window_size, fall back to
    # non-overlapping windows (defensive).
    step = window_size - overlap
    if step <= 0:
        step = window_size
        overlap = 0

    # Drop the special tokens (CLS, SEP, PAD) at the start/end of
    # offset_mapping — they have offset (0, 0) and we already
    # filtered them out above.

    windows: list[tuple[str, int, int]] = []
    n_tokens = len(real_offsets)
    for start_idx in range(0, n_tokens, step):
        end_idx = min(start_idx + window_size, n_tokens)
        # Skip windows that have zero tokens
        if end_idx <= start_idx:
            break
        char_start = real_offsets[start_idx][0]
        char_end = real_offsets[end_idx - 1][1]
        window_text = _slice(char_start, char_end)
        windows.append((window_text, char_start, char_end))
        if end_idx >= n_tokens:
            break

    return windows


def _clean_chunk_text(text: str) -> str:
    """Remove ``--- end of page=N ---`` separators from a chunk's text.

    Page metadata is extracted BEFORE this cleanup (in ``late_chunk``),
    so the separator can be safely dropped from the indexed text.
    Multi-newline whitespace is collapsed to single newlines and the
    result is stripped.
    """
    cleaned = _PAGE_SEP_RE.sub("", text)
    # Collapse runs of 3+ newlines to 2 (paragraph break).
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def _encode_chapter_with_hidden_states(
    model,
    chapter_text: str,
) -> tuple["object", list[tuple[int, int]]]:
    """Encode a chapter and return token-level hidden states + offsets.

    Backward-compatible wrapper around
    ``_encode_chapter_with_hidden_states_on_device``. The device is
    resolved from the model parameters at call time (one-shot per
    call). Production callers should use
    ``_LateChunkEncoder.encode_chapter`` for pre-detected-device
    performance; this wrapper exists for legacy/test code paths.

    Returns:
        (token_states, offset_mapping) where:
            - ``token_states`` is a torch.Tensor of shape
              ``(seq_len, hidden_dim)`` containing the LAST hidden
              layer activations for each input token (special tokens
              CLS/SEP/PAD included).
            - ``offset_mapping`` is a list of ``(char_start, char_end)``
              tuples aligned with the token_states rows. Special-token
              offsets are ``(0, 0)``.
    """
    import torch

    # Resolve the model's device (matches the device-routing in
    # ``_encode_chapter_with_hidden_states_on_device``). We compute it
    # here so the legacy function signature is preserved.
    target_device = next(model[0].auto_model.parameters()).device
    target_device_str = str(target_device)

    return _encode_chapter_with_hidden_states_on_device(
        model, chapter_text, target_device_str
    )


class _LateChunkEncoder:
    """Stateful wrapper that pre-detects the model's device and handles
    MPS→CPU fallback ONCE for the entire encode session.

    Blind-Spot-Review Hinweis 1: A failed ``auto_model.forward()`` on
    MPS can leave the model in a corrupted state. We avoid this by
    doing a warmup encode on a tiny string at construction time. If
    the warmup fails, we move the entire model to CPU and use CPU for
    all subsequent chapters.
    """

    def __init__(self, model) -> None:
        self._model = model
        self._device: str | None = None
        self._cpu_fallback_used: bool = False
        # Pre-flight: warmup on a tiny test string. If this fails, move
        # to CPU. We do NOT use try/except per-chapter — that would be
        # too late (the first chapter's forward() may have already
        # corrupted MPS state).
        self._warmup()

    def _resolve_device(self) -> str:
        try:
            return str(next(self._model[0].auto_model.parameters()).device)
        except Exception:
            return "cpu"

    def _move_model_to_cpu(self) -> None:
        """Move the inner HuggingFace model to CPU. Idempotent."""
        try:
            self._model[0].auto_model.to("cpu")
            self._cpu_fallback_used = True
        except Exception as e:
            warnings.warn(
                f"Failed to move model to CPU during MPS→CPU fallback: {e}",
                RuntimeWarning,
                stacklevel=2,
            )

    def _warmup(self) -> None:
        """Run a single tiny encode to validate device compatibility.

        If the warmup fails AND the model is on MPS, fall back to CPU.
        If the warmup fails AND the model is already on CPU, re-raise
        (the caller will see the error and can decide what to do).
        """
        test_input = "warmup"
        device = self._resolve_device()
        try:
            _ = self._encode_raw(test_input, device)
            self._device = device
        except Exception as e:
            if "mps" in device.lower():
                warnings.warn(
                    f"Phase 2.2 Late Chunking: MPS warmup failed "
                    f"({type(e).__name__}: {e}); falling back to CPU "
                    f"for the entire encoding session.",
                    RuntimeWarning,
                    stacklevel=2,
                )
                self._move_model_to_cpu()
                # Re-run warmup on CPU to confirm the model is usable.
                _ = self._encode_raw(test_input, "cpu")
                self._device = "cpu"
            else:
                # Already on CPU and still failed — propagate.
                raise

    def _encode_raw(self, text: str, device: str) -> "object":
        """Single encode call without warmup/fallback. Internal helper."""
        import torch

        transformer = self._model[0]
        enc = transformer.tokenizer(
            text,
            return_tensors="pt",
            return_offsets_mapping=True,
            truncation=True,
            max_length=LATE_CHUNK_MAX_CHAPTER_TOKENS,
        )
        model_in = {
            k: v.to(device)
            for k, v in enc.items()
            if k in ("input_ids", "attention_mask")
        }
        with torch.no_grad():
            outputs = transformer.auto_model(
                **model_in,
                output_hidden_states=True,
            )
        return outputs

    def encode_chapter(
        self, chapter_text: str
    ) -> tuple["object", list[tuple[int, int]]]:
        """Encode a chapter, returning (last_hidden_state, offset_mapping).

        Routes to the pre-detected device. ``_warmup`` has already
        handled the MPS→CPU fallback decision, so this method just
        does the encode.
        """
        assert self._device is not None, "_warmup did not run"
        return _encode_chapter_with_hidden_states_on_device(
            self._model, chapter_text, self._device
        )


def _encode_chapter_with_hidden_states_on_device(
    model,
    chapter_text: str,
    device: str,
) -> tuple["object", list[tuple[int, int]]]:
    """Encode a chapter on a SPECIFIC device (used by ``_LateChunkEncoder``).

    Same as ``_encode_chapter_with_hidden_states`` but takes the
    device explicitly so the warmup pre-flight can pin the choice
    for all subsequent chapters.
    """
    import torch

    transformer = model[0]
    tokenizer = transformer.tokenizer
    enc = tokenizer(
        chapter_text,
        return_tensors="pt",
        return_offsets_mapping=True,
        truncation=True,
        max_length=LATE_CHUNK_MAX_CHAPTER_TOKENS,
    )
    model_in = {
        k: v.to(device)
        for k, v in enc.items()
        if k in ("input_ids", "attention_mask")
    }
    with torch.no_grad():
        outputs = transformer.auto_model(
            **model_in,
            output_hidden_states=True,
        )
    last_hidden = outputs.last_hidden_state[0]
    offsets = enc["offset_mapping"][0].tolist()
    return last_hidden, offsets


def late_chunk(
    text: str,
    domain: str,
    source_file: str,
    model,
    window_size: int = LATE_CHUNK_WINDOW_TOKENS,
    overlap: int = LATE_CHUNK_POOLING_OVERLAP,
) -> tuple[list[Chunk], dict[str, "np.ndarray"]]:
    """Chapter-wise late chunking for PDF sources.

    Algorithm (Phase 2.2):
        1. Split the PDF text into chapters at page boundaries and
           markdown headings.
        2. For each chapter, encode the FULL chapter text with
           ``output_hidden_states=True`` to get token-level hidden
           states (BGE-M3, up to 8192 tokens per chapter).
        3. Slice the chapter into ``window_size``-token windows with
           ``overlap``-token overlap using the tokenizer's offset
           mapping (lossless via original-text slicing).
        4. Mean-pool the token hidden states within each window to
           get a single ``(hidden_dim,)`` embedding.
        5. Emit a Chunk per window with the cleaned text (page
           separators removed) and the precomputed embedding.

    Page metadata:
        ``page_start`` / ``page_end`` are extracted from the original
        (separator-laden) text BEFORE ``_clean_chunk_text`` runs, so
        they reflect the PDF page numbers of the window's text.
        ``_extract_page_numbers`` is called on the original chapter
        text, not the cleaned window text, because the chapter-level
        page range is the same for all windows in the chapter.

    Returns:
        ``(chunks, precomputed_embeddings)`` where ``precomputed_embeddings``
        maps ``chunk_id`` → ``np.ndarray`` of shape ``(hidden_dim,)``.
        This is the interface expected by ``embed_index.build_index``
        (Hinweis 2 from the blind-spot review).
    """
    import numpy as np

    if not text or not text.strip():
        return [], {}

    chapters = _split_into_chapters(text, max_tokens=LATE_CHUNK_MAX_CHAPTER_TOKENS)
    if not chapters:
        return [], {}

    encoder = _LateChunkEncoder(model)
    chunks: list[Chunk] = []
    precomputed: dict[str, "np.ndarray"] = {}
    chunk_idx = 0

    for chapter_text, page_start, page_end in chapters:
        try:
            last_hidden, offsets = encoder.encode_chapter(chapter_text)
        except Exception as e:
            warnings.warn(
                f"late_chunk: failed to encode chapter from {source_file} "
                f"(pages {page_start}-{page_end}): {type(e).__name__}: {e}. "
                f"Skipping chapter.",
                RuntimeWarning,
                stacklevel=2,
            )
            continue

        windows = _token_windows_from_offsets(
            chapter_text,
            offsets,
            window_size=window_size,
            overlap=overlap,
        )

        for window_text, char_start, char_end in windows:
            # The window is fully inside one chapter, so its page
            # range is the chapter's page range. We use the chapter's
            # already-correct page_start/page_end (computed by
            # _split_into_chapters via _page_at_position). The
            # chapter pages are 0-based; convert to 1-based for
            # consistency with the rest of the codebase.
            w_page_start = page_start + 1
            w_page_end = page_end + 1

            # Clean the window text (remove page separators).
            clean_text = _clean_chunk_text(window_text)
            if not clean_text:
                continue

            # Compute window embedding by mean-pooling the token hidden
            # states that fall inside the window's character range.
            # We iterate over the offsets and select tokens whose
            # [s, e) intersects [char_start, char_end) in the original
            # chapter text.
            window_token_indices: list[int] = []
            for tok_idx, (s, e) in enumerate(offsets):
                if s == 0 and e == 0:
                    continue  # special token
                if s >= char_end or e <= char_start:
                    continue
                window_token_indices.append(tok_idx)

            if not window_token_indices:
                # No tokens fell into this window (rare — e.g. window
                # is entirely whitespace). Skip.
                continue

            window_states = last_hidden[window_token_indices]  # (n_tokens, hidden_dim)
            embedding = window_states.mean(dim=0).cpu().numpy()

            chunk_id = f"{domain}::late_chunk::{source_file}::{chunk_idx}"
            chunk = Chunk(
                chunk_id=chunk_id,
                domain=domain,
                text=clean_text,
                source_type="repo",  # PDF sources live in sources/, not personal/
                source_file=source_file,
                line_start=0,  # late chunking doesn't preserve line numbers
                line_end=0,
                chunk_id_in_file=chunk_idx,
                chunk_type="late_chunk",
                page_start=w_page_start,
                page_end=w_page_end,
            )
            chunks.append(chunk)
            precomputed[chunk_id] = embedding.astype(np.float32)
            chunk_idx += 1

    return chunks, precomputed
