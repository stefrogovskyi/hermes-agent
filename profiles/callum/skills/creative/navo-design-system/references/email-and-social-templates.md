# Navo24 v6.0 Email & Social Media Specifications

## 1. Transactional & Marketing HTML Email Template (v6.0)
- **Email Container:** 600px max-width, 16px corner radius, `#FFFFFF` on `#F4F5F7` canvas.
- **Header:** Dark Graphite (`#181818`), inline vector `navo` logo (letters `nav` white with separated diagonal strokes on `v`, concentric rings `o`: `#113EC9`, `#1F4FE6`, `#E2231A`, `#FF8135`, white center dot).
- **Domain Pill:** Electric Lime (`#CEF868`) pill with 100% black text (`#000000`, Rule §2.5), JetBrains Mono 11px bold.
- **Typography:**
  - Body & paragraphs: `Switzer`, 15px, line-height 25px, color `#334155`.
  - Step headers / callouts: `Ranade`, 17px, font-weight 600, color `#0B0C0E`.
  - Badges / steps / footer: `JetBrains Mono`.
- **Callout Box («THE BEST PART»):** `#F8FAFC` card with 4px left border in Electric Cobalt (`#1F4FE6`). Step 1 in Cobalt, Step 2 in Electric Lime with black text.
- **Primary CTA:** Electric Cobalt (`#1F4FE6`) button with MSO VML fallback, white text, 8px border radius.
- **Footer:** JetBrains Mono links to `navo24.com`, `trackingmcp.com`, `schedulesmcp.com`, `freightratesmcp.com`.

---

## 2. LinkedIn Feed Social Cards (16:9 2x Retina)
- **Dimensions:** 1200×675 viewport, rendered at 2x Retina (`2400×1350`).
- **Canvas:** Dark Graphite (`#0D131A` / `#181818`) with soft radial accent glow.
- **Header:** Vector `navo` logo + subtle divider `|` + uppercase eyebrow tag (`JetBrains Mono`, 12px, letter-spacing 0.14em) + product badge pill.
- **Headings:** Large Ranade 34px (Light 300 / Bold 700), line-height 1.18.
- **Body & Metrics:** Switzer 14.5px-15px, JetBrains Mono for code/endpoints.
- **Automation:** Render via `scripts/render-social-card.py` with 2000ms delay for Fontshare web fonts.

---

## 3. High-Signal Technical Card Patterns

### Pattern A: Before vs After Architectural Flow
Used for system design evolutions, security shifts, and zero-egress pipelines.
- **Layout:** Top "BEFORE" lane with red accent border (`#FF4D4D`), bottom "AFTER" lane with electric lime border (`#CEF868`).
- **Flow Steps:** Inner `#080D14` step boxes with subtle arrows (`➔`).
- **Stats Quad:** 4-column KPI grid at the bottom (`.stats-row`) with monospaced 22px values and muted uppercase labels.

### Pattern B: API & Terminal Ledger
Used for developer-first billing, CI/CD pipelines, and endpoint transparency.
- **Left Column:** Terminal box (`#080D14`, 1px border, 16px radius, header with HTTP status badge or CI test status).
- **Right Column:** Stack of 3 feature cards (`.cards-stack`), each with a distinct left accent border (Lime `#CEF868`, Teal `#31D8FE`, Cobalt `#1F4FE6`).

### Pattern C: Client-Side Offline Intelligence & Anti-Reconnaissance
Used for client-side validators (ISO 6346 checksums, BIC owner resolution) and security boundaries.
- **Left Column:** Public input mock displaying container/AWB number + offline resolution details (`Zero Network Calls`).
- **Right Column:** Explanatory cards emphasizing the "Deliberate Refusal" rule (never confirming whether an entity exists in private customer databases to prevent competitor reconnaissance).

### Pattern D: Bimodal & Distribution Metric Charts
Used for data engineering diagnostics and carrier reliability analytics.
- **Left Column:** Bar chart box with labeled percentage tracks comparing the healthy cohort against anomalous outliers.
- **Right Column:** Technical takeaways explaining why third-party integrations experience step-function failures rather than smooth degradation.

### Pattern E: Dual-Column Identity & Policy Comparison
Used for pricing models, account uniqueness keys, and anti-abuse policies.
- **Grid:** 2 equal columns with distinct top borders (`border-top: 3px solid var(--lime)` vs `var(--teal)`), highlighting individual control layers (e.g. distinct entity tracking vs normalized mailbox keys).

---

## 4. Multi-Post Social Campaign Guidelines

### Strict Source Document Isolation
When tasked with generating a focused multi-post campaign or deep-dive from specific technical documents (e.g., "only from file A, without file B"):
- **Strict Context Boundary:** Restrict extracted themes, metrics, and narrative exclusively to the requested source files.
- **No Cross-Document Bleed:** Never mix operational bug lists, weekly sprint numbers, or unrelated release logs into conceptual architecture memos unless explicitly requested.
- **Tone & Persona:** Authoritative, direct, developer-to-developer engineering voice. Zero fluff, zero generic marketing clichés. Lead with real metrics, root causes, and architectural trade-offs.
