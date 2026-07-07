(function () {
  "use strict";
  function ready(callback) {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", callback, { once: true });
    else callback();
  }
  function normalizeAssetPaths() {
    document.querySelectorAll("img[src^='assets/']").forEach(function (image) {
      image.src = "/" + image.getAttribute("src");
    });
  }
  function normalizeLegacyLinks() {
    document.querySelectorAll("a[href]").forEach(function (anchor) {
      var href = anchor.getAttribute("href");
      if (!href || href.indexOf("http") === 0 || href.indexOf("mailto:") === 0 || href.indexOf("tel:") === 0) return;
      if (/^[^/].*\.html(?:[#?].*)?$/.test(href)) anchor.setAttribute("href", "/" + href);
    });
  }
  function addGoUpButton() {
    if (document.querySelector(".go-up-button, .scroll-top")) return;
    var button = document.createElement("button");
    button.className = "go-up-button";
    button.type = "button";
    button.textContent = "↑";
    button.setAttribute("aria-label", "Go to top");
    document.body.appendChild(button);
    function update() { button.classList.toggle("is-visible", window.scrollY > 420); }
    button.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: "smooth" }); });
    window.addEventListener("scroll", update, { passive: true });
    update();
  }
  ready(function () {
    normalizeAssetPaths();
    normalizeLegacyLinks();
    addGoUpButton();
  });
})();
