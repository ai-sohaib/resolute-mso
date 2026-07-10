'use strict';

const fs = require('fs');
const puppeteer = require('puppeteer-core');

function summarize(report, label) {
  const lines = [`===== ${label} LIGHTHOUSE =====`];
  for (const [categoryId, category] of Object.entries(report.categories || {})) {
    lines.push(`${categoryId}: ${Math.round((category.score || 0) * 100)}`);
    for (const ref of (category.auditRefs || []).filter(item => item.weight > 0)) {
      const audit = report.audits[ref.id];
      if (!audit || audit.score === 1 || audit.scoreDisplayMode === 'notApplicable') continue;
      lines.push(`FAIL [${categoryId}] ${ref.id}: ${audit.title}`);
      if (audit.displayValue) lines.push(`  ${audit.displayValue}`);
      if (audit.description) lines.push(`  ${audit.description.replace(/\s+/g, ' ')}`);
      const items = audit.details && Array.isArray(audit.details.items)
        ? audit.details.items.slice(0, 20)
        : [];
      for (const item of items) {
        const node = item.node || {};
        const text = [
          node.selector,
          node.snippet,
          node.nodeLabel,
          item.url,
          item.source,
          item.failureSummary,
          item.warning,
        ].filter(Boolean).join(' | ').replace(/\s+/g, ' ');
        if (text) lines.push(`  ITEM ${text}`);
      }
    }
  }

  const consoleErrors = report.audits && report.audits['errors-in-console'];
  if (consoleErrors && consoleErrors.details && Array.isArray(consoleErrors.details.items)) {
    lines.push('===== CONSOLE ERRORS =====');
    for (const item of consoleErrors.details.items) {
      lines.push(JSON.stringify(item));
    }
  }
  return lines.join('\n');
}

async function clickText(page, text) {
  return page.evaluate((target) => {
    const candidates = Array.from(document.querySelectorAll('button, a, [role="button"], [role="tab"]'));
    const match = candidates.find(el => (el.innerText || el.textContent || '').trim().includes(target));
    if (!match) return false;
    match.click();
    return true;
  }, text);
}

async function scrapePsi(strategy) {
  const browser = await puppeteer.launch({
    executablePath: process.env.CHROME_PATH || '/usr/bin/google-chrome',
    headless: true,
    args: ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu'],
  });
  const page = await browser.newPage();
  await page.setViewport(strategy === 'mobile'
    ? { width: 412, height: 915, deviceScaleFactor: 1 }
    : { width: 1440, height: 1000, deviceScaleFactor: 1 });
  const target = `https://pagespeed.web.dev/analysis?url=${encodeURIComponent('https://resolutemso.com/')}&form_factor=${strategy}`;
  await page.goto(target, { waitUntil: 'networkidle2', timeout: 180000 });
  await page.waitForFunction(() => document.body && document.body.innerText.includes('Diagnose performance issues'), { timeout: 180000 });
  await page.screenshot({ path: `psi-${strategy}.png`, fullPage: true });
  fs.writeFileSync(`psi-${strategy}-initial.txt`, await page.evaluate(() => document.body.innerText));

  for (const section of ['Best Practices', 'Agentic Browsing']) {
    const clicked = await clickText(page, section);
    await new Promise(resolve => setTimeout(resolve, 1800));
    const slug = section.toLowerCase().replace(/\s+/g, '-');
    fs.writeFileSync(`psi-${strategy}-${slug}.txt`, await page.evaluate(() => document.body.innerText));
    await page.screenshot({ path: `psi-${strategy}-${slug}.png`, fullPage: true });
    console.log(`${strategy}: clicked ${section}: ${clicked}`);
  }
  await browser.close();
}

(async () => {
  const mobile = JSON.parse(fs.readFileSync('live-mobile.json', 'utf8'));
  const desktop = JSON.parse(fs.readFileSync('live-desktop.json', 'utf8'));
  const report = `${summarize(mobile, 'MOBILE')}\n\n${summarize(desktop, 'DESKTOP')}\n`;
  fs.writeFileSync('live-pagespeed-diagnostics.txt', report);
  console.log(report);
  await scrapePsi('mobile');
  await scrapePsi('desktop');
})().catch(error => {
  console.error(error);
  process.exit(1);
});
