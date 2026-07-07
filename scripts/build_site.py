from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import date
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE = "https://www.resolutemso.com"
TODAY = date(2026, 7, 2).isoformat()
OG_IMAGE = f"{SITE}/assets/img/resolute-mso-og.jpg"
FORM_ENDPOINT = "https://formsubmit.co/support@resolutemso.com"
WHATSAPP_NUMBER = "17015525527"
WHATSAPP_URL = "https://wa.me/17015525527?text=Hello%20Resolute%20MSO%2C%20I%27d%20like%20to%20discuss%20RCM%20and%20billing%20automation."
LINKEDIN_URL = "https://www.linkedin.com/company/resolutemso/"
LOGO_SRC = "/assets/img/resolute-mso-logo.webp"
LOGO_WIDTH = 460
LOGO_HEIGHT = 130
HOME_HERO_IMAGE = "/assets/img/rcm-team-standing-discussion.webp"


@dataclass
class Page:
    slug: str
    name: str
    category: str
    intent: str
    keywords: list[str]
    summary: str = ""
    cta: str = "Book a Revenue Audit"
    cta_href: str = "/free-rcm-audit/"
    secondary_cta: str = "Talk to Resolute MSO"
    secondary_href: str = WHATSAPP_URL
    template: str = "standard"
    noindex: bool = False
    related: list[str] = field(default_factory=list)

    @property
    def file(self) -> str:
        return "index.html" if self.slug == "index" else f"{self.slug}/index.html"

    @property
    def legacy_file(self) -> str:
        return f"{self.slug}.html"

    @property
    def url(self) -> str:
        return f"{SITE}/" if self.slug == "index" else f"{SITE}/{self.slug}/"

    @property
    def path(self) -> str:
        return "/" if self.slug == "index" else f"/{self.slug}/"


pages: list[Page] = []


def title_case_from_slug(slug: str) -> str:
    overrides = {
        "rcm": "RCM",
        "ar": "AR",
        "era": "ERA",
        "eft": "EFT",
        "dme": "DME",
        "obgyn": "OB/GYN",
        "fqhc": "FQHC",
        "hipaa": "HIPAA",
        "cpt": "CPT",
        "icd": "ICD",
        "officeally": "OfficeAlly",
        "chargepilot": "ChargePilot",
        "mso": "MSO",
        "ai": "AI",
        "lis": "LIS",
        "ehr": "EHR",
    }
    parts = []
    for part in slug.split("-"):
        parts.append(overrides.get(part, part.capitalize()))
    return " ".join(parts).replace("OB/GYN Billing", "OB/GYN Billing")


def add(
    slug: str,
    name: str | None = None,
    category: str = "service",
    intent: str = "Core service intent",
    keywords: list[str] | None = None,
    summary: str = "",
    cta: str = "Book a Revenue Audit",
    cta_href: str = "/free-rcm-audit/",
    secondary_cta: str = "Talk to Resolute MSO",
    secondary_href: str = WHATSAPP_URL,
    template: str = "standard",
    noindex: bool = False,
) -> None:
    display = name or title_case_from_slug(slug)
    base_keywords = keywords or []
    if not base_keywords:
        base_keywords = [display.lower(), "medical billing services", "revenue cycle management"]
    pages.append(
        Page(
            slug=slug,
            name=display,
            category=category,
            intent=intent,
            keywords=base_keywords,
            summary=summary,
            cta=cta,
            cta_href=cta_href,
            secondary_cta=secondary_cta,
            secondary_href=secondary_href,
            template=template,
            noindex=noindex,
        )
    )


add(
    "index",
    "Resolute MSO",
    "home",
    "Brand and core conversion",
    ["AI-powered revenue cycle management", "medical billing automation", "RCM services"],
    "Resolute MSO is an AI-powered RCM and medical billing automation partner for U.S. healthcare providers.",
    template="home",
)
add("home", "Resolute MSO Home Redirect", "utility", "Redirect", [], template="redirect", noindex=True)
add("about", "About Resolute MSO", "company", "Trust and operations", ["Resolute MSO", "RCM operations partner"], template="company")
add("why-resolute-mso", "Why Resolute MSO", "company", "Buyer trust", ["why Resolute MSO", "AI-powered RCM partner"], template="company")
add("rcm-expertise", "RCM Expertise", "company", "RCM expertise", ["RCM expertise", "medical billing operations"], template="company")
add("industries-who-we-serve", "Industries and Who We Serve", "company", "ICP", ["healthcare providers", "who we serve"], template="hub")
add("services", "Healthcare RCM Services", "hub", "Service hub", ["RCM services", "medical billing services"], template="hub")
add("automation-suite", "Automation Suite", "hub", "Automation hub", ["RCM automation", "medical billing automation"], template="hub")
add("specialties", "Specialty Billing Services", "hub", "Specialty billing hub", ["specialty billing services", "medical billing for specialty providers"], template="hub")
add("chargepilot", "ChargePilot Billing Software Automation", "product", "Product intent", ["ChargePilot", "billing software automation", "claim entry automation"], template="chargepilot", cta="Discuss ChargePilot", cta_href="#chargepilot-assessment")
add("practice-health-dashboard", "Practice Health Dashboard", "automation", "Product intent", ["practice health dashboard", "RCM KPI dashboard"], template="standard", cta="View Dashboard Assessment")
add("free-rcm-audit", "Free RCM Audit", "conversion", "Lead generation", ["free RCM audit", "free billing audit", "free AR audit"], template="audit", cta="Start Free RCM Audit")
add("contact", "Contact Resolute MSO", "conversion", "Lead generation", ["contact Resolute MSO", "medical billing company contact"], template="contact", cta="Send Business Inquiry")
add("compliance", "Compliance", "company", "Compliance and trust", ["HIPAA-conscious RCM", "healthcare compliance"], template="company")
add("quality-compliance", "Quality Commitment", "company", "Quality and trust", ["quality commitment", "RCM quality"], template="company")
add("service-quality-feedback", "Service Feedback", "company", "Trust", ["service feedback", "RCM feedback"], template="feedback")
add("privacy", "Privacy Policy", "company", "Trust", ["privacy policy", "PHI-safe public forms"], template="privacy")
add("all-rcm-solutions", "All RCM Solutions", "hub", "SEO hub", ["all RCM solutions", "medical billing services directory"], template="all")
add("resources", "RCM Guides and Resources", "hub", "Educational hub", ["RCM guides", "medical billing resources"], template="hub")
add("rcm-insights", "RCM Insights", "resource", "Educational intent", ["RCM insights", "revenue cycle strategy"], template="standard")
add("automation-updates", "Automation Updates", "automation", "Educational intent", ["healthcare automation updates", "RCM automation"], template="standard")
add("healthcare-operations", "Healthcare Operations", "resource", "Educational intent", ["healthcare operations", "practice operations"], template="standard")
add("site-directory", "Site Directory", "hub", "Crawl support", ["site directory", "Resolute MSO pages"], template="all")


SERVICE_SLUGS = [
    "medical-billing-services",
    "revenue-cycle-management-services",
    "denial-management-services",
    "ar-follow-up-services",
    "eligibility-verification-services",
    "prior-authorization-services",
    "payment-posting-services",
    "medical-coding-services",
    "claim-submission-services",
    "claim-scrubbing-services",
    "credentialing-services",
    "provider-enrollment-services",
    "rcm-reporting-services",
    "billing-audit-services",
    "insurance-verification-services",
    "patient-statement-services",
    "era-and-eft-enrollment-services",
    "clearinghouse-support-services",
    "rcm-process-improvement",
    "revenue-leakage-analysis",
    "payment-reconciliation-services",
    "accounts-receivable-recovery",
    "underpayment-recovery",
    "payer-follow-up-services",
    "patient-billing-support",
]

for slug in SERVICE_SLUGS:
    add(
        slug,
        category="service",
        intent="Core service intent",
        keywords=[title_case_from_slug(slug).lower(), "RCM services", "medical billing outsourcing"],
        cta="Start Free RCM Audit",
    )


SPECIALTY_SLUGS = [
    "clinical-lab-billing-services",
    "toxicology-lab-billing-services",
    "molecular-lab-billing-services",
    "pathology-billing-services",
    "imaging-center-billing-services",
    "radiology-billing-services",
    "urgent-care-billing-services",
    "primary-care-billing-services",
    "internal-medicine-billing-services",
    "family-practice-billing-services",
    "cardiology-billing-services",
    "mental-health-billing-services",
    "physical-therapy-billing-services",
    "chiropractic-billing-services",
    "dme-billing-services",
    "pain-management-billing-services",
    "dermatology-billing-services",
    "pediatrics-billing-services",
    "obgyn-billing-services",
    "podiatry-billing-services",
    "behavioral-health-billing",
    "oncology-billing",
    "wound-care-billing",
    "fqhc-billing-support",
    "multi-specialty-group-billing",
]

for slug in SPECIALTY_SLUGS:
    add(
        slug,
        category="specialty",
        intent="Specialty billing intent",
        keywords=[title_case_from_slug(slug).lower(), "specialty billing services", "medical billing for providers"],
        cta="Request Specialty Billing Review",
    )


AUTOMATION_SLUGS = [
    "medical-billing-automation",
    "rcm-automation",
    "officeally-claim-entry-automation",
    "charge-entry-automation",
    "eligibility-automation",
    "denial-workflow-automation",
    "ar-follow-up-automation",
    "reporting-automation",
    "payment-posting-automation",
    "practice-management-automation",
    "healthcare-workflow-automation",
    "ai-in-medical-billing",
    "ai-revenue-cycle-management",
    "rcm-dashboard-automation",
    "chargepilot-officeally-automation",
    "chargepilot-implementation",
    "chargepilot-pricing",
    "chargepilot-support",
    "billing-software-automation",
    "healthcare-operations-automation",
    "ai-claim-entry-automation",
    "ai-denial-management",
    "ai-billing-dashboard",
    "medical-billing-bot-agentic-rcm",
    "ai-ecosystem",
    "future-ai-modules",
]

for slug in AUTOMATION_SLUGS:
    add(
        slug,
        category="automation",
        intent="Automation and AI intent",
        keywords=[title_case_from_slug(slug).lower(), "medical billing automation", "AI revenue cycle management"],
        cta="Get Automation Assessment",
        cta_href="/contact.html",
        secondary_cta="Discuss ChargePilot",
        secondary_href="/chargepilot.html",
    )


BUYER_SLUGS = [
    "best-medical-billing-company-for-small-practices",
    "medical-billing-company-for-physician-groups",
    "medical-billing-services-for-physician-groups",
    "medical-billing-outsourcing-company",
    "rcm-outsourcing-services",
    "medical-billing-company-vs-in-house-billing",
    "rcm-outsourcing-vs-in-house-team",
    "when-to-outsource-medical-billing",
    "how-to-choose-an-rcm-partner",
    "medical-billing-audit-checklist",
    "reduce-claim-denials",
    "improve-clean-claim-rate",
    "reduce-ar-over-90-days",
    "improve-net-collection-rate",
    "first-pass-claim-rate-improvement",
    "healthcare-revenue-recovery-services",
    "small-practice-rcm-support",
    "provider-billing-support-company",
    "medical-billing-cost-reduction",
    "rcm-kpi-dashboard-services",
    "practice-revenue-optimization",
    "free-ar-audit",
    "free-billing-audit",
]

for slug in BUYER_SLUGS:
    add(
        slug,
        category="buyer",
        intent="Buyer comparison and pain-point intent",
        keywords=[title_case_from_slug(slug).lower(), "medical billing company", "RCM partner"],
        cta="Book a Revenue Audit",
    )


RESOURCE_SLUGS = [
    "medical-billing-beginner-guide",
    "revenue-cycle-management-beginner-guide",
    "denial-management-guide",
    "ar-follow-up-guide",
    "clean-claim-playbook",
    "eligibility-verification-guide",
    "prior-authorization-guide",
    "payment-posting-guide",
    "charge-entry-guide",
    "claim-rejection-guide",
    "rcm-kpi-guide",
    "days-in-ar-guide",
    "net-collection-rate-guide",
    "first-pass-rate-guide",
    "hipaa-conscious-website-forms",
    "officeally-automation-guide",
    "clinical-lab-billing-guide",
    "imaging-billing-guide",
    "urgent-care-billing-guide",
    "ai-powered-rcm-guide",
    "medical-billing-terms-glossary",
    "denial-codes-guide",
    "cpt-icd-10-billing-overview",
    "revenue-leakage-guide",
    "practice-billing-workflow-guide",
    "blog-clean-claim-playbook",
    "blog-denial-management-guide",
    "blog-automation-in-medical-billing",
    "blog-chargepilot-pm-automation",
    "blog-clinical-lab-billing",
    "blog-ar-follow-up-action",
    "blog-rcm-priorities",
    "blog",
]

