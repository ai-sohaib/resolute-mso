# Domain, DNS, SSL, and Security Guide

Custom domain: `www.resolutemso.com`
Repository: `ai-sohaib/resolute-mso`
Hosting: GitHub Pages

## DNS Records

The DNS you provided is correct for GitHub Pages:

```txt
A       @       185.199.108.153
A       @       185.199.109.153
A       @       185.199.110.153
A       @       185.199.111.153
CNAME   www     ai-sohaib.github.io
```

Keep the included root-level `CNAME` file:

```txt
www.resolutemso.com
```

## GitHub Pages Settings

1. Upload all files to the repository root.
2. Go to repository Settings → Pages.
3. Set source to `main / root`.
4. Add custom domain: `www.resolutemso.com`.
5. Wait for GitHub DNS check.
6. Enable `Enforce HTTPS`.

## SSL / HTTPS

GitHub Pages provides HTTPS certificates for custom domains after DNS is valid. If HTTPS is not immediately available, wait for GitHub Pages DNS/certificate provisioning and then enable `Enforce HTTPS`.

## Security Notes

- This is a public marketing website, not a patient portal.
- Do not collect PHI on public forms.
- Do not commit private API keys, service-role keys, passwords, or GitHub tokens.
- This package removes the public `/admin/` editor to avoid exposing an editing interface on the live website.
- Make website changes through GitHub commits, pull requests, or a private CMS/admin layer protected by Cloudflare Access, WordPress, Webflow, or a custom authenticated backend.

## Recommended Optional Hardening

If using Cloudflare in front of GitHub Pages, enable:

- Always Use HTTPS
- Automatic HTTPS Rewrites
- HSTS after confirming HTTPS stability
- Security headers through Cloudflare Transform Rules
- Bot fight / rate limiting for forms

## Search Engine Setup

After deployment:

1. Verify `https://www.resolutemso.com/` in Google Search Console.
2. Verify `https://www.resolutemso.com/` in Bing Webmaster Tools.
3. Submit `https://www.resolutemso.com/sitemap.xml`.
4. Request indexing for the homepage, services, specialties, automation suite, ChargePilot, and blog pages.
