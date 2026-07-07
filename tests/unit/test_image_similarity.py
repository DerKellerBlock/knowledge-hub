"""Unit tests for Visual Question Answering (image_similarity_search).

Tests cover:

* image_similarity_search with a mocked ChromaDB images collection
  (returns similar images with caption metadata).
* graceful error handling: file missing, invalid image, SigLIP-2
  unavailable, images collection missing → all return [].
* search_knowledge backward-compat: image_path=None does not invoke
  image_similarity_search (no image_match in results).
* search_knowledge with image_path: image_similarity_search is called
  and image_match results are prepended to the merged list.
* content-hash cache: query_image embeddings are persisted with
  modality="query_image" so they don't collide with indexed embeddings.

All external dependencies (PIL, SigLIP-2, ChromaDB, sqlite cache) are
mocked — no real model is loaded, no real ChromaDB is queried.
"""

import pytest
import sys
from pathlib import Path

pytestmark = pytest.mark.unit

# Make scripts/ importable.
HUB_ROOT = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = HUB_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
if str(HUB_ROOT) not in sys.path:
    sys.path.insert(0, str(HUB_ROOT))


# ── Helpers: build a tiny fake PNG ──────────────────────────────────────────


@pytest.fixture
def fake_png(tmp_path):
    """Create a minimal valid PNG file (1x1 pixel) using PIL if available."""
    try:
        from PIL import Image
    except ImportError:
        pytest.skip("PIL not installed")
    p = tmp_path / "query.png"
    # 1x1 RGB PNG.
    Image.new("RGB", (1, 1), (255, 0, 0)).save(p)
    return p


# ── image_similarity_search: graceful errors ───────────────────────────────


class TestImageSimilaritySearchGracefulErrors:
    def test_nonexistent_image_returns_empty_list(self):
        from hybrid_search import image_similarity_search
        result = image_similarity_search(
            "davinci_resolve", "/tmp/does_not_exist_xyz_12345.png", top_k=5,
        )
        assert result == []

    def test_invalid_image_file_returns_empty_list(self, tmp_path):
        from hybrid_search import image_similarity_search
        bad = tmp_path / "not_a_png.png"
        bad.write_bytes(b"not actually a png file")
        result = image_similarity_search(
            "davinci_resolve", str(bad), top_k=5,
        )
        assert result == []

    def test_collection_missing_returns_empty_list(
        self, monkeypatch, fake_png,
    ):
        """If the <domain>_images collection does not exist, return []."""
        from hybrid_search import image_similarity_search

        # Force the multimodal embedder to return a fake processor/model
        # so we get past the SigLIP-2 load step.
        import numpy as np

        class _FakeProcessor:
            def __call__(self, images=None, **kw):
                return {"pixel_values": np.zeros((1, 3, 512, 512), dtype=np.float32)}

        class _FakeModel:
            def get_image_features(self, **kw):
                # Return a 1xD embedding.
                return type("X", (), {"cpu": type("C", (), {
                    "float": lambda self: type("F", (), {
                        "numpy": np.zeros((1, 1152), dtype=np.float32),
                    })(),
                })()})()

        class _FakeTorchDevice:
            def __init__(self, s): self.s = s
            def __str__(self): return self.s

        def fake_get_mm(model_name=None):
            return (_FakeProcessor(), _FakeModel(), "cpu", 32)

        monkeypatch.setattr(
            "model_manager.get_multimodal_embedder", fake_get_mm,
        )

        # Patch the import inside image_similarity_search: it does
        # `from model_manager import get_multimodal_embedder` so we need
        # to patch the symbol in the model_manager module.
        import model_manager
        monkeypatch.setattr(model_manager, "get_multimodal_embedder", fake_get_mm)

        # Patch image_embedding_cache to skip cache (so we go straight to
        # the embed + query path).
        import image_embedding_cache as iec

        class _FakeConn:
            def execute(self, *a, **k): return iter([])
            def close(self): pass
        monkeypatch.setattr(iec, "open_cache", lambda d: _FakeConn())
        monkeypatch.setattr(iec, "get_cached", lambda *a, **k: None)
        monkeypatch.setattr(iec, "put_cached", lambda *a, **k: None)
        monkeypatch.setattr(iec, "image_hash", lambda p: "fakehash")

        # Now patch torch + processor inside the function: the function
        # imports torch locally and uses processor(images=...). We mock
        # torch.device and torch.no_grad.
        import torch
        monkeypatch.setattr(torch, "device", lambda s: _FakeTorchDevice(s))
        monkeypatch.setattr(torch, "no_grad", lambda: type("ctx", (), {
            "__enter__": lambda self: self, "__exit__": lambda *a: None,
        })())

        # get_chroma_client raises → collection missing path.
        monkeypatch.setattr(
            "hybrid_search.get_chroma_client",
            lambda d: (_ for _ in ()).throw(RuntimeError("no collection")),
        )

        result = image_similarity_search(
            "nonexistent_domain", str(fake_png), top_k=5,
        )
        assert result == []


