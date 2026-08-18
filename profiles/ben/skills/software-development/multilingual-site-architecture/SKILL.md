---
name: multilingual-site-architecture
description: Sync and deploy multi-language static web ecosystems.
version: 1.0.0
author: Ben Jett
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [web, localization, i18n, static-site, seo, navigation, deployment]
---

# Multilingual Static Site Architecture & Synchronization

## When to Use

Use this skill when managing, generating, or updating large-scale multi-language static websites (e.g. 8+ language subdirectories, 100+ HTML files) where navigation headers, dropdown menus, footer columns, and SEO metadata must remain strictly synchronized across all locales.

## Core Architecture Principles

1. **Root + Language Subtree Structure:**
   - Primary locale (`en`) sits at root (`/` or `/dev/`).
   - Secondary locales sit in dedicated subdirectories (`/ru/`, `/uk/`, `/de/`, `/es/`, `/fr/`, `/it/`, `/ar/`, `/zh/`).
   - Clean extensionless URLs (`/services`, `/marketing`, `/ru/marketing`) handled via `.htaccess` rewrites.

2. **Modular Component Generation:**
   - Never edit 100+ files by hand. Use a Python script with structured dictionaries for translations and shared component templates.
   - Maintain isolated dictionary maps for top navigation, mobile drawers, dropdowns, and footers.
   - Keep interactive JavaScript (dropdown handlers, auth check, language router) modular and cleanly injected before `</body>`.

3. **Dev vs. Production Staging Discipline:**
   - Perform all modifications and initial tests on the `/dev/` environment.
   - Run automated HTTP 200 checks across multiple language routes prior to prod synchronization.
   - When deploying to prod, exclude staging-specific paths, kanban state files, and environment `.htaccess`.

4. **Dropdown Navigation & Category Hub UX:**
   - When converting a top navigation item (e.g. "Services") into a dropdown menu with sub-solutions, **do not** add a redundant "All Services" item.
   - Keep the parent menu label as a direct, clickable link to the main hub page (`<a href="services">Services</a>`), while allowing hover (`:hover`) or clicking the arrow `▼` to open the dropdown list of sub-solutions.
   - Mobile drawers should list the parent hub link (`Services ➔`) at the top, followed by indented sub-solution links.

5. **Precise Card CTA Updates & Content Safety:**
   - When updating call-to-action buttons on service/solution cards (e.g. adding "Learn More ↗" next to "Get Started ➔"), target strictly the anchor tag/CTA container rather than using broad regex replacements that risk truncating in-depth card text, tables, or FAQs.
   - Always verify page file size and structure before and after batch replacements to ensure zero content regression.

6. **Global Styling & Color Token Management:**
   - When updating brand colors across multi-page sites (e.g. converting royal/electric blues to brand sky blue `#5FB3F9`), parse full color histograms first.
   - Protect national SVG flag colors in language switchers (`#012169`, `#C8102E`, `#002395`, `#DE2910`, etc.) from broad find-and-replace scripts.
   - Ensure high text contrast on light/sky-blue button backgrounds (use `#0F172A` dark slate or heavy bold text).

7. **Resilient Language Routing on Staging/Dev Environments & Subdomains:**
   - When building client-side language switchers (`navigateToLang`), check both hostname and pathname: if the dev environment is accessed via a dedicated subdomain (e.g. `dev.example.com`), the document root is already the staging folder, so no `/dev` prefix should be injected into the URL.
   - If accessed via path (e.g. `example.com/dev/`), isolate `/dev` before extracting clean page slugs to prevent URL inversion like `/de/dev/contact`.
   - Standard implementation:
     ```javascript
     function navigateToLang(targetLang) {
       var host = window.location.hostname;
       var path = window.location.pathname;
       var isSubdomainDev = (host === 'dev.example.com');
       var isPathDev = (path.indexOf('/dev') === 0);
       
       var prefix = (!isSubdomainDev && isPathDev) ? '/dev' : '';
       var cleanPath = (!isSubdomainDev && isPathDev) ? path.substring(4) : path;
       
       var knownLangs = ['es', 'de', 'fr', 'it', 'uk', 'ru', 'zh', 'ar'];
       var parts = cleanPath.split('/').filter(Boolean);
       var pageParts = parts.filter(function(p) {
         return knownLangs.indexOf(p) === -1 && p !== 'dev' && p !== 'staging';
       });
       var page = pageParts.join('/').replace(/\.html$/, '');
       if (page === 'index') page = '';
       if (targetLang === 'en') {
         window.location.href = prefix + (page ? '/' + page : '/');
       } else {
         window.location.href = prefix + '/' + targetLang + (page ? '/' + page : '/');
       }
     }
     ```

8. **Dual-Access `.htaccess` Configuration (Subdomain vs. Path-Based Staging):**
   - When staging can be served both as a subfolder (`example.com/dev/`) and a subdomain (`dev.example.com`), **never** hardcode `RewriteBase /dev/<lang>/` in language subfolder `.htaccess` files. That breaks routing with 404 errors on the subdomain where the document root is already `/dev/`.
   - Use relative, directory-level rewrite rules without hardcoded path prefixes:
     ```apache
     DirectoryIndex index.html index.php
     ErrorDocument 404 /404.html

     <IfModule mod_rewrite.c>
         RewriteEngine On
         RewriteRule ^index(\.html)?$ ./ [R=301,L]
         RewriteCond %{REQUEST_FILENAME} !-f
         RewriteCond %{REQUEST_FILENAME} !-d
         RewriteCond %{REQUEST_FILENAME}.html -f
         RewriteRule ^([^/]+)/?$ $1.html [L,QSA]
     </IfModule>
     ```

