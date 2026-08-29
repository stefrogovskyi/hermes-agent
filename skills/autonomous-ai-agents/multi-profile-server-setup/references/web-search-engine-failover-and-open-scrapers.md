# Autonomous Web Search Engines & OpenSource Crawlers

## Context & Problem
- **Firecrawl API Token Depletion:** When using Firecrawl as a default `web_search` backend, API credit exhaustion results in hard HTTP 402 / `Payment Required` errors, breaking agent web navigation and live searches.
- **Chrome / Browser Automation Headless Disconnect:** Dedicated headless automation Chrome instances may not be active (`BU_CDP_URL=http://127.0.0.1:9223 Connection refused`), rendering browser-based interactive scraping unavailable.

## Solution Architecture: Multi-Engine Fallback

### 1. Zero-Cost Native DuckDuckGo Engine (ddgs)
To provide unlimited, 100% autonomous web searches without relying on paid third-party API keys or credits:
- Install Python `ddgs` library:
  ```bash
  pip install ddgs
  ```
- Configure Hermes Agent to use `ddgs` as the active search backend:
  ```bash
  hermes config set web.search_backend ddgs
  ```
- Programmatic Python query structure:
  ```python
  from ddgs import DDGS
  results = list(DDGS().text("search query", max_results=5))
  # Returns: [{'title': '...', 'href': 'https://...', 'body': '...'}]
  ```

### 2. Headless Playwright Chromium for Dynamic & WAF-Protected Portals
For parsing dynamic JavaScript SPA websites (React, Vue, Angular), business registries, or portals protected by anti-bot checks:
- Leverage installed Playwright binaries:
  ```python
  from playwright.sync_api import sync_playwright
  with sync_playwright() as p:
      browser = p.chromium.launch(headless=True)
      page = browser.new_page()
      page.goto("https://target-portal.com", wait_until="networkidle")
      content = page.content()
      browser.close()
  ```

### 3. Local Document Parsing Without Paid External OCR
- For Word documents (`.docx`):
  ```python
  from docx import Document
  doc = Document("path/to/file.docx")
  text = "\n".join([p.text for p in doc.paragraphs])
  ```
- For PDFs & Multi-page tables: Use `pymupdf` (PyMuPDF) for instant local text/table extraction without cloud tokens.
