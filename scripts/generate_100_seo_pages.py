from __future__ import annotations

import html
import json
import re
from datetime import date
from pathlib import Path

BASE = "https://www.resolutemso.com"
TODAY = date.today().isoformat()

GROUPS = {
    "RCM Services": [
        "Medical Billing Services", "Revenue Cycle Management Services", "Denial Management Services", "AR Follow Up Services", "Eligibility Verification Services", "Prior Authorization Services", "Payment Posting Services", "Medical Coding Services", "Claim Submission Services", "Claim Scrubbing Services", "Credentialing Services", "Provider Enrollment Services", "RCM Reporting Services", "Billing Audit Services", "Insurance Verification Services", "Patient Statement Services", "ERA and EFT Enrollment Services", "Clearinghouse Support Services", "RCM Process Improvement", "Revenue Leakage Analysis"
    ],
    "Specialty Billing": [
        "Clinical Lab Billing Services", "Toxicology Lab Billing Services", "Molecular Lab Billing Services", "Pathology Billing Services", "Imaging Center Billing Services", "Radiology Billing Services", "Urgent Care Billing Services", "Primary Care Billing Services", "Internal Medicine Billing Services", "Family Practice Billing Services", "Cardiology Billing Services", "Mental Health Billing Services", "Physical Therapy Billing Services", "Chiropractic Billing Services", "DME Billing Services", "Pain Management Billing Services", "Dermatology Billing Services", "Pediatrics Billing Services", "OBGYN Billing Services", "Podiatry Billing Services"
    ],
    "Automation and AI": [
        "Medical Billing Automation", "RCM Automation", "OfficeAlly Claim Entry Automation", "Charge Entry Automation", "Eligibility Automation", "Denial Workflow Automation", "AR Follow Up Automation", "Reporting Automation", "Payment Posting Automation", "Practice Management Automation", "Healthcare Workflow Automation", "AI in Medical Billing", "AI Revenue Cycle Management", "RCM Dashboard Automation", "Practice Health Dashboard", "ChargePilot OfficeAlly Automation", "ChargePilot Implementation", "ChargePilot Pricing", "ChargePilot Support", "Billing Software Automation"
    ],
    "Buyer Intent": [
        "Best Medical Billing Company for Small Practices", "Medical Billing Company for Physician Groups", "Medical Billing Outsourcing Company", "RCM Outsourcing Services", "Medical Billing Company vs In House Billing", "RCM Outsourcing vs In House Team", "When to Outsource Medical Billing", "How to Choose an RCM Partner", "Medical Billing Audit Checklist", "Reduce Claim Denials", "Improve Clean Claim Rate", "Reduce AR Over 90 Days", "Improve Net Collection Rate", "First Pass Claim Rate Improvement", "Healthcare Revenue Recovery Services", "Small Practice RCM Support", "Provider Billing Support Company", "Medical Billing Cost Reduction", "RCM KPI Dashboard Services", "Practice Revenue Optimization"
    ],
    "Guides and Resources": [
        "Medical Billing Beginner Guide", "Revenue Cycle Management Beginner Guide", "Denial Management Guide", "AR Follow Up Guide", "Clean Claim Playbook", "Eligibility Verification Guide", "Prior Authorization Guide", "Payment Posting Guide", "Charge Entry Guide", "Claim Rejection Guide", "RCM KPI Guide", "Days in AR Guide", "Net Collection Rate Guide", "First Pass Rate Guide", "HIPAA Conscious Website Forms", "OfficeAlly Automation Guide", "Clinical Lab Billing Guide", "Imaging Billing Guide", "Urgent Care Billing Guide", "AI Powered RCM Guide"
    ],
}

