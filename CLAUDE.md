# Alterbloom

Events planning & decor business site. Built with **Eleventy** (static site
generator) and edited through **Decap CMS** at `/admin/`, hosted on
**Netlify** (build command `npm run build`, publish dir `_site`, config in
`netlify.toml`). GitHub Pages is no longer used — GitHub is still where the
code and its history live, but Netlify builds and serves the actual site.

## CMS architecture — read before touching anything in `src/`

The client's husband edits the site through the Decap CMS admin panel
(`/admin/`, config in `admin/config.yml`), which commits directly to `main`
via Netlify Identity + Git Gateway. This imposes one hard constraint:

**Never put editable content in a `.njk` template's own front matter.**
Decap's file-based collections rewrite the *entire target file* on save. If
`admin/config.yml` pointed at `src/index.njk` directly, saving a text edit
in the CMS would delete all the Nunjucks/HTML markup below the front-matter
fence. This is why editable content lives in plain data files instead:

- `src/_data/home.json`, `about_page.json`, `contact_page.json`,
  `blog_page.json`, `site.json` — pure JSON, no markup. Templates
  (`src/index.njk`, `about.njk`, `contact.njk`, `blog.njk`, `_includes/
  base.njk`) read from these as global data (e.g. `{{ home.hero_lead }}`,
  `{{ about_page.story_heading }}`, `{{ site.email }}`). `site.json` is
  shared site-wide (footer + contact page) so a phone/email edit updates
  everywhere at once.
- `src/posts/*.md` — one file per blog post, front matter (title, date,
  category, excerpt, cover_image) + a markdown body. This one's safe to
  point Decap at directly because the front matter + markdown body *is*
  the entire editable content — there's no template code in the file
  itself (that lives in `_includes/post.njk`). `src/posts/posts.json` is an
  Eleventy directory-data file (sets `layout`/`permalink`/`tags` for every
  post) — it is not a post; the CMS blog collection is restricted to
  `extension: "md"` specifically so it never shows up as one.
- `src/privacy.md`, `src/terms.md` — same safe pattern: front matter +
  markdown body, layout lives separately in `_includes/legal.njk`.

**Adding a new editable field is a three-file change, always together:**
add the key to the relevant `_data/*.json` (or post front matter), add the
matching field to `admin/config.yml`, and reference it in the `.njk`
template. Do this without discussing it with the user first only for
straightforward wording/content-shape additions the user explicitly asked
for — anything that changes layout still falls under the design-system rule
below.

Images: CMS image fields upload into `src/uploads/`, served from `/uploads/`
(passthrough copy in `.eleventy.js`). Templates check `{% if
home.hero_image %}` and fall back to the on-brand placeholder graphic when
empty, so the site looks right before any real photos are uploaded.

## Local development

No Node is installed in this environment (do not download/install one
yourself — ask the user). If Node is available:

```bash
npm install
npm run build      # outputs to _site/
npm start          # eleventy --serve, local preview with live reload
```

Netlify runs `npm run build` on every push to `main`; that's the real
verification path when local Node isn't available.

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

- `src/index.njk`, `about.njk`, `contact.njk`, `blog.njk` + `src/privacy.md`,
  `terms.md` — page templates/content. `src/_includes/base.njk` (shared
  header/nav/footer), `post.njk` and `legal.njk` (layouts). Top-nav is Home /
  About / Blog / Contact; Privacy/Terms live in the footer only.
- `src/posts/*.md` — blog posts (Eleventy collection, tag `posts`).
- `src/_data/` — editable page content (see CMS architecture above) plus
  `site.json` (global contact/social info).
- `css/tokens.css`, `css/style.css`, `js/main.js` — still root-level,
  passthrough-copied into the Eleventy build. Same design-token rules as
  above apply regardless of the templating layer.
