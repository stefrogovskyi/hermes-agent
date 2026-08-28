---
name: screenshot-to-code
description: Replicate UI screenshots into pixel-perfect frontend code.
version: 1.0.0
author: Callum Vance
license: MIT
tags: [frontend, ui, vision, screenshot, css, tailwind, react, html]
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [frontend, ui, vision, screenshot, css, tailwind, react, html]
    related_skills: [navo-design-system, claude-design, sketch]
triggers:
  - screenshot to code
  - replicate screenshot
  - pixel perfect UI
  - convert image to html
  - clone UI from screenshot
  - frontend from mockup
---

# Screenshot to Code Workflow

Proven iterative workflow for turning UI screenshots, mockups, and screen recordings into clean, production-ready frontend components.

## When to Use
- When given a screenshot, design mockup, Figma frame, or screen recording to turn into a frontend screen or component.
- When replicating an existing interface with strict pixel-accuracy requirements.
- When eliminating visual regressions between design reference and rendered code.

## Core Directives

1. **Strict Reference Parity:** Match exact element positions, paddings, typography, colors, and border-radii visible in the reference screenshot. Do not add arbitrary unasked elements or placeholders.
2. **Visual Feedback Loop:** After writing code, render the screen (via Playwright or browser), take a screenshot of the artifact, compare with the reference, and sequentially fix discrepancies.
3. **Clean Architecture:** Separate semantic components, extract repeated elements into reusable cards/rows, and adhere to the active project's design system.

---

## 4-Step Iteration Pipeline

### Step 1: Vision Decomposition & Token Mapping
- Inspect the reference image (`vision_analyze`).
- Identify:
  - Layout structure (Grid, Flexbox, split columns, container bounds).
  - Color palette (Backgrounds, surface cards, primary CTAs, signal accents, borders).
  - Typography hierarchy (Display font, body font, monospace data/tags, font weights, line-heights).
  - Interactive elements (Buttons, tabs, toggles, inputs, badges).

### Step 2: Semantic Implementation
- Implement using the target stack (React, Astro, TailwindCSS, or standalone HTML/CSS).
- Follow design system tokens if active (e.g. Navo24 Ranade/Switzer/JetBrains Mono, Cobalt `#1F4FE6`, Turquoise `#12C2C2`).
- Include state handling (Light/Dark themes, active tab states, modal dialogs with `Escape` key close listeners).

### Step 3: Automated Visual Diffing (The Playwright Loop)
Render and screenshot the generated frontend using Playwright:

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(args=["--no-sandbox", "--disable-setuid-sandbox"])
    context = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
    page = context.new_page()
    page.goto(f"file://{output_html_path}")
    page.wait_for_timeout(1500)
    page.screenshot(path=preview_png_path, full_page=True)
    browser.close()
```

- Pass `preview_png_path` to `vision_analyze` and evaluate against the original screenshot.
- Fix all delta differences (padding tightness, font size, contrast, alignment).

### Step 4: Componentization & Polish
- Extract repeated widgets/cards into modular components.
- Ensure 100% responsiveness (mobile breakpoint clamping, zero horizontal scrollbar leaks).
- Deliver with clear preview/deployment URLs.
