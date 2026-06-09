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