CORE_PAGES = [
    ("/", "Home"),
    ("/about.html", "About Resolute MSO"),
    ("/services.html", "Services"),
    ("/automation-suite.html", "Automation Suite"),
    ("/chargepilot.html", "ChargePilot"),
    ("/practice-health-dashboard.html", "Practice Health Dashboard"),
    ("/free-rcm-audit.html", "Free RCM Audit"),
    ("/contact.html", "Contact"),
    ("/quality-compliance.html", "Quality Commitment"),
    ("/service-quality-feedback.html", "Service Feedback"),
    ("/compliance.html", "Compliance"),
    ("/privacy.html", "Privacy Policy"),
]

CATEGORY_COPY = {
    "RCM Services": {
        "audience": "practice managers, billing leaders, physician owners, and healthcare providers",
        "problem": "revenue leakage, delayed reimbursements, avoidable denials, incomplete follow-up, and unclear billing accountability",
        "solution": "disciplined RCM execution, cleaner work queues, denial prevention, AR visibility, and leadership-ready reporting",
    },
    "Specialty Billing": {
        "audience": "specialty providers, laboratories, imaging centers, urgent cares, and physician groups",
        "problem": "specialty-specific payer rules, documentation gaps, modifier issues, authorization risk, and aging receivables",
        "solution": "specialty-aware billing workflows, payer-focused claim review, denial root-cause tracking, and stronger AR movement",
    },
    "Automation and AI": {
        "audience": "RCM teams, billing companies, provider groups, and operations leaders",
        "problem": "manual claim entry, repetitive eligibility checks, delayed reporting, inconsistent follow-up, and limited operational visibility",
        "solution": "AI-assisted automation, workflow routing, ChargePilot automation, dashboards, exception handling, and human oversight",
    },
    "Buyer Intent": {
        "audience": "providers comparing RCM vendors, billing partners, automation tools, and outsourcing options",
        "problem": "unclear vendor accountability, hidden revenue leakage, staffing pressure, slow cash movement, and weak performance reporting",
        "solution": "transparent RCM partnership, operational diagnostics, automation readiness, measurable KPIs, and a focused free RCM audit path",
    },
    "Guides and Resources": {
        "audience": "healthcare providers, students, billing teams, RCM managers, and operations leaders",
        "problem": "confusing billing terminology, unclear KPIs, payer follow-up complexity, denial prevention gaps, and inconsistent training",
        "solution": "clear educational guidance, practical workflows, healthcare billing checklists, and Resolute MSO support pathways",
    },
}

RELATED_CORE = [
    ("/medical-billing-services.html", "Medical Billing Services"),
    ("/revenue-cycle-management-services.html", "Revenue Cycle Management"),
    ("/denial-management-services.html", "Denial Management"),
    ("/ar-follow-up-services.html", "AR Follow-Up"),
    ("/medical-billing-automation.html", "Medical Billing Automation"),
    ("/chargepilot.html", "ChargePilot"),
    ("/free-rcm-audit.html", "Free RCM Audit"),
    ("/contact.html", "Contact Resolute MSO"),
]


def slugify(title: str) -> str:
    text = title.lower().replace("&", "and")
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text


def page_keywords(title: str, group: str) -> list[str]:
    base = [title.lower(), "medical billing", "revenue cycle management", "RCM services", "healthcare provider", "billing company", "healthcare automation", "denial management", "AR follow up", "clean claim rate"]
    if "Automation" in group or "AI" in group:
        base += ["AI medical billing", "RCM automation", "OfficeAlly automation", "billing software automation", "ChargePilot"]
    if "Specialty" in group:
        base += ["specialty billing", "provider billing", "claim submission", "payer follow up", "coding review"]
    if "Buyer" in group:
        base += ["best medical billing company", "RCM outsourcing", "billing partner", "reduce AR", "increase collections"]
    return list(dict.fromkeys(base))[:14]


