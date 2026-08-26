---
name: navo-design-system
description: Use when designing Navo pages or emails. Navo Brand Book.
version: 1.0.0
author: Callum Vance
license: MIT
tags: [navo, design, brandbook, css, html, email, UI]
platforms: [linux, macos, windows]
triggers:
  - design for navo
  - navo brand
  - navo24 email
  - navo24 style
  - navo html template
  - navo brandbook
  - trackingmcp design
---

# Navo24 Design System & Brand Book (v5.52)

Guidelines, tokens, typography standards, and copy rules for all Navo24 platforms (`navo24.com`, `trackingmcp.com`, `schedulesmcp.com`, `loadingmcp.com`, `freightratesmcp.com`).

## 1. Brand Palette & Color Tokens

### Core Palette
- **Navy (`#0C2A5E`):** Navy-ink ground, primary header background on marketing surfaces.
- **Cobalt (`#1F4FE6`):** Primary signal color for buttons, key links, and CTAs (`#4A86FF` on dark grounds).
- **Signal Strong (`#1733B5`):** Button border and active state.
- **Signal Soft (`#EEF1FE`):** Light accent background for callout boxes and feature highlights.
- **Turquoise (`#12C2C2`):** Instrument accent for tracking and in-transit status.
- **Instrument Amber (`#E8A33D` / Soft `#FDF3E3`):** Functional accent for money, demurrage clocks, and attention (never used in the identity mark).
- **Canvas (`#FCFCFB`):** Light theme main background.
- **Paper (`#FFFFFF`):** Card / surface background.
- **Ink (`#0B0C0E`):** Primary text color.
- **Ink-500 (`#59616B`):** Secondary text and muted labels.
- **Line (`#E9E8E3`):** Border lines and dividers.

## 2. Typography Hierarchy

- **Display / Hero Titles:** Ranade (Fontshare: `https://api.fontshare.com/v2/css?f[]=ranade@200,300,500,700&display=swap`). Light 300 / Ultralight 210, tracking `-0.03em`.
- **Body Text:** Switzer (Fontshare: `https://api.fontshare.com/v2/css?f[]=switzer@200,300,400,500,600,700&display=swap`). Extralight 200 to Regular 400, line-height 1.5.
- **Figures, Badges, & Eyebrows:** JetBrains Mono (uppercase, tracked `+0.10em` to `+0.14em`).
- **Font Stack Fallbacks:**
  - Display Titles: `'Ranade', 'Switzer', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`
  - Body Text: `'Switzer', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`
  - Monospace: `'JetBrains Mono', SFMono-Regular, Consolas, monospace`

## 3. Copy & Prose Rules (§08 The Voice)

- **Spaced Em-Dash Rule:** The spaced em-dash (` — `) is **banned from prose** as an AI-writing tell. Use colons, semicolons, commas, or periods instead. (Allowed only in titles/labels like `"TrackingMCP — Dashboard"`).
- **Zero-Emoji UI Rule (Strict Brand Standard):** Gratuitous, arbitrary, or colorful emoji icons (`✍️`, `👁️`, `🎯`, `🕒`, `📚`, `🔍`, `🖼️`, `⚡`, `🏠`, `📦`, `📊`, `⚙️`, `🛡️`, `🚪`, etc.) are **strictly prohibited** in tab labels, buttons, navigation bars, headers, and UI controls. No unauthorized emojis anywhere in Navo UI. Interface elements must be clean, typography-led (Switzer, Ranade, JetBrains Mono) or accompanied strictly by brand SVG line icons (stroke width 1.8–2.0px).
- **Dual-Staging & Repository Topography:**
  - **Umbrella Portal (`navo24.com`):** Repo `Navo24S/navo24-web` (Astro v5, TailwindCSS v4). Staging for Stefan's isolated branch is on `https://stefan.staging.navo24.com/` (`navo24-web-stefan.pages.dev`).
  - **Product Web App (`trackingmcp.com`):** Repo `Navo24S/trackingmcp` (React SPA, Vite, Supabase). Staging is on `https://tracking.staging.navo24.com/` (`navo24-tracking-web-staging.pages.dev`).
