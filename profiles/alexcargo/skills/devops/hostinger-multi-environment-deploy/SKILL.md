---
name: hostinger-multi-environment-deploy
description: Use when deploying dev, staging, or prod sites to Hostinger.
---

# Hostinger Multi-Environment Deployment & Version Control

Workflow for deploying static/React web projects to Hostinger across `dev`, `staging`, and `production` environments while keeping strict Git version control and modular layout consistency.

## Trigger Conditions
Use when:
- Creating or updating `dev`, `staging`, or `production` environments on Hostinger across ecosystem domains (`aavalanche.com`, `cargosavior.com`, `container585.com`, `sitnei.com`, etc.).
- Inspecting or deploying to `/home/u473746908/domains/<domain>/public_html/` over SSH (`82.29.199.155:65002`).
- Syncing code changes between GitHub branches (`main`, `staging`, `dev`) and Hostinger web roots.
- Configuring `.htaccess` rules for SPA (Single Page Application) routing or static HTML page fallbacks.

## Key Principles & Quality Gates

1. **Dev-First Isolation Gate & Production Protection**
   - All experimental visual, layout, asset, and code iterations MUST remain strictly on `dev` (`https://dev.domain.com` / `/public_html/dev/`) until the user explicitly commands a production release.
   - Production (`domain.com` / `/public_html/`) is never modified during drafting or experimentation cycles.

2. **Preserve Global Modules & UI Integrity**
   - Never overwrite or drop global components (sticky Header, burger menu, language dropdown with vector SVG flags, Footer) when updating body content between Header and Footer.
   - Deconstruct sites into clean modular files (`header.html`, `footer.html`, `<page>_content.html`) so individual page updates leave global layouts untouched.
   - Sample exact color hex codes directly from user screenshots (e.g. using Python Pillow to sample `#5FB3F9` from logo images) so buttons, borders, and accents match 100%.

3. **Git Commit SHA & Branch Transparency**
   - Always state the active Git commit SHA and branch name after making any code changes, rollbacks, or deployments (e.g. `Commit SHA: 6709bc0 on branch dev`).

3. **Contact Form & Checkout Dual Mailer (dr.reenforce@gmail.com & User Confirmation)**
   - **Hostinger Linux Sendmail Line Endings (\n vs \r\n) Pitfall:** On Hostinger PHP mailers, email headers MUST use **LF (`\n`) line endings**, NOT `\r\n` (CRLF). Header strings formatted with `\r\n` cause Hostinger sendmail to reject the headers and return `false`. Header strings formatted with `\n` return `true` and deliver reliably.
   - **Active Sender Domain Mailbox:** Sender address MUST be an active registered mailbox on Hostinger (`From: info@aavalanche.com`), not an unconfigured alias like `noreply@`.
   - Deploy a `send_mail.php` handler on Hostinger that dispatches TWO emails via PHP `mail()`:
     1. **Admin Notification:** Sent to `dr.reenforce@gmail.com` with Subject `[NEW CONTACT INQUIRY] (<LANG>) from <email>` or `[PAID / NEW ORDER] #ORD-XXXX` containing client name, email, language, and message.
     2. **User Confirmation:** Sent to client's `$email` in their current site language (`en`, `es`, `de`, `fr`, `it`, `uk`, `ru`, `zh`, `ar`) with order/inquiry confirmation.
   - **Inline Contact Form Green Feedback Banner:** On `contact.html`, replace browser `alert()` popups with a clean **inline green feedback banner** (`✓ Your message has been sent successfully.`) under the form in the client's native language.

