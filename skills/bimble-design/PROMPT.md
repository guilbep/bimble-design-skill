# Bimble design prompt

Paste this into any model, design tool or brief when it has no access to the
skill folder. It is the whole system in one block.

---

You are designing for **Bimble**, an open-source, IFC-based BIM app for
structural and civil engineering offices. Its look is called **"Two discs"**:
the logo's two circles (clay and pink, black letters) become the system.
Warm, friendly, precise. A first open-source BIM tool that doesn't feel like
legacy CAD.

**Ground and ink.** Cream `#F5F2EB` page and panels; white `#FFFFFF` for
cards, paper and the model viewport; `#EDE7DB` for inner dividers and hover;
ink `#141414` for text; stone `#5C574D` for quiet text and control borders;
line `#DDD6C8` for decorative borders only.

**Five colours, one job each. Never use one for anything else.**
- Clay `#C06A41`: **do**. The single main action per view (Place, Save, Export). As text: `#A35A37`.
- Pink `#D7ACB6`: **choose**. Selection only, in the model, on paper, in lists. As text: `#80676D`.
- Moss `#6A8757`: **done**. Saved, in sync, check passed. As text: `#5B744A`.
- Ochre `#D2B347`: **look**. Not saved, borrowed, warnings. Errors are ink text on an ochre band with the word "Error"; there is no red. As text: `#7D6B2A`.
- Slate `#6E88A3`: **other**. Linked models, references, "theirs" in a merge. As text: `#5A6F85`.

Text on any of these fills is always ink `#141414` (all pass WCAG AA), never
white. Never rely on colour alone: every coloured chip has words. Pink and
ochre dots get a 1px ink outline. Chart and linked-model series order: clay,
slate, moss, ochre, pink.

**Type.** The word "bimble" as a title uses Bimble Wordmark, the logo's
letters as a font (only b, i, m, l, e). Sora 700 for display and headings, Sora 500 for panel names.
Source Sans 3 (400, 600, italic) for all reading text and UI. DM Mono for
data: dimensions with units ("250 mm"), IFC classes ("IfcSlab"), GUIDs, and
small uppercase eyebrow labels with 0.08em tracking. Sizes: 52 display,
38 title, 20 heading, 18 lead, 16 body, 14 UI, 13 small, 12 eyebrow.

**Shape.** Round where you touch, square for drawings. Buttons, chips and
tabs are pills. Swatches, status dots and axis bubbles are discs. Cards and
panels 16px radius; inputs 8px. Drawings, sheets, the viewport and tables are
square. 4px spacing scale (4, 8, 12, 16, 24, 32, 40, 56).

**App anatomy.** A top bar on white: the "b" disc icon, then pill tabs
(Project · Model · Annotate · Sheets; the active one is an ink pill with
cream text), then status chips on the right (ochre "Not saved: 2 edits",
slate "Linked: Architecture"), then one clay pill for the main action. A
cream properties panel on the left with Sora 500 title and label/value rows
(stone label, ink value, DM Mono for numbers). A white viewport where the
selected element is pink with an ink outline and linked models are slate
dashed. Status at the panel foot: a pink dot "1 selected", a moss dot
"History: in sync".

**Restraint.** One big decorative disc per screen, only on Home and empty
states, never over work. Drawings print black and white. No gradients, glows,
drop shadows, emoji, or white-on-clay. Icons: 1.5px stroke, ink. Copy is
plain, short and specific: verbs on buttons, nouns with numbers on chips,
engineering vocabulary (slab, storey, C30/37, 1:50).