- **Endorsement Rule (§06):** Legal footers and product endorsements must use `© 2026 [Product] · a Navo24 product` in lowercase JetBrains Mono (10–11px, `ink-500`).
- **Team Names:** Robert's title is Full-Stack Developer (first name "Роберт" only, do NOT add "Vance" surname). Callum Vance is Tech Lead.

## 4. Brand Vector Assets

- **White Wordmark:** `https://navo24.com/brand/navo-wordmark-white.svg`
- **Dark Wordmark:** `https://navo24.com/brand/navo-wordmark.svg`
- **Identity Mark:** `https://navo24.com/brand/navo-mark.svg`

## 5. Email Template & CTA Layout Rules

- **CTA Button Layout (Avoid Edge-to-Edge Banner Overflow):**
  - Never put `background-color` on a `width: 100%` wrapper `<td>` around a CTA button link. That stretches the button background edge-to-edge across the card padding.
  - Wrap the CTA button in `<table align="center">` and place `background-color: #1f4fe6`, `display: inline-block`, `padding: 14px 28px`, `border-radius: 6px`, and `box-sizing: border-box; max-width: 100%;` directly on the `<a>` element.
- **Vertical Step Lists:**
  - On step-by-step onboarding boxes ("Step 1 → Step 2"), stack steps vertically (one under the other) with individual step badges (`Step 1`, `Step 2`) and vertical connectors (e.g. `border-left: 2px dashed #12c2c2`). Avoid crowding steps into horizontal single-line badges.
- **Header Badging:**
  - Header right corner should feature a clean `navo24.com` badge in JetBrains Mono (`11px`, `color: #12c2c2`, `background-color: rgba(18, 194, 194, 0.12)`).
- **Secondary Contact Line Positioning:**
  - Secondary contact options (e.g. `sales@navo24.com` / demo requests) should be placed as a clean plain text sentence with an underlined mailto link directly above the sign-off (`Best regards, / The Navo24 Team`), rather than a secondary button.

## 6. Slide Decks & Presentation Artifacts

- **Theme & Both Themes Rule (§03):** Support both Dark (`#0A0E16` canvas, `#121826` paper, `#1A2234` cards) and Light (`#FCFCFB` canvas, `#FFFFFF` paper, `#F8FAFC` cards) via a Theme Toggle button in the header (`☀️ Light` / `🌙 Dark`) with state saved in `localStorage`.
- **Typography:** Ranade for display slide titles (`h1`, `h2`), Switzer for body/cards, JetBrains Mono for eyebrows/badges/SLA tags. Include Fontshare URLs in `<link>` tags.
- **Header Bar:** Navo white wordmark SVG, product badge (`navo24.com` or project badge), slide counter (`1 / N`), Theme Toggle button, and keyboard controls (`← / →`).
- **Mobile Responsiveness:**
  - On screens `<= 768px`, collapse 2-column/4-column card grids to 1 column (`1fr`).
  - Do NOT lock viewport height (`height: 100vh; overflow: hidden`) on mobile — allow smooth scrolling.
  - Implement mobile touch swipe support (`touchstart` / `touchend`).
  - Provide a sticky bottom mobile control bar (`← Назад | Слайд N из 8 | Вперед →`).
- **Modal Window UX Rule:** ALL modal windows in Navo apps and dashboards MUST support closing via Escape key (`e.key === 'Escape'` keydown listener) and backdrop click.
- **Interactive Slide Decks:** Support keyboard controls (`← / →`, `Space`, `Home`, `End`), touch swipe (`touchstart` / `touchend`), progress bar indicator, slide counter (`Slide X of N`), and both Light/Dark modes with `localStorage` persistence.
- **Deployments:** Package with static `index.html` + `vercel.json` (`cleanUrls: true`) for 1-click Vercel deployment using `VERCEL_TOKEN=vcp_2QMSKEwYW3Dg4vdKOTB8q7IRCr2uCEFWeXgVMDAr18jPnuhEKf0KYAYO vercel <dir> --prod --yes --scope navo5`.

