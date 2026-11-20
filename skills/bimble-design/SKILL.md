---
name: bimble-design
description: Use when designing, building or reviewing any Bimble UI, page, document, icon or chart (the open-source IFC/BIM app): disc colours and their jobs, tokens, fonts, logos, component rules.
---

# Bimble design

Bimble's look is **direction C, "Two discs"**, with the disc colours of the
five logo studies (chosen 20 Nov 2026). The logo's two circles are the
system: round controls, a warm cream ground, and five colours that each have
**one job**, everywhere: the app, the web page, the documents.

## Before you build

1. Load `fonts/fonts.css`, then `tokens/tokens.css` (or import `tokens/tokens.js`).
   Use the `--bb-*` role variables (`--bb-action`, `--bb-selection`…) in
   components, not raw hex.
2. Read `references/colour.md` before you colour anything. Most mistakes are
   a colour doing a second job.
3. For app screens read `references/components.md`; for type,
   `references/typography.md`; for copy, `references/voice.md`.

## The rules that matter

**One job per colour.** Never use a disc colour for decoration or for a job
that isn't its own.

| Colour | Job | Fill | As text | Examples |
|---|---|---|---|---|
| Clay | **Do** | `#C06A41` | `#A35A37` | Place, Save, Export. One primary action per view. |
| Pink | **Choose** | `#D7ACB6` | `#80676D` | Selection in the model, on paper, in lists. |
| Moss | **Done** | `#6A8757` | `#5B744A` | Saved, in sync, check passed. |
| Ochre | **Look** | `#D2B347` | `#7D6B2A` | Not saved, borrowed, warnings; errors with the word "Error". |
| Slate | **Other** | `#6E88A3` | `#5A6F85` | Linked models, references, "theirs" in a merge. |

Neutrals: cream `#F5F2EB` (ground), sheet `#FFFFFF` (cards, paper, viewport),
sunk `#EDE7DB`, ink `#141414` (text), stone `#5C574D` (quiet text), line
`#DDD6C8` (decorative borders only).

- **Text on a disc fill is always ink** (`#141414`), never white. Every fill passes 4.5:1 with ink.
- **A colour used as text uses its `-text` shade**, never the fill.
- **There is no red.** Errors are ink text on an ochre band, and the word "Error" carries the meaning.
- **Never rely on colour alone**: a chip says "Not saved", a dot has a label.
- **Pink and ochre are pale against cream (1.8:1).** Small markers (dots, swatches) get a 1px ink outline.
- **Line `#DDD6C8` is decoration.** Inputs and anything whose edge matters use stone `#5C574D`.
- Charts and linked models use the series order: clay, slate, moss, ochre, pink.

**Round where you touch, square for drawings.** Buttons, chips, tabs: pill
(`999px`). Swatches, status dots, axis bubbles: discs. Cards and panels:
`16px`. Drawings, sheets, the viewport and tables: square.

**One big disc per screen**, on Home and empty states, never over work.

**Paper stays paper.** Drawings print black and white. Disc colours on axis
bubbles are on screen only.

**Type.** Sora 700 for display and headings (Sora 500 for panel names),
Source Sans 3 for everything you read (replaces Roboto), DM Mono for data:
numbers with units, IFC classes, GUIDs, and uppercase eyebrow labels.

## Logo

- `assets/logo/bimble-mark.svg`: the main mark (study 6, clay + pink). App, installers, web page.
- `assets/logo/bimble-mark-lab.svg`: the lab mark (study 7, moss + pink). Prototype/test builds only, so a build under test never looks like the release.
- `assets/logo/bimble-icon.svg` / `bimble-icon-lab.svg`: the single "b" disc for app bars and favicons.
- `-on-cream` variants include the cream ground. Studies 3 and 4 are kept for reference; don't ship them.
- Never recolour, outline, rotate or add effects to the mark. Letters are always ink.

## Don'ts

No gradients, glows or drop shadows on controls. No emoji as icons (use
stroke icons, 1.5px, ink). No white text on clay. No second primary action.
No disc colour as a section background. No pink for anything but selection.

## Files

```
SKILL.md              this file
PROMPT.md             a paste-in prompt for any model or designer
tokens/               tokens.json (DTCG), tokens.css, tokens.js
fonts/                self-hosted woff2 + fonts.css (all SIL OFL 1.1)
assets/logo/          marks and icons, SVG
references/           colour, typography, components, voice, contrast
examples/             app-shell.html, a working reference screen
```
