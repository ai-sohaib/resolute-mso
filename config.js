window.RESOLUTE_CONFIG = window.RESOLUTE_CONFIG || {};
window.RESOLUTE_CONFIG.formEndpoint = "https://formsubmit.co/ajax/support@resolutemso.com";
window.RESOLUTE_CONFIG.newsletterEndpoint = "https://formsubmit.co/ajax/support@resolutemso.com";

(function () {
  var footerVersion = "20260701-footer-bulletin-column";
  var cssFiles = [
    "/assets/css/final-qa-fixes.css?v=" + footerVersion,
    "/assets/css/iso-ui-polish.css?v=" + footerVersion,
    "/assets/css/menu-directory-fix.css?v=" + footerVersion,
    "/assets/css/futuristic-theme.css?v=" + footerVersion,
    "/assets/css/footer-final-dark.css?v=" + footerVersion
  ];
  cssFiles.forEach(function (href) {
    if (document.querySelector('link[href="' + href + '"]')) return;
    var link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = href;
    document.head.appendChild(link);
  });
  var cleanupSrc = "/assets/js/source-cleanup.js?v=" + footerVersion;
  if (!document.querySelector('script[src="' + cleanupSrc + '"]')) {
    var script = document.createElement("script");
    script.src = cleanupSrc;
    script.defer = true;
    document.head.appendChild(script);
  }
})();
