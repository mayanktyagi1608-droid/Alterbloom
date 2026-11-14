"""The table setting on the home page ("Pull up a chair"), seen from above:
a paper poppy, a coral napkin with two forks, a gold-rimmed plate printed with
the Alterbloom mark, a knife and spoon, and a coupe glass.

There is no cloth in the picture. The background is transparent, so the page's
own teal ground is the tablecloth.

Run through scripts/art/render.sh table_setting. Colours come from
css/tokens.css via T(); see "Realism exceptions" in DESIGN_SYSTEM.md.
"""
import os
import sys
from illo import T, f, poppy, stem, paint_filter, page

# The plate's centre is 0,0. One light, from the top left.
X0, Y0, W, H = -400, -440, 800, 710

HI = T("real-highlight")
SH = T("real-shadow")
B_DARK, B_SHADE, B_DEEP, BRASS, B_LIGHT, B_SHINE = (
    T("real-brass-dark"), T("real-brass-shade"), T("real-brass-deep"),
    T("real-brass"), T("real-brass-light"), T("real-brass-shine"))
CREAM, CREAM_S, CREAM_D, LINEN = T("real-cream"), T("real-cream-shade"), T("real-cream-deep"), T("swatch-linen")

defs = """
<pattern id="weave" width="5" height="5" patternUnits="userSpaceOnUse"><path d="M0 1.5H5M0 4H5" stroke="{HI}" stroke-opacity=".05"/><path d="M1.5 0V5M4 0V5" stroke="{SH}" stroke-opacity=".12"/></pattern>
<filter id="cloth" x="0" y="0" width="100%" height="100%">
  <feTurbulence type="fractalNoise" baseFrequency=".7" numOctaves="2" seed="2" result="n"/>
  <feDiffuseLighting in="n" surfaceScale=".8" lighting-color="{HI}" result="l"><feDistantLight azimuth="225" elevation="66"/></feDiffuseLighting>
  <feBlend in="SourceGraphic" in2="l" mode="multiply" result="b"/><feComposite in="b" in2="SourceAlpha" operator="in"/>
</filter>
<filter id="b1" x="-40%" y="-10%" width="180%" height="120%"><feGaussianBlur stdDeviation="1.2"/></filter>
<filter id="b2"><feGaussianBlur stdDeviation="2"/></filter>
<filter id="b3" x="-60%" y="-30%" width="220%" height="160%"><feGaussianBlur stdDeviation="3.2"/></filter>
<filter id="b5" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="5"/></filter>
<filter id="blur10" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="10"/></filter>
<filter id="blur22" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="22"/></filter>
<filter id="popsh" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="7" dy="10" stdDeviation="8" flood-color="{SH}" flood-opacity=".5"/></filter>
<filter id="metal" x="-40%" y="-6%" width="180%" height="112%" color-interpolation-filters="sRGB">
  <feTurbulence type="fractalNoise" baseFrequency=".7 .014" numOctaves="2" seed="11" result="n"/>
  <feColorMatrix in="n" type="matrix" values=".30 0 0 0 .80  .30 0 0 0 .80  .30 0 0 0 .80  0 0 0 0 1" result="brush"/>
  <feBlend in="SourceGraphic" in2="brush" mode="multiply" result="base0"/>
  <feComposite in="base0" in2="SourceAlpha" operator="in" result="base"/>
  <feGaussianBlur in="SourceAlpha" stdDeviation="1.9" result="h"/>
  <feDiffuseLighting in="h" surfaceScale="4.2" diffuseConstant="1.18" lighting-color="{HI}" result="d"><feDistantLight azimuth="225" elevation="58"/></feDiffuseLighting>
  <feBlend in="base" in2="d" mode="multiply" result="lit0"/>
  <feComposite in="lit0" in2="SourceAlpha" operator="in" result="lit"/>
  <feSpecularLighting in="h" surfaceScale="4.2" specularConstant=".85" specularExponent="26" lighting-color="{B_SHINE}" result="s0"><feDistantLight azimuth="225" elevation="50"/></feSpecularLighting>
  <feComposite in="s0" in2="SourceAlpha" operator="in" result="s"/>
  <feComposite in="lit" in2="s" operator="arithmetic" k1="0" k2="1" k3="1" k4="0"/>
</filter>
<filter id="metalsh" x="-80%" y="-10%" width="260%" height="125%">
  <feDropShadow dx="2.5" dy="3.5" stdDeviation="1.6" flood-color="{SH}" flood-opacity=".55" result="a"/>
  <feDropShadow in="SourceGraphic" dx="7" dy="10" stdDeviation="6" flood-color="{SH}" flood-opacity=".32" result="b"/>
  <feMerge><feMergeNode in="b"/><feMergeNode in="a"/></feMerge>
</filter>
<linearGradient id="brass" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="382">
  <stop offset="0" stop-color="{B_LIGHT}"/><stop offset=".26" stop-color="{BRASS}"/><stop offset=".44" stop-color="{B_DEEP}"/>
  <stop offset=".62" stop-color="{BRASS}"/><stop offset=".86" stop-color="{B_LIGHT}"/><stop offset="1" stop-color="{B_DEEP}"/></linearGradient>
<linearGradient id="bladeg" gradientUnits="userSpaceOnUse" x1="-21" y1="0" x2="9" y2="0">
  <stop offset="0" stop-color="{B_SHINE}"/><stop offset=".2" stop-color="{B_LIGHT}"/><stop offset=".24" stop-color="{BRASS}"/>
  <stop offset=".7" stop-color="{BRASS}"/><stop offset="1" stop-color="{B_DEEP}"/></linearGradient>
<radialGradient id="bowlin" gradientUnits="userSpaceOnUse" cx="7" cy="64" r="52">
  <stop offset="0" stop-color="{B_SHINE}"/><stop offset=".35" stop-color="{BRASS}"/><stop offset=".75" stop-color="{B_DEEP}"/><stop offset="1" stop-color="{B_SHADE}"/></radialGradient>
<linearGradient id="goldrim" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{B_SHINE}"/><stop offset=".35" stop-color="{B_DEEP}"/><stop offset=".6" stop-color="{B_LIGHT}"/><stop offset="1" stop-color="{B_SHADE}"/></linearGradient>
<radialGradient id="plate" cx=".4" cy=".34" r=".8"><stop offset="0" stop-color="{LINEN}"/><stop offset=".7" stop-color="{CREAM}"/><stop offset="1" stop-color="{CREAM_S}"/></radialGradient>
<radialGradient id="well" cx=".42" cy=".38" r=".75"><stop offset="0" stop-color="{LINEN}"/><stop offset=".8" stop-color="{CREAM}"/><stop offset="1" stop-color="{CREAM_S}"/></radialGradient>
<linearGradient id="wall" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CREAM_D}"/><stop offset=".5" stop-color="{CREAM_S}" stop-opacity=".3"/><stop offset="1" stop-color="{HI}"/></linearGradient>
<linearGradient id="napkin" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{ACCENT}"/><stop offset="1" stop-color="{BLOOM}"/></linearGradient>
<radialGradient id="liquid" cx=".4" cy=".36" r=".75"><stop offset="0" stop-color="{PEACH}" stop-opacity=".9"/><stop offset=".75" stop-color="{CORAL}" stop-opacity=".88"/><stop offset="1" stop-color="{CORAL_D}" stop-opacity=".9"/></radialGradient>
<radialGradient id="glassfill" cx=".5" cy=".5" r=".5"><stop offset=".7" stop-color="{HI}" stop-opacity=".05"/><stop offset="1" stop-color="{HI}" stop-opacity=".30"/></radialGradient>
""".format(HI=HI, SH=SH, B_SHADE=B_SHADE, B_DEEP=B_DEEP, BRASS=BRASS, B_LIGHT=B_LIGHT, B_SHINE=B_SHINE,
           CREAM=CREAM, CREAM_S=CREAM_S, CREAM_D=CREAM_D, LINEN=LINEN,
           ACCENT=T("accent"), BLOOM=T("swatch-bloom"),
           PEACH=T("real-petal-peach"), CORAL=T("real-petal-coral"), CORAL_D=T("real-petal-coral-deep"))