BLOG_ARTICLES = {
    "blog-clean-claim-playbook": {
        "name": "Clean Claim Playbook for Provider Billing Teams",
        "summary": "A practical clean claim playbook for reducing front-end rework, claim rejections, and preventable denial pressure.",
        "takeaways": [
            "Clean claims start before claim submission, not after a denial arrives.",
            "Eligibility, authorization, coding, modifier, and demographic checks should be owned as a repeatable workflow.",
            "Automation helps most when it routes exceptions instead of hiding them.",
        ],
        "sections": [
            ("Start with the front-end facts", "A clean claim is built from accurate patient, payer, provider, diagnosis, procedure, modifier, authorization, and place-of-service data. Billing teams should review these facts before claim release, because downstream edits are more expensive than front-end prevention."),
            ("Use edit patterns as training material", "Repeated rejections are not just work items. They are signals that intake, coding review, payer rules, or charge entry needs a tighter loop. Resolute MSO recommends logging repeated rejection causes, assigning owners, and reviewing the pattern weekly until it stops repeating."),
            ("Where automation fits", "Automation can compare required fields, normalize repetitive entry, flag missing values, and help teams prioritize exception queues. The strongest approach keeps human review for ambiguous records while reducing manual movement for predictable claim-entry steps."),
        ],
        "sources": [
            ("CMS Medicare Claims Processing Manual", "https://www.cms.gov/regulations-and-guidance/guidance/manuals/internet-only-manuals-ioms-items/cms018912"),
            ("CMS National Correct Coding Initiative", "https://www.cms.gov/medicare/coding-billing/national-correct-coding-initiative-ncci-edits"),
            ("HHS HIPAA for Professionals", "https://www.hhs.gov/hipaa/for-professionals/index.html"),
        ],
    },
    "blog-denial-management-guide": {
        "name": "Denial Management Guide for Revenue Cycle Leaders",
        "summary": "How provider billing teams can turn denial worklists into root-cause prevention, payer follow-up discipline, and clearer RCM reporting.",
        "takeaways": [
            "Denial management should separate correction work from prevention work.",
            "Reason-code trends are more useful when grouped by owner, payer, service line, and preventability.",
            "A denial dashboard should show movement, not just volume.",
        ],
        "sections": [
            ("Do not let every denial look the same", "A high-performing denial workflow distinguishes registration issues, coding issues, authorization gaps, medical-necessity questions, timely filing risk, payer processing problems, and contract underpayment concerns. Each category needs a different owner and next action."),
            ("Build a prevention loop", "Resolute MSO treats overturned denials as operational evidence. If a denial is overturned repeatedly, the team should ask why the claim did not go out correctly the first time or why payer-specific documentation was not attached earlier."),
            ("Measure what moved", "Useful denial reporting includes denial rate, preventable denial rate, appeal aging, overturn movement, payer response timing, and dollars still pending by next action. Volume alone can make a busy team look productive while AR remains stuck."),
        ],
        "sources": [
            ("CMS Medicare Claims Processing Manual", "https://www.cms.gov/regulations-and-guidance/guidance/manuals/internet-only-manuals-ioms-items/cms018912"),
            ("CMS NCCI Edits", "https://www.cms.gov/medicare/coding-billing/national-correct-coding-initiative-ncci-edits"),
            ("OIG Compliance Guidance", "https://oig.hhs.gov/compliance/compliance-guidance/"),
        ],
    },
    "blog-automation-in-medical-billing": {
        "name": "Medical Billing Automation: Where AI Helps and Where Oversight Still Matters",
        "summary": "A healthcare operations view of medical billing automation, AI-assisted RCM, exception handling, and human oversight.",
        "takeaways": [
            "Automation is strongest on repetitive, rules-based billing movement.",
            "AI and automation should improve visibility, not remove accountability.",
            "Protected health information should never be placed into public website forms or casual channels.",
        ],
        "sections": [
            ("Start with workflow fit", "Automation should not begin with a tool demo. It should begin with a workflow map: where work starts, what data is trusted, which exceptions require human review, and which outputs leadership needs to see."),
            ("Keep exception handling visible", "Billing automation becomes risky when exceptions disappear into a black box. A better model shows which records moved, which records paused, why they paused, and who owns the next action."),
            ("Use AI carefully in healthcare operations", "AI can help summarize, route, and monitor patterns, but billing teams still need compliance-aware controls, access discipline, and human review for ambiguous or high-risk decisions."),
        ],
        "sources": [
            ("HHS HIPAA for Professionals", "https://www.hhs.gov/hipaa/for-professionals/index.html"),
            ("CMS Electronic Billing and EDI", "https://www.cms.gov/medicare/billing/electronicbillingeditrans"),
            ("OIG Compliance Guidance", "https://oig.hhs.gov/compliance/compliance-guidance/"),
        ],
    },
    "blog-chargepilot-pm-automation": {
        "name": "ChargePilot and Billing Software Automation for RCM Teams",
        "summary": "How ChargePilot supports repetitive claim-entry and billing software workflows with throughput visibility and exception review.",
        "takeaways": [
            "ChargePilot is positioned for billing software automation across supported workflows.",
            "The right implementation starts with source-data quality and exception rules.",
            "Automation should help billing teams move cleaner work faster while preserving control.",
        ],
        "sections": [
            ("Think beyond one screen", "Claim-entry automation is not only keystrokes. It includes source-file review, field readiness, validation rules, queue control, exception routing, and visibility for billing leaders."),
            ("Design for supported billing software workflows", "ChargePilot can be scoped around repetitive billing software and PM workflows, including OfficeAlly-related use cases where appropriate. The implementation should confirm the exact workflow, volume, data source, and exception requirements before go-live."),
            ("What leaders should see", "A useful automation dashboard shows queued work, completed work, paused records, exceptions, throughput, and reasons work did not move. That view helps leaders improve the process instead of only asking staff for status updates."),
        ],
        "sources": [
            ("CMS Electronic Billing and EDI", "https://www.cms.gov/medicare/billing/electronicbillingeditrans"),
            ("CMS Medicare Claims Processing Manual", "https://www.cms.gov/regulations-and-guidance/guidance/manuals/internet-only-manuals-ioms-items/cms018912"),
            ("HHS HIPAA for Professionals", "https://www.hhs.gov/hipaa/for-professionals/index.html"),
        ],
    },
    "blog-clinical-lab-billing": {
        "name": "Clinical Lab Billing: Documentation, Medical Necessity, and AR Discipline",
        "summary": "A clinical lab billing article for teams managing payer edits, documentation risk, medical necessity, and lab AR follow-up.",
        "takeaways": [
            "Clinical lab billing depends on clean ordering, diagnosis support, payer rules, and documentation discipline.",
            "Repeated lab denials should be traced back to ordering, eligibility, coding, and payer-specific requirements.",
            "Lab AR needs segmentation by payer, age, denial reason, and next action.",
        ],
        "sections": [
            ("Lab billing starts before the claim", "Laboratory revenue teams need accurate ordering provider information, test details, diagnosis support, payer data, and documentation readiness. If the order is incomplete, the billing team inherits preventable follow-up."),
            ("Medical necessity and coding signals", "Clinical lab teams should monitor medical-necessity denials, diagnosis mismatch patterns, missing documentation, and payer-specific test policies. These signals should feed back to intake and ordering workflows."),
            ("AR follow-up for lab volume", "Lab AR can become noisy quickly because claim counts are high. A practical lab follow-up model groups work by payer, age, dollar value, denial category, and action needed, then reports movement each week."),
        ],
        "sources": [
            ("CMS Clinical Laboratory Fee Schedule", "https://www.cms.gov/medicare/payment/fee-schedules/clinical-laboratory-fee-schedule"),
            ("CMS NCCI Edits", "https://www.cms.gov/medicare/coding-billing/national-correct-coding-initiative-ncci-edits"),
            ("CMS Medicare Claims Processing Manual", "https://www.cms.gov/regulations-and-guidance/guidance/manuals/internet-only-manuals-ioms-items/cms018912"),
        ],
    },
    "blog-ar-follow-up-action": {
        "name": "AR Follow-Up Action Plan for Practices and Billing Companies",
        "summary": "A practical accounts receivable follow-up framework for payer action, aging buckets, underpayment review, and leadership reporting.",
        "takeaways": [
            "AR follow-up should be prioritized by value, age, payer behavior, and next action.",
            "Aging alone is not enough; teams need denial, status, and payer response context.",
            "Leadership reporting should show what moved and what is blocked.",
        ],
        "sections": [
            ("Segment before calling", "A payer call queue is weaker than an action queue. Sort AR by payer, age, balance, denial status, claim status, authorization risk, and underpayment concern before assigning staff time."),
            ("Document the next action", "Every meaningful AR touch should leave a next action, owner, expected payer response, and follow-up date. Without that discipline, the same claim can be touched repeatedly without moving."),
            ("Report stuck money clearly", "A useful AR dashboard separates collectable follow-up, payer delay, denial work, underpayment review, patient responsibility, and write-off review. That makes the backlog easier to manage and harder to ignore."),
        ],
        "sources": [
            ("CMS Medicare Claims Processing Manual", "https://www.cms.gov/regulations-and-guidance/guidance/manuals/internet-only-manuals-ioms-items/cms018912"),
            ("CMS Electronic Billing and EDI", "https://www.cms.gov/medicare/billing/electronicbillingeditrans"),
            ("OIG Compliance Guidance", "https://oig.hhs.gov/compliance/compliance-guidance/"),
        ],
    },
    "blog-rcm-priorities": {
        "name": "RCM Priorities for Provider Leaders in 2026",
        "summary": "Revenue cycle priorities for U.S. provider leaders focused on denial prevention, automation readiness, clean data, and compliant communication.",
        "takeaways": [
            "Provider leaders should connect RCM priorities to measurable operating signals.",
            "Automation readiness depends on data quality, repeatable workflows, and exception ownership.",
            "Public website and lead forms should stay business-only and avoid PHI collection.",
        ],
        "sections": [
            ("Make denial prevention visible", "Denials should not sit only inside billing worklists. Leadership needs trends by payer, reason, department, specialty, and preventability so the organization can reduce repeat work."),
            ("Prepare workflows for automation", "Before adding automation, teams should standardize source files, define exception handling, confirm who approves changes, and decide which throughput metrics matter."),
            ("Protect communication channels", "A modern RCM website should make contact easy while clearly warning visitors not to submit patient information through public forms. That clarity protects both the provider and the operations team."),
        ],
        "sources": [
            ("HHS HIPAA for Professionals", "https://www.hhs.gov/hipaa/for-professionals/index.html"),
            ("OIG Compliance Guidance", "https://oig.hhs.gov/compliance/compliance-guidance/"),
            ("CMS National Correct Coding Initiative", "https://www.cms.gov/medicare/coding-billing/national-correct-coding-initiative-ncci-edits"),
        ],
    },
}

for slug in RESOURCE_SLUGS:
    article = BLOG_ARTICLES.get(slug)
    add(
        slug,
        name=article["name"] if article else None,
        category="resource",
        intent="Educational intent",
        keywords=[(article["name"] if article else title_case_from_slug(slug)).lower(), "medical billing guide", "RCM guide"],
        cta="Talk to Resolute MSO",
        cta_href=WHATSAPP_URL,
        secondary_cta="View All RCM Solutions",
        secondary_href="/all-rcm-solutions/",
    )


PAGE_BY_SLUG = {p.slug: p for p in pages}


def group_pages(category: str) -> list[Page]:
    return [p for p in pages if p.category == category and not p.noindex]


def meta_title(page: Page) -> str:
    if page.slug == "index":
        return "AI-Powered Revenue Cycle Management | Resolute MSO"
    if page.category == "product":
        return "ChargePilot Claim Entry Product | Resolute MSO"
    suffix = " | Resolute MSO"
    base = page.name
    if page.category == "service" and "Services" not in base:
        base = f"{base} Services"
    if page.category == "specialty" and "Billing" not in base:
        base = f"{base} Billing Support"
    if len(base + suffix) > 64:
        base = base.replace("Healthcare ", "").replace("Revenue Cycle Management", "RCM")
    return base[:64 - len(suffix)].rstrip() + suffix


def h1(page: Page) -> str:
    if page.slug == "index":
        return "AI-powered revenue cycle management for modern healthcare providers."
    if page.category == "service":
        return f"{page.name} for U.S. healthcare providers"
    if page.category == "specialty":
        return f"{page.name} for specialty providers"
    if page.category == "automation":
        return f"{page.name} for healthcare revenue teams"
    if page.category == "buyer":
        return f"{page.name}: practical guidance for provider leaders"
    if page.category == "resource":
        return f"{page.name} for healthcare revenue teams"
    return page.name


def summary(page: Page) -> str:
    if page.summary:
        return page.summary
    if page.slug in BLOG_ARTICLES:
        return BLOG_ARTICLES[page.slug]["summary"]
    if page.slug == "blog":
        return "Resolute MSO blogs publish practical RCM, medical billing automation, ChargePilot, denial management, AR follow-up, and specialty billing articles for healthcare revenue teams."
    lead = {
        "service": f"Resolute MSO helps practices, physician groups, labs, imaging centers, and RCM teams use {page.name.lower()} to improve claim movement, denial visibility, AR control, and revenue cycle discipline.",
        "specialty": f"Resolute MSO supports {page.name.lower()} with specialty-aware workflows, payer follow-up, denial prevention, clean claim readiness, and KPI visibility for U.S. provider organizations.",
        "automation": f"Resolute MSO applies AI-powered RCM automation to {page.name.lower()}, helping billing teams reduce repetitive work, improve exception handling, and see workflow throughput more clearly.",
        "buyer": f"This page helps provider leaders evaluate {page.name.lower()} with practical decision criteria, operational signals, and next steps for reducing revenue leakage.",
        "resource": f"This guide explains {page.name.lower()} in clear, operational terms so healthcare revenue teams can identify risks, improve workflows, and ask better RCM questions.",
        "company": f"{page.name} explains how Resolute MSO approaches healthcare revenue cycle management, medical billing automation, operational quality, and HIPAA-conscious public communication.",
        "hub": f"{page.name} organizes Resolute MSO services, specialty support, automation pages, and practical RCM resources for U.S. healthcare providers.",
        "conversion": f"{page.name} gives provider leaders a direct way to discuss billing, RCM, denials, AR, automation, ChargePilot, or operational reporting with Resolute MSO.",
        "product": "ChargePilot is Resolute MSO's billing software automation product for claim-entry workflows, exception handling, throughput visibility, and RCM team control.",
    }.get(page.category, f"{page.name} from Resolute MSO.")
    return lead


def meta_description(page: Page) -> str:
    text = summary(page)
    if len(text) > 158:
        text = text[:155].rsplit(" ", 1)[0] + "..."
    return text


def e(text: str) -> str:
    return escape(text, quote=True)


def attrs(**items: str | bool | None) -> str:
    parts = []
    for key, value in items.items():
        if value is None or value is False:
            continue
        key = key.replace("_", "-")
        if value is True:
            parts.append(key)
        else:
            parts.append(f'{key}="{e(str(value))}"')
    return " ".join(parts)


