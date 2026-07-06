# Resolute MSO GitHub Pages SSL / Root Domain Fix

This website package already includes a root-level `CNAME` file with:

```txt
www.resolutemso.com
```

Code files cannot issue the GitHub Pages TLS certificate. GitHub provisions it only after DNS and repository settings are correct.

## GitHub Pages settings

Repository → Settings → Pages → Custom domain:

```txt
www.resolutemso.com
```

Then save and wait for certificate provisioning. Enable **Enforce HTTPS** after the certificate becomes available.

## DNS records

Use these exact records and remove conflicting records:

```txt
A       @       185.199.108.153
A       @       185.199.109.153
A       @       185.199.110.153
A       @       185.199.111.153
CNAME   www     ai-sohaib.github.io
```

Remove extra apex A/AAAA/CNAME/redirect/wildcard records that do not belong to GitHub Pages.

If CAA records exist, make sure Let’s Encrypt is allowed:

```txt
0 issue "letsencrypt.org"
```

If stuck, remove the custom domain in GitHub Pages, save, wait 2–3 minutes, add `www.resolutemso.com` again, and wait for provisioning.
