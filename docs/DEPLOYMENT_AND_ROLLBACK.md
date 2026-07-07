# Deployment, Verification, and Rollback

## Production rule

Do not deploy or merge this branch until the pull request is approved and every required environment value is configured. This branch does not change production by itself.

## Pre-deployment gates

1. Pull-request QA workflow passes.
2. Generated preview artifact is reviewed at 320, 375, 430, 768, 1024, 1366, 1440, and 1920 pixels.
3. Chrome, Edge, Firefox, and Safari spot checks are completed.
4. Keyboard-only navigation and modal behavior pass.
5. Synthetic non-PHI form delivery succeeds.
6. `support@resolutemso.com` receives the internal email.
7. Error and rate-limit states are tested.
8. Official WhatsApp-enabled number and prefilled message are approved.
9. ChargePilot and performance claims are approved by a business owner.
10. Legacy redirect mapping is approved.
11. Privacy copy reflects the actual deployed form processor and retention policy.
12. Production backup/ref is recorded.

## Secure lead-intake deployment

Deploy `workers/lead-intake` to a controlled endpoint such as:

```text
https://forms.resolutemso.com/api/lead
```

Configure:

```text
ALLOWED_ORIGINS=https://www.resolutemso.com,https://resolutemso.com
LEAD_TO_EMAIL=support@resolutemso.com
SEND_CONFIRMATION=false
```

Store as encrypted secrets:

```text
RESEND_API_KEY
LEAD_FROM_EMAIL
```

Bind:

```text
FORM_RATE_LIMITER
```

After deployment, set the public endpoint in `config.js`:

```js
window.RESOLUTE_CONFIG.formEndpoint = "https://forms.resolutemso.com/api/lead";
```

Do not place email credentials or provider API keys in `config.js` or any browser-delivered file.

## Build and validate

```bash
python scripts/build_site.py
python scripts/apply_enterprise_upgrade.py
python scripts/validate_site.py
python -m unittest discover -s tests -p "test_*.py" -v
node --check assets/js/source-cleanup.js
node --check assets/js/enterprise-upgrade.js
node --check workers/lead-intake/src/index.js
```

## Preview

```bash
python -m http.server 8080
```

Review the homepage and representative pages from every template group. The generated preview—not only the manually edited source homepage—must be approved.

## Critical production verification

1. Homepage title and H1 are exactly identical.
2. Hero CTAs appear in one row on wide desktop and stack cleanly on mobile.
3. Request a Free Audit opens the modal without changing the URL.
4. Modal focus enters the dialog, remains trapped, closes with Escape, and returns to the trigger.
5. Required fields, service selection, and consent validate accessibly.
6. Successful submission shows the exact confirmation message inline.
7. Failed submission retains values.
8. Floating and inline WhatsApp actions open the same direct `wa.me` URL in a safe new tab.
9. No WhatsApp form or panel opens.
10. Header, footer, dropdowns, service links, sitemap, robots, canonical tags, and 404 behavior remain functional.
11. Browser console and network panel contain no uncaught errors or exposed secrets.
12. Test synthetic data only—never patient or claim data.

## Security headers

Configure at the edge where supported:

- Strict-Transport-Security
- Content-Security-Policy
- X-Content-Type-Options
- Referrer-Policy
- Permissions-Policy
- frame-ancestors through CSP

Start CSP in report-only mode when legacy third-party scripts are still present, then enforce after violations are resolved.

## DNS and email

- Preserve the current approved domain records during website deployment.
- Configure SPF and DKIM for the sending provider.
- Publish an appropriate DMARC policy.
- Use a dedicated verified sender such as `website@resolutemso.com` or `notifications@resolutemso.com`.
- Continue delivering business inquiries to `support@resolutemso.com`.

## Deployment sequence

1. Tag or record the current production commit.
2. Merge the approved pull request into `main`.
3. Build and validate from the merged commit.
4. Deploy the Worker and verify the endpoint.
5. Configure the frontend endpoint.
6. Deploy the static site through the approved GitHub Pages workflow.
7. Run the critical production verification list.
8. Monitor forms, 404s, console errors, and search coverage.

## Rollback

### Static website rollback

1. Identify the recorded pre-deployment production commit.
2. Revert the merge commit or reset the deployment source to the recorded commit through an approved pull request.
3. Rebuild and redeploy.
4. Verify homepage, navigation, contact, and WhatsApp behavior.

Do not force-push `main` unless repository governance explicitly authorizes it.

### Form endpoint rollback

1. Set `window.RESOLUTE_CONFIG.formEndpoint` to an empty string to disable submissions safely.
2. Redeploy the static configuration.
3. Keep visible email and direct WhatsApp alternatives available.
4. Roll back the Worker deployment to its previous version in Cloudflare.
5. Rotate the email-provider key if exposure is suspected.

### Emergency containment

If a form unexpectedly collects PHI or exposes credentials:

1. Disable the endpoint immediately.
2. Preserve only the minimum incident evidence.
3. Do not copy sensitive submissions into tickets or chat.
4. Rotate affected credentials.
5. Follow Resolute MSO’s incident-response and legal/compliance process.
