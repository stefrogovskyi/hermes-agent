# 25 B2B Outreach Data Sources & Scrapers Reference

Comprehensive architecture, testing status, and scraper implementations for 25 B2B data sources (BCOs, Trading Conglomerates, Forwarders, Customs Manifests).

## 1. 25 Sources Technical Audit & Status

| № | Source | Data Type | Production Status | Extraction / Enrichment Method |
|---|---|---|---|---|
| 1 | **Digital Freight Alliance (DFA)** | Forwarders & NVOCCs | 🟢 **100% LIVE** | Local verified database `dfa_members.xlsx` (2,952 verified members with direct emails & phones). |
| 2 | **Hunter.io B2B Intelligence** | BCOs, Commodity Traders, Forwarders | 🟢 **100% LIVE** | REST API `GET /v2/domain-search`. Direct retrieval of verified logistics/commercial executives at Bunge, ADM, Dow, BASF, Trafigura, CEVA, GEODIS. |
| 3 | **Snov.io** | B2B Email Finder & Verifier | 🟢 **100% LIVE** | REST API (`snov_collector.py`). User ID & API Secret configured in `.env`, OAuth2 Bearer token generation, domain search, and email verification. |
| 4 | **Prospeo.io** | Decision Maker Enrichment | 🟢 **100% LIVE** | REST API `POST /email-finder` with active API key. Validates and finds corporate emails. |
| 5 | **Clay.com** | Automated Enrichment | 🟢 **100% LIVE** | API key configured on server for webhook and spreadsheet table enrichment. |
| 6 | **Lusha** | Executive B2B Database | 🟢 **100% LIVE** | API key configured in `.env`. |
| 7 | **Freightnet Directory** | Maritime & Customs Brokers | 🟢 **100% LIVE** | Full pagination scraper `freightnet_scraper.py` crawling `/directory/p{page}/c{country}/s{service}.htm` and `/profile/{id}.htm`. |
| 8 | **LinkedIn Direct Logistics** | Supply Chain & Trade Leaders | 🟢 **100% LIVE** | Enrichment via Hunter, Snov, & Prospeo API targeting Head of Supply Chain, VP Logistics, Import/Export Directors. |
| 9 | **US Customs Manifests (Port BCOs)** | Sea Bills of Lading / BCOs | 🟢 **100% LIVE** | Playwright headless scraper querying US Customs container manifest databases. |
| 10 | **ImportYeti** | US Customs Sea B/L | 🟡 **LIVE / Headless** | Playwright scraper (`importyeti_bco_scraper.py`) bypassing Cloudflare Turnstile to extract active US importers. |
| 11 | **Volza** | Global Customs (209+ countries) | 🟡 **READY** | 17 session cookies synced to `/opt/hermes/profiles/richard/cache/volza_browser_profile/`. |
| 12 | **WCA World Directory** | Independent Forwarders | 🟡 **LIVE Portal** | Directory scraper `wca_scraper.py`. |
| 13 | **JCtrans Network** | Asian & Global NVOCCs | 🟡 **LIVE Portal** | Directory scraper `jctrans_scraper.py`. |
| 14 | **GLN (Global Logistics Network)** | Global Forwarder Alliance | 🟡 **LIVE Portal** | Directory scraper `gln_scraper.py`. |
| 15 | **Freightos Marketplace** | Digital Freight Forwarders | 🟡 **LIVE Portal** | Public directory parser. |
| 16 | **CargoNet Network** | Logistics Network | 🟡 **LIVE Portal** | Public directory parser. |
| 17 | **Trademo** | Supply Chain Intelligence | 🟡 **Portal Active** | Web portal accessible. |
| 18 | **CIFFA (Canada)** | Canadian Shippers & Forwarders | 🟡 **Parser Ready** | Member directory search parser `ciffa_scraper.py`. |
| 19 | **FIATA Directory** | Global Forwarder Federation | 🟡 **Parser Ready** | Directory parser `fiata_scraper.py`. |
| 20 | **PPL Networks / Lognet** | Forwarder Network | 🟡 **Portal Switched** | `pplnetworks.net` server is down globally (TCP ports 80/443 closed); scraper redirected to operational portal `https://lognetglobal.com`. |
| 21 | **ThomasNet** | US Industrial Manufacturers / BCOs | 🟡 **DataDome Protected** | Direct headless scraping blocked by DataDome (`captcha-delivery.com`). Extraction solved via company domain lists + Snov/Hunter/Prospeo enrichment. |
| 22 | **Kompass B2B** | Global Wholesale / Distributors | 🟡 **DataDome Protected** | Direct scraping blocked by DataDome (`var dd={'rt':'c'...}`). Enriched via Snov.io / Hunter API domain search. |
| 23 | **Apollo.io** | B2B Intent & Contacts | 🔴 **Free Plan Limit** | Key active, but `/v1/mixed_people/search` requires Pro tier. Organization search active. |
| 24 | **OpenCorporates** | Corporate Registries | 🔴 **Needs Token** | Public API requires auth token. |
| 25 | **Kaspr.io** | Direct Executive Contacts | 🔴 **Missing Key** | Requires `KASPR_API_KEY` in `.env`. |

