"""Shared drawing helpers for the Alterbloom artwork (the "Realism exceptions"
pieces in DESIGN_SYSTEM.md). Everything here builds SVG as strings.

Colours are never written in this folder. T("real-brass") looks the value up
in css/tokens.css, so the artwork can only use what the design system lists.
"""
import math
import os
import random
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FONTS = os.path.join(ROOT, "css", "fonts")


def _load_tokens():
    css = open(os.path.join(ROOT, "css", "tokens.css")).read()
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    block = css[css.index(":root{"):]
    block = block[:block.index("\n}")]
    return dict((k, v.strip()) for k, v in re.findall(r"--([a-z0-9-]+)\s*:\s*([^;]+);", block))


_TOKENS = _load_tokens()


def T(name):
    """The value of a design token, e.g. T("real-brass") or T("swatch-teal")."""
    v = _TOKENS[name]
    m = re.match(r"var\(--([a-z0-9-]+)\)$", v)
    return T(m.group(1)) if m else v


def petal_palette(name):
    return dict(
        deep=T("real-petal-%s-deep" % name), mid=T("real-petal-%s" % name),
        light=T("real-petal-%s-light" % name), edge=T("real-petal-%s-edge" % name),
        shadow=T("real-petal-shadow"))


def f(x):
    return ("%.1f" % x).rstrip("0").rstrip(".")


def smooth(pts, closed=True):
    """Catmull-Rom spline through pts, as an SVG path of cubic Beziers."""
    n = len(pts)
    if n < 3:
        return ""
    d = "M%s %s" % (f(pts[0][0]), f(pts[0][1]))
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[i]
        p1 = pts[i % n]
        p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6.0, p1[1] + (p2[1] - p0[1]) / 6.0)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6.0, p2[1] - (p3[1] - p1[1]) / 6.0)
        d += "C%s %s %s %s %s %s" % (f(c1[0]), f(c1[1]), f(c2[0]), f(c2[1]), f(p2[0]), f(p2[1]))
    return d + ("Z" if closed else "")


def pol(r, a):
    return (r * math.cos(a), r * math.sin(a))


class Ids:
    n = 0

    @classmethod
    def new(cls, p="i"):
        cls.n += 1
        return "%s%d" % (p, cls.n)


def petal_points(rnd, ac, span, length, ruffle=0.07, n=22):
    """A fan-shaped crepe petal: narrow at the centre, broad ruffled rim."""
    ph = [rnd.uniform(0, 6.28) for _ in range(3)]
    pts = [pol(length * 0.02, ac + math.pi)]
    pts.append(pol(length * 0.30, ac - span * 0.36))
    pts.append(pol(length * 0.66, ac - span * 0.50))
    for i in range(n + 1):
        t = i / float(n)
        a = ac - span / 2 + span * t
        taper = 0.86 + 0.14 * math.sin(math.pi * t) ** 0.6
        wob = (math.sin(t * 9 + ph[0]) * 0.5 + math.sin(t * 17 + ph[1]) * 0.3 + math.sin(t * 29 + ph[2]) * 0.2)
        r = length * taper * (1 + ruffle * wob + rnd.uniform(-0.012, 0.012))
        pts.append(pol(r, a))
    pts.append(pol(length * 0.66, ac + span * 0.50))
    pts.append(pol(length * 0.30, ac + span * 0.36))
    return pts