defs += paint_filter("paint", 2.0, 0.08)

b = ""

# ---- a paper poppy laid along the top, its cut stem pointing right
d1, p1 = poppy(R=94, seed=14, palette="peach", petals=6, rot=0.5)
defs += d1
b += '<g filter="url(#popsh)"><g filter="url(#paint)">%s<g transform="translate(-286 -326)">%s</g></g></g>' % (
    stem([(-250, -318), (-150, -352), (-50, -388), (40, -404)], w=11), p1)

# ---- napkin, folded, under the forks
nx, ny, nw, nh = -382, -214, 152, 404
n = '<g transform="rotate(-3 %s %s)">' % (f(nx + nw / 2), f(ny + nh / 2))
n += '<rect x="%d" y="%d" width="%d" height="%d" fill="%s" opacity=".5" filter="url(#blur10)" transform="translate(8 12)"/>' % (nx, ny, nw, nh, SH)
n += '<g filter="url(#cloth)"><rect x="%d" y="%d" width="%d" height="%d" fill="url(#napkin)"/></g>' % (nx, ny, nw, nh)
n += '<rect x="%d" y="%d" width="%d" height="%d" fill="url(#weave)"/>' % (nx, ny, nw, nh)
n += '<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="%s" stroke-opacity=".6" stroke-width="1.2" stroke-dasharray="5 4"/>' % (nx + 9, ny + 9, nw - 18, nh - 18, T("real-petal-coral-edge"))
n += '<path d="M%d %dV%d" stroke="%s" stroke-opacity=".28" stroke-width="5" filter="url(#b2)"/>' % (nx + nw - 40, ny, ny + nh, T("real-petal-shadow"))
n += '<path d="M%d %dV%d" stroke="%s" stroke-opacity=".45" stroke-width="1.5"/>' % (nx + nw - 44, ny, ny + nh, T("real-petal-coral-edge"))
n += '</g>'
b += n


