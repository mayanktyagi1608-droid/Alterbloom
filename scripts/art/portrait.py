"""The portrait on the Our story page: the two of us in flower garlands, with
giant paper poppies behind, in the same cut-paper style as the poppy.

This is only the picture inside the print. The paper border, the tape, the tilt
and the shadow are ordinary page styles (see css/sections.css, .portrait).

Run through scripts/art/render.sh portrait. Colours come from css/tokens.css
via T(); see "Realism exceptions" in DESIGN_SYSTEM.md.
"""
import math
import os
import random
import sys
from illo import T, f, smooth, poppy, stem, paint_filter, page

W, H = 484, 624
rnd = random.Random(11)

HAIR, HAIR_L = T("real-hair"), T("real-hair-light")
LINEN, CREAM, CREAM_S, CREAM_D = T("swatch-linen"), T("real-cream"), T("real-cream-shade"), T("real-cream-deep")
BRASS, BRASS_D, BRASS_L = T("real-brass"), T("real-brass-shade"), T("real-brass-light")
HI = T("real-highlight")

defs = ('<filter id="figsh" x="-20%%" y="-20%%" width="140%%" height="140%%">'
        '<feDropShadow dx="0" dy="6" stdDeviation="9" flood-color="%s" flood-opacity=".2"/></filter>' % T("real-petal-shadow"))
defs += paint_filter("paint", 2.2, 0.09)

# Garland flowers: marigold, white, peach, cream, coral, yellow.
# The white ones sit on a white shirt, so they are drawn a shade darker with pale petals.
GAR = [(T("real-stamen"), T("real-stamen-light")), (CREAM_D, CREAM), (T("real-petal-coral-light"), T("real-petal-coral-edge")),
       (CREAM_D, LINEN), (T("real-petal-coral"), T("real-petal-coral-light")), (T("real-stamen-light"), T("real-pod"))]


def garland_flower(x, y, r, col, col2):
    g = '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(x), f(y), f(r), col)
    for i in range(6):
        a = i * 1.047 + rnd.uniform(0, 0.6)
        px, py = x + math.cos(a) * r * 0.55, y + math.sin(a) * r * 0.55
        g += '<circle cx="%s" cy="%s" r="%s" fill="%s" fill-opacity=".85"/>' % (f(px), f(py), f(r * 0.48), col2)
    g += '<circle cx="%s" cy="%s" r="%s" fill="%s" fill-opacity=".5"/>' % (f(x), f(y), f(r * 0.3), col)
    return g


def garland(side, top=(38, 92), ctrl=(74, 190), end=(58, 440), n=13, r=17):
    """A strand of carnations down one side of the chest (quadratic curve)."""
    g = ""
    for i in range(n):
        t = i / float(n - 1)
        x = (1 - t) ** 2 * top[0] + 2 * (1 - t) * t * ctrl[0] + t * t * end[0]
        y = (1 - t) ** 2 * top[1] + 2 * (1 - t) * t * ctrl[1] + t * t * end[1]
        x *= side
        if i % 3 == 2:
            g += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s"/>' % (f(x), f(y - r * 0.9), f(r * 0.5), f(r * 0.32), T("real-stem"))
        col, col2 = GAR[(i + (0 if side > 0 else 3)) % len(GAR)]
        g += garland_flower(x + rnd.uniform(-3, 3), y, r * rnd.uniform(0.9, 1.1), col, col2)
    return g


SHIRT = "M-30 88C-70 96 -118 108 -135 140C-150 170 -155 300 -158 460L158 460C155 300 150 170 135 140C118 108 70 96 30 88Z"


def scaled(pts, sx, sy):
    return [(x * sx, y * sy) for (x, y) in pts]


FACE = [(0, -66), (30, -60), (48, -36), (51, -5), (47, 28), (34, 54), (14, 67), (0, 69), (-14, 67), (-34, 54), (-47, 28), (-51, -5), (-48, -36), (-30, -60)]


