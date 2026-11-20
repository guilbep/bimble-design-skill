#!/usr/bin/env python3
"""Build the claude.ai Design System files from this repo.

Single source: skills/bimble-design/tokens/tokens.json (DTCG). The Design System page cannot read
DTCG maps, so this converts them to its list format and assembles:

  dist/design-system/project/
    tokens.json                 generated (list format, meta.source = github)
    README.md, components/**    copied from design-system/src/
    assets/Logos/README.md      copied from design-system/src/
    assets/Logos/*.svg          copied from skills/bimble-design/assets/logo/ (the publisher uploads these as assets)
    fonts/*-latin-*.woff2       copied from skills/bimble-design/fonts/ (latin subset only)

It does NOT write design-system.json (the index): that names uploaded asset
ids, which only exist after the publisher uploads the logos.

Usage: python3 scripts/build-design-system.py [--ref main@abc1234] [--out dist/design-system]
"""
import argparse, datetime, json, pathlib, shutil, subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills/bimble-design"

# DTCG path -> Design System token name. Keep in step with skills/bimble-design/tokens/tokens.css.
COLOR_NAMES = {
    ("ground", "cream"): "cream", ("ground", "sheet"): "sheet", ("ground", "sunk"): "sunk",
    ("ink", "default"): "ink", ("ink", "quiet"): "stone", ("ink", "line"): "line", ("ink", "on-ink"): "on-ink",
}
DISCS = ["clay", "pink", "moss", "ochre", "slate"]
# Roles, as in skills/bimble-design/tokens/tokens.css (--bb-action etc.)
ROLES = [
    ("action", "clay", "Role: the main action. Use roles in components, not raw colours."),
    ("link", "clay-text", "Role: links."),
    ("selection", "pink", "Role: selected content."),
    ("success", "moss", "Role: done, saved, in sync."),
    ("attention", "ochre", 'Role: warnings, unsaved, and errors (always with the word "Error"). Bimble has no red.'),
    ("reference", "slate", "Role: linked and external things."),
]
TYPE_GROUPS = [("Display", "display", ["display", "title", "heading", "panel"]),
               ("Text", "text", ["lead", "body", "ui", "small"]),
               ("Data", "data", ["data", "eyebrow"])]
FONT_FILES = [("Sora", "sora", "500", "normal"), ("Sora", "sora", "700", "normal"),
              ("Source Sans 3", "source-sans-3", "400", "normal"), ("Source Sans 3", "source-sans-3", "400", "italic"),
              ("Source Sans 3", "source-sans-3", "600", "normal"),
              ("DM Mono", "dm-mono", "400", "normal"), ("DM Mono", "dm-mono", "500", "normal")]


def stack(fams):
    return ", ".join(f'"{f}"' if " " in f or f[0].isupper() and f not in ("ui-monospace", "Menlo", "Arial") else f for f in fams)


def build(ref, out):
    src = json.loads((SKILL / "tokens/tokens.json").read_text())
    c = src["color"]
    colors = []
    for (grp, key), name in COLOR_NAMES.items():
        t = c[grp][key]
        colors.append({"name": name, "value": t["$value"].lower(), "usage": t.get("$description", "")})
    for d in DISCS:
        job = c[d].get("$description", "")
        colors.append({"name": d, "value": c[d]["fill"]["$value"].lower(), "usage": f'{job} {c[d]["fill"].get("$description", "")}'.strip()})
        colors.append({"name": f"{d}-text", "value": c[d]["text"]["$value"].lower(), "usage": c[d]["text"].get("$description", "")})
    for name, target, usage in ROLES:
        colors.append({"name": name, "value": "{" + target + "}", "usage": usage})

    fam = src["font"]["family"]
    families = {k: stack(v["$value"]) for k, v in fam.items() if not k.startswith("$")}
    groups = []
    for gname, gfam, styles in TYPE_GROUPS:
        out_styles = []
        for s in styles:
            v = src["type"][s]["$value"]
            st = {"name": s, "fontSize": v["fontSize"], "lineHeight": v["lineHeight"], "fontWeight": v["fontWeight"]}
            if "letterSpacing" in v:
                st["letterSpacing"] = v["letterSpacing"]
            if src["type"][s].get("$description"):
                st["usage"] = src["type"][s]["$description"]
            out_styles.append(st)
        groups.append({"name": gname, "family": gfam, "styles": out_styles})

    def family(key, prefix):
        return {"note": src[key].get("$description", ""),
                "tokens": [{"name": f"{prefix}{k}", "value": v["$value"], "usage": v.get("$description", "")}
                           for k, v in src[key].items() if not k.startswith("$")]}

    radius = family("radius", "radius-")
    space = family("space", "space-")
    size = family("size", "")

    tokens = {
        "name": "Bimble", "version": 1,
        "meta": {"source": "github", "repo": "guilbep/bimble-design-skill", "ref": ref,
                 "paths": {"tokens": ["skills/bimble-design/tokens/tokens.json"], "fonts": ["skills/bimble-design/fonts/"], "assets": ["skills/bimble-design/assets/logo/"],
                           "docs": ["design-system/src/"]},
                 "synced": datetime.date.today().isoformat()},
        "color": {"themes": [{"id": "light", "name": "Light"}], "tokens": colors},
        "type": {"fonts": [{"family": f, "file": f"fonts/{slug}-latin-{w}-{st}.woff2", "weight": w, "style": st}
                           for f, slug, w, st in FONT_FILES],
                 "families": families, "groups": groups},
        "spacing": space, "radius": radius, "size": size,
    }

    proj = out / "project"
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(ROOT / "design-system/src", proj)
    (proj / "tokens.json").write_text(json.dumps(tokens, indent=2, ensure_ascii=False) + "\n")
    (proj / "fonts").mkdir()
    for _, slug, w, st in FONT_FILES:
        shutil.copy(SKILL / f"fonts/{slug}-latin-{w}-{st}.woff2", proj / "fonts")
    (proj / "assets/Logos").mkdir(parents=True, exist_ok=True)
    for svg in sorted((SKILL / "assets/logo").glob("*.svg")):
        shutil.copy(svg, proj / "assets/Logos")
    return proj


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", help="e.g. v1.0.0@abc1234 (default: branch@short-sha from git)")
    ap.add_argument("--out", default=str(ROOT / "dist/design-system"))
    a = ap.parse_args()
    ref = a.ref
    if not ref:
        g = lambda *x: subprocess.run(["git", "-C", str(ROOT), *x], capture_output=True, text=True).stdout.strip()
        ref = f'{g("rev-parse", "--abbrev-ref", "HEAD") or "main"}@{g("rev-parse", "--short", "HEAD")}'
    p = build(ref, pathlib.Path(a.out))
    print(f"Built {sum(1 for f in p.rglob('*') if f.is_file())} files in {p}")
