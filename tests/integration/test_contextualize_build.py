"""Integration tests for the ``--contextualize`` flag in ``embed_index.build_index``.

Phase 3.1b, Task 10 (Phase E). Verifies the build_index code path that
prepends an LLM-generated ``context_prefix`` to the embedding input
(``context_prefix + "\\n" + text``), while keeping ChromaDB documents
and BM25 on clean ``text`` (D1).

No real Ollama / LLM is started — ``contextualize_chunks`` is monkey-
patched to set deterministic fake ``context_prefix`` values. No real
embedding model is loaded — ``get_embedder`` is monkey-patched with a
``RecordingEmbedder`` that captures the exact texts passed to
``encode()`` so the test can assert the prepend behaviour.
"""

from __future__ import annotations

import numpy as np
import pytest

pytestmark = pytest.mark.integration

pytest.importorskip("chromadb")


# ── Test doubles ───────────────────────────────────────────────────────────


class RecordingEmbedder:
    """Fake embedder that records every text passed to ``encode()``.

    Returns a deterministic float32 vector per text so ChromaDB accepts
    the add(). The recorded ``encoded_texts`` list lets tests assert
    whether ``context_prefix`` was prepended (D1 verification).
    """

    def __init__(self, dim: int = 8):
        self.dim = dim
        self.encoded_texts: list[str] = []

    def encode(self, texts, batch_size=32, show_progress_bar=False,
               convert_to_numpy=True):
        # ``texts`` may be a list or a single str; normalise to list.
        if isinstance(texts, str):
            texts = [texts]
            single = True
        else:
            single = False
        self.encoded_texts.extend(texts)
        # Deterministic vector from text hash → stable across runs.
        vecs = np.zeros((len(texts), self.dim), dtype=np.float32)
        for i, t in enumerate(texts):
            h = abs(hash(t)) % (10 ** 9)
            for d in range(self.dim):
                vecs[i, d] = ((h >> (d % 31)) & 0xFF) / 255.0
        return vecs[0] if single else vecs

    @property
    def class_name(self) -> str:
        return "RecordingEmbedder"


def _patched_contextualize(domain, chunks, llm_entry, conn, model_name,
                           batch_size=50, dry_run=False):
    """Fake contextualize_chunks: set a deterministic context_prefix on
    every chunk (no LLM call)."""
    for c in chunks:
        c.context_prefix = f"CTX[{domain}:{c.source_file}]"
    return chunks


def _patched_check_ollama_available(llm_entry):
    """No-op stand-in for check_ollama_available."""
    return None


def _patched_get_llm():
    return {"client": None, "model": "fake", "backend": "ollama"}


def _patched_open_cache(domain):
    """Return a throwaway object — the fake contextualize never reads it."""
    class _NullConn:
        def close(self):
            pass
    return _NullConn()


# ── Tests ──────────────────────────────────────────────────────────────────


