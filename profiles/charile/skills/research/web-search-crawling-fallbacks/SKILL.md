---
name: web-search-crawling-fallbacks
description: "Free search, scraping, and document extraction fallbacks."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Search, Scraping, Fallbacks, DuckDuckGo, DDGS, Playwright, Documents]
    related_skills: [blocked-page-recovery, ocr-and-documents]
---

# Web Search & Crawling Fallbacks

## When to Use
Use when standard paid search/crawling APIs (e.g. Firecrawl, Tavily, SerpAPI) fail with `Payment Required`, quota exhaustion, or rate limits. Also use when extracting text from local documents or handling dynamic JS SPAs.

## 1. Direct Web Search via `ddgs` (Zero-Key DuckDuckGo API)

When `web_search` fails due to credit limits, use python's `ddgs` library directly in terminal/scripts:

```python
from ddgs import DDGS

def search_web(query: str, max_results: int = 10):
    with DDGS() as ddgs:
        return list(ddgs.text(query, max_results=max_results))
```

- **Features**: Free, requires no API keys, supports local/regional search and language filters.
- **Package name**: Ensure `ddgs` is used (the legacy `duckduckgo_search` has been migrated to `ddgs`).

## 2. Dynamic Single-Page Applications via Local Playwright

When pages use heavy JavaScript or anti-bot interstitials that static HTTP requests cannot read:

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url, timeout=30000, wait_until="networkidle")
    content = page.content()
    browser.close()
```

## 3. Local Document Parsing (PDF / DOCX)

Instead of sending documents to cloud extraction endpoints:
- **DOCX**: Use `python-docx` for structured extraction of paragraphs, tables, and metadata.
- **PDF**: Use `pymupdf` (`import fitz`) for fast text layer extraction or `marker-pdf` for complex scanned documents.

## Pitfalls & Best Practices

1. **Do not fabricate output**: If search returns empty lists, broaden the query terms or test Ukrainian/Russian keywords for local CIS/EU markets.
2. **Handle rate limits gracefully**: Add light delays (`time.sleep(1.0)`) when executing sequential batch queries through `ddgs`.
