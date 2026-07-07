from __future__ import annotations

import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
TYPOGRAPHY = ASSETS / "css" / "elegant-typography.css"
HOME_CSS = ASSETS / "css" / "pagespeed-home-source.css"
WHATSAPP_URL = (
    "https://wa.me/17015525527?text=Hello%20Resolute%20MSO%2C%20I%27d%20like%20"
    "to%20discuss%20RCM%20and%20billing%20automation."
)

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
html{scroll-behavior:auto}
.btn{min-height:44px;background:#087a70;border-color:#087a70}
.btn:hover,.btn:focus-visible{background:#05665f;border-color:#05665f}
.btn.btn-secondary{background:#fff;color:#05665f;border-color:#b9c9c5;box-shadow:none}
.btn.btn-secondary:hover,.btn.btn-secondary:focus-visible{background:#eaf8f6;color:#05665f;border-color:#087a70}
.btn-whatsapp,.whatsapp-launch{background:#006b3f;border-color:#006b3f;color:#fff}
.btn-whatsapp:hover,.btn-whatsapp:focus-visible,.whatsapp-launch:hover,.whatsapp-launch:focus-visible{background:#005331;border-color:#005331;color:#fff}
.menu-caret{width:28px;min-width:28px}
.hero-actions{overflow:visible;gap:14px}.hero-actions .btn{min-height:48px}
.hero-image picture{display:block}.card-actions{display:flex;flex-wrap:wrap;gap:12px;margin-top:16px}
.card-actions .btn{min-height:44px;padding:8px 14px}.site-header{backdrop-filter:none;-webkit-backdrop-filter:none}
.section:has(.center){content-visibility:visible;contain-intrinsic-size:auto}.center{padding:16px 0;overflow:visible}
.center .btn{min-height:48px;margin:8px 0}
@media(max-width:1060px){.menu-caret{min-width:44px}}
@media(max-width:720px){*{animation:none!important;transition:none!important}.site-header{box-shadow:none}.hero-image,.info-card,.directory-card,.related-grid a,.workflow-grid article,.answer-grid article,.dashboard-visual,.metric-panel,.trust-list a{box-shadow:none!important;filter:none!important}.hero-actions,.card-actions{gap:16px;overflow:visible}.hero-actions .btn,.card-actions .btn{min-height:48px;position:relative;z-index:1}}
"""


def minify_css(css: str) -> str:
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    return re.sub(r"\s*([{}:;,])\s*", r"\1", css).strip()


def optimize_image(source: Path, target: Path, width: int, quality: int) -> tuple[int, int]:
    with Image.open(source) as image:
        image.load()
        if image.width > width:
            height = max(1, round(image.height * width / image.width))
            image = image.resize((width, height), Image.Resampling.LANCZOS)
        if image.mode not in {"RGB", "RGBA"}:
            image = image.convert("RGB")
        target.parent.mkdir(parents=True, exist_ok=True)
        image.save(target, "WEBP", quality=quality, method=6)
        return image.size


def build_hero_images() -> dict[str, tuple[int, int]]:
    hero = ASSETS / "img" / "healthcare-hero-ai.jpg"
    if not hero.exists():
        return {}
    return {
        "mobile": optimize_image(hero, ASSETS / "img" / "healthcare-hero-ai-420.webp", 420, 68),
        "desktop": optimize_image(hero, ASSETS / "img" / "healthcare-hero-ai-720.webp", 720, 72),
    }


def strip_external_font_dependencies(text: str) -> str:
    for pattern in GOOGLE_FONT_PATTERNS:
        text = re.sub(pattern, "", text)
    text = re.sub(r'\s*<link rel="stylesheet" href="/assets/css/elegant-typography\.css">', "", text)
    return re.sub(r'\s*<link rel="manifest" href="/site\.webmanifest">', "", text)


def replace_vague_links(text: str) -> str:
    for old, new in DESCRIPTIVE_LINKS.items():
        text = text.replace(old, new)
    return text


def use_high_density_logo(text: str) -> str:
    text = re.sub(
        r"/assets/img/resolute-mso-logo(?:-\d+)?\.webp",
        "/assets/img/resolute-mso-logo.webp",
        text,
    )
    return re.sub(
        r'(<img\b[^>]*src="/assets/img/resolute-mso-logo\.webp"[^>]*?)\swidth="\d+"\sheight="\d+"',
        r'\1 width="460" height="130"',
        text,
    )


def direct_contact_controls(text: str) -> str:
    text = text.replace(
        '<button class="scroll-top" type="button" aria-label="Go to top">&#8593;</button>',
        '<a class="scroll-top visible" href="#main" aria-label="Go to top">&#8593;</a>',
    )

    def whatsapp_anchor(match: re.Match[str]) -> str:
        return (
            f'<a class="whatsapp-launch" href="{WHATSAPP_URL}" target="_blank" '
            'rel="noopener noreferrer" aria-label="Chat with Resolute MSO on WhatsApp">'
            f'{match.group(1)}</a>'
        )

    text = re.sub(r'<button class="whatsapp-launch"[^>]*>(.*?)</button>', whatsapp_anchor, text, flags=re.S)
    text = re.sub(r'\s*<section class="whatsapp-panel" id="whatsapp-panel".*?</section>', "", text, flags=re.S)
    text = re.sub(
        r'\s*<script>\(function \(\) \{ var toggle = document\.querySelector\("\.nav-toggle"\);.*?</script>',
        "",
        text,
        flags=re.S,
    )
    if 'id="resolute-nav-script"' not in text and "</body>" in text:
        nav_script = (
            '<script id="resolute-nav-script">(()=>{const t=document.querySelector(".nav-toggle"),'
            'n=document.querySelector(".main-nav");if(t&&n)t.addEventListener("click",()=>{'
            'const o=n.classList.toggle("open");t.setAttribute("aria-expanded",String(o))})})();</script>'
        )
        text = text.replace("</body>", nav_script + "</body>", 1)
    return text


def optimized_hero(dimensions: dict[str, tuple[int, int]]) -> str:
    width, height = dimensions.get("desktop", (720, 495))
    return (
        '<picture><source media="(max-width:720px)" srcset="/assets/img/healthcare-hero-ai-420.webp">'
        '<img src="/assets/img/healthcare-hero-ai-720.webp" '
        'alt="Smiling healthcare professional in a modern office with revenue dashboards in the background" '
        f'width="{width}" height="{height}" fetchpriority="high" decoding="async"></picture>'
    )


def optimize_homepage(dimensions: dict[str, tuple[int, int]]) -> None:
    path = ROOT / "index.html"
    text = path.read_text(encoding="utf-8")
    text = strip_external_font_dependencies(text)
    text = replace_vague_links(text)
    text = use_high_density_logo(text)
    text = direct_contact_controls(text)

    text = re.sub(
        r'\s*<script>\(function\(\)\{var targets=document\.querySelectorAll\("\.hero-image,.*?</script>',
        "",
        text,
        flags=re.S,
    )

    if dimensions:
        text = re.sub(
            r'<img\b[^>]*src="/assets/img/healthcare-hero-ai\.jpg"[^>]*>',
            optimized_hero(dimensions),
            text,
            count=1,
        )

    combined_css = minify_css(HOME_CSS.read_text(encoding="utf-8"))
    css_path = ASSETS / "css" / "pagespeed-home.css"
    css_path.write_text(combined_css + "\n", encoding="utf-8")

    text = re.sub(r"\s*<style(?:\s+[^>]*)?>.*?</style>", "", text, flags=re.S)
    text = text.replace(
        "</head>",
        '<link id="resolute-critical-typography" rel="stylesheet" href="/assets/css/pagespeed-home.css"></head>',
        1,
    )
    path.write_text(text, encoding="utf-8")


def optimize_other_pages(typography_css: str) -> int:
    inline_css = minify_css(typography_css + "\n" + HARDENING_CSS)
    changed = 0
    for path in ROOT.rglob("*.html"):
        if path == ROOT / "index.html" or any(part in {".git", "node_modules"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        original = text
        text = strip_external_font_dependencies(text)
        text = replace_vague_links(text)
        text = use_high_density_logo(text)
        text = direct_contact_controls(text)
        if 'id="resolute-critical-typography"' not in text and "</head>" in text:
            text = text.replace(
                "</head>",
                f'<style id="resolute-critical-typography">{inline_css}</style></head>',
                1,
            )
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed += 1
    return changed


def main() -> None:
    typography_css = TYPOGRAPHY.read_text(encoding="utf-8").replace(
        '"Manrope", "Avenir Next", "Segoe UI", Helvetica, Arial, sans-serif',
        '"Segoe UI Variable Text", "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
    )
    dimensions = build_hero_images()
    optimize_homepage(dimensions)
    changed = optimize_other_pages(typography_css)
    print(f"PageSpeed homepage built; {changed} supporting HTML files updated.")


if __name__ == "__main__":
    main()
