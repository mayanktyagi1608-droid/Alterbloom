"""The invitation envelope and its wax seal, as the separate layers that
css/sections.css stacks and js/invite.js animates:

  envelope-front     the pocket (side flaps, bottom flap, seams)
  envelope-flap-out  the outside of the top flap
  envelope-flap-in   the inside of the top flap: paper edge, poppy-printed liner
  wax-seal           the seal, on a transparent ground

All are drawn on the same 560 x 440 canvas the stylesheet uses. The three
paper layers are opaque rectangles: the stylesheet cuts their shapes with
clip-path, using the same points as POCKET and FLAP below, so keep the two in
step.

Run through scripts/art/render.sh envelope. Colours come from css/tokens.css
via T(); see "Realism exceptions" in DESIGN_SYSTEM.md.
"""
import math
import os
import random
import sys
from illo import T, f, pol, smooth, poppy, page

EW, EH = 560, 440
FH = 238                 # the top flap is 54% of the height

HI = T("real-highlight")
WARM = T("real-shadow-warm")
LINEN, CREAM, CREAM_S = T("swatch-linen"), T("real-cream"), T("real-cream-shade")

# The pocket's top edge: two side flaps meeting in a soft notch.
POCKET = "M0 0L%s %sQ%s %s %s %sL%d 0" % (f(EW * .46), f(EH * .44), f(EW * .5), f(EH * .49), f(EW * .54), f(EH * .44), EW)
# The top flap, closed (point down).
FLAP = "M0 0L%d 0L%s %sQ%s %s %s %sZ" % (EW, f(EW * .535), f(FH - 29), f(EW * .5), f(FH + 29), f(EW * .465), f(FH - 29))

PAPER = """
<filter id="paper" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">
  <feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="3" seed="3" result="n"/>
  <feDiffuseLighting in="n" surfaceScale=".5" lighting-color="{HI}" result="l"><feDistantLight azimuth="225" elevation="64"/></feDiffuseLighting>
  <feComponentTransfer in="l" result="l2"><feFuncR type="linear" slope="1.10"/><feFuncG type="linear" slope="1.10"/><feFuncB type="linear" slope="1.10"/></feComponentTransfer>
  <feBlend in="SourceGraphic" in2="l2" mode="multiply" result="b"/>
  <feComposite in="b" in2="SourceAlpha" operator="in"/>
</filter>
<filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="6"/></filter>
<linearGradient id="pbody" x1="0" y1="0" x2="1.5" y2="1.5"><stop offset="0" stop-color="{LINEN}"/><stop offset="1" stop-color="{CREAM_S}"/></linearGradient>
<linearGradient id="pflap" x1="0" y1="0" x2="0" y2="1.7"><stop offset="0" stop-color="{LINEN}"/><stop offset="1" stop-color="{CREAM_S}"/></linearGradient>
<linearGradient id="pbottom" x1="0" y1="1" x2="0" y2="-.6"><stop offset="0" stop-color="{CREAM}"/><stop offset="1" stop-color="{CREAM_S}"/></linearGradient>
<linearGradient id="pside" x1="0" y1="0" x2="1.3" y2="0"><stop offset="0" stop-color="{CREAM}"/><stop offset="1" stop-color="{CREAM_S}"/></linearGradient>
<linearGradient id="liner" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{TEAL_D}"/><stop offset="1" stop-color="{TEAL}"/></linearGradient>
""".format(HI=HI, LINEN=LINEN, CREAM=CREAM, CREAM_S=CREAM_S, TEAL=T("swatch-teal"), TEAL_D=T("swatch-teal-deep"))


def seam(x1, y1, x2, y2):
    return ('<path d="M%s %sL%s %s" stroke="%s" stroke-opacity=".16" stroke-width="1.2"/>' % (f(x1), f(y1), f(x2), f(y2), WARM)
            + '<path d="M%s %sL%s %s" stroke="%s" stroke-opacity=".7" stroke-width="1" transform="translate(0 1.4)"/>' % (f(x1), f(y1), f(x2), f(y2), HI))


