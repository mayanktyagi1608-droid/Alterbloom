# Alterbloom: homepage and site build plan

Status: **design decisions approved. Phase 1 (foundations) built on branch `redesign/foundations`; Phases 2 onward not started.** WhatsApp number deliberately left blank for now (the buttons stay hidden until it is set).
Reference design: board **F, Mobile first** in the "Alterbloom Homepage Directions" artifact.

Goals, in order: **(1) more enquiries, (2) found by search and AI tools, (3) fast on a phone, (4) still easy for the CMS editor to maintain.**

Stack stays as it is: Eleventy 2, Decap CMS, Netlify (`npm run build` to `_site`). No new framework.

---

## 0. Decisions

**Approved by the client:** the section 0.1 additions, teal-always (0.2), service area **London and the wider South East**, and **WhatsApp instead of a Call button**. Still open: section 0.4 facts and the image-package go-ahead.

### 0.1 Design-system change (approved)

`CLAUDE.md` says no new colours, fonts, spacing, radii, shadows or component patterns without explicit sign-off. Board F differs from the approved system in these ways:

| Area | Approved system today | Board F uses | Recommendation |
|---|---|---|---|
| Display type | Work Sans only, "sans-serif only" | **Fraunces** (serif) for headings | New token `--font-display`. Needs approval. |
| Accent type | none | **Caveat** (handwriting) for margin notes, signatures, form fields | New token `--font-hand`. Use sparingly. Needs approval. |
| Body type | Work Sans | Hanken Grotesk | **Keep Work Sans.** No reason to change it. Drops a font family. |
| Teal | `#1E4B54` / deep `#123138` | `#0E4A4F` / `#0A3538` | **Keep existing teal tokens.** No new colour. |
| Coral | Bloom `#E2795F` | `#F0703A` | **Keep Bloom.** Slightly less loud, already approved. |
| Paper cream | Linen `#FAF6EF`, surface `#FFFEFB` | `#FBF6EA` | **Use Linen.** |
| Page ground | Linen by default, teal in dark mode | Teal always, cream "paper" cards on top | **Decision: see 0.2.** |
| Shadows | None. Hairlines only | Soft drop shadows under cards | New token (`--shadow-paper`). The system allows shadows only for "photographed physical objects", so this is a rule change. |
| Rotation | none | Cards tilted 1 to 2 degrees | New component rule. |
| Grain | none | Paper-grain overlay | New token and asset. Optional. |
| Corners | sharp (`--radius:0`) | sharp, except the round wax seal | One-off exception, or make the seal square. |
| Dark text colour for small coral labels | none | `#C2501E` | Needed for contrast (see 0.3). New token. |

**Net effect of the approved recommendations:** colours barely change. The real additions are a serif display font, a script accent font, a paper shadow, tilt and the grain overlay. I'd update `DESIGN_SYSTEM.md` and `css/tokens.css` in one reviewed step, before any page work.

### 0.2 Light or dark default (approved: option A)

The current system is linen by default with an automatic dark mode. Board F is teal-ground only. Options were:
- **A. Teal always** (what F shows): the strongest brand look, with one theme to design and test.
- **B. Keep light and dark:** twice the visual testing, and the invitation and photo bands need a light version.

**Decision: A.** Remove the light and dark switching from `tokens.css` and keep one teal-ground theme.

### 0.3 Contrast fixes

Board F puts coral on cream in places (the "come in, you two." note, the signature, the step numbers). That's about 2.8:1, which fails WCAG for normal text and is borderline for large text. Fix: use the darker coral for any coral text on cream, and keep bright Bloom for fills, the logo full stop and anything on teal. This is the reason for the extra token above.

### 0.4 Facts only you can supply (placeholders in the design)

- Travel policy for events beyond the South East (the FAQ still has a "[Travel policy.]" placeholder). Also confirm which counties count as the South East for your copy and structured data (for example Kent, Surrey, Sussex, Essex, Hertfordshire, Berkshire, Buckinghamshire, Oxfordshire, Hampshire)
- **WhatsApp:** confirm 07752 082523 is on WhatsApp (ideally WhatsApp Business, so you get a business profile, away messages and quick replies) and who answers it
- Google review count and rating, plus 1 to 3 real quotes with permission to name people
- Typical reply time for enquiries
- Typical lead time for booking, and an honest price range or a way to think about cost
- Directory listings you're actually on
- Photo rights for all images, and a **Corporate** photo (none exists yet)
- Final domain (assumed `alterbloom.co.uk`, matching the email address)

