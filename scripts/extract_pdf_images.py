#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Image extraction from PDFs for Knowledge Hub Vision Retrieval Feature.
#
# This script imports PyMuPDF4LLM (AGPL-3.0, Artifex Software).
# It is a STANDALONE BUILD TOOL, NOT part of the MIT-licensed runtime.
# The MIT-licensed Knowledge Hub code NEVER imports pymupdf.
#
# See THIRD_PARTY_LICENSES.md for licensing details.
#
# Usage:
#   pip install -r requirements-pdf.txt
#   python scripts/extract_pdf_images.py --domain davinci_resolve
#   python scripts/extract_pdf_images.py --domain davinci_resolve --no-quality-check
#   python scripts/extract_pdf_images.py --domain davinci_resolve --limit 100

"""Extract images from PDF sources of a PDF domain.

For each PDF in ``domains/<domain>/sources/raw/*.pdf``:

1. Convert to Markdown via PyMuPDF4LLM with ``write_images=True`` so PNGs
   are written to ``domains/<domain>/images/<source-file>/<pdf>-<page>-<idx>.png``
   AND ``![](path)`` references are embedded in the Markdown.
2. Parse the Markdown to extract, for each image reference, the surrounding
   text context (±200 chars, TowardsDataScience context-aware best-practice).
3. Optional Quality-Check via Vision-LLM (Gemma 4 Cloud): classify each
   image as ``"good"`` (UI screenshot / diagram / illustration worth
   indexing) vs ``"poor"`` (logo / illegible / decorative). Disabled by
   default; enable via ``--quality-check`` (requires Ollama running).
4. Write ``chromadb_data/<domain>/image_manifest.json`` with one entry
   per image:

   .. code-block:: json

      {
        "image_id": "<domain>::img::<source_stem>::<page>::<idx>",
        "image_path": "domains/<domain>/images/<source_stem>/<pdf>-<page>-<idx>.png",
        "source_file": "<source_stem>.md",
        "pdf_file": "<pdf_filename>",
        "page": <page>,           # 0-based PDF page (PyMuPDF4LLM naming)
        "idx": <idx>,             # 0-based image index on that page
        "context_before": "<~200 chars before the image ref>",
        "context_after": "<~200 chars after the image ref>",
        "quality": "good" | "poor" | "unchecked",
        "quality_reason": "<short Vision-LLM explanation>"
      }

The manifest is consumed by ``caption_images.py`` (Task 3) and
``embed_images.py`` (Task 4). Only ``quality == "good"`` images proceed
to captioning + embedding (TowardsDataScience Rule: filter logos /
illegible early).
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
from pathlib import Path

# Make the repo root importable when run as a script.
_PKG_ROOT = Path(__file__).resolve().parent.parent
if str(_PKG_ROOT) not in sys.path:
    sys.path.insert(0, str(_PKG_ROOT))

# AGPL imports — keep them at module top so the license boundary is explicit.
import pymupdf  # AGPL-3.0
import pymupdf4llm  # AGPL-3.0

from mcp_servers.knowledge_hub import config as _config
from mcp_servers.knowledge_hub.config import (
    domain_images_dir,
    domain_image_manifest_path,
)


# ── Constants ──────────────────────────────────────────────────────────────

# Domain name validation (must match `^[a-z0-9_]+$`).
_DOMAIN_NAME_RE = re.compile(r"^[a-z0-9_]+$")

# Context window around image refs in the converted Markdown (chars).
_CONTEXT_CHARS = 200

# Regex matching PyMuPDF4LLM image references: ![](path)
_IMAGE_REF_RE = re.compile(r"!\[\]\(([^)]+\.png)\)")

# Regex extracting (page, idx) from a PyMuPDF4LLM image filename of the
# form ``<pdf_stem>-<page>-<idx>.png`` (page is 1-based, idx 0-based).
_IMG_FILE_RE = re.compile(r"^(?P<stem>.+?)-(?P<page>\d+)-(?P<idx>\d+)\.png$")


# ── Helpers ────────────────────────────────────────────────────────────────


def _source_stem_for_pdf(pdf_path: Path) -> str:
    """Map a raw PDF path to the existing converted-Markdown source stem.

    The conversion was done by ``parse_pdf_to_markdown.py`` which wrote
    ``domains/<domain>/sources/<kebab-stem>.md``. The mapping is
    convention-based: lowercase + CamelCase splitting + spaces/dots →
    hyphens. We verify the target .md exists and fall back to the PDF
    stem if no match is found (caller will warn).
    """
    name = pdf_path.stem
    # CamelCase boundary splitting: "FairlightLiveUserManual" →
    # "Fairlight Live User Manual". Use the same boundary regex as the
    # BM25 tokenizer (lowercase→UPPER, UPPER→Capitalized) so acronyms
    # stay intact.
    spaced = re.sub(r"(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])", " ", name)
    # Common substitutions
    candidate = spaced.lower().replace(" ", "-").replace("_", "-")
    # Collapse repeated hyphens
    candidate = re.sub(r"-+", "-", candidate)
    return candidate


def _normalise_for_match(s: str) -> str:
    """Aggressive normalisation for fuzzy PDF→MD matching.

    Lowercases, drops hyphens/underscores/dots/spaces entirely so that
    ``davinci-resolve-20-advanced-visual-effects`` and
    ``da-vinci-resolve-20-advanced-visual-effects`` both collapse to
    ``davinciresolve20advancedvisual.effects``. The dot is kept in
    ``.3`` style versions so ``20.3`` stays distinguishable from
    ``203``. Actually we drop dots too — versions like 20.3 vs 203 are
    not ambiguous in practice because the source-stem includes the
    version separator.
    """
    return re.sub(r"[-_.\s]", "", s.lower())


def _find_pdf_to_source_mapping(domain: str) -> dict[str, str]:
    """Build a {pdf_filename: source_md_stem} map by matching PDFs to
    existing converted Markdown files in ``sources/``.

    Matching is aggressive-fuzzy (drop all separators, lowercase) so
    both CamelCase-splits and hyphenated forms match the hand-curated
    .md filenames. Falls back to the CamelCase-split normalised PDF stem
    if no .md match is found.
    """
    sources_dir = _config.DOMAINS_DIR / domain / "sources"
    raw_dir = _config.DOMAINS_DIR / domain / "sources" / "raw"
    mapping: dict[str, str] = {}

    if not raw_dir.is_dir():
        return mapping

    # Build aggressive-normalised -> actual_stem index of existing .md files.
    md_files: dict[str, str] = {}
    if sources_dir.is_dir():
        for md in sources_dir.glob("*.md"):
            key = _normalise_for_match(md.stem)
            md_files[key] = md.stem

    for pdf in sorted(raw_dir.glob("*.pdf")):
        camel_stem = _source_stem_for_pdf(pdf)
        # Try aggressive normalisation of the CamelCase-split stem first.
        key = _normalise_for_match(camel_stem)
        if key in md_files:
            mapping[pdf.name] = md_files[key]
            continue
        # Fallback: try the raw PDF stem (no CamelCase split) with
        # aggressive normalisation — catches "DaVinci" which should NOT
        # be split into "Da Vici".
        raw_key = _normalise_for_match(pdf.stem)
        if raw_key in md_files:
            mapping[pdf.name] = md_files[raw_key]
            continue
        # No match — use the CamelCase-split stem; caller will warn.
        mapping[pdf.name] = camel_stem

    return mapping


def _extract_context(markdown: str, image_ref_start: int, image_ref_end: int) -> tuple[str, str]:
    """Extract ±200 chars of context around an image-reference position.

    The current image ref spans markdown[image_ref_start:image_ref_end];
    it is excluded from both the before/after context windows so the
    captioning prompt does not see the image's own filename. Other
    ![](path.png) refs in the window are also stripped. A truncated
    partial ref at the window boundary is removed via a second regex
    that matches incomplete ![](... runs (no closing paren).
    """
    start = max(0, image_ref_start - _CONTEXT_CHARS)
    end = min(len(markdown), image_ref_end + _CONTEXT_CHARS)
    before = markdown[start:image_ref_start]
    after = markdown[image_ref_end:end]
    # Strip complete image refs from the context.
    before = _IMAGE_REF_RE.sub("", before)
    after = _IMAGE_REF_RE.sub("", after)
    # Strip truncated image refs at the window boundaries (e.g.
    # "![](/Users/.../domai" with no closing paren, or an orphaned
    # "...path.png)" fragment from a ref that started before the window).
    before = re.sub(r"!\[\]\([^)]*$", "", before)   # truncated at end
    before = re.sub(r"^[^\s]*\.png\)\s*", "", before)  # orphaned .png) at start
    after = re.sub(r"!\[\]\([^)]*$", "", after)     # truncated at end
    after = re.sub(r"^[^\s]*\.png\)\s*", "", after)    # orphaned .png) at start
    # Collapse whitespace.
    before = re.sub(r"\s+", " ", before).strip()
    after = re.sub(r"\s+", " ", after).strip()
    return before, after


def _convert_pdf_with_images(
    pdf_path: Path,
    images_out_dir: Path,
    pages: list[int] | None = None,
) -> str:
    """Convert a single PDF to Markdown, writing PNGs to ``images_out_dir``.

    ``pages`` is an optional 1-based page list to limit conversion
    (useful for testing / --limit). ``None`` converts the whole PDF.
    """
    images_out_dir.mkdir(parents=True, exist_ok=True)
    kwargs = {
        "write_images": True,
        "image_path": str(images_out_dir),
        "page_separators": True,
    }
    if pages is not None:
        kwargs["pages"] = pages
    return pymupdf4llm.to_markdown(str(pdf_path), **kwargs)


def _parse_image_refs(
    markdown: str,
    image_root: Path,
    source_stem: str,
    pdf_filename: str,
    domain: str,
) -> list[dict]:
    """Parse ``![](path)`` refs from Markdown into manifest entries.

    Each entry is augmented with page / idx parsed from the image
    filename, plus context_before / context_after extracted from the
    Markdown around the ref position.
    """
    entries: list[dict] = []
    seen_paths: set[str] = set()

    for match in _IMAGE_REF_RE.finditer(markdown):
        abs_path = match.group(1)
        filename = Path(abs_path).name
        # Dedupe: PyMuPDF4LLM may emit the same image ref multiple times
        # if the same PNG is referenced on several pages.
        if filename in seen_paths:
            continue
        seen_paths.add(filename)

        m = _IMG_FILE_RE.match(filename)
        if not m:
            print(f"[WARN]  Unparseable image filename: {filename} — skipping")
            continue
        page = int(m.group("page"))
        idx = int(m.group("idx"))

        # Resolve a relative path under domains/<domain>/images/<source_stem>/.
        # The image_path passed to PyMuPDF4LLM is absolute; we re-anchor
        # the stored path to the repo-relative form for portability.
        rel_path = (
            domain_images_dir(domain) / source_stem / filename
        )
        # Make it repo-relative (no leading /).
        try:
            rel_str = str(rel_path.relative_to(_config.HUB_ROOT))
        except ValueError:
            rel_str = str(rel_path)

        # Sanity: the PNG file must exist on disk.
        if not Path(abs_path).exists():
            print(f"[WARN]  Image file missing: {abs_path} — skipping")
            continue

        context_before, context_after = _extract_context(markdown, match.start(), match.end())

        entry = {
            "image_id": f"{domain}::img::{source_stem}::{page}::{idx}",
            "image_path": rel_str,
            "source_file": f"{source_stem}.md",
            "pdf_file": pdf_filename,
            "page": page,
            "idx": idx,
            "context_before": context_before,
            "context_after": context_after,
            "quality": "unchecked",
            "quality_reason": "",
        }
        entries.append(entry)

    return entries


# ── Quality check via Vision-LLM (optional) ────────────────────────────────


def _encode_image_b64(image_path: Path) -> str:
    """Base64-encode an image for Ollama vision API."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def _quality_check_image(
    image_path: Path,
    context_before: str,
    context_after: str,
    llm_entry: dict,
) -> tuple[str, str]:
    """Ask the Vision-LLM whether an image is worth indexing.

    Returns ``(quality, reason)`` where quality is ``"good"`` or
    ``"poor"``. On any error returns ``"unchecked"`` with the error msg
    (caller keeps the image in the manifest but flags it for manual
    review).
    """
    if not image_path.exists():
        return "unchecked", f"image file missing: {image_path}"

    try:
        b64 = _encode_image_b64(image_path)
    except Exception as e:
        return "unchecked", f"b64 encode failed: {type(e).__name__}: {e}"

    prompt = (
        "You are a quality classifier for screenshots from a technical "
        "DaVinci Resolve handbook. Look at the image and decide if it is "
        "WORTH indexing in a knowledge retrieval system.\n\n"
        "Answer GOOD if the image shows: a UI screenshot, a dialog, a "
        "panel, a workflow diagram, a chart, an illustration that conveys "
        "information, or any figure a reader would search for.\n"
        "Answer POOR if the image is: a logo, a decorative icon, an "
        "illegible thumbnail, a blank page, or purely ornamental.\n\n"
        f"Surrounding text context (for hint only): "
        f"before='{context_before[:120]}' after='{context_after[:120]}'\n\n"
        "Reply with EXACTLY one line: GOOD <short reason> or POOR <short reason>."
    )

    try:
        response = llm_entry["client"].chat(
            model=llm_entry["model"],
            messages=[{
                "role": "user",
                "content": prompt,
                "images": [b64],
            }],
            options={"temperature": 0, "num_predict": 60},
            keep_alive="24h",
            stream=False,
        )
        try:
            raw = response.message.content.strip()
        except AttributeError:
            raw = response["message"]["content"].strip()
    except Exception as e:
        return "unchecked", f"vision-llm error: {type(e).__name__}: {e}"

    # Parse the one-line response.
    line = raw.splitlines()[0].strip() if raw else ""
    low = line.lower()
    if low.startswith("good"):
        return "good", line
    if low.startswith("poor"):
        return "poor", line
    # Unparseable → keep unchecked.
    return "unchecked", f"unparseable response: {line[:120]}"