def clean_internal_links(markup: str) -> str:
    markup = re.sub(r'href="/([a-z0-9-]+)\.html([^"]*)"', r'href="/\1/\2"', markup)
    markup = re.sub(r'url=/([a-z0-9-]+)\.html', r'url=/\1/', markup)
    return markup


def minify_css(css: str) -> str:
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{}:;,>])\s*", r"\1", css)
    return css.strip()


def minify_js(js: str) -> str:
    js = re.sub(r"\s+", " ", js)
    return js.strip()


def link(path: str, label: str, cls: str = "") -> str:
    class_attr = f' class="{cls}"' if cls else ""
    return f'<a{class_attr} href="{e(path)}">{e(label)}</a>'


def nav_html(active: str) -> str:
    groups = [
        (
            "Automation Suite",
            "/automation-suite.html",
            [
                ("ChargePilot", "/chargepilot.html"),
                ("RCM Automation", "/rcm-automation.html"),
                ("Practice Health Dashboard", "/practice-health-dashboard.html"),
                ("See More", "/automation-suite.html"),
            ],
        ),
        (
            "Services",
            "/services.html",
            [
                ("Medical Billing Services", "/medical-billing-services.html"),
                ("Revenue Cycle Management", "/revenue-cycle-management-services.html"),
                ("Denial Management", "/denial-management-services.html"),
                ("See More", "/services.html"),
            ],
        ),
        (
            "Specialties",
            "/industries-who-we-serve.html",
            [
                ("Physician Groups", "/medical-billing-company-for-physician-groups.html"),
                ("Clinical Labs", "/clinical-lab-billing-services.html"),
                ("Imaging Centers", "/imaging-center-billing-services.html"),
                ("See More", "/industries-who-we-serve.html"),
            ],
        ),
        (
            "Resources",
            "/resources.html",
            [
                ("All RCM Solutions", "/all-rcm-solutions.html"),
                ("RCM Insights", "/rcm-insights.html"),
                ("Blogs", "/blog.html"),
                ("Guides", "/resources.html#guides"),
                ("See More", "/resources.html"),
            ],
        ),
        (
            "Company",
            "/about.html",
            [
                ("About", "/about.html"),
                ("Quality Commitment", "/quality-compliance.html"),
                ("Compliance", "/compliance.html"),
                ("Contact", "/contact.html"),
            ],
        ),
    ]
    items = []
    for label, href, children in groups:
        child_links = "".join(f'<a href="{href2}">{label2}</a>' for label2, href2 in children)
        active_class = "active" if href.lstrip("/").replace(".html", "") == active else ""
        items.append(
            f"""
            <li class="nav-item has-menu">
              <a class="{active_class}" href="{href}">{label}</a>
              <button class="menu-caret" type="button" aria-expanded="false" aria-label="Open {label} menu"><span aria-hidden="true"></span></button>
              <div class="dropdown">{child_links}</div>
            </li>"""
        )
    items.append('<li class="nav-item"><a href="/contact.html">Contact</a></li>')
    return "".join(items)


def breadcrumbs(page: Page) -> str:
    if page.slug == "index":
        return ""
    crumbs = [
        ("Home", "/"),
    ]
    if page.category in {"service"}:
        crumbs.append(("Services", "/services.html"))
    elif page.category in {"specialty"}:
        crumbs.append(("Who We Serve", "/industries-who-we-serve.html"))
    elif page.category in {"automation", "product"}:
        crumbs.append(("Automation Suite", "/automation-suite.html"))
    elif page.category in {"resource"}:
        crumbs.append(("Resources", "/resources.html"))
    elif page.category in {"buyer"}:
        crumbs.append(("All RCM Solutions", "/all-rcm-solutions.html"))
    elif page.category in {"company"}:
        crumbs.append(("Company", "/about.html"))
    crumbs.append((page.name, page.path))
    links = []
    for i, (label, href) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            links.append(f"<span>{e(label)}</span>")
        else:
            links.append(f'<a href="{href}">{e(label)}</a>')
    return f'<nav class="breadcrumbs" aria-label="Breadcrumb">{"<span>/</span>".join(links)}</nav>'


def base_schema(page: Page, faq: list[tuple[str, str]] | None = None) -> list[dict]:
    schemas: list[dict] = [
        {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "Resolute MSO",
            "url": SITE,
            "logo": f"{SITE}{LOGO_SRC}",
            "email": "support@resolutemso.com",
            "telephone": "+1 701 552 5527",
            "sameAs": [LINKEDIN_URL],
        },
        {
            "@context": "https://schema.org",
            "@type": "MedicalBusiness",
            "name": "Resolute MSO",
            "url": SITE,
            "areaServed": "United States",
            "description": "AI-powered revenue cycle management, medical billing automation, ChargePilot billing software automation, and healthcare operations support for U.S. providers.",
        },
        {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": meta_title(page).replace(" | Resolute MSO", ""),
            "url": page.url,
            "description": meta_description(page),
            "isPartOf": {"@type": "WebSite", "name": "Resolute MSO", "url": SITE},
        },
    ]
    if page.slug != "index":
        items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}]
        items.append({"@type": "ListItem", "position": 2, "name": page.name, "item": page.url})
        schemas.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items})
    if page.category in {"service", "specialty", "automation", "buyer"}:
        schemas.append(
            {
                "@context": "https://schema.org",
                "@type": "Service",
                "name": page.name,
                "provider": {"@type": "Organization", "name": "Resolute MSO"},
                "areaServed": "United States",
                "serviceType": page.intent,
                "description": summary(page),
            }
        )
    if page.category == "product" or "chargepilot" in page.slug:
        schemas.extend(
            [
                {
                    "@context": "https://schema.org",
                    "@type": "Product",
                    "name": "ChargePilot",
                    "brand": {"@type": "Brand", "name": "Resolute MSO"},
                    "description": "ChargePilot is Resolute MSO's billing software claim-entry and claim-submission automation product for billing teams and RCM operations.",
                    "category": "Healthcare billing automation",
                    "url": f"{SITE}/chargepilot/",
                },
                {
                    "@context": "https://schema.org",
                    "@type": "SoftwareApplication",
                    "name": "ChargePilot",
                    "applicationCategory": "BusinessApplication",
                    "operatingSystem": "Windows desktop control center and web portal",
                    "description": "Billing software claim-entry automation with throughput visibility, exception handling, and admin/client portal support.",
                    "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD", "description": "Pricing is scoped after workflow assessment."},
                },
            ]
        )
    if page.category == "resource":
        schemas.append(
            {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": h1(page),
                "author": {"@type": "Organization", "name": "Resolute MSO"},
                "publisher": {"@type": "Organization", "name": "Resolute MSO"},
                "dateModified": TODAY,
                "mainEntityOfPage": page.url,
                "description": summary(page),
            }
        )
    if faq:
        schemas.append(
            {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": [
                    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                    for q, a in faq
                ],
            }
        )
    return schemas


def jsonld(schemas: list[dict]) -> str:
    return "\n".join(
        f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False, separators=(",", ":"))}</script>'
        for schema in schemas
    )


def head(page: Page, faq: list[tuple[str, str]] | None = None) -> str:
    robots = "noindex, follow" if page.noindex else "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"
    return f"""<meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(meta_title(page))}</title>
  <meta name="description" content="{e(meta_description(page))}">
  <meta name="robots" content="{robots}">
  <link rel="canonical" href="{page.url}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{e(meta_title(page))}">
  <meta property="og:description" content="{e(meta_description(page))}">
  <meta property="og:url" content="{page.url}">
  <meta property="og:image" content="{OG_IMAGE}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{e(meta_title(page))}">
  <meta name="twitter:description" content="{e(meta_description(page))}">
  <meta name="twitter:image" content="{OG_IMAGE}">
  <meta name="theme-color" content="#0F9D8F">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/img/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&amp;display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/css/elegant-typography.css">
  <link rel="stylesheet" href="/assets/css/site-motion.css">
  <style>{minify_css(CSS)}</style>
  {jsonld(base_schema(page, faq))}"""


def header(page: Page) -> str:
    active = page.slug
    return f"""
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="nav-shell">
      <a class="brand" href="/" aria-label="Resolute MSO home">
        <img src="{LOGO_SRC}" alt="Resolute MSO logo" width="{LOGO_WIDTH}" height="{LOGO_HEIGHT}" decoding="async">
      </a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="primary-navigation">Menu</button>
      <nav id="primary-navigation" class="main-nav" aria-label="Primary navigation">
        <ul>{nav_html(active)}</ul>
      </nav>
      <a class="btn btn-small nav-cta" href="/free-rcm-audit.html">Book a Revenue Audit</a>
    </div>
  </header>"""


def floating_tools() -> str:
    return f"""
  <div class="floating-tools" role="group" aria-label="Quick contact tools">
    <button class="scroll-top" type="button" aria-label="Go to top">&#8593;</button>
    <button class="whatsapp-launch" type="button" aria-expanded="false" aria-controls="whatsapp-panel" aria-label="Chat with Resolute MSO on WhatsApp">
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12.04 2C6.52 2 2.03 6.45 2.03 11.93c0 1.75.46 3.46 1.33 4.96L2 22l5.25-1.35a10.1 10.1 0 0 0 4.79 1.22c5.52 0 10.01-4.45 10.01-9.94S17.56 2 12.04 2Zm0 18.18c-1.52 0-3-.41-4.3-1.18l-.31-.18-3.11.8.83-3.01-.2-.31a8.16 8.16 0 0 1-1.25-4.37c0-4.55 3.74-8.25 8.34-8.25s8.34 3.7 8.34 8.25-3.74 8.25-8.34 8.25Zm4.57-6.18c-.25-.12-1.48-.73-1.71-.81-.23-.08-.4-.12-.57.12-.17.25-.65.81-.8.98-.15.17-.3.19-.55.06-.25-.12-1.06-.39-2.02-1.24-.75-.66-1.25-1.48-1.4-1.73-.15-.25-.02-.38.11-.51.11-.11.25-.3.37-.45.12-.15.17-.25.25-.42.08-.17.04-.31-.02-.43-.06-.12-.57-1.36-.78-1.86-.21-.5-.41-.43-.57-.44h-.49c-.17 0-.43.06-.66.31-.23.25-.87.85-.87 2.07s.89 2.4 1.02 2.56c.12.17 1.75 2.65 4.25 3.72.59.25 1.06.4 1.42.51.6.19 1.14.16 1.57.1.48-.07 1.48-.6 1.69-1.18.21-.58.21-1.08.15-1.18-.06-.1-.23-.16-.48-.28Z"/></svg>
    </button>
  </div>
  <section class="whatsapp-panel" id="whatsapp-panel" aria-label="WhatsApp contact panel" hidden>
    <div class="whatsapp-head">
      <strong>Chat with us</strong>
      <button class="whatsapp-close" type="button" aria-label="Close WhatsApp panel">x</button>
    </div>
    <form class="whatsapp-form">
      <p>Please fill out the required fields to start your chat immediately.</p>
      <label>Full Name<input name="name" type="text" autocomplete="name" required></label>
      <label>Email<input name="email" type="email" autocomplete="email" required></label>
      <label>Phone Number<input name="phone" type="tel" autocomplete="tel" required></label>
      <p class="phi-note">Business inquiries only. Do not submit PHI or patient information.</p>
      <button class="btn" type="submit">Chat on WhatsApp</button>
    </form>
    <a class="whatsapp-direct" href="{WHATSAPP_URL}">Chat on WhatsApp</a>
  </section>"""


