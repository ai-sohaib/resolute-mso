from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
ROBOTS = ROOT / "robots.txt"
LLMS = ROOT / "llms.txt"

AGENT_LINK = '  <link rel="alternate" type="text/plain" href="/llms.txt" title="LLM-readable Resolute MSO site guide">\n'
AGENT_SCRIPT = '  <script src="/assets/js/agentic-readiness.js" defer></script>\n'

SCHEMA = {
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "Organization",
            "@id": "https://www.resolutemso.com/#organization",
            "name": "Resolute MSO",
            "url": "https://www.resolutemso.com/",
            "email": "support@resolutemso.com",
            "telephone": "+1-701-552-5527",
            "description": "Revenue cycle management, medical billing, healthcare workflow automation, and operational support for U.S. healthcare providers.",
            "contactPoint": {
                "@type": "ContactPoint",
                "contactType": "sales and business inquiries",
                "telephone": "+1-701-552-5527",
                "email": "support@resolutemso.com",
                "availableLanguage": ["English"],
            },
        },
        {
            "@type": "WebSite",
            "@id": "https://www.resolutemso.com/#website",
            "url": "https://www.resolutemso.com/",
            "name": "Resolute MSO",
            "publisher": {"@id": "https://www.resolutemso.com/#organization"},
            "inLanguage": "en-US",
        },
        {
            "@type": "Service",
            "@id": "https://www.resolutemso.com/#rcm-service",
            "name": "Revenue Cycle Management and Medical Billing Services",
            "provider": {"@id": "https://www.resolutemso.com/#organization"},
            "areaServed": {"@type": "Country", "name": "United States"},
            "serviceType": [
                "Revenue Cycle Management",
                "Medical Billing",
                "Denial Management",
                "Accounts Receivable Follow-Up",
                "Provider Enrollment",
                "Healthcare Workflow Automation",
            ],
            "url": "https://www.resolutemso.com/services/",
        },
    ],
}


def update_robots() -> None:
    ROBOTS.write_text(
        "User-agent: *\nAllow: /\n\nSitemap: https://www.resolutemso.com/sitemap.xml\n",
        encoding="utf-8",
    )


def update_homepage() -> None:
    html = INDEX.read_text(encoding="utf-8")

    if 'href="/llms.txt"' not in html:
        html = html.replace("</head>", AGENT_LINK + "</head>", 1)

    html = re.sub(
        r'\s*<script id="resolute-agent-schema" type="application/ld\+json">.*?</script>',
        "",
        html,
        flags=re.S,
    )
    schema_markup = (
        '  <script id="resolute-agent-schema" type="application/ld+json">'
        + json.dumps(SCHEMA, separators=(",", ":"), ensure_ascii=False)
        + "</script>\n"
    )
    html = html.replace("</head>", schema_markup + "</head>", 1)

    if '/assets/js/agentic-readiness.js' not in html:
        html = html.replace("</body>", AGENT_SCRIPT + "</body>", 1)

    html = html.replace(
        '<form action="mailto:support@resolutemso.com" method="POST" enctype="text/plain">',
        '<form action="mailto:support@resolutemso.com" method="POST" enctype="text/plain" '
        'toolname="subscribe_to_resolute_updates" '
        'tooldescription="Prepare a business email subscription request for Resolute MSO updates. Never include PHI or patient information.">',
    )

    INDEX.write_text(html, encoding="utf-8")


def main() -> None:
    update_robots()
    update_homepage()

    required = [ROOT / "assets" / "js" / "agentic-readiness.js", ROBOTS, LLMS, INDEX]
    for path in required:
        if not path.exists() or path.stat().st_size == 0:
            raise RuntimeError(f"Missing agentic-readiness output: {path}")

    html = INDEX.read_text(encoding="utf-8")
    for marker in ("/llms.txt", "resolute-agent-schema", "agentic-readiness.js"):
        if marker not in html:
            raise RuntimeError(f"Homepage agentic marker missing: {marker}")

    print("Agentic browsing readiness applied.")


if __name__ == "__main__":
    main()
