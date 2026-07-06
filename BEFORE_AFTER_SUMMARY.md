# Before / After Summary

Generated: 2026-07-02

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
