#!/usr/bin/env python3
"""Build the Bimble wordmark font and the logo letters from one geometry.

The font holds only b, i, m, l, e (and B, I, M, L, E mapped to the same
glyphs), for the word "bimble". Every letter is drawn here from discs, bars and
slots: no outline comes from another typeface.

  skills/bimble-design/fonts/bimble-wordmark.ttf, .woff2   the font
  skills/bimble-design/assets/logo/*.svg                   the letters in each logo

Needs: pip install fonttools skia-pathops brotli
Usage: python3 scripts/build-wordmark.py [--check]   (--check: build in memory and test only)
"""
import argparse, io, math, pathlib, re

import pathops
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills/bimble-design"

# Geometry, in font units (1000 per em, y up, baseline 0).
UPM = 1000
X = 520          # x-height: the bowls, i, m and e
A = 740          # ascender: b and l
S = 180          # stem width
R = X / 2        # bowl radius: every bowl is a full disc
RC = 85          # counter radius of b (Bauhaus 93's is much smaller and offset)
C = 90           # width of the two m counters
# The e's counter is a rounded slot on the LEFT part of its disc, as in
# Bauhaus 93, so the e mirrors the b: the b has its mass left and its hole
# right, the e its hole left and its mass right.
E_CX = 225       # x of the counter's axis (the disc's centre is at R = 260)
E_W = 68         # half width of the counter
E_TOP, E_BOT = 330, 190  # y of the centres of the counter's round ends
BAR = 62         # e crossbar thickness: it runs from the counter to the right edge
DOT_GAP = 50     # space between the i stem and its dot
# Spacing: every letter gets the same side bearing. Kerning (below) then
# corrects each pair, so that the white between any two letters looks the same.
SB = 60
KERN_DEPTH = 80  # how far into a round side the kerning measure looks (letterspacer-style clip)
K = 0.5522847498 # cubic Bezier constant for a quarter circle


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
    p = pathops.Path()
    p.moveTo(x0, y0); p.lineTo(x1, y0); p.lineTo(x1, y1); p.lineTo(x0, y1); p.close()
    return p


def union(*ps):
    out = ps[0]
    for p in ps[1:]:
        out = pathops.op(out, p, pathops.PathOp.UNION)
    return out


def minus(a, *bs):
    for b in bs:
        a = pathops.op(a, b, pathops.PathOp.DIFFERENCE)
    return a


def arch(x0, w):
    """A round-topped arch of outer width w with a stem-wide wall: half of an m."""
    r = w / 2
    outer = union(rect(x0, 0, x0 + w, X - r), disc(x0 + r, X - r, r))
    inner = union(rect(x0 + S, -1, x0 + w - S, X - r), disc(x0 + r, X - r, r - S))
    return minus(outer, inner)


def glyphs():
    """Return {name: (path, advance)}. Each path starts at x = 0."""
    # b: a straight flat-topped stem that runs into a full disc. The stem's left
    # edge meets the disc's left edge, so the foot is round, with no slit and
    # a centred counter.
    b = minus(union(rect(0, R, S, A), disc(R, R, R)), disc(R, R, RC))
    # i: flat stem and a round dot, the brand's disc.
    i = union(rect(0, 0, S, X), disc(S / 2, X + DOT_GAP + S / 2, S / 2))
    # l: flat stem at ascender height.
    l = rect(0, 0, S, A)
    # m: two arches that share the middle stem.
    w = 2 * S + C
    m = union(arch(0, w), arch(w - S, w))
    # e: a disc with a counter slot on its left part. The bar starts at the
    # slot's left wall, so the eye is a closed loop (no slit, unlike Bauhaus 93),
    # and runs to the right edge. Under the bar the opening is cut at 45°, from
    # the bottom of the slot to the outer edge.
    slot = union(rect(E_CX - E_W, E_BOT, E_CX + E_W, E_TOP), disc(E_CX, E_TOP, E_W), disc(E_CX, E_BOT, E_W))
    e = minus(disc(R, R, R), slot)
    e = union(e, rect(E_CX - E_W - 1, R - BAR / 2, E_CX + E_W + 1, R + BAR / 2))
    yb = R - BAR / 2                       # underside of the bar
    d = E_W * 0.7071                       # the cut leaves the slot at its lower right, at 45°
    qx, qy = E_CX + d, E_BOT - d           # the cut line: y = qy - (x - qx)
    x_top, x_far = qx + qy - yb, 2 * R + 80
    e = minus(e, polygon((x_top, yb), (x_far, yb), (x_far, qy - (x_far - qx))))
    out = {}
    for name, path in {"b": b, "i": i, "l": l, "m": m, "e": e}.items():
        path.simplify()
        xmin, _, xmax, _ = path.bounds
        out[name] = (path, xmax - xmin, SB, SB)
    return out


