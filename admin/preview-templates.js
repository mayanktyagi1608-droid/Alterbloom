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

  CMS.registerPreviewStyle(
    "https://fonts.googleapis.com/css2?family=Work+Sans:wght@400;500;600;700&family=Montserrat:wght@500;600;700&display=swap"
  );
  CMS.registerPreviewStyle("/css/tokens.css");
  CMS.registerPreviewStyle("/css/style.css");

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
              h("li", null, h("a", null, "Home")),
              h("li", null, h("a", null, "About")),
              h("li", null, h("a", null, "Blog")),
              h("li", null, h("a", null, "Contact"))
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

  var HomePreview = window.createClass({
    render: function () {
      var d = this.props.entry.getIn(["data"]).toJS();
      var getAsset = this.props.getAsset;
      return siteChrome([
        h(
          "section",
          { className: "hero", key: "hero" },
          h(
            "div",
            { className: "container hero-grid" },
            h(
              "div",
              null,
              h("span", { className: "eyebrow" }, d.hero_eyebrow),
              h("h1", { className: "wordmark" }, "Alterbloom", h("span", { className: "dot" }, ".")),
              h("p", { className: "lead" }, d.hero_lead),
              h(
                "div",
                { className: "btn-row" },
                h("span", { className: "btn btn-primary" }, "Get a Quote"),
                h("span", { className: "btn" }, "About Us")
              )
            ),
            imageOrPlaceholder(d.hero_image, getAsset, "img-placeholder hero", "Hero Image — 1200×900")
          )
        ),
        h(
          "section",
          { className: "section", key: "services" },
          h(
            "div",
            { className: "container" },
            h(
              "div",
              { className: "section-head center" },
              h("span", { className: "eyebrow" }, "What We Do"),
              h("h2", null, "Planning & decor, start to finish")
            ),
            h(
              "div",
              { className: "grid grid-3" },
              (d.services || []).map(function (s, i) {
                return h(
                  "div",
                  { className: "card", key: i },
                  h("span", { className: "num" }, i + 1),
                  h("h3", null, s.title),
                  h("p", null, s.body)
                );
              })
            )
          )
        ),
        h(
          "section",
          { className: "section", key: "about" },
          h(
            "div",
            { className: "container" },
            h(
              "div",
              { className: "grid grid-2", style: { alignItems: "center" } },
              imageOrPlaceholder(d.about_image, getAsset, "img-placeholder tall", "Studio / Team Photo"),
              h(
                "div",
                null,
                h("span", { className: "eyebrow" }, "About Alterbloom"),
                h("h2", null, d.about_heading),
                h("p", null, d.about_body)
              )
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
              h("span", { className: "btn btn-primary" }, "Start a Conversation")
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
      return siteChrome([
        pageHero(d.hero_eyebrow, d.hero_heading, d.hero_body),
        h(
          "section",
          { className: "section", key: "story" },
          h(
            "div",
            { className: "container" },
            h(
              "div",
              { className: "grid grid-2", style: { alignItems: "center" } },
              h(
                "div",
                null,
                h("span", { className: "eyebrow" }, "Our Story"),
                h("h2", null, d.story_heading),
                h("p", null, d.story_body_1),
                h("p", null, d.story_body_2)
              ),
              imageOrPlaceholder(d.story_image, getAsset, "img-placeholder tall", "Founder / Origin Photo")
            )
          )
        ),
        h(
          "section",
          { className: "section", key: "values" },
          h(
            "div",
            { className: "container" },
            h(
              "div",
              { className: "section-head center" },
              h("span", { className: "eyebrow" }, "What Drives Us"),
              h("h2", null, "Our Values")
            ),
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
            h(
              "div",
              { className: "section-head center" },
              h("span", { className: "eyebrow" }, "Meet the Team"),
              h("h2", null, "The people you'll work with")
            ),
            h(
              "div",
              { className: "grid grid-4" },
              (d.team || []).map(function (m, i) {
                return h(
                  "div",
                  { key: i },
                  imageOrPlaceholder(m.photo, getAsset, "img-placeholder square", "Photo"),
                  h("h3", { style: { marginTop: "16px" } }, m.name),
                  h("p", null, m.role)
                );
              })
            )
          )
        ),
        h(
          "section",
          { className: "section", key: "stats" },
          h(
            "div",
            { className: "container" },
            h(
              "div",
              { className: "stats-row" },
              (d.stats || []).map(function (s, i) {
                return h("div", { className: "stat", key: i }, h("strong", null, s.number), h("span", null, s.label));
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
              h("span", { className: "btn btn-primary" }, "Contact Alterbloom")
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
          h("div", { className: "container" }, h("div", { style: { maxWidth: "70ch", margin: "0 auto" } }, this.props.widgetFor("body")))
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
            imageOrPlaceholder(d.cover_image, this.props.getAsset, "img-placeholder hero", "Post Cover Image"),
            h("div", { style: { maxWidth: "70ch", margin: "24px auto 0" } }, this.props.widgetFor("body"))
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
