#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
prospeo_collector.py — Richard Marlowe / Navo24
Enriches B2B decision makers at Trading, Export/Import, and Freight companies using Prospeo API.
"""

import os
import requests
from dotenv import load_dotenv
from validator import verify_email_domain

load_dotenv("/opt/hermes/profiles/richard/.env")
PROSPEO_API_KEY = os.getenv("PROSPEO_API_KEY")

def find_email_by_domain_and_name(domain: str, first_name: str, last_name: str):
    if not PROSPEO_API_KEY:
        return None
    url = "https://api.prospeo.io/email-finder"
    headers = {
        "Content-Type": "application/json",
        "X-KEY": PROSPEO_API_KEY
    }
    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "company": domain
    }
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=15)
        if r.status_code == 200:
            data = r.json().get("response", {})
            email = data.get("email")
            status = data.get("email_status")
            if email and status in ["VERIFIED", "ACCEPT_ALL"]:
                return email
    except Exception as e:
        print(f"[Prospeo] Error: {e}")
    return None

if __name__ == "__main__":
    em = find_email_by_domain_and_name("maersk.com", "Vincent", "Clerc")
    print(f"[Prospeo Test] Result: {em}")
