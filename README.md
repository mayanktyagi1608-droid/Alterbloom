# Alterbloom

Website for Alterbloom, an events planning &amp; decor business.

## Status

This is a **black-and-white wireframe** — plain HTML/CSS/JS focused on layout and
structure only. No color, imagery, or brand design has been applied yet. Once the
structure is approved, a design system (colors, type, imagery) will replace this
wireframe styling.

## Pages

- `index.html` — Home
- `about.html` — About
- `services.html` — Services
- `gallery.html` — Portfolio / Gallery
- `testimonials.html` — Testimonials
- `pricing.html` — Pricing / Packages
- `contact.html` — Contact form + info

## Local preview

No build step — just open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8000
```

Then visit `http://localhost:8000`.

## Deploying to GitHub Pages

1. Push this repo to GitHub.
2. In the repo settings, go to **Pages**.
3. Under **Build and deployment**, set **Source** to `Deploy from a branch`.
4. Choose the `main` branch and `/ (root)` folder, then save.
5. The site will be published at `https://<username>.github.io/<repo-name>/`.
