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
    var bar = parseFloat(getComputedStyle(root).getPropertyValue("--invite-bar")) || 0;
    var room = vh - bar;                                                  // height actually visible above the mobile bar
    range = w < 600 ? 2.2 : 3;
    // Fit the 560px-wide envelope to the screen, then size the opened card to ~540px or the screen width.
    var ss = Math.min(1, room / 960, (w - 24) / 560);
    var cs = Math.min(1.3, Math.min(540, w - 36) / (420 * ss));
    root.style.setProperty("--ss", ss.toFixed(3));
    root.style.setProperty("--cs", cs.toFixed(3));
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
    root.classList.toggle("is-rising", rise > 0.02);
    root.classList.toggle("is-open", rise > 0.9);
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
