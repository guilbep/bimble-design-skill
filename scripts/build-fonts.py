#!/usr/bin/env python3
"""Build the Bimble fonts and the logo letters from one geometry.

Every letter is drawn here from a few parts: stems, discs, counters, arches,
slots, bars, diagonals, and cuts at 45°. No outline comes from another typeface.

  skills/bimble-design/fonts/bimble-wordmark.ttf, .woff2   b i m l e only (B I M L E map to them): the name, small and fast
  skills/bimble-design/fonts/bimble-regular.ttf, .woff2    the Bimble typeface: printable ASCII
  skills/bimble-design/assets/logo/*.svg                   the letters in each logo

Needs: pip install fonttools skia-pathops brotli
Usage: python3 scripts/build-fonts.py [--check]   (--check: build in memory and test, write nothing)
"""
import argparse, io, math, pathlib, re

import pathops
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables._k_e_r_n import KernTable_format_0

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills/bimble-design"
VERSION = "0.2.0"

# ── geometry, in font units (1000 per em, y up, baseline 0) ─────────────────
UPM = 1000
X = 520          # x-height: the bowls and the short letters
A = 740          # ascender: b, d, f, h, k, l
DSC = -260       # descender: g, j, p, q, y
S = 180          # stem width
R = X / 2        # bowl radius: every bowl is a full disc
RC = 85          # counter radius of the bowls (b, d, o, p, q, a)
C = 90           # width of the two m counters
CN = 110         # width of the n, h and u counter
# The e's counter is a rounded slot on the LEFT part of its disc, so the e
# mirrors the b: the b has its mass left and its hole right, the e its hole
# left and its mass right. c uses the same slot.
E_CX = 225       # x of the slot's axis (the disc's centre is at R = 260)
E_W = 68         # half width of the slot
E_TOP, E_BOT = 330, 190  # y of the centres of the slot's round ends
BAR = 62         # e crossbar thickness: it runs from the slot to the right edge
H = 140          # thickness of horizontal bars: f, t, z
WD = 200         # horizontal width of diagonal strokes: k, v, w, x, y, z
HOOK = 230       # outer radius of the g and j hooks (and the f's top)
DOT_GAP = 50     # space between the i (or j) stem and its dot
# Spacing: every letter gets the same side bearing. Kerning (below) then
# corrects each pair so the white between any two letters looks the same.
SB = 60
KERN_DEPTH = 80  # how far into a round or open side the kerning measure looks
MIN_GAP = 50     # kerning never brings two letters closer than this, at any height
K = 0.5522847498 # cubic Bezier constant for a quarter circle

WORDMARK = "bimle"


# ── parts ───────────────────────────────────────────────────────────────────
def disc(cx, cy, r):
    p = pathops.Path()
    k = K * r
    p.moveTo(cx + r, cy)
    p.cubicTo(cx + r, cy + k, cx + k, cy + r, cx, cy + r)
    p.cubicTo(cx - k, cy + r, cx - r, cy + k, cx - r, cy)
    p.cubicTo(cx - r, cy - k, cx - k, cy - r, cx, cy - r)
    p.cubicTo(cx + k, cy - r, cx + r, cy - k, cx + r, cy)
    p.close()
    return p


def polygon(*pts):
    p = pathops.Path()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    p.close()
    return p


def rect(x0, y0, x1, y1):
    return polygon((x0, y0), (x1, y0), (x1, y1), (x0, y1))


def union(*ps):
    out = ps[0]
    for p in ps[1:]:
        out = pathops.op(out, p, pathops.PathOp.UNION)
    return out


def minus(a, *bs):
    for b in bs:
        a = pathops.op(a, b, pathops.PathOp.DIFFERENCE)
    return a


def inter(a, b):
    return pathops.op(a, b, pathops.PathOp.INTERSECTION)


def transform(path, sx=1, sy=1, tx=0, ty=0, simplify=True):
    """Scale, then move. A mirror (sx * sy < 0) is fixed by simplify()."""
    out = pathops.Path()
    for verb, pts in path:
        pts = [c for x, y in pts for c in (sx * x + tx, sy * y + ty)]
        {pathops.PathVerb.MOVE: out.moveTo, pathops.PathVerb.LINE: out.lineTo,
         pathops.PathVerb.CUBIC: out.cubicTo, pathops.PathVerb.QUAD: out.quadTo,
         pathops.PathVerb.CLOSE: out.close}[verb](*pts)
    if simplify:
        out.simplify()
    return out


def ring(cx, cy, ro, ri):
    return minus(disc(cx, cy, ro), disc(cx, cy, ri))


def arch(x0, w, top=X, wall=S):
    """A round-topped arch of outer width w: half of an m, all of an n."""
    r = w / 2
    outer = union(rect(x0, 0, x0 + w, top - r), disc(x0 + r, top - r, r))
    inner = union(rect(x0 + wall, -1, x0 + w - wall, top - r), disc(x0 + r, top - r, r - wall))
    return minus(outer, inner)


def bowl():
    """The disc with its centred counter: o, and the bowl of b d p q a."""
    return minus(disc(R, R, R), disc(R, R, RC))


def slot():
    """The e and c counter: a rounded slot on the left part of the disc."""
    return union(rect(E_CX - E_W, E_BOT, E_CX + E_W, E_TOP), disc(E_CX, E_TOP, E_W), disc(E_CX, E_BOT, E_W))