def footer() -> str:
    columns = [
        ("AI Ecosystem", [("ChargePilot", "/chargepilot.html"), ("Billing Software Automation", "/billing-software-automation.html"), ("AI Revenue Cycle Management", "/ai-revenue-cycle-management.html"), ("AI Billing Dashboard", "/ai-billing-dashboard.html"), ("Healthcare Workflow Automation", "/healthcare-workflow-automation.html"), ("Practice Health Dashboard", "/practice-health-dashboard.html")]),
        ("Services", [("Revenue Cycle Management", "/revenue-cycle-management-services.html"), ("Medical Billing Services", "/medical-billing-services.html"), ("Denial Management", "/denial-management-services.html"), ("AR Follow-Up Services", "/ar-follow-up-services.html"), ("Payment Posting", "/payment-posting-services.html"), ("Provider Enrollment", "/provider-enrollment-services.html")]),
        ("Specialties", [("Clinical Labs", "/clinical-lab-billing-services.html"), ("Imaging Centers", "/imaging-center-billing-services.html"), ("Urgent Care", "/urgent-care-billing-services.html"), ("Cardiology", "/cardiology-billing-services.html"), ("Dermatology", "/dermatology-billing-services.html"), ("Mental Health", "/mental-health-billing-services.html")]),
        ("Quick Links", [("About Resolute MSO", "/about.html"), ("Blogs", "/blog.html"), ("All RCM Solutions", "/all-rcm-solutions.html"), ("Compliance", "/compliance.html"), ("Quality Commitment", "/quality-compliance.html"), ("Contact Us", "/contact.html")]),
    ]
    col_html = ""
    for title, links in columns:
        col_html += f"<div><h2>{title}</h2>" + "".join(f'<a href="{href}">{label}</a>' for label, href in links) + "</div>"
    linkedin_icon = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4.98 3.5C4.98 4.88 3.86 6 2.5 6S0 4.88 0 3.5 1.12 1 2.5 1s2.48 1.12 2.48 2.5ZM.35 8.05h4.3V23H.35V8.05Zm7.28 0h4.12v2.04h.06c.57-1.08 1.98-2.22 4.08-2.22 4.36 0 5.16 2.87 5.16 6.6V23h-4.29v-7.56c0-1.8-.03-4.12-2.51-4.12-2.52 0-2.9 1.97-2.9 4V23H7.63V8.05Z"/></svg>'
    email_icon = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 5h18a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1Zm9 8.2L4.8 7H4v10h16V7h-.8L12 13.2ZM6.8 7 12 11.5 17.2 7H6.8Z"/></svg>'
    whatsapp_icon = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12.04 2C6.52 2 2.03 6.45 2.03 11.93c0 1.75.46 3.46 1.33 4.96L2 22l5.25-1.35a10.1 10.1 0 0 0 4.79 1.22c5.52 0 10.01-4.45 10.01-9.94S17.56 2 12.04 2Zm0 18.18c-1.52 0-3-.41-4.3-1.18l-.31-.18-3.11.8.83-3.01-.2-.31a8.16 8.16 0 0 1-1.25-4.37c0-4.55 3.74-8.25 8.34-8.25s8.34 3.7 8.34 8.25-3.74 8.25-8.34 8.25Zm4.57-6.18c-.25-.12-1.48-.73-1.71-.81-.23-.08-.4-.12-.57.12-.17.25-.65.81-.8.98-.15.17-.3.19-.55.06-.25-.12-1.06-.39-2.02-1.24-.75-.66-1.25-1.48-1.4-1.73-.15-.25-.02-.38.11-.51.11-.11.25-.3.37-.45.12-.15.17-.25.25-.42.08-.17.04-.31-.02-.43-.06-.12-.57-1.36-.78-1.86-.21-.5-.41-.43-.57-.44h-.49c-.17 0-.43.06-.66.31-.23.25-.87.85-.87 2.07s.89 2.4 1.02 2.56c.12.17 1.75 2.65 4.25 3.72.59.25 1.06.4 1.42.51.6.19 1.14.16 1.57.1.48-.07 1.48-.6 1.69-1.18.21-.58.21-1.08.15-1.18-.06-.1-.23-.16-.48-.28Z"/></svg>'
    return f"""
  <footer class="site-footer">
    <div class="footer-grid">
      <div class="footer-brand">
        <img src="{LOGO_SRC}" alt="Resolute MSO logo" width="{LOGO_WIDTH}" height="{LOGO_HEIGHT}" loading="lazy" decoding="async">
        <p>Resolute MSO is an AI-powered RCM and medical billing automation partner for U.S. healthcare providers. Public forms are for business inquiries only and must not include PHI or patient information.</p>
        <p><a href="mailto:support@resolutemso.com">support@resolutemso.com</a><br><a href="tel:+17015525527">+1 701 552 5527</a></p>
      </div>
      {col_html}
      <div class="footer-newsletter">
        <h2>Bulletin &amp; Updates</h2>
        <p>Receive occasional RCM, billing automation, and ChargePilot updates from Resolute MSO.</p>
        <form action="mailto:support@resolutemso.com" method="POST" enctype="text/plain">
          <label>Name<input name="name" type="text" autocomplete="name" placeholder="Name"></label>
          <label>Your Email<input name="email" type="email" autocomplete="email" placeholder="Your Email"></label>
          <button class="btn btn-dark" type="submit">Subscribe</button>
        </form>
        <div class="social-links" role="group" aria-label="Resolute MSO social and contact links">
          <a href="{LINKEDIN_URL}" aria-label="Resolute MSO on LinkedIn" target="_blank" rel="noopener">{linkedin_icon}</a>
          <a href="mailto:support@resolutemso.com" aria-label="Email Resolute MSO">{email_icon}</a>
          <a href="{WHATSAPP_URL}" aria-label="Chat with Resolute MSO on WhatsApp">{whatsapp_icon}</a>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <span>Copyright <span data-year>2026</span> Resolute MSO. All rights reserved.</span>
      <nav aria-label="Footer legal links">
        <a href="/privacy.html">Privacy</a>
        <a href="/compliance.html">Compliance</a>
        <a href="/service-quality-feedback.html">Feedback</a>
        <a href="/blog.html">Blogs</a>
        <a href="/sitemap.xml">Sitemap</a>
      </nav>
    </div>
  </footer>
  {floating_tools()}
  <script>{minify_js(JS)}</script>
  <script src="/assets/js/site-motion.js" defer></script>"""


def layout(page: Page, body: str, faq: list[tuple[str, str]] | None = None) -> str:
    return clean_internal_links(f"""<!doctype html>
<html lang="en">
<head>
  {head(page, faq)}
</head>
<body data-page="{page.slug}">
{header(page)}
<main id="main">
{body}
</main>
{footer()}
</body>
</html>
""")


def category_label(page: Page) -> str:
    return {
        "service": "RCM Service",
        "specialty": "Specialty Billing",
        "automation": "Automation Suite",
        "buyer": "Provider Decision Guide",
        "resource": "RCM Resource",
        "company": "Company",
        "hub": "Directory",
        "conversion": "Start Here",
        "product": "ChargePilot",
    }.get(page.category, "Resolute MSO")


def audience_items(page: Page) -> list[str]:
    if page.category == "specialty":
        return ["Specialty clinics and groups", "Billing managers and RCM leaders", "Practice administrators", "Medical billing companies supporting specialty volume"]
    if page.category == "automation":
        return ["Billing teams using repetitive claim workflows", "RCM companies with high-volume queues", "Operations leaders seeking throughput visibility", "Provider groups using OfficeAlly or similar billing workflows"]
    if page.category == "buyer":
        return ["Practice owners", "CFOs and revenue cycle directors", "Office managers", "Billing leaders comparing in-house and outsourced options"]
    if page.category == "resource":
        return ["New RCM leaders", "Billing managers", "Practice administrators", "Provider executives who want clearer billing language"]
    return ["Physician practices", "Specialty clinics", "Clinical and diagnostic labs", "RCM and medical billing companies"]


def problem_items(page: Page) -> list[str]:
    if page.category == "specialty":
        return ["Specialty-specific payer rules and documentation gaps", "Authorization and eligibility issues before service", "Denials that require root-cause review", "Aging AR queues without clear payer action", "Underpayments and missing follow-up", "Limited specialty KPI visibility"]
    if page.category == "automation":
        return ["Manual entry that slows billing teams", "Repeated claim status checks", "Exception queues without ownership", "Spreadsheet-driven production tracking", "Low visibility into automation throughput", "Workflow handoffs that create preventable rework"]
    if page.category == "buyer":
        return ["Unclear outsourcing economics", "Hidden revenue leakage", "Denial trends without ownership", "In-house teams overloaded by payer follow-up", "No consistent KPI dashboard", "Difficulty choosing a healthcare billing partner"]
    if page.category == "resource":
        return ["Unclear RCM terminology", "Scattered workflows and handoffs", "Weak KPI definitions", "Reactive denial handling", "Slow AR movement", "Limited executive visibility"]
    return ["Claim rejections and preventable denials", "Aging AR over 90 days", "Eligibility and authorization gaps", "Manual payer follow-up", "Revenue leakage from underpayments", "Limited billing performance visibility"]


def workflow_items(page: Page) -> list[tuple[str, str]]:
    if page.category == "automation":
        return [
            ("Map", "Document the current billing workflow, source files, exceptions, and approval points."),
            ("Configure", "Configure automation around the team's actual PM, OfficeAlly, or billing workflow."),
            ("Run", "Support controlled production with human oversight and exception handling."),
            ("Measure", "Track throughput, error patterns, and operational signals for leaders."),
        ]
    if page.category == "resource":
        return [
            ("Define", "Clarify the concept and the RCM stage it affects."),
            ("Diagnose", "Identify the operational signals that show the issue exists."),
            ("Improve", "Apply process, staffing, automation, or reporting changes."),
            ("Monitor", "Use KPIs to confirm movement and catch regression early."),
        ]
    return [
        ("Assess", "Review current workflow, payer mix, backlog, systems, and reporting needs."),
        ("Prioritize", "Segment work by risk, value, aging, denial reason, and next action."),
        ("Execute", "Apply disciplined billing, follow-up, automation, and escalation workflows."),
        ("Report", "Surface KPIs, bottlenecks, and recommended next steps for leadership."),
    ]


def kpi_items(page: Page) -> list[str]:
    return [
        "Clean claim rate",
        "First pass claim rate",
        "Denial rate and denial overturn movement",
        "Days in AR and AR over 90 days",
        "Net collection rate",
        "Payer follow-up productivity",
    ]


def faq_items(page: Page) -> list[tuple[str, str]]:
    return [
        (f"What is {page.name}?", f"{page.name} is part of the revenue cycle workflow Resolute MSO uses to improve claim movement, reduce preventable leakage, and make billing work easier to manage."),
        ("Who should get Resolute MSO services?", f"Resolute MSO services are useful for U.S. healthcare providers, billing teams, practice administrators, and RCM leaders who need clearer workflows, payer follow-up, automation support, and measurable revenue cycle visibility."),
        ("Does Resolute MSO guarantee specific collection results?", "No. Resolute MSO uses realistic operating goals and target outcomes. Public pages describe focus areas, not guaranteed financial results."),
        ("Can I submit patient details through the website?", "No. Public website forms are for business inquiries only. Do not submit PHI, patient names, claim numbers, or patient information."),
    ]


def related_slugs(page: Page) -> list[str]:
    if page.related:
        return page.related
    pool = [p.slug for p in pages if p.category == page.category and p.slug != page.slug and not p.noindex]
    defaults = ["free-rcm-audit", "contact", "chargepilot", "all-rcm-solutions"]
    selected = pool[:4]
    for slug in defaults:
        if slug != page.slug and slug not in selected:
            selected.append(slug)
    return selected[:6]


def hero(page: Page) -> str:
    takeaways = [
        "Clear operating summary for healthcare revenue leaders.",
        "Clear route to audit, contact, and related RCM pages.",
        "HIPAA-conscious public inquiry path with no PHI requested.",
    ]
    if page.category == "automation":
        takeaways[0] = "Automation should reduce repetitive billing work while preserving human oversight."
    if page.category == "specialty":
        takeaways[0] = "Specialty billing needs payer-aware workflows, denial prevention, and specialty KPI visibility."
    takeaway_html = "".join(f"<li>{e(item)}</li>" for item in takeaways)
    return f"""
<section class="hero sub-hero">
  <div class="container hero-grid">
    <div>
      {breadcrumbs(page)}
      <p class="kicker">{category_label(page)}</p>
      <h1>{e(h1(page))}</h1>
      <p class="lead">{e(summary(page))}</p>
      <div class="hero-actions">
        <a class="btn" href="{page.cta_href}">{e(page.cta)}</a>
        <a class="btn btn-secondary" href="{page.secondary_href}">{e(page.secondary_cta)}</a>
      </div>
      <p class="phi-note">Public forms are for business inquiries only. Do not submit PHI or patient information.</p>
    </div>
    <div class="dashboard-visual" role="img" aria-label="Revenue cycle dashboard visual">
      <div class="dash-top"><span></span><span></span><span></span></div>
      <div class="metric-strip">
        <div><strong>Clean Claims</strong><span>Focus area</span></div>
        <div><strong>AR Visibility</strong><span>Operating signal</span></div>
        <div><strong>Denials</strong><span>Prevention loop</span></div>
      </div>
      <div class="chart-lines"><i></i><i></i><i></i><i></i></div>
      <ul class="takeaways">{takeaway_html}</ul>
    </div>
  </div>
</section>"""


def card_grid(title: str, intro: str, items: list[str], cls: str = "") -> str:
    cards = "".join(f"<article class='info-card'><h3>{e(item)}</h3><p>{e(intro_for_item(item))}</p></article>" for item in items)
    return f"""
<section class="section {cls}">
  <div class="container">
    <div class="section-head">
      <p class="kicker">{e(title)}</p>
      <h2>{e(intro)}</h2>
    </div>
    <div class="card-grid">{cards}</div>
  </div>
</section>"""


def intro_for_item(item: str) -> str:
    lower = item.lower()
    if "public" in lower or "phi" in lower:
        return "Handled with clear website notices and business-only intake fields."
    if "dashboard" in lower or "visibility" in lower or "kpi" in lower:
        return "Tracked through concise signals that help leaders see the next operational move."
    if "automation" in lower or "manual" in lower:
        return "Reviewed for workflow fit, exception handling, and human oversight."
    if "denial" in lower:
        return "Managed through root-cause review, prevention feedback, and follow-up discipline."
    if "ar" in lower or "payer" in lower:
        return "Prioritized by aging, risk, value, payer behavior, and next action."
    return "Mapped to clear workflow ownership, measurable outputs, and practical next steps."


def answer_blocks(page: Page) -> str:
    return f"""
<section class="section answer-section">
  <div class="container answer-grid">
    <article>
      <p class="kicker">What Is This?</p>
      <h2>{e(page.name)} in plain terms.</h2>
      <p>{e(summary(page))}</p>
    </article>
    <article>
      <p class="kicker">Who Is This For?</p>
      <p>{e(' '.join(audience_items(page)[:2]))}. It is especially useful when billing work needs more structure, visibility, or automation support.</p>
    </article>
    <article>
      <p class="kicker">What Problem Does It Solve?</p>
      <p>{e(problem_items(page)[0])}. Resolute MSO connects process review, follow-up discipline, reporting, and automation where it fits.</p>
    </article>
    <article>
      <p class="kicker">When To Use It</p>
      <p>Use this when revenue teams see recurring rework, slow payer movement, preventable denials, aging AR, or limited management visibility.</p>
    </article>
  </div>
</section>"""


def workflow_section(page: Page) -> str:
    steps = "".join(
        f"<article><span>{i}</span><h3>{e(title)}</h3><p>{e(copy)}</p></article>"
        for i, (title, copy) in enumerate(workflow_items(page), 1)
    )
    return f"""
<section class="section section-soft">
  <div class="container">
    <div class="section-head">
      <p class="kicker">Workflow</p>
      <h2>How Resolute MSO approaches {e(page.name.lower())}.</h2>
      <p>Every engagement starts with operational context, not generic promises. The goal is to create cleaner work queues, better visibility, and fewer avoidable surprises.</p>
    </div>
    <div class="workflow-grid">{steps}</div>
  </div>
</section>"""


