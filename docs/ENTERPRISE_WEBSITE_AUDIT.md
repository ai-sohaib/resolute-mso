# Resolute MSO Enterprise Website Audit

**Audit date:** July 7, 2026  
**Repository:** `ai-sohaib/resolute-mso`  
**Live domain:** `https://www.resolutemso.com/`  
**Implementation branch:** `audit/enterprise-website-upgrade`

## Executive summary

Resolute MSO has a strong service footprint across U.S. healthcare RCM, medical billing, automation, analytics, staffing, and ChargePilot™. The main risk is a split implementation: production serves an older `.html`-route build with runtime patches, while `main` contains a newer generated directory-route build. This creates inconsistent titles, navigation, forms, WhatsApp behavior, and conversion experiences.

The most urgent problems were insecure or unreliable public-form handling, the floating WhatsApp control opening an intermediate form, inconsistent homepage positioning, runtime DOM rewriting, route/canonical inconsistency, and public percentage/multiplier visuals that can look like verified performance claims. The upgrade branch introduces a clean homepage, centralized WhatsApp behavior, an accessible Free Audit modal, a secure serverless lead-intake reference implementation, shared design tokens, automated checks, and deployment controls. Production has not been changed.

## Current strengths

- Clear U.S. healthcare RCM and medical-billing specialization.
- Broad coverage of core services, specialties, automation, analytics, and buyer-intent topics.
- Existing canonical tags, Open Graph metadata, Twitter cards, JSON-LD, sitemap, robots, and redirect pages.
- Existing PHI warnings on several public conversion paths.
- Static delivery with a small dependency surface.
- Python generator and validator provide a foundation for repeatable QA.
- ChargePilot™ offers a differentiated automation story.

## Severity summary

| Severity | Main themes |
|---|---|
| Critical | Public form security, production/source split, WhatsApp flow, unsupported outcome claims |
| High | Homepage message, route consistency, accessibility, repetitive content, runtime rewrites |
| Medium | Navigation depth, design tokens, metadata consistency, analytics, performance |
| Low | Editorial polish, labels, visual refinement, documentation hygiene |

## Critical findings

### C-01 — Public form delivery is not owned server-side

Existing source uses `mailto:` and client-side FormSubmit endpoints. This prevents Resolute MSO from controlling server validation, rate limiting, origin restrictions, provider credentials, and safe logging. Deploy the included Worker, keep credentials in encrypted secrets, and route every public business form through one approved endpoint.

### C-02 — Production and `main` are not the same build

Production exposes older `.html` routes and runtime-rewritten content, while `main` contains generated pretty-directory routes. Confirm the GitHub Pages source and adopt one pipeline: build, apply enterprise post-processing, validate, preview, approve, then deploy.

### C-03 — Floating WhatsApp adds conversion friction

The live floating control opens a website panel and requests contact information before opening WhatsApp. It must instead use the centralized direct `wa.me` link, safe new-tab attributes, the official green, and no modal interception.

### C-04 — Illustrative metrics can be read as verified outcomes

Percentage, multiplier, and “up to” visuals are displayed near conversion content. Remove them unless each metric has an approved evidence source, sample, period, methodology, and client permission. Do not present visual-demo data as a business result.

## High findings

- **H-01 Homepage H1/title mismatch:** live and generated versions use different positioning. The exact approved H1 and title must be `AI-Driven Medical Billing & RCM That Stops Revenue Leakage`.
- **H-02 CTA hierarchy:** hero actions previously mixed demo, automation, audit, and WhatsApp intent. Use Book a Demo, Request a Free Audit, then Talk on WhatsApp.
- **H-03 Free Audit route friction:** open an on-page accessible modal, not a separate form page.
- **H-04 Runtime patch architecture:** multiple dynamically injected CSS/JS layers rewrite titles, navigation, URLs, and footers after load, causing drift and layout changes.
- **H-05 Route inconsistency:** canonical/sitemap directory URLs coexist with live `.html` navigation. Use one route format and permanent redirects.
- **H-06 Repetitive generated content:** many pages share generic sentence patterns and FAQs. Human-edit high-commercial-intent pages and consolidate thin overlaps.
- **H-07 Form accessibility:** existing forms lack consistent field-linked errors, loading states, duplicate-submit prevention, and live-region confirmation.
- **H-08 Modal accessibility:** existing overlays require verified focus trapping, Escape close, focus restoration, and background scroll control.
- **H-09 Fragmented design tokens:** colors, spacing, shadows, radii, and button states are spread across inline and patch CSS.
- **H-10 ChargePilot claim governance:** supported software, workflow scope, throughput, pricing, agent count, and integration language need a last-verified owner and evidence source.
- **H-11 No documented approval gate:** static validation alone does not prove browser, accessibility, responsive, form-delivery, or Core Web Vitals behavior.

## Medium findings

- Navigation reflects internal service inventory more than buyer tasks.
- Case studies and testimonials lack an evidence-governance structure.
- Resource pages need visible authors, reviewers, and reviewed dates.
- Breadcrumb schema and visible hierarchy require consistency checks.
- Image alt text should describe page-specific purpose.
- Repeated inline CSS reduces cache reuse and increases HTML weight.
- Heavy 3D/reveal effects can weaken enterprise healthcare trust.
- Reduced-motion coverage is incomplete on legacy styles.
- Mobile menus and dropdowns need full keyboard and touch testing.
- Newsletter consent, frequency, delivery, and privacy purpose are unclear.
- Campaign attribution and analytics governance are not documented.
- 404 status codes and legacy redirects need production verification.
- Contact, demo, audit, and service forms should share one backend schema.
- Hosting-level security headers need Cloudflare or another controllable edge layer.

