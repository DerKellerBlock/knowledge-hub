# Validation — Knowledge Hub

## Verfügbare Checks

### Shell-Syntax
```bash
find . -name "*.sh" -exec bash -n {} \;
```

### Python-Syntax
```bash
find . -name "*.py" -not -path "*/__pycache__/*" -exec python3 -m py_compile {} \;
```

### JSON
```bash
python3 -c "import json; json.load(open('.opencode/opencode.json'))"
```

### MCP-Server Quick-Test
```bash
timeout 10 python3 -c "
import sys; sys.path.insert(0,'.')
from mcp_servers.knowledge_hub.tools import list_domains
print(list_domains())
"
```

### Domain-Status
```bash
./domains/godot/scripts/status.sh
```

### GitHub Action
```bash
[ -f .github/workflows/update-knowledge.yml ] && echo "✅" || echo "❌"
```

### Git
```bash
git status --short
```

## Structure Validation

```bash
./scripts/workspace_check.sh
./scripts/workspace_status.sh
python3 -m json.tool .opencode/opencode.json
bash -n scripts/workspace_check.sh scripts/workspace_status.sh
```

## Test Suite

```bash
pytest -m unit
pytest -m integration
pytest -m e2e
pytest -m mcp
pytest -m quality
pytest --cov=scripts --cov=mcp_servers/knowledge_hub --cov-report=term-missing
```

## Knowledge-QA Checklist

For domain/source changes, `test-hub-feature` checks:

- realistic questions from changed sources
- real-world problem prompts from websearch for domain/source changes
- relevant top search results
- `source_file` present
- PDF `page_start`/`page_end` present when available
- evidence snippets human can inspect
- weak or missing coverage documented as findings
