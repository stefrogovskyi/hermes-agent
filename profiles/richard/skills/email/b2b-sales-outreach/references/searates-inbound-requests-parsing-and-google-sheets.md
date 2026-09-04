# SeaRates Inbound Archive Parsing & Google Sheets Pipeline

## Overview
Workflow for extracting, cleaning, and uploading large historical B2B request archives (such as Telegram channel exports or raw Excel files from SeaRates / DFA requests) into an operational Google Sheet pipeline.

## 1. Data Structure & Regular Expression Extraction
Raw message texts typically follow the format:
```text
Plans & Pricing Request / IT Request №...
Tariff: Tracking System API (or Load Calculator / Web access)
From: Client Name [Company Name] [Country]
Phone: +1234567890
Email: client@domain.com
Notes: Client inquiry or requirements...
```

### Parsing Logic
```python
import re

email_re = re.compile(r'Email:\s*([^\s\n\r]+)', re.IGNORECASE)
general_email_re = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
from_re = re.compile(r'From:\s*([^\n\r]+)', re.IGNORECASE)
phone_re = re.compile(r'Phone:\s*([^\n\r]+)', re.IGNORECASE)

def parse_record(msg_text, date_str, source_year):
    msg = str(msg_text or "").strip()
    
    # Extract Email
    em = email_re.search(msg)
    email = em.group(1).strip() if em else ""
    if not email:
        gem = general_email_re.search(msg)
        email = gem.group(0).strip() if gem else ""
        
    # Extract Phone
    ph = phone_re.search(msg)
    phone = ph.group(1).strip() if ph else ""
    
    # Extract Client Name, Company, Country
    client_name, company_name, country = "", "", ""
    fm = from_re.search(msg)
    if fm:
        from_line = fm.group(1).strip()
        brackets = re.findall(r'\[(.*?)\]', from_line)
        client_name = re.sub(r'\[.*?\]', '', from_line).strip()
        if len(brackets) >= 1:
            company_name = brackets[0].strip()
        if len(brackets) >= 2:
            country = brackets[1].strip()
            
    # Extract Service / Tariff
    tariff = ""
    for l in msg.split('\n'):
        l = l.strip()
        if l.lower().startswith("tariff:"):
            tariff = l.split(":", 1)[1].strip()
            break
        elif any(k in l.lower() for k in ["tracking", "load calculator", "logistics explorer", "freight", "schedules"]):
            if not any(l.lower().startswith(p) for p in ["from:", "email:", "phone:"]):
                tariff = l
                break

    notes = msg.split("Notes:", 1)[1].strip() if "Notes:" in msg else ""
    return [client_name, email, company_name, date_str, phone, country, tariff, notes, source_year]
```

## 2. Google Drive Storage Quota: Service Account vs. User OAuth
- **Pitfall**: Google Service Accounts (`*.gserviceaccount.com`) have **0 GB storage quota** on Google Drive by default. Attempting `drive.files().create` or copying files in personal drives returns `HttpError 403: "The user's Drive storage quota has been exceeded."`.
- **Solution**: Use authorized user OAuth credentials (`google_token.json` for Stefan Rogovskiy / `dr.reenforce@gmail.com`). This creates the spreadsheet directly on the user's Google Drive with full storage allocation.

## 3. High-Volume Batch Upload to Google Sheets
For large datasets (10,000+ rows):
1. **Chunking**: Upload values in batches of 2,000–3,000 rows to stay well within Google API payload limits.
2. **Sheet Dimensions**: Set `gridProperties` row count in advance (e.g. 12,000 rows).
3. **Freeze & Style Headers**:
   - Header row: Dark navy fill (`#1A365D`), bold white text, middle aligned, height 40px.
   - Frozen row: `'frozenRowCount': 1`.
   - Column pixel sizing:
     * Client Name: 200px
     * E-mail: 250px
     * Company Name: 230px
     * Request Date: 160px
     * Phone: 170px
     * Country: 140px
     * Service / Tariff: 220px
     * Notes: 380px
     * Source Year: 120px
4. **Permissions**: Create public link access (`type: 'anyone', role: 'writer'` or `'reader'`) and grant explicit editor permissions to team members.

## 4. Resend API Key Replacement & Live Pre-Flight Check
When rotating or updating Resend API keys (`re_...`):
1. Update key across:
   - `/opt/hermes/profiles/richard/.env` (`RESEND_API_KEY=...`)
   - All active engines: `daily_online_outreach_engine.py`, `nikita_forwarders_outreach_engine.py`, `send_weekly_sales_testimonial_reminder.py`, batch dispatchers.
2. **The Dotenv Shell Precedence Trap (`override=True`)**:
   - Python's `load_dotenv()` defaults to `override=False`. If an active terminal session, daemon, or background process previously exported `RESEND_API_KEY`, `load_dotenv()` will silently keep the stale environment variable, causing repeated `401 Unauthorized: "API key is invalid"` even after updating `.env`.
   - Always use `load_dotenv("/opt/hermes/profiles/richard/.env", override=True)` in scripts.
   - When running from a shell, explicitly re-export the new key: `export RESEND_API_KEY="re_..."`.
3. **GitHub Secret Scanning Revocation Incident Management**:
   - Committing files, session dumps, or backup archives containing raw API keys to public or private GitHub repos triggers automated GitHub Secret Scanning partner alerts, which revoke the keys instantly.
   - Ensure strict `.gitignore` protection: `*.env`, `*token*.json`, `*secret*.json`, `backups/`, `sessions/`, `cache/`.
   - Keep secrets strictly in uncommitted `.env` files or GitHub Actions Encrypted Secrets.
4. Verify API key capabilities via `GET https://api.resend.com/domains` (check that `e.navo24.com`, `navo24.com`, `trackingmcp.com` are `status: 'verified'`).
5. Send a live test email to `stefan@navo24.com` and query `GET https://api.resend.com/emails/{email_id}` to confirm `last_event: 'delivered'`.