def kpi_section(page: Page) -> str:
    items = "".join(f"<li>{e(item)}</li>" for item in kpi_items(page))
    return f"""
<section class="section">
  <div class="container split">
    <div>
      <p class="kicker">Operating Signals</p>
      <h2>KPIs and target outcomes we watch.</h2>
      <p>These are focus areas, not guaranteed results. Resolute MSO uses them to guide improvement conversations, prioritize work, and clarify whether the revenue cycle is moving in the right direction.</p>
      <ul class="check-list">{items}</ul>
    </div>
    <div class="metric-panel" aria-label="RCM KPI visual">
      <div><strong>Clean claim rate</strong><span style="width:86%"></span></div>
      <div><strong>AR over 90</strong><span style="width:38%"></span></div>
      <div><strong>Denial prevention</strong><span style="width:74%"></span></div>
      <div><strong>Automation lift</strong><span style="width:68%"></span></div>
    </div>
  </div>
</section>"""


def related_section(page: Page) -> str:
    links = []
    for slug in related_slugs(page):
        if slug in PAGE_BY_SLUG:
            p = PAGE_BY_SLUG[slug]
            links.append(f'<a href="{p.path}"><span>{e(category_label(p))}</span><strong>{e(p.name)}</strong></a>')
    return f"""
<section class="section section-soft">
  <div class="container">
    <div class="section-head">
      <p class="kicker">Next Step</p>
      <h2>Related Resolute MSO pages.</h2>
    </div>
    <div class="related-grid">{''.join(links)}</div>
  </div>
</section>"""


def faq_section(page: Page) -> str:
    faq = faq_items(page)
    items = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in faq)
    return f"""
<section class="section">
  <div class="container narrow">
    <div class="section-head">
      <p class="kicker">FAQs</p>
      <h2>Common questions about {e(page.name.lower())}.</h2>
    </div>
    <div class="faq-list">{items}</div>
  </div>
</section>"""


def cta_band(page: Page) -> str:
    return f"""
<section class="section final-cta">
  <div class="container cta-grid">
    <div>
      <p class="kicker">Revenue Cycle Next Step</p>
      <h2>See where billing work can move faster, cleaner, and with better visibility.</h2>
      <p>Tell us whether you need help with RCM, medical billing, denials, AR follow-up, ChargePilot, or automation assessment.</p>
    </div>
    <div class="cta-actions">
      <a class="btn" href="{page.cta_href}">{e(page.cta)}</a>
      <a class="btn btn-secondary" href="{WHATSAPP_URL}">Talk to Resolute MSO</a>
    </div>
  </div>
</section>"""


def render_standard(page: Page) -> str:
    problems = problem_items(page)
    audience = audience_items(page)
    body = (
        hero(page)
        + answer_blocks(page)
        + card_grid("Who It Helps", f"{page.name} is built for teams that need practical RCM support.", audience)
        + card_grid("Problems Solved", "Common issues this page addresses.", problems, "section-soft")
        + workflow_section(page)
        + kpi_section(page)
        + related_section(page)
        + faq_section(page)
        + cta_band(page)
    )
    return layout(page, body, faq_items(page))


def render_hub(page: Page) -> str:
    groups = [
        ("Core Services", group_pages("service")[:12], "Direct RCM and medical billing services."),
        ("Specialty Billing", group_pages("specialty")[:12], "Specialty-aware billing support for provider segments."),
        ("Automation and AI", group_pages("automation")[:12], "Workflow automation, ChargePilot, and dashboard support."),
        ("Buyer Guides", group_pages("buyer")[:12], "Decision pages for owners and revenue leaders."),
        ("Resources", group_pages("resource")[:12], "Plain-English guides for billing and RCM teams."),
    ]
    directory = ""
    for title, group, intro in groups:
        cards = "".join(f'<a class="directory-card" href="{p.path}"><span>{e(category_label(p))}</span><strong>{e(p.name)}</strong><p>{e(meta_description(p))}</p></a>' for p in group)
        directory += f'<section class="directory-block" id="{slugify(title)}"><div class="container"><div class="section-head"><p class="kicker">{e(title)}</p><h2>{e(intro)}</h2></div><div class="directory-grid">{cards}</div></div></section>'
    body = hero(page) + directory + related_section(page) + cta_band(page)
    return layout(page, body, faq_items(page))


def render_all(page: Page) -> str:
    groups = [
        ("Core Pages", [p for p in pages if p.category in {"home", "company", "hub", "conversion", "product"} and not p.noindex]),
        ("RCM Services", group_pages("service")),
        ("Specialty Billing", group_pages("specialty")),
        ("Automation and AI", group_pages("automation")),
        ("Buyer Intent", group_pages("buyer")),
        ("Guides and Resources", group_pages("resource")),
    ]
    blocks = ""
    for title, group in groups:
        links = "".join(f'<li><a href="{p.path}">{e(p.name)}</a><span>{e(", ".join(p.keywords[:2]))}</span></li>' for p in group)
        blocks += f'<section class="solution-group" id="{slugify(title)}"><h2>{e(title)}</h2><ul>{links}</ul></section>'
    body = f"""
<section class="hero sub-hero">
  <div class="container">
    {breadcrumbs(page)}
    <p class="kicker">Complete Directory</p>
    <h1>{e(h1(page))}</h1>
    <p class="lead">{e(summary(page))}</p>
    <div class="hero-actions"><a class="btn" href="/free-rcm-audit.html">Book a Revenue Audit</a><a class="btn btn-secondary" href="{WHATSAPP_URL}">Talk to Resolute MSO</a></div>
  </div>
</section>
<section class="section"><div class="container solutions-index">{blocks}</div></section>
{cta_band(page)}
"""
    return layout(page, body, faq_items(page))


def render_home(page: Page) -> str:
    service_cards = "".join(
        f'<a class="info-card" href="{p.path}"><h3>{e(p.name)}</h3><p>{e(meta_description(p))}</p></a>'
        for p in [PAGE_BY_SLUG[s] for s in ["medical-billing-services", "revenue-cycle-management-services", "denial-management-services", "ar-follow-up-services", "eligibility-verification-services", "payment-posting-services"]]
    )
    specialties = "".join(
        f'<a class="directory-card" href="{PAGE_BY_SLUG[s].path}"><span>Specialty</span><strong>{e(PAGE_BY_SLUG[s].name)}</strong></a>'
        for s in ["clinical-lab-billing-services", "toxicology-lab-billing-services", "imaging-center-billing-services", "radiology-billing-services", "urgent-care-billing-services", "mental-health-billing-services", "physical-therapy-billing-services", "dme-billing-services"]
    )
    faq = [
        ("What does Resolute MSO do?", "Resolute MSO provides AI-powered revenue cycle management, medical billing services, healthcare operations support, automation assessment, and ChargePilot billing software automation for U.S. healthcare providers."),
        ("Who does Resolute MSO serve?", "Resolute MSO serves physician practices, groups, specialty clinics, laboratories, imaging centers, urgent care centers, RCM companies, and healthcare revenue leaders."),
        ("What is ChargePilot?", "ChargePilot is Resolute MSO's billing software claim-entry and claim-submission automation product for billing teams and RCM operations."),
        ("Can website forms include patient information?", "No. Public forms are for business inquiries only. Do not submit PHI or patient information."),
    ]
    body = f"""
<section class="hero home-hero">
  <div class="container hero-grid">
    <div>
      <p class="kicker">Advance Healthcare Solutions</p>
      <h1 class="hero-typewriter" data-typewriter-text="{e(h1(page))}"><span class="typewriter-sizer" aria-hidden="true">{e(h1(page))}</span><span class="typewriter-output" aria-hidden="true">{e(h1(page))}</span><span class="sr-only">{e(h1(page))}</span></h1>
      <p class="lead">Resolute MSO helps U.S. healthcare providers reduce revenue leakage, improve A/R movement, reduce preventable denials, automate repetitive billing workflows, and gain revenue cycle visibility.</p>
      <div class="hero-actions">
        <a class="btn" href="/free-rcm-audit.html">Book a Revenue Audit</a>
        <a class="btn btn-secondary" href="/chargepilot.html">Discuss ChargePilot</a>
        <a class="btn btn-whatsapp" href="{WHATSAPP_URL}">Talk on WhatsApp</a>
      </div>
      <p class="phi-note">Public forms are for business inquiries only. Do not submit PHI or patient information.</p>
    </div>
    <figure class="hero-image">
      <img src="{HOME_HERO_IMAGE}" alt="Healthcare revenue cycle team discussing RCM dashboard metrics in a clinical operations office" width="1200" height="675" fetchpriority="high" decoding="async">
    </figure>
  </div>
</section>
<section class="section outcome-strip" aria-label="Revenue cycle operating focus">
  <div class="container outcome-grid">
    <article><strong>Clean claims</strong><span>Front-end accuracy and claim readiness.</span></article>
    <article><strong>AR visibility</strong><span>Payer action, aging, and follow-up clarity.</span></article>
    <article><strong>Denial prevention</strong><span>Root-cause loops and prevention feedback.</span></article>
    <article><strong>Automation lift</strong><span>Less repetitive manual billing work.</span></article>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="section-head"><p class="kicker">Workflow Familiarity</p><h2>Support for the systems revenue teams already work around.</h2><p>Resolute MSO supports billing workflows around common practice management, clearinghouse, EHR, and LIS environments. Platform names describe workflow familiarity and support, not official integration unless separately confirmed.</p></div>
    <div class="platform-strip"><span><b>OA</b><em>OfficeAlly</em></span><span><b>eCW</b><em>eClinicalWorks</em></span><span><b>CC</b><em>CareCloud</em></span><span><b>NG</b><em>NextGen</em></span><span><b>AH</b><em>Athenahealth</em></span><span><b>AMD</b><em>AdvancedMD</em></span><span><b>MM</b><em>ModMed</em></span><span><b>LIS</b><em>Telcor LIS</em></span></div>
  </div>
</section>
<section class="section section-soft">
  <div class="container split">
    <div>
      <p class="kicker">Pain Points To Outcomes</p>
      <h2>From billing noise to revenue cycle control.</h2>
      <p>Providers do not need more generic dashboards. They need cleaner intake, disciplined follow-up, denial prevention, automation where it fits, and leadership reporting that shows what to do next.</p>
      <ul class="check-list"><li>Reduce preventable claim denials</li><li>Improve clean claim and first pass readiness</li><li>Prioritize AR over 90 days</li><li>Identify underpayments and revenue leakage</li><li>Automate repetitive claim-entry tasks with oversight</li></ul>
    </div>
    <div class="metric-panel"><div><strong>Denial trend</strong><span style="width:42%"></span></div><div><strong>Clean claim readiness</strong><span style="width:82%"></span></div><div><strong>AR action coverage</strong><span style="width:76%"></span></div><div><strong>Automation queue</strong><span style="width:67%"></span></div></div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="section-head"><p class="kicker">Core Services</p><h2>Medical billing and RCM support built around claim movement.</h2></div>
    <div class="card-grid">{service_cards}</div>
    <div class="center"><a class="btn btn-secondary" href="/services.html">View All RCM Solutions</a></div>
  </div>
</section>
<section class="section product-band">
  <div class="container split">
    <div>
      <p class="kicker">ChargePilot</p>
      <h2>Billing software claim-entry automation for billing teams.</h2>
      <p>ChargePilot automates repetitive claim-entry and claim-submission workflows across supported billing software and PM environments with a desktop automation control center, web-based admin/client portal, throughput visibility, and exception handling.</p>
      <ul class="check-list"><li>For practices, billing companies, and RCM teams with repetitive billing software workflows</li><li>Supports human oversight and exception review</li><li>Designed for repetitive claim-entry volume</li></ul>
      <div class="hero-actions"><a class="btn" href="/chargepilot.html">Discuss ChargePilot</a><a class="btn btn-secondary" href="/chargepilot-implementation.html">View Implementation</a></div>
    </div>
    <div class="dashboard-visual chargepilot-dashboard" role="img" aria-label="ChargePilot dashboard visual"><div class="dash-top"><span></span><span></span><span></span><strong>ChargePilot Dashboard</strong></div><div class="metric-strip"><div><strong>Queue</strong><span>Ready</span></div><div><strong>Exceptions</strong><span>Review</span></div><div><strong>Throughput</strong><span>Visible</span></div></div><div class="chart-lines"><i></i><i></i><i></i><i></i></div><div class="dashboard-table"><span>Claim batch</span><span>Status</span><span>Owner</span><span>PM import</span><span>Ready</span><span>Automation</span><span>Missing field</span><span>Exception</span><span>Billing lead</span></div></div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="section-head"><p class="kicker">Who We Serve</p><h2>Built for provider revenue leaders and billing operations.</h2></div>
    <div class="directory-grid">{specialties}</div>
  </div>
</section>
<section class="section section-soft">
  <div class="container split">
    <div>
      <p class="kicker">Trust and Compliance</p>
      <h2>Operational clarity, realistic claims, and HIPAA-conscious intake.</h2>
      <p>Resolute MSO describes target outcomes and focus areas without fake guarantees. Public forms are business-only, and service pages explain process, KPIs, related workflows, and limitations.</p>
    </div>
    <div class="trust-list"><a href="/about.html">About Resolute MSO</a><a href="/rcm-expertise.html">RCM Expertise</a><a href="/quality-compliance.html">Quality Commitment</a><a href="/compliance.html">Compliance</a></div>
  </div>
</section>
{faq_section(page)}
{cta_band(page)}
"""
    return layout(page, body, faq)


