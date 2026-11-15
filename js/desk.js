/* Christophe's desk (the Journal page). Progressive enhancement: without this script, or with
   reduced motion, the page is simply shown poured out and every post is listed.

   1. The page pours out of the typewriter as the visitor scrolls. At the top there is none;
      it then runs down to the bottom of the drawing's box and keeps flowing. On wide screens
      that box is pinned beside the posts.
   2. The filters above the posts show one kind of post at a time. */
(function () {
  var art = document.querySelector("[data-desk]");
  var scene = art && art.querySelector(".desk-scene");
  var still = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (art && scene && !still) {
    var CREST = 262 / 520;   // where the page folds over the roller, as a share of the drawing's height (see scripts/art/writer.py)
    var waiting = false;
    art.classList.add("is-live");

    var draw = function () {
      waiting = false;
      var start = scene.offsetTop + scene.offsetHeight * CREST;
      var room = Math.max(0, art.clientHeight - start);                      // how far the page can fall inside the box
      var pinned = window.getComputedStyle(art).position === "sticky";
      var over = pinned ? window.innerHeight * 0.6 : 260;                    // scroll distance over which it reaches the bottom
      var run = (window.scrollY || 0) * (room / over);
      art.style.setProperty("--pour", Math.min(room, run) + "px");           // the length of page showing
      art.style.setProperty("--run", run + "px");                            // how far the typing has travelled
    };
    var queue = function () {
      if (!waiting) { waiting = true; window.requestAnimationFrame(draw); }
    };
    window.addEventListener("scroll", queue, { passive: true });
    window.addEventListener("resize", queue);
    window.addEventListener("load", queue);
    draw();
  }

  var bar = document.querySelector("[data-filters]");
  if (bar) {
    var buttons = bar.querySelectorAll("[data-filter]");
    var cards = document.querySelectorAll(".wall [data-kind]");
    bar.addEventListener("click", function (e) {
      var button = e.target.closest ? e.target.closest("[data-filter]") : null;
      if (!button) return;
      var kind = button.getAttribute("data-filter");
      Array.prototype.forEach.call(buttons, function (b) { b.setAttribute("aria-pressed", b === button ? "true" : "false"); });
      Array.prototype.forEach.call(cards, function (c) { c.hidden = kind !== "all" && c.getAttribute("data-kind") !== kind; });
    });
  }
})();
