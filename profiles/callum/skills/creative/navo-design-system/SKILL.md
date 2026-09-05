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

### 3.1 Authoritative Font Pairing (BrandBook New pp. 24–26)
- **Main Font (Display & Headings):** **Ranade** (Light 300 for expansive display titles, Medium 500 / Bold 700 for headlines & card titles).  
  *Authoritative rule:* Ranade is the official signature display typeface of the brand. Never replace it with generic neo-grotesks (e.g. Plus Jakarta Sans, Inter, or Arial) for major titles.
- **Secondary Font (Body, UI & Descriptions):** **Switzer** (Regular 400, Medium 500, Semibold 600). Used for all body paragraphs, UI elements, subtitles, and explanatory copy.
- **Data, Code & Metrics Font:** **JetBrains Mono** (400, 500, 700). Monospaced font for API endpoints, JSON payloads, container numbers, rates, and timer metrics.

### 3.2 Font CDN Links
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<link href="https://api.fontshare.com/v2/css?f[]=ranade@200,300,400,500,600,700&f[]=switzer@300,400,500,600,700&display=swap" rel="stylesheet">
```

### 3.3 CSS Variables Setup
```css
:root {
  --font-display: 'Ranade', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-body: 'Switzer', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}
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
- **Primary Logo:** Combines the custom geometric `nav` lowercase wordmark with the multi-color concentric target replacing the `o`.
- **Vector Letterforms:** In the `nav` wordmark, the letter **`v` is constructed from two separate, non-touching diagonal strokes** (distinctive master brand geometry).
- **Clear Space:** Minimum clear space around the logo equals the inner diameter of the target ring.
- **Minimum Digital Size:** `70px` width.
- **Theme Inversion Rule for the Target Mark:**
  - **🌙 Dark Theme / Dark Canvas (`#181818` / `#0A1117`):**
    - The outer ring of the bullseye MUST be **pure white (`#FFFFFF`)**.
    - The center dot MUST be **pure white (`#FFFFFF`)**.
    - The wordmark letters `nav` MUST be **pure white (`#FFFFFF`)**.
    - Inner concentric rings retain signature colors (`#113EC9`, `#1F4FE6`, `#E2231A`, `#FF8135`).
  - **☀️ Light Theme / Light Canvas (`#FCFCFC` / `#FFFFFF`):**
    - The outer ring of the bullseye MUST be **pure black (`#000000`)**.
    - The center dot MUST be **pure black (`#000000`)**.
    - The wordmark letters `nav` MUST be **pure black (`#000000`)**.
    - Inner concentric rings retain signature colors.
- **Positioning:** Placed preferentially in the top-left corner or centered in hero layouts.

### 4.1 Product Logos & Lockups (BrandBook p. 21 Rule)
- **NO Generic Colored Text Badges:** On cover slides, hero sections, and navigation cards, **NEVER use plain solid rectangular or pill text badges** (e.g. solid colored pill with "TRACKINGMCP").
- **Authentic Product Logos:** Always represent products via their authentic logo lockups:
  - **Concentric Emblem:** Product-specific 5-ring target mark in the product's palette:
    - **TrackingMCP:** Electric Blue (`#113EC9` -> `#1F4FE6` -> `#18B6B8` -> `#72DEDD` -> white center)
    - **SchedulesMCP:** Ocean Teal (`#18B6B8` -> `#31D8FE` -> `#FF8135` -> `#FBBF24` -> white center)
    - **LoadingMCP:** Signal Orange (`#E2231A` -> `#FF8135` -> `#FFA366` -> `#FBBF24` -> white center)
    - **FreightRatesMCP:** Vivid Purple (`#4928AE` -> `#7044EC` -> `#E2231A` -> `#FF8135` -> white center)
    - **AirCargoMCP:** Sky Cyan (`#0C4A6E` -> `#0284C7` -> `#38BDF8` -> `#BAE6FD` -> white center)
  - **Typography Lockup:** `navo` in lowercase Ranade Light + **[ProductName]** in Bold + **MCP** in the product accent color.
  - **Interactive Navigation:** In digital slide decks, product logo lockups on the cover slide must be interactive (`onclick="updateSlide(N)"`), allowing immediate jumping to that product's dedicated slide.

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
  - Distinct URL deployment: Never overwrite previous presentation URLs; deploy new versions or client-tailored decks to separate Vercel projects.