def render_chargepilot(page: Page) -> str:
    faq = [
        ("What is ChargePilot?", "ChargePilot is Resolute MSO's billing software claim-entry and claim-submission automation product for medical billing teams and RCM operations."),
        ("Who is ChargePilot for?", "ChargePilot is for practices, billing companies, and RCM teams using supported billing software workflows that include repetitive claim entry, charge entry, and claim submission tasks."),
        ("Does ChargePilot replace billing staff?", "No. ChargePilot is positioned as workflow automation with human oversight, exception handling, and billing-team control."),
        ("How is ChargePilot pricing handled?", "Pricing is scoped after reviewing workflow volume, implementation needs, support requirements, and automation complexity."),
    ]
    body = f"""
<section class="hero sub-hero">
  <div class="container hero-grid">
    <div>{breadcrumbs(page)}<p class="kicker">ChargePilot</p><h1>ChargePilot billing software automation for RCM teams.</h1><p class="lead">ChargePilot is Resolute MSO's claim-entry and claim-submission automation product for billing teams that need throughput visibility, exception handling, and a controlled desktop plus web portal workflow across supported billing software environments.</p><div class="hero-actions"><a class="btn" href="#chargepilot-assessment">Get Automation Assessment</a><a class="btn btn-secondary" href="/chargepilot-pricing.html">Request Pricing</a><a class="btn btn-whatsapp" href="{WHATSAPP_URL}">Talk on WhatsApp</a></div><p class="phi-note">Public forms are for business inquiries only. Do not submit PHI or patient information.</p></div>
    <div class="dashboard-visual chargepilot-dashboard" role="img" aria-label="ChargePilot dashboard visual"><div class="dash-top"><span></span><span></span><span></span><strong>ChargePilot Dashboard</strong></div><div class="metric-strip"><div><strong>Desktop Control</strong><span>Run/stop</span></div><div><strong>Portal</strong><span>Visibility</span></div><div><strong>Exceptions</strong><span>Review</span></div></div><div class="chart-lines"><i></i><i></i><i></i><i></i></div><div class="dashboard-table"><span>Queue</span><span>Status</span><span>Action</span><span>Batch 1042</span><span>Ready</span><span>Run</span><span>Batch 1043</span><span>Exception</span><span>Review</span></div></div>
  </div>
</section>
<section class="section"><div class="container answer-grid"><article><p class="kicker">What It Does</p><h2>Automates repetitive billing software claim-entry work.</h2><p>ChargePilot supports billing teams with repeatable claim-entry and submission workflows, throughput reporting, and exception handling. It is designed for operational control, not unsupported autonomous billing decisions.</p></article><article><p class="kicker">Control Center</p><p>A desktop automation control center supports run control, input selection, job status, and production monitoring.</p></article><article><p class="kicker">Admin Portal</p><p>A web-based admin and client portal can provide visibility into throughput, exceptions, support, and workflow performance.</p></article><article><p class="kicker">Implementation</p><p>Resolute MSO maps current workflow, validates source files, configures automation, trains users, and supports go-live with human oversight.</p></article></div></section>
<section class="section section-soft"><div class="container"><div class="section-head"><p class="kicker">Features</p><h2>Built for billing teams with repetitive claim-entry volume.</h2></div><div class="card-grid"><article class="info-card"><h3>Claim-entry automation</h3><p>Reduces repetitive manual data entry for supported billing software workflows.</p></article><article class="info-card"><h3>Exception handling</h3><p>Routes incomplete, risky, or mismatched records to human review.</p></article><article class="info-card"><h3>Throughput visibility</h3><p>Helps leaders see volume, queue movement, and workflow patterns.</p></article><article class="info-card"><h3>Desktop plus portal</h3><p>Combines execution controls with web-based oversight and support views.</p></article></div></div></section>
<section class="section"><div class="container split"><div><p class="kicker">Pricing</p><h2>Scoped after workflow assessment.</h2><p>ChargePilot pricing depends on workflow complexity, volume, implementation support, source data quality, exception handling, and portal requirements. Resolute MSO will review the workflow before quoting.</p><ul class="check-list"><li>Workflow and data-source review</li><li>Automation scope and exception handling</li><li>Implementation and support requirements</li></ul></div><div class="metric-panel"><div><strong>Workflow fit</strong><span style="width:88%"></span></div><div><strong>Exception review</strong><span style="width:70%"></span></div><div><strong>Portal needs</strong><span style="width:62%"></span></div></div></div></section>
<section class="section section-soft" id="chargepilot-assessment"><div class="container form-grid"><div><p class="kicker">ChargePilot Assessment</p><h2>Discuss billing software automation.</h2><p>Use this business-only form to request a ChargePilot workflow discussion. Do not include PHI, patient details, claim numbers, or screenshots containing patient data.</p></div>{form_html("ChargePilot automation assessment", "Discuss ChargePilot", include_services=False)}</div></section>
{faq_section(page)}
{related_section(page)}
{cta_band(page)}
"""
    return layout(page, body, faq)


def render_article(page: Page) -> str:
    article = BLOG_ARTICLES[page.slug]
    takeaways = "".join(f"<li>{e(item)}</li>" for item in article["takeaways"])
    sections = "".join(
        f"<section><h2>{e(title)}</h2><p>{e(copy)}</p></section>"
        for title, copy in article["sections"]
    )
    sources = "".join(f'<li><a href="{href}" target="_blank" rel="noopener">{e(label)}</a></li>' for label, href in article["sources"])
    body = f"""
<article class="article-page">
  <section class="hero sub-hero">
    <div class="container narrow">
      {breadcrumbs(page)}
      <p class="kicker">Resolute MSO Blog</p>
      <h1>{e(page.name)}</h1>
      <p class="lead">{e(article["summary"])}</p>
      <div class="hero-actions"><a class="btn" href="/free-rcm-audit.html">Book a Revenue Audit</a><a class="btn btn-secondary" href="/blog.html">View All Blogs</a><a class="btn btn-whatsapp" href="{WHATSAPP_URL}">Talk on WhatsApp</a></div>
    </div>
  </section>
  <section class="section">
    <div class="container article-grid">
      <aside class="article-aside">
        <p class="kicker">Key Takeaways</p>
        <ul class="check-list">{takeaways}</ul>
      </aside>
      <div class="article-body">
        <p><strong>Short answer:</strong> {e(article["summary"])}</p>
        {sections}
        <section class="source-list">
          <h2>References</h2>
          <p>These articles are written by Resolute MSO for business education and link to official U.S. healthcare resources for context.</p>
          <ul>{sources}</ul>
        </section>
      </div>
    </div>
  </section>
</article>
{related_section(page)}
{cta_band(page)}
"""
    return layout(page, body, faq_items(page))


def render_blog_index(page: Page) -> str:
    cards = "".join(
        f'<a class="info-card article-card" href="{PAGE_BY_SLUG[slug].path}"><span>Resolute MSO Blog</span><h3>{e(data["name"])}</h3><p>{e(data["summary"])}</p></a>'
        for slug, data in BLOG_ARTICLES.items()
    )
    body = f"""
<section class="hero sub-hero">
  <div class="container">
    {breadcrumbs(page)}
    <p class="kicker">Blogs</p>
    <h1>Resolute MSO blogs for RCM, billing automation, and healthcare revenue teams.</h1>
    <p class="lead">{e(summary(page))}</p>
    <div class="hero-actions"><a class="btn" href="/free-rcm-audit.html">Book a Revenue Audit</a><a class="btn btn-secondary" href="/all-rcm-solutions.html">View All RCM Solutions</a></div>
  </div>
</section>
<section class="section"><div class="container"><div class="card-grid">{cards}</div></div></section>
{cta_band(page)}
"""
    return layout(page, body, faq_items(page))


def form_html(subject: str, button: str, include_services: bool = True) -> str:
    services = ""
    if include_services:
        services = """
      <label for="service-interest">Service interest
        <select id="service-interest" name="service_interest">
          <option>Revenue cycle management</option>
          <option>Medical billing services</option>
          <option>Denial management</option>
          <option>AR follow-up</option>
          <option>ChargePilot automation</option>
          <option>Practice Health Dashboard</option>
        </select>
      </label>"""
    return f"""
    <form class="lead-form" action="{FORM_ENDPOINT}" method="POST">
      <input type="hidden" name="_subject" value="{e(subject)}">
      <input type="hidden" name="_captcha" value="false">
      <input type="hidden" name="_template" value="table">
      <input type="text" name="_honey" tabindex="-1" autocomplete="off" class="honey-field" aria-hidden="true">
      <label for="{slugify(subject)}-name">Name
        <input id="{slugify(subject)}-name" name="name" type="text" autocomplete="name" required>
      </label>
      <label for="{slugify(subject)}-email">Work email
        <input id="{slugify(subject)}-email" name="email" type="email" autocomplete="email" required>
      </label>
      <label for="{slugify(subject)}-org">Organization
        <input id="{slugify(subject)}-org" name="organization" type="text" autocomplete="organization" required>
      </label>
      {services}
      <label for="{slugify(subject)}-message">Business inquiry
        <textarea id="{slugify(subject)}-message" name="message" rows="5" placeholder="Describe your business need. Do not include PHI or patient information." required></textarea>
      </label>
      <p class="phi-note">Public forms are for business inquiries only. Do not submit PHI, patient names, claim numbers, medical record numbers, or patient information.</p>
      <button class="btn" type="submit">{e(button)}</button>
    </form>"""


def render_contact(page: Page) -> str:
    body = f"""
<section class="hero sub-hero"><div class="container">{breadcrumbs(page)}<p class="kicker">Contact</p><h1>Talk to Resolute MSO about RCM, billing, automation, or ChargePilot.</h1><p class="lead">Send a business inquiry and the Resolute MSO team will route it to the right revenue cycle, automation, or operations conversation.</p></div></section>
<section class="section"><div class="container form-grid"><div><p class="kicker">Business Inquiry</p><h2>Start with the problem you want to solve.</h2><p>Email <a href="mailto:support@resolutemso.com">support@resolutemso.com</a>, call <a href="tel:+17015525527">+1 701 552 5527</a>, or use the form. Public forms are not a patient portal.</p></div>{form_html("Resolute MSO contact inquiry", "Send Business Inquiry")}</div></section>
{related_section(page)}
"""
    return layout(page, body, faq_items(page))


def render_audit(page: Page) -> str:
    body = f"""
<section class="hero sub-hero"><div class="container">{breadcrumbs(page)}<p class="kicker">Free RCM Audit</p><h1>Book a focused revenue cycle audit conversation.</h1><p class="lead">Use this business-only form to discuss denials, AR over 90 days, clean claim readiness, underpayments, staffing, reporting, or automation opportunities.</p></div></section>
<section class="section"><div class="container form-grid"><div><p class="kicker">Audit Scope</p><h2>What we can review at a high level.</h2><ul class="check-list"><li>Denial and rejection patterns</li><li>Aging AR and payer follow-up gaps</li><li>Eligibility and authorization workflow risk</li><li>Claim submission and clean claim readiness</li><li>Automation opportunities for repetitive work</li></ul></div>{form_html("Free RCM audit request", "Request Free RCM Audit")}</div></section>
{related_section(page)}
"""
    return layout(page, body, faq_items(page))


def render_feedback(page: Page) -> str:
    body = f"""
<section class="hero sub-hero"><div class="container">{breadcrumbs(page)}<p class="kicker">Service Feedback</p><h1>Share service feedback with Resolute MSO.</h1><p class="lead">This page supports quality improvement, service review, and operational accountability. Do not include PHI or patient information.</p></div></section>
<section class="section"><div class="container form-grid"><div><p class="kicker">Quality Loop</p><h2>Feedback helps improve service discipline.</h2><p>Use this business-only channel for service comments, process concerns, or quality improvement suggestions.</p></div>{form_html("Resolute MSO service feedback", "Send Feedback", include_services=False)}</div></section>
{related_section(page)}
"""
    return layout(page, body, faq_items(page))


def render_privacy(page: Page) -> str:
    body = f"""
<section class="hero sub-hero"><div class="container">{breadcrumbs(page)}<p class="kicker">Privacy</p><h1>Privacy Policy and public website notice.</h1><p class="lead">Resolute MSO public website forms are for business inquiries only and must not be used to submit PHI or patient information.</p></div></section>
<section class="section"><div class="container narrow legal-copy"><h2>Public website use</h2><p>This website is intended for general business communication about medical billing, revenue cycle management, automation, and healthcare operations services. It is not a patient portal.</p><h2>PHI notice</h2><p>Do not submit protected health information, patient names, claim numbers, medical record numbers, dates of service, screenshots containing patient data, or patient information through public forms.</p><h2>Business inquiry data</h2><p>Forms may request business contact details such as name, work email, organization, role, phone number, and a non-PHI description of the business need. This information is used to respond to inquiries and route conversations.</p><h2>Third-party form processing</h2><p>Static website forms may use a form delivery service such as FormSubmit. Do not include sensitive patient or claim details in these submissions.</p><h2>Contact</h2><p>For privacy questions, contact <a href="mailto:support@resolutemso.com">support@resolutemso.com</a>.</p></div></section>
{related_section(page)}
"""
    return layout(page, body, faq_items(page))


def render_redirect(page: Page, target: str = "/") -> str:
    return clean_internal_links(f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(page.name)} | Resolute MSO</title>
  <meta name="robots" content="noindex, follow">
  <link rel="canonical" href="{SITE}{target}">
  <meta http-equiv="refresh" content="0; url={target}">
</head>
<body>
  <p>Redirecting to <a href="{target}">Resolute MSO</a>.</p>
</body>
</html>
""")


def render_404() -> str:
    known = sorted(p.slug for p in pages if not p.noindex and p.slug != "index")
    known_js = json.dumps(known)
    links = "".join(f'<a href="{PAGE_BY_SLUG[s].path}">{e(PAGE_BY_SLUG[s].name)}</a>' for s in ["services", "chargepilot", "all-rcm-solutions", "medical-billing-services", "denial-management-services", "clinical-lab-billing-services", "officeally-claim-entry-automation", "contact"])
    return clean_internal_links(f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Page Not Found | Resolute MSO</title>
  <meta name="description" content="Resolute MSO page not found with links to RCM services, ChargePilot, and contact pages.">
  <meta name="robots" content="noindex, follow">
  <style>{minify_css(CSS)}</style>
  <script>
    (function () {{
      var known = {known_js};
      var path = window.location.pathname.replace(/^\\/+|\\/+$/g, "");
      if (path && known.indexOf(path) !== -1) {{
        window.location.replace("/" + path + "/" + window.location.search + window.location.hash);
      }}
    }})();
  </script>
</head>
<body>
{header(PAGE_BY_SLUG["index"])}
<main id="main">
  <section class="hero sub-hero"><div class="container"><p class="kicker">404</p><h1>We could not find that page.</h1><p class="lead">The page may have moved, but the main RCM and automation paths are below.</p><div class="hero-actions"><a class="btn" href="/">Return Home</a><a class="btn btn-secondary" href="/contact.html">Contact Resolute MSO</a></div></div></section>
  <section class="section"><div class="container related-grid">{links}</div></section>
</main>
{footer()}
</body>
</html>
""")


