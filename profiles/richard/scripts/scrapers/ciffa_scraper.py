#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ciffa_scraper.py — Richard Marlowe / Navo24
Parses CIFFA (Canadian International Freight Forwarders & Shippers Association) Member Directory.
"""

import requests
import json
from validator import verify_email_domain

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*"
}

def fetch_ciffa_members(limit=10):
    # CIFFA member directory endpoint / search
    url = "https://www.ciffa.com/wp-json/ciffa/v1/members?per_page=50"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            data = r.json()
            leads = []
            for item in data:
                if len(leads) >= limit:
                    break
                company = item.get("company_name") or item.get("name")
                email = item.get("email", "")
                contact_name = item.get("contact_person", "Logistics Operations Manager")
                city = item.get("city", "Toronto")
                
                if company and email and verify_email_domain(email):
                    leads.append({
                        "company": company,
                        "name": contact_name,
                        "title": "Director of Ocean Freight & Customs",
                        "email": email,
                        "website": item.get("website", ""),
                        "country": f"Canada ({city})",
                        "industry": "Freight Forwarding & Customs Brokerage",
                        "source": "CIFFA Canadian Directory"
                    })
            return leads
        else:
            print(f"[CIFFA] Status {r.status_code}")
            return []
    except Exception as e:
        print(f"[CIFFA] Exception: {e}")
        return []

if __name__ == "__main__":
    leads = fetch_ciffa_members(limit=5)
    print(f"[CIFFA] Collected {len(leads)} leads: {leads}")
