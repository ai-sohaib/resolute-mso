'use strict';

const fs = require('fs');

const reports = [
  ['MOBILE', JSON.parse(fs.readFileSync('lighthouse-mobile.json', 'utf8'))],
  ['DESKTOP', JSON.parse(fs.readFileSync('lighthouse-desktop.json', 'utf8'))],
];

let failed = false;

for (const [label, report] of reports) {
  console.log(`\n========== ${label} ==========`);
  for (const [id, category] of Object.entries(report.categories)) {
    const score = Math.round((category.score || 0) * 100);
    console.log(`${id}: ${score}`);
    if (score < 100) failed = true;

    for (const ref of category.auditRefs.filter(item => item.weight > 0)) {
      const audit = report.audits[ref.id];
      if (!audit || audit.score === 1 || audit.scoreDisplayMode === 'notApplicable') continue;
      console.log(`FAIL [${id}] ${ref.id}: ${audit.title}`);
      if (audit.displayValue) console.log(`  ${audit.displayValue}`);
      const items = audit.details && Array.isArray(audit.details.items)
        ? audit.details.items.slice(0, 12)
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
  console.error('\nOne or more Lighthouse categories are below 100.');
  process.exit(1);
}
