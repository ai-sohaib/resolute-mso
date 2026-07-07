# Resolute MSO Website

Static GitHub Pages website for Resolute MSO, an AI-powered revenue cycle management, medical billing automation, healthcare operations, and ChargePilot OfficeAlly automation partner for U.S. healthcare providers.

## Preview Branch

Active rebuild branch:

```txt
rebuild-seo-authority
```

Do not merge to `main` or change production GitHub Pages settings until the preview is approved.

## Build

The site is generated from a lightweight Python build script:

```powershell
python scripts/build_site.py
python scripts/validate_site.py
```

Generated source-of-truth deliverables include:

- `data/pages.json`
- `data/keywords.json`
- `KEYWORD_MAP.md`
- `INTERNAL_LINK_MAP.md`
- `DEPLOYMENT_NOTES.md`
- `BEFORE_AFTER_SUMMARY.md`
- `PREVIEW_QA_REPORT.md`

Primary runtime assets:

- `assets/css/resolute-authority.css`
- `assets/js/resolute-authority.js`
- `assets/img/resolute-rcm-dashboard-hero.png`

## Local Preview

```powershell
python -m http.server 8080
```

Open:

```txt
http://127.0.0.1:8080/
```

## Safety Notes

- Public forms are business-only and must not collect PHI or patient information.
- `main` is the production branch.
- `rebuild-seo-authority` is the preview branch.
- The static site does not use runtime header/footer patching.
- ChargePilot pricing is scoped after workflow assessment rather than presented as a guaranteed fixed result.
