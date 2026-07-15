from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"

CSS_LINK = '<link rel="stylesheet" href="/assets/css/enterprise-product-hero.css?v=20260715">'
JS_LINK = '<script src="/assets/js/enterprise-product-hero.js?v=20260715" defer></script>'

HERO = r'''<section class="product-hero" aria-labelledby="product-hero-title">
  <div class="container product-hero__grid">
    <div class="product-hero__content">
      <p class="product-hero__eyebrow">
        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 3v18M3 12h18"/></svg>
        AI-Driven Revenue Cycle Management
      </p>
      <h1 id="product-hero-title">Revenue Cycle Intelligence Built for Modern Healthcare</h1>
      <p class="product-hero__copy">Increase reimbursements, reduce denials, automate billing workflows, and improve financial performance through intelligent revenue cycle automation.</p>
      <div class="product-hero__actions" aria-label="Homepage actions">
        <a class="btn" href="/contact/?intent=demo">Book a Live Demo</a>
        <a class="btn btn-secondary" href="/automation-suite/">Explore the Platform</a>
      </div>
      <div class="product-hero__trust" aria-label="Platform trust indicators">
        <span><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-5"/></svg>HIPAA-Conscious Workflows</span>
        <span><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M9 3h6M10 3v3h4V3M7 8h10a3 3 0 0 1 3 3v7a3 3 0 0 1-3 3H7a3 3 0 0 1-3-3v-7a3 3 0 0 1 3-3Z"/><path d="M8 13h.01M16 13h.01M9 17h6"/></svg>AI-Powered Automation</span>
        <span><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3M12 15v2"/></svg>Enterprise Security</span>
        <span><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M3 17 9 11l4 4 8-9"/><path d="M14 6h7v7"/></svg>Faster Reimbursement Workflows</span>
      </div>
    </div>

    <div class="rcm-dashboard" data-rcm-dashboard aria-label="Illustrative Resolute MSO revenue cycle dashboard">
      <div class="rcm-dashboard__topbar">
        <div class="rcm-dashboard__brand"><span class="rcm-dashboard__brand-mark">RMSO</span><span>Revenue Intelligence</span></div>
        <div class="rcm-dashboard__status">Illustrative product view</div>
      </div>
      <div class="rcm-dashboard__body">
        <div class="rcm-dashboard__header">
          <div><h2>Revenue Overview</h2><p>Claims, collections, denials, and operational performance</p></div>
          <span class="rcm-dashboard__range">Last 30 days</span>
        </div>

        <div class="rcm-kpis" aria-label="Revenue cycle key performance indicators">
          <div class="rcm-kpi"><span>Collections</span><strong data-kpi-value="2.48" data-kpi-decimals="2" data-kpi-prefix="$" data-kpi-suffix="M">$2.48M</strong><small>↑ 12.4% period trend</small></div>
          <div class="rcm-kpi"><span>Clean Claim Rate</span><strong data-kpi-value="98.7" data-kpi-decimals="1" data-kpi-suffix="%">98.7%</strong><small>Above operating target</small></div>
          <div class="rcm-kpi"><span>AR Days</span><strong data-kpi-value="31.4" data-kpi-decimals="1">31.4</strong><small>↓ 4.8 days</small></div>
          <div class="rcm-kpi"><span>Denial Rate</span><strong data-kpi-value="4.2" data-kpi-decimals="1" data-kpi-suffix="%">4.2%</strong><small>↓ 1.6% period trend</small></div>
        </div>

        <div class="rcm-dashboard__main">
          <section class="rcm-panel" aria-label="Payment trends">
            <div class="rcm-panel__title">Payment Trends <span>Weekly collections</span></div>
            <div class="payment-chart" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
            <div class="chart-legend" aria-hidden="true"><span>W1</span><span>W2</span><span>W3</span><span>W4</span><span>W5</span><span>W6</span><span>W7</span><span>W8</span></div>
          </section>
          <section class="rcm-panel" aria-label="Claims processing status">
            <div class="rcm-panel__title">Claims Status <span>Current queue</span></div>
            <div class="claim-status">
              <div class="claim-status__row"><span>Accepted</span><strong>86%</strong><div class="claim-status__bar"><i></i></div></div>
              <div class="claim-status__row"><span>Processing</span><strong>9%</strong><div class="claim-status__bar"><i></i></div></div>
              <div class="claim-status__row"><span>Exceptions</span><strong>5%</strong><div class="claim-status__bar"><i></i></div></div>
            </div>
          </section>
        </div>

        <div class="rcm-dashboard__lower">
          <section class="rcm-panel" aria-label="Accounts receivable aging">
            <div class="rcm-panel__title">AR Aging <span>Open balance</span></div>
            <div class="aging-grid"><div><span>0–30</span><strong>62%</strong></div><div><span>31–60</span><strong>21%</strong></div><div><span>61–90</span><strong>10%</strong></div><div><span>90+</span><strong>7%</strong></div></div>
          </section>
          <section class="rcm-panel" aria-label="AI recommendations">
            <div class="rcm-panel__title">AI Recommendations <span>Next actions</span></div>
            <div class="ai-recommendations">
              <div class="ai-recommendation"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 3v18M3 12h18"/></svg><div><strong>Prioritize high-value payer follow-up</strong><span>18 claims exceed the current aging threshold.</span></div></div>
              <div class="ai-recommendation"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="m5 12 4 4L19 6"/></svg><div><strong>Apply eligibility prevention rule</strong><span>Recurring front-end errors detected in one workflow.</span></div></div>
            </div>
          </section>
        </div>

        <div class="rcm-dashboard__footer" aria-label="Operational KPIs">
          <div class="rcm-mini-kpi"><span>First-Pass Yield</span><strong>96.3%</strong></div>
          <div class="rcm-mini-kpi"><span>Automation Coverage</span><strong>74%</strong></div>
          <div class="rcm-mini-kpi"><span>Action Queue SLA</span><strong>1.8 days</strong></div>
        </div>
      </div>
    </div>
  </div>
</section>'''


