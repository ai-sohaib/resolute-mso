(function () {
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".main-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(open));
    });
  }
  document.querySelectorAll(".has-menu").forEach(function (item) {
    var button = item.querySelector(".menu-caret");
    if (!button) return;
    button.addEventListener("click", function () {
      var open = item.classList.toggle("open");
      button.setAttribute("aria-expanded", String(open));
    });
  });
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });
  var topButton = document.querySelector(".scroll-top");
  if (topButton) {
    var setTopState = function () {
      topButton.classList.toggle("visible", window.scrollY > 500);
    };
    setTopState();
    window.addEventListener("scroll", setTopState, { passive: true });
    topButton.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }
  var launch = document.querySelector(".whatsapp-launch");
  var panel = document.querySelector(".whatsapp-panel");
  var close = document.querySelector(".whatsapp-close");
  var form = document.querySelector(".whatsapp-form");
  if (launch && panel) {
    var setPanel = function (open) {
      panel.hidden = !open;
      launch.setAttribute("aria-expanded", String(open));
    };
    launch.addEventListener("click", function () {
      setPanel(panel.hidden);
    });
    if (close) {
      close.addEventListener("click", function () {
        setPanel(false);
      });
    }
  }
  if (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var data = new FormData(form);
      var text = "Hello Resolute MSO, I would like to chat about RCM and billing automation. Name: " +
        (data.get("name") || "") + ". Email: " + (data.get("email") || "") + ". Phone: " + (data.get("phone") || "") + ".";
      window.location.href = "https://wa.me/17015525527?text=" + encodeURIComponent(text);
    });
  }
})();