def hook(x_right, top):
    """The bottom of g and j: a half ring under the stem whose right wall is the
    stem, turning left and ending flat."""
    cx, cy = x_right - HOOK, top
    return inter(ring(cx, cy, HOOK, HOOK - S), rect(cx - HOOK - 1, cy - HOOK - 1, cx + HOOK + 1, cy))


def ellipse(cx, cy, ax, ay):
    return transform(disc(0, 0, 1), ax, ay, cx, cy)


# ── the letters ─────────────────────────────────────────────────────────────
def lowercase():
    """Return {glyph name: path}. Paths may start anywhere; glyphs() normalises."""
    g = {}
    wn = 2 * S + CN                        # n, h, u width
    # b: a flat-topped stem that runs into a full disc; round foot, centred counter.
    g["b"] = minus(union(rect(0, R, S, A), disc(R, R, R)), disc(R, R, RC))
    g["d"] = transform(g["b"], -1, 1, 2 * R)            # the b, mirrored
    g["p"] = minus(union(rect(0, DSC, S, R), disc(R, R, R)), disc(R, R, RC))
    g["q"] = transform(g["p"], -1, 1, 2 * R)            # the p, mirrored
    g["o"] = bowl()
    # a: the bowl with a straight stem on its right, square at the top and the foot.
    g["a"] = minus(union(disc(R, R, R), rect(2 * R - S, 0, 2 * R, X)), disc(R, R, RC))
    # e: slot on the left; the bar starts at the slot's left wall, so the eye is a
    # closed loop, and runs to the right edge; under it the opening is cut at 45°.
    d = E_W * 0.7071
    e = minus(disc(R, R, R), slot())
    e = union(e, rect(E_CX - E_W - 1, R - BAR / 2, E_CX + E_W + 1, R + BAR / 2))
    yb = R - BAR / 2
    qx, qy = E_CX + d, E_BOT - d
    x_top, x_far = qx + qy - yb, 2 * R + 80
    g["e"] = minus(e, polygon((x_top, yb), (x_far, yb), (x_far, qy - (x_far - qx))))
    # c: the e without its bar: open between two 45° cuts from the slot.
    c = minus(disc(R, R, R), slot())
    lo, hi = (E_CX + d, E_BOT - d), (E_CX + d, E_TOP + d)
    g["c"] = minus(c, polygon(hi, (hi[0] + 600, hi[1] + 600), (lo[0] + 600, lo[1] - 600), lo))
    # i, j, l: stems; the dot is the brand's disc.
    dot = disc(S / 2, X + DOT_GAP + S / 2, S / 2)
    g["i"] = union(rect(0, 0, S, X), dot)
    g["l"] = rect(0, 0, S, A)
    g["j"] = union(rect(0, DSC + HOOK, S, X), hook(S, DSC + HOOK), dot)
    # m, n, h, u, r: arches.
    w = 2 * S + C
    g["m"] = union(arch(0, w), arch(w - S, w))
    g["n"] = arch(0, wn)
    g["h"] = union(rect(0, 0, S, A), arch(0, wn))
    g["u"] = transform(arch(0, wn), 1, -1, 0, X)       # the n, upside down
    g["r"] = minus(arch(0, wn), rect(wn - S - 1, -1, wn + 1, X - wn / 2))
    # f: the j's hook turned over, on a stem, and a bar at the x-height.
    top_hook = transform(hook(S, 0), -1, -1, S, A - HOOK)
    g["f"] = union(rect(0, 0, S, A - HOOK + 1), top_hook, rect(-60, X - H, S + 120, X))
    # t: a stem a little over the x-height, with a bar.
    g["t"] = union(rect(70, 0, 70 + S, X + 150), rect(0, X - H, 70 + S + 70, X))
    # g: the q's bowl, its stem ending in the hook.
    g["g"] = minus(union(disc(R, R, R), rect(2 * R - S, DSC + HOOK, 2 * R, X), hook(2 * R, DSC + HOOK)), disc(R, R, RC))
    # s: two oval rings stacked. The top one is open at its lower right, the
    # bottom one at its upper left; where they overlap is the spine.
    sh, sv = 120, 175                      # horizontal and vertical stroke
    ay = (X + sh) / 4                      # outer half height: the spine is sh thick
    ax = 250
    tc, bc = (ax, X - ay), (ax, ay)
    oval = lambda c: minus(ellipse(*c, ax, ay), ellipse(*c, ax - sv, ay - sh))
    top = minus(oval(tc), rect(tc[0], tc[1] - ay - 1, tc[0] + ax + 1, tc[1]))
    bot = minus(oval(bc), rect(bc[0] - ax - 1, bc[1], bc[0], bc[1] + ay + 1))
    g["s"] = union(top, bot)
    # Diagonals: parallelograms of horizontal width WD, clipped flat at 0 and X.
    def leg(x_top, y_top, x_bot, y_bot):
        return polygon((x_top, y_top), (x_top + WD, y_top), (x_bot + WD, y_bot), (x_bot, y_bot))
    vw = 500
    v = union(leg(0, X, vw / 2 - WD / 2, 0), leg(vw - WD, X, vw / 2 - WD / 2, 0))
    g["v"] = v
    g["w"] = union(v, transform(v, 1, 1, vw - WD))
    g["x"] = inter(union(leg(0, X, vw - WD, 0), leg(vw - WD, X, 0, 0)), rect(-1, 0, vw + 1, X))
    # y: the v whose right stroke runs on into the descender.
    slope = (vw / 2 - WD / 2) / X                 # x per unit of height on the v's strokes
    right = leg(vw - WD, X, vw - WD - slope * (X - DSC), DSC)
    left = leg(0, X, vw / 2 - WD / 2, 0)
    g["y"] = inter(union(left, right), rect(-400, DSC, vw + 1, X))
    # k: stem, and an arm and a leg from the stem.
    kw = S + 330
    arm = polygon((S - 30, 130), (S - 30 + WD, 130), (kw, X), (kw - WD, X))
    legk = polygon((S + 30, 300), (S + 30 + WD, 300), (kw, 0), (kw - WD, 0))
    g["k"] = union(rect(0, 0, S, A), inter(union(arm, legk), rect(S - 1, 0, kw + 1, X)))
    # z: two bars and a diagonal.
    zw = 440
    g["z"] = union(rect(0, X - H, zw, X), rect(0, 0, zw, H), polygon((zw - WD, X - H), (zw, X - H), (WD, H), (0, H)))
    return g


