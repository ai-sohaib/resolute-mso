from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
CSS = ROOT / "assets" / "css" / "pagespeed-home.css"

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

SPRITE_CSS = '''
.platform-logo-strip span{padding:7px 14px 7px 8px;gap:10px;min-height:48px}
.platform-logo-strip i{display:inline-block;width:32px;height:32px;flex:0 0 32px;background-image:url('/assets/img/platform-logos-sprite.webp');background-repeat:no-repeat;background-size:256px 32px;border-radius:50%}
.platform-logo-officeally{background-position:0 0}.platform-logo-eclinicalworks{background-position:-32px 0}.platform-logo-carecloud{background-position:-64px 0}.platform-logo-nextgen{background-position:-96px 0}.platform-logo-athenahealth{background-position:-128px 0}.platform-logo-advancedmd{background-position:-160px 0}.platform-logo-modmed{background-position:-192px 0}.platform-logo-telcor{background-position:-224px 0}
.platform-logo-strip em{font-style:normal}
@media(max-width:720px){.platform-logo-strip{gap:10px}.platform-logo-strip span{min-height:46px;padding:6px 12px 6px 7px}.platform-logo-strip i{width:30px;height:30px;flex-basis:30px;background-size:240px 30px}.platform-logo-eclinicalworks{background-position:-30px 0}.platform-logo-carecloud{background-position:-60px 0}.platform-logo-nextgen{background-position:-90px 0}.platform-logo-athenahealth{background-position:-120px 0}.platform-logo-advancedmd{background-position:-150px 0}.platform-logo-modmed{background-position:-180px 0}.platform-logo-telcor{background-position:-210px 0}}
'''


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


def optimize_logo(html: str) -> str:
    html = re.sub(
        r'src="/assets/img/resolute-mso-logo(?:-\d+)?\.webp"',
        'src="/assets/img/resolute-mso-logo-320.webp"',
        html,
    )
    html = re.sub(
        r'(<img\b[^>]*src="/assets/img/resolute-mso-logo-320\.webp"[^>]*?)\swidth="\d+"\sheight="\d+"',
        r'\1 width="320" height="90"',
        html,
    )
    return html


def inline_home_css(html: str) -> str:
    if not CSS.exists():
        raise RuntimeError("pagespeed-home.css is missing.")
    css = CSS.read_text(encoding="utf-8")
    if ".platform-logo-strip i" not in css:
        css = css.rstrip() + "\n" + minify_css(SPRITE_CSS) + "\n"
        CSS.write_text(css, encoding="utf-8")
    inline = minify_css(css)
    html = re.sub(
        r'<link id="resolute-critical-typography" rel="stylesheet" href="/assets/css/pagespeed-home\.css">',
        f'<style id="resolute-critical-typography">{inline}</style>',
        html,
        count=1,
    )
    return html


def main() -> None:
    html = INDEX.read_text(encoding="utf-8")
    html = replace_platform_strip(html)
    html = remove_mailto(html)
    html = optimize_logo(html)
    html = inline_home_css(html)

    if "mailto:" in html:
        raise RuntimeError("Homepage still contains a mailto URL.")
    if "google.com/s2/favicons" in html or "gstatic.com/favicon" in html:
        raise RuntimeError("Homepage still contains a remote favicon request.")
    if "platform-logos-sprite.webp" not in html:
        raise RuntimeError("Platform sprite CSS was not inlined.")
    if "/assets/css/pagespeed-home.css" in html:
        raise RuntimeError("Render-blocking homepage stylesheet is still linked.")

    INDEX.write_text(html, encoding="utf-8")
    print("Final PageSpeed fixes applied: local logos, no mailto, optimized logo, inline CSS.")


if __name__ == "__main__":
    main()