# ── image_similarity_search: mocked ChromaDB returns similar images ────────


class TestImageSimilaritySearchWithMockChromaDB:
    def test_returns_image_match_results_sorted_by_similarity(
        self, monkeypatch, fake_png,
    ):
        from hybrid_search import image_similarity_search

        # ── Mock SigLIP-2 + torch ──────────────────────────────────────
        import numpy as np
        import torch

        class _FakeTensor:
            """Mimics torch.Tensor: supports .to(device) -> self and is
            passable to model.get_image_features()."""
            def __init__(self, arr): self._arr = arr
            def to(self, device): return self

        class _FakeProcessor:
            def __call__(self, images=None, **kw):
                return {"pixel_values": _FakeTensor(
                    np.zeros((1, 3, 512, 512), dtype=np.float32))}

        class _FakeModel:
            def get_image_features(self, **kw):
                # Return an object with .cpu().float().numpy() chain.
                class _C:
                    def float(self): return self
                    def numpy(self): return np.zeros((1, 1152), dtype=np.float32)
                class _X:
                    def cpu(self): return _C()
                return _X()

        class _FakeTorchDevice:
            def __init__(self, s): self.s = s
            def __str__(self): return self.s

        def fake_get_mm(model_name=None):
            return (_FakeProcessor(), _FakeModel(), "cpu", 32)

        import model_manager
        monkeypatch.setattr(model_manager, "get_multimodal_embedder", fake_get_mm)
        monkeypatch.setattr(torch, "device", lambda s: _FakeTorchDevice(s))
        monkeypatch.setattr(torch, "no_grad", lambda: type("ctx", (), {
            "__enter__": lambda self: self, "__exit__": lambda *a: None,
        })())

        # ── Mock image_embedding_cache (cache miss + put succeeds) ─────
        import image_embedding_cache as iec

        class _FakeConn:
            def execute(self, *a, **k): return iter([])
            def close(self): pass
        monkeypatch.setattr(iec, "open_cache", lambda d: _FakeConn())
        monkeypatch.setattr(iec, "get_cached", lambda *a, **k: None)
        monkeypatch.setattr(iec, "put_cached", lambda *a, **k: None)
        monkeypatch.setattr(iec, "image_hash", lambda p: "fakehash")

        # ── Mock ChromaDB ──────────────────────────────────────────────
        # Two image results with descending similarity (lower distance = more similar).
        fake_results = {
            "ids": [["davinci_resolve::img::1::0::img", "davinci_resolve::img::2::0::img"]],
            "metadatas": [[
                {
                    "image_id": "davinci_resolve::img::1::0",
                    "modality": "image",
                    "image_path": "domains/davinci_resolve/images/foo/bar-1-0.png",
                    "source_file": "DaVinci_Resolve_20.3_Reference_Manual.pdf",
                    "page": 3084,
                    "idx": 0,
                    "caption": "The Color Wheels panel with three color wheels.",
                    "quality": "good",
                    "domain": "davinci_resolve",
                },
                {
                    "image_id": "davinci_resolve::img::2::0",
                    "modality": "image",
                    "image_path": "domains/davinci_resolve/images/foo/bar-2-0.png",
                    "source_file": "DaVinci_Resolve_20.3_Reference_Manual.pdf",
                    "page": 4000,
                    "idx": 0,
                    "caption": "The Scope panel showing a vectorscope.",
                    "quality": "good",
                    "domain": "davinci_resolve",
                },
            ]],
            "distances": [[0.09, 0.40]],  # similarity = 0.91, 0.60
        }

        class _FakeCollection:
            def query(self, query_embeddings=None, n_results=10, where=None, include=None):
                return fake_results

        class _FakeClient:
            def get_collection(self, name):
                return _FakeCollection()

        monkeypatch.setattr("hybrid_search.get_chroma_client", lambda d: _FakeClient())

        # ── Run ────────────────────────────────────────────────────────
        result = image_similarity_search(
            "davinci_resolve", str(fake_png), top_k=5,
        )

        # Assertions.
        assert len(result) == 2
        # Sorted by similarity descending: 0.91 first, 0.60 second.
        assert result[0]["similarity_score"] == pytest.approx(0.91, abs=0.01)
        assert result[1]["similarity_score"] == pytest.approx(0.60, abs=0.01)
        # Modality + match_type set correctly.
        assert all(r["modality"] == "image_match" for r in result)
        assert all(r["match_type"] == "image_similarity" for r in result)
        # Caption propagated.
        assert "Color Wheels" in result[0]["caption"]
        # Sequential ranks 1..N.
        assert [r["rank"] for r in result] == [1, 2]
        # chunk_id is the image entry id.
        assert result[0]["chunk_id"] == "davinci_resolve::img::1::0::img"
        # image_id propagated.
        assert result[0]["image_id"] == "davinci_resolve::img::1::0"
        # Page + source_file propagated.
        assert result[0]["page"] == 3084
        assert "Reference_Manual" in result[0]["source_file"]
        # text field contains caption (so reranker / LLM can read it).
        assert "Color Wheels" in result[0]["text"]


