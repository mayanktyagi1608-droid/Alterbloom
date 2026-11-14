#!/usr/bin/env bash
# Renders one set of artwork to the images the site serves.
#
#   scripts/art/render.sh table_setting
#   scripts/art/render.sh envelope
#
# 1. runs scripts/art/<name>.py <tmp-folder>, which writes one HTML page (a
#    single SVG) per picture and prints one line for each:
#        <page.html> <width> <height> <output-name> <widths,comma,separated> <rgb|rgba> <quality>
# 2. photographs each page with headless Chrome at 2x on a transparent
#    background;
# 3. saves img/<output-name>-<width>.webp for every width asked for.
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

python3 "$here/$name.py" "$tmp" | while read -r page w h out widths mode quality; do
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    --headless=new --disable-gpu --hide-scrollbars --no-first-run --no-default-browser-check \
    --user-data-dir="$tmp/chrome-profile" --allow-file-access-from-files \
    --default-background-color=00000000 \
    --force-device-scale-factor=2 --window-size="$w,$h" --virtual-time-budget=4000 \
    --screenshot="$tmp/$out.png" "file://$tmp/$page" >/dev/null 2>&1 </dev/null

  python3 - "$tmp/$out.png" "$root/img/$out" "$w" "$widths" "$mode" "$quality" <<'PY'
import sys
from PIL import Image
src, out, w, widths, mode, q = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5], int(sys.argv[6])
im = Image.open(src).convert("RGBA")
assert im.width == w * 2, "expected a 2x screenshot, got %dpx for a %dpx page" % (im.width, w)
if mode == "rgb":
    im = im.convert("RGB")
for width in [int(x) for x in widths.split(",")]:
    r = im if width == im.width else im.resize((width, im.height * width // im.width), Image.LANCZOS)
    path = "%s-%d.webp" % (out, width)
    if mode == "rgb":
        r.save(path, "WEBP", quality=q, method=6)
    else:
        r.save(path, "WEBP", quality=q, alpha_quality=92, method=6)
    print(path, r.size)
PY
done
