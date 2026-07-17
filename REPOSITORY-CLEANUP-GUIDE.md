# Resolute MSO - Repository Cleanup Guide

## Overview

This guide outlines the cleanup process for removing unused CSS, JavaScript, images, and assets from the Resolute MSO repository. Execute carefully to avoid breaking existing pages.

## Pre-Cleanup Steps

### 1. Audit Unused Assets

```bash
# Create inventory of all CSS files
grep -r "href.*\.css" . | grep -v node_modules | sort | uniq

# Create inventory of all JS files
grep -r "src.*\.js" . | grep -v node_modules | sort | uniq

# Create inventory of all images
find ./assets/img -type f -name "*.webp" -o -name "*.png" -o -name "*.jpg" | sort
```

### 2. Document Current Usage

Before deleting anything, run searches to confirm usage:

```bash
# Find references to a specific CSS file
grep -r "pagespeed-audit-trigger.css" --include="*.html" --include="*.js"

# Find references to a specific image
grep -r "specific-image.webp" --include="*.html"

# Find references to a specific JS file
grep -r "agentic-readiness.js" --include="*.html"
```

## Current Asset Inventory

### CSS Files to Review

**Active (Keep)**
```
/assets/css/styles.css                  - Base stylesheet
/assets/css/pagespeed-home.css          - Homepage critical CSS
/assets/css/free-audit-modal.css        - Modal dialog
/assets/css/enterprise-product-hero.css - Product hero
/assets/css/enterprise-workflow.css     - Workflow section (NEW)
/assets/css/medcare-footer.css          - Footer
/assets/css/elegant-typography.css      - Typography polish
```

**Candidates for Consolidation** (review first)
```
/assets/css/resolute-authority.css              - Theme overlay?
/assets/css/resolute-minimal-theme.css          - Theme override?
/assets/css/final-qa-fixes.css                  - One-off fixes?
/assets/css/super-upgrade.css                   - Legacy?
/assets/css/iso-ui-polish.css                   - Duplicate polish?
/assets/css/brand-wall-overlay.css              - Specific page?
/assets/css/footer-final-dark.css               - Duplicate footer?
/assets/css/menu-directory-fix.css              - Bug fix?
/assets/css/pagespeed-audit-trigger.css         - Audit-specific?
/assets/css/futuristic-theme.css                - Unused theme?
```

### JavaScript Files to Review

**Active (Keep)**
```
/assets/js/agentic-readiness.js              - Platform functionality
/assets/js/free-audit-modal.js               - Modal behavior
/assets/js/enterprise-product-hero.js        - Hero animations
/assets/js/enterprise-workflow.js            - Workflow animations (NEW)
```

**Candidates for Review**
```
Check /assets/js/ directory for:
- Duplicate functionality
- Abandoned experiments
- Old animation libraries
- Legacy form handlers
```

### Image Files to Review

**Platform Logos** (Keep if referenced)
```
/assets/img/platforms/officeally.webp
/assets/img/platforms/eclinicalworks.webp
/assets/img/platforms/carecloud.webp
/assets/img/platforms/nextgen.webp
/assets/img/platforms/athenahealth.webp
/assets/img/platforms/advancedmd.webp
/assets/img/platforms/modmed.webp
/assets/img/platforms/telcor.webp
```

**Legacy Images** (Review for usage)
```
Search for any unused:
- Placeholder images
- Old screenshots
- Deprecated icons
- Unreferenced backgrounds
```

## Cleanup Process

### Phase 1: CSS Consolidation

**Goal**: Reduce duplicate CSS by consolidating overlapping styles.

1. **Audit Theme Files**
   ```bash
   wc -l /assets/css/resolute-*
   wc -l /assets/css/*-theme.css
   ```

2. **Identify Redundancy**
   - Compare `resolute-minimal-theme.css` vs `resolute-authority.css`
   - Check if multiple files override same selectors
   - Look for duplicate color/spacing rules

3. **Consolidation Strategy**
   - Merge similar theme overrides into base stylesheet
   - Keep only one "polish" CSS file
   - Move page-specific styles to page-specific CSS
   - Update version numbers after consolidation

4. **Testing After Consolidation**
   - Test homepage: visual regression
   - Test 3-4 internal pages: no layout breaks
   - Test mobile responsive: all breakpoints
   - Browser test: Chrome, Firefox, Safari

### Phase 2: JavaScript Cleanup

**Goal**: Remove duplicate or unused JavaScript.

1. **Audit All .js Files**
   ```bash
   grep -rn "window\." /assets/js/*.js
   grep -rn "document\." /assets/js/*.js
   ```

2. **Identify Duplicates**
   - Check for duplicate DOM selectors
   - Look for redundant event listeners
   - Review for copy-paste code

3. **Removal Checklist**
   - ❌ Delete only after confirming no page references it
   - ❌ Test each page that previously loaded the script
   - ✅ Keep scripts actively used by multiple pages
   - ✅ Keep polyfills and shims

4. **Alternative Approach**
   - Rather than delete, move to `/assets/js/archived/`
   - Keep for 3 months recovery period
   - Restore only if reference errors occur

### Phase 3: Image Cleanup

**Goal**: Remove unused images and optimize remaining.

1. **Audit All Images**
   ```bash
   find /assets/img -type f -name "*.webp" -o -name "*.png" -o -name "*.jpg" | wc -l
   ```

2. **Check References**
   - For each image, search entire codebase:
     ```bash
     grep -r "image-name.webp" . --include="*.html" --include="*.js"
     ```

3. **Deletion Candidates**
   - Images with zero references
   - Duplicate resolution versions
   - Old screenshot or demo content
   - Renamed files with legacy versions