def poppy(R=200, seed=1, palette="coral", petals=6, with_centre=True, rot=0.0):
    """Front-facing giant paper poppy centred on 0,0. Returns (defs, body)."""
    rnd = random.Random(seed)
    P = petal_palette(palette)
    gid = Ids.new("g")
    sid = Ids.new("s")
    defs = (
        '<radialGradient id="%s" gradientUnits="userSpaceOnUse" cx="0" cy="0" r="%s">'
        '<stop offset="0" stop-color="%s"/><stop offset=".3" stop-color="%s"/>'
        '<stop offset=".72" stop-color="%s"/><stop offset="1" stop-color="%s"/></radialGradient>'
        % (gid, f(R), P["deep"], P["mid"], P["light"], P["edge"])
    )
    defs += (
        '<filter id="%s" x="-30%%" y="-30%%" width="160%%" height="160%%">'
        '<feDropShadow dx="0" dy="%s" stdDeviation="%s" flood-color="%s" flood-opacity=".30"/></filter>'
        % (sid, f(R * 0.02), f(R * 0.035), P["shadow"])
    )
    body = '<circle r="%s" fill="%s"/>' % (f(R * 0.5), P["mid"])   # no gaps between petal bases
    # two rings: back petals (bigger), then front petals offset between them
    back = petals // 2 + petals % 2
    front = petals - back
    layers = []
    for i in range(back):
        ac = rot + i * 2 * math.pi / back + rnd.uniform(-0.12, 0.12)
        layers.append((ac, rnd.uniform(1.75, 2.05), R * rnd.uniform(0.94, 1.0)))
    for i in range(front):
        ac = rot + (i + 0.5) * 2 * math.pi / max(front, 1) + rnd.uniform(-0.15, 0.15)
        layers.append((ac, rnd.uniform(1.55, 1.85), R * rnd.uniform(0.74, 0.84)))
    for (ac, span, L) in layers:
        pts = petal_points(rnd, ac, span, L)
        d = smooth(pts)
        cid = Ids.new("c")
        defs += '<clipPath id="%s"><path d="%s"/></clipPath>' % (cid, d)
        body += '<g filter="url(#%s)"><path d="%s" fill="url(#%s)"/></g>' % (sid, d, gid)
        # crepe striations, clipped to the petal
        lines = ""
        k = int(46 * span / 1.8)
        for j in range(k):
            a = ac - span / 2 + span * (j + rnd.uniform(0.1, 0.9)) / k
            r0 = L * rnd.uniform(0.10, 0.32)
            r1 = L * rnd.uniform(0.78, 1.08)
            bend = (a - ac) * 0.10
            p0 = pol(r0, a - bend)
            p1 = pol((r0 + r1) / 2, a)
            p2 = pol(r1, a + bend)
            light = rnd.random() < 0.5
            lines += '<path d="M%s %sQ%s %s %s %s" stroke="%s" stroke-opacity="%s" stroke-width="%s"/>' % (
                f(p0[0]), f(p0[1]), f(p1[0]), f(p1[1]), f(p2[0]), f(p2[1]),
                P["edge"] if light else P["deep"],
                f(rnd.uniform(0.3, 0.6)) if light else f(rnd.uniform(0.14, 0.34)),
                f(R * rnd.uniform(0.004, 0.011)))
        # a soft fold of shadow down one side of the petal
        fa = ac + span * rnd.choice([-0.28, 0.28])
        q0 = pol(L * 0.12, fa)
        q1 = pol(L * 0.45, fa + 0.10)
        q2 = pol(L * 0.74, fa - 0.04)
        lines += '<path d="M%s %sQ%s %s %s %s" stroke="%s" stroke-opacity=".09" stroke-width="%s"/>' % (
            f(q0[0]), f(q0[1]), f(q1[0]), f(q1[1]), f(q2[0]), f(q2[1]), P["shadow"], f(R * 0.07))
        body += '<g clip-path="url(#%s)" fill="none" stroke-linecap="round">%s</g>' % (cid, lines)
        body += '<path d="%s" fill="none" stroke="%s" stroke-opacity=".55" stroke-width="%s"/>' % (d, P["edge"], f(R * 0.008))
    if with_centre:
        body += centre(R, rnd, P)
    return defs, body