# ---- cutlery: one silhouette each, lit by the "metal" filter
def fork_path():
    cs = [-17.25, -5.75, 5.75, 17.25]
    d = "M%s 7" % f(cs[0] - 2.9)
    for i, c in enumerate(cs):
        d += "C%s 2.5 %s 0 %s 0C%s 0 %s 2.5 %s 7" % (f(c - 2.9), f(c - 1.5), f(c), f(c + 1.5), f(c + 2.9), f(c + 2.9))
        if i < 3:
            nxt = cs[i + 1]
            # down the tine, round the root of the slot, up to the next tip
            d += "L%s 84C%s 90 %s 90 %s 84L%s 7" % (f(c + 4.1), f(c + 4.1), f(nxt - 4.1), f(nxt - 4.1), f(nxt - 2.9))
    d += "C22.4 40 23.6 70 23.6 100C23.6 132 6 142 4.8 174C4.2 206 10 272 10 318C10 332 5.5 340 0 340"
    d += "C-5.5 340 -10 332 -10 318C-10 272 -4.2 206 -4.8 174C-6 142 -23.6 132 -23.6 100C-23.6 70 -22.4 40 %s 7Z" % f(cs[0] - 2.9)
    return d


FORK = fork_path()
KNIFE = ("M5 0C9.5 0 9.5 7 9.5 16L8.4 212C8.4 220 8.6 224 8.6 232C9 282 10.6 330 10.6 356C10.6 372 6 382 0 382"
         "C-6 382 -10.6 372 -10.6 356C-10.6 330 -9 282 -8.6 232C-8.6 225 -9 221 -10.5 216C-19 207 -21 190 -21 160"
         "L-21 84C-21 42 -10 8 5 0Z")
SPOON = ("M0 0C17 0 27 26 27 52C27 76 13.5 91 5.2 104C4.4 110 4.5 117 4.5 124C4.5 200 10 270 10 296C10 312 5.5 320 0 320"
         "C-5.5 320 -10 312 -10 296C-10 270 -4.5 200 -4.5 124C-4.5 117 -4.4 110 -5.2 104C-13.5 91 -27 76 -27 52C-27 26 -17 0 0 0Z")
BOWL = "M0 6.5C13 6.5 21.5 28 21.5 52C21.5 74 11 90 0 90C-11 90 -21.5 74 -21.5 52C-21.5 28 -13 6.5 0 6.5Z"
defs += ('<clipPath id="cFork"><path d="%s"/></clipPath><clipPath id="cKnife"><path d="%s"/></clipPath>'
         '<clipPath id="cSpoon"><path d="%s"/></clipPath><clipPath id="cBowl"><path d="%s"/></clipPath>' % (FORK, KNIFE, SPOON, BOWL))


def piece(x, y, s, rot, inner):
    return ('<g transform="translate(%s %s) rotate(%s) scale(%s)"><g filter="url(#metalsh)"><g filter="url(#metal)">%s</g></g></g>'
            % (f(x), f(y), f(rot), f(s), inner))