def header(active: str = "") -> str:
    return '''<header class="site-header" data-header><a class="skip-link" href="#main">Skip to content</a><div class="nav-shell"><a class="brand" href="/" aria-label="Resolute MSO home"><img src="/assets/img/resolute-mso-logo.jpeg" alt="Resolute MSO logo" width="920" height="249" decoding="async"></a><button class="menu-toggle" type="button" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button><nav class="main-nav" aria-label="Primary navigation"><ul><li class="has-dropdown"><a href="/automation-suite.html">Automation Suite</a><button class="nav-caret" aria-expanded="false" aria-label="Open Automation Suite menu"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M5 12h14"/><path d="M13 6l6 6-6 6"/></svg></button><div class="dropdown" role="menu"><a href="/chargepilot.html" role="menuitem">ChargePilot</a><a href="/rcm-automation.html" role="menuitem">RCM Automation</a><a href="/practice-health-dashboard.html" role="menuitem">Practice Health Dashboard</a><a href="/automation-suite.html" role="menuitem">See More</a></div></li><li class="has-dropdown"><a href="/services.html">Services</a><button class="nav-caret" aria-expanded="false" aria-label="Open Services menu"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M5 12h14"/><path d="M13 6l6 6-6 6"/></svg></button><div class="dropdown" role="menu"><a href="/medical-billing-services.html" role="menuitem">Medical Billing Services</a><a href="/revenue-cycle-management-services.html" role="menuitem">Revenue Cycle Management</a><a href="/denial-management-services.html" role="menuitem">Denial Management</a><a href="/services.html" role="menuitem">See More</a></div></li><li class="has-dropdown"><a href="/specialties.html">Specialties</a><button class="nav-caret" aria-expanded="false" aria-label="Open Specialties menu"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M5 12h14"/><path d="M13 6l6 6-6 6"/></svg></button><div class="dropdown" role="menu"><a href="/medical-billing-services-for-physician-groups.html" role="menuitem">Physician Groups</a><a href="/imaging-center-billing-services.html" role="menuitem">Imaging & Radiology</a><a href="/clinical-lab-billing-services.html" role="menuitem">Clinical Laboratories</a><a href="/specialties.html" role="menuitem">See More</a></div></li><li class="has-dropdown"><a href="/resources.html">Resources</a><button class="nav-caret" aria-expanded="false" aria-label="Open Resources menu"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M5 12h14"/><path d="M13 6l6 6-6 6"/></svg></button><div class="dropdown" role="menu"><a href="/rcm-insights.html" role="menuitem">RCM Insights</a><a href="/automation-updates.html" role="menuitem">Automation Updates</a><a href="/healthcare-operations.html" role="menuitem">Healthcare Operations</a><a href="/resources.html" role="menuitem">See More</a></div></li><li class="has-dropdown"><a href="/about.html">Company</a><button class="nav-caret" aria-expanded="false" aria-label="Open Company menu"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M5 12h14"/><path d="M13 6l6 6-6 6"/></svg></button><div class="dropdown" role="menu"><a href="/about.html" role="menuitem">About Resolute MSO</a><a href="/quality-compliance.html" role="menuitem">Quality Commitment</a><a href="/compliance.html" role="menuitem">Compliance</a><a href="/about.html" role="menuitem">See More</a></div></li><li><a href="/contact.html">Contact</a></li></ul></nav><a class="nav-demo btn btn-small ask-demo-btn" href="/contact.html">Book a Demo</a></div></header>'''


def faq_json(title: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": f"What is {title}?", "acceptedAnswer": {"@type": "Answer", "text": f"{title} is a Resolute MSO focus area designed to help healthcare providers improve billing accuracy, revenue cycle visibility, claim movement, denial prevention, and operational accountability."}},
            {"@type": "Question", "name": f"Who needs {title}?", "acceptedAnswer": {"@type": "Answer", "text": "Healthcare providers, physician groups, clinics, laboratories, imaging centers, urgent cares, and billing teams that want cleaner workflows, stronger reporting, and better reimbursement control can benefit."}},
            {"@type": "Question", "name": "How does Resolute MSO support this area?", "acceptedAnswer": {"@type": "Answer", "text": "Resolute MSO combines RCM expertise, process improvement, automation readiness, analytics, and human oversight to reduce leakage and improve performance."}},
        ],
    }


