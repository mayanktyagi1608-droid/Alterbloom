"""Christophe's desk, on the Journal page: Christophe at his typewriter, in the
same cut-paper style as the poppy and the portrait.

He faces us and the typewriter faces him, so we see the back of the machine.
The page comes up over the roller and falls towards us like a waterfall.

Two pictures, both on a transparent ground:
  writer       the scene: poppies, Christophe, the desk and the typewriter,
               with a blank sheet standing in the roller;
  writer-page  one repeating length of the typed page. The Journal page lays it
               over the scene from the roller down and lets it pour out as the
               visitor scrolls (see css/sections.css, .desk-page, and js/desk.js).
               It tiles top to bottom, so its edges and typed lines repeat
               exactly every PAGE_H.

Run through scripts/art/render.sh writer. Colours come from css/tokens.css via
T(); see "Realism exceptions" in DESIGN_SYSTEM.md.
"""
import math
import os
import random
import sys
from illo import T, f, poppy, stem, paint_filter, page
from portrait import groom

W, H = 420, 520                 # the scene
PAGE_W, PAGE_H = 200, 600       # one repeat of the falling page
SHEET = 150                     # width of the page itself inside PAGE_W
CREST = 262                     # where the page folds over, in scene units (matches .desk-page in the CSS)

LINEN, CREAM_S, CREAM_D = T("swatch-linen"), T("real-cream-shade"), T("real-cream-deep")
TEAL, TEAL_D, SKY = T("swatch-teal"), T("swatch-teal-deep"), T("swatch-sky")
BRASS, BRASS_D, BRASS_L = T("real-brass"), T("real-brass-shade"), T("real-brass-light")
HAIR, SHADOW = T("real-hair"), T("real-shadow")


def scene():
    defs = paint_filter("paint", 2.0, 0.09)
    defs += '<clipPath id="behind"><rect width="%d" height="332"/></clipPath>' % W
    defs += ('<filter id="cast" x="-30%%" y="-30%%" width="160%%" height="160%%">'
             '<feDropShadow dx="0" dy="7" stdDeviation="8" flood-color="%s" flood-opacity=".45"/></filter>' % SHADOW)
    defs += '<filter id="soft" x="-20%" y="-200%" width="140%" height="500%"><feGaussianBlur stdDeviation="6"/></filter>'
    da, pa = poppy(R=118, seed=41, palette="coral", petals=6, rot=0.4)
    db, pb = poppy(R=50, seed=63, palette="red", petals=5, rot=0.2)
    defs += da + db

    # behind him: two poppies in a row along the back of the desk
    art = stem([(338, 150), (352, 300), (340, 478)], w=13) + stem([(64, 250), (72, 360), (62, 478)], w=8)
    art += '<g transform="translate(332 122)">%s</g><g transform="translate(62 236)">%s</g>' % (pa, pb)

    # Christophe, from the chest up; the machine hides the rest
    art += '<g filter="url(#cast)" clip-path="url(#behind)"><g transform="translate(210 142) scale(.78)">%s</g></g>' % groom("L", garlands=False)

    # the desk: its top, its front edge, and the machine's shadow on it
    d = '<path d="M8 474H412L420 494H0Z" fill="%s"/><path d="M0 494H420V503H0Z" fill="%s"/>' % (TEAL, TEAL_D)
    d += '<path d="M8 474H412" stroke="%s" stroke-opacity=".28" stroke-width="2"/>' % SKY
    d += '<ellipse cx="210" cy="478" rx="156" ry="7" fill="%s" fill-opacity=".5" filter="url(#soft)"/>' % SHADOW
    # a few finished pages, squared up at the corner of the desk
    for i, (x, y, r) in enumerate([(18, 470, -5), (22, 465, 3), (20, 460, -2)]):
        d += '<g transform="rotate(%d %d %d)"><path d="M%d %dh58l8 12h-74Z" fill="%s" stroke="%s" stroke-width=".8"/></g>' % (r, x + 30, y, x + 8, y, LINEN if i == 2 else CREAM_S, CREAM_D)
    d += '<path d="M33 464h40M32 468h34" stroke="%s" stroke-opacity=".45" stroke-width="1.4" stroke-linecap="round"/>' % TEAL_D
    art += d

    # the typewriter, from behind
    m = ""
    for x in (114, 306):                                                                   # ribbon spools
        m += '<circle cx="%d" cy="298" r="25" fill="%s" stroke="%s" stroke-width="2"/><circle cx="%d" cy="298" r="15" fill="%s"/><circle cx="%d" cy="298" r="5" fill="%s"/>' % (x, TEAL, TEAL_D, x, HAIR, x, BRASS)
    m += '<path d="M122 304H298L292 270H128Z" fill="%s"/><path d="M128 270H292" stroke="%s" stroke-opacity=".4" stroke-width="2"/>' % (TEAL, SKY)   # paper rest
    m += '<path d="M147 306H273L275 %dH145Z" fill="%s"/>' % (CREST, CREAM_S)              # the sheet standing in the roller: its blank side
    m += '<path d="M147 306H273L273.5 296H146.5Z" fill="%s" fill-opacity=".5"/>' % CREAM_D
    m += '<rect x="58" y="298" width="304" height="28" rx="13" fill="%s"/>' % HAIR         # roller
    m += '<path d="M74 305H346" stroke="%s" stroke-opacity=".28" stroke-width="3" stroke-linecap="round"/>' % SKY
    for x in (50, 370):                                                                    # roller knobs
        m += '<circle cx="%d" cy="312" r="18" fill="%s"/><circle cx="%d" cy="312" r="18" fill="none" stroke="%s" stroke-width="3" stroke-dasharray="2 4"/>' % (x, BRASS, x, BRASS_D)
        m += '<circle cx="%d" cy="312" r="7" fill="%s"/><circle cx="%d" cy="309" r="3" fill="%s" fill-opacity=".8"/>' % (x, BRASS_D, x - 4, BRASS_L)
    m += '<path d="M358 310C372 296 384 280 392 262" fill="none" stroke="%s" stroke-width="7" stroke-linecap="round"/>' % BRASS              # carriage lever
    m += '<path d="M360 306C372 294 382 280 389 264" fill="none" stroke="%s" stroke-width="2" stroke-linecap="round"/><circle cx="393" cy="258" r="9" fill="%s"/>' % (BRASS_L, LINEN)
    m += '<rect x="70" y="324" width="280" height="16" fill="%s"/><rect x="70" y="333" width="280" height="7" fill="%s" fill-opacity=".45"/>' % (BRASS, BRASS_D)
    for x in range(82, 344, 12):                                                           # the scale along the carriage
        m += '<path d="M%d 326v%d" stroke="%s" stroke-opacity=".7" stroke-width="1.2"/>' % (x, 6 if (x - 82) % 60 == 0 else 3, BRASS_D)
    m += '<path d="M86 340H334L352 452Q353 468 338 468H82Q67 468 68 452Z" fill="%s"/>' % TEAL_D                                                # body
    m += '<path d="M86 340H334L337 354H83Z" fill="%s"/>' % TEAL
    m += '<path d="M86 340L68 452Q67 468 82 468H96L104 354Z" fill="%s" fill-opacity=".12"/>' % SKY
    for y in (384, 397, 410, 423):                                                         # vents
        m += '<path d="M98 %dH132M288 %dH322" stroke="%s" stroke-opacity=".32" stroke-width="3" stroke-linecap="round"/>' % (y, y, SKY)
    for x in (96, 324):
        m += '<circle cx="%d" cy="448" r="5" fill="%s"/><path d="M%d 448h6" stroke="%s" stroke-width="1.4"/>' % (x, BRASS, x - 3, BRASS_D)
    m += '<rect x="92" y="466" width="32" height="9" fill="%s"/><rect x="296" y="466" width="32" height="9" fill="%s"/>' % (HAIR, HAIR)
    art += '<g filter="url(#cast)">%s</g>' % m
    return '<g filter="url(#paint)">%s</g>' % art, defs