4. **Keep Safe Zone**
   - All platform/partner logos
   - Hero images and backgrounds
   - Icons used in SVG/CSS
   - OG images for social

### Phase 4: Unused Styles in HTML

**Goal**: Remove inline and unused CSS classes.

1. **Find Orphaned Classes**
   ```bash
   grep -r "class.*unused" . --include="*.html"
   grep -r "id.*old" . --include="*.html"
   ```

2. **Remove from HTML**
   - Only remove classes that have zero CSS rules
   - Keep classes used for JavaScript selectors
   - Verify no scripts target the class

3. **Clean Data Attributes**
   - Remove unused `data-*` attributes
   - Keep semantic ones (e.g., `data-page`, `data-section`)

## Testing & Validation

### Pre-Cleanup Checklist

- [ ] Create new git branch: `cleanup/phase-1-css`
- [ ] Back up original `/assets/css/` directory
- [ ] Document all files to be modified
- [ ] Run full site screenshot diff test
- [ ] Create PR with changes before merging

### Post-Cleanup Validation

**Visual Testing**
```bash
# Homepage
https://www.resolutemso.com/

# Internal pages (sample 5)
https://www.resolutemso.com/about/
https://www.resolutemso.com/services/
https://www.resolutemso.com/blog/
https://www.resolutemso.com/contact/
https://www.resolutemso.com/chargepilot/

# Mobile view (375px width)
# Tablet view (768px width)
# Desktop view (1400px width)
```

**Automated Testing**
```bash
# Check for broken references
grep -r "href.*\.css" . | grep -v "node_modules" | grep -v "\/" && echo "Found CSS references"

# Check for 404 assets
curl -I https://www.resolutemso.com/assets/css/removed-file.css
```

**Console Validation**
- Open browser DevTools Console
- Look for 404 errors
- Search for "undefined" or "not a function"
- Verify no animation stuttering

## File Deletion Procedures

### Safe Deletion Workflow

**Step 1: Mark for Deletion**
```bash
# Move to archive directory
mkdir -p /assets/css/archived
mkdir -p /assets/js/archived

mv /assets/css/resolute-authority.css /assets/css/archived/
mv /assets/js/old-script.js /assets/js/archived/
```

**Step 2: Update Import References**
```html
<!-- REMOVE from all HTML files -->
<link rel="stylesheet" href="/assets/css/resolute-authority.css">
<script src="/assets/js/old-script.js"></script>
```

**Step 3: Test Full Site**
- Homepage loads without errors
- Check DevTools Network tab for 404s
- Verify all pages render correctly

**Step 4: Git Cleanup**
```bash
# After 30-day archive period, permanently delete
rm -rf /assets/css/archived/
rm -rf /assets/js/archived/
```

## Repository Size Reduction Targets

**Current State** (estimated)
```
/assets/css/    ~150KB (unminified)
/assets/js/     ~100KB (unminified)
/assets/img/    ~500KB
Total: ~750KB
```

**Target State** (after cleanup)
```
/assets/css/    ~80KB (20% reduction)
/assets/js/     ~50KB (20% reduction)
/assets/img/    ~400KB (20% reduction)
Total: ~530KB (25% overall reduction)
```

## Common Cleanup Mistakes

❌ **Don't:**
- Delete CSS without checking all HTML files
- Remove files referenced by third-party analytics
- Delete JavaScript without testing all pages
- Assume unused = safe to delete

✅ **Do:**
- Create git branch before making changes
- Test every page after cleanup
- Keep a backup of removed files
- Document what was removed and why

## Rollback Procedure

If cleanup causes issues:

```bash
# Option 1: Revert git commit
git revert <commit-hash>

# Option 2: Restore from archive
cp /assets/css/archived/*.css /assets/css/
cp /assets/js/archived/*.js /assets/js/

# Option 3: Restore from backup
rsync -av backup/assets/ assets/
```

## Repository Cleanup Timeline

### Week 1-2: Audit Phase
- Inventory all assets
- Document usage
- Create cleanup PR

### Week 3: CSS Consolidation
- Merge duplicate CSS files
- Test all pages
- Deploy to staging

### Week 4: JS & Image Cleanup
- Remove unused JavaScript
- Delete orphaned images
- Archive old files

### Week 5: Final Validation
- Full regression test
- Performance audit
- Deploy to production

## Performance Improvements After Cleanup

**Expected Gains**
- CSS delivery: ~15-20ms faster
- JS parsing: ~10-15ms faster
- Page load: ~5-10% improvement
- Bundle size: ~25% reduction

**Monitoring**
- Set up PageSpeed Insights tracking
- Monitor Core Web Vitals
- Compare before/after metrics

## Future Prevention

**To avoid future cleanup:**

1. **Version Control**
   - Use version numbers on CSS/JS files
   - Remove old versions promptly
   - Document deprecations

2. **Code Review**
   - Check for unused imports in PR reviews
   - Flag duplicate styles
   - Require justification for new files

3. **Tooling**
   - Use CSS unused selectors detection
   - Add to CI/CD pipeline
   - Generate unused asset reports monthly

4. **Documentation**
   - Keep this cleanup guide updated
   - Document why files exist
   - Maintain asset inventory

---

## Cleanup Checklist

- [ ] Phase 1: CSS Consolidation complete
- [ ] Phase 2: JavaScript cleanup complete
- [ ] Phase 3: Image cleanup complete
- [ ] Phase 4: HTML class cleanup complete
- [ ] All pages tested for visual regression
- [ ] Mobile responsive verified
- [ ] Console errors checked
- [ ] Network tab reviewed for 404s
- [ ] Performance metrics validated
- [ ] Git PR reviewed and approved
- [ ] Changes deployed to staging
- [ ] Production rollout scheduled
- [ ] Archive files backed up
- [ ] Cleanup documentation updated
