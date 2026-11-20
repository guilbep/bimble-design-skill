# bimble-design-skill

The Bimble design system as an agent skill: tokens, fonts, logo files and the
rules, in one folder that Claude (or any model, designer or developer) can
read before building a Bimble screen, page, document or chart.

Direction **C, "Two discs"**, with the disc colours of the five logo studies.
Chosen 20 Nov 2026.

![The five colours](https://img.shields.io/badge/clay-do-C06A41) ![](https://img.shields.io/badge/pink-choose-D7ACB6) ![](https://img.shields.io/badge/moss-done-6A8757) ![](https://img.shields.io/badge/ochre-look-D2B347) ![](https://img.shields.io/badge/slate-other-6E88A3)

## Use it

**As a Claude skill.** Install the folder as a skill (Claude Code: copy or
symlink it into `~/.claude/skills/bimble-design/` or the project's
`.claude/skills/`; claude.ai: upload it as a skill). `SKILL.md` is the entry
point.

**In the app.**
```html
<link rel="stylesheet" href="bimble-design-skill/fonts/fonts.css">
<link rel="stylesheet" href="bimble-design-skill/tokens/tokens.css">
```
or `import { color, role, series, font } from 'bimble-design-skill/tokens/tokens.js'`.
Use the role variables (`--bb-action`, `--bb-selection`, `--bb-success`,
`--bb-attention`, `--bb-reference`) rather than raw colours.

**Anywhere else.** Paste `PROMPT.md`.

## Contents

| Path | What |
|---|---|
| `SKILL.md` | The skill: rules that matter, file map |
| `PROMPT.md` | The whole system as one paste-in prompt |
| `tokens/` | `tokens.json` (W3C DTCG), `tokens.css`, `tokens.js` |
| `fonts/` | Sora, Source Sans 3, DM Mono as woff2, latin + latin-ext, with `fonts.css` |
| `assets/logo/` | Main mark, lab mark, "b" icons, two reference studies |
| `references/` | Colour, typography, components, voice, contrast |
| `examples/app-shell.html` | A working screen using only the tokens |
| `scripts/check-contrast.py` | Re-verifies every quoted contrast ratio from `tokens.json` |

## Changing it

Edit `tokens/tokens.json` and mirror the change in `tokens.css` and
`tokens.js`, then run `python3 scripts/check-contrast.py`. Update the tables
in `SKILL.md`, `PROMPT.md` and `references/` if a value they quote changed.

## Licences

Fonts: SIL Open Font License 1.1 (`fonts/OFL-*.txt`), from
[@fontsource](https://fontsource.org). The Bimble logo and the rest of this
repository: licence to be chosen by the Bimble project.