def render_thanks() -> str:
    page = Page("thank-you", "Thank You", "conversion", "Lead confirmation", ["thank you"], noindex=True)
    body = """<section class="hero sub-hero"><div class="container"><p class="kicker">Thank You</p><h1>Your inquiry has been received.</h1><p class="lead">Resolute MSO will review the business inquiry and follow up through the contact details provided. Do not send PHI through public website channels.</p><div class="hero-actions"><a class="btn" href="/">Return Home</a><a class="btn btn-secondary" href="/all-rcm-solutions.html">View All RCM Solutions</a></div></div></section>"""
    return layout(page, body)


def render_page(page: Page) -> str:
    if page.template == "home":
        return render_home(page)
    if page.slug == "blog":
        return render_blog_index(page)
    if page.slug in BLOG_ARTICLES:
        return render_article(page)
    if page.template == "redirect":
        return render_redirect(page, "/")
    if page.template == "hub":
        return render_hub(page)
    if page.template == "all":
        return render_all(page)
    if page.template == "chargepilot":
        return render_chargepilot(page)
    if page.template == "contact":
        return render_contact(page)
    if page.template == "audit":
        return render_audit(page)
    if page.template == "feedback":
        return render_feedback(page)
    if page.template == "privacy":
        return render_privacy(page)
    return render_standard(page)


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


CSS = r"""
:root {
  --bg: #ffffff;
  --soft: #f7faf9;
  --soft-2: #fafbf9;
  --ink: #08090a;
  --text: #101418;
  --muted: #667085;
  --teal: #0f9d8f;
  --teal-dark: #087a70;
  --teal-soft: #eaf8f6;
  --border: #e7ecea;
  --dark: #031827;
  --shadow: 0 14px 32px rgba(16, 24, 40, .07);
  --radius: 8px;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body { margin: 0; font-family: Arial, Helvetica, sans-serif; color: var(--text); background: var(--bg); line-height: 1.6; }
img { max-width: 100%; display: block; }
a { color: inherit; text-decoration: none; }
a:hover { color: var(--teal-dark); }
button, input, textarea, select { font: inherit; }
.container { width: min(1160px, calc(100% - 40px)); margin: 0 auto; }
.narrow { max-width: 860px; }
.skip-link { position: absolute; left: -999px; top: 8px; background: var(--ink); color: #fff; padding: 10px 14px; z-index: 100; border-radius: var(--radius); }
.skip-link:focus { left: 8px; }
.site-header { position: sticky; top: 0; z-index: 50; background: rgba(255,255,255,.96); border-bottom: 1px solid var(--border); backdrop-filter: blur(16px); }
.nav-shell { min-height: 74px; display: flex; align-items: center; gap: 12px; width: min(1280px, calc(100% - 28px)); margin: 0 auto; }
.brand img { width: 210px; height: auto; }
.main-nav { margin-left: auto; }
.main-nav ul { display: flex; align-items: center; gap: 0; padding: 0; margin: 0; list-style: none; }
.nav-item { position: relative; display: flex; align-items: center; }
.main-nav a, .menu-caret { min-height: 40px; display: inline-flex; align-items: center; border: 0; background: transparent; border-radius: var(--radius); padding: 0 8px; color: var(--text); font-weight: 700; }
.main-nav a:hover, .main-nav a:focus-visible, .main-nav a.active, .menu-caret:hover, .menu-caret:focus-visible { background: var(--teal-soft); color: var(--teal-dark); }
.menu-caret { width: 24px; justify-content: center; cursor: pointer; }
.menu-caret span { width: 7px; height: 7px; border-right: 2px solid currentColor; border-bottom: 2px solid currentColor; transform: rotate(45deg) translateY(-2px); }
.dropdown { position: absolute; left: 0; top: 100%; width: 270px; background: #fff; border: 1px solid var(--border); box-shadow: var(--shadow); border-radius: var(--radius); padding: 8px; opacity: 0; visibility: hidden; transform: translateY(6px); transition: .18s ease; }
.dropdown a { display: flex; width: 100%; justify-content: flex-start; padding: 10px 12px; min-height: 0; }
.has-menu:hover .dropdown, .has-menu:focus-within .dropdown, .has-menu.open .dropdown { opacity: 1; visibility: visible; transform: translateY(0); }
.nav-toggle { display: none; border: 1px solid var(--border); background: #fff; border-radius: 999px; padding: 9px 14px; font-weight: 800; color: var(--ink); }
.btn { display: inline-flex; align-items: center; justify-content: center; min-height: 42px; border-radius: 999px; padding: 9px 16px; background: var(--teal); color: #fff; font-weight: 800; border: 1px solid var(--teal); box-shadow: 0 10px 24px rgba(15,157,143,.18); transition: .18s ease; white-space: nowrap; }
.btn:hover, .btn:focus-visible { background: var(--teal-dark); color: #fff; transform: translateY(-1px); }
.btn-secondary { background: #fff; color: var(--teal-dark); border-color: var(--border); box-shadow: none; }
.btn-secondary:hover, .btn-secondary:focus-visible { background: var(--teal-soft); color: var(--teal-dark); }
.btn-whatsapp { background: #11b75c; border-color: #11b75c; color: #fff; }
.btn-whatsapp:hover, .btn-whatsapp:focus-visible { background: #079447; border-color: #079447; color: #fff; }
.btn-dark { background: var(--ink); border-color: var(--ink); color: #fff; box-shadow: none; }
.btn-small { min-height: 40px; padding: 8px 14px; }
.nav-cta { min-width: 188px; flex: 0 0 auto; }
.hero { padding: 76px 0; background: linear-gradient(180deg, var(--soft-2), #fff); }
.home-hero { padding: 56px 0 62px; }
.sub-hero { border-bottom: 1px solid var(--border); }
.hero-grid, .split, .form-grid { display: grid; grid-template-columns: 1.05fr .95fr; align-items: center; gap: 48px; }
.kicker { margin: 0 0 10px; color: var(--teal-dark); font-size: .78rem; line-height: 1.3; font-weight: 800; text-transform: uppercase; letter-spacing: 0; }
h1, h2, h3, p { overflow-wrap: anywhere; }
h1 { font-size: 3.75rem; line-height: 1.05; margin: 0 0 18px; letter-spacing: 0; color: var(--ink); }
.sub-hero h1 { font-size: 2.85rem; }
h2 { font-size: 2.1rem; line-height: 1.18; margin: 0 0 12px; letter-spacing: 0; color: var(--ink); }
h3 { font-size: 1.08rem; line-height: 1.3; margin: 0 0 8px; color: var(--ink); }
.lead { font-size: 1.12rem; color: var(--muted); max-width: 760px; }
.hero-actions { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 24px; }
.phi-note { color: var(--muted); font-size: .92rem; margin-top: 14px; }
.hero-image { margin: 0; border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; box-shadow: var(--shadow); background: #fff; }
.hero-image img { width: 100%; height: auto; aspect-ratio: 3 / 2; object-fit: cover; }
.section { padding: 74px 0; content-visibility: auto; contain-intrinsic-size: 780px; }
.section-soft { background: var(--soft); border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); }
.section-head { max-width: 780px; margin: 0 auto 32px; text-align: center; }
.section-head p { color: var(--muted); }
.card-grid, .directory-grid, .related-grid, .workflow-grid, .answer-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 18px; }
.answer-grid { grid-template-columns: repeat(4, minmax(0, 1fr)); }
.info-card, .directory-card, .related-grid a, .workflow-grid article, .answer-grid article, .outcome-grid article, .solution-group, .lead-form, .dashboard-visual, .metric-panel, .trust-list a { background: #fff; border: 1px solid var(--border); border-radius: var(--radius); padding: 20px; box-shadow: 0 8px 22px rgba(16, 24, 40, .04); transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease; }
.info-card p, .directory-card p, .workflow-grid p, .answer-grid p { margin: 0; color: var(--muted); }
.info-card:hover, .info-card:focus-visible, .directory-card:hover, .directory-card:focus-visible, .related-grid a:hover, .related-grid a:focus-visible, .trust-list a:hover, .trust-list a:focus-visible, .outcome-grid article:hover { border-color: rgba(15,157,143,.45); box-shadow: var(--shadow); color: var(--text); transform: translateY(-4px); }
.dashboard-visual { min-height: 360px; display: flex; flex-direction: column; gap: 18px; background: #fff; }
.dash-top { display: flex; gap: 8px; align-items: center; }
.dash-top strong { margin-left: auto; font-size: .9rem; color: var(--teal-dark); }
.dash-top span { width: 12px; height: 12px; border-radius: 50%; background: var(--border); }
.metric-strip { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
.metric-strip div { border: 1px solid var(--border); border-radius: var(--radius); padding: 12px; background: var(--soft-2); }
.metric-strip strong { display: block; font-size: .9rem; }
.metric-strip span { color: var(--muted); font-size: .82rem; }
.chart-lines { display: grid; gap: 12px; margin-top: 8px; }
.chart-lines i { display: block; height: 12px; border-radius: 999px; background: var(--teal-soft); position: relative; overflow: hidden; }
.chart-lines i:before { content: ""; display: block; height: 100%; width: 64%; background: var(--teal); border-radius: inherit; }
.chart-lines i:nth-child(2):before { width: 82%; }
.chart-lines i:nth-child(3):before { width: 48%; }
.chart-lines i:nth-child(4):before { width: 72%; }
.dashboard-table { display: grid; grid-template-columns: 1.2fr .8fr 1fr; gap: 0; border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; font-size: .86rem; }
.dashboard-table span { padding: 9px 10px; border-bottom: 1px solid var(--border); color: var(--muted); }
.dashboard-table span:nth-child(-n+3) { background: var(--soft); color: var(--ink); font-weight: 800; }
.dashboard-table span:nth-last-child(-n+3) { border-bottom: 0; }
.takeaways { margin: auto 0 0; padding-left: 20px; color: var(--muted); }
.outcome-strip { padding: 28px 0; }
.outcome-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
.outcome-grid strong { display: block; color: var(--teal-dark); }
.platform-strip { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; }
.platform-strip span { border: 1px solid var(--border); background: #fff; border-radius: 999px; padding: 7px 12px 7px 7px; color: var(--muted); font-weight: 800; display: inline-flex; align-items: center; gap: 8px; box-shadow: 0 8px 20px rgba(16,24,40,.04); }
.platform-strip b { display: inline-grid; place-items: center; min-width: 32px; height: 32px; border-radius: 50%; background: var(--teal-soft); color: var(--teal-dark); font-size: .72rem; }
.platform-strip em { font-style: normal; }
.check-list { list-style: none; padding: 0; margin: 18px 0 0; display: grid; gap: 10px; }
.check-list li { position: relative; padding-left: 26px; color: var(--muted); }
.check-list li:before { content: ""; position: absolute; left: 0; top: .45em; width: 12px; height: 12px; border-radius: 50%; background: var(--teal); }
.metric-panel { display: grid; gap: 18px; }
.metric-panel strong { display: block; margin-bottom: 8px; }
.metric-panel span { display: block; height: 10px; border-radius: 999px; background: var(--teal); }
.workflow-grid article span { display: inline-grid; place-items: center; width: 32px; height: 32px; border-radius: 50%; background: var(--teal-soft); color: var(--teal-dark); font-weight: 900; margin-bottom: 12px; }
.related-grid a span, .directory-card span { display: block; color: var(--teal-dark); font-size: .78rem; font-weight: 800; text-transform: uppercase; margin-bottom: 6px; }
.related-grid a strong, .directory-card strong { display: block; }
.faq-list { display: grid; gap: 12px; }
details { border: 1px solid var(--border); border-radius: var(--radius); padding: 16px 18px; background: #fff; }
summary { cursor: pointer; font-weight: 800; color: var(--ink); }
details p { color: var(--muted); margin-bottom: 0; }
.final-cta { background: var(--dark); color: #fff; }
.final-cta h2, .final-cta .kicker { color: #fff; }
.final-cta p { color: rgba(255,255,255,.78); }
.cta-grid { display: grid; grid-template-columns: 1fr auto; align-items: center; gap: 26px; }
.cta-actions { display: grid; gap: 12px; min-width: 220px; }
.product-band { background: #fff; }
.trust-list { display: grid; gap: 12px; }
.center { margin-top: 26px; text-align: center; }
.breadcrumbs { display: flex; align-items: center; flex-wrap: wrap; gap: 8px; color: var(--muted); font-size: .9rem; margin-bottom: 18px; }
.breadcrumbs a { color: var(--teal-dark); font-weight: 700; }
.directory-block { padding: 56px 0; border-bottom: 1px solid var(--border); }
.solutions-index { display: grid; gap: 24px; }
.solution-group h2 { font-size: 1.35rem; }
.solution-group ul { list-style: none; padding: 0; margin: 0; columns: 2; column-gap: 28px; }
.solution-group li { break-inside: avoid; display: grid; gap: 2px; padding: 9px 0; border-bottom: 1px solid var(--border); }
.solution-group a { color: var(--teal-dark); font-weight: 800; }
.solution-group span { color: var(--muted); font-size: .86rem; }
.lead-form { display: grid; gap: 14px; }
.lead-form label { display: grid; gap: 7px; color: var(--ink); font-weight: 800; }
input, select, textarea { width: 100%; border: 1px solid var(--border); border-radius: var(--radius); padding: 12px; background: #fff; color: var(--text); }
input:focus, select:focus, textarea:focus { outline: 3px solid rgba(15,157,143,.2); border-color: var(--teal); }
.honey-field { position: absolute; left: -9999px; }
.legal-copy h2 { font-size: 1.4rem; margin-top: 28px; }
.site-footer { background: var(--soft); border-top: 1px solid var(--border); padding: 52px 0 0; }
.footer-grid { width: min(1160px, calc(100% - 40px)); margin: 0 auto; display: grid; grid-template-columns: 1.25fr repeat(4, 1fr) 1.25fr; gap: 24px; align-items: start; }
.footer-brand img { max-width: 230px; height: auto; margin-bottom: 14px; }
.site-footer p, .site-footer a { color: var(--muted); }
.site-footer h2 { font-size: .95rem; margin: 0 0 10px; color: var(--ink); }
.site-footer a { display: block; margin: 7px 0; }
.footer-newsletter form { display: grid; gap: 12px; margin-top: 12px; }
.footer-newsletter label { display: grid; gap: 6px; color: var(--muted); font-weight: 700; }
.footer-newsletter input { border: 0; border-bottom: 1px solid var(--border); border-radius: 0; background: transparent; padding-left: 0; }
.social-links { display: flex; gap: 12px; margin-top: 18px; align-items: center; }
.social-links a { width: 38px; height: 38px; display: inline-grid; place-items: center; border: 1px solid var(--border); border-radius: 50%; background: #fff; margin: 0; }
.social-links svg { width: 18px; height: 18px; fill: var(--ink); }
.footer-bottom { width: min(1160px, calc(100% - 40px)); margin: 34px auto 0; padding: 18px 0; border-top: 1px solid var(--border); display: flex; justify-content: space-between; gap: 16px; color: var(--muted); }
.footer-bottom nav { display: flex; gap: 16px; flex-wrap: wrap; }
.floating-tools { position: fixed; right: 18px; bottom: 18px; z-index: 70; display: grid; gap: 10px; }
.scroll-top, .whatsapp-launch { width: 52px; height: 52px; border: 0; border-radius: 50%; display: grid; place-items: center; cursor: pointer; box-shadow: var(--shadow); font-weight: 900; }
.scroll-top { background: #fff; color: var(--teal-dark); border: 1px solid var(--border); opacity: 0; pointer-events: none; transform: translateY(8px); transition: .18s ease; }
.scroll-top.visible { opacity: 1; pointer-events: auto; transform: translateY(0); }
.whatsapp-launch { background: #11b75c; color: #fff; }
.whatsapp-launch svg { width: 26px; height: 26px; fill: currentColor; }
.whatsapp-panel { position: fixed; right: 18px; bottom: 88px; z-index: 75; width: min(360px, calc(100vw - 28px)); background: #fff; border: 1px solid var(--border); border-radius: 14px; box-shadow: 0 22px 60px rgba(16,24,40,.22); overflow: hidden; }
.whatsapp-head { display: flex; align-items: center; justify-content: space-between; background: #11b75c; color: #fff; padding: 15px 18px; }
.whatsapp-close { border: 0; background: transparent; color: #fff; font-size: 1.2rem; cursor: pointer; }
.whatsapp-form { display: grid; gap: 12px; padding: 18px; }
.whatsapp-form p { margin: 0; color: var(--muted); }
.whatsapp-form label { display: grid; gap: 6px; font-weight: 800; color: var(--ink); }
.whatsapp-direct { display: none; }
.article-grid { display: grid; grid-template-columns: 280px 1fr; gap: 32px; align-items: start; }
.article-aside { position: sticky; top: 96px; border: 1px solid var(--border); border-radius: var(--radius); padding: 20px; background: var(--soft); }
.article-body { max-width: 780px; }
.article-body section { margin-top: 30px; }
.article-body h2 { font-size: 1.55rem; }
.source-list ul { padding-left: 20px; }
.source-list a { color: var(--teal-dark); font-weight: 800; }
.article-card span { display: block; color: var(--teal-dark); font-size: .78rem; font-weight: 800; text-transform: uppercase; margin-bottom: 6px; }
:focus-visible { outline: 3px solid rgba(15,157,143,.55); outline-offset: 3px; }
@media (max-width: 1060px) {
  .nav-toggle { display: inline-flex; margin-left: auto; }
  .nav-cta { display: none; }
  .main-nav { position: fixed; inset: 74px 0 auto 0; background: #fff; border-bottom: 1px solid var(--border); box-shadow: var(--shadow); padding: 14px; display: none; max-height: calc(100vh - 74px); overflow: auto; }
  .main-nav.open { display: block; }
  .main-nav ul { display: grid; gap: 6px; }
  .nav-item { display: block; }
  .main-nav a { width: 100%; justify-content: flex-start; }
  .menu-caret { display: none; }
  .dropdown { position: static; opacity: 1; visibility: visible; transform: none; box-shadow: none; border: 0; width: 100%; padding: 0 0 6px 12px; }
  .dropdown a { border: 1px solid var(--border); margin-top: 5px; background: var(--soft-2); }
  .hero-grid, .split, .form-grid, .cta-grid { grid-template-columns: 1fr; }
  .footer-grid { grid-template-columns: repeat(3, 1fr); }
  .answer-grid, .outcome-grid { grid-template-columns: repeat(2, 1fr); }
  .article-grid { grid-template-columns: 1fr; }
  .article-aside { position: static; }
}
@media (max-width: 720px) {
  .container, .footer-grid, .footer-bottom { width: min(100% - 28px, 1160px); }
  .section, .hero, .home-hero { padding: 52px 0; }
  h1 { font-size: 2.35rem; }
  .sub-hero h1, h2 { font-size: 1.8rem; }
  .lead { font-size: 1rem; }
  .hero-actions, .cta-actions { display: grid; width: 100%; }
  .btn { width: 100%; }
  .card-grid, .directory-grid, .related-grid, .workflow-grid, .answer-grid, .outcome-grid, .metric-strip { grid-template-columns: 1fr; }
  .solution-group ul { columns: 1; }
  .footer-grid { grid-template-columns: 1fr; }
  .footer-bottom { display: grid; }
  .brand img { width: 180px; }
  .floating-tools { right: 14px; bottom: 14px; }
  .scroll-top, .whatsapp-launch { width: 48px; height: 48px; }
  .whatsapp-panel { right: 14px; bottom: 76px; }
}
@media (prefers-reduced-motion: reduce) {
  * { scroll-behavior: auto !important; transition: none !important; }
}
"""