def test_contextualize_flag_prepend_context(dummy_domain, monkeypatch):
    """``build_index(domain, contextualize=True)`` prepends
    ``context_prefix + "\\n" + text`` to the embedding input and stores
    ``context_prefix`` in ChromaDB metadata (M3)."""
    import embed_index
    import model_manager as mm
    from model_manager import get_chroma_client

    embedder = RecordingEmbedder()
    monkeypatch.setattr(mm, "get_embedder", lambda domain: embedder)
    monkeypatch.setattr(embed_index, "get_embedder", lambda domain: embedder)
    # Stub the contextualize pipeline so no real Ollama is contacted.
    import contextualize_chunks as ctx_mod
    monkeypatch.setattr(ctx_mod, "contextualize_chunks", _patched_contextualize)
    monkeypatch.setattr(
        ctx_mod, "check_ollama_available", _patched_check_ollama_available,
    )
    import context_cache as cc_mod
    monkeypatch.setattr(cc_mod, "open_cache", _patched_open_cache)
    import model_manager as mm2
    monkeypatch.setattr(mm2, "get_llm", _patched_get_llm)

    embed_index.build_index(dummy_domain, contextualize=True)

    # 1. Embedding input was context_prefix + "\n" + text for every chunk
    #    that got a context_prefix (the fake contextualize sets one on all
    #    Path-A chunks, i.e. every chunk in this repo-only dummy domain).
    assert len(embedder.encoded_texts) > 0
    for encoded in embedder.encoded_texts:
        assert encoded.startswith("CTX[dummy:"), (
            f"Embedding input was not contextualized: {encoded[:60]!r}"
        )
        assert "\n" in encoded, (
            "Embedding input must contain the prefix/text separator '\\n'"
        )

    # 2. ChromaDB metadata carries context_prefix.
    client = get_chroma_client(dummy_domain)
    collection = client.get_collection(f"{dummy_domain}_knowledge")
    result = collection.get(include=["metadatas"])
    prefixes = [m.get("context_prefix") for m in result["metadatas"]]
    assert any(p for p in prefixes), (
        "No context_prefix in ChromaDB metadata after --contextualize build"
    )
    for p in prefixes:
        if p is not None:
            assert p.startswith("CTX[dummy:")

    # 3. ChromaDB documents stay clean (D1): no prefix in the stored text.
    docs_result = collection.get(include=["documents"])
    for doc in docs_result["documents"]:
        assert not doc.startswith("CTX[dummy:"), (
            f"ChromaDB document leaked context_prefix (D1 violation): "
            f"{doc[:60]!r}"
        )


def test_no_contextualize_default_unchanged(dummy_domain, monkeypatch):
    """``build_index(domain)`` without contextualize → embedding input is
    plain ``c.text`` and metadata has no ``context_prefix``."""
    import embed_index
    import model_manager as mm
    from model_manager import get_chroma_client

    embedder = RecordingEmbedder()
    monkeypatch.setattr(mm, "get_embedder", lambda domain: embedder)
    monkeypatch.setattr(embed_index, "get_embedder", lambda domain: embedder)

    embed_index.build_index(dummy_domain)

    # Embedding input is exactly the chunk text — no "CTX[" prefix.
    assert len(embedder.encoded_texts) > 0
    for encoded in embedder.encoded_texts:
        assert not encoded.startswith("CTX["), (
            f"Default build contextualized unexpectedly: {encoded[:60]!r}"
        )

    client = get_chroma_client(dummy_domain)
    collection = client.get_collection(f"{dummy_domain}_knowledge")
    result = collection.get(include=["metadatas"])
    prefixes = [m.get("context_prefix") for m in result["metadatas"]]
    assert all(p is None for p in prefixes), (
        f"Default build wrote context_prefix metadata: {prefixes}"
    )


