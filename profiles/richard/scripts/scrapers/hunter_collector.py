#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hunter_collector.py — Richard Marlowe / Navo24
Discovers verified decision makers for target trading, export/import, and shipping companies using Hunter.io Domain Search API.
"""

import os
import requests
from dotenv import load_dotenv
from validator import verify_email_domain

load_dotenv("/opt/hermes/profiles/richard/.env")
HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")

# Target high-volume BCO trading & global logistics domains
TARGET_DOMAINS = [
    # Global Commodity & Trading Houses (BCOs)
    "bunge.com",
    "adm.com",
    "louisdreyfus.com",
    "trafigura.com",
    "glencore.com",
    "vitol.com",
    "gunvorgroup.com",
    "olamgroup.com",
    "wilmar-international.com",
    # Global Manufacturing Exporters / Importers
    "arcelormittal.com",
    "tatasteel.com",
    "basf.com",
    "dow.com",
    "danone.com",
    "nestle.com",
    "unilever.com",
    # Global Logistics / Freight Forwarders
    "geodis.com",
    "ceva.com",
    "kuehne-nagel.com",
    "dbschenker.com",
    "expeditors.com",
    "bollore-logistics.com",
    "hellmann.com"
]

def search_hunter_domain(domain: str):
    if not HUNTER_API_KEY:
        print("[Hunter] Error: HUNTER_API_KEY is missing.")
        return []

    url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={HUNTER_API_KEY}&department=logistics,management,executive"
    try:
        r = requests.get(url, timeout=15)
        if r.status_code != 200:
            return []
        data = r.json().get("data", {})
        emails = data.get("emails", [])
        org_name = data.get("organization", domain)
        
        leads = []
        for e in emails:
            email = e.get("value")
            fn = e.get("first_name", "")
            ln = e.get("last_name", "")
            position = e.get("position", "Logistics Executive")
            confidence = e.get("confidence", 0)
            
            if email and confidence >= 70 and verify_email_domain(email):
                leads.append({
                    "company": org_name or domain,
                    "name": f"{fn} {ln}".strip() or "Logistics Director",
                    "title": position,
                    "email": email,
                    "website": f"https://{domain}",
                    "country": "Global",
                    "industry": "Export/Import & Trade",
                    "source": "Hunter.io B2B Intelligence"
                })
        return leads
    except Exception as e:
        print(f"[Hunter] Exception for {domain}: {e}")
        return []

def collect_hunter_leads(limit=10):
    all_leads = []
    for dom in TARGET_DOMAINS:
        if len(all_leads) >= limit:
            break
        leads = search_hunter_domain(dom)
        all_leads.extend(leads)
    return all_leads[:limit]

if __name__ == "__main__":
    leads = collect_hunter_leads(limit=5)
    print(f"[Hunter] Extracted {len(leads)} leads.")
    for l in leads:
        print(l)
