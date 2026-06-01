/* Yiska Cleaning VOF — interactions (vanilla JS, no dependencies) */
(function () {
  "use strict";

  /* ----- Mobile navigation ----- */
  var toggle = document.querySelector(".nav__toggle");
  var menu = document.getElementById("nav-menu");
  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      var open = menu.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    menu.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        menu.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  /* ----- Reveal on scroll ----- */
  var reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && reveals.length) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) {
            e.target.classList.add("in");
            io.unobserve(e.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("in"); });
  }

  /* ----- Image fallback: hide broken images, reveal text fallback ----- */
  document.querySelectorAll("img[data-fallback]").forEach(function (img) {
    img.addEventListener("error", function () {
      var fb = document.querySelector(img.getAttribute("data-fallback"));
      img.style.display = "none";
      if (fb) fb.style.display = "";
    });
  });

  /* ----- Contact form (front-end only; wire to a real endpoint in production) ----- */
  var form = document.getElementById("contact-form");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var data = new FormData(form);
      var naam = encodeURIComponent(data.get("naam") || "");
      var bedrijf = encodeURIComponent(data.get("bedrijf") || "");
      var email = encodeURIComponent(data.get("email") || "");
      var tel = encodeURIComponent(data.get("telefoon") || "");
      var dienst = encodeURIComponent(data.get("dienst") || "");
      var bericht = encodeURIComponent(data.get("bericht") || "");

      var body =
        "Naam: " + decodeURIComponent(naam) + "%0D%0A" +
        "Bedrijf: " + decodeURIComponent(bedrijf) + "%0D%0A" +
        "E-mail: " + decodeURIComponent(email) + "%0D%0A" +
        "Telefoon: " + decodeURIComponent(tel) + "%0D%0A" +
        "Dienst: " + decodeURIComponent(dienst) + "%0D%0A%0D%0A" +
        decodeURIComponent(bericht);

      var to = form.getAttribute("data-mailto") || "info@yiskacleaning.nl";
      var subject = encodeURIComponent("Offerteaanvraag via website — " + decodeURIComponent(bedrijf || naam));

      var status = document.getElementById("form-status");
      if (status) {
        status.textContent =
          "Bedankt! Uw e-mailprogramma wordt geopend om de aanvraag te versturen. " +
          "Liever direct contact? Bel ons gerust.";
        status.classList.add("show", "ok");
      }
      window.location.href = "mailto:" + to + "?subject=" + subject + "&body=" + body;
    });
  }

  /* ----- Footer year ----- */
  var yr = document.getElementById("year");
  if (yr) yr.textContent = new Date().getFullYear();
})();