def thick(p0, p1, t):
    """A straight stroke of thickness t from p0 to p1, with square ends."""
    (x0, y0), (x1, y1) = p0, p1
    d = math.hypot(x1 - x0, y1 - y0)
    nx, ny = -(y1 - y0) / d * t / 2, (x1 - x0) / d * t / 2
    return polygon((x0 + nx, y0 + ny), (x1 + nx, y1 + ny), (x1 - nx, y1 - ny), (x0 - nx, y0 - ny))


def leg(x_top, y_top, x_bot, y_bot, w=WD):
    """A diagonal of horizontal width w, flat at both ends."""
    return polygon((x_top, y_top), (x_top + w, y_top), (x_bot + w, y_bot), (x_bot, y_bot))


def open_wedge(cx, cy, a0, a1, far=2000):
    """The pie slice from angle a0 to a1 (degrees, counter-clockwise) around (cx, cy)."""
    pts = [(cx, cy)]
    steps = max(2, int((a1 - a0) / 15) + 1)
    for k in range(steps + 1):
        a = math.radians(a0 + (a1 - a0) * k / steps)
        pts.append((cx + far * math.cos(a), cy + far * math.sin(a)))
    return polygon(*pts)


# ── capitals: cap height = ascender, the same stems, discs and 45° cuts ──────
CH = A           # cap height
RO = CH / 2      # radius of the round capitals
TC = 190         # ring thickness of round capitals and bowls
WDC = 220        # horizontal width of the capitals' diagonals


def right_half(cx, cy, r):
    """The right half of a disc: the round side of D, P, R and B."""
    return inter(disc(cx, cy, r), rect(cx, cy - r - 1, cx + r + 1, cy + r + 1))


