"""HyDE — Hypothetical Document Embeddings (Zero-Shot Dense Retrieval).

Improves retrieval quality by generating a hypothetical answer document
with an LLM and embedding that instead of the raw query. The hypothetical
document contains the same terminology and structure as the real technical
docs, so the embedding distance to real chunks is smaller.

Paper: https://arxiv.org/abs/2212.10496

Usage in hybrid_search::

    from hyde import generate_hypothetical_document, should_use_hyde
    if should_use_hyde(query):
        hyp_doc = generate_hypothetical_document(query)
        query_for_embedding = hyp_doc  # instead of raw query
    else:
        query_for_embedding = query

The LLM call is optional (env var ``KH_HYDE_ENABLED=1``). When disabled,
``generate_hypothetical_document()`` returns the raw query unchanged.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

_pkg_root = Path(__file__).resolve().parent.parent
if str(_pkg_root) not in sys.path:
    sys.path.insert(0, str(_pkg_root))


def is_hyde_enabled() -> bool:
    """Check if HyDE is enabled via env var. Default: disabled."""
    return os.environ.get("KH_HYDE_ENABLED", "0") == "1"


def should_use_hyde(query: str) -> bool:
    """Decide if HyDE should be used for a given query.

    HyDE is most beneficial for:
    - Questions (contain '?' or question words)
    - Longer queries (>5 words — short keyword queries don't benefit)

    Short keyword queries like "CharacterBody3D" are better embedded
    directly (BM25 already handles keyword overlap).
    """
    if not is_hyde_enabled():
        return False
    word_count = len(query.split())
    if word_count < 5:
        return False
    # Skip pure keyword queries (no spaces between identifiers)
    if word_count == 1:
        return False
    return True


def generate_hypothetical_document(query: str, timeout: float = 15.0) -> str:
    """Generate a hypothetical document for the query using an LLM.

    The LLM generates a short technical documentation paragraph that
    would answer the query. This paragraph is then embedded instead of
    the raw query, improving semantic matching.

    Args:
        query: The user's search query.
        timeout: Max seconds for the LLM call. On timeout or error,
            returns the raw query (graceful fallback).

    Returns:
        Hypothetical document text, or the raw query on error/timeout.
    """
    if not should_use_hyde(query):
        return query

    try:
        from model_manager import get_llm
        llm_entry = get_llm()
    except Exception:
        return query  # No LLM available — use raw query

    prompt = (
        "You are a technical documentation writer. Write a short "
        "paragraph (3-5 sentences) that would answer this question "
        "as if it were from a technical manual. Use technical "
        "terminology and be specific. Do not write 'The answer is' "
        "or any preamble — just the documentation paragraph.\n\n"
        f"Question: {query}\n\n"
        "Documentation paragraph:"
    )

    try:
        response = llm_entry["client"].chat(
            model=llm_entry["model"],
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.3, "num_predict": 200},
            keep_alive="24h",
            stream=False,
        )
        try:
            content = response.message.content.strip()
        except AttributeError:
            content = response["message"]["content"].strip()
    except Exception:
        return query  # LLM error — graceful fallback

    if not content or len(content) < 20:
        return query  # Empty/too short response — fallback

    # Prepend the original query for BM25 token overlap (HyDE for
    # embedding only, but BM25 still benefits from original keywords).
    # The caller uses this for embedding; BM25 uses the raw query.
    return content