4. **Routing, Clean Extensionless URLs & Subdomain / Subfolder Dev Configuration (.htaccess)**
   - **Subdomain Custom Folder & Instant SSL Provisioning:** In Hostinger hPanel (*Websites ➔ Domains ➔ Subdomains*), create subdomain `dev` pointing to custom directory `public_html/dev`. Hostinger automatically routes `https://dev.domain.com` directly to `public_html/dev` and provisions Let's Encrypt / Hostinger SSL.
   - **Subdomain Rewrite Base Gotcha:** On Hostinger Apache subdomains (`dev.domain.com` whose DocumentRoot IS `/public_html/dev`), DO NOT use `RewriteBase /dev/`. `RewriteBase /dev/` causes double-prefixing (`/dev/dev/services`), resulting in Hostinger's 404 page (`htdocs_error/page_not_found.svg`).
   - **Dual Compatibility (`dev.domain.com` & `domain.com/dev/`):** When deploying dev builds, use relative asset and script paths (`src="./assets/..."`, `href="./index.css"`) or dynamic base tags. This allows the exact same build files to function identically on both the dedicated subdomain `https://dev.domain.com` and fallback subpath `https://domain.com/dev/` without asset resolution failures.
   - Direct route mapping for extensionless URLs (`/services`, `/pricing`, `/about`, `/contact`, `/login`, `/dashboard`, `/evaluation`) and automatic directory index serving (`DirectoryIndex index.html index.php`):
     ```apache
     DirectoryIndex index.html index.php

     <IfModule mod_headers.c>
       Header set Cache-Control "no-cache, no-store, must-revalidate"
       Header set Pragma "no-cache"
       Header set Expires 0
       Header set X-Robots-Tag "noindex, nofollow"
     </IfModule>

     <IfModule mod_rewrite.c>
       RewriteEngine On
       RewriteBase /

       RewriteCond %{REQUEST_FILENAME} -d
       RewriteRule ^(.*)$ $1/index.html [L]

       RewriteCond %{REQUEST_FILENAME} !-d
       RewriteCond %{REQUEST_FILENAME}\.html -f
       RewriteRule ^([^/]+)/?$ $1.html [L]

       RewriteCond %{REQUEST_FILENAME} !-d
       RewriteCond %{REQUEST_FILENAME}\.html -f
       RewriteRule ^(es|de|fr|it|uk|ru|zh|ar)/([^/]+)/?$ $1/$2.html [L]
     </IfModule>
     ```

5. **Clean Language Switcher & Persistent Auth Session**
   - **No `index.html` in Language Switcher Links:** The `navigateToLang(langCode)` JS function must navigate to clean root paths (`/` for English, `/uk/`, `/es/`, `/de/`, etc. for subfolders) WITHOUT appending `index.html` to URLs.
   - **Persistent Single-Domain Auth Session:** In `auth.php`, configure `ini_set('session.cookie_path', '/')` and `session_set_cookie_params(['path' => '/', 'samesite' => 'Lax'])` before `session_start()`. This guarantees the `PHPSESSID` cookie is valid across all language subfolders (`/uk/`, `/es/`, `/de/`, etc.) so users remain logged in when switching site languages.

4. **Chrome Browser Caching vs. Server Verification**
   - Chrome aggressively caches 200 OK HTML pages. When the user reports "Nothing changed" ("Ничего не поменялось") despite `md5sum` or SSH confirming remote file updates, include `Cache-Control: no-cache, no-store, must-revalidate` in `.htaccess` and share a cache-busting URL parameter (e.g. `dev.domain.com/contact.html?v=2`) or suggest `Ctrl + Shift + R`.

5. **Single Source of Truth & 1-to-1 Multilingual Page Clones**
   - **English (`/` root) as Master Baseline:** The English version is the single source of truth. Any structural change, section addition/deletion, component modification, header, footer, or layout update made to English MUST be mirrored identically across all 8 language subfolders (`/es/`, `/de/`, `/fr/`, `/it/`, `/zh/`, `/ar/`, `/uk/`, `/ru/`). The layout, cards, buttons, logos, and DOM structure across all languages must remain 100% mirrored clones.
   - When generating localized versions (`/es/`, `/de/`, `/fr/`, `/it/`, `/zh/`, `/ar/`, `/uk/`, `/ru/`), copy the master English HTML/CSS layout 1-to-1. ONLY translate text strings (headings, paragraphs, feature lists, button labels) — NEVER add extra buttons, alter card geometry, or change page design.
   - **Company Logos:** On all language subfolder pages, the Header and Footer logo MUST use the default company logo (`../avalanche_logo.png` / relative path), exactly matching the master English version.
   - **Dynamic Flag & Label on Selector Button:** The language selector button on any page MUST display the flag and code of the active language for that page (e.g. 🇪🇸 `ES` on `/es/`, 🇩🇪 `DE` on `/de/`, 🇫🇷 `FR` on `/fr/`), while the dropdown menu lists all 9 languages.
   - **Cross-Page Language Switching:** Ensure the language switcher script calculates relative paths cleanly (`../es/pricing.html` if switching from `/de/pricing.html` to Spanish, or `es/pricing.html` if switching from root) so language switching works from ANY subpage URL without triggering 404 errors.

