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
  function addStyle(href) {
    if (document.querySelector('link[href="' + href + '"]')) return;
    var link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = href;
    document.head.appendChild(link);
  }
  function addScript(src) {
    if (document.querySelector('script[src="' + src + '"]')) return;
    var script = document.createElement("script");
    script.src = src;
    script.defer = true;
    document.head.appendChild(script);
  }
  addStyle("/assets/css/final-qa-fixes.css?v=" + version);
  addStyle("/assets/css/iso-ui-polish.css?v=" + version);
  addStyle("/assets/css/menu-directory-fix.css?v=" + version);
  addStyle("/assets/css/futuristic-theme.css?v=" + version);
  addStyle("/assets/css/footer-final-dark.css?v=" + version);
  addStyle("/assets/css/enterprise-upgrade.css?v=" + version);
  addScript("/assets/js/source-cleanup.js?v=" + version);
  addScript("/assets/js/enterprise-upgrade.js?v=" + version);
})();
