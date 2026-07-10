'use strict';

const fs = require('fs');

const REQUIRED_CATEGORIES = ['performance', 'accessibility', 'best-practices', 'seo'];
const REQUIRED_AGENTIC_AUDITS = ['agent-accessibility-tree', 'cumulative-layout-shift', 'llms-txt'];
const reports = [
  ['MOBILE', JSON.parse(fs.readFileSync('lighthouse-mobile.json', 'utf8'))],
  ['DESKTOP', JSON.parse(fs.readFileSync('lighthouse-desktop.json', 'utf8'))],
];

let failed = false;

function auditPassed(audit) {
  return audit && (audit.score === 1 || audit.scoreDisplayMode === 'notApplicable');
}

for (const [label, report] of reports) {
  console.log(`\n========== ${label} ==========`);

  for (const categoryId of REQUIRED_CATEGORIES) {
    const category = report.categories[categoryId];
    const score = category ? Math.round((category.score || 0) * 100) : 0;
    console.log(`${categoryId}: ${score}`);
    if (score !== 100) failed = true;
  }

  const agentic = report.categories['agentic-browsing'];
  const agenticScore = agentic ? Math.round((agentic.score || 0) * 3) : 0;
  console.log(`agentic-browsing: ${agenticScore}/3`);
  if (!agentic || agentic.score !== 1) failed = true;

  for (const auditId of REQUIRED_AGENTIC_AUDITS) {
    const audit = report.audits[auditId];
    const passed = auditPassed(audit);
    console.log(`${auditId}: ${passed ? 'PASS' : 'FAIL'}${audit && audit.title ? ` — ${audit.title}` : ''}`);
    if (!passed) failed = true;
  }

  const categoryIds = [...REQUIRED_CATEGORIES, 'agentic-browsing'];
  for (const categoryId of categoryIds) {
    const category = report.categories[categoryId];
    if (!category) continue;
    for (const ref of (category.auditRefs || []).filter(item => item.weight > 0)) {
      const audit = report.audits[ref.id];
      if (auditPassed(audit)) continue;
      console.log(`FAIL [${categoryId}] ${ref.id}: ${audit ? audit.title : 'Missing audit'}`);
      if (audit && audit.displayValue) console.log(`  ${audit.displayValue}`);
      const items = audit && audit.details && Array.isArray(audit.details.items)
        ? audit.details.items.slice(0, 15)
        : [];
      for (const item of items) {
        const node = item.node || {};
        const summary = [node.selector, node.snippet, item.url, item.source, item.failureSummary]
          .filter(Boolean)
          .join(' | ')
          .replace(/\s+/g, ' ');
        if (summary) console.log(`  ITEM ${summary}`);
      }
    }
  }
}

if (failed) {
  console.error('\nPerfect PageSpeed gate failed. Required: 100 in all four standard categories and Agentic Browsing 3/3 on mobile and desktop.');
  process.exit(1);
}

console.log('\nPerfect PageSpeed gate passed on mobile and desktop.');
