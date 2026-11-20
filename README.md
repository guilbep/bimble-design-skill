# Bimble design skill

The design system of Bimble, the open-source IFC/BIM app, as an agent skill: colours,
fonts, logos, tokens and rules. See it in the catalog:
<https://guilbep.github.io/bimble-design-skill/>.

## Install

Nothing to clone. Pick the line for your tool.

### Claude Desktop and claude.ai: upload the skill

1. Download `bimble-design.zip` from the
   [latest release](https://github.com/guilbep/bimble-design-skill/releases/latest/download/bimble-design.zip).
2. In Claude, go to Customize › Skills.
3. Click "+", then "Create skill", then "Upload a skill".
4. Select `bimble-design.zip`.

The skill then shows in your skills list, where you can turn it on or off. The
release also has the same archive as `bimble-design.skill`.

### Claude Code: a plugin

```bash
claude plugin marketplace add guilbep/bimble-design-skill
claude plugin install bimble@bimble-design-skill
```

Inside a session, type the same two commands as `/plugin marketplace add …` and
`/plugin install …`. The skill then works in every repo. To get new versions, run
`claude plugin marketplace update bimble-design-skill`.

To give the skill to a whole project team, commit this to the project's
`.claude/settings.json`. Claude Code offers the plugin to each person who trusts the
folder, with no setup per person:

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

### Codex, OpenCode and other agents: unzip the skill

```bash
curl -fsSL https://github.com/guilbep/bimble-design-skill/releases/latest/download/bimble-design.zip -o /tmp/bimble-design.zip
unzip -o /tmp/bimble-design.zip -d ~/.codex/skills/    # Codex
unzip -o /tmp/bimble-design.zip -d ~/.claude/skills/   # OpenCode, and Claude Code without plugins
```

To update, run the two lines again. A model with no skill support can read
`skills/bimble-design/PROMPT.md`, which holds the whole system as one prompt.

### In an app

Copy `skills/bimble-design/` into the project. Load the fonts first, then the tokens:

```html
<link rel="stylesheet" href="bimble-design/fonts/fonts.css">
<link rel="stylesheet" href="bimble-design/tokens/tokens.css">
```

For the word "bimble" as a title, use `font-family: var(--bb-font-wordmark)`. That
font has only the letters b, i, m, l and e. Native apps can load
`fonts/bimble-wordmark.ttf`. The full Bimble typeface (`--bb-font-bimble`,
lowercase only for now) is for short brand lines. The catalog's Fonts section
shows which font goes where.

In components, use the role variables (`--bb-action`, `--bb-selection`,
`--bb-success`, `--bb-attention`, `--bb-reference`), not the raw colours.
`tokens/tokens.js` has the same values for JavaScript.

## Use

Ask for Bimble UI and the skill starts by itself. You can also call it with a brief:
`/bimble:bimble-design` in Claude Code with the plugin. The agent reads `SKILL.md`,
then the files in `references/` that the task needs, then studies
`examples/app-shell.html`.

## Contents

```
skills/bimble-design/     the skill: every install ships this folder, and nothing else
  SKILL.md                entry point: the rules and the file map
  PROMPT.md               the whole system as one paste-in prompt
  tokens/                 tokens.json (W3C DTCG), tokens.css, tokens.js
  fonts/                  Sora, Source Sans 3, DM Mono as woff2, the two Bimble fonts, fonts.css, licences
  assets/logo/            main mark, lab mark, "b" icons, two reference studies
  references/             colour, typography, components, voice, contrast
  examples/app-shell.html a working screen that uses only the tokens
design-system/src/        the claude.ai Design System page: README and component previews
scripts/
  check-contrast.py       checks every contrast ratio that the docs quote
  build-design-system.py  builds the Design System files into dist/design-system/
  build-fonts.py          draws both Bimble fonts and the logo letters from one geometry
  build-catalog.mjs       builds the catalog into site/ (Node built-ins only)
  dev.mjs                 live catalog server with reload
.claude-plugin/           the Claude Code marketplace and plugin manifests
.github/workflows/        release, catalog on Pages, catalog preview for each PR
Makefile                  check, skill, design-system, catalog, dev, fonts
```

Run `make` to see the targets. They need Python 3 and Node 20, and no packages.
Only `make fonts` needs packages: `pip install fonttools skia-pathops brotli`.

## Releasing

1. Increase `version` in `.claude-plugin/plugin.json`.
2. Move the entries in `CHANGELOG.md` under the new version.
3. Merge to `main`.
4. Push a tag with the same version: `git tag vX.Y.Z && git push origin vX.Y.Z`.

The release workflow then runs `make check`. If a ratio fails, the release stops.
Otherwise the workflow publishes three files on the GitHub release:

- `bimble-design.zip` and `bimble-design.skill`: the skill, for upload and unzip installs.
- `bimble-design-system.zip`: the files for the claude.ai Design System page.

CI cannot publish to the claude.ai Design System page. After each release, sync it
by hand. [`RELEASING.md`](RELEASING.md) gives the steps.

## Licences

Fonts: SIL Open Font License 1.1 (`skills/bimble-design/fonts/OFL-*.txt`), from
[@fontsource](https://fontsource.org). The OFL lets the catalog serve them. The
Bimble logo, the two Bimble fonts and the rest of this repository: the Bimble
project has not chosen a licence yet. The logo letters and the Bimble fonts are
drawn in `scripts/build-fonts.py` from discs and bars. They replace earlier
letters that came from the Bauhaus 93 typeface.
