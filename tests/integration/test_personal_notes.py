"""Integration tests for tools.py personal note functions."""

import pytest

pytestmark = pytest.mark.integration


def test_add_personal_note_success(dummy_domain):
    """add_personal_note should append to the category file."""
    from mcp_servers.knowledge_hub.tools import add_personal_note

    result = add_personal_note(
        domain=dummy_domain,
        topic="Test Topic",
        content="This is a test note.",
        category="gotchas",
    )
    assert result["status"] == "added"
    assert result["domain"] == dummy_domain
    assert "gotchas" in result["file"]


def test_list_personal_notes_returns_entries(dummy_domain):
    """list_personal_notes should parse the notes file."""
    from mcp_servers.knowledge_hub.tools import add_personal_note, list_personal_notes

    add_personal_note(dummy_domain, "Topic A", "Content A", "gotchas")
    add_personal_note(dummy_domain, "Topic B", "Content B", "tips")

    result = list_personal_notes(dummy_domain)
    assert result["domain"] == dummy_domain
    assert "gotchas" in result["notes"]
    assert "tips" in result["notes"]
    assert len(result["notes"]["gotchas"]) >= 1
    assert len(result["notes"]["tips"]) >= 1


def test_add_personal_note_invalid_category(dummy_domain):
    """Invalid category name should return an error dict."""
    from mcp_servers.knowledge_hub.tools import add_personal_note

    result = add_personal_note(dummy_domain, "T", "C", "bad/cat")
    assert "error" in result


def test_add_personal_note_uppercase_category_rejected(dummy_domain):
    """Uppercase category should be rejected by the regex."""
    from mcp_servers.knowledge_hub.tools import add_personal_note

    result = add_personal_note(dummy_domain, "T", "C", "UPPERCASE")
    assert "error" in result


def test_list_personal_notes_category_filter(dummy_domain):
    """list_personal_notes with category filter should return only that category."""
    from mcp_servers.knowledge_hub.tools import add_personal_note, list_personal_notes

    add_personal_note(dummy_domain, "Topic A", "Content A", "gotchas")
    add_personal_note(dummy_domain, "Topic B", "Content B", "tips")

    result = list_personal_notes(dummy_domain, category="gotchas")
    assert "gotchas" in result["notes"]
    assert "tips" not in result["notes"]


def test_list_personal_notes_nonexistent_domain():
    """list_personal_notes on a nonexistent domain should return error."""
    from mcp_servers.knowledge_hub.tools import list_personal_notes

    result = list_personal_notes("totally_nonexistent_domain_xyz")
    assert "error" in result