def falling_page():
    """One repeat of the page. Everything here is periodic over PAGE_H so the tile joins itself."""
    rnd = random.Random(23)
    cx = lambda y: PAGE_W / 2 + 6 * math.sin(2 * math.pi * y / PAGE_H) + 3 * math.sin(4 * math.pi * y / PAGE_H + 1.1)
    ys = range(-140, PAGE_H + 141, 10)
    left = [(cx(y) - SHEET / 2, y) for y in ys]
    right = [(cx(y) + SHEET / 2, y) for y in ys]
    d = "M" + "L".join("%s %s" % (f(x), f(y)) for x, y in left + right[::-1]) + "Z"
    defs = ('<filter id="fall" x="-20%%" y="-5%%" width="140%%" height="110%%">'
            '<feDropShadow dx="0" dy="5" stdDeviation="6" flood-color="%s" flood-opacity=".42"/></filter>' % SHADOW)
    defs += '<filter id="fold" x="-10%" y="-80%" width="120%" height="260%"><feGaussianBlur stdDeviation="9"/></filter>'
    defs += '<clipPath id="sheet"><path d="%s"/></clipPath>' % d
    g = '<path d="%s" fill="%s" filter="url(#fall)"/>' % (d, LINEN)
    folds = ""
    for k in (-1, 0, 1):                                                                   # soft folds where the page bellies out
        for y, o in ((96, .5), (298, .38), (488, .46)):
            folds += '<rect x="0" y="%d" width="%d" height="34" fill="%s" fill-opacity="%s" filter="url(#fold)"/>' % (y + k * PAGE_H, PAGE_W, CREAM_S, o)
    g += '<g clip-path="url(#sheet)">%s</g>' % folds
    n = 42                                                                                 # typed lines, in short paragraphs
    step = PAGE_H / n
    para = [rnd.randint(4, 8)]
    line, new = 0, True
    for i in range(n):
        y = (i + 0.5) * step
        if line == para[-1]:
            para.append(rnd.randint(4, 8))
            line, new = 0, True
            continue                                                                       # a blank line between paragraphs
        last = line == para[-1] - 1
        a = SHEET * (0.30 if new else 0.39)
        b = SHEET * (0.39 - (rnd.uniform(0.25, 0.5) if last else rnd.choice([0, 0, 0.02, 0.05])))
        g += '<path d="M%s %sH%s" stroke="%s" stroke-opacity=".5" stroke-width="2.3" stroke-linecap="round"/>' % (f(cx(y) - a), f(y), f(cx(y) + b), TEAL_D)
        line, new = line + 1, False
    return g, defs


out_dir = sys.argv[1] if len(sys.argv) > 1 else "."
body, defs = scene()
open(os.path.join(out_dir, "writer.html"), "w").write(page("0 0 %d %d" % (W, H), W, H, body, defs))
print("writer.html", W, H, "writer", "840,560", "rgba", 84)
body, defs = falling_page()
open(os.path.join(out_dir, "writer-page.html"), "w").write(page("0 0 %d %d" % (PAGE_W, PAGE_H), PAGE_W, PAGE_H, body, defs))
print("writer-page.html", PAGE_W, PAGE_H, "writer-page", "400", "rgba", 84)
