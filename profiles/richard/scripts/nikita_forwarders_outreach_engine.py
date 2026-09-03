#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
nikita_forwarders_outreach_engine.py — Richard Marlowe / Nikita Kurudzhy (Navo24)
Executes Touch #1 Outbound Campaign for 100 Forwarders & NVOCC leads from Google Sheet:
https://docs.google.com/spreadsheets/d/1ceJzlfTCQIvJeMoBZfIhxesFxPM9mbV_iAMe6qXEIMo

Delivery Standards:
- From: Nikita Kurudzhy <nikita@e.navo24.com>
- Reply-To: nikita@navo24.com
- CC: nikita@navo24.com, stefan@navo24.com
- Signature: Nikita Kurudzhy, Account Executive (+380932285150)
- Updates Google Sheet row statuses to 'contacted_pending' and Touch 1 Date
"""

import os
import sys
import json
import time
import requests
from datetime import datetime, timezone
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SPREADSHEET_ID = "1ceJzlfTCQIvJeMoBZfIhxesFxPM9mbV_iAMe6qXEIMo"
TOKEN_PATH = "/opt/hermes/google_token.json"
RESEND_API_KEY = "re_HYSmY1vz_JDgFN8YzffnTeT6mR2YnSufo"

SIGNATURE_HTML = """<div style="margin-top: 24px; font-family: Tahoma, Arial, sans-serif; font-size: 13px; color: #334155; line-height: 1.4; text-align: left;">
  <b>Nikita Kurudzhy</b><br>
  <b>Account Executive</b><br>
  <div style="margin: 8px 0 10px 0;">
    <img src="https://bit.ly/4hLg86T" alt="navo" style="height: 35px; width: auto; display: block;" border="0">
  </div>
  API-MCP for Logistics & Trade<br>
  +380932285150<br>
  <a href="mailto:nikita@navo24.com" style="color: #2563eb; text-decoration: underline;">nikita@navo24.com</a><br>
  30 St Mary Axe, London, EC3A 8BF<br>
  <a href="https://www.navo24.com" style="color: #2563eb; text-decoration: underline;">www.navo24.com</a>
</div>"""

def get_sheets_service():
    with open(TOKEN_PATH, 'r') as f:
        token_data = json.load(f)
    creds = Credentials.from_authorized_user_info(token_data)
    return build('sheets', 'v4', credentials=creds)

def format_email_body(text_content):
    # Split paragraphs by double newlines or single newlines
    paragraphs = [p.strip() for p in text_content.split("\n\n") if p.strip()]
    
    # Check if signature is already at the end of text_content and strip "Best,\nNikita\nNavo24"
    cleaned_paras = []
    for p in paragraphs:
        if p.lower().startswith("best,") or p.lower().startswith("best regards,"):
            continue
        cleaned_paras.append(f"<p>{p.replace(chr(10), '<br>')}</p>")
        
    body_html = "\n".join(cleaned_paras)
    
    html = f"""<div style="font-family: Arial, sans-serif; font-size: 14px; color: #1e293b; line-height: 1.6; max-width: 600px; text-align: left;">
{body_html}

<p>Best regards,</p>

