#!/usr/bin/env bash
# Guards against drifting from css/tokens.css.
# Flags raw hex colors and hardcoded font-family declarations in any
# .html/.css file other than tokens.css itself. Run before committing any
# UI change: scripts/check-design-tokens.sh
#
# A hit here doesn't always mean something is wrong (e.g. inline SVG data
# URIs, comments) — but every hit should be checked against
# DESIGN_SYSTEM.md, and any real new value belongs in css/tokens.css after
# an explicit discussion, not inline.

set -uo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

files=$(find . \
  -type d \( -name .git -o -name node_modules \) -prune -o \
  -type f \( -name "*.html" -o -name "*.css" \) -not -name "tokens.css" -print)

found=0

echo "== Raw hex colors outside css/tokens.css =="
hex_hits=$(grep -nE '#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b' $files 2>/dev/null | grep -v '^\s*$')
if [ -n "$hex_hits" ]; then
  echo "$hex_hits"
  found=1
else
  echo "(none)"
fi

echo
echo "== font-family declarations outside css/tokens.css =="
font_hits=$(grep -nE 'font-family\s*:' $files 2>/dev/null | grep -v 'var(--font-')
if [ -n "$font_hits" ]; then
  echo "$font_hits"
  found=1
else
  echo "(none)"
fi

echo
if [ "$found" -eq 1 ]; then
  echo "Found values outside the design system. Check each against DESIGN_SYSTEM.md."
  echo "A genuinely new value goes into css/tokens.css after discussing it with the user first."
  exit 1
else
  echo "Clean — no stray colors or fonts found."
  exit 0
fi