## 7. AI-Augmented Developer KPI & Velocity Benchmarking

- **Name Conventions:** Robert is "Роберт" (Full-Stack Developer), NOT "Роберт Vance".
- **Baseline Observation Phase (Month 1):**
  - Do NOT set arbitrary hardcoded SLA numbers (e.g. "48 hours Cycle Time") without project-specific baseline data.
  - Phase 1 focuses on 0 Prod Regressions (Sev-1) + 100% AI Review & Test pass, while logging real velocity with Claude Code on Dev-servers.
  - Log AI tool usage via GitHub PR templates (`[x] Claude Code Assisted`) and CI/CD time-to-dev-server metrics to set accurate company SLAs on Month 2.

## 8. Multilingual, Navigation & Account Standards (9 Languages)

- **URL Structure & Hierarchy:**
  - Root `navo24.com/` is default English.
  - Multilingual localized versions use clean prefix paths: `navo24.com/es`, `navo24.com/de`, `navo24.com/fr`, `navo24.com/it`, `navo24.com/uk`, `navo24.com/ru`, `navo24.com/zh`, `navo24.com/ar`.
- **Dynamic Localization & i18n Rules:**
  - Never leave hardcoded English strings in shared marketing components (`MarketingNav`, `HomePage`, `MarketingFooter`). All rendered copy must call `t(...)` from `useTranslation()` linked to `src/locales/{lang}.json`.
  - Route wrapper (`LanguageRouteWrapper` at `/:lang/*`) must automatically synchronize `i18n.changeLanguage(lang)` and set `document.documentElement.setAttribute('dir', lang === 'ar' ? 'rtl' : 'ltr')`.
- **Language Switcher & Flags:**
  - 9 standard languages: English, Español, Deutsch, Français, Italiano, Українська, Русский, 中文, العربية.
  - **Russian (`ru`) Flag Directive:** Strictly use the White-Blue-White flag (⬜🟦⬜ / SVG with three equal horizontal stripes: White, `#0083D6` Blue, White).
  - **Arabic (`ar`):** Must toggle document direction to RTL (`document.documentElement.setAttribute('dir', 'rtl')`).
- **Header Auth State & User Menu:**
  - Unauthenticated: Display ONLY the primary "Start free" button (do NOT add a separate "Sign in" button — "Start free" serves as the single action point).
  - Authenticated: Display ONLY the user avatar button (`UserAccountMenu`) styled in brand Cobalt blue (`color: var(--signal)` / `#1F4FE6`, `background: rgba(31, 79, 230, 0.12)`, `border: 1px solid rgba(31, 79, 230, 0.32)`) with hover/click dropdown popover. Do NOT show an extra blue "Dashboard →" button in the header navbar or mobile drawer (the avatar dropdown already provides direct access to all workspace destinations). The dropdown menu contains:
    - User email and role tag (*SUPERADMIN / MEMBER*).
    - Workspace Home (`/home`), Shipments Board (`/dashboard`), Analytics (`/analytics`), Settings (`/settings`).
    - Superadmin only: Blog Publisher (`/home/blog`), Superuser Panel (`/admin`).
    - Sign out action.
- **Routing & User Navigation Preservation:**
  - Never automatically redirect logged-in users away from the public marketing homepage (`/`) into `/home` or `/dashboard`. A user (logged-in or guest) must always land on the exact URL they requested. Logged-in users access the workspace via the user account dropdown.
- **Static Hosting & Client Sub-Routes (Cloudflare Pages):**
  - Cloudflare Pages serves physical assets before `_redirects`. Every localized prefix route (`/es`, `/de`, `/fr`, `/it`, `/uk`, `/ru`, `/zh`, `/ar`) AND client-side application sub-routes (e.g. `/home/blog`, `/blog-editor`, `/sales/accounts`, `/sales/people`) MUST have static HTML shells pre-emitted at build time for both `dist/<route>.html` AND `dist/<route>/index.html` (via `prerender.mjs`) to avoid CDN 404 fallbacks on direct page hits and page refreshes.
