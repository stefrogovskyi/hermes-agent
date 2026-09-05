# Case: Navo24 Design System v6.0 BrandBook Integration & Web Summit Lisbon 100% CMYK Vector Spec

**Date:** 2026-09-04  
**Profiles involved:** `callum`, `default` (Hermes)  
**Domains:** `business`, `agent_club`

---

## 1. Context & Request
Stefan provided an updated corporate brandbook archive `BrandBook New.zip` (68 slides + vector `18.svg`) to Callum Vance (`@callumvancebot`) to upgrade the existing Navo24 design system (v5.52) into version 6.0, creating both an agent skill and an interactive live artifact. Additionally, for the Web Summit Lisbon ALPHA exhibition stand setup, the portal required an `.EPS` vector logo meeting strict commercial print standards.

---

## 2. Technical Analysis & Challenges
1. **Design System Evolution:**
   - The brand evolved from blue-only palettes to a multi-product umbrella brand centered around the **Target Motif** (the letter "o" in `navo` made of 5 concentric rings).
   - Each product needed distinct color accents while maintaining brand unity.
   - High-contrast rules were needed to avoid unreadable white text on bright promotional backdrops.
2. **Web Summit Print Pre-Flight Validation:**
   - The Web Summit validation system rejected standard RGB PostScript files with orange warnings (`This file uses RGB colors / multiple color spaces`), which risked color drift on physical exhibition boards.
   - Offset printing required 100% CMYK color space definition with pure process black for sharp vector typography.

---

## 3. Implementation & Solutions

### A. Navo24 Design System v6.0
* **Skill Updated:** `profiles/callum/skills/creative/navo-design-system/SKILL.md` updated to v6.0.
* **Interactive Showroom Deployed:** Deployed to Vercel at `https://navo-design-system-showroom.vercel.app`.
* **Canvases:**
  - **Dark Graphite (`#181818`):** Official preferred dark background.
  - **Product SaaS Canvas (`#0A1117`):** Dashboard and analytics interface background.
  - **Light Canvas (`#FCFCFC` / `#FFFFFF`):** High-clarity light theme.
* **Target Motif (5 Concentric Rings):**
  - Ring 1 (Outer): Royal Blue (`#113EC9`)
  - Ring 2: Electric Cobalt Blue (`#1F4FE6`)
  - Ring 3: Rate / Demurrage Red (`#E2231A`)
  - Ring 4: Signal Orange (`#FF8135`)
  - Center: Pure White (`#FFFFFF`) on dark / Black on light.
  - Minimum digital diameter: `70px`.
* **Product Color Differentiation (Umbrella Architecture):**
  - **TrackingMCP:** Electric Blue (`#1F4FE6`)
  - **SchedulesMCP:** Ocean Teal (`#77E6FF` / `#31D8FE`)
  - **LoadingMCP:** Signal Orange (`#FF8135`)
  - **FreightRatesMCP:** Vivid Purple (`#A055FF`) & Rate Red (`#E2231A`)
  - **Promo / High-Energy:** Lime Citron (`#CEF868`) & Gold Yellow (`#FFCF01`)
* **Strict Contrast Rule (§2.5):**
  - On Lime (`#CEF868`), Yellow (`#FFCF01`), and Orange (`#FF8135`), **ONLY 100% black text (`#000000`)** is permitted. White text is strictly forbidden.
* **Geometry:** Card and slide border radius standard set to `35px`.

### B. Web Summit Lisbon 100% CMYK Vector EPS
* Converted the logo descriptor to pure PostScript CMYK (`setcmykcolor` only):
  - Header: `%%DocumentProcessColors: Cyan Magenta Yellow Black`
  - Typography (`nav`): Pure Process Black `0 0 0 1 setcmykcolor` (no RGB/gray mixing).
  - Blue ring: `0.91 0.69 0 0.21 setcmykcolor`
  - Cobalt ring: `0.86 0.66 0 0.10 setcmykcolor`
  - Red ring: `0 0.85 0.88 0.11 setcmykcolor`
  - Orange ring: `0 0.61 0.86 0 setcmykcolor`
  - Center: `0 0 0 0 setcmykcolor`
* Result: Web Summit pre-flight validation checklist passed with 100% green checkmarks on `CMYK color space?`, `No spot colors?`, and `Valid for print?`.

---

## 4. Key Rules & Reflection
1. Whenever exporting brand assets for commercial printing (exhibitions, roll-ups, merch), always output pure CMYK vector PostScript (`.eps` / `.pdf`) with `0 0 0 1 setcmykcolor` for text, never RGB.
2. Maintain both an engineering memory skill (`navo-design-system`) and an interactive Vercel showroom artifact (`navo-design-system-showroom.vercel.app`) for seamless design parity across all agents.
