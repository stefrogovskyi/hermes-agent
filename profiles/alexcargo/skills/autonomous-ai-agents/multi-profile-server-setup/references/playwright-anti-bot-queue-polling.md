# Playwright Anti-Bot Scraping & Resilient Polling Reference

## 1. Context & Problem
Modern governmental, ticketing, and administrative portals (e.g. State Enterprise Document / e-queue `odesa3.pasport.org.ua`, Cloudflare Managed Challenge, Akamai Bot Manager) strictly block standard HTTP clients (`urllib`, `requests`, `curl`) with `403 Forbidden`, `402 Payment Required`, or challenge redirects (`Just a moment...`, `__cf_chl_tk`).

## 2. Headless Playwright Resilient Pattern
When building recurring watchdog pollers for dynamic queue openings, slot releases, or ticketing systems:

### Python Playwright Async Blueprint
```python
import asyncio
from playwright.async_api import async_playwright

async def check_queue():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Use clean desktop context with real User-Agent & viewport
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        page = await context.new_page()
        try:
            resp = await page.goto("https://odesa3.pasport.org.ua/solutions/e-queue", wait_until="networkidle", timeout=40000)
            await page.wait_for_timeout(4000)
            
            body_text = await page.evaluate("() => document.body.innerText")
            if "Наразі всі місця зайняті" in body_text:
                # Silent state: no slots
                pass
            else:
                # Slots detected -> capture evidence screenshot and dispatch urgent alert
                await page.screenshot(path="/opt/hermes/cache/slot_alert.png")
                # Send immediate notification with direct link
        finally:
            await browser.close()
```

## 3. Recurring Cron Watchdog Rule
- For high-frequency checking (e.g. every 10 minutes), use a `no_agent=True` script cron job.
- **Delivery Semantics:** Design the script to stay completely silent (`stdout` empty or minimal) when no slots are found. Only emit non-empty stdout or fire direct Telegram API alerts when actionable changes (open slots) are detected.
