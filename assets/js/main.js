window.RESOLUTE_CONFIG = window.RESOLUTE_CONFIG || {};

var SITE = {
  email: "support@resolutemso.com",
  wa: "https://wa.me/17015525527",
  waMessage: "Hello Resolute MSO, I would like to discuss RCM, medical billing, automation, or ChargePilot services."
};

function each(selector, callback) {
  Array.prototype.slice.call(document.querySelectorAll(selector)).forEach(callback);
}

function setText(selector, text) {
  each(selector, function (el) { el.textContent = text; });
}

setText("[data-year]", String(new Date().getFullYear()));

var toggle = document.querySelector(".menu-toggle");
var mainNav = document.querySelector(".main-nav");
if (toggle && mainNav) {
  toggle.addEventListener("click", function () {
    var open = mainNav.classList.toggle("open");
    toggle.setAttribute("aria-expanded", String(open));
  });
}

each(".has-dropdown", function (item) {
  var caret = item.querySelector(".nav-caret");
  if (!caret) return;
  item.addEventListener("mouseenter", function () { caret.setAttribute("aria-expanded", "true"); });
  item.addEventListener("mouseleave", function () { caret.setAttribute("aria-expanded", "false"); });
});

if ("IntersectionObserver" in window) {
  var revealObserver = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });
  each(".reveal", function (el) { revealObserver.observe(el); });
} else {
  each(".reveal", function (el) { el.classList.add("is-visible"); });
}

function cleanSupabaseUrl(url) {
  return url && url.charAt(url.length - 1) === "/" ? url.slice(0, -1) : url;
}

function supabaseInsert(table, payload) {
  var cfg = window.RESOLUTE_CONFIG || {};
  if (!cfg.supabaseUrl || !cfg.supabaseAnonKey || !window.fetch) return Promise.resolve(false);
  var endpoint = cleanSupabaseUrl(cfg.supabaseUrl) + "/rest/v1/" + table;
  return fetch(endpoint, {
    method: "POST",
    headers: {
      apikey: cfg.supabaseAnonKey,
      Authorization: "Bearer " + cfg.supabaseAnonKey,
      "Content-Type": "application/json",
      Prefer: "return=minimal"
    },
    body: JSON.stringify(payload)
  }).then(function (response) { return response.ok; }).catch(function () { return false; });
}

function getFormData(form) {
  var data = {};
  Array.prototype.slice.call(new FormData(form).entries()).forEach(function (entry) {
    data[entry[0]] = entry[1];
  });
  return data;
}

function sendSupportEmail(subject, data, message) {
  var cfg = window.RESOLUTE_CONFIG || {};
  var endpoint = cfg.formEndpoint || "https://formsubmit.co/ajax/support@resolutemso.com";
  if (!endpoint || !window.fetch) return Promise.resolve(false);
  var payload = Object.assign({}, data || {}, {
    _subject: subject,
    subject: subject,
    message: message || "",
    source: "Resolute MSO website",
    to: SITE.email,
    phi_notice: "No PHI requested on this public form.",
    _template: "table",
    _captcha: "false"
  });
  return fetch(endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify(payload)
  }).then(function (response) { return response.ok; }).catch(function () { return false; });
}
each(".portal-tab", function (button) {
  button.addEventListener("click", function () {
    each(".portal-tab", function (item) { item.classList.remove("active"); });
    button.classList.add("active");
    var role = button.getAttribute("data-portal");
    var title = document.querySelector("[data-portal-title]");
    var adminPanel = document.querySelector("[data-admin-panel]");
    var employeePanel = document.querySelector("[data-employee-panel]");
    if (title) title.textContent = role === "admin" ? "Admin Dashboard" : "Employee Dashboard";
    if (adminPanel) adminPanel.classList.toggle("hidden", role !== "admin");
    if (employeePanel) employeePanel.classList.toggle("hidden", role !== "employee");
  });
});

