#!/usr/bin/env python3
"""
Plugin system for domain-specific structured parsing.

Defines the Chunk dataclass (unified schema for all chunks) and the
DomainParser abstract base class. Domains MAY provide a parser.py that
subclasses DomainParser. If no parser exists, fallback_chunk() is used.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


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
    chunk_type: str | None = None       # "class" | "method" | "property" | "signal" | "enum" | "section"
    class_name: str | None = None       # z.B. "Node3D"
    name: str | None = None             # Methoden-/Property-Name, z.B. "rotate_y"
    signature: str | None = None        # "void rotate_y(angle: float)"
    inherits_from: list[str] | None = None  # ["Node"]
    docstring: str | None = None        # Beschreibungstext

    # Position
    source_file: str = ""
    line_start: int = 0
    line_end: int = 0

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
            meta["inherits_from"] = "::".join(self.inherits_from)
        if self.docstring:
            meta["docstring"] = self.docstring[:500]
        return meta

    @staticmethod
    def from_chromadb_metadata(chunk_id: str, text: str, meta: dict) -> "Chunk":
        """Reconstruct a Chunk from ChromaDB metadata (used in search results)."""
        inherits = None
        if meta.get("inherits_from"):
            inherits = meta["inherits_from"].split("::")
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

FALLBACK_CHUNK_SIZE = 500   # approximate tokens
FALLBACK_CHUNK_OVERLAP = 100
CHARS_PER_TOKEN = 4
FALLBACK_CHUNK_CHARS = FALLBACK_CHUNK_SIZE * CHARS_PER_TOKEN       # 2000
FALLBACK_OVERLAP_CHARS = FALLBACK_CHUNK_OVERLAP * CHARS_PER_TOKEN  # 400


def fallback_chunk(
    text: str,
    domain: str,
    source_type: str,
    source_file: str,
    chunk_size: int = FALLBACK_CHUNK_CHARS,
    overlap: int = FALLBACK_OVERLAP_CHARS,
) -> list[Chunk]:
    """Sliding-window chunking (fallback when no parser exists)."""
    chunks = []
    start = 0
    chunk_idx = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk_text_slice = text[start:end]
        line_offset = text[:start].count("\n") + 1
        line_end = text[:end].count("\n") + 1

        chunks.append(Chunk(
            chunk_id=f"{domain}::fallback::{chunk_idx}",
            domain=domain,
            text=chunk_text_slice,
            source_type=source_type,
            source_file=source_file,
            line_start=line_offset,
            line_end=line_end,
            chunk_id_in_file=chunk_idx,
        ))

        chunk_idx += 1
        start += (chunk_size - overlap)

    return chunks