---

## 1. Constraints from the existing setup

- **CMS rule:** editable content lives in `src/_data/*.json` or markdown files with front matter, never in a `.njk` template's own front matter. Every new field is a three-file change: data file, `admin/config.yml`, template.
- **No local Node.** I won't install it. Verification is a **Netlify deploy preview on a branch**. Decap commits straight to `main`, so I'll build on a branch and merge only when the preview is approved.
- **Decap previews:** `admin/preview-templates.js` imitates the site. It needs updating alongside any new section so the editor still sees something close to the page.
- **Token check:** `scripts/check-design-tokens.sh` must pass (no raw hex or stray `font-family` outside `tokens.css`).
- **Existing titles:** `base.njk` builds `<title>` as `{{ title }} — Alterbloom`. Per-page SEO titles will override it.

---

## 2. Information architecture

```
/                       Home (the invitation)
/weddings/              Service page
/corporate/             Service page
/celebrations/          Service page
/the-show/              Service page (drag, bhangra, hosts, first dances)
/about/                 Our story
/blog/ and /blog/<slug>/   Journal (exists)
/contact/               Enquiry (also embedded on home)
/thank-you/             Form confirmation (also the conversion goal)
/privacy/  /terms/      exist
/sitemap.xml  /robots.txt
```

Later, once the core is live, niche pages aimed at the searches only you can win: **queer weddings London**, **drag queen wedding host London**, **DIY-friendly wedding decor London**. Each is a service-page template with its own copy, photos and FAQ. Don't start these until the real copy exists, because thin pages would hurt.

Top nav: Weddings, Corporate, Celebrations, The show, Our story, Journal, plus an **Enquire** button. Service area wording throughout: **"London and the South East"**. Footer carries the same links, contact details and the one-sentence "who, what, where" statement.

---

## 3. Build phases

Sizes: S = under a day, M = 1 to 2 days, L = 3 or more. Work happens on one branch with a deploy preview.

### Phase 1: Foundations (M)
1. Update `DESIGN_SYSTEM.md` and `css/tokens.css` as approved in section 0. Run the token check.
2. **Self-host fonts** (committed `.woff2` files in `css/fonts/` or similar, `font-display: swap`, preload the display font). This drops the Google Fonts render-blocking request and needs no Node.
3. New `base.njk`: skip link, sticky header, mobile menu (native `<details>` or a small toggle), thumb bar (**Enquire** and **WhatsApp**, hidden on desktop), per-page `<title>`, meta description, canonical, Open Graph and Twitter tags, and a JSON-LD slot.
4. Layout primitives in `style.css`: section, full-height band (using `100svh`, not the JS-measured height used in the prototype), paper card, tilt modifier, tag, button styles per the new tokens.

### Phase 2: Home page (L)
Sections, in order, as on board F:
1. **Invitation** (`<h1>` is real text inside the card: "Wedding decor & entertainment in London. Refusing Ordinary.")
2. Hero photo with an **Enquire** button
3. Services ("Pull up a chair"), each linking to its service page
4. Entertainment photo pair
5. Proof (story, reviews, quote, directories)
6. Poppy photo band
7. How it works (3 steps)
8. Full-bleed photo with the line
9. Gallery (swipe on phone, columns on desktop)
10. FAQ
11. Journal (latest 3 posts, automatically)
12. Enquiry card

**Invitation behaviour, built as progressive enhancement:**
- Without JavaScript, or with `prefers-reduced-motion`, the page shows the **opened** state (card visible, no scroll animation). The heading and links are always in the HTML.
- With JavaScript and motion allowed, scroll progress drives the flap, card and seal (about 60 lines of vanilla JS in `js/main.js`, one `requestAnimationFrame`, passive scroll listener). "Skip the intro" is always available. The seal button is a real button.
- Verify on a real iPhone and a mid-range Android, because this is the most fragile piece.

