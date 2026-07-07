# Secure Lead Intake Worker

This Cloudflare Worker provides the server-side endpoint required by Resolute MSO public business forms.

## Controls

- Origin allow-list
- JSON body-size limit
- Server-side required-field and email validation
- Input normalization and HTML escaping
- Cloudflare Rate Limiting binding
- Honeypot and minimum-completion-time checks
- PHI-pattern rejection for free-text fields
- No submitted form content written to logs
- Email credentials stored only as Worker secrets
- CORS and restrictive API response headers

## Deploy

1. Copy `wrangler.toml.example` to `wrangler.toml`.
2. Replace the rate-limit `namespace_id` with a unique positive integer string for the Cloudflare account.
3. Verify a sender domain with the selected email provider.
4. Add encrypted secrets:

```bash
npx wrangler secret put RESEND_API_KEY
npx wrangler secret put LEAD_FROM_EMAIL
```

5. Deploy:

```bash
npx wrangler deploy
```

6. Route the Worker to an approved endpoint such as `https://forms.resolutemso.com/api/lead`.
7. Set `window.RESOLUTE_CONFIG.formEndpoint` in `/config.js` to that endpoint.
8. Submit a synthetic, non-PHI inquiry and confirm secure delivery to `support@resolutemso.com`.

The repository intentionally contains no API key, SMTP password, or provider token.