def centre(R, rnd, P):
    stamen, stamen_d, stamen_l = T("real-stamen"), T("real-stamen-shade"), T("real-stamen-light")
    out = '<circle r="%s" fill="%s" opacity=".35"/>' % (f(R * 0.30), P["deep"])
    st = ""
    tips = ""
    for _ in range(95):
        a = rnd.uniform(0, 2 * math.pi)
        r1 = R * rnd.uniform(0.15, 0.31)
        p0 = pol(R * 0.05, a)
        p1 = pol(r1, a + rnd.uniform(-0.08, 0.08))
        col = rnd.choice([stamen, stamen, stamen_d, stamen_l])
        st += '<path d="M%s %sL%s %s" stroke="%s" stroke-width="%s"/>' % (f(p0[0]), f(p0[1]), f(p1[0]), f(p1[1]), col, f(R * rnd.uniform(0.008, 0.014)))
        tips += '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(p1[0]), f(p1[1]), f(R * rnd.uniform(0.012, 0.02)), rnd.choice([stamen_l, stamen, stamen_l]))
    out += '<g stroke-linecap="round">%s</g>%s' % (st, tips)
    pod = Ids.new("p")
    out += ('<radialGradient id="%s" cx=".4" cy=".35" r=".8"><stop offset="0" stop-color="%s"/>'
            '<stop offset=".7" stop-color="%s"/><stop offset="1" stop-color="%s"/></radialGradient>'
            % (pod, T("real-brass-shine"), T("real-pod"), T("real-brass-deep")))
    out += '<circle r="%s" fill="url(#%s)"/>' % (f(R * 0.095), pod)
    rays = ""
    for i in range(9):
        a = i * 2 * math.pi / 9 + 0.2
        p = pol(R * 0.08, a)
        rays += '<path d="M0 0L%s %s"/>' % (f(p[0]), f(p[1]))
    out += '<g stroke="%s" stroke-width="%s" stroke-linecap="round" opacity=".8">%s</g>' % (T("real-brass-deep"), f(R * 0.01), rays)
    return out


def stem(pts, w=14):
    """A paper-wrapped stem through pts (list of (x, y))."""
    d = smooth(pts, closed=False)
    return (
        '<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round"/>' % (d, T("real-stem-shade"), f(w))
        + '<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round"/>' % (d, T("real-stem"), f(w * 0.82))
        + '<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" stroke-opacity=".7" transform="translate(%s %s)"/>' % (d, T("real-stem-light"), f(w * 0.22), f(-w * 0.14), f(-w * 0.14))
    )


def paint_filter(fid="paint", scale=3.0, grain=0.10):
    """Hand-cut wobble on the edges plus a little paper tooth."""
    return (
        '<filter id="%s" x="-5%%" y="-5%%" width="110%%" height="110%%" color-interpolation-filters="sRGB">'
        '<feTurbulence type="fractalNoise" baseFrequency=".018" numOctaves="2" seed="4" result="w"/>'
        '<feDisplacementMap in="SourceGraphic" in2="w" scale="%s" xChannelSelector="R" yChannelSelector="G" result="d"/>'
        '<feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="9" result="n"/>'
        '<feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 %s 0" result="g"/>'
        '<feComposite in="g" in2="d" operator="in" result="gi"/>'
        '<feMerge><feMergeNode in="d"/><feMergeNode in="gi"/></feMerge>'
        '</filter>' % (fid, f(scale), f(grain * 2))
    )


def page(viewbox, w, h, svg_inner, defs="", bg="transparent"):
    """A standalone HTML page holding one SVG, with the site's own fonts."""
    return """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Fraunces;src:url(file://%(F)s/fraunces.woff2) format("woff2");font-weight:100 900;font-style:normal}
@font-face{font-family:Fraunces;src:url(file://%(F)s/fraunces-italic.woff2) format("woff2");font-weight:100 900;font-style:italic}
@font-face{font-family:"Work Sans";src:url(file://%(F)s/work-sans.woff2) format("woff2");font-weight:100 900}
@font-face{font-family:Montserrat;src:url(file://%(F)s/montserrat-600.woff2) format("woff2");font-weight:600}
@font-face{font-family:Caveat;src:url(file://%(F)s/caveat-600.woff2) format("woff2");font-weight:600}
html,body{margin:0;background:%(bg)s}
svg{display:block}
</style></head><body>
<svg xmlns="http://www.w3.org/2000/svg" width="%(w)d" height="%(h)d" viewBox="%(vb)s"><defs>%(defs)s</defs>%(inner)s</svg>
</body></html>""" % dict(F=FONTS, bg=bg, w=w, h=h, vb=viewbox, defs=defs, inner=svg_inner)