def uppercase():
    g = {}
    o = ring(RO, RO, RO, RO - TC)
    g["O"] = o
    g["Q"] = union(o, thick((RO + 120, RO - 150), (2 * RO + 40, -60), 170))
    # C and G: the O opened on the right; C at ±45°, G only above.
    g["C"] = minus(o, open_wedge(RO, RO, -45, 45))
    g["G"] = union(minus(o, open_wedge(RO, RO, 0, 45)), rect(RO + 30, RO - 130, 2 * RO, RO))
    # D: stem and a half disc.
    dcx = 250
    g["D"] = minus(union(rect(0, 0, dcx, CH), right_half(dcx, RO, RO)),
                   union(rect(S, TC, dcx, CH - TC), right_half(dcx, RO, RO - TC)))
    # P, R, B: stem and bowls made of a bar and a half disc.
    def bowl_cap(y0, h, cx, t=125):
        r = h / 2
        outer = union(rect(0, y0, cx, y0 + h), right_half(cx, y0 + r, r))
        inner = union(rect(S, y0 + t, cx, y0 + h - t), right_half(cx, y0 + r, r - t))
        return minus(outer, inner)
    stem = rect(0, 0, S, CH)
    hp = 490
    g["P"] = union(stem, bowl_cap(CH - hp, hp, 200))
    g["R"] = union(stem, bowl_cap(CH - hp, hp, 200),
                   inter(leg(260, CH - hp + 60, 470, 0, WDC), rect(S, 0, 1000, CH - hp + 60)))
    g["B"] = union(stem, bowl_cap(CH - 390, 390, 190, 120), bowl_cap(0, 410, 220, 120))
    # Bars and stems.
    g["E"] = union(stem, rect(0, CH - H, 480, CH), rect(0, RO - H / 2, 420, RO + H / 2), rect(0, 0, 480, H))
    g["F"] = union(stem, rect(0, CH - H, 480, CH), rect(0, RO - H / 2, 420, RO + H / 2))
    g["L"] = union(stem, rect(0, 0, 460, H))
    g["I"] = stem
    hw = 620
    g["H"] = union(stem, rect(hw - S, 0, hw, CH), rect(0, RO - H / 2, hw, RO + H / 2))
    g["T"] = union(rect(0, CH - H, 580, CH), rect(290 - S / 2, 0, 290 + S / 2, CH))
    # J and U: the lowercase hook and the n's arch, at capital size.
    jr = 240
    g["J"] = union(rect(2 * jr - S, jr, 2 * jr, CH), inter(ring(jr, jr, jr, jr - S), rect(-1, -1, 2 * jr + 1, jr)))
    uw = 640
    g["U"] = union(rect(0, uw / 2, S, CH), rect(uw - S, uw / 2, uw, CH),
                   inter(ring(uw / 2, uw / 2, uw / 2, uw / 2 - S), rect(-1, -1, uw + 1, uw / 2)))
    # Diagonals.
    vw = 720
    v = union(leg(0, CH, vw / 2 - WDC / 2, 0, WDC), leg(vw - WDC, CH, vw / 2 - WDC / 2, 0, WDC))
    g["V"] = v
    ww = 600
    vn = union(leg(0, CH, ww / 2 - WDC / 2, 0, WDC), leg(ww - WDC, CH, ww / 2 - WDC / 2, 0, WDC))
    g["W"] = union(vn, transform(vn, 1, 1, ww - WDC))
    aw = 720
    g["A"] = union(minus(polygon((0, 0), (aw / 2 - WDC / 2, CH), (aw / 2 + WDC / 2, CH), (aw, 0)),
                         polygon((WDC, 0), (aw / 2, CH - 330), (aw - WDC, 0))),
                   inter(rect(0, 170, aw, 300), polygon((0, 0), (aw / 2 - WDC / 2, CH), (aw / 2 + WDC / 2, CH), (aw, 0))))
    xw = 680
    g["X"] = inter(union(leg(0, CH, xw - WDC, 0, WDC), leg(xw - WDC, CH, 0, 0, WDC)), rect(-1, 0, xw + 1, CH))
    yw, ym = 700, 330
    g["Y"] = union(inter(union(leg(0, CH, yw / 2 - WDC / 2, ym, WDC), leg(yw - WDC, CH, yw / 2 - WDC / 2, ym, WDC)), rect(-1, ym, yw + 1, CH)),
                   rect(yw / 2 - S / 2, 0, yw / 2 + S / 2, ym + 1))
    zw = 580
    g["Z"] = union(rect(0, CH - H, zw, CH), rect(0, 0, zw, H), leg(zw - WDC, CH - H, 0, H, WDC))
    nw = 660
    g["N"] = union(stem, rect(nw - S, 0, nw, CH), inter(leg(0, CH, nw - WDC, 0, WDC), rect(0, 0, nw, CH)))
    mw = 800
    g["M"] = union(stem, rect(mw - S, 0, mw, CH),
                   inter(union(leg(0, CH, mw / 2 - WDC / 2, 120, WDC), leg(mw - WDC, CH, mw / 2 - WDC / 2, 120, WDC)), rect(0, 120, mw, CH)))
    kw = 640
    arm = polygon((S - 30, 240), (S - 30 + WDC, 240), (kw, CH), (kw - WDC, CH))
    legk = polygon((S + 40, 440), (S + 40 + WDC, 440), (kw, 0), (kw - WDC, 0))
    g["K"] = union(stem, inter(union(arm, legk), rect(S - 1, 0, kw + 1, CH)))
    # S: the lowercase s's two oval rings at capital size.
    sh, sv = 140, 190
    ay, ax = (CH + sh) / 4, 300
    tc, bc = (ax, CH - ay), (ax, ay)
    oval = lambda c: minus(ellipse(*c, ax, ay), ellipse(*c, ax - sv, ay - sh))
    g["S"] = union(minus(oval(tc), rect(tc[0], tc[1] - ay - 1, tc[0] + ax + 1, tc[1])),
                   minus(oval(bc), rect(bc[0] - ax - 1, bc[1], bc[0], bc[1] + ay + 1)))
    return g


def digits():
    g = {}
    t = 150
    g["zero"] = minus(ellipse(280, RO, 280, RO), ellipse(280, RO, 280 - t - 10, RO - t))
    g["one"] = union(rect(150, 0, 150 + S, CH), polygon((150, CH), (150, CH - 200), (0, CH - 350), (0, CH - 150)))
    # two: a top ring kept from -45° to 135° (both ends cut at 45°), a 45° diagonal, a bottom bar.
    r2 = 260
    c2 = (r2, CH - r2)
    top = inter(ring(*c2, r2, r2 - t), open_wedge(*c2, -45, 135))
    q = math.sqrt(0.5)
    p_out, p_in = (c2[0] + r2 * q, c2[1] - r2 * q), (c2[0] + (r2 - t) * q, c2[1] - (r2 - t) * q)
    drop = lambda p: (p[0] - (p[1] - H), H)
    diag = polygon(p_out, drop(p_out), drop(p_in), p_in)
    g["two"] = inter(union(top, diag, rect(0, 0, 2 * r2, H)), rect(0, 0, 2 * r2, CH))
    # three: two rings open on the left between ±135°.
    r3t, r3b = 200, 220
    g["three"] = union(minus(ring(260, CH - r3t, r3t, r3t - t + 10), open_wedge(260, CH - r3t, 135, 225)),
                       minus(ring(260, r3b, r3b, r3b - t), open_wedge(260, r3b, 135, 225)))
    # four: a stem, a bar, and a diagonal from the stem's top to the bar.
    g["four"] = union(rect(360, 0, 360 + S, CH), rect(0, 160, 620, 160 + H),
                      inter(leg(360 - WDC + 40, CH, 0, 160, WDC), rect(0, 160, 620, CH)))
    # five: a top bar, a short stem, and a ring open on the left.
    r5 = 255
    c5 = (r5 + 20, r5)
    g["five"] = union(rect(60, CH - H, 540, CH), rect(60, 380, 60 + S, CH),
                      minus(ring(*c5, r5, r5 - t), open_wedge(*c5, 135, 225)))
    # six and nine: a ring and a 45°-ish stroke rising from it.
    r6 = 260
    six = union(ring(r6, r6, r6, r6 - t), inter(leg(0, r6, 300, CH, 200), rect(0, r6, 2 * r6, CH)))
    g["six"] = six
    g["nine"] = transform(six, -1, -1, 2 * r6, CH)
    g["seven"] = union(rect(0, CH - H, 560, CH), leg(560 - WDC, CH - H, 100, 0, WDC))
    g["eight"] = union(ring(270, CH - 195, 195, 195 - t + 15), ring(270, 225, 225, 225 - t))
    return g


