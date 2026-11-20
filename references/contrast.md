# Contrast

WCAG 2.x ratios, computed from `tokens/tokens.json` by
`scripts/check-contrast.py` (run it after any colour change; it exits 1 on a
failure).

| Pair | Ratio | |
|---|---|---|
| Ink on clay fill | 4.72 | AA |
| Ink on pink fill | 9.18 | AA |
| Ink on moss fill | 4.58 | AA (closest to the limit: don't lighten moss) |
| Ink on ochre fill | 9.02 | AA |
| Ink on slate fill | 5.01 | AA |
| Clay / pink / moss / ochre / slate text on cream | 4.61 / 4.61 / 4.65 / 4.69 / 4.64 | AA |
| Same on sheet | 5.15 / 5.15 / 5.20 / 5.24 / 5.19 | AA |
| Ink on cream | 16.48 | AAA |
| Stone on cream | 6.42 | AA |
| Stone border on sheet | 7.18 | ≥ 3 for UI edges |

Fills against cream (non-text contrast, needs 3:1 when the shape alone
carries meaning): clay 3.49, moss 3.60, slate 3.29 pass; **pink 1.79 and
ochre 1.83 don't**, hence the 1px ink outline on pink and ochre dots and
swatches. Line `#DDD6C8` is 1.29 on cream: decoration only.
