// Settings shared by every journal post in this folder. This file is not a post.
module.exports = {
  layout: "post.njk",
  tags: "posts",
  eleventyComputed: {
    // Only long reads get a page of their own. Short notes and Instagram posts
    // appear on the Journal page and nowhere else.
    permalink: (data) => (data.kind && data.kind !== "long" ? false : `/blog/${data.page.fileSlug}/`),
  },
};