def replace_hero(html: str) -> str:
    patterns = (
        r'<section class="hero home-hero">.*?</section>',
        r'<section class="r-hero home-hero">.*?</section>',
        r'<section class="product-hero".*?</section>',
    )
    for pattern in patterns:
        updated, count = re.subn(pattern, HERO, html, count=1, flags=re.S)
        if count:
            return updated
    raise RuntimeError("Could not locate a supported homepage hero section.")


def main() -> None:
    html = INDEX.read_text(encoding="utf-8")
    html = replace_hero(html)

    html = re.sub(r'\s*<link rel="stylesheet" href="/assets/css/enterprise-product-hero\.css[^\"]*">', "", html)
    html = re.sub(r'\s*<script src="/assets/js/enterprise-product-hero\.js[^\"]*" defer></script>', "", html)

    if CSS_LINK not in html:
        html = html.replace("</head>", f"  {CSS_LINK}\n</head>", 1)
    if JS_LINK not in html:
        html = html.replace("</body>", f"  {JS_LINK}\n</body>", 1)

    if "healthcare-hero-ai" in html:
        raise RuntimeError("Legacy doctor-image hero references remain in index.html.")
    if html.count('href="/assets/css/pagespeed-home.css"') > 1:
        first = True
        def dedupe(match: re.Match[str]) -> str:
            nonlocal first
            if first:
                first = False
                return match.group(0)
            return ""
        html = re.sub(r'<link[^>]+href="/assets/css/pagespeed-home\.css"[^>]*>', dedupe, html)

    required = (
        "Revenue Cycle Intelligence Built for Modern Healthcare",
        "Book a Live Demo",
        "Explore the Platform",
        "data-rcm-dashboard",
        "AI Recommendations",
        "Accounts receivable aging",
    )
    missing = [value for value in required if value not in html]
    if missing:
        raise RuntimeError(f"Hero validation failed: {missing}")

    INDEX.write_text(html, encoding="utf-8")
    print("Enterprise product hero applied to index.html.")


if __name__ == "__main__":
    main()
