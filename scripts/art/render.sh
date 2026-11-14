#!/usr/bin/env bash
# Renders one piece of artwork to the images the site serves.
#
#   scripts/art/render.sh table_setting
#
# 1. runs scripts/art/<name>.py, which writes <name>.html (one SVG) into a
#    temporary folder and prints "<width> <height> <output-name>";
# 2. photographs it with headless Chrome at 2x on a transparent background;
# 3. saves img/<output-name>-<width>.webp at 2x and 1x.
#
# Needs Google Chrome and Python 3 with Pillow. Only needed when the artwork
# changes: the rendered images are committed, so the Netlify build never
# runs this.
set -euo pipefail

name="$1"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root="$(cd "$here/../.." && pwd)"
tmp="${ART_TMP:-${TMPDIR:-/tmp}/alterbloom-art}"
mkdir -p "$tmp" "$root/img"

read -r w h out < <(python3 "$here/$name.py" "$tmp/$name.html")

"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --hide-scrollbars --no-first-run --no-default-browser-check \
  --user-data-dir="$tmp/chrome-profile" --allow-file-access-from-files \
  --default-background-color=00000000 \
  --force-device-scale-factor=2 --window-size="$w,$h" --virtual-time-budget=4000 \
  --screenshot="$tmp/$name.png" "file://$tmp/$name.html" >/dev/null 2>&1

python3 - "$tmp/$name.png" "$root/img/$out" "$w" <<'PY'
import sys
from PIL import Image
src, out, w = sys.argv[1], sys.argv[2], int(sys.argv[3])
im = Image.open(src).convert("RGBA")
assert im.width == w * 2, "expected a 2x screenshot, got %dpx for a %dpx page" % (im.width, w)
for width in (w * 2, w):
    r = im if width == im.width else im.resize((width, im.height * width // im.width), Image.LANCZOS)
    path = "%s-%d.webp" % (out, width)
    r.save(path, "WEBP", quality=84, alpha_quality=92, method=6)
    print(path, r.size)
PY
