# Enterprise Website Upgrade Change Log

## Branch

`audit/enterprise-website-upgrade`

## Files changed

### Homepage and public configuration

- `index.html`
  - Rebuilt homepage around four buyer-oriented capability categories.
  - Set the exact homepage title and H1.
  - Added the required three-CTA order.
  - Added direct WhatsApp actions, ChargePilot positioning, trust content, and PHI warnings.
- `config.js`
  - Centralized the WhatsApp number and message.
  - Removed the hard-coded third-party form endpoint.
  - Added the secure form-endpoint configuration slot.
  - Isolates the enterprise homepage from conflicting legacy theme patches.
- `assets/js/source-cleanup.js`
  - Removed runtime title and footer rewrites.
  - Retained only limited legacy path and go-to-top compatibility behavior.
- `README.md`
  - Replaced the stale preview-branch instructions.
  - Documented the tested enterprise build, validation, form-security, and deployment workflow.

### Components and interaction

- `assets/css/enterprise-upgrade.css`
  - Added shared design tokens for brand, state colors, spacing, typography, radii, shadows, container width, and button height.
  - Added desktop/tablet/mobile hero CTA behavior.
  - Added gold audit CTA and official WhatsApp styling.
  - Added accessible modal, form, focus, reduced-motion, navigation, footer, and responsive styles.
- `assets/js/enterprise-upgrade.js`
  - Added the accessible Free Audit modal.
  - Added focus entry, focus trapping, Escape close, scroll lock, and focus restoration.
  - Added required form fields, PHI warning, consent, validation, loading, inline error, and inline success behavior.
  - Added direct centralized WhatsApp URLs and safe new-tab attributes.
  - Prevents legacy `mailto:` and FormSubmit forms from redirecting unexpectedly.
- `assets/js/whatsapp-normalize.js`
  - Added a cross-site safeguard for legacy WhatsApp-labeled anchors and buttons.
  - Converts them to the same centralized direct `wa.me` URL with official styling, icon, accessible label, and safe new-tab attributes.

### Build and backend

- `scripts/build_enterprise_site.py`
  - Added the controlled production build entry point.
  - Runs the existing route generator while preserving the approved enterprise homepage.
  - Applies the shared generated-HTML hardening step.
- `scripts/apply_enterprise_upgrade.py`
  - Added an idempotent post-build step for generated HTML.
  - Injects enterprise assets, removes insecure public form actions, and enforces homepage metadata requirements where needed.
- `workers/lead-intake/src/index.js`
  - Added a serverless lead-intake reference implementation.
  - Includes origin validation, input normalization, required-field checks, email validation, rate limiting, spam checks, PHI-pattern rejection, safe logging, email delivery, and optional prospect confirmation.
- `workers/lead-intake/wrangler.toml.example`
  - Added non-secret Cloudflare Worker and rate-limit configuration.
- `workers/lead-intake/README.md`
  - Added secure deployment and environment setup instructions.

### Tests, CI, and evidence

- `tests/test_enterprise_upgrade.py`
  - Added regression tests for exact title/H1, meta description, CTA order, modal fields/accessibility, centralized WhatsApp, frontend secret absence, Worker controls, and postprocessor idempotence.
- `.github/workflows/enterprise-website-qa.yml`
  - Added controlled enterprise generation, repository validation, Python tests, JavaScript syntax checks, secret scanning, generated-home acceptance checks, browser setup, visual evidence, and preview artifact upload.
- `scripts/capture_before_after.py`
  - Added reproducible desktop and mobile screenshots of the live homepage and generated branch preview.

### Audit and architecture

- `docs/ENTERPRISE_WEBSITE_AUDIT.md`
  - Added the complete severity-classified website and repository audit.
- `docs/RECOMMENDED_INFORMATION_ARCHITECTURE.md`
  - Added the proposed sitemap, navigation, hierarchy, CTA strategy, internal-link strategy, content gaps, and migration approach.
- `docs/ENTERPRISE_UPGRADE_CHANGELOG.md`
  - Added this implementation inventory.
- `docs/DEPLOYMENT_AND_ROLLBACK.md`
  - Added deployment gates, environment variables, verification, and rollback instructions.

## Components added

- Enterprise homepage shell and sections.
- Centralized WhatsApp link hydrator.
- Cross-site WhatsApp normalization safeguard.
- Accessible Free Audit modal.
- Shared inline form handler.
- Enterprise design-token layer.
- Secure lead-intake Worker.
- Controlled enterprise build wrapper.
- Post-build upgrade processor.
- Enterprise regression test suite.
- Pull-request QA workflow.
- Desktop and mobile before/after screenshot capture.

## Components removed or bypassed

- Homepage `View Automation Suite` lead-generation CTA.
- Floating WhatsApp pre-chat website form behavior.
- Runtime homepage-title rewriting in the legacy cleanup script.
- Runtime footer replacement in the legacy cleanup script.
- Client-side FormSubmit endpoint configuration.
- `mailto:` submission as an accepted form-delivery path.
- Legacy theme-patch loading on the rebuilt enterprise homepage.

## Routes changed

- No production route was deployed or deleted.
- The rebuilt homepage uses preferred directory routes.
- The audit recommends permanently redirecting legacy `.html` URLs to the matching directory URLs only after preview testing and redirect-map approval.

## Metadata changed

Homepage title, H1, Open Graph title, and Twitter title use:

`AI-Driven Medical Billing & RCM That Stops Revenue Leakage`

Homepage meta description:

`Resolute MSO helps U.S. healthcare providers improve medical billing and RCM, reduce denials, recover AR, and use automation to strengthen revenue workflows.`

## Form behavior changed

- Free Audit opens on the current page.
- No route change or page reload is required.
- Validation and errors appear in context.
- Submit buttons expose a loading state and prevent duplicate submissions.
- Failed submissions preserve entered values.
- Success appears below the submit area.
- Public forms contain PHI warnings and do not request patient information.
- Secure email delivery requires the serverless endpoint described below.

## Tests added

- Exact homepage title/H1 equality.
- Meta-description length and required-topic coverage.
- CTA ordering.
- Modal field and accessibility controls.
- WhatsApp centralization, official green, safe new tab, and no homepage popup panel.
- Cross-site normalization of legacy WhatsApp-labeled controls.
- Absence of third-party client-side form endpoints and obvious plaintext credential assignments.
- Worker security controls.
- Postprocessor idempotence.
- JavaScript syntax checks.
- Existing repository validation.
- Generated-homepage structure checks.
- Automated desktop/mobile screenshot capture.

## Required environment configuration

### Frontend

- `window.RESOLUTE_CONFIG.whatsappNumber`
- `window.RESOLUTE_CONFIG.whatsappMessage`
- `window.RESOLUTE_CONFIG.formEndpoint`

### Lead-intake Worker

- `ALLOWED_ORIGINS`
- `LEAD_TO_EMAIL`
- `SEND_CONFIRMATION`
- `RESEND_API_KEY` — encrypted secret
- `LEAD_FROM_EMAIL` — encrypted secret
- `FORM_RATE_LIMITER` — Cloudflare rate-limit binding

No API key, SMTP password, email token, or private credential is committed.
