#!/usr/bin/env bash
# Install the skill into the personal Claude Code skills directory.
# Usage: ./install.sh [target_dir]   (default: ~/.claude/skills/travel-planner)
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${1:-$HOME/.claude/skills/travel-planner}"

if [ ! -f "$SRC/SKILL.md" ]; then
  echo "SKILL.md not found next to install.sh" >&2
  exit 1
fi

mkdir -p "$DEST"
# Copy only what the skill needs (no git history, tests cache or local files).
for item in SKILL.md README.md README.es.md LICENSE references templates scripts examples assets; do
  if [ -e "$SRC/$item" ]; then
    rm -rf "${DEST:?}/$item"
    cp -R "$SRC/$item" "$DEST/$item"
  fi
done
find "$DEST" -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null || true

echo "Installed to $DEST"
echo "Start a new Claude Code session and ask for a trip, for example:"
echo '  "I have a long weekend in November, budget 300, help me choose and prepare the purchases."'