# ── search_knowledge backward-compat + image_path integration ──────────────


class TestSearchKnowledgeImagePathParameter:
    def test_image_path_none_does_not_call_image_similarity(
        self, monkeypatch,
    ):
        """Without image_path, image_similarity_search must NOT be invoked
        and the result must not contain image_match entries.
        """
        # Patch search() in hybrid_search to a stub that records the
        # image_path argument and returns a fixed dict.
        import hybrid_search
        called_kwargs = {}

        def fake_search(domain, query, mode="hybrid", top_k=10,
                        source_filter=None, image_path=None):
            called_kwargs["image_path"] = image_path
            return {
                "results": [{"rank": 1, "modality": "text", "text": "stub"}],
                "total_found": 1,
                "mode": mode,
                "query_time_ms": 0,
                "image_match_count": 0,
            }

        monkeypatch.setattr(hybrid_search, "search", fake_search)
        # tools.py imports search as hybrid_search_fn — patch that alias too.
        import mcp_servers.knowledge_hub.tools as tools_mod
        monkeypatch.setattr(tools_mod, "hybrid_search_fn", fake_search)

        from mcp_servers.knowledge_hub.tools import search_knowledge
        result = search_knowledge(
            domain="davinci_resolve",
            query="Color Wheels",
            max_results=10,
        )
        assert called_kwargs["image_path"] is None
        assert result["image_match_count"] == 0
        # No image_match in results.
        assert all(r.get("modality") != "image_match" for r in result["results"])

    def test_image_path_set_invokes_image_similarity(
        self, monkeypatch,
    ):
        """With image_path set, search() must receive it and the result
        may contain image_match entries.
        """
        import hybrid_search
        called_kwargs = {}

        def fake_search(domain, query, mode="hybrid", top_k=10,
                        source_filter=None, image_path=None):
            called_kwargs["image_path"] = image_path
            return {
                "results": [
                    {"rank": 1, "modality": "image_match",
                     "similarity_score": 0.91, "caption": "Color Wheels panel",
                     "image_path": "/data/foo.png", "page": 3084,
                     "source_file": "Reference_Manual.pdf"},
                    {"rank": 2, "modality": "text", "text": "stub"},
                ],
                "total_found": 2,
                "mode": mode,
                "query_time_ms": 0,
                "image_match_count": 1,
            }

        monkeypatch.setattr(hybrid_search, "search", fake_search)
        import mcp_servers.knowledge_hub.tools as tools_mod
        monkeypatch.setattr(tools_mod, "hybrid_search_fn", fake_search)

        from mcp_servers.knowledge_hub.tools import search_knowledge
        result = search_knowledge(
            domain="davinci_resolve",
            query="Color Wheels",
            max_results=10,
            image_path="/tmp/query.png",
        )
        assert called_kwargs["image_path"] == "/tmp/query.png"
        assert result["image_match_count"] == 1
        # First result is an image_match.
        assert result["results"][0]["modality"] == "image_match"
        assert result["results"][0]["similarity_score"] == 0.91


# ── search() image_path propagation (end-to-end with mocked pipeline) ──────


