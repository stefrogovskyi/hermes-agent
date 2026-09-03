#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
apollo_collector.py — Richard Marlowe / Navo24
Searches Apollo.io for real decision makers at:
1. Export / Import & Trading Houses (BCOs, Wholesalers, Commodity & Retail Traders).
2. Large Manufacturing & Industrial Companies shipping containerized freight.
3. Top Freight Forwarders & NVOCCs.
"""

import os
import requests
import json
from dotenv import load_dotenv
from validator import verify_email_domain

load_dotenv("/opt/hermes/profiles/richard/.env")
APOLLO_API_KEY = os.getenv("APOLLO_API_KEY")

TARGET_INDUSTRIES = [
    "import and export",
    "wholesale",
    "international trade and development",
    "manufacturing",
    "food & beverages",
    "chemicals",
    "building materials",
    "logistics and supply chain"
]

TARGET_TITLES = [
    "Head of Logistics",
    "VP Supply Chain",
    "Director of Supply Chain",
    "Import Manager",
    "Export Manager",
    "Global Logistics Manager",
    "Head of Procurement",
    "Director of Global Trade"
]

def search_apollo_bco_leads(page=1, per_page=10):
    if not APOLLO_API_KEY:
        print("[Apollo] Error: APOLLO_API_KEY is missing.")
        return []

    url = "https://api.apollo.io/v1/mixed_people/search"
    headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
        "X-Api-Key": APOLLO_API_KEY
    }
    
    payload = {
        "person_titles": TARGET_TITLES,
        "organization_num_employees_ranges": ["51,200", "201,500", "501,1000", "1001,5000"],
        "page": page,
        "per_page": per_page
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        if response.status_code != 200:
            print(f"[Apollo] API returned status {response.status_code}: {response.text}")
            return []
            
        data = response.json()
        people = data.get("people", [])
        
        valid_leads = []
        for p in people:
            email = p.get("email")
            first_name = p.get("first_name", "")
            last_name = p.get("last_name", "")
            org = p.get("organization", {}) or {}
            company_name = org.get("name", "")
            domain = org.get("primary_domain", "")
            title = p.get("title", "")
            country = p.get("country", "") or org.get("country", "")
            
            # If email is obscured or missing, try constructing from domain if pattern is available, or use verified email
            if email and email != "email_not_unlocked@domain.com":
                if verify_email_domain(email):
                    valid_leads.append({
                        "company": company_name,
                        "name": f"{first_name} {last_name}".strip(),
                        "title": title,
                        "email": email,
                        "website": f"https://{domain}" if domain else "",
                        "country": country or "Global",
                        "industry": org.get("industry", "Trade / Logistics"),
                        "source": "Apollo.io (Trading & BCOs)"
                    })
        return valid_leads
    except Exception as e:
        print(f"[Apollo] Exception: {e}")
        return []

if __name__ == "__main__":
    leads = search_apollo_bco_leads(page=1, per_page=10)
    print(f"[Apollo] Extracted {len(leads)} verified leads.")
    for l in leads[:3]:
        print(l)