# ---------------------------------------------------------------- the pocket
def front():
    p = '<g filter="url(#paper)">'
    p += '<rect width="%d" height="%d" fill="url(#pbody)"/>' % (EW, EH)
    p += '<path d="M0 0L%s %sL0 %dZ" fill="url(#pside)"/>' % (f(EW * .5), f(EH * .5), EH)
    p += '<path d="M%d 0L%s %sL%d %dZ" fill="url(#pside)"/>' % (EW, f(EW * .5), f(EH * .5), EW, EH)
    p += '<path d="M0 %dL%s %sQ%s %s %s %sL%d %dZ" fill="url(#pbottom)"/>' % (
        EH, f(EW * .46), f(EH * .50), f(EW * .5), f(EH * .455), f(EW * .54), f(EH * .50), EW, EH)
    p += '</g>'
    p += seam(0, EH, EW * .46, EH * .50) + seam(EW, EH, EW * .54, EH * .50)
    # the lit top edge of the pocket, and the paper's outer edge
    p += '<path d="%s" fill="none" stroke="%s" stroke-opacity=".85" stroke-width="1.6" transform="translate(0 1)"/>' % (POCKET, HI)
    p += '<rect x=".5" y=".5" width="%d" height="%d" fill="none" stroke="%s" stroke-opacity=".5"/>' % (EW - 1, EH - 1, HI)
    return page("0 0 %d %d" % (EW, EH), EW, EH, p, PAPER)


# ------------------------------------------------------- the flap, outside
def flap_out():
    p = '<g filter="url(#paper)"><rect width="%d" height="%d" fill="url(#pflap)"/></g>' % (EW, FH)
    # a soft crease of shade along the fold, and a lit edge down the left side
    p += '<rect width="%d" height="10" fill="%s" opacity=".10" filter="url(#soft)"/>' % (EW, WARM)
    p += '<path d="%s" fill="none" stroke="%s" stroke-opacity=".8" stroke-width="1.6" transform="translate(0 -1)"/>' % (FLAP, HI)
    return page("0 0 %d %d" % (EW, FH), EW, FH, p, PAPER)


# -------------------------------------------------------- the flap, inside
def flap_in():
    """Drawn as it is seen once open: point up, liner showing."""
    # the same outline, turned over, then a liner set in from the paper's edge
    inset = 15
    lin = "M%d %dL%s %sQ%s %s %s %sL%d %dZ" % (
        inset + 6, FH, f(EW * .468), f(34 + inset), f(EW * .5), f(inset - 14), f(EW * .532), f(34 + inset), EW - inset - 6, FH)
    defs = PAPER + '<clipPath id="linclip"><path d="%s"/></clipPath>' % lin
    p = '<g filter="url(#paper)"><rect width="%d" height="%d" fill="url(#pflap)"/></g>' % (EW, FH)
    p += '<path d="%s" fill="url(#liner)"/>' % lin
    minis = ""
    blooms = [(62, 212, 30, 3, "coral"), (498, 210, 30, 5, "coral"), (280, 62, 30, 4, "peach"), (226, 104, 21, 8, "coral"),
              (336, 102, 22, 9, "red"), (280, 142, 25, 6, "coral"), (158, 166, 24, 11, "peach"), (402, 164, 24, 12, "peach"),
              (232, 204, 23, 15, "red"), (334, 206, 22, 17, "coral"), (120, 222, 16, 19, "peach"), (444, 224, 16, 21, "red")]
    for (mx, my, mr, sd, pal) in blooms:
        d_, b_ = poppy(R=mr, seed=sd, palette=pal, petals=5, rot=sd)
        defs += d_
        minis += '<g transform="translate(%d %d)">%s</g>' % (mx, my, b_)
    p += '<g clip-path="url(#linclip)" opacity=".94">%s</g>' % minis
    # where the liner meets the paper: a hair of shade
    p += '<path d="%s" fill="none" stroke="%s" stroke-opacity=".35" stroke-width="1"/>' % (lin, WARM)
    return page("0 0 %d %d" % (EW, FH), EW, FH, p, defs)


