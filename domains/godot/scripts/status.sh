#!/usr/bin/env bash
# status.sh — Show Godot domain status
#
# Usage:
#   ./domains/godot/scripts/status.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
DOMAIN_DIR="${REPO_ROOT}/domains/godot"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

echo ""
echo -e "${BOLD}Domain: godot${NC}"
echo ""

# Sources
echo "Sources:"
for f in "$DOMAIN_DIR/sources"/*.md; do
    if [ -f "$f" ]; then
        size=$(du -h "$f" | cut -f1)
        lines=$(wc -l < "$f")
        echo -e "  ${GREEN}✓${NC} $(basename "$f") — ${size}, ${lines} lines"
    fi
done
echo ""

# Personal
echo "Personal knowledge:"
for f in "$DOMAIN_DIR/personal"/*.md; do
    if [ -f "$f" ]; then
        entries=$(grep -c "^## " "$f" 2>/dev/null || echo 0)
        echo -e "  ${GREEN}✓${NC} $(basename "$f") — ${entries} entries"
    fi
done
echo ""

# Index
INDEX_DIR="${REPO_ROOT}/chromadb_data"
if [ -d "$INDEX_DIR" ]; then
    index_mb=$(python3 -c "
import os
from pathlib import Path
d = Path('${INDEX_DIR}')
if d.exists():
    total = sum(f.stat().st_size for f in d.rglob('*') if f.is_file())
    print(f'{total/1024/1024:.0f}')
" 2>/dev/null || echo "?")
    echo -e "ChromaDB Index: ${GREEN}✓${NC} ${index_mb} MB (collection: godot_knowledge)"
else
    echo -e "ChromaDB Index: ${RED}✗${NC} NOT BUILT"
    echo "  Build: python3 scripts/embed_index.py --domain godot"
fi
echo ""

echo "Commands:"
echo "  Update:  ./domains/godot/scripts/update.sh"
echo "  Search:  ./domains/godot/scripts/search.sh '<query>'"
echo "  Status:  ./domains/godot/scripts/status.sh"
echo ""
