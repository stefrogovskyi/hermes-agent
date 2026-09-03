#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
thomasnet_scraper.py — Richard Marlowe / Navo24
Scrapes ThomasNet directory for US Industrial Manufacturers, Exporters, and Importers using Playwright.
"""

from playwright.sync_api import sync_playwright
import time

def search_thomasnet_companies(keyword="freight-forwarding-services", limit=10):
    leads = []
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage"
            ]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={"width": 1366, "height": 768},
            locale="en-US",
            timezone_id="America/New_York"
        )
        page = context.new_page()
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
        try:
            url = f"https://www.thomasnet.com/products/{keyword}-29850407-1.html"
            print(f"[ThomasNet] Navigating to: {url}")
            page.goto(url, wait_until="domcontentloaded", timeout=45000)
            time.sleep(3)
            
            # Extract cards
            cards = page.query_selector_all("[data-analytics*='supplier-card'], .cop-card, .search-result, article, div[class*='card']")
            print(f"[ThomasNet] Found {len(cards)} raw card elements on page.")
            
            # Alternative: query company links
            comp_links = page.query_selector_all("a[data-analytics*='supplier_name'], h2 a, a[href*='/profile/']")
            for link in comp_links:
                if len(leads) >= limit:
                    break
                name = link.inner_text().strip()
                href = link.get_attribute("href")
                if name and len(name) > 2 and not any(l["company"] == name for l in leads):
                    leads.append({
                        "company": name,
                        "name": "Director of Supply Chain & Logistics",
                        "title": "Supply Chain & Procurement Director",
                        "website": href or "",
                        "country": "United States",
                        "industry": "US Industrial Manufacturing & Trade",
                        "source": "ThomasNet Industrial Directory"
                    })
        except Exception as e:
            print(f"[ThomasNet] Exception: {e}")
        finally:
            browser.close()
            
    return leads

if __name__ == "__main__":
    results = search_thomasnet_companies(limit=5)
    print(f"[ThomasNet Live Test] Extracted {len(results)} companies:")
    for r in results:
        print(f" - {r['company']} ({r['website']})")
