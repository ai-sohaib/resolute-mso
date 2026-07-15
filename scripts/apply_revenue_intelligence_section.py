from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
CSS_FILES = [
    ROOT / "assets" / "css" / "pagespeed-home.css",
    ROOT / "assets" / "css" / "pagespeed-home-source.css",
]

SECTION_MARKER = 'class="section revenue-intelligence"'
CSS_MARKER = "/* revenue-intelligence-section */"

SECTION_HTML = r'''<section class="section revenue-intelligence" aria-labelledby="revenue-intelligence-title">
  <div class="container">
    <header class="revenue-intelligence__header">
      <p class="revenue-intelligence__brand">Resolute MSO</p>
      <h2 id="revenue-intelligence-title">AI-Driven Revenue Cycle Management</h2>
      <p>Streamline medical billing, accelerate reimbursements, improve claim accuracy, and reduce administrative workload through intelligent revenue cycle automation.</p>
    </header>

    <div class="revenue-intelligence__grid">
      <article class="revenue-card">
        <div class="revenue-card__top">
          <span class="revenue-card__icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h8"/><path d="M14 2v6h6"/><path d="M14 2l6 6v3"/><path d="m15 18 2 2 4-5"/><path d="M8 13h4M8 17h3"/></svg>
          </span>
          <div>
            <h3>Clean Claims</h3>
            <p>AI validates claims before submission to reduce coding errors, eligibility issues, and billing rejections.</p>
          </div>
        </div>
        <ul class="revenue-card__list">
          <li>AI Claim Validation</li>
          <li>Eligibility Verification</li>
          <li>Error Detection</li>
        </ul>
        <div class="revenue-card__metric"><span aria-hidden="true">98.7%</span><strong>98.7% Claim Accuracy</strong></div>
      </article>

      <article class="revenue-card">
        <div class="revenue-card__top">
          <span class="revenue-card__icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none"><path d="M4 20V10h4v10M10 20V4h4v16M16 20v-7h4v7"/><path d="M2 20h20"/></svg>
          </span>
          <div>
            <h3>AR Visibility</h3>
            <p>Gain real-time insight into aging accounts, payer performance, and reimbursement trends.</p>
          </div>
        </div>
        <ul class="revenue-card__list">
          <li>Aging Dashboard</li>
          <li>Payer Tracking</li>
          <li>Collection Analytics</li>
        </ul>
        <div class="revenue-card__metric"><span aria-hidden="true">Live</span><strong>Live Revenue Intelligence</strong></div>
      </article>

      <article class="revenue-card">
        <div class="revenue-card__top">
          <span class="revenue-card__icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-5"/></svg>
          </span>
          <div>
            <h3>Denial Prevention</h3>
            <p>Identify recurring denial patterns, automate root-cause analysis, and prevent repeat claim failures.</p>
          </div>
        </div>
        <ul class="revenue-card__list">
          <li>AI Root Cause Analysis</li>
          <li>Prevention Rules</li>
          <li>Smart Recommendations</li>
        </ul>
        <div class="revenue-card__metric"><span aria-hidden="true">42%</span><strong>42% Fewer Denials</strong></div>
      </article>

      <article class="revenue-card">
        <div class="revenue-card__top">
          <span class="revenue-card__icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none"><path d="M8 8V5a4 4 0 0 1 8 0v3"/><rect x="4" y="8" width="16" height="11" rx="2"/><path d="M8 12h.01M16 12h.01M9 16h6"/><path d="m12 19-1.5 3h3L12 19Z"/></svg>
          </span>
          <div>
            <h3>Intelligent Automation</h3>
            <p>Reduce repetitive administrative work by automating billing workflows, follow-ups, and payment processing.</p>
          </div>
        </div>
        <ul class="revenue-card__list">
          <li>Automated Workflows</li>
          <li>Smart Follow-ups</li>
          <li>Reduced Manual Tasks</li>
        </ul>
        <div class="revenue-card__metric"><span aria-hidden="true">75%</span><strong>75% Faster Processing</strong></div>
      </article>
    </div>

    <div class="revenue-value-bar" aria-label="Revenue cycle benefits">
      <span>Faster Reimbursements</span>
      <span>Higher Claim Acceptance</span>
      <span>Improved Cash Flow</span>
      <span>Reduced Administrative Burden</span>
    </div>
  </div>
</section>'''

