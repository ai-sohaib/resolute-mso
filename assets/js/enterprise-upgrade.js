(function () {
  "use strict";

  const TITLE = "AI-Driven Medical Billing & RCM That Stops Revenue Leakage";
  const DESCRIPTION = "Resolute MSO helps U.S. healthcare providers improve medical billing and RCM, reduce denials, recover AR, and use automation to strengthen revenue workflows.";
  const AUDIT_SUCCESS = "Thank you. Your free audit request has been received. A Resolute MSO specialist will contact you shortly.";
  const CFG = () => (window.RESOLUTE_CONFIG = window.RESOLUTE_CONFIG || {});
  let modal;
  let returnFocus;

  const icon = '<svg class="r-whatsapp-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M12.04 2C6.52 2 2.03 6.45 2.03 11.93c0 1.75.46 3.46 1.33 4.96L2 22l5.25-1.35a10.1 10.1 0 0 0 4.79 1.22c5.52 0 10.01-4.45 10.01-9.94S17.56 2 12.04 2Zm0 18.18c-1.52 0-3-.41-4.3-1.18l-.31-.18-3.11.8.83-3.01-.2-.31a8.16 8.16 0 0 1-1.25-4.37c0-4.55 3.74-8.25 8.34-8.25s8.34 3.7 8.34 8.25-3.74 8.25-8.34 8.25Zm4.57-6.18c-.25-.12-1.48-.73-1.71-.81-.23-.08-.4-.12-.57.12-.17.25-.65.81-.8.98-.15.17-.3.19-.55.06-.25-.12-1.06-.39-2.02-1.24-.75-.66-1.25-1.48-1.4-1.73-.15-.25-.02-.38.11-.51.11-.11.25-.3.37-.45.12-.15.17-.25.25-.42.08-.17.04-.31-.02-.43-.06-.12-.57-1.36-.78-1.86-.21-.5-.41-.43-.57-.44h-.49c-.17 0-.43.06-.66.31-.23.25-.87.85-.87 2.07s.89 2.4 1.02 2.56c.12.17 1.75 2.65 4.25 3.72.59.25 1.06.4 1.42.51.6.19 1.14.16 1.57.1.48-.07 1.48-.6 1.69-1.18.21-.58.21-1.08.15-1.18-.06-.1-.23-.16-.48-.28Z"/></svg>';

  function esc(value) {
    return String(value).replace(/[&<>"']/g, c => ({ "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;" })[c]);
  }

  function waUrl() {
    const number = String(CFG().whatsappNumber || "").replace(/\D/g, "");
    const message = CFG().whatsappMessage || "Hello Resolute MSO, I would like to discuss your medical billing, RCM, or healthcare automation services.";
    return number ? `https://wa.me/${number}?text=${encodeURIComponent(message)}` : "";
  }

  function hydrateWhatsApp() {
    const url = waUrl();
    if (!url) return;
    document.querySelectorAll(".whatsapp-panel").forEach(panel => { panel.hidden = true; panel.setAttribute("aria-hidden", "true"); });
    document.querySelectorAll(".whatsapp-launch").forEach(control => {
      if (control.tagName === "A") return;
      const link = document.createElement("a");
      link.className = control.className;
      link.innerHTML = control.innerHTML || icon;
      control.replaceWith(link);
    });
    document.querySelectorAll("[data-whatsapp-link], .whatsapp-launch, a[href*='wa.me/']").forEach(link => {
      link.href = url;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      link.removeAttribute("aria-controls");
      link.removeAttribute("aria-expanded");
      link.classList.add("btn-whatsapp");
      link.setAttribute("aria-label", "Talk with Resolute MSO on WhatsApp");
      if (!link.querySelector("svg") && /whatsapp/i.test(link.textContent || "")) link.insertAdjacentHTML("afterbegin", icon);
    });
  }

  function updateHomepage() {
    const path = location.pathname.replace(/\/(?:index|home)\.html$/, "/");
    if (path !== "/") return;
    document.title = TITLE;
    [["meta[name='description']", DESCRIPTION],["meta[property='og:title']", TITLE],["meta[property='og:description']", DESCRIPTION],["meta[name='twitter:title']", TITLE],["meta[name='twitter:description']", DESCRIPTION]]
      .forEach(([selector, value]) => { const node = document.querySelector(selector); if (node) node.content = value; });
    const h1 = document.querySelector("main h1");
    if (h1) h1.textContent = TITLE;
    const lead = document.querySelector(".home-hero .lead, .r-hero-copy");
    if (lead) lead.textContent = "Resolute MSO combines expert medical billing, denial prevention, AR recovery, intelligent automation, and executive dashboards to help U.S. healthcare providers accelerate collections and gain control of their revenue cycle.";
    document.querySelectorAll(".home-hero a,.home-hero button,.r-hero a,.r-hero button").forEach(el => {
      if ((el.textContent || "").trim() === "View Automation Suite") {
        const button = el.tagName === "BUTTON" ? el : document.createElement("button");
        if (button !== el) { button.className = el.className; el.replaceWith(button); }
        button.type = "button";
        button.textContent = "Request a Free Audit";
        button.classList.add("btn-audit");
        button.dataset.openAudit = "";
      }
    });
  }

  const input = (name, label, type="text", required=false) =>
    `<div class="r-field"><label for="audit-${name}">${label}${required ? ' <span aria-hidden="true">*</span>' : ""}</label><input id="audit-${name}" name="${name}" type="${type}" maxlength="180"${required ? " required" : ""}></div>`;
  const textarea = (name, label, required=false) =>
    `<div class="r-field r-field-full"><label for="audit-${name}">${label}${required ? ' <span aria-hidden="true">*</span>' : ""}</label><textarea id="audit-${name}" name="${name}" maxlength="2000"${required ? " required" : ""}></textarea></div>`;
  const select = (name, label, values, required=false) =>
    `<div class="r-field"><label for="audit-${name}">${label}${required ? ' <span aria-hidden="true">*</span>' : ""}</label><select id="audit-${name}" name="${name}"${required ? " required" : ""}><option value="">Select an option</option>${values.map(v => `<option value="${esc(v)}">${esc(v)}</option>`).join("")}</select></div>`;

  function modalMarkup() {
    const services = ["Free RCM Audit","End-to-End RCM","Medical Billing and Coding","AR Follow-Up","Denial Management","Payment Posting","Eligibility and Benefits Verification","Credentialing","Reporting and Analytics","Modern Dashboards","ChargePilot™","Workflow Automation","Custom Healthcare Software","Remote Staffing","Other"];
    const serviceChoices = services.map((service, index) => `<label class="r-choice"><input type="checkbox" name="servicesOfInterest" value="${esc(service)}"${index === 0 ? " required" : ""}><span>${esc(service)}</span></label>`).join("");
    return `<section class="r-modal" id="free-audit-modal" role="dialog" aria-modal="true" aria-labelledby="free-audit-title" hidden>
      <div class="r-modal-backdrop" data-close-audit></div>
      <div class="r-modal-dialog" tabindex="-1">
        <header class="r-modal-header"><div><h2 id="free-audit-title">Request a Free RCM Audit</h2><p>Tell us about your organization and revenue-cycle priorities.</p></div><button class="r-modal-close" type="button" data-close-audit aria-label="Close free audit form">&times;</button></header>
        <div class="r-modal-body">
          <p class="r-form-warning">Do not submit protected health information, patient information, claim data, or medical records through this public form.</p>
          <form id="free-audit-form" data-resolute-form="free-audit" novalidate>
            <input type="hidden" name="formType" value="Free RCM Audit"><input type="hidden" name="pageSource"><input type="hidden" name="campaign"><input type="hidden" name="startedAt">
            <div class="r-honeypot" aria-hidden="true"><label>Website<input name="website" tabindex="-1" autocomplete="off"></label></div>
            <div class="r-form-grid">
              ${input("fullName","Full Name","text",true)}${input("workEmail","Work Email","email",true)}${input("phone","Phone Number","tel")}
              ${input("organizationName","Practice or Organization Name","text",true)}${input("jobTitle","Job Title")}
              ${select("organizationType","Organization Type",["Physician Practice","Provider Group","Clinical Laboratory","Imaging or Radiology Center","Urgent Care Center","Medical Billing Company","RCM Organization","MSO","Other"],true)}
              ${input("specialty","Specialty")}${input("state","State")}
              ${select("monthlyClaimVolume","Estimated Monthly Claim Volume",["Under 500","500–1,999","2,000–4,999","5,000–9,999","10,000–24,999","25,000+","Not sure"])}
              ${input("billingSoftware","Current Billing or PM Software")}
              <fieldset class="r-fieldset"><legend>Services of Interest <span aria-hidden="true">*</span></legend><div class="r-choice-grid">${serviceChoices}</div></fieldset>
              ${textarea("challenge","Main Revenue Cycle Challenge",true)}
              ${select("preferredContactMethod","Preferred Contact Method",["Email","Phone","WhatsApp"],true)}
              ${textarea("notes","Optional Notes")}
              <div class="r-field r-field-full"><label class="r-choice"><input type="checkbox" name="consent" value="yes" required><span>I consent to Resolute MSO contacting me about this business inquiry. I understand this public form must not contain PHI or patient information.</span></label></div>
            </div>
            <div class="r-form-actions"><button class="r-btn r-btn-audit" type="submit">Submit Free Audit Request</button><button class="r-btn r-btn-secondary" type="button" data-close-audit>Cancel</button></div>
            <p class="r-form-status" role="status" aria-live="polite"></p>
          </form>
        </div>
      </div>
    </section>`;
  }

  function ensureModal() {
    modal = document.getElementById("free-audit-modal");
    if (!modal) { document.body.insertAdjacentHTML("beforeend", modalMarkup()); modal = document.getElementById("free-audit-modal"); }
    return modal;
  }

  function openModal(trigger) {
    const dialog = ensureModal();
    returnFocus = trigger || document.activeElement;
    const form = dialog.querySelector("form");
    form.elements.pageSource.value = location.href;
    form.elements.campaign.value = JSON.stringify(Object.fromEntries([...new URLSearchParams(location.search)].filter(([k]) => /^(utm_|gclid|msclkid)/.test(k))));
    form.elements.startedAt.value = String(Date.now());
    dialog.hidden = false;
    document.body.classList.add("r-modal-open");
    requestAnimationFrame(() => dialog.querySelector(".r-modal-dialog").focus());
  }

  function closeModal() {
    if (!modal || modal.hidden) return;
    modal.hidden = true;
    document.body.classList.remove("r-modal-open");
    if (returnFocus && returnFocus.focus) returnFocus.focus();
  }

  function trapFocus(event) {
    if (!modal || modal.hidden) return;
    if (event.key === "Escape") { event.preventDefault(); closeModal(); return; }
    if (event.key !== "Tab") return;
    const items = [...modal.querySelectorAll('a[href],button:not([disabled]),input:not([disabled]):not([type="hidden"]),select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex="-1"])')].filter(el => el.offsetParent !== null);
    if (!items.length) return;
    if (event.shiftKey && document.activeElement === items[0]) { event.preventDefault(); items.at(-1).focus(); }
    else if (!event.shiftKey && document.activeElement === items.at(-1)) { event.preventDefault(); items[0].focus(); }
  }

  function tagLegacyForms() {
    document.querySelectorAll('form[action^="mailto:"],form[action*="formsubmit.co"],form.lead-form,form[data-lead-form]').forEach(form => {
      form.dataset.resoluteForm ||= "general-inquiry";
      form.removeAttribute("action"); form.removeAttribute("method");
      if (!form.querySelector(".r-form-status")) form.insertAdjacentHTML("beforeend", '<p class="r-form-status" role="status" aria-live="polite"></p>');
    });
  }

  function payload(form) {
    const data = {};
    new FormData(form).forEach((value, key) => {
      const clean = String(value).trim();
      if (key in data) data[key] = [].concat(data[key], clean); else data[key] = clean;
    });
    data.submittedAt = new Date().toISOString();
    data.pageSource ||= location.href;
    return data;
  }

  async function submit(form) {
    const status = form.querySelector(".r-form-status");
    const services = [...form.querySelectorAll('[name="servicesOfInterest"]')];
    if (services.length) services[0].setCustomValidity(services.some(box => box.checked) ? "" : "Select at least one service of interest.");
    if (!form.checkValidity()) { form.reportValidity(); status.dataset.state = "error"; status.textContent = "Review the highlighted fields and try again."; return; }
    const endpoint = String(CFG().formEndpoint || "").trim();
    if (!endpoint) { status.dataset.state = "error"; status.textContent = "Secure form delivery is not configured yet. Please email support@resolutemso.com."; return; }
    const button = form.querySelector('[type="submit"]');
    if (!button || button.disabled) return;
    const label = button.textContent;
    button.disabled = true; button.setAttribute("aria-busy","true"); button.textContent = "Submitting…"; status.textContent = "";
    try {
      const response = await fetch(endpoint, { method:"POST", headers:{"Content-Type":"application/json","Accept":"application/json"}, credentials:"omit", body:JSON.stringify(payload(form)) });
      const result = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(result.error || "Submission failed");
      status.dataset.state = "success";
      status.textContent = form.dataset.resoluteForm === "free-audit" ? AUDIT_SUCCESS : "Thank you. Your request has been received. A Resolute MSO specialist will contact you shortly.";
    } catch (error) {
      status.dataset.state = "error";
      status.textContent = "We could not submit your request. Your entries are still here—please retry or email support@resolutemso.com.";
      console.error("Resolute form submission failed", { name:error.name, message:error.message });
    } finally {
      button.disabled = false; button.removeAttribute("aria-busy"); button.textContent = label;
    }
  }

  function bind() {
    document.addEventListener("click", event => {
      const opener = event.target.closest("[data-open-audit]");
      if (opener) { event.preventDefault(); openModal(opener); }
      else if (event.target.closest("[data-close-audit]")) { event.preventDefault(); closeModal(); }
    });
    document.addEventListener("submit", event => {
      const form = event.target.closest("form[data-resolute-form]");
      if (form) { event.preventDefault(); submit(form); }
    });
    document.addEventListener("keydown", trapFocus);
    const toggle = document.querySelector(".r-nav-toggle");
    const nav = document.querySelector(".r-main-nav");
    if (toggle && nav) toggle.addEventListener("click", () => { const open = nav.dataset.open !== "true"; nav.dataset.open = String(open); toggle.setAttribute("aria-expanded", String(open)); });
  }

  function init() { updateHomepage(); ensureModal(); tagLegacyForms(); hydrateWhatsApp(); bind(); }
  document.readyState === "loading" ? document.addEventListener("DOMContentLoaded", init, { once:true }) : init();
})();
