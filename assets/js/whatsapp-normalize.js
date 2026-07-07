(function () {
  "use strict";

  function config() {
    return window.RESOLUTE_CONFIG || {};
  }

  function directUrl() {
    var settings = config();
    var number = String(settings.whatsappNumber || "").replace(/\D/g, "");
    var message = settings.whatsappMessage ||
      "Hello Resolute MSO, I would like to discuss your medical billing, RCM, or healthcare automation services.";
    return number ? "https://wa.me/" + number + "?text=" + encodeURIComponent(message) : "";
  }

  function icon() {
    return '<svg class="r-whatsapp-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M12.04 2C6.52 2 2.03 6.45 2.03 11.93c0 1.75.46 3.46 1.33 4.96L2 22l5.25-1.35a10.1 10.1 0 0 0 4.79 1.22c5.52 0 10.01-4.45 10.01-9.94S17.56 2 12.04 2Zm0 18.18c-1.52 0-3-.41-4.3-1.18l-.31-.18-3.11.8.83-3.01-.2-.31a8.16 8.16 0 0 1-1.25-4.37c0-4.55 3.74-8.25 8.34-8.25s8.34 3.7 8.34 8.25-3.74 8.25-8.34 8.25Zm4.57-6.18c-.25-.12-1.48-.73-1.71-.81-.23-.08-.4-.12-.57.12-.17.25-.65.81-.8.98-.15.17-.3.19-.55.06-.25-.12-1.06-.39-2.02-1.24-.75-.66-1.25-1.48-1.4-1.73-.15-.25-.02-.38.11-.51.11-.11.25-.3.37-.45.12-.15.17-.25.25-.42.08-.17.04-.31-.02-.43-.06-.12-.57-1.36-.78-1.86-.21-.5-.41-.43-.57-.44h-.49c-.17 0-.43.06-.66.31-.23.25-.87.85-.87 2.07s.89 2.4 1.02 2.56c.12.17 1.75 2.65 4.25 3.72.59.25 1.06.4 1.42.51.6.19 1.14.16 1.57.1.48-.07 1.48-.6 1.69-1.18.21-.58.21-1.08.15-1.18-.06-.1-.23-.16-.48-.28Z"/></svg>';
  }

  function toAnchor(control) {
    if (control.tagName === "A") return control;
    var link = document.createElement("a");
    Array.prototype.forEach.call(control.attributes, function (attribute) {
      if (!/^(type|aria-controls|aria-expanded)$/i.test(attribute.name)) {
        link.setAttribute(attribute.name, attribute.value);
      }
    });
    link.className = control.className;
    link.innerHTML = control.innerHTML;
    control.replaceWith(link);
    return link;
  }

  function normalize() {
    var url = directUrl();
    if (!url) return;

    document.querySelectorAll("a, button").forEach(function (control) {
      var label = (control.textContent || "").trim();
      var isWhatsApp = /whatsapp/i.test(label) ||
        control.matches("[data-whatsapp-link], .whatsapp-launch, a[href*='wa.me/']");
      if (!isWhatsApp) return;

      var link = toAnchor(control);
      link.href = url;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      link.classList.add("btn-whatsapp");
      link.removeAttribute("aria-controls");
      link.removeAttribute("aria-expanded");
      link.setAttribute("aria-label", "Talk with Resolute MSO on WhatsApp");
      if (!link.querySelector("svg")) link.insertAdjacentHTML("afterbegin", icon());
    });

    document.querySelectorAll(".whatsapp-panel").forEach(function (panel) {
      panel.hidden = true;
      panel.setAttribute("aria-hidden", "true");
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", normalize, { once: true });
  } else {
    normalize();
  }
})();
