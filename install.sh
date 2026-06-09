#!/usr/bin/env bash
# install.sh — Install Knowledge Hub Skills in another OpenCode project
#
# Usage:
#   cd ~/Documents/work/knowledge-hub
#   ./install.sh /path/to/target-project              # alle Domains
#   ./install.sh /path/to/target-project godot        # nur godot
#   ./install.sh /path/to/target-project godot blender # mehrere
#   ./install.sh /path/to/target-project --symlink     # Symlinks (dev mode)
#
# What it does:
#   - Copies (or symlinks) .agents/skills/ from hub to target project
#   - Skips if target skill already exists (no overwrite)
#   - Lists installed skills after completion

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

log_info()  { echo -e "${GREEN}[INFO]${NC}  $*"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*"; }

HUB_ROOT="$(cd "$(dirname "$0")" && pwd)"
USE_SYMLINK=false
TARGET=""
DOMAINS=()

while [[ $# -gt 0 ]]; do
    case "$1" in
        --symlink) USE_SYMLINK=true; shift ;;
        -h|--help)
            echo "Usage: $0 [--symlink] <target-project> [domain...]"
            echo ""
            echo "Install Knowledge Hub Skills in another OpenCode project."
            echo ""
            echo "Options:"
            echo "  --symlink    Create symlinks instead of copies (dev mode)"
            echo ""
            echo "Examples:"
            echo "  $0 ~/Documents/work/nak-hopper-game godot"
            echo "  $0 ~/my-project --symlink"
            exit 0
            ;;
        *)
            if [ -z "$TARGET" ]; then
                TARGET="$1"
            else
                DOMAINS+=("$1")
            fi
            shift
            ;;
    esac
done

if [ -z "$TARGET" ]; then
    log_error "No target project specified."
    echo "Usage: $0 <target-project> [domain...]"
    exit 1
fi

if [ ! -d "$TARGET" ]; then
    log_error "Target directory does not exist: $TARGET"
    exit 1
fi

# If no domains specified, install all available
if [ ${#DOMAINS[@]} -eq 0 ]; then
    for d in "$HUB_ROOT/.agents/skills"/*/; do
        [ -d "$d" ] || continue
        DOMAINS+=("$(basename "$d")")
    done
fi

if [ ${#DOMAINS[@]} -eq 0 ]; then
    log_error "No domains found in $HUB_ROOT/.agents/skills/"
    log_error "Run: mkdir -p .agents/skills/<domain>/references"
    exit 1
fi

log_info "Installing Knowledge Hub Skills into: $TARGET"
log_info "Domains: ${DOMAINS[*]}"
if [ "$USE_SYMLINK" = true ]; then
    log_info "Mode: symlink (development)"
else
    log_info "Mode: copy"
fi
echo ""

INSTALLED=0
SKIPPED=0

for domain in "${DOMAINS[@]}"; do
    src="$HUB_ROOT/.agents/skills/$domain"
    dst="$TARGET/.agents/skills/$domain"

    if [ ! -d "$src" ]; then
        log_warn "  $domain: source not found, skipping"
        SKIPPED=$((SKIPPED + 1))
        continue
    fi

    if [ -d "$dst" ] || [ -L "$dst" ]; then
        log_warn "  $domain: already exists in target, skipping (no overwrite)"
        SKIPPED=$((SKIPPED + 1))
        continue
    fi

    mkdir -p "$(dirname "$dst")"

    if [ "$USE_SYMLINK" = true ]; then
        ln -s "$src" "$dst"
        log_info "  $domain: symlinked ✓"
    else
        cp -r "$src" "$dst"
        log_info "  $domain: copied ✓"
    fi
    INSTALLED=$((INSTALLED + 1))
done

echo ""
echo -e "${BOLD}Done:${NC} $INSTALLED installed, $SKIPPED skipped"

if [ "$USE_SYMLINK" = true ]; then
    echo ""
    echo -e "${YELLOW}Symlink mode active.${NC} Changes in hub are immediately visible in target."
    echo "To remove: rm $TARGET/.agents/skills/<domain>"
fi