- **Editorial & Rich-Text Editor State Management (`contentEditable`):**
  - Superadmin RTF studio with Brand Book fonts (Ranade, Switzer, JetBrains Mono), 11-step self-audit metrics (99% originality, <15% AI score), and live corner-drag image resizing handles.
  - **React contentEditable Rule:** NEVER bind `dangerouslySetInnerHTML` directly onto a `contentEditable` element on every controlled re-render. Doing so collides with React's DOM reconciler during typing, causing `TypeError: Cannot read properties of null (reading 'innerHTML')`. Instead, synchronize initial/tab-switch HTML via `ref.current.innerHTML` in `useEffect`, and read `e.currentTarget.innerHTML` in `onInput` without letting React manage child nodes.
  - **Asynchronous Auth & Ref Mounting Rule:** When the editor wraps around an asynchronous auth check (`if (checking) return <Spinner />`), `useEffect` hooks for syncing `post.contentHtml` into `contentRef.current.innerHTML` and attaching image click/resize listeners MUST include `checking` in their dependency array (`[checking, activeTab, post.id, post.contentHtml]`), otherwise effects run during the early return when `contentRef.current` is `null` and fail to bind once auth resolves.
  - **Direct In-Canvas Image Drag Resizing:** Images inside the editor must be directly resizable via an absolute transform overlay on the clicked `<img>` with 4 corner drag handles (`nw`, `ne`, `se`, `sw`) and a floating action pill (`Left`, `Center`, `Right`, `100%`, presets, `Delete`). Never put separate image control boxes outside the editor canvas.
  - **Articles Catalog & Search:** Provide an "All Articles" management tab placed at the end of the editor tab hierarchy (`Content Editor` [default] → `Live Brand Preview` → `SEO & AI Quality` → `Version History` → `All Articles`) with instant live search across titles, slugs, categories, tags, and authors, segmented status filters (`All`, `Published`, `Draft`, `Scheduled`), category filtering, and 1-click `Edit` / `Preview` / `Delete` actions.
- **Deployment Pipeline Target & Repository Topography:**
  - **Product App (TrackingMCP):** `Navo24S/trackingmcp` (React SPA, Vite, Bun). Staging deliverables must be committed and pushed to `dev` branch to trigger `.github/workflows/deploy-web-staging.yml` deploying to Cloudflare Pages (`https://tracking.staging.navo24.com/`). Avoid temporary Vercel deploys for main product features.
  - **Umbrella Portal (navo24.com):** `Navo24S/navo24-web` (Astro v5.18.2, TailwindCSS v4). Features automatic brand and schema audits. When carrier or connector counts drift, run `bun run sync:stats` before `bun run build` to synchronize `stats.json` across comparative markdown tables.
    - General Staging: Deployed to `https://navo24-web-staging.pages.dev/` via `.github/workflows/deploy-staging.yml` on push to `dev` or `main`.
    - Stefan Personal Staging (`stefan` branch): Push to branch `stefan` triggers `.github/workflows/deploy-stefan.yml`, deploying to Cloudflare Pages project `navo24-web-stefan` (`https://navo24-web-stefan.pages.dev/` / custom domain `https://stefan.staging.navo24.com/`).
    - Cloudflare DNS & SSL Provisioning: Custom subdomains require a CNAME in Cloudflare DNS pointing to the respective `<project-name>.pages.dev` with `Proxied: true`. Deep 3rd-level subdomains (`*.staging.navo24.com`) trigger automated Edge TLS certificate issuance by Cloudflare, during which HTTP 301 is active while HTTPS may return TLS alert 552 for 5-15 minutes before the edge cert becomes active.

## 9. Mobile Responsiveness & Viewport Overflow Rules

