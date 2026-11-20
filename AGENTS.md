# Maintaining the Bimble design skill

This repo ships one agent skill, `skills/bimble-design/`. To use it, follow
`skills/bimble-design/SKILL.md`. This file is for changes to the design system itself.
`CLAUDE.md` imports it.

## Where things live

- Everything that the skill reads lives in `skills/bimble-design/`, with relative
  paths. The release zips this folder as it is, for claude.ai, Codex and projects.
  No file in it can point outside it.
- The `SKILL.md` frontmatter has `name` and `description` only. The description
  stays under 200 characters, the limit of claude.ai.
- The zip's top folder is `bimble-design`, the same as the skill name. If the names
  differ, claude.ai refuses the upload.
- Repo tooling stays at the root: `design-system/` (the claude.ai Design System
  sources), `scripts/`, `.github/workflows/`, `.claude-plugin/`.

## Changing a token

1. Edit `skills/bimble-design/tokens/tokens.json`.
2. Make the same change in `tokens.css` and `tokens.js`.
3. If you add a token family or rename one, update the name maps in
   `scripts/build-design-system.py` and in `dsVarsCss()` in `scripts/build-catalog.mjs`.
4. Run `make check`. Every check line must say "ok".
5. If a value that they quote changed, update `SKILL.md`, `PROMPT.md`,
   `references/` and `design-system/src/README.md`.
6. Add a line to `CHANGELOG.md`.

## Changing the wordmark or the logo letters

The wordmark font and the letters in every logo SVG come from one geometry, in
`scripts/build-wordmark.py`. Never edit the letter paths in the SVGs by hand.

1. Change the constants or the shapes in `scripts/build-wordmark.py`.
2. Run `make wordmark`. It needs `pip install fonttools skia-pathops brotli`.
3. It writes `fonts/bimble-wordmark.ttf` and `.woff2`, and replaces the letters in
   `assets/logo/*.svg`. The discs in the SVGs do not change.
4. Kerning is measured, not typed: `kerning()` in the script sets each pair so the white
   between the letters matches two straight stems. Do not add pairs by hand.
5. Never trace or copy outlines from another typeface.

## Adding a component preview

1. Add `design-system/src/components/<Name>/preview.html` and a `README.md` next to it.
2. The first line must be a `@dsCard` comment, for example
   `<!-- @dsCard group="Actions" height=96 subtitle="Static rendition" -->`. The
   catalog and the claude.ai page both read it. A preview with no `@dsCard` is dropped.
3. Use the design system's variable names (`--clay`, `--ink`, `--space-4`), not `--bb-*`.
   The catalog defines them in `site/ds-vars.css`.
4. Run `make catalog` and open `site/index.html`, or run `make dev`.

## Releasing

Increase `version` in `.claude-plugin/plugin.json` and move the `CHANGELOG.md`
entries under the new version. Merge, then tag `vX.Y.Z`. The release workflow runs
`make check`, builds the zips and publishes them. Plugin users get the update with
`claude plugin marketplace update`. Then sync the claude.ai Design System page by
hand, as `RELEASING.md` describes.
