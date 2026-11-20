# bimble-design-skill

The Bimble design system as an agent skill. It holds the tokens, the fonts,
the logo files and the rules, in one folder. Claude, another model, a designer
or a developer reads it before building a Bimble screen, page, document or chart.

Direction C, "Two discs", with the disc colours of the five logo studies.
Chosen 20 Nov 2026.

![clay: do](https://img.shields.io/badge/clay-do-C06A41) ![pink: choose](https://img.shields.io/badge/pink-choose-D7ACB6) ![moss: done](https://img.shields.io/badge/moss-done-6A8757) ![ochre: look](https://img.shields.io/badge/ochre-look-D2B347) ![slate: other](https://img.shields.io/badge/slate-other-6E88A3)

## Install

Nothing to clone. Pick the line for your tool.

### Claude Code: a plugin (recommended)

```bash
claude plugin install bimble --marketplace guilbep/bimble-design-skill
```

This line needs Claude Code 2.1.275 or later. Inside a session, type the same
command as `/plugin install bimble --marketplace guilbep/bimble-design-skill`.
On an older Claude Code, use two commands:

```bash
claude plugin marketplace add guilbep/bimble-design-skill
claude plugin install bimble@bimble-design-skill
```

The skill then works in every repo. To get new versions, run
`claude plugin marketplace update bimble-design-skill`.

To give the skill to a whole project team, commit this to the project's
`.claude/settings.json`. Claude Code offers the plugin to each person who
trusts the folder, with no setup per person:

```json
{
  "extraKnownMarketplaces": {
    "bimble-design-skill": {
      "source": { "source": "github", "repo": "guilbep/bimble-design-skill" }
    }
  },
  "enabledPlugins": { "bimble@bimble-design-skill": true }
}
```

### claude.ai and Claude Desktop: upload the skill

Download `bimble-design.zip` from the
[latest release](https://github.com/guilbep/bimble-design-skill/releases/latest).
Then open Settings, go to the Skills section and click "Upload skill". The
release also has the same archive as `bimble-design.skill`.

### Codex, OpenCode and other agents: unzip the skill

```bash
curl -fsSL https://github.com/guilbep/bimble-design-skill/releases/latest/download/bimble-design.zip -o /tmp/bimble-design.zip
unzip -o /tmp/bimble-design.zip -d ~/.codex/skills/    # Codex
unzip -o /tmp/bimble-design.zip -d ~/.claude/skills/   # OpenCode, and Claude Code without plugins
```

To update, run the two lines again.

### Any other model or designer

Paste [`PROMPT.md`](skills/bimble-design/PROMPT.md). It holds the whole system
as one prompt.

## Use

Ask for Bimble UI and the skill starts by itself. You can also call it with a
brief, as `/bimble:bimble-design` in Claude Code with the plugin. The agent
reads `SKILL.md`, then the files in `references/` that the task needs, then
`examples/app-shell.html`.

### In the app

Load the fonts, then the tokens:

```html
<link rel="stylesheet" href="skills/bimble-design/fonts/fonts.css">
<link rel="stylesheet" href="skills/bimble-design/tokens/tokens.css">
```

From JavaScript, import the same values:

```js
import { color, role, series, font } from './skills/bimble-design/tokens/tokens.js'
```

Use the role variables (`--bb-action`, `--bb-selection`, `--bb-success`,
`--bb-attention`, `--bb-reference`), not the raw colours.

## Contents

All files that an install ships are in `skills/bimble-design/`.

| Path | What it is |
|---|---|
| `skills/bimble-design/SKILL.md` | The skill entry point: the rules and the file map |
| `skills/bimble-design/PROMPT.md` | The whole system as one paste-in prompt |
| `skills/bimble-design/tokens/` | `tokens.json` (W3C DTCG), `tokens.css`, `tokens.js` |
| `skills/bimble-design/fonts/` | Sora, Source Sans 3, DM Mono as woff2, latin and latin-ext, with `fonts.css` |
| `skills/bimble-design/assets/logo/` | Main mark, lab mark, "b" icons, two reference studies |
| `skills/bimble-design/references/` | Colour, typography, components, voice, contrast |
| `skills/bimble-design/examples/app-shell.html` | A working screen that uses only the tokens |
| `skills/bimble-design/scripts/check-contrast.py` | Calculates again every contrast ratio that the docs quote, from `tokens.json` |
| `.claude-plugin/` | The Claude Code marketplace and plugin manifests |
| `.github/workflows/release.yml` | On a `v*` tag, publishes the skill as `bimble-design.zip` |

## Change it

1. Edit `skills/bimble-design/tokens/tokens.json`.
2. Make the same change in `tokens.css` and `tokens.js`.
3. Run `python3 skills/bimble-design/scripts/check-contrast.py`. Every check line must say "ok".
4. If a value that they quote changed, update the tables in `SKILL.md`, `PROMPT.md` and `references/`.
5. Increase `version` in `.claude-plugin/plugin.json`.
6. Push a tag with the same version, for example `git tag v0.2.0 && git push origin v0.2.0`. The release workflow then publishes the zip.

## Licences

Fonts: SIL Open Font License 1.1 (`skills/bimble-design/fonts/OFL-*.txt`), from
[@fontsource](https://fontsource.org). The Bimble logo and the rest of this
repository: the Bimble project has not chosen a licence yet.
