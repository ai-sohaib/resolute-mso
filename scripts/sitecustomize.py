from __future__ import annotations

import atexit
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "index.html"
_ORIGINAL_WRITE_TEXT = Path.write_text


def _high_density_logo(html: str) -> str:
    html = re.sub(
        r"/assets/img/resolute-mso-logo(?:-\d+)?\.webp",
        "/assets/img/resolute-mso-logo.webp",
        html,
    )
    return re.sub(
        r'(<img\b[^>]*src="/assets/img/resolute-mso-logo\.webp"[^>]*?)\swidth="\d+"\sheight="\d+"',
        r'\1 width="460" height="130"',
        html,
    )


def _guarded_write_text(self: Path, data: str, *args, **kwargs):
    if self.resolve() == INDEX_PATH.resolve() and isinstance(data, str):
        data = _high_density_logo(data)
    return _ORIGINAL_WRITE_TEXT(self, data, *args, **kwargs)


def _externalize_home_css() -> None:
    if not INDEX_PATH.exists():
        return

    text = INDEX_PATH.read_text(encoding="utf-8")
    style_blocks = re.findall(r"<style(?:\s+[^>]*)?>(.*?)</style>", text, flags=re.S)
    if not style_blocks:
        return

    combined = "\n".join(style_blocks)
    combined = re.sub(r"/\*.*?\*/", "", combined, flags=re.S)
    combined = re.sub(r"\s+", " ", combined)
    combined = re.sub(r"\s*([{}:;,])\s*", r"\1", combined).strip()

    css_path = ROOT / "assets" / "css" / "pagespeed-home.css"
    css_path.parent.mkdir(parents=True, exist_ok=True)
    _ORIGINAL_WRITE_TEXT(css_path, combined + "\n", encoding="utf-8")

    text = re.sub(r"\s*<style(?:\s+[^>]*)?>.*?</style>", "", text, flags=re.S)
    text = text.replace(
        "</head>",
        '<link id="resolute-critical-typography" rel="stylesheet" href="/assets/css/pagespeed-home.css"></head>',
        1,
    )
    INDEX_PATH.write_text(_high_density_logo(text), encoding="utf-8")
    print("Externalized homepage CSS and enforced the high-density logo source.")


if sys.argv and sys.argv[0].endswith("apply_pagespeed_100.py"):
    Path.write_text = _guarded_write_text
    atexit.register(_externalize_home_css)
