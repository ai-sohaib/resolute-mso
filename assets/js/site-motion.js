(function () {
  "use strict";

  var reducedMotion = window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  document.documentElement.classList.add("motion-enabled");

  function sleep(milliseconds) {
    return new Promise(function (resolve) {
      window.setTimeout(resolve, milliseconds);
    });
  }

  async function startTypewriter() {
    var heading = document.querySelector(".hero-typewriter");
    if (!heading) return;

    var output = heading.querySelector(".typewriter-output");
    var fullText = heading.getAttribute("data-typewriter-text") || "";
    if (!output || !fullText) return;

    if (reducedMotion) {
      output.textContent = fullText;
      return;
    }

    while (document.documentElement.contains(heading)) {
      output.textContent = "";

      for (var index = 0; index < fullText.length; index += 1) {
        output.textContent = fullText.slice(0, index + 1);
        await sleep(46);
      }

      await sleep(1850);

      for (var remaining = fullText.length; remaining > 0; remaining -= 1) {
        output.textContent = fullText.slice(0, remaining - 1);
        await sleep(24);
      }

      await sleep(520);
    }
  }

  function prepareReveal(element, direction, index, isCard) {
    if (!element || element.classList.contains("scroll-reveal")) return;

    element.classList.add("scroll-reveal", direction);
    if (isCard) element.classList.add("reveal-card");
    element.style.setProperty("--reveal-delay", Math.min(index % 6, 5) * 70 + "ms");
  }

  function setupScrollReveal() {
    var sections = Array.prototype.slice.call(
      document.querySelectorAll("main > section, main > article, .site-footer")
    );

    sections.forEach(function (element, index) {
      prepareReveal(element, index % 2 === 0 ? "from-left" : "from-right", index, false);
    });

    var cardSelector = [
      ".card-grid > *",
      ".directory-grid > *",
      ".workflow-grid > *",
      ".answer-grid > *",
      ".outcome-grid > *",
      ".related-grid > *",
      ".solutions-index > *",
      ".trust-list > *",
      ".platform-strip > *",
      ".footer-grid > *",
      ".form-grid > *",
      ".split > *",
      ".article-grid > *",
      ".hero-grid > *"
    ].join(",");

    var cards = Array.prototype.slice.call(document.querySelectorAll(cardSelector));

    cards.forEach(function (element, index) {
      prepareReveal(element, index % 2 === 0 ? "from-left" : "from-right", index, true);
    });

    var targets = Array.prototype.slice.call(document.querySelectorAll(".scroll-reveal"));

    if (reducedMotion || !("IntersectionObserver" in window)) {
      targets.forEach(function (element) {
        element.classList.add("is-visible");
      });
      return;
    }

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.12,
      rootMargin: "0px 0px -8% 0px"
    });

    targets.forEach(function (element) {
      observer.observe(element);
    });
  }

  function initializeMotion() {
    setupScrollReveal();
    startTypewriter();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initializeMotion, { once: true });
  } else {
    initializeMotion();
  }
})();