## Page and template findings

### Homepage — Critical/High

**Strengths:** broad service positioning, visible CTAs, automation differentiation.  
**Issues:** wrong required H1/title, mixed CTA hierarchy, illustrative metrics, WhatsApp form interception, runtime title rewriting, generic proof.  
**Action:** rebuilt with the exact title/H1, four buyer-oriented capability categories, accountable ChargePilot positioning, trust messaging, and accessible conversions.

### Services hub — High

**Strengths:** extensive capability coverage.  
**Issues:** internal-list orientation, repetitive labels, weak prioritization by buyer outcome.  
**Action:** organize around Revenue Cycle Management, Healthcare Automation, Healthcare Technology, and Staffing & Operations.

### Individual RCM service pages — High/Medium

**Strengths:** strong topical and search coverage.  
**Issues:** repetitive copy, insufficient workflow depth, limited evidence, similar FAQs.  
**Action:** prioritize medical billing, end-to-end RCM, denials, AR, eligibility, payment posting, credentialing, and analytics for human editorial improvement.

### Automation Suite — High

**Strengths:** differentiated service category.  
**Issues:** product versus custom-service boundaries are unclear; automation claims need exception and prerequisite language.  
**Action:** separate productized tools from custom RPA/AI development and describe human review.

### ChargePilot™ — Critical/High

**Strengths:** memorable product tied to a clear operational problem.  
**Issues:** release status, supported systems, throughput, pricing, integrations, and agent-count claims need verification.  
**Action:** add a capability matrix, supported-workflow statement, security architecture, implementation process, demo flow, and evidence-backed case study.

### Specialty pages — High/Medium

**Strengths:** useful audience segmentation.  
**Issues:** template repetition and insufficient specialty-specific payer, authorization, coding, and denial nuance.  
**Action:** prioritize laboratories, imaging/radiology, urgent care, mental health, DME, and physician groups.

### Buyer-intent/comparison pages — Medium/High

Add transparent decision criteria, assumptions, evidence citations, and stronger links to relevant services. Avoid pages whose only purpose is a keyword variation.

### Resources/blog — Medium

Add author/reviewer profiles, reviewed dates, source policy, complete article schema, topic clusters, and maintenance ownership.

### Contact, Demo, Audit, and service inquiries — Critical

Use one secure server-side handler, no PHI fields, inline loading/error/success states, value preservation on failure, and no unexpected redirects.

### Compliance, Quality, and Privacy — High

Do not state that the marketing site is automatically HIPAA compliant. After the form backend is deployed, disclose the real processor, purpose, retention, security controls, and contact process.

### Footer — High

Remove insecure newsletter behavior until consent and delivery are fully configured. Use stable hub links, consistent route format, and no runtime footer replacement.

### 404 and legacy routes — Medium

Verify real HTTP status codes, preserve a redirect inventory, and test `.html` to directory-route behavior in production.

## Accessibility target: WCAG 2.1 AA practices

Implemented or specified: skip link, semantic regions, visible focus, 44–48px controls, modal focus entry/trap, Escape close, focus restoration, scroll lock, explicit labels, inline live-region status, keyboard controls, reduced-motion treatment, and mobile stacking.

Still required on a deployed preview: axe scan, VoiceOver/NVDA spot checks, Safari keyboard testing, 200% zoom/reflow, and contrast/error-link verification across legacy pages.

## Performance

Primary risks are repeated inline CSS, dynamically injected styles, runtime DOM rewriting, heavy reveal/3D effects, and post-load layout changes. Extract shared assets, remove obsolete patches after visual regression testing, add explicit image dimensions, defer noncritical scripts, and measure LCP, CLS, INP, and TTFB on a preview. No Lighthouse score is reported because no instrumented deployed preview was available; scores must not be invented.

## Security

- Never collect PHI through public forms.
- Keep provider credentials in Worker secrets.
- Use origin allow-listing, body-size limits, validation, sanitization, rate limiting, spam checks, and no-store responses.
- Do not log form bodies.
- Configure SPF, DKIM, and DMARC for the sending domain.
- Define lead retention and deletion rules.
- Review analytics/pixels before enabling them on healthcare pages.
- Add HSTS, CSP, frame restrictions, referrer policy, permissions policy, and MIME protection at the edge where supported.

## Repository and branches

- Static GitHub Pages site.
- Python generator: `scripts/build_site.py`.
- Validator: `scripts/validate_site.py`.
- No root npm application framework/package manifest.
- Generated directory routes and legacy `.html` routes coexist.
- `config.js` and cleanup scripts provide runtime patching.
- `main` is the resolvable default/production-intended branch.
- README references a rebuild branch that was not resolvable during this audit and should be treated as stale until confirmed.
- Dedicated branch created: `audit/enterprise-website-upgrade`.
- Production was not overwritten or deployed.

## Approval decision

The branch is suitable for review as a high-priority stabilization and conversion upgrade. It is not ready for production until the secure form endpoint is configured, the generated preview is visually tested, legacy redirects are confirmed, and product/outcome claims receive business-owner approval.