SECTION_CSS = r'''
/* revenue-intelligence-section */
.revenue-intelligence{background:#fff;padding:82px 0}.revenue-intelligence__header{max-width:860px;margin:0 auto 42px;text-align:center}.revenue-intelligence__brand{margin:0 0 8px;color:#0c345f;font-size:1.05rem;font-weight:700;letter-spacing:.025em}.revenue-intelligence__header h2{margin:0 0 14px;color:#071f4e;font-size:clamp(2rem,4vw,3rem);letter-spacing:-.035em}.revenue-intelligence__header>p:last-child{max-width:780px;margin:0 auto;color:#59697a;font-size:1.06rem}.revenue-intelligence__grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px}.revenue-card{position:relative;display:flex;min-height:390px;flex-direction:column;overflow:hidden;border:1px solid #dbe3eb;border-radius:18px;background:#fff;padding:32px;box-shadow:0 10px 28px rgba(9,32,70,.07);transition:transform 250ms ease,box-shadow 250ms ease,border-color 250ms ease}.revenue-card::before{content:"";position:absolute;inset:0 0 auto;height:3px;background:#1267d6;transform:scaleX(0);transform-origin:left;transition:transform 250ms ease}.revenue-card:hover,.revenue-card:focus-within{transform:translateY(-7px);border-color:#c2d6ed;box-shadow:0 18px 42px rgba(9,32,70,.13)}.revenue-card:hover::before,.revenue-card:focus-within::before{transform:scaleX(1)}.revenue-card__top{display:grid;grid-template-columns:68px 1fr;gap:20px;align-items:start}.revenue-card__icon{display:grid;width:64px;height:64px;place-items:center;border:1px solid #dce8f5;border-radius:50%;background:#eef5fc;color:#0f55ad;transition:background 250ms ease,color 250ms ease,transform 250ms ease}.revenue-card:hover .revenue-card__icon{background:#dfeeff;color:#08458f;transform:scale(1.04)}.revenue-card__icon svg{width:32px;height:32px;stroke:currentColor;stroke-width:1.75;stroke-linecap:round;stroke-linejoin:round}.revenue-card h3{margin:3px 0 9px;color:#071f4e;font-size:1.34rem}.revenue-card__top p{margin:0;color:#5d6975}.revenue-card__list{display:grid;gap:10px;margin:25px 0 28px;padding:22px 0 0 88px;border-top:1px solid #e1e7ed;list-style:none}.revenue-card__list li{position:relative;color:#263a50;font-weight:600}.revenue-card__list li::before{content:"✓";position:absolute;left:-28px;top:-1px;display:grid;width:18px;height:18px;place-items:center;border:1.5px solid #1267d6;border-radius:50%;color:#1267d6;font-size:.7rem;font-weight:900}.revenue-card__metric{display:flex;align-items:center;gap:13px;margin-top:auto;padding-top:20px;border-top:1px solid #e1e7ed;color:#0d53ad}.revenue-card__metric span{display:grid;min-width:44px;height:34px;padding:0 8px;place-items:center;border:1px solid #d2e1f3;border-radius:999px;background:#f5f9fe;font-size:.75rem;font-weight:800}.revenue-card__metric strong{font-size:1rem}.revenue-value-bar{display:grid;grid-template-columns:repeat(4,1fr);margin-top:28px;border:1px solid #dbe3eb;border-radius:16px;background:#fff;box-shadow:0 8px 24px rgba(9,32,70,.06)}.revenue-value-bar span{position:relative;display:flex;min-height:72px;align-items:center;justify-content:center;padding:18px 22px;color:#173354;font-weight:700;text-align:center}.revenue-value-bar span+span{border-left:1px solid #dbe3eb}.revenue-value-bar span::before{content:"✓";display:grid;width:24px;height:24px;flex:0 0 24px;margin-right:10px;place-items:center;border:1.5px solid #1267d6;border-radius:50%;color:#1267d6;font-size:.78rem;font-weight:900}@media(max-width:900px){.revenue-intelligence__grid{grid-template-columns:1fr}.revenue-card{min-height:0}.revenue-value-bar{grid-template-columns:repeat(2,1fr)}.revenue-value-bar span:nth-child(3){border-left:0;border-top:1px solid #dbe3eb}.revenue-value-bar span:nth-child(4){border-top:1px solid #dbe3eb}}@media(max-width:620px){.revenue-intelligence{padding:58px 0}.revenue-intelligence__header{margin-bottom:30px}.revenue-card{padding:24px;border-radius:16px}.revenue-card__top{grid-template-columns:54px 1fr;gap:15px}.revenue-card__icon{width:52px;height:52px}.revenue-card__icon svg{width:27px;height:27px}.revenue-card__list{padding-left:28px}.revenue-value-bar{grid-template-columns:1fr}.revenue-value-bar span+span{border-left:0;border-top:1px solid #dbe3eb}}@media(prefers-reduced-motion:reduce){.revenue-card,.revenue-card::before,.revenue-card__icon{transition:none}.revenue-card:hover,.revenue-card:focus-within{transform:none}}
'''


def update_index() -> None:
    html = INDEX.read_text(encoding="utf-8")
    if SECTION_MARKER in html:
        print("Revenue intelligence section already present.")
        return

    pattern = re.compile(
        r'<section class="section outcome-strip" aria-label="Revenue cycle operating focus">.*?</section>',
        flags=re.S,
    )
    updated, count = pattern.subn(SECTION_HTML, html, count=1)
    if count != 1:
        raise RuntimeError("Could not find the existing revenue cycle outcome strip.")
    INDEX.write_text(updated, encoding="utf-8")
    print("Replaced the simple outcome strip with the revenue intelligence dashboard section.")


def update_css(path: Path) -> None:
    if not path.exists():
        return
    css = path.read_text(encoding="utf-8")
    if CSS_MARKER in css:
        return
    path.write_text(css.rstrip() + "\n" + SECTION_CSS.strip() + "\n", encoding="utf-8")
    print(f"Added revenue intelligence styles to {path.relative_to(ROOT)}.")


def main() -> None:
    update_index()
    for css_file in CSS_FILES:
        update_css(css_file)


if __name__ == "__main__":
    main()
