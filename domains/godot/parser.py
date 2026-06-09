#!/usr/bin/env python3
"""
Godot RST documentation parser.

Parses Godot's RST class documentation into structured Chunk objects.
Handles: .. class:: ClassName, methods, properties, signals, enums, and
inheritance chains. Non-class content (tutorials, getting-started) falls
through to fallback_chunk() via the caller (embed_index.py).

Reference: https://github.com/godotengine/godot-docs (classes/*.rst)
"""

import re
import sys
from pathlib import Path

# Add scripts/ to path so we can import parser_base
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))

from parser_base import Chunk, DomainParser


class Parser(DomainParser):
    """Parser for Godot RST class documentation files."""

    source_type_name = "rst-godot"

    # ── Regex patterns ─────────────────────────────────────────────────
    CLASS_PATTERN = re.compile(r"^\.\.\s+class::\s+(\w+)")
    INHERITS_PATTERN = re.compile(r"inherits.*?:?\s*(.+)$", re.IGNORECASE)
    METHOD_PATTERN = re.compile(
        r"^\s*(?:static\s+)?(?:\w[\w.]*\s+)?(\w+(?:\.\w+)*)\s*\([^)]*\)",
    )
    PROPERTY_PATTERN = re.compile(
        r"^\s*var\s+(\w+)\s*(?::\s*\w+)?",
    )
    SIGNAL_PATTERN = re.compile(r"^\s*signal\s+(\w+)\s*\(([^)]*)\)")
    ENUM_PATTERN = re.compile(r"^\s*enum\s+(\w+)")

    def __init__(self):
        self.domain = "godot"

    def parse(self, file_path: str, content: str) -> list[Chunk]:
        """Parse Godot RST content into structured chunks."""
        chunks = []
        lines = content.splitlines()
        current_class = None
        current_inherits = None
        i = 0

        while i < len(lines):
            line = lines[i]

            # Detect class definition:    .. class:: ClassName
            class_match = self.CLASS_PATTERN.match(line)
            if class_match:
                current_class = class_match.group(1)
                current_inherits = self._parse_inherits(line)
                # Generate class overview chunk from the next few lines
                overview_lines = self._collect_section(lines, i + 1, max_lines=20)
                overview_text = "\n".join(overview_lines)
                chunks.append(self._make_class_chunk(
                    current_class, current_inherits, overview_text, file_path, i
                ))
                i += len(overview_lines) + 1
                continue

            # Detect member within a class
            if current_class:
                chunk = self._try_parse_member(
                    lines, i, current_class, current_inherits, file_path
                )
                if chunk:
                    chunks.append(chunk)
                    i += 1
                    continue

            i += 1

        return chunks

    def _parse_inherits(self, line: str) -> list[str] | None:
        """Extract inheritance from class definition line."""
        m = self.INHERITS_PATTERN.search(line)
        if m:
            raw = m.group(1).strip()
            # Split on comma or whitespace
            return [c.strip() for c in re.split(r"[,\s]+", raw) if c.strip()]
        return None

    def _collect_section(
        self, lines: list[str], start: int, max_lines: int = 20
    ) -> list[str]:
        """Collect lines until empty line or next directive."""
        result = []
        for i in range(start, min(start + max_lines, len(lines))):
            line = lines[i]
            if not line.strip():
                break
            if line.lstrip().startswith(".. "):
                break
            result.append(line)
        return result

    def _make_class_chunk(
        self,
        class_name: str,
        inherits: list[str] | None,
        overview: str,
        file_path: str,
        line_start: int,
    ) -> Chunk:
        inherits_text = ""
        if inherits:
            chain = " → ".join(inherits)
            inherits_text = f" extends {chain}"
        text = f"Class: {class_name}{inherits_text}\n\n{overview}"
        return Chunk(
            chunk_id=f"godot::{class_name}::class",
            domain="godot",
            text=text,
            source_type="repo",
            chunk_type="class",
            class_name=class_name,
            name=class_name,
            inherits_from=inherits,
            docstring=overview[:500],
            source_file=file_path,
            line_start=line_start + 1,
            line_end=line_start + len(overview.splitlines()) + 1,
        )

    def _try_parse_member(
        self,
        lines: list[str],
        i: int,
        class_name: str,
        inherits: list[str] | None,
        file_path: str,
    ) -> Chunk | None:
        """Try to parse a method, property, signal, or enum on this line."""
        line = lines[i].strip()
        if not line:
            return None

        # Method: type name(...)
        method_match = self.METHOD_PATTERN.match(line)
        if method_match:
            name = method_match.group(1)
            signature = line
            doc = self._collect_section(lines, i + 1, max_lines=10)
            text = self._build_member_text(
                "Method", class_name, name, signature, inherits, doc
            )
            return Chunk(
                chunk_id=f"godot::{class_name}::method::{name}",
                domain="godot",
                text=text,
                source_type="repo",
                chunk_type="method",
                class_name=class_name,
                name=name,
                signature=signature,
                inherits_from=inherits,
                docstring="\n".join(doc)[:500] if doc else signature,
                source_file=file_path,
                line_start=i + 1,
                line_end=i + 1 + len(doc),
            )

        # Signal: signal name(...)
        signal_match = self.SIGNAL_PATTERN.match(line)
        if signal_match:
            name = signal_match.group(1)
            params = signal_match.group(2)
            signature = f"signal {name}({params})"
            doc = self._collect_section(lines, i + 1, max_lines=10)
            text = self._build_member_text(
                "Signal", class_name, name, signature, inherits, doc
            )
            return Chunk(
                chunk_id=f"godot::{class_name}::signal::{name}",
                domain="godot",
                text=text,
                source_type="repo",
                chunk_type="signal",
                class_name=class_name,
                name=name,
                signature=signature,
                inherits_from=inherits,
                docstring="\n".join(doc)[:500] if doc else signature,
                source_file=file_path,
                line_start=i + 1,
                line_end=i + 1 + len(doc),
            )

        # Enum: enum Name
        enum_match = self.ENUM_PATTERN.match(line)
        if enum_match:
            name = enum_match.group(1)
            doc = self._collect_section(lines, i + 1, max_lines=10)
            text = f"Enum: {class_name}.{name}\n" + "\n".join(doc)
            return Chunk(
                chunk_id=f"godot::{class_name}::enum::{name}",
                domain="godot",
                text=text,
                source_type="repo",
                chunk_type="enum",
                class_name=class_name,
                name=name,
                inherits_from=inherits,
                docstring="\n".join(doc)[:500] if doc else "",
                source_file=file_path,
                line_start=i + 1,
                line_end=i + 1 + len(doc),
            )

        return None

    def _build_member_text(
        self,
        kind: str,
        class_name: str,
        name: str,
        signature: str,
        inherits: list[str] | None,
        doc: list[str],
    ) -> str:
        """Build rich text for a class member chunk."""
        parts = [f"{kind}: {class_name}.{name}"]
        parts.append(f"Signature: {signature}")
        if inherits:
            parts.append(f"Inherits: {' → '.join(inherits)}")
        if doc:
            parts.append("")
            parts.extend(doc)
        return "\n".join(parts)
