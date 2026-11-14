/* The menu card on the home page: it starts as a small cover on the plate and
   opens to its full size as the page scrolls past the table setting.
   Progressive enhancement: without this script, or with reduced motion, the
   card is simply shown at full size (see css/sections.css). */
(function () {
  var card = document.querySelector("[data-menu]");
  var scene = document.querySelector(".setting-scene");
  if (!card || !scene) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  var sheet = card.querySelector(".menu-sheet");
  var COVER_W = 252, COVER_H = 350;      // the cover's canvas in css/sections.css
  var PLATE_Y = 440 / 710;               // the plate's centre, as a share of the picture's height
  var PLATE_D = 452 / 800;               // the plate's width, as a share of the picture's width
  var m = null;                          // measurements
  var last = -1;
  var queued = false;

  function clamp(x) { return Math.max(0, Math.min(1, x)); }
  function lerp(a, b, t) { return a + (b - a) * t; }
  function smooth(x) { return x * x * (3 - 2 * x); }

  function measure() {
    // Read the card at rest: full size, no transform.
    card.classList.remove("is-live");
    var c = card.getBoundingClientRect();
    var s = scene.getBoundingClientRect();
    if (!c.width || !s.width) return;
    var w0 = PLATE_D * s.width * 0.52;                 // the cover is about half the plate wide
    var h0 = w0 * COVER_H / COVER_W;
    m = {
      w: c.width,
      h: sheet.offsetHeight,
      k0: w0 / c.width,
      h0: h0,
      y0: (s.top + PLATE_Y * s.height - h0 / 2) - c.top,   // lifts the cover onto the middle of the plate
      plate: PLATE_Y * s.height                            // plate centre, measured from the picture's top
    };
    card.style.setProperty("--menu-h", m.h + "px");
    card.style.setProperty("--menu-cover-s", (sheet.clientWidth / COVER_W).toFixed(4));
    card.classList.add("is-live");
    last = -1;
    update();
  }

  function update() {
    queued = false;
    if (!m) return;
    var header = document.querySelector(".site-header");
    var bar = document.querySelector(".thumb-bar");
    var top = header ? header.offsetHeight : 0;
    var room = window.innerHeight - top - (bar ? bar.offsetHeight : 0);
    var plateY = scene.getBoundingClientRect().top + m.plate;
    // Closed until the plate is a little below the middle of the screen; fully open once it nears the top.
    var from = top + room * 0.6, to = top + room * 0.22;
    var p = clamp((from - plateY) / (from - to));
    if (p === last) return;
    last = p;
    var e = smooth(p);
    var k = lerp(m.k0, 1, e);
    var s = card.style;
    s.setProperty("--menu-k", k.toFixed(4));
    s.setProperty("--menu-y", lerp(m.y0, 0, e).toFixed(1));
    s.setProperty("--menu-r", lerp(4, 0, e).toFixed(2));
    // The sheet keeps the cover's proportions while the cover is showing, then lengthens to the full card.
    var asCover = Math.min(k * m.w * COVER_H / COVER_W, m.h);
    s.setProperty("--menu-sheet-h", (lerp(asCover, m.h, smooth(clamp((p - 0.3) / 0.7))) / k).toFixed(1));
    s.setProperty("--menu-cover-o", (1 - clamp((p - 0.28) / 0.24)).toFixed(2));
    s.setProperty("--menu-body-o", clamp((p - 0.46) / 0.34).toFixed(2));
    card.classList.toggle("is-opened", p > 0.75);
  }

  function queue() {
    if (queued) return;
    queued = true;
    requestAnimationFrame(update);
  }

  window.addEventListener("scroll", queue, { passive: true });
  window.addEventListener("resize", measure);
  window.addEventListener("load", function () {
    scene.loading = "eager";   // once the first screen is done, fetch the picture so it is there before the card is
    measure();
  });
  scene.addEventListener("load", measure);   // lazy-loaded; its width and height attributes already give it its size
  measure();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(measure);
})();