def profile(path, side, n=52):
    """Distance from the glyph's edge box to its ink, at n heights in the x-height zone."""
    xmin, _, xmax, _ = path.bounds
    out = []
    for k in range(n):
        y = X * (k + 0.5) / n
        cut = pathops.op(path, rect(xmin - 1, y - 0.5, xmax + 1, y + 0.5), pathops.PathOp.INTERSECTION)
        if not list(cut):
            out.append(None); continue
        cx0, _, cx1, _ = cut.bounds
        out.append(cx0 - xmin if side == "left" else xmax - cx1)
    return out


def kerning(gs):
    """Kern every pair so the white between the two letters, in the x-height
    zone, equals the white between two straight stems (2 * SB). Depth into a
    round side is clipped at KERN_DEPTH, as letterspacing tools do."""
    right = {g: profile(p, "right") for g, (p, *_ ) in gs.items()}
    left = {g: profile(p, "left") for g, (p, *_ ) in gs.items()}
    pairs = {}
    for a in gs:
        for b in gs:
            gaps = [2 * SB + min((ra if ra is not None else KERN_DEPTH) + (lb if lb is not None else KERN_DEPTH), KERN_DEPTH)
                    for ra, lb in zip(right[a], left[b])]
            k = round(2 * SB - sum(gaps) / len(gaps))
            if k:
                pairs[(a, b)] = k
    return pairs


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


def build_font(gs, kern):
    order = [".notdef", "space", "b", "i", "m", "l", "e"]
    fb = FontBuilder(UPM, isTTF=True)
    fb.setupGlyphOrder(order)
    cmap = {0x20: "space"}
    for ch in "bimle":
        cmap[ord(ch)] = ch
        cmap[ord(ch.upper())] = ch
    fb.setupCharacterMap(cmap)
    glyf, hmtx = {}, {}
    for name in order:
        pen = TTGlyphPen(None)
        if name == ".notdef":
            draw(minus(rect(0, 0, 400, A), rect(60, 60, 340, A - 60)), Cu2QuPen(pen, 1.0, reverse_direction=True), 40)
            hmtx[name] = (480, 40)
        elif name == "space":
            hmtx[name] = (220, 0)
        else:
            path, width, lsb, rsb = gs[name]
            draw(path, Cu2QuPen(pen, max_err=1.0, reverse_direction=True), lsb)
            hmtx[name] = (round(lsb + width + rsb), lsb)
        glyf[name] = pen.glyph()
    fb.setupGlyf(glyf)
    fb.setupHorizontalMetrics(hmtx)
    fb.setupHorizontalHeader(ascent=800, descent=-200)
    fb.setupNameTable({
        "familyName": "Bimble Wordmark",
        "styleName": "Regular",
        "uniqueFontIdentifier": "Bimble Wordmark Regular 0.1.1",
        "fullName": "Bimble Wordmark Regular",
        "psName": "BimbleWordmark-Regular",
        "version": "Version 0.1.1",
        "description": "Only the letters of the word bimble. Drawn from discs and bars for the Bimble project.",
    })
    fb.setupOS2(sTypoAscender=800, sTypoDescender=-200, sTypoLineGap=0, usWinAscent=800, usWinDescent=200,
                sxHeight=X, sCapHeight=A, achVendID="BMBL", fsType=0)
    fb.setupPost()
    fea = "languagesystem DFLT dflt;\nlanguagesystem latn dflt;\nfeature kern {\n" + "".join(
        f"    pos {a} {b} {v};\n" for (a, b), v in sorted(kern.items())) + "} kern;\n"
    addOpenTypeFeaturesFromString(fb.font, fea)
    return fb.font


