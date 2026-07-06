# Deployment Notes

Generated: 2026-07-02

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
