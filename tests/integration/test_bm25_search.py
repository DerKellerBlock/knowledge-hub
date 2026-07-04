"""Integration tests for bm25_search with a real (small) index."""

import pytest

pytestmark = pytest.mark.integration


def test_bm25_finds_node3d_results(indexed_dummy):
    """BM25 should find results for 'Node3D rotate'."""
    from bm25_search import bm25_search

    results = bm25_search(indexed_dummy, "Node3D rotate", top_k=10)
    assert len(results) >= 1
    assert results[0]["score"] > 0
    assert results[0]["match_type"] == "bm25"


def test_bm25_no_results_for_gibberish(indexed_dummy):
    """BM25 should return empty list for non-matching query."""
    from bm25_search import bm25_search

    results = bm25_search(indexed_dummy, "zzznonexistentword12345", top_k=10)
    assert results == []


def test_bm25_top_k_limits_results(indexed_dummy):
    """top_k should limit the number of results."""
    from bm25_search import bm25_search

    results = bm25_search(indexed_dummy, "Node3D", top_k=1)
    assert len(results) <= 1


def test_bm25_score_positive(indexed_dummy):
    """All returned results should have positive scores."""
    from bm25_search import bm25_search

    results = bm25_search(indexed_dummy, "camera follow", top_k=10)
    for r in results:
        assert r["score"] > 0


def test_bm25_tokenized_query(indexed_dummy):
    """BM25 should handle multi-word queries."""
    from bm25_search import bm25_search

    results = bm25_search(indexed_dummy, "audio bus volume", top_k=10)
    assert len(results) >= 1


# ── Phase 3.2 Contextual BM25 (use_context_prefix) ────────────────────────


def _make_chunk(chunk_id: str, text: str,
                context_prefix: "str | None" = None,
                name: "str | None" = None,
                signature: "str | None" = None):
    """Build a minimal Chunk for BM25 corpus construction."""
    from parser_base import Chunk
    return Chunk(
        chunk_id=chunk_id,
        domain="ctx_test",
        text=text,
        source_type="repo",
        chunk_type=None,
        source_file="src.md",
        context_prefix=context_prefix,
        name=name,
        signature=signature,
    )


def _score_for(bm25_data: dict, chunk_id: str, query: str) -> float:
    """Return the BM25 score of ``chunk_id`` for ``query`` from a loaded
    index dict (``_load_index`` result)."""
    from bm25_search import tokenize
    chunk_ids = bm25_data["chunk_ids"]
    scores = bm25_data["index"].get_scores(tokenize(query))
    return float(scores[chunk_ids.index(chunk_id)])


def _doc_tokens(bm25_data: dict, chunk_id: str) -> set:
    """Return the set of tokens present in the BM25 corpus for ``chunk_id``.

    ``BM25Okapi`` exposes ``doc_freqs`` (a list of ``{token: tf}`` dicts
    per document). Inspecting token presence directly avoids the BM25 IDF
    quirk where a token that appears in only one of N=2 documents gets
    ``idf = log((N - n + 0.5) / (n + 0.5)) = log(1) = 0`` and thus a
    score of 0 even though the token IS in the corpus.
    """
    chunk_ids = bm25_data["chunk_ids"]
    idx = chunk_ids.index(chunk_id)
    return set(bm25_data["index"].doc_freqs[idx].keys())


def test_build_bm25_index_use_context_prefix_false(tmp_hub):
    """Default ``use_context_prefix=False`` → BM25 corpus uses
    tokenize(chunk.text), context_prefix is ignored (D1 backward-compat).

    Verified via ``doc_freqs``: a token that appears ONLY in the
    context_prefix ("characterbody") must be absent from chunk A's BM25
    corpus when the default build is used. We inspect ``doc_freqs``
    directly because BM25Okapi IDF yields score 0 for single-doc tokens
    on a 2-document corpus (idf = log(1) = 0), which would mask the
    presence/absence signal.
    """
    from bm25_search import build_bm25_index, _load_index, tokenize

    chunks = [
        _make_chunk("ctx_test::a", "rotate_y Node3D rotation",
                    context_prefix="CharacterBody3D rotation"),
        _make_chunk("ctx_test::b", "camera follow target",
                    context_prefix="Camera3D follow"),
    ]
    assert build_bm25_index("ctx_test", chunks, use_context_prefix=False)
    data = _load_index("ctx_test")
    tokens_a = _doc_tokens(data, "ctx_test::a")
    # "characterbody" only appears in chunk A's context_prefix — with the
    # default build it must NOT be in the BM25 corpus.
    assert "character" not in tokens_a, (
        "Default build leaked context_prefix token into BM25 corpus (D1 break)"
    )
    # Sanity: a text token ("rotate") is present. (The tokenizer splits
    # "rotate_y" into ["rotate", "y"] via the underscore/non-word boundary.)
    assert "rotate" in tokens_a, (
        f"Text token missing from default BM25 corpus: {tokens_a}"
    )