def punctuation():
    """ASCII punctuation, keyed by Unicode character."""
    g = {}
    dot = lambda x=S / 2, y=S / 2: disc(x, y, S / 2)
    comma = union(dot(), thick((S * 0.8, S * 0.35), (S * 0.15, -170), 110))
    g["."] = dot()
    g[","] = comma
    g[":"] = union(dot(), dot(y=X - S / 2))
    g[";"] = union(comma, dot(y=X - S / 2))
    g["!"] = union(rect(0, 270, S, CH), dot())
    r = 210
    hook_q = minus(ring(r, CH - r, r, r - 160), rect(-1, CH - 2 * r - 1, r, CH - r))
    g["?"] = union(hook_q, rect(r, 270, r + S, CH - 2 * r + 160), dot(r + S / 2))
    g["'"] = rect(0, CH - 260, 130, CH)
    g['"'] = union(rect(0, CH - 260, 130, CH), rect(200, CH - 260, 330, CH))
    g["`"] = thick((0, CH), (170, CH - 190), 120)
    g["-"] = rect(0, 210, 320, 210 + 120)
    g["_"] = rect(0, -170, 520, -170 + 110)
    g["+"] = union(rect(0, 220, 460, 330), rect(175, 45, 285, 505))
    g["="] = union(rect(0, 150, 460, 260), rect(0, 300, 460, 410))
    g["<"] = inter(union(thick((480, 520), (40, 280), 130), thick((40, 280), (480, 40), 130)), rect(0, 0, 480, 560))
    g[">"] = transform(g["<"], -1, 1, 480)
    g["^"] = union(thick((0, 400), (240, CH), 130), thick((240, CH), (480, 400), 130))
    g["~"] = union(thick((0, 230), (150, 340), 110), thick((150, 340), (300, 230), 110), thick((300, 230), (450, 340), 110))
    g["*"] = union(*[thick((230 + 170 * math.cos(math.radians(a)), CH - 200 + 170 * math.sin(math.radians(a))),
                           (230 - 170 * math.cos(math.radians(a)), CH - 200 - 170 * math.sin(math.radians(a))), 100)
                     for a in (90, 30, 150)])
    g["/"] = leg(460 - 180, CH, 0, DSC + 120, 180)
    g["\\"] = transform(g["/"], -1, 1, 460)
    g["|"] = rect(0, DSC + 60, 130, CH + 20)
    g["["] = union(rect(0, -120, S, CH + 20), rect(0, CH + 20 - 120, 320, CH + 20), rect(0, -120, 320, 0))
    g["]"] = transform(g["["], -1, 1, 320)
    g["{"] = union(rect(120, -120, 120 + 150, CH + 20), rect(120, CH + 20 - 110, 340, CH + 20), rect(120, -120, 340, -10),
                   rect(0, 240, 121, 380))
    g["}"] = transform(g["{"], -1, 1, 340)
    pr = 460
    g["("] = inter(ring(pr, 320, pr, pr - 160), rect(0, -140, 230, 780))
    g[")"] = transform(g["("], -1, 1, 230)
    g["#"] = union(rect(0, 170, 600, 280), rect(0, 410, 600, 520), leg(220, CH - 60, 110, 0, 120), leg(420, CH - 60, 310, 0, 120))
    g["%"] = union(ring(140, CH - 140, 140, 55), ring(560, 140, 140, 55), leg(560, CH, 20, 0, 160))
    g["$"] = union(uppercase()["S"], rect(300 - 50, -90, 300 + 50, CH + 90))
    # &: a small ring over a large one, the large one opened on the upper right, with a leg.
    g["&"] = union(minus(ring(250, 230, 230, 90), open_wedge(250, 230, 0, 50)), ring(230, 570, 170, 50),
                   inter(thick((110, 460), (600, 0), 170), rect(0, 0, 640, 470)))
    # @: a ring with a small a inside, open at the lower right.
    g["@"] = union(minus(ring(400, 300, 400, 300), open_wedge(400, 300, -60, -20)),
                   ring(400, 300, 170, 70), rect(500, 140, 640, 460))
    return g


