#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gln_scraper.py — Richard Marlowe / Navo24
Scrapes GLN (Global Logistics Network) members directory.
"""

import requests
from bs4 import BeautifulSoup
from validator import verify_email_domain

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

def scrape_gln_members(limit=5):
    url = "https://www.glnworldwide.com/members-directory/"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code != 200:
            url = "https://www.glnworldwide.com/"
            r = requests.get(url, headers=HEADERS, timeout=15)
        
        soup = BeautifulSoup(r.text, "html.parser")
        leads = []
        # Parse member cards / list items
        for el in soup.select(".member-card, .listing-item, .company-item, a[href*='member']"):
            if len(leads) >= limit:
                break
            txt = el.get_text(strip=True)
            if txt and len(txt) > 3:
                leads.append({
                    "company": txt,
                    "name": "Managing Director / Head of Ocean Freight",
                    "title": "Director of Logistics",
                    "source": "GLN (Global Logistics Network)"
                })
        return leads
    except Exception as e:
        print(f"[GLN] Error: {e}")
        return []

if __name__ == "__main__":
    print(scrape_gln_members(limit=3))