6. **Hero Screen Layout & Interactive Input Field ("Describe your project")**
   - Right column (`hero-right-col`): Lifted blue visual card (`hero-visual`) at the top, and DIRECTLY UNDERNEATH it a double-height textarea field (`Describe your project` / placeholder *"Tell us in your own words what do you wish to arrange or create, your objectives is our mission."*) with a circular blue Send Arrow button (`#5FB3F9`).
   - Left column: CTA buttons (`View Services`, `Talk to us`) remain in the left column under the lead text.

7. **User Auth, Personal Cabinet, Orders Table & Admin Management System (`auth.php`, `login.html`, `dashboard.html`)**
   - **Backend (`auth.php`):** SQLite DB (`data/database.sqlite`) + PHP PDO. Tables `users` and `orders`. Default admin seed `admin` / `admin`.
   - **Persistent Auth Session Across Subfolders:** In `auth.php`, set `ini_set('session.cookie_path', '/')` and `session_set_cookie_params(['path' => '/', 'samesite' => 'Lax'])` before `session_start()`. This ensures the `PHPSESSID` cookie is valid across all language subfolders (`/uk/`, `/es/`, `/de/`, etc.) so users are NOT logged out when switching site languages.
   - **Login Page (`login.html`):** Email/Password login + **Google & Facebook OAuth login buttons** + Register form + Placeholder `john@company.com` (NO demo admin banners).
   - **404 Auth Fix:** Place copies of `login.html`, `dashboard.html`, and `auth.php` at the domain root AND inside every language subfolder (`/uk/login.html`, `/es/login.html`, etc.) while using absolute `/auth.php` API fetch paths so authentication never 404s.
   - **User Dashboard (`dashboard.html`):**
     * Profile & Verification tab (`✓ Verified` badges / SMS verification popup).
     * My Orders tab ("Мои заказы") with active & past orders table.
     * Admin Panel tab ("Users Table") visible ONLY for `admin / admin` listing all registered clients (ID, Name, Email, Country, Phone, Role, Verification, Date).
   - **Persistent Header User Avatar:** On ALL pages and languages, when a user is logged in, the `Sign In` button in the header transforms into a **white user silhouette inside a blue circle (`#5FB3F9`)** linking to `dashboard.html`.

8. **1-to-1 Rollback Guard**
   - Verify file identity using MD5 checksums (`md5sum <file1> <file2>`) over SSH before claiming a rollback or sync is 100% complete.

9. **AI Project Evaluation, 10-Point Dollar Pricing Calculator & Monobank Payment Flow (`evaluation.html`)**
   - **Hero Input & Enter Key Handler:** The `Describe your project` textarea on `index.html` submits on button click AND on keyboard **`Enter`** key press (`onkeydown="if(event.key==='Enter' && !event.shiftKey){...}"`). Saves the inquiry string into `localStorage.setItem('hero_project_desc', val)` and redirects to `dev.domain.com/evaluation.html`.
   - **Animated AI Preloader:** Percentage counter animating from 0% to 100% with live progress messages (*Analyzing project objectives...*, *Evaluating architectural complexity...*, *Calculating AI agentic requirements & memory index...*).
   - **Real AI Complexity Analyzer & Full 10-Level Price Graduation ($9+$5/mo ➔ $99+$50/mo):** Dynamic NLP algorithm evaluating scope, word count, and technical keywords (CRM, ERP, Scrapy, high load, vector DB, RAG, multi-tenant):
     * Score 1..10 ($9 setup + $5/mo ➔ $99 setup + $50/mo):
       - 1 point ($9 setup + $5/mo): Simple single-purpose bot or reminder ("записывать и слать мне напоминания").
       - 2 points ($19 setup + $10/mo): Multi-function assistant / note keeper / password vault ("со мной общаться, помогать и хранить все мои пароли и заметки").
       - 10 points ($99 setup + $50/mo): Intergalactic superproject / universal management system ("межгалактический суперпроект по управлению Вселенной").
     * Client NEVER sees the point score, ONLY sees calculated price in USD and local currency approximation.
   - **Dynamic IP Currency Detection:** Visitor country detected via IP Geolocation API (`ipapi.co`). Displays local currency approximation: UAH (`~ 789 UAH`) for Ukraine `UA`, EUR (`~ €17.48 EUR`) for Eurozone, GBP (`~ £15.01 GBP`) for UK, USD (`$19.00 USD`) for US/Others.
   - **Deliverables List ("You Receive" / "Ви отримуєте"):**
     * 7 Universal Mandatory Deliverables: Always-on Telegram AI Agent, Latest Enterprise AI Model Stack (without listing specific model names), Configured Unlimited Memory Engine, Continuous Self-Learning System, Extensible Skill Set, Custom API & Service Integration, 24/7 Avalanche Agency Support.
     * Dynamic Custom Skill requested in hero input.
   - **Payment Gateway Modal & Checkout:**
     * Express Pay Buttons: **Pay with Apple Pay 🍏** & **Pay with Google Pay 💳**.
     * Action Button: **`💳 Pay Now ➔`** (No Monobank text mentions or Monobank acquiring titles in modal).
     * Auto-fills logged-in user email into `#checkout-user-email`.
   - **Monobank Acquiring Setup Requirements (ФОП):**
     * `X-Token` (Merchant API Token) from `web.monobank.ua` or Monobank App (*Монобанк для ФОП ➔ Еквайринг ➔ API Токен*).
     * Merchant Account ID.
     * Webhook URL (`https://dev.domain.com/mono_webhook.php`).
   - **Post-Payment Confirmation & Multilingual Branded Email Notifications:**
     * Confirmation Screen: *"Your order has been accepted! Your AI agent will be ready within 48 hours."*
     * Multilingual Dual Branded Email via `send_mail.php`:
       - **Client Email:** Dispatched in the client's current site language (`en`, `es`, `de`, `fr`, `it`, `uk`, `ru`, `zh`, `ar`) with Order `#ORD-XXXX`, price breakdown, and 48-hour delivery timeline.
       - **Admin Email (`dr.reenforce@gmail.com`):** Branded HTML notification with Subject `[PAID / NEW ORDER] #ORD-XXXX (<LANG>)` and client details.
     * Auto-records order into `orders` table in `database.sqlite` for display under **My Orders ("Мои заказы")** in `dashboard.html`.

