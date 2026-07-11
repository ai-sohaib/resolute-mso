# Resolute MSO — Clean Replacement Repository

This package contains the final static website, all public pages and assets, the optimized PageSpeed build scripts, the agentic-readiness layer, and one production GitHub Pages deployment workflow.

## Replace the repository

1. Keep the existing restore branch: `restore/pre-psi-agentic-100-2026-07-11`.
2. Delete the current files from the repository `main` branch.
3. Extract this ZIP locally.
4. Upload **the extracted contents**, including the hidden `.github` folder, directly to the root of `main`.
5. Commit the replacement. The workflow `.github/workflows/deploy-pages.yml` will validate and deploy the website.

Do not upload the outer ZIP as a file inside the repository. Upload its extracted contents.