# ── Main pipeline ──────────────────────────────────────────────────────────


def extract_domain_images(
    domain: str,
    quality_check: bool = False,
    limit: int | None = None,
    pdf_filter: str | None = None,
) -> dict:
    """Extract images for a domain. Returns a summary dict.

    Args:
        domain: Domain name.
        quality_check: If True, classify each image via Vision-LLM.
        limit: Optional cap on the number of PDFs processed (after
            sorting). Useful for testing.
        pdf_filter: Optional substring filter on PDF filenames.
    """
    raw_dir = _config.DOMAINS_DIR / domain / "sources" / "raw"
    if not raw_dir.is_dir():
        raise FileNotFoundError(
            f"No raw PDF directory for domain '{domain}': {raw_dir}"
        )

    pdfs = sorted(raw_dir.glob("*.pdf"))
    if pdf_filter:
        pdfs = [p for p in pdfs if pdf_filter in p.name]
    if limit is not None:
        pdfs = pdfs[:limit]

    if not pdfs:
        raise FileNotFoundError(
            f"No PDFs found in {raw_dir}"
            + (f" matching '{pdf_filter}'" if pdf_filter else "")
        )

    pdf_to_source = _find_pdf_to_source_mapping(domain)

    # Optional Vision-LLM for quality check.
    llm_entry = None
    if quality_check:
        from model_manager import get_llm, DEFAULT_LLM_MODEL
        from contextualize_chunks import check_ollama_available
        llm_entry = get_llm()
        check_ollama_available(llm_entry)
        print(f"[INFO]  Quality-check enabled (model={llm_entry['model']})")

    manifest: list[dict] = []
    summary = {
        "domain": domain,
        "pdfs_processed": 0,
        "images_extracted": 0,
        "images_good": 0,
        "images_poor": 0,
        "images_unchecked": 0,
    }

    for pdf_path in pdfs:
        source_stem = pdf_to_source.get(pdf_path.name, _source_stem_for_pdf(pdf_path))
        # Sanity: warn if the corresponding .md does not exist.
        md_path = _config.DOMAINS_DIR / domain / "sources" / f"{source_stem}.md"
        if not md_path.exists():
            print(f"[WARN]  No converted .md for {pdf_path.name} "
                  f"(expected {md_path.name}) — using normalised stem '{source_stem}'")

        out_dir = domain_images_dir(domain) / source_stem
        print(f"[INFO]  Converting {pdf_path.name} → {out_dir}")
        try:
            md_text = _convert_pdf_with_images(pdf_path, out_dir)
        except Exception as e:
            print(f"[ERROR] Conversion failed for {pdf_path.name}: "
                  f"{type(e).__name__}: {e}")
            continue

        entries = _parse_image_refs(
            md_text, out_dir, source_stem, pdf_path.name, domain
        )
        summary["pdfs_processed"] += 1

        # Quality check (optional).
        if quality_check and llm_entry is not None:
            for entry in entries:
                abs_img = _config.HUB_ROOT / entry["image_path"]
                q, reason = _quality_check_image(
                    abs_img,
                    entry["context_before"],
                    entry["context_after"],
                    llm_entry,
                )
                entry["quality"] = q
                entry["quality_reason"] = reason
                if q == "good":
                    summary["images_good"] += 1
                elif q == "poor":
                    summary["images_poor"] += 1
                else:
                    summary["images_unchecked"] += 1
        else:
            for entry in entries:
                entry["quality"] = "unchecked"
                entry["quality_reason"] = ""
                summary["images_unchecked"] += 1

        summary["images_extracted"] += len(entries)
        manifest.extend(entries)
        print(f"[INFO]  {pdf_path.name}: {len(entries)} images extracted")

    # Write manifest.
    manifest_path = domain_image_manifest_path(domain)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(
            {"summary": summary, "images": manifest},
            f, indent=2, ensure_ascii=False,
        )
    print(f"[OK]    Manifest written: {manifest_path} "
          f"({summary['images_extracted']} images, "
          f"{summary['images_good']} good, "
          f"{summary['images_poor']} poor, "
          f"{summary['images_unchecked']} unchecked)")
    return summary