**Content model (new fields, all editable):** extend `home.json` and `home` in `admin/config.yml`:
- Invitation: eyebrow, heading line 1, heading accent word, sub-line, margin note
- Photo bands: a list, each with image, alt text (required), caption, focal point (select: top, centre, bottom, left, right). Editors reorder and swap them without touching code.
- Proof: story text and signature, review figure and count, quote and attribution, directory list
- How it works: 3 steps (title, body)
- FAQ: a list (question, answer). The same list feeds the page and the `FAQPage` JSON-LD.

### Phase 3: Service pages (M)
A markdown **folder collection** `src/services/*.md`, the same safe pattern as `src/posts/`. Front matter: title, SEO title, meta description, intro, hero image and alt, gallery, FAQ list, related posts. One shared `service.njk` layout. The home page services list reads from the same collection, so adding a service updates both places. Four pages at launch: Weddings, Corporate, Celebrations, The show.

### Phase 4: Enquiry and tracking (S to M)
1. Enquiry form with **Netlify Forms** (`data-netlify`, honeypot, labelled fields, 48px targets). Fields: names, email or phone, occasion, date and place, "the one thing guests must remember". Redirect to `/thank-you/`. Form notifications go to `info@alterbloom.co.uk`.
2. The same form partial on home and `/contact/`, so one component and one set of fields.
3. **WhatsApp link** `https://wa.me/447752082523?text=…` with a short pre-filled message ("Hi Alterbloom, we'd like to talk about our event."). It's built from a new `whatsapp_number` field in `site.json` and Site Settings in the CMS, with the pre-filled text as a second field, so a change updates the bar, the enquiry card and the footer together. Plain text label "WhatsApp", no green brand colour, in keeping with the design system. The phone number stays in the footer and structured data as plain text and a `tel:` link, because a consistent name, phone and website matters for local search.
4. WhatsApp replies are only as fast as whoever answers. The page promises a reply time, so decide who covers it.
3. **Analytics: cookieless** (Plausible, Netlify Analytics or similar), so no consent banner is needed under UK PECR. Track three events: Enquire click, WhatsApp click, form submit. If you want Google Analytics 4 instead, it needs a cookie consent banner, which is a separate design decision.

### Phase 5: Search and AI visibility (M)
**On every page:** unique `<title>` and meta description (new "SEO title" and "Meta description" CMS fields on each page file, post and service), canonical URL, Open Graph image (default plus per-page override), one `<h1>`, a sensible heading order, descriptive alt text.

**Site-wide:** `sitemap.xml` generated by Eleventy, `robots.txt`, `lang="en-GB"`, clean 301s for any changed URLs (added to `netlify.toml`).

**Structured data (JSON-LD):**
- `ProfessionalService` (or `LocalBusiness`) with `areaServed` listing London and each South East county you serve, phone, email, `sameAs` Instagram. **No street address**, since you're a service-area business.
- `Service` on each service page.
- `FAQPage` where the FAQ is visible. Google now shows FAQ rich results only for a few site types, so treat this as machine-readable clarity, not a promise of rich snippets.
- `BlogPosting` and `BreadcrumbList` on journal posts.
- `AggregateRating` and `Review` **only** when real, visible on the page and matching Google's rules. Never placeholder values.

**Off-site (not code, but it matters most for local ranking):**
- **Google Business Profile** set up as a service-area business covering London and the South East counties you serve (Google allows a limited number of service areas, so choose the ones that matter most).
- Consistent name, phone and website on the directories you actually use.
- A review request routine after every event.

**AI answer engines:** they favour plain, specific, quotable statements. The footer sentence, the FAQ answers, the service page intros and the "how it works" steps are written for this. I would **not** spend time on an `llms.txt` file, since there is no evidence it changes anything.

