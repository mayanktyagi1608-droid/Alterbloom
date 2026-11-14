/* Enquiry form helpers (progressive enhancement: without JavaScript the forms still work,
   with a native date picker and a plain dropdown of places).

   1. Date: type it (DD/MM/YYYY) or pick it from the calendar. The form submits it as YYYY-MM-DD.
   2. Place: type to filter the list; only places from the list are accepted. */
(function () {
  "use strict";

  function pad(n) { return String(n).padStart(2, "0"); }
  function iso(d) { return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()); }

  /* ---------------------------------------------------------------- date */
  var CAL = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><rect x="3.5" y="5" width="17" height="15.5" rx="0"/><path d="M3.5 10h17M8 3v4M16 3v4"/></svg>';

  function enhanceDate(native) {
    var todayIso = iso(new Date());
    var name = native.name;
    var wrap = document.createElement("div");
    wrap.className = "date-field";

    var text = document.createElement("input");
    text.type = "text";
    text.id = native.id;
    text.className = "date-text";
    text.inputMode = "numeric";
    text.autocomplete = "off";
    text.placeholder = "DD/MM/YYYY";
    text.maxLength = 10;
    var describedBy = native.getAttribute("aria-describedby");
    if (describedBy) text.setAttribute("aria-describedby", describedBy);

    var value = document.createElement("input");   // what is actually submitted: YYYY-MM-DD
    value.type = "hidden";
    value.name = name;

    var pick = document.createElement("span");
    pick.className = "date-pick";
    pick.innerHTML = CAL;

    native.removeAttribute("name");
    native.removeAttribute("id");
    native.removeAttribute("data-min-today");
    native.removeAttribute("required");
    native.min = todayIso;
    native.value = "";
    native.tabIndex = -1;
    native.className = "date-native";
    native.setAttribute("aria-label", "Open calendar");

    native.parentNode.insertBefore(wrap, native);
    wrap.appendChild(text);
    wrap.appendChild(value);
    wrap.appendChild(pick);
    pick.appendChild(native);

    function setFromIso(s) {
      value.value = s;
      native.value = s;
      text.value = s ? s.slice(8, 10) + "/" + s.slice(5, 7) + "/" + s.slice(0, 4) : "";
      text.setCustomValidity("");
    }

    function parse(s) {
      var m = /^(\d{2})\/(\d{2})\/(\d{4})$/.exec(s);
      if (!m) return "";
      var d = new Date(+m[3], +m[2] - 1, +m[1]);
      if (d.getFullYear() !== +m[3] || d.getMonth() !== +m[2] - 1 || d.getDate() !== +m[1]) return "";
      return iso(d);
    }

    text.addEventListener("input", function (e) {
      var v = text.value;
      // Add the slashes as the digits are typed (not when deleting).
      if (!e.inputType || e.inputType.indexOf("delete") !== 0) {
        var digits = v.replace(/\D/g, "").slice(0, 8);
        v = digits.length > 4 ? digits.slice(0, 2) + "/" + digits.slice(2, 4) + "/" + digits.slice(4)
          : digits.length > 2 ? digits.slice(0, 2) + "/" + digits.slice(2)
          : digits;
        text.value = v;
      }
      var parsed = parse(v);
      if (!v) {
        value.value = ""; native.value = ""; text.setCustomValidity("");
      } else if (!parsed) {
        value.value = ""; native.value = "";
        text.setCustomValidity("Enter the date as DD/MM/YYYY, for example 12/06/2027.");
      } else if (parsed < todayIso) {
        value.value = ""; native.value = "";
        text.setCustomValidity("That date has already passed. Choose a date from today on.");
      } else {
        value.value = parsed; native.value = parsed; text.setCustomValidity("");
      }
    });

    native.addEventListener("change", function () { setFromIso(native.value); });
    native.addEventListener("click", function () {
      if (native.showPicker) { try { native.showPicker(); } catch (err) { /* the browser opens it itself */ } }
    });
  }

  /* --------------------------------------------------------------- place */
  var CHEVRON = '<svg viewBox="0 0 12 8" width="12" height="8" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true" focusable="false"><path d="M1 1.5l5 5 5-5"/></svg>';
  var comboCount = 0;

  function enhancePlace(sel) {
    var groups = Array.prototype.map.call(sel.querySelectorAll("optgroup"), function (g) {
      return { label: g.label, items: Array.prototype.map.call(g.querySelectorAll("option"), function (o) { return o.textContent.trim(); }) };
    });
    var all = [];
    groups.forEach(function (g) { all = all.concat(g.items); });
    if (!all.length) return;

    var uid = "combo" + (++comboCount);
    var wrap = document.createElement("div");
    wrap.className = "combo";

    var input = document.createElement("input");
    input.type = "text";
    input.id = sel.id;
    input.className = "combo-input";
    input.autocomplete = "off";
    input.autocapitalize = "off";
    input.spellcheck = false;
    input.placeholder = "Start typing a place";
    input.required = sel.required;
    input.setAttribute("role", "combobox");
    input.setAttribute("aria-autocomplete", "list");
    input.setAttribute("aria-expanded", "false");
    input.setAttribute("aria-controls", uid + "-list");

    var list = document.createElement("ul");
    list.className = "combo-list";
    list.id = uid + "-list";
    list.setAttribute("role", "listbox");
    list.hidden = true;

    var caret = document.createElement("span");
    caret.className = "combo-caret";
    caret.innerHTML = CHEVRON;

    // The original <select> stays in the form (it carries the name and the value) but is hidden.
    sel.removeAttribute("id");
    sel.removeAttribute("required");
    sel.style.display = "none";
    sel.tabIndex = -1;
    sel.setAttribute("aria-hidden", "true");
    sel.parentNode.insertBefore(wrap, sel);
    wrap.appendChild(input);
    wrap.appendChild(caret);
    wrap.appendChild(list);
    wrap.appendChild(sel);

    var options = [];   // the <li role=option> elements currently shown
    var active = -1;

    function exact(v) {
      var q = v.trim().toLowerCase();
      for (var i = 0; i < all.length; i++) if (all[i].toLowerCase() === q) return all[i];
      return "";
    }

    function setValue(v) {
      sel.value = v;
      if (sel.value !== v) sel.selectedIndex = 0;
      input.value = v;
      input.setCustomValidity("");
    }

    function validate() {
      var v = input.value.trim();
      var hit = exact(v);
      if (!v) { sel.selectedIndex = 0; input.setCustomValidity(""); return; }
      if (hit) { setValue(hit); return; }
      sel.selectedIndex = 0;
      input.setCustomValidity("Please choose a place from the list. Try Elsewhere in the UK if yours isn't there.");
    }

    function setActive(i) {
      if (active > -1 && options[active]) options[active].setAttribute("aria-selected", "false");
      active = i;
      if (i > -1 && options[i]) {
        options[i].setAttribute("aria-selected", "true");
        input.setAttribute("aria-activedescendant", options[i].id);
        options[i].scrollIntoView({ block: "nearest" });
      } else {
        input.removeAttribute("aria-activedescendant");
      }
    }

    function render() {
      var q = input.value.trim().toLowerCase();
      list.textContent = "";
      options = [];
      var shown = 0;
      groups.forEach(function (g) {
        var hits = g.items.filter(function (p) { return !q || p.toLowerCase().indexOf(q) > -1; });
        if (q) {   // places that start with the typed text come first
          hits.sort(function (a, b) { return (b.toLowerCase().indexOf(q) === 0) - (a.toLowerCase().indexOf(q) === 0); });
        }
        if (!hits.length) return;
        var head = document.createElement("li");
        head.className = "combo-group";
        head.setAttribute("role", "presentation");
        head.textContent = g.label;
        list.appendChild(head);
        hits.forEach(function (p) {
          var li = document.createElement("li");
          li.className = "combo-option";
          li.id = uid + "-o" + (options.length);
          li.setAttribute("role", "option");
          li.setAttribute("aria-selected", "false");
          li.textContent = p;
          li.addEventListener("mousedown", function (e) { e.preventDefault(); });   // keep focus in the field
          li.addEventListener("click", function () { setValue(p); close(); });
          list.appendChild(li);
          options.push(li);
          shown++;
        });
      });
      if (!shown) {
        var none = document.createElement("li");
        none.className = "combo-none";
        none.setAttribute("role", "presentation");
        none.textContent = "No match in our list. Try Elsewhere in the UK.";
        list.appendChild(none);
      }
      active = -1;
      input.removeAttribute("aria-activedescendant");
      if (q && options.length) setActive(0);
    }

    function open() {
      render();
      list.hidden = false;
      input.setAttribute("aria-expanded", "true");
    }
    function close() {
      list.hidden = true;
      input.setAttribute("aria-expanded", "false");
      setActive(-1);
    }

    input.addEventListener("focus", open);
    input.addEventListener("click", function () { if (list.hidden) open(); });
    input.addEventListener("input", function () { validate(); open(); });
    input.addEventListener("blur", function () { validate(); close(); });
    input.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown") {
        e.preventDefault();
        if (list.hidden) open();
        if (options.length) setActive(active + 1 >= options.length ? 0 : active + 1);
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        if (list.hidden) open();
        if (options.length) setActive(active - 1 < 0 ? options.length - 1 : active - 1);
      } else if (e.key === "Enter") {
        if (!list.hidden && active > -1 && options[active]) {
          e.preventDefault();
          setValue(options[active].textContent);
          close();
        }
      } else if (e.key === "Escape") {
        if (!list.hidden) { e.preventDefault(); close(); }
      }
    });

    // A browser that remembers the previous choice (back button) may pre-select the <select>.
    if (sel.value) input.value = sel.value;
    validate();
  }

  document.addEventListener("DOMContentLoaded", function () {
    Array.prototype.forEach.call(document.querySelectorAll("input[type=date][data-min-today]"), enhanceDate);
    Array.prototype.forEach.call(document.querySelectorAll("select[data-places]"), enhancePlace);
  });
})();
