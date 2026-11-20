# Components

The patterns from the brand board, written down so they are built the same
way everywhere. CSS uses the `--bb-*` variables from `tokens/tokens.css`.
`examples/app-shell.html` shows them together.

## Buttons

| Kind | Look | When |
|---|---|---|
| Primary | Clay fill, ink text 600, pill, 6px 16px padding | The one main action of the view |
| Secondary | Sheet fill, 1px ink border, ink text, pill | Other actions |
| Quiet | No fill, ink text, pill on hover (sunk) | Toolbar and inline actions |
| Icon | 32px disc, 1.5px stroke icon, `aria-label` | Toolbars |

Min height 32px in the desktop app, 44px on touch and the web. Disabled:
stone text on sunk fill, no border. Never white text on clay.

## Tabs (mode switcher)

Row of pills: inactive is stone text on no fill; active is an ink pill with
cream text. Project · Model · Annotate · Sheets.

## Chips (status)

Pill, 3px 12px, ink text 14px on a disc fill, always with words:
- Ochre: "Not saved: 2 edits", "Borrowed from Architecture"
- Slate: "Linked: Architecture"
- Moss: "Saved", "In sync"
- Pink: "3 selected"

## Status dots

12px disc with a 1px ink outline, followed by a label. Used at the foot of
panels: pink "1 selected", moss "History: in sync with the shared folder".

## Top bar

White (`--bb-sheet`), 1px `--bb-sunk` bottom border, 10px 14px padding,
14px text. Left to right: "b" icon (26px), tabs, flexible space, status
chips, the primary button.

## Panels

Cream ground, 16px padding, 10px row gap. Title in Sora 500 14px. Property
rows: `display:flex; justify-content:space-between`, label stone, value ink
(DM Mono for measurements). Status dots pinned to the bottom
(`margin-top:auto`).

## Cards

Sheet fill, 1px line border, 16px radius, 14–24px padding. Selected card:
2px ink border (not pink: pink is for selected *content*, and a pink border
on cream is too faint).

## Inputs

Sheet fill, 1px stone border, 8px radius, 32px height, ink text. Label
above in stone 13px. Focus: 2px ink ring, 2px offset. Invalid: ochre band
under the field with "Error: …".

## Viewport

White, square, no radius. Elements: white faces, sunk/line side faces, 1.2px
ink edges. Selection: pink at 75% opacity with a 1.6px ink outline. Linked
models: slate, 1.4px, dashed `6 4`. Hover: 1.6px ink outline only.

## Drawings and sheets

Square, black and white. Hatching in ink. Axis bubbles are discs: clay and
pink on screen, white with ink outline when printed. Dimension text in DM Mono.

## Banners

Full-width band, 12px 16px, ink text:
- Ochre: warnings and errors ("Error: the IFC file could not be read. Line 214: …")
- Moss: a finished long task ("Exported 12 sheets")
No icons-only banners; the first word says what it is.

## Empty states and Home

The one place for a big decorative disc (a 420px pink or clay circle bled
off a corner, `aria-hidden`). Sora 700 display title, one lead line, one clay
action.

## Icons

1.5px stroke, round caps and joins, ink, 20px on a 24px grid. No filled
icons except the logo. No emoji.
