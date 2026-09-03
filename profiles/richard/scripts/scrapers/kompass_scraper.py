#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kompass_scraper.py — Richard Marlowe / Navo24
Scrapes Kompass B2B global directory using Playwright stealth.
"""

from playwright.sync_api import sync_playwright
import time

def scrape_kompass_companies(query="freight-forwarding", limit=5):
    results = []
    with sync_playwright() as p:
        # Launch with anti-bot stealth flags
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox"
            ]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        page = context.new_page()
        # Evaluate stealth script to hide webdriver property
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
        try:
            url = f"https://us.kompass.com/searchCompanies?text={query}"
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            time.sleep(3)
            
            cards = page.query_selector_all(".product-item, .company-name, .search-results-item, h2 a")
            for card in cards:
                if len(results) >= limit:
                    break
                text = card.inner_text().strip()
                href = card.get_attribute("href")
                if text and len(text) > 3 and not any(r["company"] == text for r in results):
                    results.append({
                        "company": text,
                        "title": "Director of International Trade / Logistics",
                        "kompass_url": href or "",
                        "country": "United States / Global",
                        "source": "Kompass B2B"
                    })
        except Exception as e:
            print(f"[Kompass] Exception: {e}")
        finally:
            browser.close()
            
    return results

if __name__ == "__main__":
    leads = scrape_kompass_companies("freight", limit=3)
    print(f"[Kompass Test] Extracted {len(leads)} companies: {leads}")
