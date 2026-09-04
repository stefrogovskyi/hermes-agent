---
name: navo-design-system
description: Navo24 Design System v6.0 (Official Master Brand Guidelines).
version: 6.0.0
author: Callum Vance
license: MIT
tags: [design-system, navo, branding, tokens, ui, colors, typography]
---

# Navo24 Design System (v6.0 Master Brand Guidelines)

Authoritative specification for all Navo24 digital interfaces, product apps, landing pages, slide decks, and marketing visuals.

---

## 1. Brand Philosophy & Ecosystem Identity
- **Master Brand Rule:** NAVO operates as one master brand. Individual products are NOT independent visual brands — the NAVO identity remains consistent while product accent colors help users recognize different capabilities.
- **Core Purpose:** Move global logistics from coordination to orchestration.
- **The Target Motif:** The "O" in NAVO is built from concentric rings representing a destination, signal, and convergence of multiple systems around one objective.

---

## 2. Color Palette & Design Tokens

### 2.1 Backgrounds & Environments
- **Primary Dark Graphite (Brand Canvas):** `#181818` (Preferred dark environment for the primary NAVO identity).
- **Product Page Canvas:** `#0A1117` (Deep technical navy/slate for SaaS app surfaces, cards, and tables).
- **Deep Black:** `#000000` (Pure contrast base).
- **Warm Dark:** `#201F1C` (Soft dark background alternative).
- **Light Canvas:** `#FCFCFC` / `#FFFFFF` (Clean light mode canvas).

### 2.2 The Target Rings & Ecosystem Products
Built with strict concentric color hierarchy:
1. **Outer Ring / Base:** `#113EC9` (Deep Royal Blue)
2. **Ring 2 / TrackingMCP:** `#1F4FE6` (Electric Cobalt Blue — Visibility, movement, real-time tracking)
3. **Ring 3 / Rates / Demurrage:** `#E2231A` (Vivid Red — Market rates, alerts, cost thresholds)
4. **Ring 4 / LoadingMCP:** `#FF8135` / `#FF7A1F` (Signal Orange — Execution, operational movement)
5. **Inner Center:** White (`#FFFFFF`) on dark backgrounds, Black (`#000000`) on light backgrounds.

### 2.3 Product Specific Accent Colors
- **TrackingMCP:** Electric Blue (`#1F4FE6` / `#113EC9`)
- **SchedulesMCP:** Ocean Teal (`#77E6FF` / `#31D8FE` / `#12C2C2`)
- **LoadingMCP:** Signal Orange (`#FF8135` / `#FF7A1F`)
- **FreightRatesMCP:** Vivid Purple (`#A055FF`) & Rate Red (`#E2231A`)
- **AirCargoMCP:** Sky Cyan (`#31D8FE`)

### 2.4 Accent & Communications Colors
- **Citron / Electric Lime:** `#CEF868` / `#B5ED30` (High energy external communications, badges, key callouts).
- **Yellow Gold:** `#FFCF01` (Metrics, star ratings, warm badges).
- **Hyper Pink / Magenta:** `#FA61AA` / `#FE8FC9` (Internal communications, highlights).

### 2.5 Strict Accessibility & Text Contrast Rules
- **Color text:** Recommended ONLY on solid Black, Dark Graphite (`#181818`), or Pure White backgrounds.
- **Colored background surfaces:** On bright colored cards/pills (e.g. `#CEF868`, `#FFCF01`, `#FF8135`), **ONLY 100% Black text (`#000000`)** is permitted. Never use white text on yellow, lime, or orange.
- **Never use light gray shadows** on white backgrounds.

---

## 3. Typography Hierarchy

### 3.1 Typefaces
- **Primary Display / Headlines:** **Ranade** (Light 300, Medium 500, Bold 700). Geometric, directional, architectural.
- **Interface & Body:** **Switzer** (Regular 400, Medium 500, Semibold 600). Clean neo-grotesque sans-serif with high legibility.
- **Code, Data & Badges:** **JetBrains Mono** (400, 500, 700). Monospaced for ports, container numbers, logs, SLAs.

