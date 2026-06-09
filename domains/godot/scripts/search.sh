#!/usr/bin/env bash
# search.sh — Search Godot domain knowledge (exact + semantic)
#
# Usage:
#   ./domains/godot/scripts/search.sh "CharacterBody3D"               # exact (ripgrep)
#   ./domains/godot/scripts/search.sh --semantic "gravity"            # semantic (ChromaDB)
#   ./domains/godot/scripts/search.sh --hybrid "player movement"       # hybrid (ripgrep + ChromaDB)
#
# Shortcuts:
#   -e    exact (default)
#   -s    semantic
#   -x    hybrid

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
SKILLS_DIR="${REPO_ROOT}/.agents/skills"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

MODE="exact"
QUERY=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        -e|--exact) MODE="exact"; shift ;;
        -s|--semantic) MODE="semantic"; shift ;;
        -x|--hybrid) MODE="hybrid"; shift ;;
        -h|--help)
            echo "Usage: $0 [MODE] <query>"
            echo ""
            echo "Modes:"
            echo "  -e, --exact      Exact search via ripgrep (default)"
            echo "  -s, --semantic   Semantic search via ChromaDB"
            echo "  -x, --hybrid     Hybrid search (exact + semantic)"
            echo ""
            echo "Examples:"
            echo "  $0 -x 'player character controller'"
            echo "  $0 -s 'how to do gravity'"
            exit 0
            ;;
        *) QUERY="$1"; shift ;;
    esac
done

if [ -z "$QUERY" ]; then
    echo "Usage: $0 [MODE] <query>"
    exit 1
fi

case "$MODE" in
    exact)
        echo -e "${GREEN}Exact search:${NC} $QUERY"
        echo ""
        rg -L --no-ignore -n -i -- "$QUERY" "${SKILLS_DIR}/godot/references/" 2>/dev/null | head -20 || echo "(no matches)"
        ;;
    semantic)
        python3 "${REPO_ROOT}/scripts/embed_search.py" --domain godot --query "$QUERY" --top 5 2>/dev/null
        ;;
    hybrid)
        python3 "${REPO_ROOT}/scripts/hybrid_search.py" --domain godot --query "$QUERY" --top 10 2>/dev/null
        ;;
esac
