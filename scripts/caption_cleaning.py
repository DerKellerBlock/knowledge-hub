"""Caption cleaning for Vision Retrieval Feature.

Strips DaVinci PDF header/footer noise from context-aware captions so BM25
and embedding models see clean descriptive text instead of page numbers,
chapter titles, and Unicode decorative bars.

Patterns stripped:
- ``--- end of page=N ---`` (PyMuPDF4LLM page markers)
- DaVinci section headers (``Fairlight Live | Section **N**``)
- Chapter headers (``Color | Chapter 136 Color Warper **3179**``)
- Bold page numbers (``**4**``, ``**13**``)
- Bold section titles (``**Using ATEM Switchers**``)
- Unicode decorative bars (█▓▒░, U+FFFD replacement chars, backspace)
- Markdown headers (``##### Welcome``, ``#### **Controls**``)
- Bare section title fragments (short non-sentence text outside [IMAGE: ...])

Keeps:
- ``[IMAGE: ...]`` descriptions (protected throughout)
- Actual handbook text that forms sentences (contains period/comma)

Usage in caption_images.py::

    from caption_cleaning import clean_caption
    full_caption = f"{cb} [IMAGE: {description}] {ca}".strip()
    full_caption = clean_caption(full_caption)
    put_cached(conn, image_id, img_hash, model_name, full_caption)
"""

from __future__ import annotations

import re

# ── Cleaning patterns ──────────────────────────────────────────────────────

END_OF_PAGE_RE = re.compile(r'--- end of page=\d+ ---')
DV_HEADER_RE = re.compile(
    r'[A-Z][a-zA-Z]+ (?:Live|Page|Studio|Audio|Resolve) \| [^\n]*?\*\*\d+\*\*'
)
CHAPTER_RE = re.compile(
    r'[A-Z][a-zA-Z]+ \| Chapter \d+ [^\n]*?\*\*\d+\*\*'
)
PAGE_NUM_RE = re.compile(r'\*\*\d+\*\*')
BOLD_TITLE_RE = re.compile(r'\*\*[A-Z][a-zA-Z\s]+\*\*')
UNICODE_BAR_RE = re.compile(r'[\u2500-\u259f\u2580-\u259f\x08\u0080-\u009f\ufffd]+')
MD_HEADER_RE = re.compile(r'#{1,6}\s+')

# Standalone "Word | Word **N**" pattern (catches section headers not
# matched by DV_HEADER_RE, e.g. "Fusion | Effects **42**")
SECTION_PIPE_RE = re.compile(
    r'[A-Z][a-zA-Z]+ \| [A-Z][a-zA-Z\s]+\s*\*\*\d+\*\*'
)


def clean_caption(raw: str) -> str:
    """Clean a context-aware caption by stripping DaVinci PDF header/footer noise.

    Strips:
    - ``--- end of page=N ---`` page markers
    - DaVinci section headers (``Fairlight Live | Section **N**``)
    - Chapter headers (``Color | Chapter 136 Color Warper **3179**``)
    - Bold page numbers (``**4**``, ``**13**``)
    - Bold section titles (``**Using ATEM Switchers**``)
    - Unicode decorative bars and U+FFFD replacement characters
    - Markdown headers (``##### Welcome``, ``#### **Controls**``)
    - Bare section title fragments (short non-sentence text outside
      ``[IMAGE: ...]`` blocks — e.g. ``Control Room Meter Studio Meter
      Loudness Meter``)

    Keeps:
    - ``[IMAGE: ...]`` descriptions (protected throughout)
    - Actual handbook text that forms sentences (contains period/comma)

    Args:
        raw: The raw context-aware caption (context_before +
            ``[IMAGE: description]`` + context_after).

    Returns:
        Cleaned caption with noise stripped and whitespace collapsed.
    """
    if not raw:
        return ""
    text = raw

    # 1. Strip --- end of page=N ---
    text = END_OF_PAGE_RE.sub(' ', text)

    # 2. Strip DaVinci section headers (most specific first)
    text = CHAPTER_RE.sub(' ', text)
    text = DV_HEADER_RE.sub(' ', text)
    text = SECTION_PIPE_RE.sub(' ', text)

    # 3. Strip standalone **N** page numbers
    text = PAGE_NUM_RE.sub(' ', text)

    # 4. Strip bold section titles: **Using ATEM Switchers**
    text = BOLD_TITLE_RE.sub(' ', text)

    # 5. Strip Unicode decorative bars and control chars + U+FFFD
    text = UNICODE_BAR_RE.sub(' ', text)

    # 6. Strip Markdown headers (####, #####, etc.)
    text = MD_HEADER_RE.sub(' ', text)

    # 7. Strip leftover ** from broken bold markers
    text = re.sub(r'\*\*', ' ', text)

    # 8. Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # 9. Remove leading/trailing fragments that are just section titles
    # (short non-sentence text outside [IMAGE: ...] blocks)
    parts = re.split(r'(\[IMAGE:[^\]]+\])', text)
    cleaned_parts: list[str] = []
    for part in parts:
        if part.startswith('[IMAGE:'):
            cleaned_parts.append(part)
        else:
            words = part.strip().split()
            if words and len(part.strip()) < 80:
                has_sentence = any(
                    w.endswith('.') or w.endswith(',') or w.endswith(';')
                    for w in words
                )
                if not has_sentence and len(words) >= 3:
                    # Likely a header/title fragment — skip
                    continue
            cleaned_parts.append(part)

    text = ' '.join(cleaned_parts)
    text = re.sub(r'\s+', ' ', text).strip()
    return text
