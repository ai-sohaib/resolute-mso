from __future__ import annotations

import atexit
import re
import sys
from pathlib import Path


def _finalize_pagespeed_home() -> None:
    if not sys.argv or not sys.argv[0].endswith("apply_pagespeed_100.py"):
        return

    root = Path(__file__).resolve().parents[1]
    index_path = root / "index.html"
    if not index_path.exists():
        return

    text = index_path.read_text(encoding="utf-8")
    style_blocks = re.findall(r"<style(?:\s+[^>]*)?>(.*?)</style>", text, flags=re.S)
    if not style_blocks:
        return

    combined = "\n".join(style_blocks)
    combined = re.sub(r"/\*.*?\*/", "", combined, flags=re.S)
    combined = re.sub(r"\s+", " ", combined)
    combined = re.sub(r"\s*([{}:;,])\s*", r"\1", combined).strip()

    css_path = root / "assets" / "css" / "pagespeed-home.css"
    css_path.parent.mkdir(parents=True, exist_ok=True)
    css_path.write_text(combined + "\n", encoding="utf-8")

    text = re.sub(r"\s*<style(?:\s+[^>]*)?>.*?</style>", "", text, flags=re.S)
    text = text.replace(
        "</head>",
        '<link id="resolute-critical-typography" rel="stylesheet" href="/assets/css/pagespeed-home.css"></head>',
        1,
    )

    original_logo = root / "assets" / "img" / "resolute-mso-logo.webp"
    optimized_logo = root / "assets" / "img" / "resolute-mso-logo-460.webp"
    if original_logo.exists():
        from PIL import Image

        with Image.open(original_logo) as image:
            image.load()
            if image.mode not in {"RGB", "RGBA"}:
                image = image.convert("RGBA" if "transparency" in image.info else "RGB")
            image.save(optimized_logo, format="WEBP", quality=58, method=6)

        text = text.replace(
            "/assets/img/resolute-mso-logo-208.webp",
            "/assets/img/resolute-mso-logo-460.webp",
        )
        text = re.sub(
            r'(<img\b[^>]*src="/assets/img/resolute-mso-logo-460\.webp"[^>]*?)\swidth="\d+"\sheight="\d+"',
            r'\1 width="460" height="130"',
            text,
        )

    index_path.write_text(text, encoding="utf-8")
    print("Externalized homepage CSS and supplied a high-density optimized logo.")


if sys.argv and sys.argv[0].endswith("apply_pagespeed_100.py"):
    atexit.register(_finalize_pagespeed_home)
