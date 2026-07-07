# Resolute MSO Website

Static GitHub Pages website for Resolute MSO, covering U.S. healthcare revenue cycle management, medical billing, healthcare automation, ChargePilot™, analytics, staffing, administrative support, and custom healthcare technology.

## Review branch

Active enterprise upgrade branch:

```text
audit/enterprise-website-upgrade
```

Production branch:

```text
main
```

Do not merge, change GitHub Pages settings, or deploy production until the draft pull request is approved and the deployment gates are complete.

## Enterprise build

Use the controlled wrapper so the generator updates the full static site without overwriting the approved enterprise homepage:

```bash
python scripts/build_enterprise_site.py
python scripts/validate_site.py
python -m unittest discover -s tests -p "test_*.py" -v
```

The wrapper:

1. Preserves the reviewed root `index.html`.
2. Runs `scripts/build_site.py` for generated routes and supporting files.
3. Restores the reviewed homepage.
4. Runs `scripts/apply_enterprise_upgrade.py` to inject shared assets and remove insecure public form actions.

Do not run `scripts/build_site.py` as the final production step by itself because it regenerates the legacy homepage template.

## Local preview

```bash
python -m http.server 8080
```

Open:

```text
http://127.0.0.1:8080/
```

## Primary enterprise assets

- `index.html` — approved enterprise homepage and canonical homepage source.
- `assets/css/enterprise-upgrade.css` — design tokens, conversion, accessibility, modal, and responsive styles.
- `assets/js/enterprise-upgrade.js` — Free Audit modal, direct WhatsApp behavior, and inline form states.
- `config.js` — public, non-secret WhatsApp and form-endpoint configuration.
- `scripts/build_enterprise_site.py` — controlled build entry point.
- `scripts/apply_enterprise_upgrade.py` — generated-HTML hardening step.
- `workers/lead-intake/` — secure serverless lead-intake reference implementation.
- `tests/test_enterprise_upgrade.py` — enterprise regression tests.
- `.github/workflows/enterprise-website-qa.yml` — PR validation, generated preview, and before/after screenshots.

## Audit and delivery documentation

- `docs/ENTERPRISE_WEBSITE_AUDIT.md`
- `docs/RECOMMENDED_INFORMATION_ARCHITECTURE.md`
- `docs/ENTERPRISE_UPGRADE_CHANGELOG.md`
- `docs/DEPLOYMENT_AND_ROLLBACK.md`

## Form delivery

The browser must send business inquiries only to the approved secure serverless endpoint configured through:

```js
window.RESOLUTE_CONFIG.formEndpoint = "https://forms.resolutemso.com/api/lead";
```

Keep API keys, SMTP credentials, and provider tokens in encrypted Worker secrets. Never place them in `config.js`, HTML, or browser JavaScript.

## Safety and compliance notes

- Public forms are business-only and must not collect PHI, patient information, claim data, or medical records.
- The marketing website should use accurate language such as “HIPAA-conscious”; it should not claim the public site is automatically HIPAA compliant.
- WhatsApp actions use one centralized direct-link implementation.
- Performance, pricing, supported-system, and outcome statements require business-owner verification before publication.
- Production deployment is intentionally outside the pull request and requires final approval.
