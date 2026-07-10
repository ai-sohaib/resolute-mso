from __future__ import annotations

import io
import re
import time
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
.platform-logo-strip img{width:32px;height:32px;object-fit:contain;flex:0 0 32px;border-radius:8px}
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


def download_logo(domain: str) -> bytes:
    query = urllib.parse.urlencode({"domain": domain, "sz": 128})
    url = f"https://www.google.com/s2/favicons?{query}"
    last_error: Exception | None = None
    for attempt in range(4):
        try:
            request = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (compatible; ResoluteMSO-StaticBuild/1.0)",
                    "Accept": "image/avif,image/webp,image/apng,image/png,image/*,*/*;q=0.8",
                },
            )
            with urllib.request.urlopen(request, timeout=30) as response:
                payload = response.read()
            if len(payload) < 150:
                raise RuntimeError(f"Unexpectedly small logo response for {domain}: {len(payload)} bytes")
            return payload
        except Exception as error:  # pragma: no cover - network retry path
            last_error = error
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"Unable to download the platform logo for {domain}: {last_error}")


def save_optimized_logo(payload: bytes, destination: Path) -> None:
    with Image.open(io.BytesIO(payload)) as image:
        image.load()
        image = image.convert("RGBA")
        image.thumbnail((96, 96), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (96, 96), (255, 255, 255, 0))
        canvas.alpha_composite(image, ((96 - image.width) // 2, (96 - image.height) // 2))
        destination.parent.mkdir(parents=True, exist_ok=True)
        canvas.save(destination, "WEBP", quality=90, method=6)


def main() -> None:
    LOGO_DIR.mkdir(parents=True, exist_ok=True)
    for slug, _, domain in PLATFORMS:
        save_optimized_logo(download_logo(domain), LOGO_DIR / f"{slug}.webp")

    markup = '<div class="platform-strip platform-logo-strip">' + "".join(
        f'<span><img src="/assets/img/platforms/{slug}.webp" width="96" height="96" '
        f'alt="" aria-hidden="true" loading="lazy" decoding="async"><em>{label}</em></span>'
        for slug, label, _ in PLATFORMS
    ) + "</div>"

    html = INDEX.read_text(encoding="utf-8")
    pattern = re.compile(
        r'<div class="platform-strip(?: platform-logo-strip)?">(?=.*?OfficeAlly)(?=.*?Telcor LIS).*?</div>',
        re.S,
    )
    updated, count = pattern.subn(markup, html, count=1)
    if count != 1:
        raise RuntimeError("Could not locate the workflow-familiarity platform strip.")
    INDEX.write_text(updated, encoding="utf-8")

    css = CSS.read_text(encoding="utf-8")
    css = re.sub(
        r'\.platform-logo-strip span\{.*?@media\(max-width:720px\)\{.*?\}\s*\}',
        "",
        css,
        flags=re.S,
    )
    CSS.write_text(css.rstrip() + "\n" + minify_css(PLATFORM_CSS) + "\n", encoding="utf-8")

    for slug, _, _ in PLATFORMS:
        path = LOGO_DIR / f"{slug}.webp"
        if not path.exists() or path.stat().st_size < 150:
            raise RuntimeError(f"Missing or invalid generated platform logo: {path}")

    print("Local optimized platform logos applied to the workflow-familiarity section.")


if __name__ == "__main__":
    main()
