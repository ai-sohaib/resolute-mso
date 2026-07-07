from __future__ import annotations

from pathlib import Path

from playwright.sync_api import sync_playwright

OUTPUT = Path("artifacts/visual-evidence")
OUTPUT.mkdir(parents=True, exist_ok=True)

TARGETS = [
    ("desktop", {"width": 1440, "height": 1000}),
    ("mobile", {"width": 390, "height": 844}),
]

PAGES = [
    ("before-home", "https://www.resolutemso.com/"),
    ("after-home", "http://127.0.0.1:8080/"),
]


def main() -> int:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        for label, viewport in TARGETS:
            context = browser.new_context(viewport=viewport, device_scale_factor=1)
            page = context.new_page()
            page.emulate_media(reduced_motion="reduce")
            for name, url in PAGES:
                page.goto(url, wait_until="domcontentloaded", timeout=90000)
                page.wait_for_timeout(2500)
                page.screenshot(path=OUTPUT / f"{name}-{label}.png", full_page=True)
            context.close()
        browser.close()
    print(f"Saved before-and-after evidence to {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