### 6.1 Pixel-Perfect Non-Editable PowerPoint (.pptx) Export
When exporting web slide decks to PowerPoint for executives, conferences, or partners:
- **Requirement:** Must be 100% pixel-perfect and completely non-editable (locks custom fonts like Ranade and Switzer, protects layout against reflow, and prevents accidental edits).
- **The Golden Rule — Match the 13-Inch Laptop Browser Viewport 1:1:**
  Do NOT attempt to re-engineer or stretch CSS styles into an arbitrary 1920×1080 full-bleed canvas (doing so results in tiny squished text, massive empty dead spaces, or broken flexbox layouts).
  The user approves presentations as they see them on their standard 13-inch laptop. Capture them **directly from the web layout at 1440×900 (16:10 standard 13" laptop viewport) with `device_scale_factor=2` (Retina 2880×1800)**:
  - Preserves exact typography scale, button proportions, card paddings, and header margins 1:1 without inventing new layouts.
  - Automatically eliminates awkward empty dead space.
  - PowerPoint configuration:
    ```python
    prs = Presentation()
    prs.slide_width = Inches(14.4)   # 1440 / 100
    prs.slide_height = Inches(9.0)   # 900 / 100
    blank_layout = prs.slide_layouts[6]
    for i in range(1, total_slides + 1):
        slide = prs.slides.add_slide(blank_layout)
        slide.shapes.add_picture(img_path, left=0, top=0, width=prs.slide_width, height=prs.slide_height)
    ```

- **CRITICAL PITFALL — The Display:Flex Slide Pileup Bug:**
  In single-page slider decks where slides are toggled via an `.active` class (`.slide { display: none; } .slide.active { display: flex; }`):
  - **NEVER** apply `.slide { display: flex !important; }` globally during export. Doing so unhides all slides at once, causing CSS flexbox to crush all 14 slides side-by-side into unreadable 100px vertical columns on every frame.
  - Keep inactive slides strictly hidden (`.slide { display: none !important; }`), and ensure only the active slide is displayed (`.slide.active { display: flex !important; }`).
  - Script reference: `scripts/export-deck-to-pptx.py`.

### 6.2 HTML Email Templates (v6.0 Specification)
When designing B2B and transactional HTML emails under Navo Design System v6.0:
- **Header:** Dark Graphite `#181818` Brand Canvas (never use legacy v5 navy `#0c2a5e`).
- **Logo Lockup:** Inlined vector SVG `navo` logo with pure white text `#FFFFFF` and target `o` (`#113EC9`, `#1F4FE6`, `#E2231A`, `#FF8135`).
- **Domain Badge:** Electric Lime `#CEF868` pill with strict 100% Black text `#000000` (Rule §2.5).
- **Body & Callouts:** Main text in Switzer, callout borders in Electric Cobalt `#1F4FE6`, action pills (Step 1 Cobalt `#1F4FE6` / Step 2 Lime `#CEF868`).
- **Primary CTA:** Electric Cobalt `#1F4FE6` button with MSO VML fallback for Microsoft Outlook.

### 6.3 LinkedIn Social Cards (16:9 2x Retina)
When generating technical social media cards for LinkedIn / X:
- **Dimensions:** 1200×675 viewport rendered at `device_scale_factor=2` (2400×1350 2x Retina PNG).
- **Layout:**
  - Header: Inlined vector `navo` logo + vertical divider + Eyebrow tag in JetBrains Mono (`POST XX // TOPIC`) + Product Pill.
  - Title: Ranade Display (Light 300 / Bold 700, ~34px).
  - Body / Center: Dual-column or 3-step workflow diagram with dark card surfaces (`#141D26`), subtle accent radial glow (`rgba(31,79,230,0.2)` or `rgba(206,248,104,0.15)`), and real UI screenshots or code terminals.
  - Footer: Monospaced footer with URL and call-to-action arrow.
- **Rendering Script:** Use `render-social-card.py` with 2000ms delay to allow Fontshare web fonts (Ranade, Switzer) to render cleanly.

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

## 9. HTML Email & Social Media Card Templates
- Master HTML email template (v6.0 Dark Graphite header, vector logo, Switzer body, Ranade callouts, Cobalt CTA) and LinkedIn 16:9 2x Retina technical card specifications (Patterns A–E: Architectural Flows, Terminal Ledgers, Client-Side Offline Resolvers, Bimodal Metric Charts, and Dual-Column Policies) are documented in `references/email-and-social-templates.md`.
- Automated card rendering: `scripts/render-social-card.py`.