# ── CLI ────────────────────────────────────────────────────────────────────


def _build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="extract_pdf_images",
        description=(
            "Extract images from PDF sources of a domain (Vision Retrieval "
            "Feature). AGPL build tool — uses PyMuPDF4LLM."
        ),
    )
    p.add_argument(
        "--domain", required=True,
        help="Domain name (must match ^[a-z0-9_]+$).",
    )
    p.add_argument(
        "--quality-check", action="store_true",
        help="Classify each image via Vision-LLM (good/poor). "
             "Requires Ollama running with a vision model.",
    )
    p.add_argument(
        "--no-quality-check", action="store_true",
        help="Skip Vision-LLM quality check (default). All images get "
             "quality='unchecked' and proceed to captioning.",
    )
    p.add_argument(
        "--limit", type=int, default=None,
        help="Only process the first N PDFs (after sorting). Useful for testing.",
    )
    p.add_argument(
        "--pdf-filter", default=None,
        help="Substring filter on PDF filenames (e.g. 'Fairlight').",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_arg_parser().parse_args(argv)

    if not _DOMAIN_NAME_RE.match(args.domain):
        print(f"[ERROR] Invalid domain name '{args.domain}' — "
              "must match ^[a-z0-9_]+$")
        return 1

    quality_check = args.quality_check and not args.no_quality_check

    try:
        extract_domain_images(
            domain=args.domain,
            quality_check=quality_check,
            limit=args.limit,
            pdf_filter=args.pdf_filter,
        )
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        return 1
    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