{SIGNATURE_HTML}
</div>"""
    return html

def run_outreach(dry_run=False):
    service = get_sheets_service()
    
    # Read sheet data
    range_name = "'🎯 Forwarders & NVOCC'!A2:V101"
    res = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name
    ).execute()
    
    rows = res.get('values', [])
    print(f"Loaded {len(rows)} rows from Google Sheet.")
    
    sent_count = 0
    errors_count = 0
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    next_followup_str = datetime.now(timezone.utc).strftime("%Y-%m-%d") # + 3 days in real life
    
    updates_status = [] # list of (row_idx, status, touch_date, next_date, step)
    
    # Load suppression list
    suppressed_emails = set()
    suppression_file = "/opt/hermes/profiles/richard/cache/optout_suppression_list.json"
    if os.path.exists(suppression_file):
        try:
            with open(suppression_file, "r", encoding="utf-8") as f:
                suppressed_emails = set(x.strip().lower() for x in json.load(f))
        except Exception:
            pass

    for idx, row in enumerate(rows):
        row_num = idx + 2 # 1-based index in Sheet
        
        # Safe extraction
        status = row[1] if len(row) > 1 else ""
        company = row[3] if len(row) > 3 else ""
        contact = row[7] if len(row) > 7 else ""
        email = row[9].strip() if len(row) > 9 and row[9] else ""
        
        if email.lower() in suppressed_emails:
            print(f"Row {row_num}: ⛔ Opt-Out Suppressed email '{email}' for {company} — skipping.")
            continue
        subject = row[13] if len(row) > 13 and row[13] else f"{company} / container tracking feeds"
        touch1_body = row[14] if len(row) > 14 and row[14] else ""
        
        if not email or "@" not in email:
            print(f"Row {row_num}: Invalid email '{email}' for {company} — skipping.")
            continue
            
        if status in ["contacted_pending", "replied_warm", "closed_won"]:
            print(f"Row {row_num}: {company} already in status '{status}' — skipping.")
            continue
            
        if not touch1_body:
            touch1_body = f"Hi {contact},\n\nReaching out regarding ocean tracking at {company}.\n\nWe built Navo24 (founding team and engineers from SeaRates) to give forwarders a clean API across 239 ocean carriers and 97 air cargo carriers, with observed ETAs and automated D&D free-time calculation.\n\nWorth exploring if our free tier (5 active containers/mo) could help your ops team?"
            
        html_content = format_email_body(touch1_body)
        to_formatted = f"{contact} <{email}>" if contact else email
        
        payload = {
            "from": "Nikita Kurudzhy <nikita@e.navo24.com>",
            "to": [to_formatted],
            "cc": ["Nikita Kurudzhy <nikita@navo24.com>", "Stefan Rogovskiy <stefan@navo24.com>"],
            "reply_to": "nikita@navo24.com",
            "subject": subject,
            "html": html_content
        }
        
        if dry_run:
            print(f"[DRY RUN] Would send to {to_formatted} | Subject: {subject}")
            sent_count += 1
            continue
            
        try:
            r = requests.post(
                "https://api.resend.com/emails",
                headers={"Authorization": f"Bearer {RESEND_API_KEY}", "Content-Type": "application/json"},
                json=payload,
                timeout=15
            )
            if r.status_code == 200:
                res_id = r.json().get("id")
                sent_count += 1
                print(f"[{sent_count}/100] ✅ Sent to {contact} ({company}) <{email}> | Resend ID: {res_id}")
                
                # Queue batch update for sheet: Column B (Status), S (Touch 1 Date), T (Next Follow-up), U (Current Step)
                updates_status.append({
                    "range": f"'🎯 Forwarders & NVOCC'!B{row_num}",
                    "values": [["contacted_pending"]]
                })
                updates_status.append({
                    "range": f"'🎯 Forwarders & NVOCC'!S{row_num}:U{row_num}",
                    "values": [[today_str, "2026-09-04", "Touch #1 (Sent)"]]
                })
                
            else:
                errors_count += 1
                print(f"❌ Failed for {email} ({company}) -> HTTP {r.status_code}: {r.text}")
        except Exception as e:
            errors_count += 1
            print(f"❌ Exception for {email}: {e}")
            
        time.sleep(0.4) # Polite rate limiting
        
    # Apply batch updates to Google Sheet
    if updates_status and not dry_run:
        print("\nUpdating Google Sheet statuses...")
        batch_body = {
            "valueInputOption": "USER_ENTERED",
            "data": updates_status
        }
        service.spreadsheets().values().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body=batch_body
        ).execute()
        print("✅ Google Sheet statuses successfully updated to 'contacted_pending'.")
        
    print(f"\n==========================================")
    print(f"🎉 OUTREACH BATCH FINISHED:")
    print(f"Total Sent: {sent_count}")
    print(f"Total Errors: {errors_count}")
    print(f"==========================================")
    return sent_count, errors_count

if __name__ == "__main__":
    run_outreach(dry_run=False)