- **Navbar Header Isolation (< 760px):**
  - Keep the mobile navbar header ultra-clean: **Logo + Language Switcher + Theme Toggle + Hamburger**.
  - Long CTA buttons (*«Start free»* / *«Comenzar gratis»* / *«Sign in»*) must be hidden from the top bar on mobile (`.marketing-nav-cta { display: none !important; }`) and placed prominently full-width inside the hamburger drawer to prevent top bar overflow.
- **Ambient Glow & Pseudo-elements:**
  - Absolute ambient glow pseudo-elements (e.g. `.cp-hero::before`) must use `width: min(1320px, 100vw)` and the parent section MUST have `overflow: hidden; position: relative;` to prevent off-canvas horizontal scrolling.
- **Grid Auto-fit Clamping:**
  - Do not use fixed pixel minimums like `minmax(300px, 1fr)` on mobile grids with container padding, as 320px–360px phones will overflow. Use `minmax(min(260px, 100%), 1fr)` and explicit single-column collapse (`grid-template-columns: 1fr !important`).
- **Global Viewport Safeguard:**
  - `html, body { overflow-x: hidden; max-width: 100vw; }` to guarantee zero horizontal drag.

## 10. Social Media & Marketing Visuals (LinkedIn & X)

- **Canvas & Resolution Standards:**
  - LinkedIn Standard: `1200 x 675` (16:9 landscape) rendered with `device_scale_factor: 2` (produces `2400 x 1350` ultra-crisp Retina PNG).
  - Square / Carousel: `1200 x 1200` (1:1).
- **Background & Atmospheric Lighting:**
  - Deep Obsidian / Navy ground (`#060911` or `#070C18`).
  - Subtle radial glow pseudo-elements: Cobalt (`rgba(31, 79, 230, 0.22)`, blur `60px`) at top-right, Turquoise (`rgba(18, 194, 194, 0.14)`, blur `70px`) at bottom-left.
  - Ambient grid overlay: `40px 40px` with `rgba(255, 255, 255, 0.03)` masked radially.
- **Typography & Headline Composition:**
  - Eyebrows & Meta: JetBrains Mono (`11-12px`, uppercase, tracking `+0.14em`, color `#4A86FF` or `#12C2C2`).
  - Core Statement: Ranade Light 300 (`36-42px`, line-height `1.18`, tracking `-0.03em`), bolding key phrase in white/cobalt gradient (`#FFFFFF` to `#90B2FF`) and brand terms in turquoise (`#12C2C2`).
  - Subtitle: Switzer Regular 400 (`15-17px`, line-height `1.5`, color `#8E9BAE`).
  - Punchline Pill: JetBrains Mono badge (`#E2ECFF`, border `1px solid rgba(74, 134, 255, 0.35)`, background `rgba(31, 79, 230, 0.12)`).
- **Interactive Architectural & Execution Mockup Cards:**
  - Glassmorphic card styling: `background: rgba(14, 20, 36, 0.85)`, `border: 1px solid rgba(255, 255, 255, 0.10)`, `backdrop-filter: blur(16px)`, `border-radius: 14px`.
  - Top border gradient accent: `linear-gradient(90deg, transparent, #4A86FF, #12C2C2, transparent)`.
  - Real Domain Elements: Verified container ID (e.g. `MSCU9284102`), UN/LOCODE port route (`Rotterdam NLRTM ➔ Singapore SGSIN`), 3-tier status rows:
    - *Signal:* Problem / trigger in Amber (`#E8A33D`).
    - *Resolution:* Autonomous action in Cobalt (`#1F4FE6` / `#4A86FF`).
    - *Impact:* Preserved SLA / $0 demurrage in Turquoise (`#12C2C2`).
    - *Terminal Log:* Real DCSA API call (`POST /v1/containers/... [200 OK]`).
- **Rendering Workflow (Playwright):**
  - Render HTML template to PNG via headless Chromium using Playwright: launch with `--no-sandbox`, viewport `1200x675`, `device_scale_factor: 2`, wait 2000ms for Fontshare fonts (`Ranade`, `Switzer`) to hydrate before `page.screenshot()`.



