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
- **Deployments:** Package with static `index.html` + `vercel.json` (`cleanUrls: true`) for 1-click Vercel deployment using `VERCEL_TOKEN=vcp_2QMSKEwYW3Dg4vdKOTB8q7IRCr2uCEFWeXgVMDAr18jPnuhEKf0KYAYO vercel <dir> --prod --yes --scope navo5`.

## 7. AI-Augmented Developer KPI & Velocity Benchmarking

- **Name Conventions:** Robert is "Роберт" (Full-Stack Developer), NOT "Роберт Vance".
- **Baseline Observation Phase (Month 1):**
  - Do NOT set arbitrary hardcoded SLA numbers (e.g. "48 hours Cycle Time") without project-specific baseline data.
  - Phase 1 focuses on 0 Prod Regressions (Sev-1) + 100% AI Review & Test pass, while logging real velocity with Claude Code on Dev-servers.
  - Log AI tool usage via GitHub PR templates (`[x] Claude Code Assisted`) and CI/CD time-to-dev-server metrics to set accurate company SLAs on Month 2.

