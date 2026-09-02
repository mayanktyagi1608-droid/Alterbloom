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

  var pills = document.querySelectorAll(".filter-pill");
  var items = document.querySelectorAll("[data-category]");

  pills.forEach(function (pill) {
    pill.addEventListener("click", function () {
      pills.forEach(function (p) { p.classList.remove("is-active"); });
      pill.classList.add("is-active");
      var filter = pill.getAttribute("data-filter");

      items.forEach(function (item) {
        var show = filter === "all" || item.getAttribute("data-category") === filter;
        item.style.display = show ? "" : "none";
      });
    });
  });

  var form = document.querySelector(".contact-form");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      alert("This wireframe form is not yet connected to a backend. We'll wire this up to send real enquiries in a later step.");
    });
  }
});
