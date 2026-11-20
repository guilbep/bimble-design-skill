#!/usr/bin/env python3
"""Re-verify every contrast ratio the Bimble docs quote (WCAG 2.x).
Reads skills/bimble-design/tokens/tokens.json so the check follows the tokens. Exit 1 if a rule fails."""
import json, pathlib, sys

T = json.loads((pathlib.Path(__file__).resolve().parent.parent / "skills" / "bimble-design" / "tokens" / "tokens.json").read_text())["color"]

def lum(h):
    h = h.lstrip("#"); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]

def ratio(a, b):
    a, b = lum(a), lum(b); return (max(a, b) + 0.05) / (min(a, b) + 0.05)

ink, cream, sheet = T["ink"]["default"]["$value"], T["ground"]["cream"]["$value"], T["ground"]["sheet"]["$value"]
fails = 0
def check(label, r, need):
    global fails
    ok = r >= need; fails += not ok
    print(f"{'ok  ' if ok else 'FAIL'} {label:34} {r:5.2f}:1  (needs {need})")

for k in ("clay", "pink", "moss", "ochre", "slate"):
    f, t = T[k]["fill"]["$value"], T[k]["text"]["$value"]
    check(f"ink on {k} fill", ratio(ink, f), 4.5)
    check(f"{k} text on cream", ratio(t, cream), 4.5)
    check(f"{k} text on sheet", ratio(t, sheet), 4.5)
    print(f"     {k} fill vs cream (info)            {ratio(f, cream):5.2f}:1  (<3 means outline small markers)")
check("ink on cream", ratio(ink, cream), 4.5)
check("stone on cream", ratio(T["ink"]["quiet"]["$value"], cream), 4.5)
check("stone border vs sheet (control)", ratio(T["ink"]["quiet"]["$value"], sheet), 3)
print(f"     line vs cream (decoration only)    {ratio(T['ink']['line']['$value'], cream):5.2f}:1")
sys.exit(1 if fails else 0)