def handle_sheen(y0, y1, w0, w1):
    """A long soft highlight down the left of a handle and a shade down the right."""
    return (
        '<path d="M%s %sC%s %s %s %s %s %s" fill="none" stroke="%s" stroke-opacity=".55" stroke-width="2.6" stroke-linecap="round" filter="url(#b1)"/>'
        % (f(-w0 * .3), f(y0), f(-w0 * .3), f((y0 + y1) / 2), f(-w1 * .42), f(y1 - 30), f(-w1 * .42), f(y1), B_SHINE)
        + '<path d="M%s %sC%s %s %s %s %s %s" fill="none" stroke="%s" stroke-opacity=".34" stroke-width="3.4" stroke-linecap="round" filter="url(#b1)"/>'
        % (f(w0 * .55), f(y0), f(w0 * .55), f((y0 + y1) / 2), f(w1 * .62), f(y1 - 30), f(w1 * .62), f(y1), B_DARK)
    )


def fork(x, y, s=1.0, rot=0.0):
    g = '<path d="%s" fill="url(#brass)"/>' % FORK
    o = '<ellipse cx="-2" cy="103" rx="24" ry="13" fill="%s" opacity=".5" filter="url(#b3)"/>' % B_SHINE     # the head curves up here
    o += '<ellipse cx="2" cy="150" rx="13" ry="20" fill="%s" opacity=".38" filter="url(#b3)"/>' % B_DARK      # and dips at the neck
    o += '<rect x="-24" y="66" width="48" height="22" fill="%s" opacity=".16" filter="url(#b3)"/>' % B_DARK   # tine roots
    o += handle_sheen(184, 324, 4.6, 10)
    g += '<g clip-path="url(#cFork)">%s</g>' % o
    return piece(x, y, s, rot, g)


def knife(x, y, s=1.0, rot=0.0):
    g = '<path d="%s" fill="url(#brass)"/>' % KNIFE
    o = '<path d="M-22 -2H10V214H-22Z" fill="url(#bladeg)"/>'                                             # polished blade
    o += '<path d="M-14.5 206C-14.5 190 -14.6 170 -14.6 160L-14.6 86C-14.6 50 -6 18 5 4" fill="none" stroke="%s" stroke-opacity=".7" stroke-width=".9"/>' % B_SHINE   # grind line
    o += '<path d="M2 20C4 80 4 150 3 204" fill="none" stroke="%s" stroke-opacity=".3" stroke-width="5" filter="url(#b3)"/>' % B_SHINE
    o += '<path d="M-12 215.5H10" stroke="%s" stroke-opacity=".55" stroke-width="1.2"/>' % B_DARK          # bolster
    o += '<path d="M-12 218H10" stroke="%s" stroke-opacity=".5" stroke-width="1"/>' % B_SHINE
    o += handle_sheen(238, 364, 8.6, 10.6)
    g += '<g clip-path="url(#cKnife)">%s</g>' % o
    return piece(x, y, s, rot, g)


def spoon(x, y, s=1.0, rot=0.0):
    g = '<path d="%s" fill="url(#brass)"/>' % SPOON
    o = '<ellipse cx="1" cy="112" rx="12" ry="14" fill="%s" opacity=".3" filter="url(#b3)"/>' % B_DARK
    o += handle_sheen(130, 304, 4.5, 10)
    g += '<g clip-path="url(#cSpoon)">%s</g>' % o
    # the bowl is a hollow: lit on the far wall, in shade under the near rim
    bw = '<path d="%s" fill="url(#bowlin)"/>' % BOWL
    bw += '<path d="%s" fill="none" stroke="%s" stroke-opacity=".55" stroke-width="7" filter="url(#b3)" transform="translate(3 4)"/>' % (BOWL, B_DARK)
    bw += '<ellipse cx="9" cy="64" rx="3" ry="9" fill="%s" opacity=".6" filter="url(#b1)" transform="rotate(-24 9 64)"/>' % HI
    bw += '<path d="M-12 30C-15.5 42 -15.5 58 -11 70" fill="none" stroke="%s" stroke-opacity=".22" stroke-width="3" stroke-linecap="round" filter="url(#b1)"/>' % B_SHINE
    g += '<g clip-path="url(#cBowl)">%s</g>' % bw
    g += '<path d="%s" fill="none" stroke="%s" stroke-opacity=".5" stroke-width=".8"/>' % (BOWL, B_SHINE)
    return piece(x, y, s, rot, g)


FOOT = 170   # every handle ends on this line
b += fork(-334, FOOT - 340 * .92, .92, -1.2) + fork(-274, FOOT - 340 * 1.04, 1.04, .8)

