from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FONT_LINKS = """  <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">\n  <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>\n  <link href=\"https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&amp;display=swap\" rel=\"stylesheet\">\n  <link rel=\"stylesheet\" href=\"/assets/css/elegant-typography.css\">\n"""
STYLE_MARKER = '/assets/css/elegant-typography.css'
MANIFEST_MARKER = '  <link rel="manifest" href="/site.webmanifest">\n'


def inject_into_html(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if STYLE_MARKER in text:
        return False
    if "</head>" not in text:
        return False
    text = text.replace("</head>", FONT_LINKS + "</head>", 1)
    path.write_text(text, encoding="utf-8")
    return True


def update_generator(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if STYLE_MARKER in text:
        return False
    if MANIFEST_MARKER not in text:
        raise RuntimeError("Could not find the manifest link in scripts/build_site.py")
    text = text.replace(MANIFEST_MARKER, MANIFEST_MARKER + FONT_LINKS, 1)
    path.write_text(text, encoding="utf-8")
    return True


def main() -> None:
    changed = []
    for html_file in ROOT.rglob("*.html"):
        if any(part in {".git", "node_modules"} for part in html_file.parts):
            continue
        if inject_into_html(html_file):
            changed.append(html_file.relative_to(ROOT).as_posix())

    generator = ROOT / "scripts" / "build_site.py"
    generator_changed = update_generator(generator)

    print(f"Typography stylesheet injected into {len(changed)} HTML files.")
    if generator_changed:
        print("Future generated pages will also include the typography stylesheet.")
    if not changed and not generator_changed:
        print("No changes required; typography refresh is already applied.")


if __name__ == "__main__":
    main()
