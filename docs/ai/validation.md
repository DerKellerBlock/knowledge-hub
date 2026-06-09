# Validation — Knowledge Hub

## Verfügbare Checks

### Shell-Skript-Syntax
```bash
# Alle Shell-Skripte prüfen
find . -name "*.sh" -exec bash -n {} \;
```

### Python-Syntax
```bash
# Alle Python-Dateien prüfen
find . -name "*.py" -exec python3 -m py_compile {} \;
```

### JSON-Validierung
```bash
# opencode.json prüfen
python3 -c "import json; json.load(open('.opencode/opencode.json'))"
```

### Verzeichnisstruktur
```bash
# Prüft ob alle erwarteten Ordner existieren
for dir in domains scripts mcp_servers docs; do
  [ -d "$dir" ] && echo "✓ $dir" || echo "✗ $dir MISSING"
done
```

### ChromaDB-Status
```bash
# Prüft ob Index existiert
python3 -c "
import os
if os.path.exists('chromadb_data'):
    size = sum(os.path.getsize(os.path.join(r,f)) for r,_,fs in os.walk('chromadb_data') for f in fs)
    print(f'Index: {size/1024/1024:.0f} MB')
else:
    print('Index: NOT FOUND')
"
```

### Git-Status
```bash
git status --short
git diff --stat
```

## Noch nicht verfügbar

- pytest/bats Unit-Tests (später)
- MCP-Server-Integrationstest (später)
- Embedding-Qualitäts-Test (später)