def test_contextualize_skips_late_chunk(tmp_hub, monkeypatch):
    """H3 / Spec N1: late_chunk chunks are NOT contextualized.

    Builds a tiny PDF domain with one late_chunk source (which produces
    precomputed embeddings and is skipped by the Path-A filter) plus a
    fallback chunk path, then verifies:

    * late_chunk chunks keep ``context_prefix = None`` in metadata,
    * non-late chunks (fallback) get a context_prefix.

    Because real late chunking requires BGE-M3, we stub
    ``load_domain_sources`` to return a mixed chunk list with a fake
    ``precomputed_embeddings`` dict — this exercises the precomputed
    branch of build_index (the H3 fallback-text prepend path) without
    loading any model.
    """
    import embed_index
    import model_manager as mm
    import parser_base
    from model_manager import get_chroma_client

    # Minimal PDF-domain directory (only domain.md is read by
    # get_domain_config; sources are stubbed via load_domain_sources).
    domain = "pdfmix"
    domain_dir = tmp_hub / "domains" / domain
    domain_dir.mkdir(parents=True)
    (domain_dir / "domain.md").write_text(
        f"# Domain: {domain}\n\n## Metadaten\n"
        "- Embedding-Model: BAAI/bge-m3 (1024 dims)\n"
        f"- Collection: {domain}_knowledge\n"
        "- Source-Types: pdf\n"
        "- Letztes Update: 2026-07-02\n",
        encoding="utf-8",
    )

    # Build a mixed chunk list: one late_chunk (with precomputed emb) +
    # one fallback chunk (chunk_type=None, to be embedded via
    # _encode_robust).
    late = parser_base.Chunk(
        chunk_id=f"{domain}::late::0",
        domain=domain,
        text="Late chunk body about Fusion compositing.",
        source_type="repo",
        chunk_type="late_chunk",
        source_file="manual.md",
        page_start=1, page_end=2,
    )
    fb = parser_base.Chunk(
        chunk_id=f"{domain}::fallback::0",
        domain=domain,
        text="Fallback chunk body about Color page basics.",
        source_type="repo",
        chunk_type=None,
        source_file="manual.md",
    )
    chunks = [late, fb]

    fake_precomputed = {
        late.chunk_id: np.zeros(8, dtype=np.float32),
    }

    def fake_load_domain_sources(d):
        return chunks, fake_precomputed

    monkeypatch.setattr(embed_index, "load_domain_sources", fake_load_domain_sources)

    embedder = RecordingEmbedder(dim=8)
    monkeypatch.setattr(mm, "get_embedder", lambda domain: embedder)
    monkeypatch.setattr(embed_index, "get_embedder", lambda domain: embedder)

    # Stub the contextualize pipeline.
    import contextualize_chunks as ctx_mod
    monkeypatch.setattr(ctx_mod, "contextualize_chunks", _patched_contextualize)
    monkeypatch.setattr(
        ctx_mod, "check_ollama_available", _patched_check_ollama_available,
    )
    import context_cache as cc_mod
    monkeypatch.setattr(cc_mod, "open_cache", _patched_open_cache)
    monkeypatch.setattr(mm, "get_llm", _patched_get_llm)

    embed_index.build_index(domain, contextualize=True)

    # The fake contextualize was called only on the Path-A subset
    # (fallback chunk). late_chunk must keep context_prefix=None.
    assert late.context_prefix is None, (
        "late_chunk was contextualized — Path-A filter broken"
    )
    assert fb.context_prefix is not None, (
        "fallback chunk was not contextualized"
    )

    # Embedding input: only the fallback chunk was embedded (late_chunk
    # used precomputed). Its input must be prefix + "\n" + text.
    assert len(embedder.encoded_texts) == 1, (
        f"Expected exactly 1 encoded text (fallback only), "
        f"got {len(embedder.encoded_texts)}"
    )
    assert embedder.encoded_texts[0].startswith("CTX[pdfmix:"), (
        f"Fallback embedding input not contextualized: "
        f"{embedder.encoded_texts[0][:60]!r}"
    )

    # ChromaDB metadata: late_chunk has no context_prefix, fallback has.
    client = get_chroma_client(domain)
    collection = client.get_collection(f"{domain}_knowledge")
    result = collection.get(include=["metadatas"])
    by_id = dict(zip(result["ids"], result["metadatas"]))
    assert by_id[late.chunk_id].get("context_prefix") is None, (
        f"late_chunk context_prefix leaked into ChromaDB: "
        f"{by_id[late.chunk_id]}"
    )
    assert by_id[fb.chunk_id].get("context_prefix") is not None, (
        f"fallback context_prefix missing in ChromaDB: {by_id[fb.chunk_id]}"
    )


