# Alterbloom Design System

Status: **Approved v2 ("Invitation")**. v1 was approved via the "Alterbloom
Design System" artifact, built from the client's own business card (deep teal
/ sky two-tone, hand-drawn botanical line art, tracked-caps micro-labels,
Montserrat wordmark with a trailing full stop). v2 was approved by the client
for the mobile-first redesign (boards E and F in the "Alterbloom Homepage
Directions" artifact): one teal-ground theme, cream paper surfaces, a serif
display face, a handwriting accent, and a paper shadow and tilt.

> **Change control:** This document and `css/tokens.css` are the source of
> truth. Don't introduce a new color, font, spacing value, radius, or shadow
> outside of what's listed here — reuse an existing token. If a real design
> need isn't covered by the current system, that's a conversation to have
> with the client first, not a value to invent inline. See `CLAUDE.md` for
> the enforcement rule.

## Direction

Upscale minimalism as the frame, handmade whimsy as the exception: a deep
teal ground, cream "paper" cards that look like stationery on a table, one
warm coral accent, one hand-drawn botanical line, one signature full stop
after the wordmark. Mobile first: the phone layout is the design, and larger
screens add columns. No true black or pure white anywhere — every "black"
and "white" on the site is tinted from the same teal or linen.

There is **one theme**: teal ground, linen paper. There is no light/dark
switch.

## Color

All values live in `css/tokens.css`. Never hardcode a hex value in HTML or
CSS outside that file — reference the custom property. (The one allowed
exception is the `<meta name="theme-color">` tag, which cannot read a CSS
variable.)

### Raw brand swatches (fixed)

| Name       | Hex       | Token               | Usage |
|------------|-----------|---------------------|-------|
| Deep Teal  | `#1E4B54` | `--swatch-teal`      | Ink on paper, primary button on paper |
| Teal Deep  | `#123138` | `--swatch-teal-deep` | Header, footer, photo-band fallback (`--bg-deep`); text on coral buttons |
| Sky        | `#A9D3DA` | `--swatch-sky`       | Tags and dividers, sparingly |
| Linen      | `#FAF6EF` | `--swatch-linen`     | The paper: cards, panels, forms (`--surface`) |
| Bloom      | `#E2795F` | `--swatch-bloom`     | The raw brand coral (the card). On screen use the brightened `--accent` |

Coral is the only color not literally on the business card. Use it like a
wax seal: the lead button, the logo's full stop, the botanical line, link
underlines, the seal on the invitation.

### Semantic tokens (this is what components actually use)

| Token | Value | Purpose |
|---|---|---|
| `--bg` | deep teal `#17383F` | Page ground |
| `--bg-alt` | lighter teal | Alternating section background |
| `--bg-deep` | Teal Deep | Header, footer, photo bands |
| `--surface` | Linen | Paper: cards, panels |
| `--text` / `--text-muted` | cream / pale sky | Text on `--bg` |
| `--border` | translucent cream | Hairlines on `--bg` |
| `--cta-bg` / `--cta-text` | coral / Teal Deep | The lead button (Enquire) on `--bg` |
| `--accent` | brightened coral | The one warm spark on teal |
| `--text-on-surface`, `--text-on-surface-muted`, `--border-on-surface`, `--cta-bg-on-surface`, `--cta-text-on-surface`, `--accent-on-surface` | teal inks and a deeper coral | Everything on paper |

### Surface panels — the rule that's easy to get wrong

Paper is light on a dark page, so its text needs the *inverse* mapping from
the page's text. **Any element with `background: var(--surface)` must locally
redefine `--text`, `--text-muted`, `--border`, `--cta-bg`, `--cta-text` and
`--accent` to their on-surface counterparts**, so everything nested inside
resolves correctly:

```css
.card{
  background:var(--surface);
  color:var(--text-on-surface);
  --text:var(--text-on-surface);
  --text-muted:var(--text-on-surface-muted);
  --border:var(--border-on-surface);
  --cta-bg:var(--cta-bg-on-surface);
  --cta-text:var(--cta-text-on-surface);
  --accent:var(--accent-on-surface);
}
```

`.card`, `.paper` and `.cta-banner` already do this; reuse them. Skipping it
produces cream-on-cream text that renders but cannot be read.

An element whose own background is `var(--bg)` even while nested inside a
paper panel (e.g. a form `<input>`) should NOT inherit the surface override —
give it an explicit page-level token (see `--field-text`).

### Contrast rules

- **Coral text on paper** must use `--accent-on-surface` (that is what
  `--accent` becomes inside a paper component). Bright coral on cream is
  about 2.8:1 and fails.
- **Coral text on the teal ground** is for large text and decoration only.
  Small text on the ground uses `--text` or `--text-muted`.
- The coral lead button uses `--cta-text` (Teal Deep): about 5.9:1.

## Typography

Four faces, each with one job. All are self-hosted (`css/fonts/`, declared
in `css/tokens.css`) — do not add a Google Fonts link.

- **`--font-logo` (Montserrat, weight 600)** — the wordmark ONLY:
  `Alterbloom.` in sentence case with the trailing period, period in coral.
- **`--font-display` (Fraunces, weights 300–600, with italic)** — every
  heading and large pull-line. Tight tracking (`-0.035em`), line-height about
  1. Italic is for one emphasised word, not whole lines.
- **`--font-body` (Work Sans, 400–700)** — body copy, buttons, labels, nav
  on desktop, forms.
- **`--font-hand` (Caveat, 600)** — margin notes, signatures, and nothing
  else. Never below `--fs-hand` (1.75rem), never for anything a visitor
  must read to complete a task, and at most a few per page.

Type scale (tokens in `css/tokens.css`): `--fs-display`, `--fs-h1`,
`--fs-h2`, `--fs-h3`, `--fs-body-lg`, `--fs-body`, `--fs-small`,
`--fs-label`, `--fs-hand`. Labels/eyebrows are uppercase with
`letter-spacing: 0.12–0.16em` — the site's recurring typographic signature.

## Motif

A single-stroke, hand-drawn wildflower, in the spirit of the illustration on
the business card. It is decoration, not a photo substitute — use only as:

- A section divider (small, inline, `--accent` colored)
- A background watermark behind a heading (~8% opacity, `--text` colored)
- A corner detail on an otherwise-empty panel
- The mark on the plate illustration

Never redraw a new illustration ad hoc — reuse this exact path data so the
motif stays consistent everywhere it appears:

```svg
<svg viewBox="0 0 120 150" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round">
  <path d="M60 140 C 58 100, 66 80, 60 55"/>
  <path d="M60 90 C 45 84, 38 92, 34 84"/>
  <path d="M62 100 C 76 96, 80 106, 88 100"/>
  <ellipse cx="60" cy="40" rx="10" ry="16" transform="rotate(-18 60 40)"/>
  <ellipse cx="60" cy="40" rx="10" ry="16" transform="rotate(18 60 40)"/>
  <ellipse cx="60" cy="34" rx="10" ry="16"/>
  <ellipse cx="60" cy="42" rx="9" ry="15" transform="rotate(-42 60 42)"/>
  <ellipse cx="60" cy="42" rx="9" ry="15" transform="rotate(42 60 42)"/>
</svg>
```

## Shape, paper and spacing

- **Sharp corners everywhere** — `--radius: 0`. The one exception is the
  round wax seal on the invitation.
- **Hairlines for ordinary UI.** `--border-width: 1px` separates sections,
  inputs, tags and buttons.
- **Paper is the physical-object treatment.** Cards, notes, the RSVP card and
  journal cards are "paper on a table": `--shadow-paper` (large) or
  `--shadow-note` (small caption slips) and an optional tilt of `--tilt-a` /
  `--tilt-b` (about one degree). Don't put shadows on buttons, inputs, tags
  or text, and don't tilt anything with a form control in it that a visitor
  must read quickly.
- **Grain.** `body::before` lays one small tiled noise over the page
  (`--grain`, `--grain-opacity`). It is switched off for
  `prefers-reduced-data`.
- **8px spacing scale** — `--space-1` (8px) through `--space-7` (96px).
  Don't use arbitrary margin/padding values; pick the nearest step.
- **Touch.** Every control is at least `--tap` (48px) tall. Inputs are 16px or
  larger so iOS doesn't zoom.

## Components

- **Buttons** — primary (lead): filled `--cta-bg` / `--cta-text`, sharp
  corners, no shadow, uppercase label, tracked. Secondary: transparent fill,
  1px border in `--text`, same label treatment. On paper the primary flips to
  teal fill automatically.
- **Mobile bar** (`.thumb-bar`) — fixed at the bottom on screens up to 860px:
  **Enquire** (lead) plus **WhatsApp** when a number is set in Site
  Settings. Hidden above 860px, where the header carries Enquire.
- **Tags/labels** (`.tag`) — 1px border, uppercase, tracked, `--text-muted`.
- **Cards and paper** (`.card`, `.paper`) — `--surface` background with the
  surface-panel remap above. `.paper` adds the paper shadow; `.tilt-a` /
  `.tilt-b` add the tilt.
- **Notes** (`.note`) — the handwriting accent, in `--accent`.
- **Photo bands** (`.band`) — full-bleed, one screen tall (`100svh`),
  photograph covers the band, focal point set per image via `--focus`.
  A `.band-caption` is a tilted paper slip.
- **Forms** — inputs sit on `--bg` (not `--surface`), 1px border, label is
  an uppercase tracked caption in `--text-muted`.
- **Nav** — wordmark left. On phones, a Menu button opens a list in the
  display face. From 861px, links sit right in tracked caps with the current
  page underlined in `--accent` and an **Enquire** button last.

## Reference

The living visual reference for the direction is board F ("Mobile first") in
the published "Alterbloom Homepage Directions" artifact. Consult it for what
things should *look* like; consult `css/tokens.css` for the exact values to
*use*.
