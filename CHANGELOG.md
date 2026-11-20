# Changelog

## 0.1.0

- The skill moves to `skills/bimble-design/`, so every install ships one folder.
- Claude Code plugin and marketplace: `claude plugin install bimble@bimble-design-skill`.
- Release workflow: a `v*` tag publishes `bimble-design.zip`, `bimble-design.skill`
  and `bimble-design-system.zip`.
- Catalog on GitHub Pages, with a preview for each pull request.
- The claude.ai Design System sources (`design-system/src/`) and their build
  (`scripts/build-design-system.py`).
- New token: `size.icon` (20px), `--bb-icon` in `tokens.css`.
- New font: Bimble Wordmark (`fonts/bimble-wordmark.woff2` and `.ttf`), only for the
  word "bimble". New tokens `font.family.wordmark`, `type.wordmark` and `--bb-font-wordmark`.
- The logo letters are redrawn from the same geometry as the wordmark font. The old
  letters came from the Bauhaus 93 typeface. All eight logo SVGs change.
- The `SKILL.md` description is now 185 characters, under the 200-character limit of claude.ai.
