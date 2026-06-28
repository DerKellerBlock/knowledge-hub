"""Unit tests for bm25_search.tokenize (pure function, no DB needed)."""

from bm25_search import tokenize


def test_tokenize_simple_two_words():
    assert tokenize("Node3D rotate") == ["node3d", "rotate"]


def test_tokenize_preserves_underscores():
    assert tokenize("rotate_y") == ["rotate_y"]


def test_tokenize_multiple_spaces():
    assert tokenize("  multiple   spaces  ") == ["multiple", "spaces"]


def test_tokenize_empty_string():
    assert tokenize("") == []


def test_tokenize_only_punctuation():
    assert tokenize("!@#$%^&*()") == []


def test_tokenize_camelcase_lowercased():
    # tokenizer lowercases everything; CamelCase is not split
    assert tokenize("CamelCaseString") == ["camelcasestring"]


def test_tokenize_mixed_alphanumeric():
    assert tokenize("Vector3 1.5 2.0") == ["vector3", "1", "5", "2", "0"]


def test_tokenize_newlines_and_tabs():
    assert tokenize("line1\nline2\ttab") == ["line1", "line2", "tab"]


def test_tokenize_german_umlaute():
    # \w in Python regex includes unicode word chars by default
    tokens = tokenize("übermäßige Größe")
    assert "übermäßige" in tokens
    assert "größe" in tokens


def test_tokenize_hyphen_separated():
    assert tokenize("all-mpnet-base-v2") == ["all", "mpnet", "base", "v2"]


def test_tokenize_numbers_only():
    assert tokenize("123 456") == ["123", "456"]