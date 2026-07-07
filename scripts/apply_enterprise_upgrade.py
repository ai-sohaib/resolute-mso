from __future__ import annotations

import argparse
import re
from html import escape
from pathlib import Path

EXACT_TITLE = "AI-Driven Medical Billing & RCM That Stops Revenue Leakage"
META_DESCRIPTION = (
    "Resolute MSO helps U.S. healthcare providers improve medical billing and RCM, "
    "reduce denials, recover AR, and use automation to strengthen revenue workflows."
)
STYLE_TAG = '<link rel="stylesheet" href="/assets/css/enterprise-upgrade.css?v=20260707">'
CONFIG_TAG = '<script src="/config.js?v=20260707" defer></script>'


def inject_assets(markup: str) -> str:
    additions = []
    if "/assets/css/enterprise-upgrade.css" not in markup:
        additions.append(STYLE_TAG)
    if 'src="/config.js' not in markup:
        additions.append(CONFIG_TAG)
    if additions:
        markup = markup.replace("</head>", "  " + "\n  ".join(additions) + "\n</head>", 1)
    return markup


def remove_insecure_form_actions(markup: str) -> str:
    return re.sub(
        r'\s+action=["\'](?:mailto:[^"\']+|https?://(?:www\.)?formsubmit\.co/[^"\']+)["\']',
        "",
        markup,
        flags=re.I,
    )


def upgrade_home(markup: str) -> str:
    safe_title = escape(EXACT_TITLE)
    markup = re.sub(r"<title>.*?</title>", f"<title>{safe_title}</title>", markup, count=1, flags=re.S)
    markup = re.sub(
        r'<meta\s+name=["\']description["\']\s+content=["\'][^"\']*["\']\s*/?>',
        f'<meta name="description" content="{META_DESCRIPTION}">',
        markup,
        count=1,
        flags=re.I,
    )
    markup = re.sub(r"<h1\b[^>]*>.*?</h1>", f"<h1>{safe_title}</h1>", markup, count=1, flags=re.S)
    return markup.replace(">View Automation Suite<", ">Request a Free Audit<", 1)


def process_file(path: Path, root: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    updated = remove_insecure_form_actions(inject_assets(original))
    if path.resolve() == (root / "index.html").resolve():
        updated = upgrade_home(updated)
    if updated == original:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply enterprise website upgrades to generated HTML.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    changed = sum(process_file(path, root) for path in root.rglob("*.html"))
    print(f"Enterprise upgrade applied to {changed} HTML files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