# ---- plate
R, WELL = 226, 150
b += '<circle cx="14" cy="22" r="%d" fill="%s" opacity=".6" filter="url(#blur22)"/>' % (R, SH)
b += '<circle cx="4" cy="6" r="%d" fill="%s" opacity=".55" filter="url(#b5)"/>' % (R, SH)
b += '<circle r="%d" fill="url(#plate)"/>' % R
b += '<circle r="%d" fill="none" stroke="url(#goldrim)" stroke-width="3.2"/>' % (R - 7)
b += '<circle r="%s" fill="none" stroke="%s" stroke-width="1.6" stroke-opacity=".9"/>' % (f(R - 0.8), HI)
b += '<circle r="%d" fill="url(#well)"/>' % WELL
b += '<circle r="%d" fill="none" stroke="url(#wall)" stroke-width="11" filter="url(#b2)"/>' % (WELL + 2)
# glaze highlights on the rim, top left
b += '<path d="M-172 -82A190 190 0 0 1 -82 -172" fill="none" stroke="%s" stroke-width="9" stroke-linecap="round" stroke-opacity=".9" filter="url(#b5)"/>' % HI
b += '<path d="M-160 -108A193 193 0 0 1 -120 -150" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round" stroke-opacity=".9" filter="url(#b2)"/>' % HI

# ---- the mark, printed on the plate: the brand motif (path data from DESIGN_SYSTEM.md) and the wordmark
b += ('<svg x="-40" y="-116" width="80" height="100" viewBox="0 0 120 150" fill="none" stroke="%s" stroke-width="2" stroke-linecap="round">'
      '<path d="M60 140 C 58 100, 66 80, 60 55"/><path d="M60 90 C 45 84, 38 92, 34 84"/><path d="M62 100 C 76 96, 80 106, 88 100"/>'
      '<ellipse cx="60" cy="40" rx="10" ry="16" transform="rotate(-18 60 40)"/><ellipse cx="60" cy="40" rx="10" ry="16" transform="rotate(18 60 40)"/>'
      '<ellipse cx="60" cy="34" rx="10" ry="16"/><ellipse cx="60" cy="42" rx="9" ry="15" transform="rotate(-42 60 42)"/>'
      '<ellipse cx="60" cy="42" rx="9" ry="15" transform="rotate(42 60 42)"/></svg>' % T("swatch-bloom"))
b += ('<text x="0" y="24" text-anchor="middle" style="font-family:Montserrat;font-weight:600" font-size="21" fill="%s">'
      'Alterbloom<tspan fill="%s">.</tspan></text>' % (T("swatch-teal"), T("swatch-bloom")))

# ---- knife and spoon
b += knife(276, FOOT - 382, 1.0, .6) + spoon(336, FOOT - 320, 1.0, -1.4)

# ---- coupe glass seen from above, with its light on the cloth
gx, gy, gr = 310, -318, 62
b += '<circle cx="%d" cy="%d" r="%d" fill="%s" opacity=".45" filter="url(#blur10)"/>' % (gx + 12, gy + 18, gr, SH)
b += '<ellipse cx="%d" cy="%d" rx="%s" ry="%s" fill="%s" opacity=".22" filter="url(#blur10)"/>' % (gx + 26, gy + 36, f(gr * 0.6), f(gr * 0.5), T("real-petal-peach"))
b += '<circle cx="%d" cy="%d" r="%d" fill="url(#glassfill)"/>' % (gx, gy, gr)
b += '<circle cx="%d" cy="%d" r="%d" fill="url(#liquid)"/>' % (gx, gy, gr - 8)
b += '<circle cx="%d" cy="%d" r="26" fill="none" stroke="%s" stroke-opacity=".28" stroke-width="1.5"/>' % (gx, gy, HI)
b += '<circle cx="%d" cy="%d" r="%s" fill="none" stroke="%s" stroke-opacity=".85" stroke-width="2.4"/>' % (gx, gy, f(gr - 1.2), HI)
b += '<path d="M%d %dA48 48 0 0 1 %d %d" fill="none" stroke="%s" stroke-width="5" stroke-linecap="round" stroke-opacity=".8" filter="url(#b2)"/>' % (gx - 44, gy - 16, gx - 16, gy - 44, HI)
for (bx, by, br) in [(12, 9, 2.0), (20, -5, 1.5), (-5, 21, 1.6), (27, 20, 1.3), (4, -12, 1.2)]:
    b += '<circle cx="%d" cy="%d" r="%s" fill="%s" fill-opacity=".55"/>' % (gx + bx, gy + by, f(br), HI)

out_dir = sys.argv[1] if len(sys.argv) > 1 else "."
open(os.path.join(out_dir, "table-setting.html"), "w").write(page("%d %d %d %d" % (X0, Y0, W, H), W, H, b, defs))
print("table-setting.html", W, H, "table-setting", "1600,800", "rgba", 84)
