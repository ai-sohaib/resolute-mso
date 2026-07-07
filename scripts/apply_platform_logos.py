from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
CSS = ROOT / "assets" / "css" / "pagespeed-home.css"

PLATFORMS = [
    ("OfficeAlly", "officeally.com"),
    ("eClinicalWorks", "eclinicalworks.com"),
    ("CareCloud", "carecloud.com"),
    ("NextGen", "nextgen.com"),
    ("Athenahealth", "athenahealth.com"),
    ("AdvancedMD", "advancedmd.com"),
    ("ModMed", "modmed.com"),
    ("Telcor LIS", "telcor.com"),
]

PLATFORM_CSS = """
.platform-logo-strip span{padding:7px 14px 7px 8px;gap:10px;min-height:48px}
.platform-logo-strip img{width:32px;height:32px;object-fit:contain;flex:0 0 32px;border-radius:50%}
.platform-logo-strip em{font-style:normal}
@media(max-width:720px){
.platform-logo-strip{gap:10px}
.platform-logo-strip span{min-height:46px;padding:6px 12px 6px 7px}
.platform-logo-strip img{width:30px;height:30px;flex-basis:30px}
}
"""


def minify_css(css: str) -> str:
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    return re.sub(r"\s*([{}:;,])\s*", r"\1", css).strip()


def main() -> None:
    markup = '<div class="platform-strip platform-logo-strip">' + "".join(
        f'<span><img src="https://www.google.com/s2/favicons?domain={domain}&amp;sz=128" '
        f'width="64" height="64" alt="" aria-hidden="true" loading="lazy" '
        f'decoding="async" referrerpolicy="no-referrer"><em>{label}</em></span>'
        for label, domain in PLATFORMS
    ) + "</div>"

    html = INDEX.read_text(encoding="utf-8")
    pattern = re.compile(
        r'<div class="platform-strip">(?=.*?OfficeAlly)(?=.*?Telcor LIS).*?</div>',
        re.S,
    )
    updated, count = pattern.subn(markup, html, count=1)
    if count != 1:
        raise RuntimeError("Could not locate the workflow-familiarity platform strip.")
    INDEX.write_text(updated, encoding="utf-8")

    css = CSS.read_text(encoding="utf-8")
    if ".platform-logo-strip img" not in css:
        CSS.write_text(css.rstrip() + "\n" + minify_css(PLATFORM_CSS) + "\n", encoding="utf-8")

    print("Official platform logos applied to the workflow-familiarity section.")


if __name__ == "__main__":
    main()