def service_json(title: str, desc: str, slug: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": title,
        "serviceType": title,
        "provider": {"@type": "Organization", "name": "Resolute MSO", "url": BASE},
        "areaServed": "United States",
        "url": f"{BASE}/{slug}.html",
        "description": desc,
    }


def render_page(title: str, group: str, idx: int) -> str:
    slug = slugify(title)
    c = CATEGORY_COPY[group]
    keywords = page_keywords(title, group)
    desc = f"{title} from Resolute MSO helps U.S. healthcare providers improve RCM performance, billing accuracy, denial prevention, AR movement, automation readiness, and revenue visibility."
    related = [x for x in RELATED_CORE if slugify(x[1]) != slug][:6]
    keyword_spans = "".join(f"<span>{html.escape(k)}</span>" for k in keywords)
    related_links = "".join(f"<a href='{href}'>{text}</a>" for href, text in related)
    faq = faq_json(title)
    service = service_json(title, desc, slug)
    page = f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>{html.escape(title)} | Resolute MSO</title>
  <meta name=\"description\" content=\"{html.escape(desc)}\">
  <link rel=\"canonical\" href=\"{BASE}/{slug}.html\">
  <meta name=\"robots\" content=\"index, follow, max-image-preview:large, max-snippet:-1\">
  <meta property=\"og:type\" content=\"website\">
  <meta property=\"og:title\" content=\"{html.escape(title)} | Resolute MSO\">
  <meta property=\"og:description\" content=\"{html.escape(desc)}\">
  <meta property=\"og:url\" content=\"{BASE}/{slug}.html\">
  <meta property=\"og:image\" content=\"{BASE}/assets/img/rcm-operations-ai.jpg\">
  <meta name=\"twitter:card\" content=\"summary_large_image\">
  <link rel=\"stylesheet\" href=\"/assets/css/styles.css\">
  <link rel=\"stylesheet\" href=\"/assets/css/super-upgrade.css\">
  <link rel=\"icon\" type=\"image/png\" sizes=\"32x32\" href=\"/assets/img/favicon-32.png\">
  <script type=\"application/ld+json\">{json.dumps(service, separators=(',', ':'))}</script>
  <script type=\"application/ld+json\">{json.dumps(faq, separators=(',', ':'))}</script>