JS = r"""
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
"""


def write(path: str, content: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8", newline="\n")


def build_sitemap() -> str:
    urls = []
    for page in pages:
        if page.noindex:
            continue
        priority = "0.90" if page.category in {"home", "hub", "product", "conversion"} else "0.72"
        change = "weekly" if page.category in {"home", "hub", "product", "conversion"} else "monthly"
        urls.append(f"  <url><loc>{page.url}</loc><lastmod>{TODAY}</lastmod><changefreq>{change}</changefreq><priority>{priority}</priority></url>")
    return "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n" + "\n".join(urls) + "\n</urlset>\n"


def build_robots() -> str:
    return f"""User-agent: *
Allow: /
Disallow: /supabase/
Disallow: /content-templates/
Disallow: /tracking-crm/
Disallow: /seo-lead-generation/
Disallow: /config.example.js
Disallow: /README.md
Disallow: /DEPLOYMENT_GUIDE.md
Disallow: /DOMAIN_GUIDE.md
Disallow: /QA_REPORT.md

Sitemap: {SITE}/sitemap.xml
"""


def build_llms() -> str:
    important = ["services", "chargepilot", "all-rcm-solutions", "medical-billing-services", "denial-management-services", "clinical-lab-billing-services", "officeally-claim-entry-automation", "free-rcm-audit", "contact"]
    lines = [
        "# Resolute MSO",
        "",
        "Resolute MSO is an AI-powered revenue cycle management, medical billing automation, and healthcare operations partner for U.S. healthcare providers.",
        "ChargePilot is Resolute MSO's billing software claim-entry and claim-submission automation product for medical billing teams and RCM operations. OfficeAlly automation is one supported use case where the workflow is confirmed.",
        "Resolute MSO helps providers reduce preventable denials, improve A/R movement, automate repetitive billing workflows, and gain revenue cycle visibility. Public website forms are for business inquiries only and must not collect PHI or patient information.",
        "",
        "## Key pages",
    ]
    for slug in important:
        p = PAGE_BY_SLUG[slug]
        lines.append(f"- {p.name}: {p.url}")
    lines.extend(["", "## Page directory"])
    for p in pages:
        if not p.noindex:
            lines.append(f"- {p.name} ({p.category}; {p.intent}): {p.url}")
    return "\n".join(lines) + "\n"


def build_keyword_map() -> str:
    groups: dict[str, list[Page]] = {}
    for p in pages:
        if p.noindex:
            continue
        groups.setdefault(p.intent, []).append(p)
    out = ["# Resolute MSO Keyword Map", "", f"Generated: {TODAY}", ""]
    for intent, group in sorted(groups.items()):
        out.append(f"## {intent}")
        for p in group:
            out.append(f"- `{p.path}` - {p.name}: {', '.join(p.keywords)}")
        out.append("")
    return "\n".join(out)


def build_internal_link_map() -> str:
    out = ["# Resolute MSO Internal Link Map", "", f"Generated: {TODAY}", ""]
    for p in pages:
        if p.noindex:
            continue
        related = [PAGE_BY_SLUG[s].path for s in related_slugs(p) if s in PAGE_BY_SLUG]
        out.append(f"- `{p.path}` links to: {', '.join(related)}")
    return "\n".join(out) + "\n"


def build_deployment_notes() -> str:
    return f"""# Deployment Notes

Generated: {TODAY}

Branch: `rebuild-seo-authority`
Production branch: `main` remains untouched until owner approval.

## Preview

After this branch is pushed, preview through one of these safe options:

1. GitHub branch file preview:
   `https://github.com/ai-sohaib/resolute-mso/tree/rebuild-seo-authority`
2. GitHub Pages branch preview instruction:
   In repository Settings -> Pages, temporarily choose branch `rebuild-seo-authority` and `/root` only if you want GitHub Pages to serve the preview. Do not change the production custom domain until approved.
3. Local preview:
   Run `python -m http.server 8080` from the repository root and open `http://localhost:8080/`.

## Deployment after approval

1. Review the branch output and validation report.
2. Merge `rebuild-seo-authority` into `main`.
3. Confirm GitHub Pages still points to `main` and `/root`.
4. Verify live pages:
   `/`, `/services.html`, `/chargepilot.html`, `/all-rcm-solutions.html`, `/medical-billing-services.html`, `/denial-management-services.html`, `/clinical-lab-billing-services.html`, `/officeally-claim-entry-automation.html`, `/contact.html`.

## Rollback

If deployment is approved and later needs rollback, revert the merge commit on `main` or switch Pages back to the previous known-good commit.
"""


def build_before_after() -> str:
    return f"""# Before / After Summary

Generated: {TODAY}

## Before

- Static HTML pages existed, but header/footer and URL behavior were partly patched at runtime through `config.js` and cleanup scripts.
- The root homepage redirected to `/home.html`.
- Several titles and content blocks were generic.
- CSS was spread across multiple patch files.

## After

- `index.html` is the canonical homepage.
- `home.html` redirects to `/`.
- Pages are generated from one source template with consistent meta, canonical, OG, Twitter, schema, breadcrumbs, FAQ, CTA, related links, and PHI notice.
- Sitemap, robots, llms.txt, keyword map, internal link map, 404 page, and deployment notes are generated together.
- Runtime footer/header patching is removed from generated pages.
"""


def build_manifest() -> str:
    return json.dumps(
        {
            "name": "Resolute MSO",
            "short_name": "Resolute MSO",
            "start_url": "/",
            "display": "standalone",
            "background_color": "#ffffff",
            "theme_color": "#0F9D8F",
            "icons": [
                {"src": "/assets/img/favicon-32.png", "sizes": "32x32", "type": "image/png"},
                {"src": "/assets/img/favicon.png", "sizes": "512x512", "type": "image/png"},
            ],
        },
        indent=2,
    ) + "\n"


def build_data_exports() -> None:
    data = [
        {
            "slug": p.slug,
            "name": p.name,
            "category": p.category,
            "intent": p.intent,
            "url": p.url,
            "keywords": p.keywords,
            "title": meta_title(p),
            "description": meta_description(p),
        }
        for p in pages
        if not p.noindex
    ]
    write("data/pages.json", json.dumps(data, indent=2))
    keyword_data = {}
    for p in data:
        keyword_data.setdefault(p["intent"], []).append({"url": p["url"], "page": p["name"], "keywords": p["keywords"]})
    write("data/keywords.json", json.dumps(keyword_data, indent=2))


def main() -> None:
    write("assets/css/resolute-authority.css", CSS.strip() + "\n")
    write("assets/js/resolute-authority.js", JS.strip() + "\n")
    for page in pages:
        write(page.file, render_page(page))
        if page.slug != "index":
            target = "/" if page.slug == "home" else page.path
            write(page.legacy_file, render_redirect(Page(page.slug, f"{page.name} Redirect", "utility", "Redirect", [], noindex=True), target))
    write("404.html", render_404())
    write("thank-you.html", render_thanks())
    write("sitemap.xml", build_sitemap())
    write("robots.txt", build_robots())
    write("llms.txt", build_llms())
    write("KEYWORD_MAP.md", build_keyword_map())
    write("INTERNAL_LINK_MAP.md", build_internal_link_map())
    write("DEPLOYMENT_NOTES.md", build_deployment_notes())
    write("BEFORE_AFTER_SUMMARY.md", build_before_after())
    write("site.webmanifest", build_manifest())
    build_data_exports()
    print(f"Generated {len([p for p in pages if not p.noindex])} indexable pages plus utility pages.")


if __name__ == "__main__":
    main()
