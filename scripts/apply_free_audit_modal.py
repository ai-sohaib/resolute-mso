from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"

MODAL_MARKUP = '''
  <section class="audit-modal" id="free-audit-modal" role="dialog" aria-modal="true" aria-labelledby="free-audit-title" hidden>
    <button class="audit-modal__backdrop" type="button" data-close-free-audit aria-label="Close Free RCM Audit form"></button>
    <div class="audit-modal__dialog">
      <button class="audit-modal__close" type="button" data-close-free-audit aria-label="Close dialog">&times;</button>
      <p class="audit-modal__kicker">Free RCM Audit</p>
      <h2 id="free-audit-title">Request your free RCM audit</h2>
      <p class="audit-modal__intro">Share your contact details and a Resolute MSO specialist will follow up about your revenue cycle audit.</p>
      <form class="audit-form" id="free-audit-form" novalidate>
        <input type="hidden" name="_subject" value="New Free RCM Audit Request — Resolute MSO">
        <input type="hidden" name="_template" value="table">
        <input type="hidden" name="_captcha" value="false">
        <input type="hidden" name="source" value="Homepage Free RCM Audit Popup">
        <label class="audit-honeypot" aria-hidden="true">Leave this field empty<input name="_honey" type="text" tabindex="-1" autocomplete="off"></label>
        <label>Name<input name="name" type="text" autocomplete="name" required maxlength="100"></label>
        <label>Phone<input name="phone" type="tel" autocomplete="tel" required maxlength="30" inputmode="tel"></label>
        <label>Email<input name="email" type="email" autocomplete="email" required maxlength="160"></label>
        <button class="btn" type="submit">Send Request</button>
        <p class="audit-form__status" role="status" aria-live="polite"></p>
      </form>
      <p class="audit-modal__privacy">Business inquiries only. Do not submit PHI or patient information.</p>
    </div>
  </section>
'''


def main() -> None:
    html = INDEX.read_text(encoding="utf-8")

    html = html.replace(
        '<a class="btn btn-secondary" href="/automation-suite/">View Automation Suite</a>',
        '<button class="btn btn-secondary" type="button" data-open-free-audit>Get Free RCM Audit</button>',
        1,
    )

    if '/assets/css/free-audit-modal.css' not in html:
        html = html.replace(
            '</head>',
            '  <link rel="stylesheet" href="/assets/css/free-audit-modal.css">\n</head>',
            1,
        )

    if 'id="free-audit-modal"' not in html:
        marker = '  <div class="floating-tools" role="group" aria-label="Quick contact tools">'
        if marker not in html:
            raise RuntimeError('Could not locate floating tools insertion point.')
        html = html.replace(marker, MODAL_MARKUP + '\n' + marker, 1)

    if '/config.js' not in html:
        html = html.replace(
            '</body>',
            '  <script src="/config.js"></script>\n  <script src="/assets/js/free-audit-modal.js" defer></script>\n</body>',
            1,
        )
    elif '/assets/js/free-audit-modal.js' not in html:
        html = html.replace(
            '</body>',
            '  <script src="/assets/js/free-audit-modal.js" defer></script>\n</body>',
            1,
        )

    required = [
        'data-open-free-audit',
        'id="free-audit-modal"',
        'name="phone"',
        'name="email"',
        '/assets/css/free-audit-modal.css',
        '/assets/js/free-audit-modal.js',
        '/config.js',
    ]
    for needle in required:
        if needle not in html:
            raise RuntimeError(f'Missing required audit modal marker: {needle}')

    INDEX.write_text(html, encoding="utf-8")
    print('Free RCM Audit CTA and modal applied to homepage.')


if __name__ == '__main__':
    main()