def test_build_bm25_index_use_context_prefix_true(tmp_hub):
    """``use_context_prefix=True`` → corpus contains context_prefix tokens
    (Phase 3.2 Contextual BM25). Verified via ``doc_freqs``: the
    context_prefix-only token "character" now appears in chunk A's
    BM25 corpus.
    """
    from bm25_search import build_bm25_index, _load_index

    chunks = [
        _make_chunk("ctx_test::a", "rotate_y Node3D rotation",
                    context_prefix="CharacterBody3D rotation"),
        _make_chunk("ctx_test::b", "camera follow target",
                    context_prefix="Camera3D follow"),
    ]
    assert build_bm25_index("ctx_test", chunks, use_context_prefix=True)
    data = _load_index("ctx_test")
    tokens_a = _doc_tokens(data, "ctx_test::a")
    tokens_b = _doc_tokens(data, "ctx_test::b")
    # "character" is only in chunk A's context_prefix — with
    # contextual BM25 it must now be in chunk A's corpus.
    assert "character" in tokens_a, (
        "context_prefix token missing in contextual BM25 corpus"
    )
    # Chunk B has no "characterbody" → not in its corpus (no false positive).
    assert "character" not in tokens_b, (
        "context_prefix token leaked into chunk B (wrong chunk)"
    )


def test_build_bm25_index_use_context_prefix_none_chunk(tmp_hub):
    """Defensive: a chunk with ``context_prefix=None`` falls back to
    tokenize(chunk.text) even when ``use_context_prefix=True``."""
    from bm25_search import build_bm25_index, _load_index

    chunks = [
        _make_chunk("ctx_test::a", "rotate_y Node3D rotation",
                    context_prefix=None),
    ]
    assert build_bm25_index("ctx_test", chunks, use_context_prefix=True)
    data = _load_index("ctx_test")
    tokens_a = _doc_tokens(data, "ctx_test::a")
    # No context_prefix → "characterbody" must not be in the corpus.
    assert "character" not in tokens_a, (
        "None context_prefix should fall back to tokenize(text)"
    )
    # Text token still present (tokenizer splits "rotate_y" → ["rotate","y"]).
    assert "rotate" in tokens_a


def test_build_bm25_index_backward_compatible(tmp_hub):
    """Calling ``build_bm25_index`` without ``use_context_prefix`` keeps
    the legacy default (False) — no behaviour change for existing
    callers (productive godot/davinci_resolve builds, integration tests)."""
    from bm25_search import build_bm25_index, _load_index

    chunks = [
        _make_chunk("ctx_test::a", "rotate_y Node3D rotation",
                    context_prefix="CharacterBody3D rotation"),
    ]
    # No use_context_prefix kwarg → default False.
    assert build_bm25_index("ctx_test", chunks)
    data = _load_index("ctx_test")
    tokens_a = _doc_tokens(data, "ctx_test::a")
    # context_prefix token must NOT leak (default path).
    assert "character" not in tokens_a, (
        "Default kwarg should equal use_context_prefix=False"
    )
    # Text token still present.
    assert "rotate" in tokens_a


def test_contextual_bm25_tf_increase(tmp_hub):
    """BS-4: ``use_context_prefix=True`` adds query-keyword tokens from
    context_prefix to a chunk's BM25 corpus that would otherwise be absent.

    Setup (3 chunks):

      * Chunk A: context_prefix="CharacterBody3D rotation",
                 text="func rotate_y()"  → short text, no query keywords.
      * Chunk B: context_prefix=None,
                 text="CharacterBody3D rotation func rotate_y()".
      * Chunk C: context_prefix=None, text="audio bus volume routing"
        → filler so query-keywords are not in every doc.

    Query: "CharacterBody3D rotation" → tokens ["character", "body", "3",
    "d", "rotation"].

    Without contextual BM25, Chunk A's corpus has only ["func", "rotate",
    "y"] — none overlap with the query. With contextual BM25, Chunk A's
    corpus gains ["character", "body", "3", "d", "rotation"] from the
    context_prefix → these query tokens are now present (TF > 0).

    We verify via ``doc_freqs`` (token presence) instead of BM25 scores
    because rank-bm25 yields negative IDF for tokens in 2/3 documents
    (``log((3-2+0.5)/(2+0.5)) < 0``), which makes raw score comparisons
    unreliable on small corpora. Token-presence is the stable signal.
    """
    from bm25_search import build_bm25_index, _load_index

    chunk_a = _make_chunk(
        "ctx_test::a",
        text="func rotate_y()",
        context_prefix="CharacterBody3D rotation",
    )
    chunk_b = _make_chunk(
        "ctx_test::b",
        text="CharacterBody3D rotation func rotate_y()",
        context_prefix=None,
    )
    chunk_c = _make_chunk(
        "ctx_test::c",
        text="audio bus volume routing",
        context_prefix=None,
    )
    query_tokens = {"character", "body", "3", "d", "rotation"}

    # Baseline build (D1: clean text).
    build_bm25_index("ctx_test", [chunk_a, chunk_b, chunk_c],
                     use_context_prefix=False)
    tokens_a_clean = _doc_tokens(_load_index("ctx_test"), "ctx_test::a")
    overlap_clean = query_tokens & tokens_a_clean

    # Contextual build (context_prefix prepended for chunk A).
    build_bm25_index("ctx_test", [chunk_a, chunk_b, chunk_c],
                     use_context_prefix=True)
    tokens_a_ctx = _doc_tokens(_load_index("ctx_test"), "ctx_test::a")
    overlap_ctx = query_tokens & tokens_a_ctx

    assert overlap_ctx > overlap_clean, (
        f"Contextual BM25 should add query-keyword tokens from "
        f"context_prefix to chunk A's corpus: "
        f"clean overlap={overlap_clean}, contextual overlap={overlap_ctx}"
    )
    # "character" only in context_prefix, not in text → must appear with ctx.
    assert "character" in overlap_ctx and "character" not in overlap_clean