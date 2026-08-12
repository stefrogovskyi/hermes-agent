# Navo24 Brand Book v5.52 — Design & Aesthetic Guidelines

Quick reference for generating visual assets, graphics, 404 pages, and social creatives compliant with `navo24.com/brand-book`.

## 1. Logo & Mark (§01 & §05)
* **Wordmark**: Lowercase `navo`. The final letter `o` is drawn as **The Disc (7 concentric rings)**.
* **Vector Source**: Download white logo directly from `https://navo24.com/brand/navo-wordmark-white.svg` or dark logo from `https://navo24.com/brand/navo-wordmark.svg`.
* **7-Ring Sequence (Core to Rim)**:
  1. `#FFFFFF` (white core)
  2. `#FFC42E` (gold)
  3. `#FF7A1F` (sun)
  4. `#E2231A` (red)
  5. `#12C2C2` (turquoise)
  6. `#1F4FE6` (cobalt)
  7. `#0C2A5E` (navy)
* **Endorsement**: `by navo24` in JetBrains Mono, lowercase, 10–11px, tracked `+0.08em`.
* **Rule**: Do not add "by navo24" next to the logo when the standalone page/context does not require an explicit product endorsement.

## 2. Color System (§02 & §03 Dark Theme)
* **Dark Ground / Background**: Navy-ink `#0A0E16` or `#0C2A5E` with hairline borders `#212B3D`. (NEVER pure black `#000000`).
* **Light Ground / Paper**: Warm paper `#FCFCFB` / `#FFFFFF` cards, hairline border `#E9E8E3`, Signal Soft `#EEF1FE`.
* **Cobalt Accent**: `#4A86FF` (dark ground) / `#1F4FE6` (light ground).
* **Instrument Amber**: `#E8A33D` (money, attention, metrics — never used inside the logo mark).
* **Borders**: Thin, visible hairlines `#212B3D` or `#E9E8E3`.

## 3. Typography (§04)
* **Ranade**: The Voice / Display font.
  * **Ultralight (200, -0.03em)** for Display headlines (≥46px).
  * **Light (300)** for section headings.
  * **NEVER bold display headlines**.
* **Switzer**: Text grotesque.
  * Extralight (200) for large statements.
  * Regular/Medium (400) for subheads and card copy.
* **JetBrains Mono**: Numbers, labels, eyebrows, code.
  * Eyebrows: Uppercase, tracked `+0.14em`.
  * Figures: Tabular digits.

## 4. Page Anatomy & Copy Rules (§07 & §08)
* **Eyebrow**: `● TERRITORY, NAMED` in JetBrains Mono.
* **The One-Liner Rule**: Supporting subheads/hooks must stretch across the full measure in **one single line**. Trim copy until it fits single-line.
* **Prose Rules**: Spaced em-dash (` — `) is **BANNED from prose**. Use colons, periods, or semicolons.
* **Theme Switching**: Pages should dynamically adapt to user theme (dark vs light) using `theme-light` class, `prefers-color-scheme`, or `localStorage` key.

## 5. Hostinger / Apache `.htaccess` Extensionless Routing & Logo Link Normalization
When configuring extensionless HTML routes on Hostinger / Apache servers:
* **Logo Links**: Ensure logo `href` attributes use `href="/"` (or `href="/uk/"`, `href="/ru/"`, etc.) instead of relative `href="index"` or `href="index.html"`, which cause 404 errors on servers without explicit `/index` rewrites.
* **Redirecting `/index`**: Include explicit 301 redirects for `/index` and `/<lang>/index` in `.htaccess`:
  ```apache
  RewriteRule ^index(\.html)?$ / [R=301,L]
  RewriteRule ^(es|de|fr|it|uk|ru|zh|ar)/index(\.html)?$ /$1/ [R=301,L]
  ```
* **Subfolder `.htaccess`**: Place a dedicated `.htaccess` inside each language subdirectory (`/uk/`, `/ru/`, `/de/`, `/es/`, `/fr/`, `/it/`, `/zh/`, `/ar/`) setting `RewriteBase /<lang>/` and `RewriteRule ^([^/]+)/?$ $1.html [L]`.