PUNCT_NAMES = {".": "period", ",": "comma", ":": "colon", ";": "semicolon", "!": "exclam", "?": "question",
               "'": "quotesingle", '"': "quotedbl", "`": "grave", "-": "hyphen", "_": "underscore", "+": "plus",
               "=": "equal", "<": "less", ">": "greater", "^": "asciicircum", "~": "asciitilde", "*": "asterisk",
               "/": "slash", "\\": "backslash", "|": "bar", "[": "bracketleft", "]": "bracketright",
               "{": "braceleft", "}": "braceright", "(": "parenleft", ")": "parenright", "#": "numbersign",
               "%": "percent", "$": "dollar", "&": "ampersand", "@": "at"}
DIGIT_NAMES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
LOWER = set("abcdefghijklmnopqrstuvwxyz")


def all_glyphs():
    """{glyph name: path} for every drawn glyph."""
    out = dict(lowercase())
    out.update(uppercase())
    out.update(digits())
    out.update({PUNCT_NAMES[c]: p for c, p in punctuation().items()})
    return out


def char_map():
    """{codepoint: glyph name} for the full font: printable ASCII."""
    cmap = {0x20: "space"}
    for c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
        cmap[ord(c)] = c
    for d, name in enumerate(DIGIT_NAMES):
        cmap[ord(str(d))] = name
    for c, name in PUNCT_NAMES.items():
        cmap[ord(c)] = name
    return cmap


def glyphs(names=None):
    """Return {name: (path, width, lsb, rsb)}, each path moved to start at x = 0.

    Side bearings are measured on the letter's body. For a lowercase letter that is
    its ink between the baseline and 90% of the x-height; for any other glyph, all of it. What reaches out above or below (the f's top,
    the j's hook) may hang over the neighbours; kerning keeps them clear."""
    out = {}
    for name, path in all_glyphs().items():
        if names and name not in names:
            continue
        path.simplify()
        xmin = path.bounds[0]
        if xmin:
            path = transform(path, 1, 1, -xmin)
        # lowercase: the body is the x-height zone; anything else: all of it
        _, y0, _, y1 = path.bounds
        band = rect(-1, 1, path.bounds[2] + 1, 0.9 * X) if name in LOWER else rect(-1, y0 - 1, path.bounds[2] + 1, y1 + 1)
        x0, _, x1, _ = inter(path, band).bounds
        out[name] = (path, path.bounds[2], round(SB - x0), round(SB - (path.bounds[2] - x1)))
    return out


# ── kerning ─────────────────────────────────────────────────────────────────
def profile(path, side, lo, hi, n=60):
    """Distance from the glyph's box to its ink, on one side, at n heights in [lo, hi].
    None where the glyph has no ink at that height."""
    xmin, _, xmax, _ = path.bounds
    out = []
    for k in range(n):
        y = lo + (hi - lo) * (k + 0.5) / n
        cut = inter(path, rect(xmin - 1, y - 0.5, xmax + 1, y + 0.5))
        if not list(cut):
            out.append(None); continue
        cx0, _, cx1, _ = cut.bounds
        out.append(cx0 - xmin if side == "left" else xmax - cx1)
    return out


def kerning(gs):
    """Kern every pair so the white between the two letters, in the x-height
    zone, equals the white between two straight stems (2 * SB). Depth into a
    round or open side is clipped at KERN_DEPTH. Then a floor: at no height do
    the two letters come closer than MIN_GAP."""
    cache = {}
    def prof(g, side, lo, hi):
        key = (g, side, round(lo), round(hi))
        if key not in cache:
            cache[key] = profile(gs[g][0], side, lo, hi)
        return cache[key]
    full = {}
    for g, (p, *_) in gs.items():
        _, y0, _, y1 = p.bounds
        full[g] = (y0, y1)
    pairs = {}
    deep = 2 * SB + KERN_DEPTH
    for a in gs:
        for b in gs:
            # The zone where the white is judged: the x-height zone when a
            # lowercase letter is involved, else the height both glyphs share.
            if a in LOWER or b in LOWER:
                zlo, zhi = 0, X
            else:
                zlo, zhi = max(0, full[a][0], full[b][0]), min(full[a][1], full[b][1])
            k = 0
            if zhi - zlo >= 40:
                gaps = [deep if ra is None or lb is None else min(gs[a][3] + ra + gs[b][2] + lb, deep)
                        for ra, lb in zip(prof(a, "right", zlo, zhi), prof(b, "left", zlo, zhi))]
                k = round(2 * SB - sum(gaps) / len(gaps))
            lo, hi = max(full[a][0], full[b][0]), min(full[a][1], full[b][1])
            if hi > lo:
                raw = [gs[a][3] + gs[b][2] + ra + lb for ra, lb in zip(prof(a, "right", lo, hi), prof(b, "left", lo, hi))
                       if ra is not None and lb is not None]
                if raw:
                    k = max(k, MIN_GAP - round(min(raw)))
            if k:
                pairs[(a, b)] = k
    return pairs


def kern_classes(gs, pairs):
    """Group glyphs whose kerning is the same on one side, so the feature is
    written as class pairs, not one line per pair."""
    names = sorted(gs)
    def classes(side):
        groups = {}
        for g in names:
            key = tuple(pairs.get((g, o) if side == "left" else (o, g), 0) for o in names)
            groups.setdefault(key, []).append(g)
        return list(groups.values())
    return classes("left"), classes("right")


