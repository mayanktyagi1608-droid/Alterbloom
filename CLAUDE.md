# Alterbloom

Static site (plain HTML/CSS/JS, no build step) for Alterbloom, an events
planning & decor business. Deployed via GitHub Pages from `main` at the repo
root.

## Design system — read before touching any HTML or CSS

`DESIGN_SYSTEM.md` and `css/tokens.css` are the approved design system
(colors, type, spacing, shape, components), built from the client's business
card and signed off via the "Alterbloom Design System" artifact.

**Hard rule: do not change colors, fonts, spacing values, radii, shadows, or
component patterns from what's already in `css/tokens.css` /
`DESIGN_SYSTEM.md`, and do not introduce new ones inline, without first
discussing it explicitly with the user in conversation and getting their
go-ahead.** This applies even if a value would look better, is a "small"
tweak, or seems obviously implied by a request — if it's not already a
token, stop and ask before adding it as one.

What this means in practice:

- Never hardcode a hex color, `font-family`, `border-radius`, or `box-shadow`
  in a page or stylesheet — use the custom properties from `css/tokens.css`
  (`var(--text)`, `var(--accent)`, etc.).
- Any new component that has its own `background: var(--surface)` must
  locally redefine `--text`, `--text-muted`, `--border`, `--cta-bg`,
  `--cta-text` to their `-on-surface` equivalents — see "Surface panels" in
  `DESIGN_SYSTEM.md`. This is the one rule that's easy to silently violate.
- Reuse the existing botanical-motif SVG path data verbatim (in
  `DESIGN_SYSTEM.md`) rather than drawing a new illustration.
- Before committing a UI change, run `scripts/check-design-tokens.sh` — it
  flags raw hex colors and stray `font-family` declarations outside
  `css/tokens.css`.
- If the user's request genuinely needs something outside the current
  system (a new color, a new font, rounded corners, a shadow), say so and
  ask, rather than quietly adding it.

## Site structure

- `index.html`, `about.html`, `blog.html` (+ `blog-post.html` template),
  `contact.html`, `privacy.html`, `terms.html` — top-nav is Home / About /
  Blog / Contact; Privacy/Terms live in the footer only.
- `css/style.css` — current (wireframe-era) layout styles.
- `css/tokens.css` — design tokens; load this before `style.css` once the
  site is restyled from the black-and-white wireframe to the approved system.
- `js/main.js` — mobile nav toggle, gallery-style filter helper, contact
  form placeholder handler.

## Local preview

```bash
python3 -m http.server 8000
```
