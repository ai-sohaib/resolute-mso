from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
CSS = ROOT / "assets" / "css" / "pagespeed-home.css"
PLATFORM_CSS = ROOT / "assets" / "css" / "platform-logos-inline.css"

PLATFORM_MARKUP = '''<div class="platform-strip platform-logo-strip">
  <span><i class="platform-logo platform-logo-officeally" aria-hidden="true"></i><em>OfficeAlly</em></span>
  <span><i class="platform-logo platform-logo-eclinicalworks" aria-hidden="true"></i><em>eClinicalWorks</em></span>
  <span><i class="platform-logo platform-logo-carecloud" aria-hidden="true"></i><em>CareCloud</em></span>
  <span><i class="platform-logo platform-logo-nextgen" aria-hidden="true"></i><em>NextGen</em></span>
  <span><i class="platform-logo platform-logo-athenahealth" aria-hidden="true"></i><em>Athenahealth</em></span>
  <span><i class="platform-logo platform-logo-advancedmd" aria-hidden="true"></i><em>AdvancedMD</em></span>
  <span><i class="platform-logo platform-logo-modmed" aria-hidden="true"></i><em>ModMed</em></span>
  <span><i class="platform-logo platform-logo-telcor" aria-hidden="true"></i><em>Telcor LIS</em></span>
</div>'''


def minify_css(css: str) -> str:
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    return re.sub(r"\s*([{}:;,])\s*", r"\1", css).strip()


def replace_platform_strip(html: str) -> str:
    patterns = [
        r'<div class="platform-strip platform-logo-strip">.*?</div>',
        r'<div class="platform-strip">(?=.*?OfficeAlly)(?=.*?Telcor LIS).*?</div>',
    ]
    for pattern in patterns:
        updated, count = re.subn(pattern, PLATFORM_MARKUP, html, count=1, flags=re.S)
        if count:
            return updated
    raise RuntimeError("Workflow-familiarity platform strip was not found.")


def remove_mailto(html: str) -> str:
    html = re.sub(
        r'<a href="mailto:support@resolutemso\.com">support@resolutemso\.com</a>',
        '<a href="/contact/" aria-label="Contact Resolute MSO">support@resolutemso.com</a>',
        html,
    )
    html = re.sub(
        r'<a href="mailto:support@resolutemso\.com" aria-label="Email Resolute MSO">',
        '<a href="/contact/" aria-label="Contact Resolute MSO">',
        html,
    )
    html = re.sub(
        r'<form action="mailto:support@resolutemso\.com" method="POST" enctype="text/plain">',
        '<form action="/contact/" method="GET">',
        html,
    )
    return html


def inline_home_css(html: str) -> str:
    if not CSS.exists() or not PLATFORM_CSS.exists():
        raise RuntimeError("Required homepage CSS source is missing.")
    css = minify_css(
        CSS.read_text(encoding="utf-8")
        + "\n"
        + PLATFORM_CSS.read_text(encoding="utf-8")
    )

    style = f'<style id="resolute-critical-typography">{css}</style>'
    linked_pattern = r'<link id="resolute-critical-typography" rel="stylesheet" href="/assets/css/pagespeed-home\.css">'
    inline_pattern = r'<style id="resolute-critical-typography">.*?</style>'

    if re.search(linked_pattern, html):
        return re.sub(linked_pattern, style, html, count=1)
    if re.search(inline_pattern, html, flags=re.S):
        return re.sub(inline_pattern, style, html, count=1, flags=re.S)
    raise RuntimeError("Homepage critical stylesheet marker was not found.")


def main() -> None:
    html = INDEX.read_text(encoding="utf-8")
    html = replace_platform_strip(html)
    html = remove_mailto(html)
    html = inline_home_css(html)

    checks = {
        "mailto:": "Homepage still contains a mailto URL.",
        "google.com/s2/favicons": "Homepage still contains a remote Google favicon request.",
        "gstatic.com/favicon": "Homepage still contains a remote gstatic favicon request.",
        "/assets/css/pagespeed-home.css": "Render-blocking homepage stylesheet is still linked.",
    }
    for needle, message in checks.items():
        if needle in html:
            raise RuntimeError(message)
    if "data:image/png;base64" not in html or "platform-logo-officeally" not in html:
        raise RuntimeError("Embedded platform logos were not added.")

    INDEX.write_text(html, encoding="utf-8")
    print("Final PageSpeed fixes applied: embedded logos, no mailto, inline CSS.")


if __name__ == "__main__":
    main()
