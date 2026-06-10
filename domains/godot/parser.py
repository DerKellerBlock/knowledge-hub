#!/usr/bin/env python3
"""
Godot RST documentation parser.

Parses Godot's RST class documentation (from the official godot-docs repo) into
structured Chunk objects. Handles the real RST format used by Godot:

- Class anchors:    .. _class_Node3D:
- Inheritance:      **Inherits:** :ref:`Node<class_Node>` **<** :ref:`Object<class_Object>`
- RST tables:       Properties, Methods, Signals, Constructors, Operators
- Description blocks per member (anchor + classref-* + signature + text)
- Enums with constants, theme_* sub-types, operators, constructors, annotations

Non-class content (tutorials, demos, other source files) returns an empty list
so the caller (embed_index.py) falls back to sliding-window chunking.

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

    # ── File boundary detection (in the repomix-packed file) ───────────
    FILE_HEADER_CLASS = re.compile(
        r"^## File: classes/class_([\w@]+)\.rst",
    )
    # 6 backticks for the repomix code fence (with or without trailing 'rst')
    RST_BLOCK_START = re.compile(r"^```````?rst\s*$")
    RST_BLOCK_END = re.compile(r"^```````?\s*$")

    # ── Class header ───────────────────────────────────────────────────
    CLASS_ANCHOR = re.compile(r"^\.\. _class_([\w@]+):$")
    INHERITS_LINE = re.compile(r"^\*\*Inherits:\*\*\s*(.+)$")
    INHERITED_BY_LINE = re.compile(r"^\*\*Inherited By:\*\*\s*(.+)$")
    REF_EXTRACT = re.compile(r":ref:`([^`<]+)<[^>]+>`")

    # ── RST markup cleanup ──────────────────────────────────────────────
    RST_MARKUP_CLEANUP = [
        (re.compile(r":ref:`🔗<[^>]+>`"), ""),
        (re.compile(r":ref:`([^`<]+)<[^>]+>`"), r"\1"),
        (re.compile(r":doc:`([^`<]+)<[^>]+>`"), r"\1"),
        (re.compile(r"``([^`]+)``"), r"\1"),
        (re.compile(r"\*\*([^*]+)\*\*"), r"\1"),
        (re.compile(r"\*([^*]+)\*"), r"\1"),
        (re.compile(r"\|(\w+)\|"), ""),
        (re.compile(r"\\ "), " "),
        (re.compile(r"\\\("), "("),
        (re.compile(r"\\\)"), ")"),
    ]

    # ── Section headers / sub-headers ───────────────────────────────────
    SECTION_PROPERTIES_TABLE = re.compile(r"^Properties\s*$")
    SECTION_METHODS_TABLE = re.compile(r"^Methods\s*$")
    SECTION_SIGNALS_TABLE = re.compile(r"^Signals\s*$")
    SECTION_CONSTRUCTORS_TABLE = re.compile(r"^Constructors\s*$")
    SECTION_OPERATORS_TABLE = re.compile(r"^Operators\s*$")
    SECTION_THEME_PROPERTIES_TABLE = re.compile(r"^Theme Properties\s*$")
    SECTION_DESCRIPTIONS_GROUP = re.compile(
        r"^\.\. rst-class:: classref-descriptions-group\s*$",
    )
    # Order matters: longer phrases first (Method Descriptions before Methods,
    # Operator Descriptions before Operators, Property Descriptions before Properties).
    SECTION_SUBHEADER = re.compile(
        r"^(Method Descriptions|Operator Descriptions|Constructor Descriptions|"
        r"Property Descriptions|Theme Property Descriptions|"
        r"Signals|Enumerations|Constants|Annotations)$",
    )

    # ── Table parsing ───────────────────────────────────────────────────
    TABLE_ROW = re.compile(r"^\|.+\|.+\|")
    # Property table: 2nd column has :ref:`name<class_X_property_name>`
    PROPERTY_TABLE_CELL = re.compile(
        r":ref:`([^`]+)<class_[\w@]+_property_([^`]+)>`",
    )
    # Method/constructor/operator table: last column has :ref:`name<class_X_method_NAME>`
    METHOD_TABLE_CELL = re.compile(
        r":ref:`([^`]+)<class_[\w@]+_(method|operator|constructor)_([^`]+)>`",
    )
    # Signal table: :ref:`name<class_X_signal_NAME>`
    SIGNAL_TABLE_CELL = re.compile(
        r":ref:`([^`]+)<class_[\w@]+_signal_([^`]+)>`",
    )
    # Theme property table: :ref:`name<class_X_theme_*_NAME>`
    THEME_PROPERTY_TABLE_CELL = re.compile(
        r":ref:`([^`]+)<class_[\w@]+_theme_(constant|color|icon|style|font|font_size)_([^`]+)>`",
    )

    # ── Unified member anchor (handles all 14 variants) ─────────────────
    # Order in alternation is critical: longer prefixes first.
    MEMBER_ANCHOR = re.compile(
        r"^\.\. _class_([\w@.]+?)_"
        r"(private_method|theme_constant|theme_color|theme_icon|"
        r"theme_style|theme_font|theme_font_size|"
        r"method|operator|constructor|"
        r"property|signal|constant|annotation|theme_property)_"
        r"([\w@.]+):$",
    )

    # Enum anchor: .. _enum_X:
    ENUM_ANCHOR = re.compile(r"^\.\. _enum_([\w@.]+):$")

    # ── RST classref markers per description block ─────────────────────
    CLASSREF_GROUP = re.compile(
        r"^\.\. rst-class::\s+"
        r"(classref-(?:method|operator|constructor|"
        r"property|signal|constant|annotation|"
        r"enumeration|enumeration-constant|"
        r"themeproperty|item-separator|section-separator))$",
    )

    # ── Signature line patterns (per member type) ──────────────────────
    # Method/operator/constructor: e.g. ":ref:`bool<class_bool>` **operator !=**\ (\ right\: ...)"
    METHOD_SIGNATURE = re.compile(
        r":ref:`[^`]+`\s*\*\*([\w@.+\-*\/=<>!%&|^~ ]+?)\*\*"
        r"\s*\\?\s*(.*?)(?:\s*:ref:`🔗|\s*$)",
    )
    # Property/theme property: ":ref:`Type<class_Type>` **name** :ref:`🔗...`"
    PROPERTY_SIGNATURE = re.compile(
        r":ref:`([^`]+)`\s*\*\*([\w@.]+?)\*\*\s*(?:=?\s*``([^`]*)``)?",
    )
    # Signal: "**signal_name**\ (\ params\ )"
    SIGNAL_SIGNATURE = re.compile(
        r"^\*\*([\w@.]+)\*\*\s*\\?\s*\(([^)]*)\)",
    )
    # Constant / enumeration-constant: "**NAME** = ``value``"
    CONSTANT_SIGNATURE = re.compile(
        r"^\*\*([\w@.]+)\*\*\s*=\s*``([^`]*)``",
    )
    # Annotation: "**@abstract**\ (\ )"
    ANNOTATION_SIGNATURE = re.compile(
        r"^\*\*([\w@.]+)\*\*\s*\\?\s*(.*?)(?:\s*:ref:`🔗|\s*$)",
    )
    # Theme property: ":ref:`Type<class_Type>` **name**"  (same as property)
    THEME_PROPERTY_SIGNATURE = PROPERTY_SIGNATURE
    # Enum header: "enum **Name**:"
    ENUM_SIGNATURE = re.compile(r"^enum\s+\*\*([\w@.]+)\*\*")

    # ── Mapping: RST member type → chunk_type ──────────────────────────
    MEMBER_TYPE_TO_CHUNK_TYPE = {
        "method": "method",
        "operator": "operator",
        "constructor": "constructor",
        "private_method": "method",
        "property": "property",
        "signal": "signal",
        "constant": "constant",
        "annotation": "annotation",
        "theme_property": "theme_property",
        "theme_constant": "theme_property",
        "theme_color": "theme_property",
        "theme_icon": "theme_property",
        "theme_style": "theme_property",
        "theme_font": "theme_property",
        "theme_font_size": "theme_property",
        "enum": "enum",
    }

    # Description sub-header → expected chunk_type
    SUBHEADER_TO_CHUNK_TYPE = {
        "Signals": "signal",
        "Enumerations": "enum",
        "Constants": "constant",
        "Annotations": "annotation",
        "Property Descriptions": "property",
        "Method Descriptions": "method",
        "Operator Descriptions": "operator",
        "Constructor Descriptions": "constructor",
        "Theme Property Descriptions": "theme_property",
    }

    def __init__(self) -> None:
        self.domain = "godot"

    # ── Public API ──────────────────────────────────────────────────────
    def parse(self, file_path: str, content: str) -> list[Chunk]:
        """Parse Godot RST content into structured chunks.

        Returns an empty list for non-class content (tutorials, demos, test files)
        so the caller can fall back to sliding-window chunking.
        """
        # Fast heuristic: only proceed if this file contains class RST content.
        if "## File: classes/class_" not in content:
            return []

        chunks: list[Chunk] = []
        lines = content.splitlines()
        i = 0
        n = len(lines)

        while i < n:
            # Look for the next class file header
            m = self.FILE_HEADER_CLASS.match(lines[i])
            if not m:
                i += 1
                continue

            class_name = m.group(1)
            i += 1

            # Find the start of the RST code block (```````rst)
            while i < n and not self.RST_BLOCK_START.match(lines[i]):
                i += 1
            i += 1  # skip the ````````rst line

            # Look for class anchor in first ~10 lines to get case-correct name
            for j in range(i, min(i + 15, n)):
                cm = self.CLASS_ANCHOR.match(lines[j])
                if cm:
                    class_name = cm.group(1)
                    break

            # Parse this class's RST content
            class_chunks, i = self._parse_class_block(lines, i, class_name, file_path)
            chunks.extend(class_chunks)

        return chunks

    # ── Per-class state machine ─────────────────────────────────────────
    def _parse_class_block(
        self,
        lines: list[str],
        start: int,
        class_name: str,
        file_path: str,
    ) -> tuple[list[Chunk], int]:
        """Parse a single class RST block starting at line index ``start``.

        Returns (chunks, next_line) where next_line is past the block.
        """
        chunks: list[Chunk] = []
        n = len(lines)
        i = start

        # Class-level state
        inherits_from: list[str] | None = None
        header_lines: list[str] = []
        class_chunk_emitted = False

        # Tables state (collect names/signatures while scanning)
        in_properties_table = False
        in_methods_table = False
        in_signals_table = False
        in_constructors_table = False
        in_operators_table = False
        in_theme_properties_table = False

        # Description sections state
        in_descriptions = False
        current_section: str | None = None  # sub-header name, e.g. "Signals"
        current_desc_lines: list[str] = []
        # Pending member (anchor was just seen, signature not yet collected)
        pending_member: dict | None = None

        # Emit class chunk as soon as we have basic info (anchors+inherits).
        # The header text gets accumulated until the first "Properties" / "Methods" /
        # "Signals" table OR the first descriptions group, whichever comes first.
        def emit_class_chunk(line_start: int, line_end: int) -> None:
            nonlocal class_chunk_emitted
            if class_chunk_emitted:
                return
            class_chunk_emitted = True
            text = self._build_class_text(
                class_name, inherits_from, header_lines,
            )
            docstring = self._join_clean(header_lines)[:500]
            chunks.append(Chunk(
                chunk_id=f"{class_name}::class",
                domain="godot",
                text=text,
                source_type="repo",
                chunk_type="class",
                class_name=class_name,
                name=class_name,
                inherits_from=inherits_from,
                docstring=docstring,
                source_file=file_path,
                line_start=line_start,
                line_end=line_end,
            ))

        line_start_class = i
        while i < n:
            line = lines[i]

            # End of RST code block
            if self.RST_BLOCK_END.match(line):
                i += 1
                break

            # Class anchor (e.g. .. _class_Node3D:) — override case-correct name
            if not inherits_from and not in_descriptions:
                m = self.CLASS_ANCHOR.match(line)
                if m:
                    class_name = m.group(1)  # override with case-correct name
                    i += 1
                    continue

            # Inherits line
            if not inherits_from:
                im = self.INHERITS_LINE.match(line)
                if im:
                    inherits_from = self._extract_ref_names(im.group(1))
                    i += 1
                    continue
                # Also try Inherited By (rare but valid)
                ibm = self.INHERITED_BY_LINE.match(line)
                if ibm:
                    i += 1
                    continue

            # Accumulate free-text class header content (Description, Tutorials, etc.)
            if (
                not in_descriptions
                and not in_properties_table
                and not in_methods_table
                and not in_signals_table
                and not in_constructors_table
                and not in_operators_table
                and not in_theme_properties_table
                and not self._is_section_separator_line(line)
                and not self._is_table_separator_line(line)
                and not line.lstrip().startswith(".. ")
                and line.strip()
            ):
                header_lines.append(line)
                i += 1
                continue

            # Table section headers (Properties, Methods, ...)
            if self.SECTION_PROPERTIES_TABLE.match(line):
                in_properties_table = True
                in_methods_table = in_signals_table = False
                in_constructors_table = in_operators_table = False
                in_theme_properties_table = False
                emit_class_chunk(line_start_class, i)
                i += 1
                continue
            if self.SECTION_METHODS_TABLE.match(line):
                in_methods_table = True
                in_properties_table = in_signals_table = False
                in_constructors_table = in_operators_table = False
                in_theme_properties_table = False
                emit_class_chunk(line_start_class, i)
                i += 1
                continue
            if self.SECTION_SIGNALS_TABLE.match(line):
                in_signals_table = True
                in_properties_table = in_methods_table = False
                in_constructors_table = in_operators_table = False
                in_theme_properties_table = False
                emit_class_chunk(line_start_class, i)
                i += 1
                continue
            if self.SECTION_CONSTRUCTORS_TABLE.match(line):
                in_constructors_table = True
                in_properties_table = in_methods_table = in_signals_table = False
                in_operators_table = in_theme_properties_table = False
                emit_class_chunk(line_start_class, i)
                i += 1
                continue
            if self.SECTION_OPERATORS_TABLE.match(line):
                in_operators_table = True
                in_properties_table = in_methods_table = in_signals_table = False
                in_constructors_table = in_theme_properties_table = False
                emit_class_chunk(line_start_class, i)
                i += 1
                continue
            if self.SECTION_THEME_PROPERTIES_TABLE.match(line):
                in_theme_properties_table = True
                in_properties_table = in_methods_table = in_signals_table = False
                in_constructors_table = in_operators_table = False
                emit_class_chunk(line_start_class, i)
                i += 1
                continue

            # Table separator lines (e.g. +---+---+)
            if self._is_table_separator_line(line):
                i += 1
                continue

            # Table row (e.g. | col1 | col2 |)
            if self.TABLE_ROW.match(line):
                emit_class_chunk(line_start_class, i)
                if in_properties_table:
                    self._extract_property_row(line, chunks, class_name, inherits_from, file_path, i)
                elif in_methods_table:
                    self._extract_method_row(line, chunks, class_name, "method", inherits_from, file_path, i)
                elif in_constructors_table:
                    self._extract_method_row(line, chunks, class_name, "constructor", inherits_from, file_path, i)
                elif in_operators_table:
                    self._extract_method_row(line, chunks, class_name, "operator", inherits_from, file_path, i)
                elif in_signals_table:
                    self._extract_signal_row(line, chunks, class_name, inherits_from, file_path, i)
                elif in_theme_properties_table:
                    self._extract_theme_property_row(line, chunks, class_name, inherits_from, file_path, i)
                i += 1
                continue

            # Empty line ends a table
            if not line.strip() and (
                in_properties_table
                or in_methods_table
                or in_signals_table
                or in_constructors_table
                or in_operators_table
                or in_theme_properties_table
            ):
                in_properties_table = in_methods_table = in_signals_table = False
                in_constructors_table = in_operators_table = in_theme_properties_table = False
                i += 1
                continue

            # Description group marker
            if self.SECTION_DESCRIPTIONS_GROUP.match(line):
                in_descriptions = True
                in_properties_table = in_methods_table = in_signals_table = False
                in_constructors_table = in_operators_table = in_theme_properties_table = False
                emit_class_chunk(line_start_class, i)
                i += 1
                continue

            # Sub-header within descriptions (Signals, Enumerations, ...)
            if in_descriptions and self.SECTION_SUBHEADER.match(line):
                # Flush pending member (if any) and any prior accumulated text
                if pending_member is not None:
                    self._emit_member_chunk(
                        pending_member, current_desc_lines,
                        chunks, class_name, inherits_from, file_path, i,
                    )
                    pending_member = None
                elif current_section and current_desc_lines:
                    # Text without a member anchor (rare; skip silently)
                    pass

                current_desc_lines = []
                sub_m = self.SECTION_SUBHEADER.match(line)
                current_section = sub_m.group(1)
                i += 1
                continue

            # Inside descriptions: collect member anchors
            if in_descriptions:
                # Flush previous member on item/section separator
                if (
                    line.strip() == "----"
                    or "classref-item-separator" in line
                    or "classref-section-separator" in line
                ):
                    if pending_member is not None:
                        self._emit_member_chunk(
                            pending_member, current_desc_lines,
                            chunks, class_name, inherits_from, file_path, i,
                        )
                        pending_member = None
                        current_desc_lines = []
                    i += 1
                    continue

                # Member anchor
                mm = self.MEMBER_ANCHOR.match(line)
                if mm:
                    # Flush previous member
                    if pending_member is not None:
                        self._emit_member_chunk(
                            pending_member, current_desc_lines,
                            chunks, class_name, inherits_from, file_path, i,
                        )
                    pending_member = {
                        "anchor_class": mm.group(1),
                        "member_type": mm.group(2),
                        "member_name": mm.group(3),
                    }
                    current_desc_lines = []
                    i += 1
                    continue

                # Enum anchor
                em = self.ENUM_ANCHOR.match(line)
                if em:
                    if pending_member is not None:
                        self._emit_member_chunk(
                            pending_member, current_desc_lines,
                            chunks, class_name, inherits_from, file_path, i,
                        )
                    pending_member = {
                        "anchor_class": class_name,
                        "member_type": "enum",
                        "member_name": em.group(1),
                    }
                    current_desc_lines = []
                    i += 1
                    continue

                # Skip RST directives (rst-class, tabs, code-block, etc.)
                if line.lstrip().startswith(".. "):
                    i += 1
                    continue

                # Skip classref-* markers
                if self.CLASSREF_GROUP.match(line):
                    i += 1
                    continue

                # Skip empty lines but keep them as paragraph breaks
                if not line.strip():
                    if current_desc_lines and current_desc_lines[-1] != "":
                        current_desc_lines.append("")
                    i += 1
                    continue

                # Regular description text → accumulate (cleaned)
                if pending_member is not None:
                    current_desc_lines.append(self._clean_rst(line))

            i += 1

        # Flush any pending member at end of class block
        if pending_member is not None:
            self._emit_member_chunk(
                pending_member, current_desc_lines,
                chunks, class_name, inherits_from, file_path, i,
            )

        # If the class chunk was never emitted (no tables, no descriptions group),
        # emit it now with whatever header we collected.
        if not class_chunk_emitted:
            text = self._build_class_text(class_name, inherits_from, header_lines)
            docstring = self._join_clean(header_lines)[:500]
            chunks.append(Chunk(
                chunk_id=f"{class_name}::class",
                domain="godot",
                text=text,
                source_type="repo",
                chunk_type="class",
                class_name=class_name,
                name=class_name,
                inherits_from=inherits_from,
                docstring=docstring,
                source_file=file_path,
                line_start=line_start_class,
                line_end=i,
            ))

        return chunks, i

    # ── Table row extractors ────────────────────────────────────────────
    def _extract_property_row(
        self,
        line: str,
        chunks: list[Chunk],
        class_name: str,
        inherits: list[str] | None,
        file_path: str,
        line_idx: int,
    ) -> None:
        """Extract a property name from a Properties table row (2nd column)."""
        for m in self.PROPERTY_TABLE_CELL.finditer(line):
            name = m.group(2)
            # Build minimal chunk; full description comes from description block
            chunks.append(self._make_minimal_chunk(
                class_name=class_name,
                chunk_type="property",
                name=name,
                signature=name,
                inherits=inherits,
                source_file=file_path,
                line_start=line_idx + 1,
                line_end=line_idx + 1,
            ))

    def _extract_method_row(
        self,
        line: str,
        chunks: list[Chunk],
        class_name: str,
        chunk_type: str,  # "method" | "operator" | "constructor"
        inherits: list[str] | None,
        file_path: str,
        line_idx: int,
    ) -> None:
        """Extract a method/operator/constructor name from the rightmost column."""
        for m in self.METHOD_TABLE_CELL.finditer(line):
            name = m.group(3)
            if m.group(2) != {
                "method": "method", "operator": "operator", "constructor": "constructor",
            }.get(chunk_type):
                # Skip mismatches (rare; conservative)
                pass
            chunks.append(self._make_minimal_chunk(
                class_name=class_name,
                chunk_type=chunk_type,
                name=name,
                signature=name,
                inherits=inherits,
                source_file=file_path,
                line_start=line_idx + 1,
                line_end=line_idx + 1,
            ))

    def _extract_signal_row(
        self,
        line: str,
        chunks: list[Chunk],
        class_name: str,
        inherits: list[str] | None,
        file_path: str,
        line_idx: int,
    ) -> None:
        for m in self.SIGNAL_TABLE_CELL.finditer(line):
            name = m.group(2)
            chunks.append(self._make_minimal_chunk(
                class_name=class_name,
                chunk_type="signal",
                name=name,
                signature=name,
                inherits=inherits,
                source_file=file_path,
                line_start=line_idx + 1,
                line_end=line_idx + 1,
            ))

    def _extract_theme_property_row(
        self,
        line: str,
        chunks: list[Chunk],
        class_name: str,
        inherits: list[str] | None,
        file_path: str,
        line_idx: int,
    ) -> None:
        for m in self.THEME_PROPERTY_TABLE_CELL.finditer(line):
            name = m.group(3)
            chunks.append(self._make_minimal_chunk(
                class_name=class_name,
                chunk_type="theme_property",
                name=name,
                signature=name,
                inherits=inherits,
                source_file=file_path,
                line_start=line_idx + 1,
                line_end=line_idx + 1,
            ))

    # ── Member description chunk emission ───────────────────────────────
    def _emit_member_chunk(
        self,
        member: dict,
        desc_lines: list[str],
        chunks: list[Chunk],
        class_name: str,
        inherits: list[str] | None,
        file_path: str,
        line_idx: int,
    ) -> None:
        member_type = member["member_type"]
        name = member["member_name"]
        chunk_type = self.MEMBER_TYPE_TO_CHUNK_TYPE.get(member_type, "section")

        # If the chunk_id for this member was already emitted from a table row,
        # remove that placeholder so the full description chunk replaces it.
        chunk_id = f"{class_name}::{chunk_type}::{name}"
        chunks[:] = [c for c in chunks if c.chunk_id != chunk_id]

        # Extract the signature from the first non-empty description line
        signature = self._extract_signature_from_desc(desc_lines, member_type, name)

        # Build text
        kind_label = chunk_type.replace("_", " ").capitalize()
        text_parts = [f"{kind_label}: {class_name}.{name}"]
        if signature and signature != name:
            text_parts.append(f"Signature: {signature}")
        if inherits:
            text_parts.append(f"Inherits: {' → '.join(inherits)}")
        if desc_lines:
            docstring = self._join_clean(desc_lines)
            if docstring:
                text_parts.append("")
                text_parts.append(docstring)

        text = "\n".join(text_parts)
        docstring_clean = self._join_clean(desc_lines)[:500]

        # Determine line range (best-effort: anchor was at this point)
        chunks.append(Chunk(
            chunk_id=chunk_id,
            domain="godot",
            text=text,
            source_type="repo",
            chunk_type=chunk_type,
            class_name=class_name,
            name=name,
            signature=signature,
            inherits_from=inherits,
            docstring=docstring_clean,
            source_file=file_path,
            line_start=line_idx,
            line_end=line_idx + len(desc_lines),
        ))

    def _extract_signature_from_desc(
        self,
        desc_lines: list[str],
        member_type: str,
        name: str,
    ) -> str | None:
        """Pull the signature line out of the description block."""
        chunk_type = self.MEMBER_TYPE_TO_CHUNK_TYPE.get(member_type, "section")
        for line in desc_lines:
            if not line.strip():
                continue
            # Fallback for cleaned text: just extract the bold name + params
            if chunk_type in ("method", "operator", "constructor"):
                fm = re.search(r"([\w@.]+)\s*\(([^)]*)\)", line)
                if fm and fm.group(1) == name:
                    return f"{fm.group(1)}({fm.group(2).strip()})" if fm.group(2).strip() else fm.group(1)
            elif chunk_type in ("property", "theme_property"):
                fp = re.search(r"(\w[\w@.]*)\s+([\w@.]+)(?:\s*=\s*(.+))?", line)
                if fp:
                    sig = f"{fp.group(1)} {fp.group(2)}"
                    if fp.group(3):
                        sig += f" = {fp.group(3)}"
                    return sig
            elif chunk_type == "signal":
                fs = re.search(r"([\w@.]+)\s*\(([^)]*)\)", line)
                if fs:
                    return f"{fs.group(1)}({fs.group(2).strip()})" if fs.group(2).strip() else fs.group(1)
            elif chunk_type == "constant":
                fc = re.search(r"(\w[\w@.]+)\s*=\s*(.+)", line)
                if fc:
                    return f"{fc.group(1)} = {fc.group(2)}"
            break
        # If fallback didn't match, try original regex approach
        for line in desc_lines:
            if not line.strip():
                continue
            if chunk_type in ("method", "operator", "constructor"):
                m = self.METHOD_SIGNATURE.search(line)
                if m:
                    sig = m.group(1).strip()
                    params = m.group(2).strip()
                    return f"{sig}({params})" if params else sig
                # Fallback: just use the bold name
                bm = re.search(r"\*\*([^*]+)\*\*", line)
                if bm:
                    return bm.group(1)
            elif chunk_type in ("property", "theme_property"):
                m = self.PROPERTY_SIGNATURE.search(line)
                if m:
                    type_str = m.group(1)
                    prop_name = m.group(2)
                    default = m.group(3)
                    sig = f"{type_str} {prop_name}"
                    if default:
                        sig += f" = {default}"
                    return sig
                bm = re.search(r"\*\*([^*]+)\*\*", line)
                if bm:
                    return bm.group(1)
            elif chunk_type == "signal":
                m = self.SIGNAL_SIGNATURE.match(line)
                if m:
                    return f"{m.group(1)}({m.group(2)})"
            elif chunk_type == "constant":
                m = self.CONSTANT_SIGNATURE.match(line)
                if m:
                    return f"{m.group(1)} = {m.group(2)}"
            elif chunk_type == "annotation":
                m = self.ANNOTATION_SIGNATURE.match(line)
                if m:
                    return f"{m.group(1)}({m.group(2)})" if m.group(2) else m.group(1)
            elif chunk_type == "enum":
                m = self.ENUM_SIGNATURE.match(line)
                if m:
                    return m.group(1)
            break
        return name

    # ── Helpers ─────────────────────────────────────────────────────────
    def _is_section_separator_line(self, line: str) -> bool:
        """A line that visually separates sections (e.g. '----' alone)."""
        return line.strip() == "----"

    def _is_table_separator_line(self, line: str) -> bool:
        """A line like '+-----+-----+' that separates table rows."""
        s = line.strip()
        return bool(s) and s.startswith("+") and s.endswith("+") and "-" in s

    def _make_minimal_chunk(
        self,
        class_name: str,
        chunk_type: str,
        name: str,
        signature: str | None,
        inherits: list[str] | None,
        source_file: str,
        line_start: int,
        line_end: int,
    ) -> Chunk:
        kind_label = chunk_type.replace("_", " ").capitalize()
        parts = [f"{kind_label}: {class_name}.{name}"]
        if inherits:
            parts.append(f"Inherits: {' → '.join(inherits)}")
        return Chunk(
            chunk_id=f"{class_name}::{chunk_type}::{name}",
            domain="godot",
            text="\n".join(parts),
            source_type="repo",
            chunk_type=chunk_type,
            class_name=class_name,
            name=name,
            signature=signature,
            inherits_from=inherits,
            docstring="",
            source_file=source_file,
            line_start=line_start,
            line_end=line_end,
        )

    def _build_class_text(
        self,
        class_name: str,
        inherits: list[str] | None,
        header_lines: list[str],
    ) -> str:
        parts = [f"Class: {class_name}"]
        if inherits:
            parts.append(f"extends {' → '.join(inherits)}")
        cleaned = self._join_clean(header_lines)
        if cleaned:
            parts.append("")
            parts.append(cleaned)
        return "\n".join(parts)

    def _join_clean(self, lines: list[str]) -> str:
        cleaned = [self._clean_rst(l) for l in lines if l.strip()]
        # Collapse multiple blank lines
        result: list[str] = []
        prev_blank = False
        for line in cleaned:
            is_blank = not line.strip()
            if is_blank and prev_blank:
                continue
            result.append(line)
            prev_blank = is_blank
        return "\n".join(result).strip()

    def _clean_rst(self, text: str) -> str:
        """Strip RST markup from a single line for clean embedding text."""
        for pattern, replacement in self.RST_MARKUP_CLEANUP:
            text = pattern.sub(replacement, text)
        # Collapse internal whitespace
        text = re.sub(r"[ \t]+", " ", text).strip()
        return text

    def _extract_ref_names(self, text: str) -> list[str]:
        """Extract class names from an **Inherits:** or similar line.

        Input: ':ref:`Node<class_Node>` **<** :ref:`Object<class_Object>`'
        Output: ['Node', 'Object']
        """
        names = []
        for m in self.REF_EXTRACT.finditer(text):
            name = m.group(1).strip()
            if name and name not in names:
                names.append(name)
        return names