def space_pairs(gs):
    """A letter that hangs out on one side (the j's hook, the f's top) takes
    that much more room from the space beside it, so words do not run together."""
    out = {}
    for g, (_, _, lsb, rsb) in gs.items():
        if lsb < 0:
            out[("space", g)] = -lsb
        if rsb < 0:
            out[(g, "space")] = -rsb
    return out


def kern_feature(gs, pairs):
    left, right = kern_classes(gs, pairs)
    lines = ["languagesystem DFLT dflt;", "languagesystem latn dflt;"]
    lines += [f"@L{i} = [{' '.join(c)}];" for i, c in enumerate(left)]
    lines += [f"@R{i} = [{' '.join(c)}];" for i, c in enumerate(right)]
    lines.append("feature kern {")
    sp = space_pairs(gs)
    lines += [f"    pos {a} {b} {v};" for (a, b), v in sorted(sp.items())]
    if sp:
        lines.append("    subtable;")
    for i, lc in enumerate(left):
        for j, rc in enumerate(right):
            v = pairs.get((lc[0], rc[0]), 0)
            if v:
                lines.append(f"    pos @L{i} @R{j} {v};")
    lines.append("} kern;")
    return "\n".join(lines) + "\n"


# ── fonts ───────────────────────────────────────────────────────────────────
def draw(path, pen, dx):
    """Replay a pathops path into a fontTools pen, moved right by dx."""
    for verb, pts in path:
        pts = [(x + dx, y) for x, y in pts]
        if verb == pathops.PathVerb.MOVE:
            pen.moveTo(*pts)
        elif verb == pathops.PathVerb.LINE:
            pen.lineTo(*pts)
        elif verb == pathops.PathVerb.CUBIC:
            pen.curveTo(*pts)
        elif verb == pathops.PathVerb.QUAD:
            pen.qCurveTo(*pts)
        elif verb == pathops.PathVerb.CLOSE:
            pen.closePath()


def build_font(gs, pairs, family, ps_name, cmap, description):
    order = [".notdef", "space"] + sorted(gs)
    ascent = math.ceil(max(max(p.bounds[3] for p, *_ in gs.values()), A) / 10) * 10
    descent = math.floor(min(min(p.bounds[1] for p, *_ in gs.values()), 0) / 10) * 10
    ascent, descent = max(ascent, 800), min(descent, -200)
    fb = FontBuilder(UPM, isTTF=True)
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap(cmap)
    glyf, hmtx = {}, {}
    for name in order:
        pen = TTGlyphPen(None)
        if name == ".notdef":
            draw(minus(rect(0, 0, 400, A), rect(60, 60, 340, A - 60)), Cu2QuPen(pen, 1.0, reverse_direction=True), 40)
            hmtx[name] = (480, 40)
        elif name == "space":
            hmtx[name] = (240, 0)
        else:
            path, width, lsb, rsb = gs[name]
            draw(path, Cu2QuPen(pen, max_err=1.0, reverse_direction=True), lsb)
            hmtx[name] = (round(lsb + width + rsb), lsb)
        glyf[name] = pen.glyph()
    fb.setupGlyf(glyf)
    fb.setupHorizontalMetrics(hmtx)
    fb.setupHorizontalHeader(ascent=ascent, descent=descent)
    style = "Regular"
    fb.setupNameTable({
        "familyName": family, "styleName": style,
        "uniqueFontIdentifier": f"{family} {style} {VERSION}",
        "fullName": f"{family} {style}", "psName": ps_name,
        "version": f"Version {VERSION}", "description": description,
    })
    fb.setupOS2(sTypoAscender=ascent, sTypoDescender=descent, sTypoLineGap=0,
                usWinAscent=ascent, usWinDescent=-descent,
                sxHeight=X, sCapHeight=A, achVendID="BMBL", fsType=0)
    fb.setupPost()
    if pairs:
        addOpenTypeFeaturesFromString(fb.font, kern_feature(gs, pairs))
        # A legacy 'kern' table too, for text stacks that do not read GPOS.
        kt = newTable("kern"); kt.version = 0
        sub = KernTable_format_0(); sub.version, sub.coverage, sub.format = 0, 1, 0
        legacy = {**pairs, **space_pairs(gs)}
        # A format-0 subtable holds at most 10920 pairs; keep the biggest ones if there are more.
        if len(legacy) > 10000:
            legacy = dict(sorted(legacy.items(), key=lambda kv: -abs(kv[1]))[:10000])
        sub.kernTable = legacy; kt.kernTables = [sub]
        fb.font["kern"] = kt
    buf = io.BytesIO(); fb.font.save(buf)
    return TTFont(io.BytesIO(buf.getvalue()))


def wordmark_font(gs, pairs):
    cmap = {0x20: "space"}
    for ch in WORDMARK:
        cmap[ord(ch)] = ch
        cmap[ord(ch.upper())] = ch      # B I M L E show the same letters: "Bimble" works
    sub = {g: gs[g] for g in WORDMARK}
    return build_font(sub, {p: v for p, v in pairs.items() if p[0] in sub and p[1] in sub},
                      "Bimble Wordmark", "BimbleWordmark-Regular", cmap,
                      "Only the letters of the word bimble. Drawn from discs and bars for the Bimble project.")


