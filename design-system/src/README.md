# Bimble

Bimble is an open-source, IFC-based BIM app for structural and civil
engineering offices. Its look is **"Two discs"**: the logo's two circles
(clay and pink, black letters) become the whole system. It's warm, friendly
and precise, a first open-source BIM tool that doesn't feel like legacy CAD.

Source of truth: [guilbep/bimble-design-skill](https://github.com/guilbep/bimble-design-skill),
`main@750848d`. Direction C with the logo palette, chosen 20 Nov 2026.

## Colour: one job each

Five colours from the logo studies. Each has **one job**, everywhere: the
app, the web page, the documents. The test for any use of colour: *which
job is this?* If the answer is "it looks nice", use a neutral.

| Token | Job | Use it for |
|---|---|---|
| `clay` (`action`) | **Do** | The one main action per view: Place slab, Save, Export IFC. Links in `clay-text`. |
| `pink` (`selection`) | **Choose** | Selection only: in the viewport, in lists, on printed markup. Hover is not pink. |
| `moss` (`success`) | **Done** | Saved, in sync, check passed. The lab build's mark. |
| `ochre` (`attention`) | **Look** | Not saved, borrowed, warnings. Errors too, always starting with the word "Error". There is no red. |
| `slate` (`reference`) | **Other** | Linked models, references, "theirs" in a merge. |

Neutrals: `cream` ground, `sheet` cards and viewport, `sunk` hover and inner
dividers, `ink` text, `stone` quiet text and control borders, `line`
decoration only.

Rules:
- **Ink on every fill.** Text on clay, pink, moss, ochre or slate is `ink`, never white. All pass 4.5:1.
- **`-text` shades for coloured words.** A clay link is `clay-text`, not `clay`.
- **Words with colour.** Every coloured chip, band or dot has a label.
- **Outline pale markers.** `pink` and `ochre` are 1.8:1 on `cream`: dots and swatches get a 1px `ink` border.
- **`line` is decoration.** Inputs use a `stone` border; focus is a 2px `ink` ring, 2px offset.
- **Series order** for charts and linked models: clay, slate, moss, ochre, pink.
- **No disc colour as a background region**, except the one big decorative disc on Home or an empty state.

## Type

Sora for display and headings (700; 500 for panel names), Source Sans 3 for
everything you read (replaces Roboto), DM Mono for data: dimensions with
units, IFC classes, GUIDs and uppercase eyebrow labels. Sentence case
everywhere; uppercase only for eyebrows. A space before units and as the
thousands separator: `250 mm`, `+3 000`.

## Shape and space

**Round where you touch, square for drawings.** Buttons, chips, tabs:
`radius-pill`. Swatches, dots, axis bubbles: `radius-disc`. Cards and panels:
`radius-md`. Inputs: `radius-sm`. Drawings, sheets, the viewport, tables and
banners: `radius-none`. Spacing on a 4px base, `space-1` to `space-8`.

**One big disc per screen**, on Home and empty states, never over work.
**Paper stays paper**: drawings print black and white; axis bubbles are clay
and pink on screen only.

## App anatomy

A `sheet` top bar: the "b" icon, pill tabs (Project · Model · Annotate ·
Sheets; active = `ink` pill with `on-ink` text), status chips on the right,
then one `clay` button. A `cream` properties panel on the left: Sora 500
title, rows with `stone` labels and `ink` values (DM Mono for
measurements), status dots at the foot. A `sheet` viewport: the selected
element `pink` at 75% with a 1.6px `ink` outline; linked models `slate`
dashed.

## Iconography

1.5px stroke icons, round caps and joins, `ink`, 20px on a 24px grid. No
filled icons except the logo. No emoji.

## Voice

Plain, short, specific, like a good site engineer. Buttons are verbs with an
object ("Place slab", "Export IFC"); chips are nouns with numbers ("Not
saved: 2 edits"). Use the trade's words (slab, storey, C30/37, 1:50). Errors
say what happened, then what to do. No blame, no "Oops". The app ships in
English and French: leave room for +20–30% length.

## Logos

`bimble-mark` (study 6) is the main mark; `bimble-mark-lab` (study 7, moss)
marks builds under test only. `bimble-icon` is the single "b" disc for app
bars and favicons. Never recolour, outline or add effects; letters are
always ink.

## Don'ts

No gradients, glows or drop shadows on controls. No white text on clay. No
second primary action. No pink for anything but selection. No red.

## Not synced

Only the latin subset of each font is here (covers English and French). The
latin-ext files are in the repo's `skills/bimble-design/fonts/`. There's no dark theme yet:
none has been decided. The components below are static renditions of the
patterns in `skills/bimble-design/references/components.md`. There's no component library to
build from yet.
