"""Unit tests for hybrid_search.rrf_fusion — pure function, no models needed."""

from hybrid_search import rrf_fusion


def test_empty_inputs_returns_empty():
    assert rrf_fusion([], []) == []


def test_only_sparse_results():
    sparse = [{"chunk_id": "A", "score": 5.0}]
    results = rrf_fusion(sparse, [])
    assert len(results) == 1
    assert results[0]["chunk_id"] == "A"
    assert results[0]["score"] > 0
    assert "bm25" in results[0]["stage1_sources"]


def test_only_dense_results():
    dense = [{"chunk_id": "B", "score": 0.9, "text": "hello"}]
    results = rrf_fusion([], dense)
    assert len(results) == 1
    assert results[0]["chunk_id"] == "B"
    assert "semantic" in results[0]["stage1_sources"]
    assert results[0]["text"] == "hello"


def test_same_chunk_in_both_sources():
    sparse = [{"chunk_id": "A", "score": 5.0}]
    dense = [{"chunk_id": "A", "score": 0.9, "text": "hello"}]
    results = rrf_fusion(sparse, dense)
    assert len(results) == 1
    assert results[0]["chunk_id"] == "A"
    assert "bm25" in results[0]["stage1_sources"]
    assert "semantic" in results[0]["stage1_sources"]


def test_different_chunks_in_sources():
    sparse = [{"chunk_id": "A", "score": 5.0}]
    dense = [{"chunk_id": "B", "score": 0.9, "text": "hello"}]
    results = rrf_fusion(sparse, dense)
    assert len(results) == 2
    # Both should have positive scores
    assert results[0]["score"] > 0
    assert results[1]["score"] > 0
    # Ranks assigned
    assert results[0]["rank"] == 1
    assert results[1]["rank"] == 2


def test_top_n_limits_results():
    sparse = [{"chunk_id": f"s{i}", "score": 10.0 - i} for i in range(10)]
    dense = [{"chunk_id": f"d{i}", "score": 0.9 - i * 0.05} for i in range(10)]
    results = rrf_fusion(sparse, dense, top_n=5)
    assert len(results) == 5


def test_score_is_rounded():
    sparse = [{"chunk_id": "A", "score": 5.0}]
    results = rrf_fusion(sparse, [])
    # score is rounded to 4 decimal places
    assert results[0]["score"] == round(results[0]["score"], 4)


def test_match_type_is_hybrid():
    sparse = [{"chunk_id": "A", "score": 5.0}]
    dense = [{"chunk_id": "A", "score": 0.9, "text": "hello"}]
    results = rrf_fusion(sparse, dense)
    assert results[0]["match_type"] == "hybrid"


def test_dense_metadata_propagated():
    dense = [{
        "chunk_id": "B", "score": 0.9, "text": "hello",
        "source_type": "repo", "domain": "test",
        "source_file": "file.md", "line_start": 1, "line_end": 5,
        "chunk_type": "method", "class_name": "Node3D",
        "name": "rotate", "signature": "void rotate()",
        "page_start": 42, "page_end": 43,
        "section_path": "Chapter 1 > Section 2",
    }]
    results = rrf_fusion([], dense)
    r = results[0]
    assert r["source_type"] == "repo"
    assert r["domain"] == "test"
    assert r["source_file"] == "file.md"
    assert r["page_start"] == 42
    assert r["section_path"] == "Chapter 1 > Section 2"