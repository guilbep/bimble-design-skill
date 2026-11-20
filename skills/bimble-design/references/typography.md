# Typography

Three families, all SIL OFL 1.1, self-hosted in `fonts/` (no network needed,
which matters for a desktop app), and two Bimble fonts drawn from the logo.

| Family | Weights shipped | Job |
|---|---|---|
| **Sora** | 500, 700 | Display, titles, headings (700); panel names (500) |
| **Source Sans 3** | 400, 400 italic, 600 | Everything you read: body, UI, labels, buttons. Replaces Roboto. |
| **DM Mono** | 400, 500 | Data: dimensions with units, IFC classes, GUIDs, coordinates, eyebrow labels |
| **Bimble Wordmark** | 400 | The word "bimble" only: the app title, the web page title. It has only b, i, m, l and e. |
| **Bimble** | 400 | The full typeface from the same geometry: every printable ASCII character. Short brand lines and big words on the web page. Never UI, headings or running text: Sora and Source Sans 3 do those. |

Need another weight? Copy it from the `@fontsource/<family>` npm package and
add an `@font-face` block to `fonts/fonts.css`. Don't load Google Fonts at
runtime in the app.

## Scale

| Style | Family | Size / line height | Use |
|---|---|---|---|
| display | Sora 700 | 52 / 1.02 | Home, empty states, web hero. One per screen. |
| title | Sora 700 | 38 / 1.1 | Page and sheet titles |
| heading | Sora 700 | 20 / 1.25 | Section headings |
| panel | Sora 500 | 14 / 1.3 | Panel names in the app (Properties, Layers) |
| lead | Source Sans 3 400 | 18 / 1.5 | Intro paragraphs |
| body | Source Sans 3 400 | 16 / 1.5 | Reading text |
| ui | Source Sans 3 400 | 14 / 1.4 | App chrome, property rows, chips, buttons (600 for the main action) |
| small | Source Sans 3 400 | 13 / 1.4 | Captions, help |
| data | DM Mono 400 | 13 / 1.6 | Values with units, IFC classes, GUIDs |
| eyebrow | DM Mono 400 | 12, uppercase, 0.08em | Labels above titles, swatch names |

## The wordmark font

`fonts/bimble-wordmark.woff2` (and `.ttf` for native apps) draws the word
"bimble" in the logo's letters. Use `font-family: var(--bb-font-wordmark)` on
the title and write the word in lower case. The font has no other letters, so
any other text in it falls back to Sora. Never set a sentence in it. The logo
SVGs use the same letters, from the same geometry.

The wordmark maps B, I, M, L and E to the lowercase letters, so "Bimble" also
shows as "bimble". The Bimble typeface has real capitals, digits and
punctuation. It has no accented letters yet. Both fonts carry kerning, as GPOS and as a legacy `kern` table.

## Rules

- **Numbers with units are data**: `250 mm`, `+3 000 mm`, `1:50` in DM Mono. Use a thin space or regular space as thousands separator, as in Swiss/French engineering practice (`3 000`), and always a space before the unit.
- **IFC names stay as written**: `IfcSlab`, `IfcColumn`, in DM Mono.
- **Mixed rows**: label in Source Sans 3 stone, value in ink (DM Mono if it is a measurement).
- **Sentence case** everywhere, including buttons and tabs. Uppercase only for eyebrows.
- **Weights**: don't use Sora below 14px or Source Sans 3 700 (not shipped; 600 is the bold).
- Body text minimum 13px in the app, 16px on the web page; printed body ≥ 9pt on drawings, ≥ 11pt in reports.