def full_font(gs, pairs):
    cmap = char_map()
    return build_font(gs, pairs, "Bimble", "Bimble-Regular", cmap,
                      "The Bimble typeface, drawn from discs, bars and 45-degree cuts for the Bimble project.")


# ── the logos ───────────────────────────────────────────────────────────────
# Each logo keeps its discs. Its letters are replaced by the glyphs above, at
# the size the old letters had (x-height 89 units), with the font's spacing
# and kerning. Rows sit at baseline 197 ("bim") and 408 ("ble"); each b
# starts at x = 104.4.
LOGO_K = 89 / X
LOGO_ROWS = [("bim", 197), ("ble", 408)]
LOGO_LEFT = 104.4
ICON_SHIFT = (-3.15, -36.46)  # the icon's b is the mark's b, moved


def svg_d(path, k, ox, baseline):
    pen = SVGPathPen(None, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
    draw(transform(path, k, -k, ox, baseline, simplify=False), pen, 0)
    return pen.getCommands()


def logo_letters(gs, kern, icon=False):
    if icon:
        dx, dy = ICON_SHIFT
        return f'  <path fill="#141414" d="{svg_d(gs["b"][0], LOGO_K, 104.4 + dx, 197 + dy)}"/>\n'
    ds = []
    for word, base in LOGO_ROWS:
        x = LOGO_LEFT - gs[word[0]][2] * LOGO_K       # pen position, as in the font
        for ch, nxt in zip(word, word[1:] + " "):
            path, width, lsb, rsb = gs[ch]
            ds.append(svg_d(path, LOGO_K, x + lsb * LOGO_K, base))
            x += (lsb + width + rsb + kern.get((ch, nxt), 0)) * LOGO_K
    return '  <g fill="#141414">\n' + "".join(f'    <path d="{d}"/>\n' for d in ds) + "  </g>\n"


def update_logos(gs, kern):
    changed = []
    for svg in sorted((SKILL / "assets/logo").glob("*.svg")):
        s = svg.read_text()
        if "-icon" in svg.name:
            new = re.sub(r'  <path fill="#141414" d="[^"]*"/>\n', lambda _: logo_letters(gs, kern, icon=True), s, count=1)
        else:
            new = re.sub(r'  <g fill="#141414">\n.*?  </g>\n', lambda _: logo_letters(gs, kern), s, count=1, flags=re.S)
        if new == s and "#141414" not in s:
            raise SystemExit(f"{svg.name}: no ink letters found")
        if new != s:
            svg.write_text(new); changed.append(svg.name)
    return changed


# ── checks ──────────────────────────────────────────────────────────────────
def check(wm, full, pairs):
    """The one runnable check for both fonts."""
    cmap = wm.getBestCmap()
    assert set(cmap.values()) <= {"space", *WORDMARK}, cmap
    for ch in "bimble BIMBLE":
        assert ord(ch) in cmap, ch
    assert set(full.getBestCmap()) == set(range(0x20, 0x7F)), "the full font must cover printable ASCII, exactly"
    for f in (wm, full):
        assert "GPOS" in f and "kern" in f
        top, bot = f["hhea"].ascent, f["hhea"].descent
        for g in f.getGlyphOrder():
            gl = f["glyf"][g]
            if gl.numberOfContours:
                assert bot <= gl.yMin and gl.yMax <= top, (g, gl.yMin, gl.yMax, bot, top)
    # one geometry: the wordmark's letters are the full font's letters
    for g in WORDMARK:
        assert wm["glyf"][g].coordinates == full["glyf"][g].coordinates, g
        assert wm["hmtx"][g] == full["hmtx"][g], g
    # two straight stems need no kerning; a round side comes closer
    assert ("l", "i") not in pairs and ("i", "l") not in pairs, pairs
    assert pairs[("b", "l")] < 0 and pairs[("l", "e")] < 0, pairs
    assert wm["glyf"]["b"].numberOfContours == 2 and wm["glyf"]["e"].numberOfContours == 2


def font_bytes(font, flavor=None):
    font.flavor = flavor
    buf = io.BytesIO(); font.save(buf)
    font.flavor = None
    return buf.getvalue()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="build in memory and test, write nothing")
    a = ap.parse_args()
    gs = glyphs()
    pairs = kerning(gs)
    wm, full = wordmark_font(gs, pairs), full_font(gs, pairs)
    check(wm, full, pairs)
    wm_woff2 = font_bytes(wm, "woff2")
    assert len(wm_woff2) < 2048, f"the wordmark font grew to {len(wm_woff2)} bytes"
    print("Kerning in bimble:", ", ".join(f"{x}{y} {pairs.get((x, y), 0)}" for x, y in zip("bimble", "imble")))
    print(f"{len(pairs)} kern pairs; wordmark woff2 {len(wm_woff2)} bytes")
    if a.check:
        print("ok: both fonts built and checked")
        raise SystemExit(0)
    out = SKILL / "fonts"
    for font, stem in ((wm, "bimble-wordmark"), (full, "bimble-regular")):
        (out / f"{stem}.ttf").write_bytes(font_bytes(font))
        (out / f"{stem}.woff2").write_bytes(font_bytes(font, "woff2"))
        print("Wrote", out / f"{stem}.ttf", "and .woff2")
    print("Updated logos:", ", ".join(update_logos(gs, pairs)) or "none")
