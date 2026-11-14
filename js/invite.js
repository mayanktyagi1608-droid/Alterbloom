/* The invitation: scroll position opens the envelope.
   Progressive enhancement: without this script, or with reduced motion, the
   page shows the invitation card already open (see css/sections.css). The
   heading and links are always in the HTML. */
(function () {
  var root = document.querySelector("[data-invite]");
  if (!root) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  var track = root.querySelector(".invite-track");
  var stage = root.querySelector(".invite-stage");
  var seal = root.querySelector(".env-seal");
  var vh = 800;
  var range = 2.2;
  var queued = false;

  function clamp(x) { return Math.max(0, Math.min(1, x)); }
  function ease(x) { return 1 - Math.pow(1 - x, 3); }

  function measure() {
    var w = window.innerWidth;
    vh = stage.offsetHeight || window.innerHeight;                       // scroll distance unit
    var tb = document.querySelector(".thumb-bar");                        // the fixed mobile bar (hidden on desktop, so 0)
    var bar = tb ? tb.offsetHeight : 0;
    var room = vh - bar;                                                  // height actually visible above the mobile bar
    range = w < 600 ? 2.2 : 3;
    // Fit the 560 x 440 envelope, with its flap open above it, to the screen.
    var ss = Math.min(1, room / 960, (w - 24) / 560);
    // The letter comes partway out: its top ends 177px above the envelope's top edge, as on the
    // design board. If the wording is long it comes out a little further, just enough for each
    // line's lower corners to clear the pocket's edge (which runs down at 0.75 to the middle).
    var lift = 187;
    var lines = root.querySelectorAll(".env-eyebrow, .env-title, .env-note");
    for (var i = 0; i < lines.length; i++) {
      var bottom = lines[i].offsetTop + lines[i].offsetHeight;        // from the letter's top edge
      var edge = 0.7516 * (280 - lines[i].offsetWidth / 2) - 16;       // how low this line may sit
      lift = Math.max(lift, 10 + bottom - edge);
    }
    lift = Math.min(lift, 215);                                        // the letter's foot stays in the pocket
    root.style.setProperty("--lift", (-lift).toFixed(1));
    root.style.setProperty("--ss", ss.toFixed(3));
    root.style.setProperty("--rng", range);
    update();
  }

  function update() {
    queued = false;
    var p = clamp(-track.getBoundingClientRect().top / (range * vh));
    var flap = ease(clamp((p - 0.1) / 0.25));
    var rise = ease(clamp((p - 0.38) / 0.34));
    var sealK = clamp((p - 0.06) / 0.12);
    var s = root.style;
    s.setProperty("--flap", (flap * 180).toFixed(1));
    s.setProperty("--rise", rise.toFixed(3));
    s.setProperty("--seal-o", (1 - sealK).toFixed(2));
    s.setProperty("--seal-s", (1 + 0.5 * sealK).toFixed(2));
    s.setProperty("--seal-r", (25 * sealK).toFixed(1));
    s.setProperty("--hint-o", (1 - clamp(p / 0.08)).toFixed(2));
    s.setProperty("--skip-o", (1 - clamp((p - 0.5) / 0.3)).toFixed(2));
    root.classList.toggle("is-opening", p > 0.02);
    root.classList.toggle("is-flap-over", flap > 0.5);                    // past upright: show the lined inside
    root.classList.toggle("is-rising", rise > 0.02);
  }

  function queue() {
    if (queued) return;
    queued = true;
    requestAnimationFrame(update);
  }

  if (seal) {
    seal.addEventListener("click", function () {
      var top = track.getBoundingClientRect().top + window.scrollY;
      window.scrollTo({ top: top + range * vh * 0.82, behavior: "smooth" });
    });
  }

  window.addEventListener("scroll", queue, { passive: true });
  window.addEventListener("resize", measure);
  measure();
})();
