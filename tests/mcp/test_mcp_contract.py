"""MCP Contract Tests — verify the 6 tool functions return correct contracts.

Calls the actual tool functions (not via stdio transport) and verifies
return types, required keys, and error handling.

Run: pytest tests/mcp/test_mcp_contract.py -v -m mcp
"""

import pytest

pytestmark = pytest.mark.mcp


@pytest.fixture(autouse=True)
def reset_scope():
    """Reset domain scope before and after each test."""
    from mcp_servers.knowledge_hub.tools import set_domain_scope
    set_domain_scope(None)
    yield
    set_domain_scope(None)


class TestListDomains:
    def test_list_domains_returns_list(self):
        """list_domains should return a list of strings."""
        from mcp_servers.knowledge_hub.tools import list_domains

        result = list_domains()
        assert isinstance(result, list)
        for d in result:
            assert isinstance(d, str)

    def test_list_scoped_domains_unscoped(self):
        """Without scope, list_scoped_domains == list_domains."""
        from mcp_servers.knowledge_hub.tools import list_domains, list_scoped_domains

        assert list_scoped_domains() == list_domains()

    def test_list_scoped_domains_with_scope(self):
        """With scope, only scoped domains are returned."""
        from mcp_servers.knowledge_hub.tools import list_domains, set_domain_scope, list_scoped_domains

        all_domains = list_domains()
        if not all_domains:
            pytest.skip("no domains available")
        target = all_domains[0]
        set_domain_scope([target])
        assert list_scoped_domains() == [target]


class TestSearchKnowledge:
    def test_search_returns_dict_with_required_keys(self):
        """search_knowledge should return a dict with results, total_found, mode, query_time_ms."""
        from mcp_servers.knowledge_hub.tools import list_domains, search_knowledge

        domains = list_domains()
        if not domains:
            pytest.skip("no domains available")
        result = search_knowledge(domain=domains[0], query="test", max_results=3)
        assert isinstance(result, dict)
        assert "results" in result
        assert "total_found" in result
        assert "mode" in result
        assert "query_time_ms" in result

    def test_search_out_of_scope_returns_error(self):
        """Out-of-scope domain should return an error dict, not raise."""
        from mcp_servers.knowledge_hub.tools import list_domains, set_domain_scope, search_knowledge

        all_domains = list_domains()
        if len(all_domains) < 2:
            pytest.skip("need at least 2 domains")
        set_domain_scope([all_domains[0]])
        result = search_knowledge(domain=all_domains[1], query="test")
        assert "error" in result
        assert all_domains[0] in result["error"]


class TestGetDomainStatus:
    def test_status_for_single_domain(self):
        """get_domain_status(domain) should return a dict with status keys."""
        from mcp_servers.knowledge_hub.tools import list_domains, get_domain_status

        domains = list_domains()
        if not domains:
            pytest.skip("no domains available")
        result = get_domain_status(domains[0])
        assert domains[0] in result
        info = result[domains[0]]
        assert "sources" in info
        assert "personal_notes" in info
        assert "index_exists" in info
        assert "index_size_mb" in info

    def test_status_for_all_domains(self):
        """get_domain_status() (no arg) should return all scoped domains."""
        from mcp_servers.knowledge_hub.tools import list_scoped_domains, get_domain_status

        result = get_domain_status()
        assert isinstance(result, dict)
        for d in list_scoped_domains():
            assert d in result

    def test_status_out_of_scope_returns_error(self):
        """Out-of-scope domain should return an error dict."""
        from mcp_servers.knowledge_hub.tools import list_domains, set_domain_scope, get_domain_status

        all_domains = list_domains()
        if len(all_domains) < 2:
            pytest.skip("need at least 2 domains")
        set_domain_scope([all_domains[0]])
        result = get_domain_status(all_domains[1])
        assert "error" in result


class TestAddPersonalNote:
    def test_add_note_returns_status_added(self, tmp_path, monkeypatch):
        """add_personal_note should return status='added'."""
        from mcp_servers.knowledge_hub.tools import add_personal_note

        # Create a fake domain
        domain_dir = tmp_path / "domains" / "testdomain"
        (domain_dir / "personal").mkdir(parents=True)
        (domain_dir / "domain.md").write_text("# Domain: testdomain\n")

        from mcp_servers.knowledge_hub import config
        monkeypatch.setattr(config, "DOMAINS_DIR", tmp_path / "domains")

        result = add_personal_note("testdomain", "Topic", "Content", "gotchas")
        assert result["status"] == "added"

    def test_add_note_invalid_category(self, tmp_path, monkeypatch):
        """Invalid category should return error."""
        from mcp_servers.knowledge_hub.tools import add_personal_note

        domain_dir = tmp_path / "domains" / "testdomain"
        (domain_dir / "personal").mkdir(parents=True)
        (domain_dir / "domain.md").write_text("# Domain: testdomain\n")

        from mcp_servers.knowledge_hub import config
        monkeypatch.setattr(config, "DOMAINS_DIR", tmp_path / "domains")

        result = add_personal_note("testdomain", "T", "C", "bad/cat")
        assert "error" in result


class TestListPersonalNotes:
    def test_list_notes_nonexistent_domain(self):
        """list_personal_notes on nonexistent domain should return error."""
        from mcp_servers.knowledge_hub.tools import list_personal_notes

        result = list_personal_notes("totally_nonexistent_xyz")
        assert "error" in result


class TestUpdateDomain:
    def test_update_nonexistent_domain(self):
        """update_domain on nonexistent domain should return error (no update.sh)."""
        from mcp_servers.knowledge_hub.tools import update_domain

        result = update_domain("totally_nonexistent_xyz")
        assert "error" in result
        assert "update.sh" in result["error"]