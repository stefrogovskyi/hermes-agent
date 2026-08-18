# Case: Hostinger Multi-Environment Deployment & i18n Mirroring

## Symptom
Avalanche Agency dev and staging environments required deployment on Hostinger hosting (`82.29.199.155:65002`) with 8 localized language versions (`/uk/`, `/es/`, etc.) without breaking default English layouts, contact forms, or router navigation.

## Hypothesis vs Fact
- **Hypothesis**: Updating the main English build automatically updates all localized subdirectories.
- **Fact**: Hostinger static directory structures require atomic build uploads per language subfolder, and client-side SPA routing requires `200.html` / `.htaccess` rewrites in each subpath to prevent 404 errors on direct navigation or authentication popups.

## Root Cause
Language subfolders were missing updated HTML build assets and SPA fallback configuration, leading to missing header/footer logos, broken Contact Us email endpoints, and routing 404s on localized routes.

## Fix
1. English `/` root designated as single canonical source of truth for all content updates.
2. Built automated sync script deploying Vite build artifacts to `/` and mirroring transformed localized bundles to all 8 language subfolders.
3. Fixed contact form SMTP target endpoints on dev/staging to direct leads to `dr.reenforce@gmail.com`.
4. Enforced requirement to explicitly print active Git commit SHA and branch name on every build/deployment action.

## Key Lesson / Principle
Always maintain root `/` as single source of truth for multi-language deployments. Validate SPA fallback files (`200.html`) and asset asset paths in every localized subfolder independently before confirming deployment.
