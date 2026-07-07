window.RESOLUTE_CONFIG = window.RESOLUTE_CONFIG || {};

window.RESOLUTE_CONFIG.whatsappNumber =
  window.RESOLUTE_CONFIG.whatsappNumber || "17015525527";
window.RESOLUTE_CONFIG.whatsappMessage =
  window.RESOLUTE_CONFIG.whatsappMessage ||
  "Hello Resolute MSO, I would like to discuss your medical billing, RCM, or healthcare automation services.";

/* Set this at deployment time to the secure serverless endpoint. Never place API keys or mail credentials here. */
window.RESOLUTE_CONFIG.formEndpoint =
  window.RESOLUTE_CONFIG.formEndpoint || "";

(function () {
  "use strict";
  var version = "20260707-enterprise-upgrade";
  var enterpriseHome = Boolean(document.querySelector(".r-site-header"));

  function addStyle(path) {
    if (document.querySelector('link[href*="' + path + '"]')) return;
    var link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = path + "?v=" + version;
    document.head.appendChild(link);
  }

  function addScript(path) {
    if (document.querySelector('script[src*="' + path + '"]')) return;
    var script = document.createElement("script");
    script.src = path + "?v=" + version;
    script.defer = true;
    document.head.appendChild(script);
  }

  if (!enterpriseHome) {
    addStyle("/assets/css/final-qa-fixes.css");
    addStyle("/assets/css/iso-ui-polish.css");
    addStyle("/assets/css/menu-directory-fix.css");
    addStyle("/assets/css/futuristic-theme.css");
    addStyle("/assets/css/footer-final-dark.css");
    addScript("/assets/js/source-cleanup.js");
  }

  addStyle("/assets/css/enterprise-upgrade.css");
  addScript("/assets/js/enterprise-upgrade.js");
  addScript("/assets/js/whatsapp-normalize.js");
})();
