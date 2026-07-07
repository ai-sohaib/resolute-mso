from __future__ import annotations

import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
TYPOGRAPHY_CSS = ASSETS / "css" / "elegant-typography.css"

GOOGLE_FONT_PATTERNS = (
    r'\s*<link rel="preconnect" href="https://fonts\.googleapis\.com">',
    r'\s*<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>',
    r'\s*<link href="https://fonts\.googleapis\.com/css2\?family=Manrope:[^"]+" rel="stylesheet">',
)

DESCRIPTIVE_LINKS = {
    '<a href="/automation-suite/">See More</a>': '<a href="/automation-suite/">View Automation Suite</a>',
    '<a href="/services/">See More</a>': '<a href="/services/">View All Services</a>',
    '<a href="/industries-who-we-serve/">See More</a>': '<a href="/industries-who-we-serve/">View All Specialties</a>',
    '<a href="/resources/">See More</a>': '<a href="/resources/">View All Resources</a>',
    '<a href="/about/">See More</a>': '<a href="/about/">View Company Information</a>',
}

HARDENING_CSS = """
:root{--teal:#087a70;--teal-dark:#05665f;--font-ui:"Segoe UI Variable Text","Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.btn{background:#087a70;border-color:#087a70}
.btn:hover,.btn:focus-visible{background:#05665f;border-color:#05665f}
.btn-whatsapp,.whatsapp-launch{background:#006b3f;border-color:#006b3f;color:#fff}
.btn-whatsapp:hover,.btn-whatsapp:focus-visible,.whatsapp-launch:hover,.whatsapp-launch:focus-visible{background:#005331;border-color:#005331;color:#fff}
.menu-caret{width:28px;min-width:28px}
@media(max-width:1060px){.menu-caret{min-width:44px}}
"""


def minify_css(css: str) -> str:
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{}:;,])\s*", r"\1", css)
    return css.strip()


def optimize_image(source: Path, destination: Path, width: int, quality: int) -> tuple[int, int]:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as image:
        image.load()
        if image.width > width:
            height = max(1, round(image.height * width / image.width))
            image = image.resize((width, height), Image.Resampling.LANCZOS)
        else:
            width, height = image.size
        if image.mode not in {"RGB", "RGBA"}:
            image = image.convert("RGBA" if "transparency" in image.info else "RGB")
        image.save(destination, format="WEBP", quality=quality, method=6)
        return image.size


def build_images() -> dict[str, tuple[int, int]]:
    dimensions: dict[str, tuple[int, int]] = {}
    logo = ASSETS / "img" / "resolute-mso-logo.webp"
    hero = ASSETS / "img" / "healthcare-hero-ai.jpg"

    if logo.exists():
        dimensions["logo"] = optimize_image(
            logo,
            ASSETS / "img" / "resolute-mso-logo-240.webp",
            240,
            82,
        )

    if hero.exists():
        dimensions["hero480"] = optimize_image(
            hero,
            ASSETS / "img" / "healthcare-hero-ai-480.webp",
            480,
            76,
        )
        dimensions["hero768"] = optimize_image(
            hero,
            ASSETS / "img" / "healthcare-hero-ai-768.webp",
            768,
            78,
        )

    return dimensions


def optimized_logo_tag(match: re.Match[str], dimensions: tuple[int, int] | None) -> str:
    tag = match.group(0).replace(
        '/assets/img/resolute-mso-logo.webp',
        '/assets/img/resolute-mso-logo-240.webp',
    )
    if dimensions:
        width, height = dimensions
        tag = re.sub(r'\swidth="\d+"', f' width="{width}"', tag)
        tag = re.sub(r'\sheight="\d+"', f' height="{height}"', tag)
    return tag


def optimized_hero_tag(dimensions: dict[str, tuple[int, int]]) -> str:
    width, height = dimensions.get("hero768", (768, 512))
    return (
        '<img src="/assets/img/healthcare-hero-ai-768.webp" '
        'srcset="/assets/img/healthcare-hero-ai-480.webp 480w, '
        '/assets/img/healthcare-hero-ai-768.webp 768w" '
        'sizes="(max-width:720px) calc(100vw - 28px), '
        '(max-width:1060px) calc(100vw - 40px), 540px" '
        'alt="Smiling healthcare professional in a modern office with revenue dashboards in the background" '
        f'width="{width}" height="{height}" fetchpriority="high" decoding="async">'
    )


def remove_legacy_reveal(text: str) -> str:
    text = re.sub(
        r'\s*\.reveal\{opacity:0;transform:translateY\(18px\) scale\(\.985\);transition:opacity \.6s ease,transform \.6s ease\}',
        "",
        text,
    )
    text = re.sub(r'\s*\.reveal\.is-visible\{opacity:1;transform:none\}', "", text)
    text = text.replace(
        'transform:translateZ(0);will-change:transform,box-shadow,filter;backface-visibility:hidden',
        '',
    )
    text = re.sub(
        r'\s*<script>\(function\(\)\{var targets=document\.querySelectorAll\("\.hero-image,.*?</script>',
        "",
        text,
        flags=re.S,
    )
    return text


def patch_html(path: Path, inline_css: str, dimensions: dict[str, tuple[int, int]]) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    for pattern in GOOGLE_FONT_PATTERNS:
        text = re.sub(pattern, "", text)

    text = re.sub(
        r'\s*<link rel="stylesheet" href="/assets/css/elegant-typography\.css">',
        "",
        text,
    )

    if 'id="resolute-critical-typography"' not in text and "</head>" in text:
        text = text.replace(
            "</head>",
            f'<style id="resolute-critical-typography">{inline_css}</style></head>',
            1,
        )

    for old, new in DESCRIPTIVE_LINKS.items():
        text = text.replace(old, new)

    logo_dimensions = dimensions.get("logo")
    if logo_dimensions:
        text = re.sub(
            r'<img\b[^>]*src="/assets/img/resolute-mso-logo\.webp"[^>]*>',
            lambda match: optimized_logo_tag(match, logo_dimensions),
            text,
        )

    if path == ROOT / "index.html" and dimensions.get("hero768"):
        text = re.sub(
            r'<img\b[^>]*src="/assets/img/healthcare-hero-ai\.jpg"[^>]*>',
            optimized_hero_tag(dimensions),
            text,
            count=1,
        )
        text = remove_legacy_reveal(text)

    if text == original:
        return False

    path.write_text(text, encoding="utf-8")
    return True


def main() -> None:
    typography = TYPOGRAPHY_CSS.read_text(encoding="utf-8")
    typography = typography.replace(
        '"Manrope", "Avenir Next", "Segoe UI", Helvetica, Arial, sans-serif',
        '"Segoe UI Variable Text", "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
    )
    inline_css = minify_css(typography + HARDENING_CSS)
    dimensions = build_images()

    changed: list[str] = []
    for html_file in ROOT.rglob("*.html"):
        if any(part in {".git", "node_modules"} for part in html_file.parts):
            continue
        if patch_html(html_file, inline_css, dimensions):
            changed.append(html_file.relative_to(ROOT).as_posix())

    print(f"PageSpeed fixes applied to {len(changed)} HTML files.")
    for relative_path in changed[:20]:
        print(f"- {relative_path}")
    if len(changed) > 20:
        print(f"- ... and {len(changed) - 20} additional files")


if __name__ == "__main__":
    main()
