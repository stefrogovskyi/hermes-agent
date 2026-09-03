#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
importyeti_bco_scraper.py — Richard Marlowe / Navo24
Scrapes top-tier US BCO Importers & Exporters from ImportYeti sea bills of lading data.
"""

import sys
import json
from playwright.sync_api import sync_playwright

def scrape_importyeti_shippers(query="solar panels", limit=5):
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        try:
            url = f"https://www.importyeti.com/search?q={query}"
            page.goto(url, wait_until="networkidle", timeout=30000)
            
            # Wait for company cards
            page.wait_for_selector(".company-card, .search-result-card, a[href*='/company/']", timeout=15000)
            
            links = page.query_selector_all("a[href*='/company/']")
            for link in links:
                if len(results) >= limit:
                    break
                text = link.inner_text().strip()
                href = link.get_attribute("href")
                if text and len(text) > 3 and not any(r["company"] == text for r in results):
                    results.append({
                        "company": text,
                        "name": "VP of Global Supply Chain / Import Director",
                        "title": "Director of International Logistics",
                        "importyeti_url": f"https://www.importyeti.com{href}" if href.startswith("/") else href,
                        "country": "United States",
                        "industry": f"BCO Importer ({query.title()})",
                        "source": "ImportYeti (US Customs Sea Manifests)"
                    })
        except Exception as e:
            print(f"[ImportYeti] Exception: {e}")
        finally:
            browser.close()
            
    return results

if __name__ == "__main__":
    leads = scrape_importyeti_shippers("machinery", limit=3)
    print(f"[ImportYeti] Extracted {len(leads)} BCO Importers: {leads}")
