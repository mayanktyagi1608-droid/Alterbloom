// Custom Decap CMS preview panes — reuse the real site CSS (tokens.css +
// style.css) so editors see something close to the actual page, not a
// generic field dump.
//
// Written with the `h` (hyperscript) and `createClass` globals that
// decap-cms.js exposes on window, deliberately avoiding JSX/Babel — this
// project has no JS build step, and mixing a separately-loaded React with
// the React bundled inside decap-cms.js is a common source of preview
// pane crashes that are hard to debug without a local dev environment.

(function () {
  var h = window.h;

  CMS.registerPreviewStyle("/css/tokens.css");
  CMS.registerPreviewStyle("/css/style.css");
  CMS.registerPreviewStyle("/css/sections.css");

  function wordmark() {
    return h("span", { className: "logo wordmark" }, "Alterbloom", h("span", { className: "dot" }, "."));
  }

  function siteChrome(children) {
    return h(
      "div",
      null,
      h(
        "header",
        { className: "site-header" },
        h(
          "div",
          { className: "container nav-row" },
          wordmark(),
          h(
            "nav",
            { className: "site-nav" },
            h(
              "ul",
              null,
              h("li", null, h("a", null, "Our story")),
              h("li", null, h("a", null, "Journal")),
              h("li", { className: "nav-cta" }, h("a", null, "Enquire"))
            )
          )
        )
      ),
      h("main", null, children)
    );
  }

  function pageHero(eyebrow, heading, body) {
    return h(
      "section",
      { className: "page-hero" },
      h(
        "div",
        { className: "container" },
        h("span", { className: "eyebrow" }, eyebrow),
        h("h1", null, heading),
        h("p", null, body)
      )
    );
  }

  function imageOrPlaceholder(src, getAsset, className, label) {
    if (src) {
      return h("img", { className: className, src: getAsset(src), style: { objectFit: "cover" } });
    }
    return h("div", { className: className }, h("span", null, label));
  }

  function bandImage(p, getAsset, label) {
    p = p || {};
    var focus = (typeof p.focus_x === "number" ? p.focus_x : 50) + "% " + (typeof p.focus_y === "number" ? p.focus_y : 50) + "%";
    if (p.image) {
      return h("img", { src: getAsset(p.image), alt: p.alt || "", style: { "--focus": focus } });
    }
    return h("div", { className: "band-placeholder" }, h("span", null, label));
  }

  function photoBand(p, getAsset, label, extraClass, key) {
    p = p || {};
    return h(
      "section",
      { className: "band " + (extraClass || ""), key: key },
      bandImage(p, getAsset, label),
      p.caption ? h("div", { className: "band-caption note" }, p.caption) : null
    );
  }

  var HomePreview = window.createClass({
    render: function () {
      var d = this.props.entry.getIn(["data"]).toJS();
      var getAsset = this.props.getAsset;
      var inv = d.invitation || {};
      var svc = d.services || {};
      var proof = d.proof || {};
      var how = d.how || {};
      var faq = d.faq || {};
      var enq = d.enquiry || {};
      return siteChrome([
        // The scroll-open envelope can't run in a preview, so the editor sees the opened card.
        h(
          "section",
          { className: "invite", key: "invite" },
          h(
            "div",
            { className: "invite-stage" },
            h(
              "div",
              { className: "env" },
              h(
                "div",
                { className: "env-card" },
                h(
                  "h1",
                  null,
                  h("span", { className: "env-eyebrow" }, inv.eyebrow),
                  h("span", { className: "env-title" }, inv.title + " ", h("em", null, inv.title_accent))
                ),
                h("p", { className: "env-lead" }, inv.lead),
                h("div", { className: "note env-note" }, inv.note)
              )
            )
          )
        ),
        photoBand(d.hero, getAsset, "Opening photo", "band-hero", "hero"),
        h(
          "section",
          { className: "section services", key: "services" },
          h(
            "div",
            { className: "container" },
            h("div", { className: "section-head center" }, h("span", { className: "eyebrow" }, svc.eyebrow), h("h2", null, svc.heading)),
            h(
              "div",
              { className: "paper menu-card" },
              h("div", { className: "menu-label" }, svc.menu_label),
              h(
                "ul",
                { className: "svc-list" },
                (svc.items || []).map(function (it, i) {
                  return h(
                    "li",
                    { key: i },
                    h(
                      "div",
                      { className: "svc" },
                      it.image
                        ? h("img", { className: "svc-thumb", src: getAsset(it.image), alt: "" })
                        : h("span", { className: "svc-thumb svc-thumb-empty" }, "Photo soon"),
                      h(
                        "span",
                        { className: "svc-text" },
                        h("span", { className: "svc-title" }, it.title),
                        h("span", { className: "svc-body" }, it.body)
                      )
                    )
                  );
                })
              ),
              h("div", { className: "note menu-note" }, svc.note)
            )
          )
        ),
        h(
          "section",
          { className: "duo", key: "show" },
          ((d.show || {}).photos || []).map(function (p, i) {
            return h("div", { className: "band", key: i }, bandImage(p, getAsset, "Entertainment photo"), p.caption ? h("div", { className: "band-caption note" }, p.caption) : null);
          })
        ),
        h(
          "section",
          { className: "section proof", key: "proof" },
          h(
            "div",
            { className: "container" },
            h("div", { className: "section-head" }, h("span", { className: "eyebrow" }, proof.eyebrow), h("h2", null, proof.heading)),
            h(
              "div",
              { className: "proof-grid" },
              h("div", { className: "letter tilt-a" }, h("p", { className: "letter-text note" }, proof.story), h("p", { className: "letter-sign note" }, proof.signature)),
              h(
                "div",
                { className: "proof-side" },
                h("div", { className: "paper review-card" }, h("div", { className: "menu-label" }, proof.review_label), h("div", { className: "review-headline" }, proof.review_headline), h("p", { className: "review-note" }, proof.review_note)),
                h("figure", { className: "paper quote-card" }, h("blockquote", null, "“" + (proof.quote || "") + "”"), h("figcaption", null, proof.quote_by))
              )
            )
          )
        ),
        photoBand(d.poppies, getAsset, "Poppies photo", "", "poppies"),
        h(
          "section",
          { className: "section", key: "how" },
          h(
            "div",
            { className: "container" },
            h("div", { className: "section-head" }, h("h2", null, how.heading), h("p", null, how.intro)),
            h(
              "ol",
              { className: "steps" },
              (how.steps || []).map(function (s, i) {
                return h("li", { className: "paper step", key: i }, h("span", { className: "note step-num" }, i + 1), h("h3", null, s.title), h("p", null, s.body));
              })
            )
          )
        ),
        h(
          "section",
          { className: "band band-statement", key: "statement" },
          bandImage(d.statement, getAsset, "Statement photo"),
          h("div", { className: "band-dim" }),
          h("p", { className: "statement" }, ((d.statement || {}).text || "") + " ", h("em", null, (d.statement || {}).accent))
        ),
        h(
          "section",
          { className: "section", key: "faq" },
          h(
            "div",
            { className: "container" },
            h("div", { className: "section-head" }, h("h2", null, faq.heading), h("p", null, faq.intro)),
            h(
              "div",
              { className: "faq" },
              (faq.items || []).map(function (f, i) {
                return h("details", { className: "faq-item", key: i, open: true }, h("summary", null, h("span", null, f.question)), h("p", null, f.answer));
              })
            )
          )
        ),
        h(
          "section",
          { className: "section", key: "enquiry" },
          h(
            "div",
            { className: "container" },
            h(
              "div",
              { className: "paper rsvp" },
              h("div", { className: "rsvp-inner" }, h("div", { className: "menu-label center" }, enq.kicker), h("h2", null, enq.heading), h("p", { className: "rsvp-intro" }, enq.intro), h("span", { className: "btn btn-primary rsvp-send" }, enq.button))
            )
          )
        ),
      ]);
    },
  });

  var AboutPreview = window.createClass({
    render: function () {
      var d = this.props.entry.getIn(["data"]).toJS();
      var getAsset = this.props.getAsset;
      var pic = d.story_image ? getAsset(d.story_image).toString() : "/img/portrait-640.webp";
      return siteChrome([
        h(
          "section",
          { className: "story-open", key: "story" },
          h(
            "div",
            { className: "container story-grid" },
            h("div", { className: "story-head" }, h("span", { className: "eyebrow" }, d.hero_eyebrow), h("h1", null, d.hero_heading)),
            h(
              "figure",
              { className: "paper portrait tilt-a" },
              h("span", { className: "tape" }),
              h("img", { src: pic, alt: "" })
            ),
            h(
              "div",
              { className: "story-words" },
              h("p", null, d.story_body_1),
              h("p", null, d.story_body_2),
              d.story_body_3 ? h("p", null, d.story_body_3) : null,
              h("p", { className: "note story-sign" }, d.signature)
            )
          )
        ),
        photoBand(d.band, getAsset, "Photo from the wedding", "", "band"),
        h(
          "section",
          { className: "section", key: "values" },
          h(
            "div",
            { className: "container" },
            h("div", { className: "section-head" }, h("span", { className: "eyebrow" }, d.values_eyebrow), h("h2", null, d.values_heading)),
            h(
              "div",
              { className: "grid grid-3" },
              (d.values || []).map(function (v, i) {
                return h("div", { className: "card", key: i }, h("h3", null, v.title), h("p", null, v.body));
              })
            )
          )
        ),
        h(
          "section",
          { className: "section", key: "team" },
          h(
            "div",
            { className: "container" },
            h("div", { className: "section-head" }, h("span", { className: "eyebrow" }, d.team_eyebrow), h("h2", null, d.team_heading)),
            h(
              "div",
              { className: "grid grid-2" },
              (d.team || []).map(function (m, i) {
                return h(
                  "div",
                  { className: "card person", key: i },
                  m.photo ? h("img", { className: "person-photo", src: getAsset(m.photo).toString(), alt: "" }) : null,
                  h("h3", null, m.name),
                  h("p", null, m.role)
                );
              })
            )
          )
        ),
        h(
          "section",
          { className: "section", key: "cta" },
          h(
            "div",
            { className: "container" },
            h(
              "div",
              { className: "cta-banner" },
              h("h2", null, d.cta_heading),
              h("p", null, d.cta_body),
              h("span", { className: "btn btn-primary" }, "Enquire")
            )
          )
        ),
      ]);
    },
  });

  var SimpleHeroPreview = window.createClass({
    render: function () {
      var d = this.props.entry.getIn(["data"]).toJS();
      return siteChrome([pageHero(d.hero_eyebrow, d.hero_heading, d.hero_body)]);
    },
  });

  var LegalPreview = window.createClass({
    render: function () {
      var d = this.props.entry.getIn(["data"]).toJS();
      return siteChrome([
        pageHero("Legal", d.title, "Last updated: " + d.updated_date),
        h(
          "section",
          { className: "section", key: "body" },
          h("div", { className: "container" }, h("div", { className: "paper sheet prose" }, this.props.widgetFor("body")))
        ),
      ]);
    },
  });

  var BlogPostPreview = window.createClass({
    render: function () {
      var d = this.props.entry.getIn(["data"]).toJS();
      var dateStr = d.date ? new Date(d.date).toLocaleDateString() : "";
      return siteChrome([
        h(
          "section",
          { className: "page-hero", key: "hero" },
          h(
            "div",
            { className: "container" },
            h("span", { className: "eyebrow" }, d.category + " · " + dateStr),
            h("h1", null, d.title)
          )
        ),
        h(
          "section",
          { className: "section", key: "body" },
          h(
            "div",
            { className: "container" },
            d.cover_image
              ? h("figure", { className: "paper print tilt-b" }, h("span", { className: "tape" }), h("img", { src: this.props.getAsset(d.cover_image).toString(), alt: d.cover_image_alt || "" }))
              : null,
            h("div", { className: "paper sheet prose" }, this.props.widgetFor("body"))
          )
        ),
      ]);
    },
  });

  CMS.registerPreviewTemplate("home", HomePreview);
  CMS.registerPreviewTemplate("about", AboutPreview);
  CMS.registerPreviewTemplate("contact", SimpleHeroPreview);
  CMS.registerPreviewTemplate("blog_intro", SimpleHeroPreview);
  CMS.registerPreviewTemplate("privacy", LegalPreview);
  CMS.registerPreviewTemplate("terms", LegalPreview);
  CMS.registerPreviewTemplate("blog", BlogPostPreview);
})();
