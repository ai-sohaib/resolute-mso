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
    pattern = re.compile(
        r'<div class="platform-strip(?: platform-logo-strip)?">(?:(?!</div>).)*?(?:OfficeAlly)(?:(?!</div>).)*?(?:Telcor LIS)(?:(?!</div>).)*?</div>',
        re.S,
    )
    updated, count = pattern.subn(PLATFORM_MARKUP, html, count=1)
    if count != 1:
        raise RuntimeError("Could not locate the workflow-familiarity platform strip.")
    return updated


def remove_mailto(html: str) -> str:
    html = re.sub(r'href="mailto:[^"]+"', 'href="/contact/"', html, flags=re.I)
    html = re.sub(r'action="mailto:[^"]+"', 'action="/contact/"', html, flags=re.I)
    html = re.sub(r'\s+enctype="text/plain"', "", html, flags=re.I)
    html = re.sub(r'method="POST"(?=[^>]*action="/contact/")', 'method="GET"', html, flags=re.I)
    return html


def inline_critical_css(html: str) -> str:
    if not CSS.exists() or not PLATFORM_CSS.exists():
        raise RuntimeError("Required homepage CSS source is missing.")

    css = minify_css(
        CSS.read_text(encoding="utf-8")
        + "\n"
        + PLATFORM_CSS.read_text(encoding="utf-8")
    )
    style = f'<style id="resolute-critical-typography">{css}</style>'

    html = re.sub(
        r'\s*<link id="resolute-critical-typography"[^>]*>',
        "",
        html,
        flags=re.I,
    )
    html = re.sub(
        r'\s*<style id="resolute-critical-typography">.*?</style>',
        "",
        html,
        flags=re.S | re.I,
    )
    if "</head>" not in html:
        raise RuntimeError("Homepage closing head tag is missing.")
    return html.replace("</head>", style + "</head>", 1)


def validate(html: str) -> None:
    forbidden = {
        "mailto:": "mailto URL",
        "google.com/s2/favicons": "remote Google favicon",
        "gstatic.com/favicon": "remote gstatic favicon",
        'href="/assets/css/pagespeed-home.css"': "render-blocking stylesheet link",
        "data:image/png;base64": "large inline platform sprite",
    }
    for needle, label in forbidden.items():
        if needle.lower() in html.lower():
            raise RuntimeError(f"Final homepage still contains a {label}.")

    required = [
        "/assets/img/platform-logos-sprite.png",
        "platform-logo-officeally",
        "platform-logo-telcor",
        '<style id="resolute-critical-typography">',
    ]
    for needle in required:
        if needle not in html:
            raise RuntimeError(f"Final homepage is missing required marker: {needle}")

    if not (ROOT / "assets" / "img" / "platform-logos-sprite.png").exists():
        raise RuntimeError("Local platform logo sprite file is missing.")


def main() -> None:
    html = INDEX.read_text(encoding="utf-8")
    html = replace_platform_strip(html)
    html = remove_mailto(html)
    html = inline_critical_css(html)
    validate(html)
    INDEX.write_text(html, encoding="utf-8")
    print("Final PageSpeed output created: local logo sprite, no mailto requests, inline critical CSS.")


if __name__ == "__main__":
    main()
