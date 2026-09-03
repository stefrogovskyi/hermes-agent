#!/usr/bin/env python3
"""
Grain Outreach Response Monitor & Bounce Cleaner (Auto-Delete Dead Leads)
Checks INBOX on contact@cargosavior.com for:
1. Genuine Prospect Inquiries (Lead Alerts)
2. Delivery Bounces / NDRs -> AUTOMATICALLY DELETES dead/unreachable rows from Google Sheet & local tracker!
"""

import os
import sys
sys.path.insert(0, "/opt/hermes/profiles/alexcargo/scripts")
import re
import json
import time
import email
import imaplib
import datetime
from email.header import decode_header
import pandas as pd
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

EMAIL_USER = "contact@cargosavior.com"
EMAIL_PASS = "Cargo#171004"
IMAP_SERVER = "imap.hostinger.com"
IMAP_PORT = 993

TRACKER_XLSX = "/root/grain_outreach_tracker.xlsx"
TRACKER_CSV = "/root/grain_outreach_tracker.csv"
GOOGLE_TOKEN_PATH = "/opt/hermes/profiles/harrison/google_token.json"
SPREADSHEET_ID = "1myIArwPaeaYjCnN85cq6qJQJJNmfCaHxGrm-1_ugyaw"
SEEN_MSGS_FILE = "/root/seen_inbox_uids.json"

def decode_mime_words(s):
    if not s:
        return ""
    decoded_parts = decode_header(s)
    res = []
    for part, enc in decoded_parts:
        if isinstance(part, bytes):
            res.append(part.decode(enc or "utf-8", errors="ignore"))
        else:
            res.append(str(part))
    return "".join(res)

def get_email_body(msg):
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get("Content-Disposition"))
            if ctype in ["text/plain", "message/delivery-status", "text/rfc822-headers"] and "attachment" not in cdispo:
                payload = part.get_payload(decode=True)
                if payload:
                    body += "\n" + payload.decode(part.get_content_charset() or "utf-8", errors="ignore")
            elif ctype == "text/html" and not body and "attachment" not in cdispo:
                payload = part.get_payload(decode=True)
                if payload:
                    body = payload.decode(part.get_content_charset() or "utf-8", errors="ignore")
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            body = payload.decode(msg.get_content_charset() or "utf-8", errors="ignore")
    return body.strip()

def update_google_sheet(df):
    """Sync dataframe changes to Google Spreadsheet (clears old range and rewrites cleanly)."""
    try:
        with open(GOOGLE_TOKEN_PATH) as f:
            token_data = json.load(f)
        creds = Credentials.from_authorized_user_info(token_data)
        sheets_service = build("sheets", "v4", credentials=creds)
        
        # Clear sheet first to remove leftover rows if we pruned/deleted items
        sheets_service.spreadsheets().values().clear(
            spreadsheetId=SPREADSHEET_ID,
            range="Grain Outreach Tracker!A1:Z100"
        ).execute()
        
        header = list(df.columns)
        values = [header] + df.fillna("").astype(str).values.tolist()
        
        body = {"values": values}
        sheets_service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range="Grain Outreach Tracker!A1",
            valueInputOption="RAW",
            body=body
        ).execute()
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Google Spreadsheet updated cleanly ({len(df)} rows).")
    except Exception as e:
        print(f"Error syncing to Google Sheet: {e}")

def extract_bounced_email(body_text, subject_text):
    """Detect bounced email address from NDR text."""
    # Pattern 1: Final-Recipient: rfc822; user@domain.com
    m = re.search(r"Final-Recipient:\s*(?:rfc822;)?\s*([^\s;<>]+@[^\s;<>]+)", body_text, re.IGNORECASE)
    if m:
        return m.group(1).strip()
        
    # Pattern 2: Original-Recipient: rfc822; user@domain.com
    m = re.search(r"Original-Recipient:\s*(?:rfc822;)?\s*([^\s;<>]+@[^\s;<>]+)", body_text, re.IGNORECASE)
    if m:
        return m.group(1).strip()
        
    # Pattern 3: <user@domain.com> ... 550 / User not found
    m = re.search(r"<([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)>.*?(?:550|554|does not exist|User unknown|No such user|Recipient address rejected|not found|disabled|mailbox unavailable)", body_text, re.IGNORECASE | re.DOTALL)
    if m:
        return m.group(1).strip()

    # Pattern 4: Match against existing tracked leads
    if os.path.exists(TRACKER_XLSX):
        try:
            temp_df = pd.read_excel(TRACKER_XLSX)
            for em in temp_df["Email"].dropna():
                if str(em).lower() in body_text.lower() or str(em).lower() in subject_text.lower():
                    return str(em).lower().strip()
        except Exception:
            pass
            
    return None

