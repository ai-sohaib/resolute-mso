from __future__ import annotations

import io
import re
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
CSS = ROOT / "assets" / "css" / "pagespeed-home.css"
LOGO_DIR = ROOT / "assets" / "img" / "platforms"

PLATFORMS = [
    ("officeally", "OfficeAlly", "officeally.com"),
    ("eclinicalworks", "eClinicalWorks", "eclinicalworks.com"),
    ("carecloud", "CareCloud", "carecloud.com"),
    ("nextgen", "NextGen", "nextgen.com"),
    ("athenahealth", "Athenahealth", "athenahealth.com"),
    ("advancedmd", "AdvancedMD", "advancedmd.com"),
    ("modmed", "ModMed", "modmed.com"),
    ("telcor", "Telcor LIS", "telcor.com"),
]

PLATFORM_CSS = """
.platform-logo-strip span{padding:7px 14px 7px 8px;gap:10px;min-height:48px}
.platform-logo-strip img{width:32px;height:32px;object-fit:contain;flex:0 0 32px}
.platform-logo-strip em{font-style:normal}
@media(max-width:720px){
.platform-logo-strip{gap:10px}
.platform-logo-strip span{min-height:46px;padding:6px 12px 6px 7px}
.platform-logo-strip img{width:30px;height:30px;flex-basis:30px}
}
"""


def fetch_logo(domain: str, destination: Path) -> None:
    query = urllib.parse.urlencode({"domain_url": f"https://{domain}", "sz": 128})
    url = f"https://www.google.com/s2/favicons?{query}"
    request = urllib.request.Request(url, headers={"User-Agent": "ResoluteMSO-Build/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = response.read()
    if len(payload) < 100:
        raise RuntimeError(f"Logo download for {domain} returned an invalid payload.")

    with Image.open(io.BytesIO(payload)) as image:
        image.load()
        image = image.convert("RGBA")
        image.thumbnail((64, 64), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (64, 64), (255, 255, 255, 0))
        canvas.alpha_composite(image, ((64 - image.width) // 2, (64 - image.height) // 2))
        destination.parent.mkdir(parents=True, exist_ok=True)
        canvas.save(destination, "WEBP", quality=88, method=6)


def minify_css(css: str) -> str:
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    return re.sub(r"\s*([{}:;,])\s*", r"\1", css).strip()


def main() -> None:
    LOGO_DIR.mkdir(parents=True, exist_ok=True)
    for slug, _, domain in PLATFORMS:
        destination = LOGO_DIR / f"{slug}.webp"
        fetch_logo(domain, destination)

    markup = '<div class="platform-strip platform-logo-strip">' + "".join(
        f'<span><img src="/assets/img/platforms/{slug}.webp" width="64" height="64" '
        f'alt="" aria-hidden="true" loading="lazy" decoding="async"><em>{label}</em></span>'
        for slug, label, _ in PLATFORMS
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

    for slug, _, _ in PLATFORMS:
        if not (LOGO_DIR / f"{slug}.webp").exists():
            raise RuntimeError(f"Missing generated platform logo: {slug}")

    print("Official platform logos applied to the workflow-familiarity section.")


if __name__ == "__main__":
    main()