def groom(kind, garlands=True):
    """One of the two of us: "L" is Christophe, "R" is Mayank. garlands=False for a picture away from the wedding."""
    left = kind == "L"
    if left:
        skin, shade, lip = T("real-skin-a"), T("real-skin-a-shade"), T("real-lip-a")
    else:
        skin, shade, lip = T("real-skin-b"), T("real-skin-b-shade"), T("real-lip-b")
    collar = 'fill="%s" stroke="%s" stroke-width="1.5" stroke-linejoin="round"' % (LINEN, CREAM_D)
    g = ""
    # ---------- body: a white shirt, in shade down the sides
    g += '<path d="%s" fill="%s"/>' % (SHIRT, LINEN)
    g += '<path d="M-135 140C-150 170 -155 300 -158 460L-120 460C-122 320 -124 200 -112 132Z" fill="%s" fill-opacity=".8"/>' % CREAM_S
    g += '<path d="M135 140C150 170 155 300 158 460L124 460C126 320 126 200 114 132Z" fill="%s" fill-opacity=".55"/>' % CREAM_S
    g += '<path d="M-24 44L24 44L27 96C10 112 -10 112 -27 96Z" fill="%s"/>' % shade           # neck
    if left:
        # buttoned collar and a patterned tie
        g += '<path d="M-8 126L8 126L19 460L-19 460Z" fill="%s"/>' % T("swatch-teal")
        dots = [T("real-petal-coral"), T("swatch-sky"), T("real-petal-coral"), T("real-stamen-light")]
        for i, (tx, ty) in enumerate([(-3, 158), (6, 190), (-6, 224), (5, 258), (-4, 292), (8, 326), (-7, 362), (4, 398), (-5, 434)]):
            g += '<path d="M%d %dc5 -7 12 -2 8 5c-3 5 -9 4 -8 -5Z" fill="%s"/>' % (tx, ty, dots[i % 4])
        g += '<path d="M-10 106L10 106L8 128L-8 128Z" fill="%s"/>' % T("swatch-teal-deep")
        g += '<path d="M-31 82L-3 110L-20 140L-46 104Z" %s/>' % collar
        g += '<path d="M31 82L3 110L20 140L46 104Z" %s/>' % collar
    else:
        # open shirt, a gold choker and a long pendant
        g += '<path d="M-28 90L28 90L15 250L0 286L-15 250Z" fill="%s"/>' % skin
        g += '<path d="M-27 96C-10 112 10 112 27 96L27 104C8 122 -8 122 -27 104Z" fill="%s" fill-opacity=".55"/>' % shade
        chest = ""
        for (hx, hy) in [(-9, 176), (2, 184), (10, 172), (-4, 198), (7, 204), (-10, 214), (1, 222), (9, 230), (-5, 240), (4, 250)]:
            chest += '<path d="M%d %dq4 -5 8 0"/>' % (hx, hy)
        g += '<g fill="none" stroke="%s" stroke-opacity=".3" stroke-width="2" stroke-linecap="round">%s</g>' % (HAIR, chest)
        g += '<path d="M-30 84L-62 108L-30 196L-9 130Z" %s/>' % collar
        g += '<path d="M30 84L62 108L30 196L9 130Z" %s/>' % collar
        g += '<path d="M-15 250L0 286L15 250" fill="none" stroke="%s" stroke-width="1.5"/>' % CREAM_D
        g += '<path d="M-26 96Q0 120 26 96" fill="none" stroke="%s" stroke-width="12" stroke-linecap="round"/>' % BRASS
        g += '<path d="M-26 96Q0 120 26 96" fill="none" stroke="%s" stroke-width="12" stroke-linecap="round" stroke-dasharray="1.5 7"/>' % BRASS_D
        g += '<path d="M-24 93Q0 116 24 93" fill="none" stroke="%s" stroke-width="3.4" stroke-linecap="round" stroke-dasharray=".1 8.5"/>' % T("real-petal-coral-deep")
        g += '<path d="M-22 100Q0 122 22 100" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round" stroke-dasharray=".1 8.5" stroke-dashoffset="4"/>' % T("real-stem-shade")
        g += '<path d="M-25 108Q0 200 25 108" fill="none" stroke="%s" stroke-width="2.4"/>' % BRASS_D
        g += '<path d="M0 148C12 150 16 162 12 172C8 182 4 186 0 192C-4 186 -8 182 -12 172C-16 162 -12 150 0 148Z" fill="%s" stroke="%s" stroke-width="1.4"/>' % (BRASS, BRASS_D)
        g += '<circle cx="0" cy="166" r="4.2" fill="%s"/><circle cx="0" cy="196" r="3" fill="%s"/>' % (T("real-petal-coral-deep"), BRASS_L)
    if garlands:
        g += garland(-1) + garland(1)

    # ---------- head, tilted a little towards the other
    h = '<g transform="rotate(%d 0 62)">' % (5 if left else -7)
    face = scaled(FACE, 1.03, 0.98) if left else scaled(FACE, 0.97, 1.04)
    h += '<ellipse cx="-53" cy="2" rx="8" ry="14" fill="%s"/><ellipse cx="53" cy="2" rx="8" ry="14" fill="%s"/>' % (shade, shade)
    h += '<path d="%s" fill="%s"/>' % (smooth(face), skin)
    h += '<path d="M51 -5C47 28 34 54 14 67C30 44 38 16 36 -30Z" fill="%s" fill-opacity=".5"/>' % shade
    h += '<circle cx="-27" cy="12" r="11" fill="%s" fill-opacity=".16"/><circle cx="27" cy="12" r="11" fill="%s" fill-opacity=".16"/>' % (T("real-petal-coral"), T("real-petal-coral"))
    if left:
        # short boxed beard, moustache joined to it
        beard = [(-53, 6), (-50, 34), (-36, 59), (-15, 72), (0, 74), (15, 72), (36, 59), (50, 34), (53, 6), (46, 16), (40, 26), (28, 28), (14, 24), (0, 26), (-14, 24), (-28, 28), (-40, 26), (-46, 16)]
        h += '<path d="%s" fill="%s"/>' % (smooth(beard), HAIR)
        h += '<path d="M-22 30C-14 22 -5 22 0 26C5 22 14 22 22 30C14 30 6 31 0 31C-6 31 -14 30 -22 30Z" fill="%s"/>' % HAIR
        # a tall quiff, swept up and back, short at the sides
        hair = [(-54, -4), (-57, -38), (-52, -70), (-36, -96), (-8, -110), (22, -108), (46, -92), (58, -62), (56, -8),
                (49, -30), (42, -50), (24, -62), (0, -58), (-22, -50), (-38, -54), (-46, -36), (-48, -14)]
        h += '<path d="%s" fill="%s"/>' % (smooth(hair), HAIR)
        h += '<path d="M-36 -62C-24 -86 2 -98 30 -92M-22 -58C-8 -76 14 -84 40 -76M-44 -44C-42 -58 -38 -66 -32 -72" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % HAIR_L
        # an open, happy smile
        h += '<path d="M-16 35Q0 53 16 35Q0 40 -16 35Z" fill="%s" stroke="%s" stroke-width="2" stroke-linejoin="round"/>' % (LINEN, lip)
        h += '<path d="M-35 -24Q-23 -32 -9 -26M9 -26Q23 -32 35 -24" fill="none" stroke="%s" stroke-width="6.5" stroke-linecap="round"/>' % HAIR
        h += '<ellipse cx="-21" cy="-10" rx="4.6" ry="5" fill="%s"/><ellipse cx="21" cy="-10" rx="4.6" ry="5" fill="%s"/>' % (HAIR, HAIR)
        h += '<circle cx="-19.5" cy="-11.5" r="1.4" fill="%s"/><circle cx="22.5" cy="-11.5" r="1.4" fill="%s"/>' % (HI, HI)
    else:
        # fuller beard
        beard = [(-51, -8), (-50, 32), (-38, 64), (-16, 82), (0, 85), (16, 82), (38, 64), (50, 32), (51, -8), (44, 4), (38, 18), (26, 22), (12, 18), (0, 20), (-12, 18), (-26, 22), (-38, 18), (-44, 4)]
        h += '<path d="%s" fill="%s"/>' % (smooth(beard), HAIR)
        # hair slicked straight back, faded at the sides
        h += '<path d="M-51 -6C-55 -30 -50 -52 -40 -64L-38 -30Z" fill="%s"/><path d="M51 -6C55 -30 50 -52 40 -64L38 -30Z" fill="%s"/>' % (HAIR_L, HAIR_L)
        hair = [(-44, -36), (-46, -58), (-34, -80), (-10, -92), (16, -92), (38, -80), (48, -58), (45, -36), (36, -52), (20, -60), (0, -62), (-20, -60), (-36, -52)]
        h += '<path d="%s" fill="%s"/>' % (smooth(hair), HAIR)
        h += '<path d="M-30 -62C-26 -76 -14 -84 -4 -86M-12 -62C-8 -76 4 -84 16 -86M8 -62C12 -74 22 -80 32 -78" fill="none" stroke="%s" stroke-width="2.6" stroke-linecap="round"/>' % HAIR_L
        # a wide smile under a handlebar moustache with curled tips
        h += '<path d="M-18 36Q0 56 18 36Q0 42 -18 36Z" fill="%s" stroke="%s" stroke-width="2" stroke-linejoin="round"/>' % (LINEN, lip)
        h += ('<path d="M0 22C-10 16 -24 20 -32 30C-38 36 -45 31 -43 24C-40 31 -33 28 -27 21C-17 12 -5 14 0 19'
              'C5 14 17 12 27 21C33 28 40 31 43 24C45 31 38 36 32 30C24 20 10 16 0 22Z" fill="%s" stroke="%s" stroke-width="3.4" stroke-linejoin="round"/>' % (HAIR, HAIR))
        # a lighter line over the moustache so it reads against the beard
        h += '<path d="M-2 18C-8 13 -20 14 -28 22C-33 28 -39 30 -42 25M2 18C8 13 20 14 28 22C33 28 39 30 42 25" fill="none" stroke="%s" stroke-width="2.2" stroke-linecap="round"/>' % HAIR_L
        h += '<path d="M-35 -23Q-23 -32 -9 -27M9 -27Q23 -32 35 -23" fill="none" stroke="%s" stroke-width="6" stroke-linecap="round"/>' % HAIR
        h += '<path d="M-27 -8Q-21 -16 -15 -8M15 -8Q21 -16 27 -8" fill="none" stroke="%s" stroke-width="3.6" stroke-linecap="round"/>' % HAIR
        h += '<circle cx="56" cy="16" r="4.4" fill="none" stroke="%s" stroke-width="2.4"/>' % BRASS
    h += '<path d="M3 -14C6 -2 9 6 7 11C4 15 -3 15 -5 12" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>' % shade
    h += '</g>'
    return g + h


