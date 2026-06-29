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

## Quality Evaluation Platform

CLI tools for Golden Dataset maintenance and quality reporting:

```bash
# Validate Golden Dataset structure (YAML, required fields, dates, difficulty)
python scripts/quality/validate_dataset.py --domain godot

# Plus: verify expected_source_files exist in domains/<domain>/sources/ or personal/
python scripts/quality/validate_dataset.py --domain godot --check-sources

# Plus: treat URL validation warnings as errors (file/ftp/data schemes, localhost,
# loopback IPs, RFC1918 private IPs)
python scripts/quality/validate_dataset.py --domain godot --strict-urls

# Add a curated question to the Golden Dataset (manual curation step,
# test-hub-feature is forbidden from running this)
python scripts/quality/add_question.py \
  --domain godot \
  --question "How do I rotate a Node3D around the Y axis?" \
  --expected-sources godot-docs-reference-packed.md \
  --difficulty easy \
  --tags rotation,node3d,3d,gdscript \
  --notes "Beginner question"

# Run evaluation against the live index (requires prebuilt index)
python scripts/quality/run_evaluation.py --domain godot
python scripts/quality/run_evaluation.py --domain godot --output results.json
python scripts/quality/run_evaluation.py --domain godot --baseline previous.json

# Generate Markdown and JSON report from a results.json
python scripts/quality/generate_report.py --input results.json
python scripts/quality/generate_report.py --input results.json --output-dir my-reports/
python scripts/quality/generate_report.py --input results.json --archive
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
