"""Unit tests for tools.py — domain scoping and category validation.

Does NOT call search_knowledge (which requires a loaded index).
Tests only the pure-logic helpers: set_domain_scope, _check_domain_scope,
list_scoped_domains, and regex validation.
"""

import pytest

pytestmark = pytest.mark.unit

from mcp_servers.knowledge_hub import tools
from mcp_servers.knowledge_hub.tools import (
    set_domain_scope,
    _check_domain_scope,
    list_domains,
    list_scoped_domains,
    _CATEGORY_RE,
)


@pytest.fixture(autouse=True)
def reset_scope():
    """Reset domain scope before and after each test."""
    set_domain_scope(None)
    yield
    set_domain_scope(None)


class TestDomainScoping:
    def test_no_scope_all_visible(self):
        set_domain_scope(None)
        assert _check_domain_scope("godot") is None
        assert _check_domain_scope("davinci_resolve") is None
        assert _check_domain_scope("anything") is None

    def test_empty_list_all_visible(self):
        set_domain_scope([])
        assert _check_domain_scope("anything") is None

    def test_single_domain_scope(self):
        # Use a domain that actually exists for the scope to be accepted
        available = list_domains()
        if not available:
            pytest.skip("no domains available")
        target = available[0]
        set_domain_scope([target])
        assert _check_domain_scope(target) is None
        # Any other domain → error
        for other in available:
            if other != target:
                result = _check_domain_scope(other)
                assert result is not None
                assert "error" in result
                assert target in result["error"]

    def test_scope_with_nonexistent_domain_raises(self):
        with pytest.raises(ValueError, match="Domain\\(s\\) not found"):
            set_domain_scope(["totally_nonexistent_xyz"])

    def test_scope_restricts_list_scoped_domains(self):
        available = list_domains()
        if len(available) < 2:
            pytest.skip("need at least 2 domains")
        target = available[0]
        set_domain_scope([target])
        scoped = list_scoped_domains()
        assert scoped == [target]

    def test_no_scope_list_scoped_equals_list_domains(self):
        set_domain_scope(None)
        assert list_scoped_domains() == list_domains()


class TestCategoryRegex:
    def test_valid_lowercase(self):
        assert _CATEGORY_RE.match("gotchas")
        assert _CATEGORY_RE.match("tips")
        assert _CATEGORY_RE.match("best-practices")
        assert _CATEGORY_RE.match("faq")
        assert _CATEGORY_RE.match("my_category")

    def test_uppercase_rejected(self):
        assert not _CATEGORY_RE.match("Gotchas")
        assert not _CATEGORY_RE.match("TIPS")

    def test_slash_rejected(self):
        assert not _CATEGORY_RE.match("bad/cat")

    def test_empty_rejected(self):
        assert not _CATEGORY_RE.match("")

    def test_space_rejected(self):
        assert not _CATEGORY_RE.match("two words")

    def test_dot_rejected(self):
        assert not _CATEGORY_RE.match("file.txt")