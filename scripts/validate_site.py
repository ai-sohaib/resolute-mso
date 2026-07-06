from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE = "https://www.resolutemso.com"


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.in_title = False
        self.meta_description = ""
        self.canonical = ""
        self.robots = ""
        self.h1_count = 0
        self.links: list[str] = []
        self.images: list[str] = []
        self.forms = 0
        self.text_chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {k.lower(): v or "" for k, v in attrs}
        if tag == "title":
            self.in_title = True
        if tag == "meta" and data.get("name", "").lower() == "description":
            self.meta_description = data.get("content", "")
        if tag == "meta" and data.get("name", "").lower() == "robots":
            self.robots = data.get("content", "")
        if tag == "link" and data.get("rel") == "canonical":
            self.canonical = data.get("href", "")
        if tag == "h1":
            self.h1_count += 1
        if tag == "a" and data.get("href"):
            self.links.append(data["href"])
        if tag == "img" and data.get("src"):
            self.images.append(data["src"])
        if tag == "form":
            self.forms += 1

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title += data
        self.text_chunks.append(data)

    @property
    def text(self) -> str:
        return " ".join(chunk.strip() for chunk in self.text_chunks if chunk.strip())


def local_path_from_url(url: str) -> Path | None:
    if url.startswith("mailto:") or url.startswith("tel:") or url.startswith("sms:"):
        return None
    if url.startswith("https://wa.me") or url.startswith("https://www.linkedin.com") or url.startswith("https://formsubmit.co"):
        return None
    if url.startswith(SITE):
        url = url[len(SITE):]
    if url.startswith("http://") or url.startswith("https://"):
        return None
    url = url.split("#", 1)[0].split("?", 1)[0]
    if not url:
        return None
    if url == "/":
        return ROOT / "index.html"
    if url.startswith("/"):
        path = ROOT / url.lstrip("/")
        if url.endswith("/"):
            return path / "index.html"
        if path.is_dir():
            return path / "index.html"
        return path
    return ROOT / url


def main() -> int:
    failures: list[str] = []
    html_files = sorted(
        p for p in ROOT.rglob("*.html")
        if ".git" not in p.parts and p.name != "thank-you.html"
    )
    titles: dict[str, str] = {}
    indexable_count = 0

    for path in html_files:
        parser = PageParser()
        parser.feed(path.read_text(encoding="utf-8"))
        rel = path.relative_to(ROOT).as_posix()
        if parser.robots and "noindex" not in parser.robots:
            indexable_count += 1
        if not parser.title:
            failures.append(f"{rel}: missing title")
        if parser.title == "Home | Resolute MSO":
            failures.append(f"{rel}: generic Home title")
        if parser.title in titles and "noindex" not in parser.robots:
            failures.append(f"{rel}: duplicate title with {titles[parser.title]} -> {parser.title}")
        titles[parser.title] = rel
        if "noindex" not in parser.robots:
            if not parser.meta_description:
                failures.append(f"{rel}: missing meta description")
            if not parser.canonical:
                failures.append(f"{rel}: missing canonical")
            if parser.h1_count != 1:
                failures.append(f"{rel}: expected one H1, found {parser.h1_count}")
        if parser.forms and "Do not submit PHI" not in parser.text:
            failures.append(f"{rel}: form missing PHI warning text")
        for href in parser.links:
            target = local_path_from_url(href)
            if target and not target.exists():
                failures.append(f"{rel}: broken link {href}")
        for src in parser.images:
            target = local_path_from_url(src)
            if target and not target.exists():
                failures.append(f"{rel}: broken image {src}")

    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    sitemap_urls = re.findall(r"<loc>(.*?)</loc>", sitemap)
    if indexable_count < 100:
        failures.append(f"indexable page count below requirement: {indexable_count}")
    if len(sitemap_urls) < 100:
        failures.append(f"sitemap URL count below requirement: {len(sitemap_urls)}")
    for url in sitemap_urls:
        target = local_path_from_url(url)
        if target and not target.exists():
            failures.append(f"sitemap broken URL {url}")
    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    if f"Sitemap: {SITE}/sitemap.xml" not in robots:
        failures.append("robots.txt missing sitemap")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    for needle in ["Resolute MSO", "ChargePilot", "OfficeAlly", "medical billing automation"]:
        if needle not in llms:
            failures.append(f"llms.txt missing {needle}")

    report = [
        "# Preview QA Report",
        "",
        f"HTML files checked: {len(html_files)}",
        f"Indexable pages: {indexable_count}",
        f"Sitemap URLs: {len(sitemap_urls)}",
        "",
    ]
    if failures:
        report.append("## Failures")
        report.extend(f"- {failure}" for failure in failures)
    else:
        report.append("## Result")
        report.append("No validation failures found.")
    (ROOT / "PREVIEW_QA_REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    if failures:
        print("\n".join(failures))
        return 1
    print(f"Validation passed: {indexable_count} indexable pages, {len(sitemap_urls)} sitemap URLs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