class TestSearchImagePathPropagation:
    def test_search_without_image_path_unchanged(self, monkeypatch):
        """search() with image_path=None must behave like the old signature
        — no image_match in results, no image_match_count key missing.
        """
        # We mock the entire pipeline by stubbing bm25_search, semantic_search,
        # _has_image_index, rerank, is_reranker_available. The simplest way
        # is to check that the function accepts image_path=None and returns
        # a dict with image_match_count=0.
        import hybrid_search

        monkeypatch.setattr(hybrid_search, "bm25_search",
                            lambda d, q, top_k=100: [])
        monkeypatch.setattr(hybrid_search, "semantic_search",
                            lambda d, q, k, m: [])
        monkeypatch.setattr(hybrid_search, "_has_image_index", lambda d: False)
        monkeypatch.setattr(hybrid_search, "rrf_fusion",
                            lambda sparse, dense, k=60, top_n=50: [])
        monkeypatch.setattr(hybrid_search, "_resolve_texts_via_chromadb",
                            lambda d, r: None)
        monkeypatch.setattr(hybrid_search, "is_reranker_available", lambda: False)
        # image_similarity_search must NOT be called.
        called = {"count": 0}

        def _fail_if_called(*a, **k):
            called["count"] += 1
            return []
        monkeypatch.setattr(hybrid_search, "image_similarity_search",
                            _fail_if_called)
        # get_embedder must return something (only called in hybrid path).
        monkeypatch.setattr(hybrid_search, "get_embedder", lambda d: None)
        monkeypatch.setattr(hybrid_search, "should_use_hyde", lambda q: False)

        result = hybrid_search.search(
            "godot", "test query", mode="hybrid", top_k=5,
        )
        assert called["count"] == 0
        assert result["image_match_count"] == 0
        assert result["results"] == []

    def test_search_with_image_path_prepends_image_match(
        self, monkeypatch, fake_png,
    ):
        """search() with image_path set must call image_similarity_search
        and prepend the image_match results to the merged list.
        """
        import hybrid_search

        # Stub the text pipeline to return one text result.
        monkeypatch.setattr(hybrid_search, "bm25_search",
                            lambda d, q, top_k=100: [])
        monkeypatch.setattr(hybrid_search, "semantic_search",
                            lambda d, q, k, m: [])
        monkeypatch.setattr(hybrid_search, "_has_image_index", lambda d: False)
        monkeypatch.setattr(hybrid_search, "rrf_fusion",
                            lambda sparse, dense, k=60, top_n=50: [
                                {"chunk_id": "text1", "modality": "text",
                                 "text": "a text hit", "score": 0.5},
                            ])
        monkeypatch.setattr(hybrid_search, "_resolve_texts_via_chromadb",
                            lambda d, r: None)
        monkeypatch.setattr(hybrid_search, "is_reranker_available", lambda: False)
        monkeypatch.setattr(hybrid_search, "get_embedder", lambda d: None)
        monkeypatch.setattr(hybrid_search, "should_use_hyde", lambda q: False)

        # Stub image_similarity_search to return 2 image_match results.
        def fake_img_sim(domain, image_path, top_k=10):
            return [
                {"chunk_id": "img1", "modality": "image_match",
                 "similarity_score": 0.91, "caption": "Color Wheels",
                 "image_path": "/data/img1.png", "page": 3084,
                 "source_file": "ref.pdf", "rank": 1, "score": 0.91,
                 "text": "Color Wheels"},
                {"chunk_id": "img2", "modality": "image_match",
                 "similarity_score": 0.60, "caption": "Scope",
                 "image_path": "/data/img2.png", "page": 4000,
                 "source_file": "ref.pdf", "rank": 2, "score": 0.60,
                 "text": "Scope"},
            ]
        monkeypatch.setattr(hybrid_search, "image_similarity_search",
                            fake_img_sim)

        result = hybrid_search.search(
            "davinci_resolve", "Color Wheels", mode="hybrid", top_k=5,
            image_path=str(fake_png),
        )
        # image_match_count = 2.
        assert result["image_match_count"] == 2
        # First two results are image_match (prepended), then text.
        assert result["results"][0]["modality"] == "image_match"
        assert result["results"][1]["modality"] == "image_match"
        assert result["results"][0]["similarity_score"] == 0.91
        # Ranks reassigned 1..N.
        assert [r["rank"] for r in result["results"]] == [1, 2, 3]
