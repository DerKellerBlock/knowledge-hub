#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# PDF → Markdown converter for Knowledge Hub.
#
# This script imports PyMuPDF4LLM (AGPL-3.0, Artifex Software).
# It is a STANDALONE BUILD TOOL, NOT part of the MIT-licensed runtime.
# The MIT-licensed Knowledge Hub code NEVER imports pymupdf.
#
# See THIRD_PARTY_LICENSES.md for licensing details.
#
# Usage:
#   pip install -r requirements-pdf.txt
#   python scripts/parse_pdf_to_markdown.py --pdf <input.pdf> --out <output.md>

"""Convert a PDF to section-aware Markdown using PyMuPDF4LLM.

Outputs GitHub-compatible Markdown with:
- # / ## / ### heading hierarchy derived from font sizes
- Tables as GFM pipe tables
- Correct reading order for multi-column pages
- Page number metadata preserved as HTML comments
"""

import argparse
import sys
from pathlib import Path

import pymupdf          # AGPL-3.0
import pymupdf4llm      # AGPL-3.0


def convert_pdf(pdf_path: Path, out_path: Path) -> dict:
    """Convert a PDF to section-aware Markdown.

    Returns a summary dict with stats.
    """
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    # Phase 1a: Markdown extraction via PyMuPDF4LLM
    print(f"[INFO]  Converting: {pdf_path.name}")
    md_text = pymupdf4llm.to_markdown(str(pdf_path))

    if not md_text or not md_text.strip():
        raise RuntimeError(f"PDF produced empty Markdown: {pdf_path}")

    # Phase 1b: Extract TOC for metadata (optional, appended as comment)
    doc = pymupdf.open(str(pdf_path))
    toc = doc.get_toc()  # [[level, title, page], ...]
    doc.close()

    # Build header comment with TOC summary
    toc_lines = []
    if toc:
        toc_lines.append("<!-- TOC")
        for level, title, page in toc:
            indent = "  " * (level - 1)
            toc_lines.append(f"{indent}- {title} (p.{page})")
        toc_lines.append("-->")
        toc_lines.append("")

    full_md = "\n".join(toc_lines) + md_text

    # Write output
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(full_md, encoding="utf-8")

    stats = {
        "pdf": str(pdf_path),
        "output": str(out_path),
        "chars": len(full_md),
        "toc_entries": len(toc),
        "headings": full_md.count("\n# ") + full_md.count("\n## ") + full_md.count("\n### "),
    }
    print(f"[OK]    {pdf_path.name} → {out_path.name} "
          f"({stats['chars']} chars, {stats['toc_entries']} TOC entries, "
          f"{stats['headings']} headings)")
    return stats


def main():
    parser = argparse.ArgumentParser(
        description="PDF → Markdown converter (AGPL build tool, uses PyMuPDF4LLM)"
    )
    parser.add_argument("--pdf", required=True, type=Path, help="Input PDF file")
    parser.add_argument("--out", required=True, type=Path, help="Output Markdown file")
    args = parser.parse_args()

    try:
        convert_pdf(args.pdf, args.out)
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()