var previewButton = document.querySelector("[data-login-preview]");
if (previewButton) {
  previewButton.addEventListener("click", function () {
    var note = document.querySelector(".login-card p");
    if (note) note.textContent = "Preview loaded. Connect Supabase authentication before production use.";
  });
}

if (window.fetch) {
  fetch("content/site-config.json").then(function (response) { return response.ok ? response.json() : null; }).then(function (config) {
    if (!config) return;
    each("[data-config-email]", function (el) { el.textContent = config.primaryEmail || SITE.email; });
  }).catch(function () {});
}

(function(){
  function ready(fn){ if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn); else fn(); }
  ready(function(){
    function eachLocal(selector, callback){ Array.prototype.slice.call(document.querySelectorAll(selector)).forEach(callback); }
    var modal = document.querySelector('[data-demo-modal]');
    if (!modal) return;
    var firstInput = modal.querySelector('input,select,textarea,button');
    function openModal(event){ if(event) event.preventDefault(); modal.removeAttribute('hidden'); document.body.classList.add('modal-open'); setTimeout(function(){ if(firstInput) firstInput.focus(); }, 30); }
    function closeModal(event){ if(event) event.preventDefault(); modal.setAttribute('hidden',''); document.body.classList.remove('modal-open'); }
    eachLocal('[data-open-demo], .nav-demo, a[href="#demo"], a[href="index.html#demo"], a[href="#ask-demo"]', function(el){ el.setAttribute('href','#ask-demo'); el.setAttribute('data-open-demo',''); el.addEventListener('click', openModal); });
    eachLocal('[data-close-demo]', function(el){ el.addEventListener('click', closeModal); });
    document.addEventListener('keydown', function(event){ if(event.key === 'Escape' && !modal.hasAttribute('hidden')) closeModal(event); });
  });
})();