10. **Logo Asset Extraction, Multi-Resolution Favicon Generation & Vectorized HSV Swatch Recoloring**
    - **Logo & Emblem Processing via Python Pillow:** When replacing placeholder CSS circles or existing branding with a user-provided logo image:
      * Crop tight bounding box around visible alpha content (`alpha > 10`).
      * Pad to 1:1 square canvas with transparent background for icons and Favicons (`Image.new("RGBA", (max_dim, max_dim), (0, 0, 0, 0))`).
      * Generate multi-resolution `favicon.ico` (`sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128)]`), `favicon-16x16.png`, `favicon-32x32.png`, `apple-touch-icon.png` (180x180), `icon-192.png`, and `icon-512.png`.
    - **Vectorized HSV Color Swatch Retinting:** When recoloring a brand logo based on a user-provided color swatch:
      * Sample median RGB/Hex from the swatch screenshot via Pillow.
      * Convert RGBA image to HSV space; isolate colored/saturated pixels using a smooth saturation mask (`sat_mask = np.clip((s - 0.15) / 0.25, 0.0, 1.0)`).
      * Replace Hue and Saturation of the mask region with the target swatch while keeping white typography (saturation near 0) and alpha transparency untouched.
      * Update Tailwind config and CSS variables (`cargo-orange`, accent borders, scrollbars) to match the new hex code across the site.
    - **SPA Header & Footer Replacement:** In bundled React/Vite applications, locate JSX element trees defining CSS circle shapes (e.g. `border-4 border-cargo-orange rounded-full`) in Header navbar (`Ae`), Footer branding, and Sidebar components, and replace with clean `<img>` tags referencing `/assets/logo.png` (or relative `./assets/logo.png`) with `object-contain` and hover transitions.
    - **HTML `<head>` Injection:** Include all standard favicon rel links in `index.html`:
      ```html
      <link rel="icon" type="image/x-icon" href="/assets/favicon.ico">
      <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32x32.png">
      <link rel="icon" type="image/png" sizes="16x16" href="/assets/favicon-16x16.png">
      <link rel="apple-touch-icon" sizes="180x180" href="/assets/apple-touch-icon.png">
      ```

## References
- `references/subdomain_routing_and_caching.md` — Detailed `.htaccess` snippets, double-prefixing gotchas for Hostinger subdomains, and Chrome cache-busting procedures.
- `references/evaluation_and_monobank_flow.md` — Complete technical architecture for AI project estimation, 10-point price graduation, IP currency detection, Monobank Acquiring setup, and multilingual email dispatch.
