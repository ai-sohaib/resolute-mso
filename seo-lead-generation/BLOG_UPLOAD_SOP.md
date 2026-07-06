# Resolute MSO Blog Upload SOP for GitHub Pages

## Step 1: Create new blog HTML page
Copy an existing blog page, for example:

`blog-clean-claim-playbook.html`

Rename it using lowercase hyphen format, for example:

`blog-eligibility-verification-denials.html`

## Step 2: Update SEO fields
Update:
- `<title>`
- `<meta name="description">`
- canonical URL
- Open Graph title/description/URL
- Twitter title/description
- H1
- Article date
- Image alt text

## Step 3: Update article content
Recommended structure:
- H1
- Short intro
- Problem section
- Why it matters
- Common causes
- Recommended workflow
- How Resolute MSO helps
- FAQ
- CTA

## Step 4: Add article to blog.html
Add a new card linking to the article.

## Step 5: Add article to resources.html if it is a major guide
Only add important articles to resources page.

## Step 6: Update sitemap.xml
Add:

```xml
<url>
  <loc>https://www.resolutemso.com/NEW-ARTICLE.html</loc>
  <lastmod>2026-06-30</lastmod>
</url>
```

## Step 7: Update llms.txt
Add the new article link under Educational Resources.

## Step 8: Commit to GitHub
Commit directly to main branch.

## Step 9: Request indexing
Google Search Console → URL Inspection → Request Indexing.
Bing Webmaster Tools → URL Inspection → Request Indexing.

## Step 10: Promote
Create:
- 1 LinkedIn post
- 1 LinkedIn carousel idea
- 1 email bulletin
- 1 direct outreach message