def test_contextualize_bm25_flag_enables_contextual_bm25(dummy_domain, monkeypatch):
    """``--contextualize-bm25`` (Phase 3.2) now enables Contextual BM25:
    the BM25 pickle corpus includes ``context_prefix`` tokens (D1 no
    longer applies when the flag is set).

    Replaces the former ``test_contextualize_bm25_flag_accepted_but_unused``
    stub from Phase 3.1b (deferred). The fake contextualize sets a
    deterministic ``CTX[domain:source]`` prefix on every Path-A chunk;
    the BM25 corpus must now contain the ``CTX`` token.
    """
    import embed_index
    import model_manager as mm
    from bm25_search import _load_index
    from mcp_servers.knowledge_hub.config import domain_bm25_path

    embedder = RecordingEmbedder()
    monkeypatch.setattr(mm, "get_embedder", lambda domain: embedder)
    monkeypatch.setattr(embed_index, "get_embedder", lambda domain: embedder)
    import contextualize_chunks as ctx_mod
    monkeypatch.setattr(ctx_mod, "contextualize_chunks", _patched_contextualize)
    monkeypatch.setattr(
        ctx_mod, "check_ollama_available", _patched_check_ollama_available,
    )
    import context_cache as cc_mod
    monkeypatch.setattr(cc_mod, "open_cache", _patched_open_cache)
    monkeypatch.setattr(mm, "get_llm", _patched_get_llm)

    embed_index.build_index(
        dummy_domain, contextualize=True, contextualize_bm25=True,
    )

    # BM25 pickle exists and the corpus now CONTAINS the context_prefix
    # tokens (CTX) — Phase 3.2 Contextual BM25 is active. Verified via
    # scores: the "ctx" token (only present in the fake context_prefix)
    # must score > 0 on at least one chunk. (BM25Okapi does not expose
    # ``corpus`` directly, so score inspection is the canonical check.)
    assert domain_bm25_path(dummy_domain).exists()
    data = _load_index(dummy_domain)
    bm25 = data["index"]
    chunk_ids = data["chunk_ids"]
    from bm25_search import tokenize
    scores = bm25.get_scores(tokenize("ctx"))
    has_prefix_score = any(float(s) > 0 for s in scores)
    assert has_prefix_score, (
        "BM25 corpus does not contain context_prefix tokens — "
        "Contextual BM25 (Phase 3.2) is not active although "
        "contextualize_bm25=True"
    )


def test_contextualize_bm25_false_keeps_clean_bm25(dummy_domain, monkeypatch):
    """BS-7 Backward-Compat: ``contextualize=True`` with
    ``contextualize_bm25=False`` keeps the BM25 corpus on clean ``text``
    (D1 default). The embedding is still contextualized (prefix prepended
    for the embedder), but BM25 stays on plain text — this is the
    Phase 3.1 default and must not regress in Phase 3.2.
    """
    import embed_index
    import model_manager as mm
    from bm25_search import _load_index
    from mcp_servers.knowledge_hub.config import domain_bm25_path

    embedder = RecordingEmbedder()
    monkeypatch.setattr(mm, "get_embedder", lambda domain: embedder)
    monkeypatch.setattr(embed_index, "get_embedder", lambda domain: embedder)
    import contextualize_chunks as ctx_mod
    monkeypatch.setattr(ctx_mod, "contextualize_chunks", _patched_contextualize)
    monkeypatch.setattr(
        ctx_mod, "check_ollama_available", _patched_check_ollama_available,
    )
    import context_cache as cc_mod
    monkeypatch.setattr(cc_mod, "open_cache", _patched_open_cache)
    monkeypatch.setattr(mm, "get_llm", _patched_get_llm)

    # contextualize=True but contextualize_bm25=False (D1 default).
    embed_index.build_index(
        dummy_domain, contextualize=True, contextualize_bm25=False,
    )

    # Embedding was contextualized (sanity check).
    assert embedder.encoded_texts, "no texts were encoded"
    assert any(t.startswith("CTX[dummy:") for t in embedder.encoded_texts), (
        "contextualize=True did not prepend context_prefix to embeddings"
    )

    # BM25 corpus stays clean (no CTX tokens) — D1 preserved.
    assert domain_bm25_path(dummy_domain).exists()
    data = _load_index(dummy_domain)
    bm25 = data["index"]
    from bm25_search import tokenize
    scores = bm25.get_scores(tokenize("ctx"))
    has_prefix_score = any(float(s) > 0 for s in scores)
    assert not has_prefix_score, (
        "contextualize_bm25=False leaked context_prefix into BM25 corpus "
        "— D1 backward-compat broken"
    )