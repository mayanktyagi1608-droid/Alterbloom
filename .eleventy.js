module.exports = function (eleventyConfig) {
  // Static assets shared with the pre-CMS site — unchanged locations.
  eleventyConfig.addPassthroughCopy("css");
  eleventyConfig.addPassthroughCopy("js");
  eleventyConfig.addPassthroughCopy("admin");
  // Rendered artwork (see scripts/art/). Photos still go through the CMS into src/uploads.
  eleventyConfig.addPassthroughCopy("img");

  // Images uploaded through the CMS land in src/uploads and are served from /uploads.
  eleventyConfig.addPassthroughCopy({ "src/uploads": "uploads" });

  eleventyConfig.addGlobalData("currentYear", () => new Date().getFullYear());

  // The journal. A post's "kind" is long (the default), short or instagram.
  const kindOf = (item) => item.data.kind || "long";
  const newestFirst = (api) => api.getFilteredByTag("posts").sort((a, b) => b.date - a.date);
  eleventyConfig.addCollection("journal", (api) => newestFirst(api));
  eleventyConfig.addCollection("longReads", (api) => newestFirst(api).filter((i) => kindOf(i) === "long"));
  eleventyConfig.addCollection("shortNotes", (api) => newestFirst(api).filter((i) => kindOf(i) === "short"));
  eleventyConfig.addCollection("instagramPosts", (api) => newestFirst(api).filter((i) => kindOf(i) === "instagram"));

  // "12 Nov", for the small cards on the Journal page.
  eleventyConfig.addFilter("shortDate", function (dateObj) {
    return new Date(dateObj).toLocaleDateString("en-GB", { day: "numeric", month: "short" });
  });

  // Minutes to read a post, from its rendered HTML.
  eleventyConfig.addFilter("readingTime", function (html) {
    const words = String(html || "").replace(/<[^>]+>/g, " ").split(/\s+/).filter(Boolean).length;
    return Math.max(1, Math.round(words / 220));
  });

  eleventyConfig.addFilter("postDate", function (dateObj) {
    return new Date(dateObj).toLocaleDateString("en-GB", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  });

  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      data: "_data",
    },
    templateFormats: ["njk", "md"],
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
  };
};