def check_for_replies_and_bounces():
    seen_uids = []
    if os.path.exists(SEEN_MSGS_FILE):
        try:
            with open(SEEN_MSGS_FILE, "r") as f:
                seen_uids = json.load(f)
        except Exception:
            seen_uids = []

    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("INBOX")
        status, msgs = mail.search(None, "ALL")
        if status != "OK" or not msgs[0]:
            mail.logout()
            return [], []

        msg_ids = msgs[0].split()
        new_replies = []
        new_bounces = []
        current_uids = []
        bounced_emails_to_delete = set()
        table_modified = False

        df = pd.read_excel(TRACKER_XLSX) if os.path.exists(TRACKER_XLSX) else None

        for num in msg_ids:
            uid_str = num.decode("utf-8")
            current_uids.append(uid_str)
            if uid_str in seen_uids:
                continue

            status, data = mail.fetch(num, "(RFC822)")
            if status != "OK":
                continue

            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            from_header = decode_mime_words(msg.get("From", ""))
            subject = decode_mime_words(msg.get("Subject", ""))
            date_header = msg.get("Date", "")
            body = get_email_body(msg)

            email_match = re.search(r"[\w\.-]+@[\w\.-]+", from_header)
            sender_email = email_match.group(0).lower() if email_match else from_header.lower()

            if sender_email == EMAIL_USER.lower() or any(s in sender_email for s in ["hostinger.com", "google.com", "noreply", "no-reply"]):
                continue

            # Check if this is a BOUNCE / NDR notification
            is_bounce = any(k in from_header.lower() for k in ["mailer-daemon", "postmaster", "delivery status", "mail delivery", "mail-daemon"]) or \
                        any(k in subject.lower() for k in ["undelivered", "delivery failure", "failure notice", "returned mail", "undeliverable", "delivery status notification"])

            if is_bounce:
                bounced_email = extract_bounced_email(body, subject)
                if bounced_email:
                    bounced_clean = bounced_email.lower().strip()
                    bounced_emails_to_delete.add(bounced_clean)
                    print(f"🚨 Bounce detected for: {bounced_clean}")

                new_bounces.append({
                    "bounced_email": bounced_email,
                    "subject": subject,
                    "date": date_header
                })
                continue

            # Genuine prospect reply
            company_match = "Prospect"
            if df is not None:
                match_row = df[df["Email"].str.lower() == sender_email]
                if not match_row.empty:
                    company_match = match_row.iloc[0]["Company"]
                    idx = match_row.index[0]
                    df.at[idx, "Status"] = "Replied / Lead Inbound"
                    df.at[idx, "Response / Follow-up"] = f"[{datetime.datetime.now().strftime('%d-%m %H:%M')}] {body[:150]}"
                    table_modified = True

            new_replies.append({
                "uid": uid_str,
                "from": from_header,
                "sender_email": sender_email,
                "company": company_match,
                "subject": subject,
                "date": date_header,
                "body_snippet": body[:500]
            })

        # DELETE BOUNCED / DEAD LEADS FROM TABLE
        if bounced_emails_to_delete and df is not None:
            initial_count = len(df)
            df = df[~df["Email"].str.lower().isin(bounced_emails_to_delete)].reset_index(drop=True)
            # Re-index IDs
            df["ID"] = range(1, len(df) + 1)
            pruned_count = initial_count - len(df)
            print(f"🗑️ Deleted {pruned_count} dead/bounced leads from tracker! Remaining active: {len(df)}")
            table_modified = True

        if table_modified and df is not None:
            df.to_excel(TRACKER_XLSX, index=False)
            df.to_csv(TRACKER_CSV, index=False, encoding="utf-8-sig")
            update_google_sheet(df)

        with open(SEEN_MSGS_FILE, "w") as f:
            json.dump(current_uids, f)

        mail.logout()
        return new_replies, new_bounces

    except Exception as e:
        print(f"Error checking IMAP: {e}")
        return [], []

if __name__ == "__main__":
    replies, bounces = check_for_replies_and_bounces()
    if bounces:
        print(f"🧹 Cleaned/Deleted {len(bounces)} dead leads from tracker.")
    if replies:
        print(f"🔥 FOUND {len(replies)} NEW PROSPECT REPLIES!")
        for r in replies:
            print(f"\n==============================")
            print(f"From: {r['from']} (Company: {r['company']})")
            print(f"Subject: {r['subject']}")
            print(f"Body snippet:\n{r['body_snippet']}")
    if not replies and not bounces:
        print("Inbox clean. No new replies or bounces.")