# ------------------------------------------------------------------ the picture
def main():
    global defs
    art = '<rect width="%d" height="%d" fill="%s"/>' % (W, H, LINEN)
    art += '<path d="M12 %d V222 A230 230 0 0 1 472 222 V%d Z" fill="%s" fill-opacity=".55"/>' % (H, H, T("swatch-sky"))
    da, pa = poppy(R=165, seed=41, palette="coral", petals=6, rot=0.4)
    db, pb = poppy(R=185, seed=52, palette="peach", petals=6, rot=1.2)
    dc, pc = poppy(R=84, seed=63, palette="red", petals=5, rot=0.2)
    defs += da + db + dc
    art += stem([(122, 192), (92, 352), (122, 512), (82, 672)], w=17)
    art += stem([(372, 162), (422, 332), (392, 512), (442, 672)], w=19)
    art += stem([(247, 68), (234, 172), (252, 302)], w=11)
    art += '<g transform="translate(94 140)">%s</g>' % pa
    art += '<g transform="translate(390 114)">%s</g>' % pb
    art += '<g transform="translate(244 46)">%s</g>' % pc
    art += '<g filter="url(#figsh)"><g transform="translate(144 322) scale(1.02)">%s</g></g>' % groom("L")
    art += '<g filter="url(#figsh)"><g transform="translate(324 310) scale(1.02)">%s</g></g>' % groom("R")

    body = '<g filter="url(#paint)">%s</g>' % art
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    open(os.path.join(out_dir, "portrait.html"), "w").write(page("0 0 %d %d" % (W, H), W, H, body, defs, bg=LINEN))
    print("portrait.html", W, H, "portrait", "968,640", "rgb", 82)


if __name__ == "__main__":
    main()