# ------------------------------------------------------------ the wax seal
def seal():
    """A height map drawn in alpha (thick uneven rim, pressed disc, raised
    monogram), lit as wax. 96 units across at the disc, on a 136-unit canvas."""
    r, S = 50, 136
    rnd = random.Random(5)
    defs = """
<filter id="wax" x="-25%" y="-25%" width="150%" height="150%" color-interpolation-filters="sRGB">
  <feComponentTransfer in="SourceAlpha" result="mask"><feFuncA type="linear" slope="12"/></feComponentTransfer>
  <feGaussianBlur in="SourceAlpha" stdDeviation="2.3" result="h"/>
  <feDiffuseLighting in="h" surfaceScale="6.5" diffuseConstant="1.3" lighting-color="{LIT}" result="dif"><feDistantLight azimuth="225" elevation="50"/></feDiffuseLighting>
  <feSpecularLighting in="h" surfaceScale="6.5" specularConstant=".6" specularExponent="22" lighting-color="{GLINT}" result="spec"><feDistantLight azimuth="225" elevation="55"/></feSpecularLighting>
  <feFlood flood-color="{BASE}" result="basec"/><feComposite in="basec" in2="mask" operator="in" result="basem"/>
  <feComposite in="dif" in2="mask" operator="in" result="difr"/>
  <feComposite in="difr" in2="basem" operator="arithmetic" k1="0" k2=".78" k3=".24" k4="0" result="difm"/>
  <feComposite in="spec" in2="mask" operator="in" result="specm"/>
  <feComposite in="difm" in2="specm" operator="arithmetic" k1="0" k2="1" k3="1" k4="0" result="lit"/>
  <feGaussianBlur in="mask" stdDeviation="3.2" result="shb"/>
  <feOffset in="shb" dx="2.5" dy="4.5" result="sho"/>
  <feFlood flood-color="{SHADE}" flood-opacity=".5"/><feComposite in2="sho" operator="in" result="sh"/>
  <feMerge><feMergeNode in="sh"/><feMergeNode in="lit"/></feMerge>
</filter>""".format(LIT=T("accent"), GLINT=T("real-petal-peach-edge"), BASE=T("swatch-bloom"), SHADE=WARM)
    pts = []
    n = 26
    ph = [rnd.uniform(0, 6.28) for _ in range(3)]
    for i in range(n):
        a = i * 2 * math.pi / n
        rr = r * (1 + 0.05 * math.sin(a * 3 + ph[0]) + 0.035 * math.sin(a * 5 + ph[1]) + 0.02 * math.sin(a * 9 + ph[2]))
        if 1.9 < a < 2.5:      # one soft drip of wax, bottom left
            rr *= 1.10
        pts.append(pol(rr, a))
    blob = smooth(pts)
    ri = r * 0.66
    inner = "M%s 0A%s %s 0 1 0 %s 0A%s %s 0 1 0 %s 0Z" % (f(ri), f(ri), f(ri), f(-ri), f(ri), f(ri), f(ri))
    ink = T("real-shadow")   # only its alpha matters: the filter reads this as height
    g = '<g transform="translate(%s %s)" filter="url(#wax)">' % (f(S / 2), f(S / 2))
    g += '<path d="%s %s" fill-rule="evenodd" fill="%s"/>' % (blob, inner, ink)                    # raised rim
    g += '<circle r="%s" fill="%s" fill-opacity=".5"/>' % (f(ri + 1), ink)                          # pressed disc
    g += '<circle r="%s" fill="none" stroke="%s" stroke-opacity=".55" stroke-width="2"/>' % (f(ri * 0.84), ink)   # stamp ring
    g += '<text x="0" y="%s" text-anchor="middle" style="font-family:Montserrat;font-weight:600" font-size="%s" fill="%s">A.</text>' % (f(r * 0.24), f(r * 0.72), ink)
    g += '</g>'
    return page("0 0 %d %d" % (S, S), 204, 204, g, defs)


out_dir = sys.argv[1] if len(sys.argv) > 1 else "."
# Paper grain survives heavy compression, and these load with the first screen, so they are kept small.
for name, html, w, h, widths, mode, quality in [
        ("envelope-front", front(), EW, EH, "840", "rgb", 52),
        ("envelope-flap-out", flap_out(), EW, FH, "840", "rgb", 52),
        ("envelope-flap-in", flap_in(), EW, FH, "840", "rgb", 62),
        ("wax-seal", seal(), 204, 204, "408", "rgba", 84)]:
    open(os.path.join(out_dir, name + ".html"), "w").write(html)
    print(name + ".html", w, h, name, widths, mode, quality)
