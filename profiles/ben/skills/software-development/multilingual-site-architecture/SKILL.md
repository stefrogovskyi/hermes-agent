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

15. **Interactive AI Sales Rep Widget & Lead-Capture Ecosystem:**
    - Deploy a lightweight, standalone JS widget (`ai-widget.js`) injected across all pages before `</body>` to provide instant 24/7 client discovery and live sales qualification.
    - Incorporate interactive elements: pulsing online status badge, conversational quick-reply pills, simulated typing indicators, and markdown formatting for readability.
    - Backend handling (`auth.php?action=ai_chat`): parse incoming user messages, detect contact handles (Telegram `@username`, email, phone numbers), log qualified leads into the database/CRM, and trigger team alerts.
    - Ecosystem cross-linking: highlight the live widget via prominent showcase cards on category hub pages (e.g. `ai-agents`) linking directly to dedicated conversion landing pages (e.g. `ai-sales-agent`).

16. **Consistent Standalone Page Navbar CSS & Responsive Drawer Injections:**
    - When generating standalone child landing pages (such as `/ai-sales-agent`), do not rely solely on body inline styles. Ensure the standard site-wide navigation `<style>` blocks (`#mobile-responsive-system`, `.services-nav-item:hover #services-dropdown-menu`, `.company-dropdown-container:hover #company-dropdown-menu`, `.mobile-menu-btn`, `.mobile-nav-drawer`) are fully included in the `<head>` or before `</body>`.
    - This guarantees that top navigation, dropdowns, and responsive mobile drawers render with 100% visual fidelity across both light-themed and dark-themed pages.

17. **Bulletproof Dropdown Hover Bridge & Event Propagation Pitfalls:**
    - When building hover dropdown menus (like language selectors `#lang-menu`, solutions `#services-dropdown-menu`, company `#company-dropdown-menu`), avoid placing the dropdown list with an empty gap (e.g. `top: 46px` when the button is `34px` high). Moving the cursor down crosses that 10px empty space, causing the browser to immediately lose `:hover` and close the menu.
    - Solution:
      1. Position with `top: calc(100% + 4px);` relative to an inline container (`.lang-dropdown-container`).
      2. Attach an invisible `::before` pseudo-element bridge spanning `top: -14px; height: 18px;` over the gap so the mouse never leaves the hover bounding box while transitioning into the menu:
         ```css
         #lang-menu::before, #services-dropdown-menu::before, #company-dropdown-menu::before {
           content: "";
           position: absolute;
           top: -14px; left: -10px; right: -10px; height: 18px; background: transparent; z-index: 1999;
         }
         ```
      3. In click toggle handlers (`toggleLangDropdown(e)`), always pass the event and call `if (e) e.stopPropagation();` to prevent the click event from bubbling to `document.addEventListener('click')`, which would immediately close the newly opened menu.

18. **Browser Cache-Busting for Static Assets & Dynamic Widgets:**
    - When updating standalone JavaScript files (such as `ai-widget.js`, analytics scripts, or CSS theme overrides) across an existing static site, browsers often cache the previous version locally on disk for hours or days.
    - Always append an explicit cache-busting version query string to the script tag (e.g. `<script src="/ai-widget.js?v=2.2" defer></script>`) across all HTML files during batch generation, so all client browsers immediately fetch the latest version without requiring manual hard refreshes.

19. **Autonomous AI Sales Agent Studio & Dual-Engine Architecture:**
    - When embedding an autonomous AI sales widget into customer portals and marketing sites, structure a dual-engine architecture:
      - **Deterministic BANT Engine (Default / Fast):** Latency <0.1s, deterministic intent matching, regex-based lead contact capture (Telegram `@username`, email, phone), zero token cost, and 100% reliable fallback.
      - **Generative OpenRouter LLM + RAG:** Injects real-time articles from an `ai_knowledge_base` SQLite table into the system prompt, synthesizes grounded answers without hallucinations, and supports free/low-cost models (e.g. `google/gemini-2.0-flash-thinking-exp:free`, `deepseek/deepseek-r1:free`, `openai/gpt-4o-mini`).
    - Expose a dedicated management studio in the admin cabinet (`/dashboard`) allowing administrators to dynamically switch engine modes, test API keys, edit knowledge base articles, adjust prompt temperatures, and review live visitor chat transcripts.

20. **Admin Dashboard UI Harmonization & Hostinger CDN Cache Invalidation:**
    - When adding new workspace tabs or navigation items into existing dashboards (e.g. `dashboard.html`), ensure new elements strictly follow the standard styling of neighboring navigation items (`dash-nav-item`) without persistent inline highlights, custom borders, or contrasting backgrounds unless explicitly requested.
    - When deploying static HTML updates behind edge caching proxies (such as Hostinger CDN `hcdn`), the CDN edge may continue serving cached pages if file modification times (`mtime`) appear unchanged to the edge. Run a touch pass over deployed files on the remote server (`find <web_root> -name '*.html' -exec touch {} \;`) to ensure edge caches register updated file timestamps immediately.

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
