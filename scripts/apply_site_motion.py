from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOTION_CSS = '  <link rel="stylesheet" href="/assets/css/site-motion.css">\n'
MOTION_JS = '  <script src="/assets/js/site-motion.js" defer></script>\n'
FULL_H1 = "AI-powered revenue cycle management for modern healthcare providers."
STATIC_H1 = f"<h1>{FULL_H1}</h1>"
MOTION_H1 = (
    f'<h1 class="hero-typewriter" data-typewriter-text="{FULL_H1}">'
    f'<span class="typewriter-sizer" aria-hidden="true">{FULL_H1}</span>'
    f'<span class="typewriter-output" aria-hidden="true">{FULL_H1}</span>'
    f'<span class="sr-only">{FULL_H1}</span>'
    "</h1>"
)


def update_html(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    if "/assets/css/site-motion.css" not in text and "</head>" in text:
        text = text.replace("</head>", MOTION_CSS + "</head>", 1)

    if "/assets/js/site-motion.js" not in text and "</body>" in text:
        text = text.replace("</body>", MOTION_JS + "</body>", 1)

    if path == ROOT / "index.html" and "hero-typewriter" not in text:
        text = text.replace(STATIC_H1, MOTION_H1, 1)

    if text == original:
        return False

    path.write_text(text, encoding="utf-8")
    return True


def update_generator(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    typography_link = '  <link rel="stylesheet" href="/assets/css/elegant-typography.css">\n'
    if "/assets/css/site-motion.css" not in text:
        text = text.replace(typography_link, typography_link + MOTION_CSS, 1)

    inline_footer_script = '  <script>{minify_js(JS)}</script>"""'
    if "/assets/js/site-motion.js" not in text:
        text = text.replace(
            inline_footer_script,
            '  <script>{minify_js(JS)}</script>\n  <script src="/assets/js/site-motion.js" defer></script>"""',
            1,
        )

    home_heading = '      <p class="kicker">Advance Healthcare Solutions</p>\n      <h1>{e(h1(page))}</h1>'
    motion_heading = (
        '      <p class="kicker">Advance Healthcare Solutions</p>\n'
        '      <h1 class="hero-typewriter" data-typewriter-text="{e(h1(page))}">'
        '<span class="typewriter-sizer" aria-hidden="true">{e(h1(page))}</span>'
        '<span class="typewriter-output" aria-hidden="true">{e(h1(page))}</span>'
        '<span class="sr-only">{e(h1(page))}</span></h1>'
    )
    if "hero-typewriter" not in text:
        text = text.replace(home_heading, motion_heading, 1)

    if text == original:
        return False

    path.write_text(text, encoding="utf-8")
    return True


def main() -> None:
    changed = []
    for html_file in ROOT.rglob("*.html"):
        if any(part in {".git", "node_modules"} for part in html_file.parts):
            continue
        if update_html(html_file):
            changed.append(html_file.relative_to(ROOT).as_posix())

    generator_changed = update_generator(ROOT / "scripts" / "build_site.py")

    print(f"Motion assets integrated into {len(changed)} HTML files.")
    if generator_changed:
        print("The site generator now preserves the typewriter and scroll motion system.")


if __name__ == "__main__":
    main()