9. **Localization Purity (Zero English Parenthetical Artifacts):**
   - In multilingual navigation, headers, and footer column titles, never append source English labels in parentheses (e.g. `Рішення (Solutions)` ❌, `Company (Компания)` ❌, `Legal (قانوني)` ❌).
   - Keep translations purely native, concise, and professional across all target languages (`Рішення` ✅, `Компания` ✅, `قانوني` ✅).

10. **Brand Logo Routing & Subdomain 404 Prevention:**
    - On static sites served across both subdomains (`dev.example.com`) and subfolders (`example.com/dev/`), never hardcode `href="/dev/"` or `href="/dev/<lang>/"` on the brand logo. On a subdomain, that creates an invalid route (`dev.example.com/dev/`) resulting in a 404.
    - Attach an inline click handler that resolves the root correctly:
      ```javascript
      function handleBrandLogoClick(e, lang) {
        if (e) e.preventDefault();
        var host = window.location.hostname;
        var path = window.location.pathname;
        var isSubdomainDev = (host === 'dev.example.com');
        var isPathDev = (path.indexOf('/dev') === 0);
        var prefix = (!isSubdomainDev && isPathDev) ? '/dev' : '';
        var target = prefix + (lang && lang !== 'en' ? '/' + lang + '/' : '/');
        window.location.href = target;
      }
      ```
    - Additionally, include a protective safety redirect in root `.htaccess` using strict slash boundaries to avoid prefix collisions (e.g. matching `/development` as `/dev`):
      ```apache
      # Strip redundant /dev prefix on subdomain without colliding with /development
      RewriteCond %{HTTP_HOST} ^dev\.example\.com$ [NC]
      RewriteRule ^dev/?$ / [R=301,L]

      RewriteCond %{HTTP_HOST} ^dev\.example\.com$ [NC]
      RewriteRule ^dev/(.+)$ /$1 [R=301,L]
      ```

11. **Prefix Collision Pitfall in Rewrite Rules & Cache Self-Healing:**
    - When stripping folder prefixes on subdomains, never use unbounded regexes like `^/dev(.*)$` or `^dev.*`. That matches any page starting with those letters (e.g. `/development` gets stripped to `/elopment`, resulting in a 404). Always require an explicit slash or end of string.
    - If a flawed 301 redirect was previously served and cached by browsers (e.g. `/elopment`), add a self-healing forward rule in `.htaccess` (`RewriteRule ^elopment/?(.*)$ /development$1 [R=301,L]`) to recover all cached client sessions.

12. **Dynamic Active Language Flag Rendering:**
    - When generating the `#lang-btn` selector component across static localized pages, ensure the button's rendered SVG flag dynamically reflects the current page's locale (e.g. 🇩🇪 for `/de/`, 🇺🇦 for `/uk/`, 🇷🇺 for `/ru/`, 🇪🇸 for `/es/`, 🇫🇷 for `/fr/`, 🇮🇹 for `/it/`, 🇨🇳 for `/zh/`, 🇦🇪 for `/ar/`, 🇬🇧 for `/en/`), rather than leaving a hardcoded default flag across all templates.

13. **Non-Destructive Staging Discipline:**
    - Never perform blanket overwrites, bulk file deletions, or blind rollbacks of the dev environment. Always isolate specific regressions and perform targeted, verified fixes.

14. **Google Identity Services (GIS) & OAuth Integration Across Multilingual Static Pages:**
    - When implementing official Google Sign-In on static/PHP web apps, load the official GIS client (`<script src="https://accounts.google.com/gsi/client" async defer></script>`) on all localized login pages.
    - Initialize `google.accounts.id.initialize` with the Client ID and provide a callback `handleGoogleCredentialResponse(response)` that posts `response.credential` (JWT) to `auth.php`.
    - On the backend (`auth.php`), verify the token with Google's endpoint:
      `https://oauth2.googleapis.com/tokeninfo?id_token=` . urlencode($credential)
    - Validate `aud === $GOOGLE_CLIENT_ID` and extract verified user details (`email`, `name`, `picture`, `email_verified`).
    - After successful authentication, preserve the user's active language by redirecting to `/<lang>/dashboard` (or `/dashboard` for English).

## Synchronization Workflow

1. **Define Dictionaries & Slugs:**
   Create a centralized mapping of all navigation labels, page slugs, SEO titles, and meta descriptions per locale.

2. **Automated Batch Scripting:**
   - Iterate through `base_dir` and each language subdirectory.
   - Generate dedicated solution pages with localized H1, badges, value pillars, and CTA sections.
   - Replace `<nav ... </nav>` and `<footer ... </footer>` tags with localized versions.
   - Ensure dynamic JavaScript (e.g. `toggleSolutionsDropdown`, `toggleCompanyDropdown`, `navigateToLang`) is present across all files.

3. **Routing Verification:**
   Verify clean URLs on server using `urllib.request` or `curl`:
   ```bash
   python3 -c "import urllib.request; [print(urllib.request.urlopen('https://example.com/dev/' + path).status) for path in ['marketing', 'ru/marketing', 'de/infrastructure']]"
   ```