</head>
<body data-page=\"seo-authority\">
{header()}
<main id=\"main\">
  <section class=\"sub-hero section-dark\"><div class=\"container hero-grid\"><div><p class=\"kicker\">{html.escape(group)} • Resolute MSO</p><h1>{html.escape(title)} for U.S. Healthcare Providers</h1><p class=\"lead\">{html.escape(desc)} This page is written for {html.escape(c['audience'])} searching for practical, expert-level support.</p><div class=\"hero-actions\"><a class=\"btn\" href=\"/free-rcm-audit.html\">Request Free RCM Audit</a><a class=\"btn btn-ghost\" href=\"/contact.html\">Talk to Resolute MSO</a></div></div><div class=\"visual-panel glow-card about-wide-visual\"><img src=\"/assets/img/rcm-operations-ai.jpg\" alt=\"Healthcare revenue cycle team reviewing {html.escape(title)} workflows\" width=\"1200\" height=\"675\" loading=\"eager\" decoding=\"async\"></div></div></section>
  <section class=\"section\"><div class=\"container split\"><div><p class=\"kicker\">Provider Search Intent</p><h2>Why {html.escape(title.lower())} matters.</h2><p>{html.escape(title)} is important when healthcare organizations face {html.escape(c['problem'])}. Providers often search for this support when cash flow slows, claims age, denials increase, or internal teams cannot clearly see the next best action.</p><p>Resolute MSO approaches this area with {html.escape(c['solution'])}. The goal is not only more activity; the goal is cleaner revenue movement, better accountability, and fewer avoidable surprises for leadership.</p></div><div class=\"card accent-card\"><h3>High-intent keywords covered</h3><div class=\"seo-badge-row\">{keyword_spans}</div></div></div></section>
  <section class=\"section section-soft\"><div class=\"container\"><div class=\"section-head\"><p class=\"kicker\">Operating Model</p><h2>How Resolute MSO supports {html.escape(title.lower())}.</h2></div><div class=\"card-grid three\"><article class=\"card\"><h3>1. Diagnose leakage</h3><p>We review workflow signals such as eligibility gaps, claim edits, denial categories, payer behavior, AR aging, documentation issues, and reporting blind spots.</p></article><article class=\"card\"><h3>2. Improve execution</h3><p>We align billing, follow-up, denial prevention, automation readiness, and accountability so the work becomes measurable and easier to manage.</p></article><article class=\"card\"><h3>3. Report what matters</h3><p>Leadership needs visibility into clean claims, denials, aging AR, productivity, payer actions, and revenue risk. We focus reporting around those signals.</p></article></div></div></section>
  <section class=\"section\"><div class=\"container split\"><div class=\"card\"><h3>Recommended next step</h3><p>Start with a focused RCM audit. Resolute MSO can review your current revenue cycle pressure points and identify whether service support, automation, or dashboard visibility should be prioritized first.</p><a class=\"btn\" href=\"/free-rcm-audit.html\">Start Free Audit</a></div><div><p class=\"kicker\">Related Pages</p><h2>Continue exploring Resolute MSO solutions.</h2><div class=\"seo-link-grid\">{related_links}</div></div></div></section>
  <section class=\"section section-soft\"><div class=\"container\"><div class=\"section-head\"><p class=\"kicker\">FAQ</p><h2>Questions providers ask about {html.escape(title.lower())}.</h2></div><div class=\"card-grid three\"><article class=\"card\"><h3>What is {html.escape(title)}?</h3><p>It is a Resolute MSO service or knowledge area focused on improving revenue cycle performance, billing accuracy, workflow visibility, and operational control.</p></article><article class=\"card\"><h3>Can automation help?</h3><p>Automation can help when tasks are repetitive, rules are clear, and exceptions are reviewed by trained people. Resolute MSO uses automation as a support layer, not a replacement for expert judgment.</p></article><article class=\"card\"><h3>How do we begin?</h3><p>Begin with a discovery call or free RCM audit. We identify the biggest financial and operational friction points before recommending a service path.</p></article></div></div></section>
