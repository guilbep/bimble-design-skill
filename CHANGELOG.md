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
- The `SKILL.md` description is now 185 characters, under the 200-character limit of claude.ai.
