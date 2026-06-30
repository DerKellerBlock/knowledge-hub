"""Unit tests for bm25_search.tokenize (pure function, no DB needed)."""

from bm25_search import tokenize


# ── Bestehende Tests (an neue CamelCase-/Unicode-Tokenizer-Logik angepasst) ──


def test_tokenize_simple_two_words():
    # "Node3D" → "Node" + "3" + "D" nach CamelCase-Split (Boundary zwischen
    # "Node" und "3D" wird nicht eingefügt, aber "3D" wird durch den
    # digit-or-word-Run in "3" und "d" aufgetrennt).
    assert tokenize("Node3D rotate") == ["node", "3", "d", "rotate"]


def test_tokenize_preserves_underscores():
    # Underscore ist im Unicode-Word-Run non-word → split zwischen Wörtern.
    assert tokenize("rotate_y") == ["rotate", "y"]


def test_tokenize_multiple_spaces():
    assert tokenize("  multiple   spaces  ") == ["multiple", "spaces"]


def test_tokenize_empty_string():
    assert tokenize("") == []


def test_tokenize_only_punctuation():
    assert tokenize("!@#$%^&*()") == []


def test_tokenize_camelcase_lowercased():
    # CamelCase wird an lowercase→UPPER-Boundaries gesplittet.
    assert tokenize("CamelCaseString") == ["camel", "case", "string"]


def test_tokenize_mixed_alphanumeric():
    # "Vector3" → ["vector", "3"], "1.5" → ["1", "5"], "2.0" → ["2", "0"].
    assert tokenize("Vector3 1.5 2.0") == ["vector", "3", "1", "5", "2", "0"]


def test_tokenize_newlines_and_tabs():
    # "line1" → ["line", "1"] (digit-run am Ende wird extrahiert).
    assert tokenize("line1\nline2\ttab") == ["line", "1", "line", "2", "tab"]


def test_tokenize_german_umlaute():
    # \W matcht keine Unicode-Buchstaben → Umlaute bleiben im selben Token.
    assert tokenize("übermäßige Größe") == ["übermäßige", "größe"]


def test_tokenize_hyphen_separated():
    # "v2" → ["v", "2"]: Hyphen trennt, digit-run extrahiert.
    assert tokenize("all-mpnet-base-v2") == ["all", "mpnet", "base", "v", "2"]


def test_tokenize_numbers_only():
    assert tokenize("123 456") == ["123", "456"]


# ── Neue Tests für CamelCase-, Unicode- und API-Method-Tokenization ──


def test_tokenize_allcaps_acronym():
    # Acronym "GPU" bleibt intakt (keine Boundary bei AA→AA), und das
    # Leerzeichen trennt es von "shader".
    assert tokenize("GPU shader") == ["gpu", "shader"]


def test_tokenize_camelcase_with_numbers():
    # "CharacterBody3D" splittet an "rB" und "y3", "3D" wird zu ["3", "d"].
    assert tokenize("CharacterBody3D") == ["character", "body", "3", "d"]


def test_tokenize_snake_case():
    # Underscore ist non-word → snake_case wird aufgetrennt.
    assert tokenize("move_and_slide") == ["move", "and", "slide"]


def test_tokenize_mixed_camel_snake():
    # Underscore trennt, CamelCase-Boundary splittet "N" → "n" bei get_node|Name.
    assert tokenize("get_node_Name") == ["get", "node", "name"]


def test_tokenize_german_umlaut_word():
    assert tokenize("Größe") == ["größe"]


def test_tokenize_german_prose():
    # Mehrere deutsche Wörter mit Umlauten bleiben erhalten.
    assert tokenize("übermäßige Größe") == ["übermäßige", "größe"]


def test_tokenize_godot_api_method():
    # snake_case-Methode aus der Godot-4-API.
    assert tokenize("set_process_mode") == ["set", "process", "mode"]


def test_tokenize_html_acronym():
    # Acronym gefolgt von CamelCase: AAa-Pattern fügt Boundary ein.
    assert tokenize("HTMLRenderer") == ["html", "renderer"]