(function(){
  var SUPPORT_EMAIL = 'support@resolutemso.com';
  var WHATSAPP_NUMBER = '17015525527';
  function encode(value){ return encodeURIComponent(value || ''); }
  function getDemoPayload(form){
    var name = (form.querySelector('[name="name"]') || {}).value || '';
    var email = (form.querySelector('[name="email"]') || {}).value || '';
    var service = (form.querySelector('[name="services_interested"]') || {}).value || '';
    return { name: name.trim(), email: email.trim(), service: service.trim() };
  }
  function buildMessage(data){
    return [
      'Hello Resolute MSO, I would like to book a demo.',
      'Name: ' + data.name,
      'Email: ' + data.email,
      'Services Interested: ' + data.service,
      '',
      'No PHI submitted.'
    ].join('\n');
  }
  window.resoluteAskDemoSubmit = function(form){
    var data = getDemoPayload(form);
    var status = form.querySelector('.form-status');
    if (!data.name || !data.email || !data.service) {
      if (status) status.textContent = 'Please fill name, email, and services interested.';
      return false;
    }
    var body = buildMessage(data);
    var button = form.querySelector('button[type="submit"]');
    if (button) button.disabled = true;
    if (status) status.textContent = 'Sending your demo request to Resolute MSO...';
    supabaseInsert('demo_requests', data).then(function(){
      return sendSupportEmail('Resolute MSO Book a Demo Request', data, body);
    }).then(function(sent){
      if (sent) {
        if (status) status.textContent = 'Demo request sent to support@resolutemso.com.';
        form.reset();
      } else if (status) {
        status.textContent = 'Email delivery is configured through FormSubmit. If this is the first submission, please confirm the activation email sent to support@resolutemso.com.';
      }
    }).finally(function(){ if (button) button.disabled = false; });
    return false;
  };
  function attachDemoForms(){
    Array.prototype.slice.call(document.querySelectorAll('#demo-form')).forEach(function(form){
      form.setAttribute('onsubmit', 'return resoluteAskDemoSubmit(this)');
      var button = form.querySelector('button[type="submit"]');
      if (button) {
        button.removeAttribute('disabled');
        button.setAttribute('aria-disabled', 'false');
        button.style.pointerEvents = 'auto';
      }
      var whatsappLink = form.querySelector('[data-whatsapp-demo]');
      var updateLink = function(){
        var data = getDemoPayload(form);
        if (whatsappLink) whatsappLink.href = 'https://wa.me/' + WHATSAPP_NUMBER + '?text=' + encode(buildMessage(data));
      };
      form.addEventListener('input', updateLink);
      updateLink();
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', attachDemoForms);
  else attachDemoForms();
  document.addEventListener('submit', function(event){
    if (event.target && event.target.id === 'demo-form') {
      event.preventDefault();
      event.stopImmediatePropagation();
      window.resoluteAskDemoSubmit(event.target);
    }
  }, true);
})();

(function(){
  function contactMessage(data){
    return [
      'Resolute MSO website contact request.',
      'Name: ' + (data.name || ''),
      'Email: ' + (data.email || ''),
      'Phone: ' + (data.phone || ''),
      'Organization: ' + (data.organization || ''),
      'Service Interest: ' + (data.service_interest || ''),
      'Message: ' + (data.message || ''),
      '',
      'No PHI submitted.'
    ].join('\n');
  }
  function attachContactForm(){
    var contactForm = document.getElementById('contact-form');
    if (!contactForm || contactForm.getAttribute('data-direct-handler') === 'ready') return;
    contactForm.setAttribute('data-direct-handler', 'ready');
    contactForm.addEventListener('submit', function(event){
      event.preventDefault();
      event.stopImmediatePropagation();
      var data = getFormData(contactForm);
      var status = contactForm.querySelector('.form-status');
      var submitButton = contactForm.querySelector('button[type="submit"]');
      var body = contactMessage(data);
      if (status) status.textContent = 'Sending your message to Resolute MSO...';
      if (submitButton) submitButton.disabled = true;
      supabaseInsert('contact_messages', data).then(function(){
        return sendSupportEmail('Resolute MSO Website Contact Request', data, body);
      }).then(function(sent){
        if (sent) {
          if (status) status.textContent = 'Message sent to support@resolutemso.com.';
          contactForm.reset();
        } else if (status) {
          status.textContent = 'Email delivery is configured through FormSubmit. If this is the first submission, please confirm the activation email sent to support@resolutemso.com.';
        }
      }).finally(function(){
        if (submitButton) submitButton.disabled = false;
      });
    }, true);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', attachContactForm);
  else attachContactForm();
})();

(function(){
  function attachNewsletter(){
    Array.prototype.slice.call(document.querySelectorAll('#newsletter-form')).forEach(function(form){
      if (form.getAttribute('data-newsletter-ready') === 'true') return;
      form.setAttribute('data-newsletter-ready', 'true');
      form.addEventListener('submit', function(event){
        event.preventDefault();
        event.stopPropagation();
        var emailInput = form.querySelector('[name="email"]');
        var email = emailInput ? emailInput.value.trim() : '';
        var status = form.querySelector('.form-status');
        var btn = form.querySelector('button[type="submit"]');
        if (!email) { if(status) status.textContent = 'Please enter your email.'; return; }
        if(status) status.textContent = 'Sending bulletin signup to Resolute MSO...';
        if(btn) btn.disabled = true;
        var payload = { email: email, signup_note: 'Sign up for Bulletin & Updates', source_area: 'Footer Bulletin & Updates' };
        supabaseInsert('newsletter_subscribers', payload).then(function(){
          return sendSupportEmail('Sign up for Bulletin & Updates', payload, 'Please add this email to the Resolute MSO bulletin and updates directory: ' + email);
        }).then(function(sent){
          if (sent) {
            if(status) status.textContent = 'Signup sent to support@resolutemso.com.';
            form.reset();
          } else if(status) {
            status.textContent = 'Signup captured locally. Please confirm the FormSubmit activation email for support@resolutemso.com if this is the first submission.';
          }
        }).finally(function(){ if(btn) btn.disabled = false; });
      }, true);
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', attachNewsletter);
  else attachNewsletter();
})();