</main>
<footer class=\"site-footer\"></footer><a class=\"whatsapp-float\" href=\"https://wa.me/17015525527?text=Hello%20Resolute%20MSO%2C%20I%20would%20like%20to%20discuss%20RCM%2C%20medical%20billing%2C%20automation%2C%20or%20ChargePilot%20services.\" target=\"_blank\" rel=\"noopener\" aria-label=\"Talk on WhatsApp\"><span>Talk on WhatsApp</span></a>
<script src=\"/config.js\" defer></script><script src=\"/assets/js/main.js\" defer></script><script src=\"/assets/js/super-upgrade.js\" defer></script>
</body></html>"""
    return page


def render_hub(pages: list[dict]) -> str:
    groups_html = []
    for group in GROUPS:
        links = [p for p in pages if p["group"] == group]
        cards = "".join(f"<a class='card link-card' href='/{p['slug']}.html'><h3>{html.escape(p['title'])}</h3><p>{html.escape(p['description'])}</p></a>" for p in links)
        groups_html.append(f"<section class='section' id='{slugify(group)}'><div class='container'><div class='section-head'><p class='kicker'>{html.escape(group)}</p><h2>{html.escape(group)} pages</h2><p>Focused Resolute MSO pages for healthcare providers, billing leaders, and RCM decision-makers.</p></div><div class='card-grid three'>{cards}</div></div></section>")
    return f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'><title>All RCM Solutions | Resolute MSO</title><meta name='description' content='Explore 100 Resolute MSO pages covering medical billing, RCM services, specialty billing, healthcare automation, ChargePilot, denial management, AR follow-up, and provider revenue growth.'><link rel='canonical' href='{BASE}/all-rcm-solutions.html'><meta name='robots' content='index, follow, max-image-preview:large, max-snippet:-1'><link rel='stylesheet' href='/assets/css/styles.css'><link rel='stylesheet' href='/assets/css/super-upgrade.css'></head><body data-page='all-rcm-solutions.html'>{header()}<main id='main'><section class='sub-hero section-dark'><div class='container'><p class='kicker'>Resolute MSO SEO Authority Hub</p><h1>All RCM, medical billing, automation, and healthcare provider solutions.</h1><p class='lead'>A complete hub for healthcare providers searching for billing services, RCM outsourcing, denial management, AR follow-up, healthcare automation, ChargePilot, dashboards, specialty billing, and practical revenue cycle education.</p><div class='hero-actions'><a class='btn' href='/free-rcm-audit.html'>Request Free RCM Audit</a><a class='btn btn-ghost' href='/contact.html'>Contact Resolute MSO</a></div></div></section>{''.join(groups_html)}</main><footer class='site-footer'></footer><script src='/config.js' defer></script><script src='/assets/js/main.js' defer></script><script src='/assets/js/super-upgrade.js' defer></script></body></html>"""


def sitemap_xml(pages: list[dict]) -> str:
    urls = [(BASE + href, "weekly", "0.90") for href, _ in CORE_PAGES]
    urls.append((f"{BASE}/all-rcm-solutions.html", "weekly", "0.88"))
    urls.extend((f"{BASE}/{p['slug']}.html", "monthly", "0.74") for p in pages)
    body = "\n".join(f"  <url><loc>{loc}</loc><lastmod>{TODAY}</lastmod><changefreq>{freq}</changefreq><priority>{pri}</priority></url>" for loc, freq, pri in urls)
    return f"<?xml version='1.0' encoding='UTF-8'?>\n<urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>\n{body}\n</urlset>\n"


def llms_text(pages: list[dict]) -> str:
    lines = [
        "# Resolute MSO",
        "",
        "Resolute MSO provides healthcare revenue cycle management, medical billing, denial management, AR follow-up, automation, dashboards, ChargePilot OfficeAlly automation, specialty billing, and healthcare operations support for U.S. healthcare providers.",
        "",
        "## Core pages",
    ]
    lines += [f"- {title}: {BASE}{href}" for href, title in CORE_PAGES]
    lines += ["", "## 100-page RCM authority library", f"- All RCM Solutions: {BASE}/all-rcm-solutions.html"]
    for p in pages:
        lines.append(f"- {p['title']}: {BASE}/{p['slug']}.html")
    return "\n".join(lines) + "\n"


def main() -> None:
    pages: list[dict] = []
    count = 0
    for group, titles in GROUPS.items():
        for title in titles:
            count += 1
            slug = slugify(title)
            desc = f"{title} from Resolute MSO helps U.S. healthcare providers improve RCM performance, billing accuracy, denial prevention, AR movement, automation readiness, and revenue visibility."
            Path(f"{slug}.html").write_text(render_page(title, group, count), encoding="utf-8")
            pages.append({"title": title, "slug": slug, "group": group, "description": desc})
    Path("all-rcm-solutions.html").write_text(render_hub(pages), encoding="utf-8")
    Path("sitemap.xml").write_text(sitemap_xml(pages), encoding="utf-8")
    Path("llms.txt").write_text(llms_text(pages), encoding="utf-8")
    print(f"Generated {len(pages)} SEO authority pages plus hub, sitemap, and llms.txt")


if __name__ == "__main__":
    main()