# ── the logos ──────────────────────────────────────────────────────────────
# Each logo keeps its discs. Its letters are replaced by the glyphs above, at
# the size the old letters had (x-height 89 units), with the font's own spacing.
# Rows sit at baseline 197 ("bim") and 408 ("ble"); each b starts at x = 104.4.
LOGO_K = 89 / X
LOGO_ROWS = [("bim", 197), ("ble", 408)]
LOGO_LEFT = 104.4
ICON_SHIFT = (-3.15, -36.46)  # the icon's b is the mark's b, moved


def svg_d(path, k, ox, baseline):
    pen = SVGPathPen(None, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
    tp = pathops.Path()
    for verb, pts in path:
        pts = [(ox + x * k, baseline - y * k) for x, y in pts]
        getattr(tp, {pathops.PathVerb.MOVE: "moveTo", pathops.PathVerb.LINE: "lineTo",
                     pathops.PathVerb.CUBIC: "cubicTo", pathops.PathVerb.QUAD: "quadTo",
                     pathops.PathVerb.CLOSE: "close"}[verb])(*[c for p in pts for c in p])
    draw(tp, pen, 0)
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


def check(font):
    """The one runnable check: the font covers bimble, and nothing else."""
    cmap = font.getBestCmap()
    assert set(cmap.values()) <= {"space", "b", "i", "m", "l", "e"}, cmap
    for ch in "bimble BIMBLE":
        assert ord(ch) in cmap, ch
    assert all(font["hmtx"][g][0] > 0 for g in "bimle")
    assert font["glyf"]["b"].numberOfContours == 2       # outline + counter
    assert font["glyf"]["e"].numberOfContours == 2       # outline + upper counter
    assert font["glyf"]["m"].numberOfContours == 1
    assert font["glyf"]["i"].numberOfContours == 2       # stem + dot
    assert "GPOS" in font and any(f.FeatureTag == "kern" for f in font["GPOS"].table.FeatureList.FeatureRecord)


def check_kerning(kern):
    """Two straight stems need no kerning; a round side always comes closer."""
    assert ("l", "i") not in kern and ("i", "l") not in kern, kern
    assert kern[("b", "l")] < 0 and kern[("l", "e")] < 0, kern


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="build in memory and test, write nothing")
    a = ap.parse_args()
    gs = glyphs()
    kern = kerning(gs)
    check_kerning(kern)
    font = build_font(gs, kern)
    buf = io.BytesIO(); font.save(buf); font = TTFont(io.BytesIO(buf.getvalue()))
    check(font)
    print("Kerning in bimble:", ", ".join(f"{a}{b} {kern.get((a, b), 0)}" for a, b in zip("bimble", "imble")))
    if a.check:
        print("ok: the font covers bimble and BIMBLE, glyph shapes and kerning as expected")
        raise SystemExit(0)
    out = SKILL / "fonts"
    font.save(out / "bimble-wordmark.ttf")
    font.flavor = "woff2"; font.save(out / "bimble-wordmark.woff2")
    print("Wrote", out / "bimble-wordmark.ttf", "and .woff2")
    print("Updated logos:", ", ".join(update_logos(gs, kern)) or "none")