### 3.2 Font CDN Links
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<link href="https://api.fontshare.com/v2/css?f[]=ranade@200,300,500,700&f[]=switzer@200,300,400,500,600,700&display=swap" rel="stylesheet">
```

### 3.3 Sizing Scale
- **Primary Heading (H1):** `44pt` (`~56px`), line-height `1.15`, letter-spacing `-0.03em`.
- **Secondary Heading (H2):** `33pt` (`~42px`), line-height `1.2`, letter-spacing `-0.02em`.
- **Tertiary Heading (H3):** `22pt` (`~28px`), line-height `1.3`.
- **Large Body / Subhead:** `18pt` (`~24px`), line-height `1.5`.
- **Standard Body:** `14pt - 16pt` (`~18px - 20px`), line-height `1.6`.
- **Badges / Eyebrows / Captions:** `11pt - 12pt` (`~14px`), uppercase, JetBrains Mono, letter-spacing `0.12em`.

---

## 4. Logo Usage & Geometry
- **Primary Logo:** Combines the `navo` lowercase wordmark with the multi-color concentric target replacing the `o`.
- **Clear Space:** Minimum clear space around the logo equals the inner diameter of the target ring.
- **Minimum Digital Size:** `70px` width.
- **Dark Backgrounds:** White wordmark + multi-color target (preferred environment: `#181818` / `#0A1117`).
- **Light Backgrounds:** Black wordmark + multi-color target.
- **Positioning:** Placed preferentially in the top-left corner or centered in hero layouts.

---

## 5. UI Elements, Shapes & Radii
- **Signature Corner Radius:**
  - **Large Containers, Modals & Slide Cards:** `35px` (`border-radius: 35px` / `rounded-[35px]`).
  - **Standard Cards:** `16px - 20px`.
  - **Buttons & Pills:** `8px - 12px` (or full pill `9999px` for chips).
- **Geometric Elements:** Clean rounded polygons, stars, text underline wings.
- **Modal Windows:** Must support closing via `Escape` key (`e.key === 'Escape'`).

---

## 6. Slide Decks & Interactive Presentations
- **Top Header Bar Rule:** In the presentation top navigation header, show ONLY the clean target logo mark (32px-36px). **NEVER write words, titles, or product names next to it in the header** (e.g. no "navo rates" text).
- **Inner Slides Logo Placement:** On all slides EXCEPT the title cover slide (slides 2 through N), place the official product logo (white version of `navo <Product>MCP` with target 'o') in the top-right of the slide content area. In light mode, wrap in a dark graphite pill (`#0E1626`) for contrast.
- **Title Cover Slide:** Render the title slide cleanly as an intact visual, maintaining the search input bar, route selectors, and action CTA.
- **Dark Graphite Canvas:** Presentations strictly use Dark Graphite (`#181818`) or Product Slate (`#0A1117`) backgrounds.
- **Corner Radii:** Strictly apply signature `35px` border radius (`border-radius: 35px`) to presentation cards and container placeholders.
- **Interactive Controls:**
  - Keyboard: `ArrowLeft`, `ArrowRight`, `Space`, `PageUp`, `PageDown`, `Home`, `End`.
  - Mobile touch swipe support (`touchstart` / `touchend` with >50px delta).
  - Top animated progress bar (`linear-gradient` matching product accent).
  - Slide counter formatted with leading zero (`01 / 10`).
  - Dark/Light theme toggle with `localStorage` persistence.

---

## 7. Vercel & Production Deployments
- **Project Structure:** Standalone directory with `index.html`, `assets/`, and `vercel.json`:
  ```json
  {
    "version": 2,
    "cleanUrls": true,
    "routes": [{ "src": "/(.*)", "dest": "/index.html" }]
  }
  ```
- **Deployment Command:** `vercel <dir> --prod --yes --scope navo5`
- **CLI Authentication:** Omit `--token` flag unless explicitly provided; use the active local CLI session (`navo5` team scope).

---

## 8. Print, Exhibition & Conference Stand Specifications
- Detailed EPS print specifications, header validation, CairoSVG generation script, and conference pitch formulas are documented in `references/print-and-exhibition-specs.md`.

