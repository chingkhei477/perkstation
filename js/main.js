/* ==========================================================================
   PERKSTATION — site behaviour
   Navigation, scroll effects, config-driven details, offers, contact form.
   ========================================================================== */
(function () {
  "use strict";

  var doc = document.documentElement;
  doc.classList.remove("no-js");
  doc.classList.add("js");

  var CONFIG = window.PERKSTATION_CONFIG || {};
  var OFFERS = Array.isArray(window.PERKSTATION_OFFERS) ? window.PERKSTATION_OFFERS : [];

  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $all(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }
  function clean(v) { return typeof v === "string" ? v.trim() : ""; }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function safeUrl(u) {
    u = clean(u);
    return /^https:\/\//i.test(u) ? u : "";
  }

  /* ---------- Mobile navigation ---------- */
  var toggle = $(".nav-toggle");
  var nav = $("#site-nav");
  function setNav(open) {
    document.body.classList.toggle("nav-open", open);
    if (toggle) {
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    }
  }
  if (toggle && nav) {
    toggle.addEventListener("click", function () { setNav(!document.body.classList.contains("nav-open")); });
    $all("a", nav).forEach(function (a) { a.addEventListener("click", function () { setNav(false); }); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && document.body.classList.contains("nav-open")) { setNav(false); toggle.focus(); }
    });
    window.addEventListener("resize", function () { if (window.innerWidth > 960) setNav(false); });
  }

  /* ---------- Header shadow + back to top ---------- */
  var header = $(".site-header");
  var toTop = $(".to-top");
  function onScroll() {
    var y = window.scrollY || window.pageYOffset;
    if (header) header.classList.toggle("is-scrolled", y > 8);
    if (toTop) toTop.classList.toggle("is-visible", y > 600);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
  if (toTop) toTop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: "smooth" }); });

  /* ---------- Reveal on scroll ---------- */
  var reveals = $all(".reveal");
  if ("IntersectionObserver" in window && reveals.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-in"); });
  }

  /* ---------- Config-driven business details ----------
     <span data-cfg="supportEmail" data-fallback="...">  -> text (or fallback)
     <a data-cfg-link="supportEmail">                   -> mailto / tel link
     <li data-cfg-show="phone">                         -> hidden when empty   */
  $all("[data-cfg]").forEach(function (el) {
    var v = clean(CONFIG[el.getAttribute("data-cfg")]);
    var fb = el.getAttribute("data-fallback");
    if (v) el.textContent = v;
    else if (fb !== null) el.textContent = fb;
  });
  $all("[data-cfg-link]").forEach(function (el) {
    var key = el.getAttribute("data-cfg-link");
    var v = clean(CONFIG[key]);
    if (!v) { el.removeAttribute("href"); return; }
    el.textContent = v;
    if (key === "supportEmail") el.setAttribute("href", "mailto:" + v);
    if (key === "phone") el.setAttribute("href", "tel:" + v.replace(/[^\d+]/g, ""));
  });
  $all("[data-cfg-show]").forEach(function (el) {
    var keys = el.getAttribute("data-cfg-show").split(",");
    var any = keys.some(function (k) { return clean(CONFIG[k.trim()]); });
    el.hidden = !any;
  });
  $all("[data-cfg-hide]").forEach(function (el) {
    var keys = el.getAttribute("data-cfg-hide").split(",");
    var any = keys.some(function (k) { return clean(CONFIG[k.trim()]); });
    el.hidden = any;
  });

  /* ---------- Year ---------- */
  $all("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* ---------- Offers ---------- */
  var PALETTE = ["#FF5B2E", "#102A27", "#1F7A4D", "#2F5F9E", "#B5651D", "#7A3E9D"];
  function colorFor(o, i) {
    var c = clean(o.color);
    return /^#[0-9a-f]{3,8}$/i.test(c) ? c : PALETTE[i % PALETTE.length];
  }
  function formatDate(s) {
    s = clean(s);
    if (!/^\d{4}-\d{2}-\d{2}$/.test(s)) return "";
    var d = new Date(s + "T00:00:00");
    if (isNaN(d)) return "";
    return d.toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" });
  }
  function isExpired(o) {
    var s = clean(o.validTill);
    if (!/^\d{4}-\d{2}-\d{2}$/.test(s)) return false;
    var end = new Date(s + "T23:59:59");
    return !isNaN(end) && end < new Date();
  }
  function validOffers() {
    return OFFERS.filter(function (o) {
      return o && clean(o.store) && clean(o.rate) && safeUrl(o.url) && !isExpired(o);
    });
  }
  function offerCard(o, i) {
    var id = esc(clean(o.id) || ("offer-" + i));
    var terms = Array.isArray(o.terms) ? o.terms.filter(function (t) { return clean(t); }) : [];
    var till = formatDate(o.validTill);
    var initial = esc(clean(o.store).charAt(0).toUpperCase());
    return '' +
      '<article class="ticket" style="--accent:' + colorFor(o, i) + '">' +
        (o.featured ? '<span class="ticket-badge">Featured</span>' : '') +
        '<div class="ticket-head">' +
          '<div class="monogram" aria-hidden="true">' + initial + '</div>' +
          '<div><h3 class="ticket-store">' + esc(o.store) + '</h3>' +
          '<span class="ticket-cat">' + esc(clean(o.category) || "Offer") + '</span></div>' +
        '</div>' +
        '<div class="ticket-rate"><span class="amt">' + esc(o.rate) + '<small>' + esc(clean(o.rateNote) || "cashback") + '</small></span></div>' +
        (clean(o.description) ? '<p class="ticket-desc">' + esc(o.description) + '</p>' : '') +
        '<div class="perf" aria-hidden="true"><span class="notch-r"></span></div>' +
        '<div class="ticket-foot">' +
          '<div class="ticket-meta"><span>' + (till ? "Valid till " + esc(till) : "Ongoing") + '</span><span>Terms apply</span></div>' +
          (terms.length ? '<div class="ticket-terms" id="terms-' + id + '"><ul>' + terms.map(function (t) { return "<li>" + esc(t) + "</li>"; }).join("") + '</ul></div>' : '') +
          '<div class="ticket-actions">' +
            (terms.length ? '<button type="button" class="terms-toggle" aria-expanded="false" aria-controls="terms-' + id + '">Terms</button>' : '') +
            '<a class="btn btn--signal btn--sm" href="' + esc(safeUrl(o.url)) + '" target="_blank" rel="nofollow sponsored noopener">Activate cashback</a>' +
          '</div>' +
        '</div>' +
      '</article>';
  }
  function emptyState(title, text, withCta) {
    return '<div class="empty">' +
      '<div class="icon-tile icon-tile--sun" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9a2 2 0 0 0 2-2V6a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v1a2 2 0 0 0 0 4v1a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1v-1a2 2 0 0 0-2-2z" transform="translate(0 3)"/><path d="M9 8v8" stroke-dasharray="2 2.5"/></svg></div>' +
      '<h3>' + title + '</h3><p>' + text + '</p>' +
      (withCta ? '<div class="btn-row" style="justify-content:center"><a class="btn btn--ghost btn--sm" href="how-it-works.html">See how cashback works</a></div>' : '') +
      '</div>';
  }
  function bindTerms(root) {
    $all(".terms-toggle", root).forEach(function (b) {
      b.addEventListener("click", function () {
        var card = b.closest(".ticket");
        var open = !card.classList.contains("terms-open");
        card.classList.toggle("terms-open", open);
        b.setAttribute("aria-expanded", String(open));
        b.textContent = open ? "Hide terms" : "Terms";
      });
    });
  }

  // Home preview
  var preview = $("#offer-preview");
  if (preview) {
    var list = validOffers().slice().sort(function (a, b) { return (b.featured ? 1 : 0) - (a.featured ? 1 : 0); }).slice(0, 6);
    preview.innerHTML = list.length
      ? list.map(offerCard).join("")
      : emptyState("First departures are being scheduled", "We only list offers we have confirmed with partner stores. New offers will appear here as soon as they go live.", true);
    bindTerms(preview);
  }

  // Offers page
  var grid = $("#offer-grid");
  if (grid) {
    var all = validOffers();
    var chipsBox = $("#offer-chips");
    var search = $("#offer-search");
    var sortSel = $("#offer-sort");
    var count = $("#offer-count");
    var state = { cat: "All", q: "", sort: "featured" };

    var cats = ["All"].concat(all.map(function (o) { return clean(o.category) || "Other"; })
      .filter(function (c, i, arr) { return arr.indexOf(c) === i; }).sort());
    var hashCat = decodeURIComponent((location.hash || "").replace(/^#cat=/, ""));
    if (cats.indexOf(hashCat) > -1) state.cat = hashCat;

    if (chipsBox) {
      chipsBox.innerHTML = cats.map(function (c) {
        return '<button type="button" class="chip-btn" aria-pressed="' + (c === state.cat) + '" data-cat="' + esc(c) + '">' + esc(c) + '</button>';
      }).join("");
      chipsBox.addEventListener("click", function (e) {
        var b = e.target.closest(".chip-btn");
        if (!b) return;
        state.cat = b.getAttribute("data-cat");
        $all(".chip-btn", chipsBox).forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
        if (history.replaceState) history.replaceState(null, "", state.cat === "All" ? location.pathname : "#cat=" + encodeURIComponent(state.cat));
        render();
      });
    }
    if (search) search.addEventListener("input", function () { state.q = search.value.trim().toLowerCase(); render(); });
    if (sortSel) sortSel.addEventListener("change", function () { state.sort = sortSel.value; render(); });

    function rateNum(o) { var n = parseFloat(String(o.rate).replace(/[^\d.]/g, "")); return isNaN(n) ? 0 : n; }

    function render() {
      var items = all.filter(function (o) {
        var cat = clean(o.category) || "Other";
        if (state.cat !== "All" && cat !== state.cat) return false;
        if (!state.q) return true;
        return (o.store + " " + cat + " " + (o.description || "")).toLowerCase().indexOf(state.q) > -1;
      });
      if (state.sort === "az") items.sort(function (a, b) { return a.store.localeCompare(b.store); });
      else if (state.sort === "rate") items.sort(function (a, b) { return rateNum(b) - rateNum(a); });
      else items.sort(function (a, b) { return (b.featured ? 1 : 0) - (a.featured ? 1 : 0); });

      if (!all.length) {
        grid.innerHTML = emptyState("Offers are on their way", "PerkStation lists only genuine, confirmed partner offers, so nothing is shown until an offer is live. Meanwhile, read how tracking and approval work so you're ready to earn.", true);
      } else if (!items.length) {
        grid.innerHTML = emptyState("No offers match that search", "Try a different store name or choose another category.", false);
      } else {
        grid.innerHTML = items.map(offerCard).join("");
        bindTerms(grid);
      }
      if (count) count.textContent = all.length ? items.length + (items.length === 1 ? " offer" : " offers") + " shown" : "";
      var tools = $("#offer-tools");
      if (tools) tools.hidden = !all.length;
    }
    render();
  }

  /* ---------- Legal TOC active state ---------- */
  var tocLinks = $all(".toc a[href^='#']");
  if (tocLinks.length && "IntersectionObserver" in window) {
    var map = {};
    tocLinks.forEach(function (a) { map[a.getAttribute("href").slice(1)] = a; });
    var tio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          tocLinks.forEach(function (a) { a.classList.remove("is-active"); });
          var a = map[en.target.id];
          if (a) a.classList.add("is-active");
        }
      });
    }, { rootMargin: "-20% 0px -70% 0px" });
    Object.keys(map).forEach(function (id) { var s = document.getElementById(id); if (s) tio.observe(s); });
  }

  /* ---------- Contact form ---------- */
  var form = $("#contact-form");
  if (form) {
    var status = $("#form-status");
    var rules = {
      name: function (v) { return v.length >= 2 || "Please enter your name."; },
      email: function (v) { return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v) || "Please enter a valid email address."; },
      topic: function (v) { return !!v || "Please choose a topic."; },
      message: function (v) { return v.length >= 15 || "Please add a few more details (at least 15 characters)."; }
    };
    function check(field) {
      var el = form.elements[field];
      if (!el) return true;
      var res = rules[field](el.value.trim());
      var wrap = el.closest(".field");
      var err = wrap && $(".err", wrap);
      if (res !== true) {
        if (wrap) wrap.classList.add("has-error");
        if (err) err.textContent = res;
        el.setAttribute("aria-invalid", "true");
        return false;
      }
      if (wrap) wrap.classList.remove("has-error");
      el.removeAttribute("aria-invalid");
      return true;
    }
    Object.keys(rules).forEach(function (f) {
      var el = form.elements[f];
      if (!el) return;
      el.addEventListener("blur", function () { if (el.value) check(f); });
      el.addEventListener("input", function () { if (el.closest(".field").classList.contains("has-error")) check(f); });
    });

    var consent = form.elements.consent;
    var consentErr = $("#consent-err");

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      status.className = "form-status";
      status.textContent = "";
      if (form.elements.website && form.elements.website.value) return; // spam trap

      var ok = Object.keys(rules).map(check).every(Boolean);
      if (consent && !consent.checked) {
        ok = false;
        if (consentErr) consentErr.hidden = false;
      } else if (consentErr) consentErr.hidden = true;
      if (!ok) {
        var first = $(".has-error input, .has-error select, .has-error textarea", form) || (consent && !consent.checked ? consent : null);
        if (first) first.focus();
        return;
      }

      var to = clean(CONFIG.supportEmail);
      var v = function (n) { return (form.elements[n] && form.elements[n].value.trim()) || ""; };
      var subject = "[PerkStation] " + v("topic") + (v("order") ? " – Order " + v("order") : "");
      var body = "Name: " + v("name") + "\nEmail: " + v("email") + "\nTopic: " + v("topic") +
        (v("order") ? "\nOrder ID / store: " + v("order") : "") + "\n\n" + v("message");

      if (!to) {
        status.className = "form-status is-warn";
        status.textContent = "Thanks — your message is ready, but our support inbox isn't published yet. Please check back shortly and try again.";
        return;
      }
      window.location.href = "mailto:" + encodeURIComponent(to).replace(/%40/g, "@") +
        "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
      status.className = "form-status is-ok";
      status.textContent = "Your email app should now open with your message filled in — just press send. If nothing opened, write to us at " + to + ".";
    });
  }
})();
