#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
snov_collector.py — Richard Marlowe / Navo24
Discovers verified decision makers for target companies using Snov.io Domain Search API.
"""

import os
import requests
from dotenv import load_dotenv
from validator import verify_email_domain

load_dotenv("/opt/hermes/profiles/richard/.env")
SNOV_CLIENT_ID = os.getenv("SNOV_CLIENT_ID")
SNOV_CLIENT_SECRET = os.getenv("SNOV_CLIENT_SECRET")

def get_snov_token():
    if not SNOV_CLIENT_ID or not SNOV_CLIENT_SECRET:
        return None
    url = "https://api.snov.io/v1/oauth/access_token"
    data = {
        "grant_type": "client_credentials",
        "client_id": SNOV_CLIENT_ID,
        "client_secret": SNOV_CLIENT_SECRET
    }
    try:
        r = requests.post(url, data=data, timeout=12)
        if r.status_code == 200:
            return r.json().get("access_token")
    except Exception:
        pass
    return None

def search_snov_domain(domain: str, limit: int = 5):
    token = get_snov_token()
    if not token:
        return []
    url = f"https://api.snov.io/v2/domain-emails-with-info?domain={domain}&type=all&limit={limit}"
    headers = {"Authorization": f"Bearer {token}"}
    leads = []
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            data = r.json()
            for item in data.get("emails", []):
                em = item.get("email")
                if em and verify_email_domain(em):
                    leads.append({
                        "name": f"{item.get('firstName', '')} {item.get('lastName', '')}".strip() or "Logistics Director",
                        "title": item.get("position", "Logistics & Supply Chain Manager"),
                        "email": em.strip().lower(),
                        "company": domain.split(".")[0].capitalize(),
                        "domain": domain,
                        "source": f"Snov.io Domain Search ({domain})"
                    })
    except Exception as e:
        print(f"Snov search error for {domain}: {e}")
    return leads
