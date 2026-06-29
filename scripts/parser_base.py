#!/usr/bin/env python3
"""
Plugin system for domain-specific structured parsing.

Defines the Chunk dataclass (unified schema for all chunks) and the
DomainParser abstract base class. Domains MAY provide a parser.py that
subclasses DomainParser. If no parser exists, fallback_chunk() is used.
"""

import json
import re
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
FALLBACK_CHUNK_OVERLAP = 200
CHARS_PER_TOKEN = 4
FALLBACK_CHUNK_CHARS = FALLBACK_CHUNK_SIZE * CHARS_PER_TOKEN       # 2000
FALLBACK_OVERLAP_CHARS = FALLBACK_CHUNK_OVERLAP * CHARS_PER_TOKEN  # 400


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
