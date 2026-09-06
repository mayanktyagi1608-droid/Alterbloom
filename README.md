# Alterbloom

Website for Alterbloom, an events planning &amp; decor business.

## Stack

- **[Eleventy](https://www.11ty.dev/)** — static site generator. Templates
  and content live in `src/`, built to `_site/`.
- **[Decap CMS](https://decapcms.org/)** — content editor at `/admin/`,
  authenticated via Netlify Identity + Git Gateway. Commits go straight to
  this repo's `main` branch.
- **[Netlify](https://www.netlify.com/)** — hosting. Builds and deploys
  automatically on every push to `main`.

GitHub remains the permanent home of the code and all its history — Netlify
just builds and serves whatever's on `main`; it doesn't store anything on
its own.

## Structure

See `CLAUDE.md` for the full content/CMS architecture (how editable content
is split from templates so the CMS can never corrupt page layout) and
`DESIGN_SYSTEM.md` for the approved colors/type/spacing system.

- `src/*.njk`, `src/_includes/` — page templates and shared layout.
- `src/posts/*.md` — blog posts.
- `src/_data/*.json` — editable page content, edited through the CMS.
- `css/`, `js/` — stylesheets and scripts, passthrough-copied into the build.
- `admin/` — Decap CMS config and custom preview templates.

## Local development

Requires [Node.js](https://nodejs.org/).

```bash
npm install
npm run build      # outputs to _site/
npm start          # local preview with live reload
```

## Deployment

Push to `main` — Netlify builds and deploys automatically (config in
`netlify.toml`). No manual deploy step.
