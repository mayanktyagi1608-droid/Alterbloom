document.addEventListener("DOMContentLoaded", function () {
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".site-nav");

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      nav.classList.toggle("is-open");
      var expanded = nav.classList.contains("is-open");
      toggle.setAttribute("aria-expanded", expanded);
    });
  }

  // Only the legacy (pre-Netlify-Forms) contact form needs this — the
  // Eleventy version has data-netlify="true" and submits for real.
  var form = document.querySelector(".contact-form:not([data-netlify])");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      alert("This form isn't connected to a backend yet — we'll wire it up to send real enquiries in a later step.");
    });
  }
});
