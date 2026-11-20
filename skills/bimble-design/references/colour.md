# Colour

Five disc colours from the logo studies, each with **one job**. The test for
any use of colour: *which job is this?* If the answer is "it looks nice",
use a neutral.

## The jobs

### Clay: do
`--bb-clay` `#C06A41` fill · `--bb-clay-text` `#A35A37` text

The main action of the view: Place slab, Save, Export IFC. **One per view.**
Secondary actions are ink-outlined pills on sheet or plain ink text. Links
use clay text. Clay is also the main logo disc.

### Pink: choose
`--bb-pink` `#D7ACB6` fill · `--bb-pink-text` `#80676D` text

Selection and only selection: selected element in the viewport (75% fill +
1.6px ink outline), selected rows in lists, selected item on a printed
markup sheet, `::selection`. Hover is **not** pink (use sunk `#EDE7DB`).

### Moss: done
`--bb-moss` `#6A8757` fill · `--bb-moss-text` `#5B744A` text

Saved, synced, check passed, export finished. Also the lab build's logo disc,
which is fine: a lab build is a state, not a decoration.

### Ochre: look
`--bb-ochre` `#D2B347` fill · `--bb-ochre-text` `#7D6B2A` text

Needs attention: unsaved edits, an element borrowed from someone else's
model, warnings, failed checks. **Errors** are also ochre: an ochre band with
ink text that starts with the word "Error". Bimble has no red; the word does
the work, which also keeps it readable for red-green colour blindness.

### Slate: other
`--bb-slate` `#6E88A3` fill · `--bb-slate-text` `#5A6F85` text

Things that aren't yours: linked models (dashed slate outline in the
viewport), references, "theirs" in a merge view.

## Neutrals

| Token | Hex | Use |
|---|---|---|
| `--bb-cream` | `#F5F2EB` | Page ground, side panels |
| `--bb-sheet` | `#FFFFFF` | Cards, top bar, viewport, paper |
| `--bb-sunk` | `#EDE7DB` | Inner dividers, hover on cream/sheet, drawing side faces |
| `--bb-ink` | `#141414` | Text, icons, outlines, active tab |
| `--bb-stone` | `#5C574D` | Quiet text, labels, control borders |
| `--bb-line` | `#DDD6C8` | Card edges and dividers (decoration only) |

## Rules

1. **Ink on fills.** Text on any disc colour is `#141414`. White fails on most of them.
2. **`-text` shades for text.** A coloured word uses the `-text` shade (all ≥ 4.6:1 on cream).
3. **Words with colour.** Every coloured chip, band or dot has a label.
4. **Outline pale markers.** Pink and ochre are 1.8:1 against cream; dots and swatches in those get a 1px ink border.
5. **Line is decoration.** An input's border is stone (6.4:1), not line (1.3:1). Focus is a 2px ink ring, 2px offset.
6. **Series order:** clay, slate, moss, ochre, pink. Beyond five, vary pattern or label, not new hues.
7. **No disc colour as a background region.** Panels are cream or sheet. The one exception is the single big decorative disc on Home or an empty state.
8. **Print.** Drawings are black and white. Axis bubbles are clay/pink on screen and white with ink outline on paper.

## Mapping from a generic UI kit

| Kit role | Bimble |
|---|---|
| primary | clay |
| secondary | ink (outlined) |
| accent / selected | pink |
| success | moss |
| warning | ochre |
| error / danger | ochre + the word "Error" |
| info | slate |
| background | cream |
| surface | sheet |