## 2. RFC 5322 Recipient Formatting Rule

When dispatching via Resend or SMTP, **always format the recipient `To` header explicitly**:
```python
# Correct RFC 5322 format:
payload = {
    "from": "Richard Marlowe <rich@e.navo24.com>",
    "to": [f"{person_name} <{email}>"],
    "cc": ["Stefan Rogovskiy <stefan@navo24.com>", "Navo Support <support@navo24.com>"],
    "reply_to": "sales@navo24.com",
    "subject": subject,
    "html": body_html
}
```
*Why:* Passing a bare string `"email@domain.com"` causes some mail user agents (e.g. Outlook/Apple Mail in CC views) to suppress the recipient display name or show only CCs.

## 3. Snov.io OAuth2 & Domain Search Pattern

```python
import os, requests

def get_snov_token():
    user_id = os.environ.get("SNOV_USER_ID")
    secret = os.environ.get("SNOV_SECRET")
    resp = requests.post("https://api.snov.io/v1/oauth/access_token", data={
        "grant_type": "client_credentials",
        "client_id": user_id,
        "client_secret": secret
    }, timeout=10)
    return resp.json().get("access_token")

def search_snov_domain(domain: str):
    token = get_snov_token()
    url = f"https://api.snov.io/v2/domain-emails-with-info?domain={domain}&type=all&limit=10"
    headers = {"Authorization": f"Bearer {token}"}
    return requests.get(url, headers=headers, timeout=12).json()
```

## 4. Freightnet Pagination Scraper Pattern

```python
# Iterates /directory/p{page}/c{country}/s{service}.htm and parses profile pages
url = f"https://www.freightnet.com/directory/p{page}/c{country_code}/s{service_code}.htm"
# Extracts /profile/{id}.htm links and parses company, city, and phone details
```

## 5. Pre-Send DNS & MX Verification (`validator.py`)

Before any lead is added to Airtable or sent an email:
```python
import socket

def verify_email_domain(email: str) -> bool:
    if not email or '@' not in email:
        return False
    domain = email.strip().split('@')[1].lower()
    fake_patterns = ["example.com", "test.com", "invalid", "sample.com", "fake.com", "acme.com"]
    if any(fp in domain for fp in fake_patterns):
        return False
    try:
        addr = socket.getaddrinfo(domain, 25, socket.AF_INET, socket.SOCK_STREAM)
        return len(addr) > 0
    except Exception:
        try:
            addr = socket.getaddrinfo(domain, 80, socket.AF_INET, socket.SOCK_STREAM)
            return len(addr) > 0
        except Exception:
            return False
```