### Phase 6: Performance and accessibility (M)
**Images:** CMS uploads are arbitrary sizes. Add `@11ty/eleventy-img` (npm dependency, installed by Netlify on build, so I'll ask before adding it) with a shortcode that outputs AVIF and WebP at several widths with `srcset`, `sizes`, `width` and `height`, and lazy-loads everything except the first photo. Hero image: `fetchpriority="high"`.

**Budgets, checked on the deploy preview (Lighthouse, mobile profile):**
- LCP under 2.5 s, CLS under 0.1, INP under 200 ms
- Home page under about 1.5 MB transferred on first load
- Performance score 90 or more on mobile

**Other speed items:** grain as a tiny tiled image (not full-page SVG filter), no layout shift from the sticky bars, fonts preloaded.

**Accessibility:** visible focus on every control, 48px touch targets, `prefers-reduced-motion` honoured, the seal is a labelled button, FAQ via native `<details>`, colour contrast checked on both teal and cream surfaces (see 0.3), required alt text in the CMS wherever an image is chosen, the scroll-driven intro never traps focus or hides content.

### Phase 7: CMS and preview updates (M)
- Add every new field to `admin/config.yml` with friendly labels and hints, so the editor can work without a developer.
- Update `admin/preview-templates.js` to render the new sections.
- Add an editor cheat sheet to the README (3 to 5 lines per task: change a photo, add an FAQ, publish a post).

### Phase 8: QA and launch (S to M)
1. Deploy preview checks: all links, forms deliver an email, `/thank-you/` fires the conversion event, redirects, sitemap, structured data validates (Google Rich Results Test and Schema.org validator).
2. Real-device pass: iPhone Safari, Android Chrome, one small phone (320px), one tablet, desktop. Check the invitation, the thumb bar over the footer, and iOS keyboard behaviour on the form.
3. Merge to `main`. Netlify deploys.
4. Search Console: verify the domain, submit `sitemap.xml`, request indexing for the home and service pages.
5. Rollback plan: Netlify keeps previous deploys, so a bad release can be restored from the Deploys list in one click.

---

## 4. Order of work and dependencies

```
0. Decisions + content  ->  1. Foundations  ->  2. Home  \
                                              3. Services  ->  5. SEO  ->  8. QA + launch
                                              4. Forms     /   6. Perf/a11y, 7. CMS (alongside 2 to 4)
```

Phases 2, 3 and 4 can run in parallel once Phase 1 is done. The slowest dependency is **your content** (section 0.4). I can build with clearly marked placeholders, but nothing with a `[bracket]` should go live.

## 5. Risks

| Risk | Mitigation |
|---|---|
| Invitation animation janks or breaks on some phones | Progressive enhancement, skip link, reduced-motion fallback, real-device testing, and a switch to turn it off if it underperforms |
| Placeholders reach production | Build check: fail the Netlify build if any `[` placeholder pattern appears in rendered HTML |
| Editor breaks layout via CMS | Constrained widgets (selects for focal point, required alt text), previews, no free HTML |
| Heavy images slow the site | Build-time image pipeline and a Lighthouse budget before merge |
| Competitive London keywords | Lead with the niches (queer, drag, bhangra, DIY) and Google Business Profile, not generic "wedding decor". The South East is a good second market with less competition, so give the larger counties their own section or page later |
| Design-system drift | Update the docs and tokens first, then run the token check on every change |

## 6. What I need from you to start

1. The section 0.4 facts (even partial)
2. Go-ahead to add the image dependency in Phase 6
3. Go-ahead to start Phase 1 on a branch (design docs and tokens first)

---

## 7. Photo sources and how to replace them

Originals live in `~/Downloads/Reception Photos` (1,220 untouched files). Web copies go in `src/uploads/` (long edge 2000px, or 1600px for portraits, JPEG quality 80, GPS and camera data stripped). The home page reads photos from CMS image fields, so any photo can be swapped later in `/admin/` without touching code. The files below are just the starting set.

| Web file | Original | Used for (board F) |
|---|---|---|
| `bhangra-crowd.jpg` | `IMG_1836.JPG` | Full-bleed band: "The lights dim..." |
| `necklaces-detail.jpg` | `IMG_0922.JPG` | Gallery |
| `performer-closeup.jpg` | `IMG_1266.JPG` | Entertainment pair, and the show service card |
| `groom-garland.jpg` | `IMG_1961.JPG` | Gallery |
| `performer-pink-skirt.jpg` | `IMG_0908.JPG` | Entertainment pair |
| `hero-grooms-poppies.jpg` | `IMG_1890.JPG` | Hero photograph |
| `grooms-behind-cake.jpg` | `IMG_1679.JPG` | Gallery, weddings service card |
| `poppy-table.jpg` | `IMG_1407.JPG` | Full-bleed band: guests under paper poppies |
| `grooms-dancing.jpg` | `IMG_1594.JPG` | Gallery |
| `cake-with-poppy.jpg` | `IMG_1680.JPG` | Gallery |

Photo rights and consent: confirm everyone recognisable in these photos is happy for them to appear on the public site.
