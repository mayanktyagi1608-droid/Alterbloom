# Alterbloom Design System

Status: **Approved v1** — approved via the "Alterbloom Design System" artifact,
built from the client's own business card (deep teal / sky two-tone, hand-drawn
botanical line art, tracked-caps micro-labels, Montserrat wordmark with a
trailing full stop).

> **Change control:** This document and `css/tokens.css` are the source of
> truth. Don't introduce a new color, font, spacing value, radius, or shadow
> outside of what's listed here — reuse an existing token. If a real design
> need isn't covered by the current system, that's a conversation to have
> with the client first, not a value to invent inline. See `CLAUDE.md` for
> the enforcement rule.

## Direction

Upscale minimalism as the frame, whimsy as the exception: one warm coral
accent, one hand-drawn botanical line, one signature full stop after the
wordmark. Sans-serif only. No true black or pure white anywhere — every
"black" and "white" on the site is tinted from the same teal.

## Color

All values live in `css/tokens.css`. Never hardcode a hex value in HTML or
CSS outside that file — reference the custom property.

### Raw brand swatches (fixed, never theme-swapped)

| Name       | Hex       | Token               | Usage |
|------------|-----------|---------------------|-------|
| Deep Teal  | `#1E4B54` | `--swatch-teal`      | Primary ink, dark-mode ground, primary button fill in light mode |
| Teal Deep  | `#123138` | `--swatch-teal-deep` | Text on Sky surfaces in dark mode; darkest anchor, used sparingly |
| Sky        | `#A9D3DA` | `--swatch-sky`       | Light-mode card face, dark-mode ground panels, tags & dividers |
| Linen      | `#FAF6EF` | `--swatch-linen`     | Light-mode page ground and dark-mode text — never pure white |
| Bloom      | `#E2795F` | `--swatch-bloom`     | The whimsy: logo's full stop, hover states, the botanical line, one tag |

Bloom is the **only** color not literally on the business card. Use it like a
wax seal, not a paint job — logo period, link/button hover, the motif line,
at most one "featured" tag per view.

### Semantic tokens (theme-aware — this is what components actually use)

| Token | Light | Dark | Purpose |
|---|---|---|---|
| `--bg` | Linen | Deep Teal | Page background |
| `--bg-alt` | pale teal wash | slightly lighter teal | Alternating section background |
| `--surface` | near-white | Sky | Card / panel background |
| `--text` | Deep Teal | Linen | Primary text on `--bg` |
| `--text-muted` | muted teal-grey | muted sky | Secondary text on `--bg` |
| `--border` | pale teal-grey | translucent linen | Hairlines on `--bg` |
| `--cta-bg` / `--cta-text` | teal / linen | sky / teal-deep | Primary button, on `--bg` |
| `--accent` | Bloom | brightened Bloom | The one warm spark |

### Surface panels — the rule that's easy to get wrong

Dark mode is not a simple invert: the page background becomes Deep Teal, but
card/panel surfaces become **Sky** (the light card's own color) — so a card's
text needs the *inverse* mapping from the page's text. That's what the
`-on-surface` tokens are for (`--text-on-surface`, `--text-on-surface-muted`,
`--border-on-surface`, `--cta-bg-on-surface`, `--cta-text-on-surface`).

**Any element with `background: var(--surface)` must locally redefine
`--text`, `--text-muted`, `--border`, `--cta-bg`, `--cta-text` to their
on-surface counterparts**, so everything nested inside automatically resolves
correctly instead of inheriting page-level colors calibrated for the wrong
background:

```css
.card{
  background:var(--surface);
  color:var(--text-on-surface);
  --text:var(--text-on-surface);
  --text-muted:var(--text-on-surface-muted);
  --border:var(--border-on-surface);
  --cta-bg:var(--cta-bg-on-surface);
  --cta-text:var(--cta-text-on-surface);
}
```

Skipping this is the single most common mistake — it produces sky-on-sky or
cream-on-cream text that's technically rendered but unreadable in dark mode.

An element whose own background is `var(--bg)` even while nested inside a
surface panel (e.g. a form `<input>`) should NOT inherit the surface
override — give it an explicit page-level token (see `--field-text`) instead
of `var(--text)`.

## Typography

Two fonts, full stop:

- **`--font-logo` (Montserrat, weight 600)** — the wordmark ONLY:
  `Alterbloom.` in sentence case with the trailing period. Never used for
  headings, body, or UI text.
- **`--font-body` (Work Sans)** — every heading, paragraph, button, label,
  and nav item on the site. Weights 400 (body) / 500 / 600 (buttons, labels,
  h2/h3) / 700 (h1/display).

Load both from Google Fonts:

```html
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Work+Sans:wght@400;500;600;700&family=Montserrat:wght@500;600;700&display=swap">
```

Type scale (tokens in `css/tokens.css`): `--fs-display`, `--fs-h1`,
`--fs-h2`, `--fs-h3`, `--fs-body-lg`, `--fs-body`, `--fs-small`,
`--fs-label`. Labels/eyebrows are uppercase with `letter-spacing: 0.12–0.16em`
— this echoes the tracked capitals on the business card ("DESIGNER", phone,
email) and is the site's one recurring typographic signature.

The wordmark is always `Alterbloom.` — capital A, rest lowercase, trailing
period. The period renders in `--accent` (Bloom) as a small logo easter egg.

## Motif

A single-stroke, hand-drawn wildflower, in the spirit of the illustration on
the business card. It is decoration, not a photo substitute — use only as:

- A section divider (small, inline, `--accent` colored)
- A background watermark behind a heading (~8% opacity, `--text` colored)
- A corner detail on an otherwise-empty panel

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

## Shape & spacing

- **Sharp corners everywhere** — `--radius: 0`. No rounded corners on
  buttons, cards, tags, inputs, or images. This matches the crisp edges of
  actual cardstock.
- **Hairline borders, never drop shadows** — `--border-width: 1px` is the
  only separation device for UI. The one exception is a literal photographed
  object (e.g. a business-card mockup) where a soft shadow depicts real
  physical depth — that exception does not extend to ordinary cards/buttons.
- **8px spacing scale** — `--space-1` (8px) through `--space-7` (96px).
  Don't use arbitrary margin/padding values; pick the nearest step.

## Components

- **Buttons** — primary: filled `--cta-bg` / `--cta-text`, sharp corners, no
  shadow, uppercase label, letter-spacing `0.05em`. Secondary: transparent
  fill, 1px border in `--text`, same label treatment.
- **Tags/labels** — 1px border, uppercase, tracked, `--text-muted`; a
  "featured" tag may use `--accent` for its border/text — sparingly (see
  Bloom usage above).
- **Cards** — `--surface` background, 1px `--border`, no shadow, apply the
  surface-panel token overrides above.
- **Forms** — inputs sit on `--bg` (not `--surface`), 1px border, label is
  an uppercase tracked caption in `--text-muted`.
- **Nav** — wordmark left, links right, current page underlined in
  `--accent`.

## Reference

The living visual reference for all of the above is the published
"Alterbloom Design System" artifact (Montserrat + Work Sans version). Consult
it for what things should *look* like; consult `css/tokens.css` for the exact
values to *use*.
