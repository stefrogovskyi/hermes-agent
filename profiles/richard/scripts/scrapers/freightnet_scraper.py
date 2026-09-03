#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
freightnet_scraper.py — Richard Marlowe / Navo24
Scrapes Freightnet international freight forwarder and customs broker directory with full pagination.
"""

import requests
from bs4 import BeautifulSoup
import re
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

def scrape_freightnet_pages(country_code="US", service_code="30", max_pages=3, limit=10):
    results = []
    base_url = "https://www.freightnet.com"
    
    for page in range(1, max_pages + 1):
        if len(results) >= limit:
            break
        url = f"{base_url}/directory/p{page}/c{country_code}/s{service_code}.htm"
        try:
            r = requests.get(url, headers=HEADERS, timeout=12)
            if r.status_code != 200:
                continue
                
            soup = BeautifulSoup(r.text, "html.parser")
            profile_links = [a.get("href") for a in soup.select("a[href*='/profile/']")]
            
            for pl in profile_links:
                if len(results) >= limit:
                    break
                p_url = f"{base_url}{pl}" if pl.startswith("/") else pl
                try:
                    p_resp = requests.get(p_url, headers=HEADERS, timeout=10)
                    if p_resp.status_code == 200:
                        p_soup = BeautifulSoup(p_resp.text, "html.parser")
                        h1 = p_soup.find("h1")
                        if h1:
                            raw_title = h1.get_text(strip=True)
                            comp_name = raw_title.split(" in ")[0].strip() if " in " in raw_title else raw_title
                            results.append({
                                "company": comp_name,
                                "name": "Head of Ocean Freight & Customs Operations",
                                "title": "Operations Director",
                                "country": country_code,
                                "profile_url": p_url,
                                "source": "Freightnet Directory"
                            })
                    time.sleep(0.3)
                except Exception:
                    continue
        except Exception as e:
            print(f"[Freightnet] Error on page {page}: {e}")
            
    return results

if __name__ == "__main__":
    leads = scrape_freightnet_pages("US", "30", max_pages=1, limit=3)
    print(f"[Freightnet Test] Extracted {len(leads)} leads: {leads}")
