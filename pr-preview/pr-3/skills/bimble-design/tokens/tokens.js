// Bimble design tokens as an ES module (for Vue/JS themes, charts, canvas/WebGL viewers).
// Mirrors tokens.json and tokens.css.

export const color = {
  cream: '#F5F2EB', sheet: '#FFFFFF', sunk: '#EDE7DB',
  ink: '#141414', stone: '#5C574D', line: '#DDD6C8', onInk: '#F5F2EB',
  clay:  { fill: '#C06A41', text: '#A35A37' }, // do
  pink:  { fill: '#D7ACB6', text: '#80676D' }, // choose
  moss:  { fill: '#6A8757', text: '#5B744A' }, // done
  ochre: { fill: '#D2B347', text: '#7D6B2A' }, // look
  slate: { fill: '#6E88A3', text: '#5A6F85' }, // other
};

export const role = {
  action: color.clay.fill,
  link: color.clay.text,
  selection: color.pink.fill,
  success: color.moss.fill,
  attention: color.ochre.fill,
  error: color.ochre.fill, // always paired with the word "Error"
  reference: color.slate.fill,
};

/** Charts and linked models, in this order. */
export const series = [color.clay.fill, color.slate.fill, color.moss.fill, color.ochre.fill, color.pink.fill];

export const font = {
  display: "'Sora', 'Source Sans 3', 'Helvetica Neue', Arial, sans-serif",
  text: "'Source Sans 3', 'Helvetica Neue', Arial, sans-serif",
  data: "'DM Mono', ui-monospace, Menlo, monospace",
  wordmark: "'Bimble Wordmark', 'Sora', sans-serif", // the word bimble only
  bimble: "'Bimble', 'Sora', sans-serif", // brand lines, big words; printable ASCII
};

export const radius = { none: 0, sm: 8, md: 16, pill: 999 };
export const space = [0, 4, 8, 12, 16, 24, 32, 40, 56];

export default { color, role, series, font, radius, space };
