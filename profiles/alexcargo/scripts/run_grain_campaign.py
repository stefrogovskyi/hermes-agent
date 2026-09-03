#!/usr/bin/env python3
"""
Grain Outreach Campaign Dispatcher
Sends personalized emails sequentially with anti-spam pacing (10-20s delay),
updates the Google Spreadsheet tracker and local Excel/CSV files in real-time.
"""

import os
import sys
sys.path.insert(0, "/opt/hermes/profiles/alexcargo/scripts")
import time
import json
import random
import datetime
import pandas as pd
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

import email_client

TRACKER_XLSX = "/root/grain_outreach_tracker.xlsx"
TRACKER_CSV = "/root/grain_outreach_tracker.csv"
GOOGLE_TOKEN_PATH = "/opt/hermes/profiles/harrison/google_token.json"
SPREADSHEET_ID = "1myIArwPaeaYjCnN85cq6qJQJJNmfCaHxGrm-1_ugyaw"

def update_google_sheet(df):
    """Update Google Sheet with current dataframe."""
    try:
        with open(GOOGLE_TOKEN_PATH) as f:
            token_data = json.load(f)
        creds = Credentials.from_authorized_user_info(token_data)
        sheets_service = build("sheets", "v4", credentials=creds)
        
        # Prepare values
        header = list(df.columns)
        # Convert nan to empty string
        values = [header] + df.fillna("").astype(str).values.tolist()
        
        body = {
            "values": values
        }
        sheets_service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range="Grain Outreach Tracker!A1",
            valueInputOption="RAW",
            body=body
        ).execute()
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Google Sheet updated successfully.")
    except Exception as e:
        print(f"Error updating Google Sheet: {e}")

def run_campaign(batch_size=50, min_delay=12, max_delay=25):
    if not os.path.exists(TRACKER_XLSX):
        print(f"Tracker file {TRACKER_XLSX} not found!")
        return
        
    df = pd.read_excel(TRACKER_XLSX)
    print(f"Loaded {len(df)} leads from tracker.")
    
    sent_count = 0
    error_count = 0
    
    for idx, row in df.iterrows():
        status = str(row.get("Status", "")).strip()
        email = str(row.get("Email", "")).strip()
        subject = str(row.get("Subject Line", "")).strip()
        body = str(row.get("Personalized Email Body", "")).strip()
        company = str(row.get("Company", "")).strip()
        
        if status.lower() == "sent":
            print(f"Row {idx+1}: {email} already sent, skipping.")
            continue
            
        if not email or "@" not in email:
            df.at[idx, "Status"] = "Invalid Email"
            continue
            
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Sending lead #{idx+1}/{len(df)}: {company} ({email})...")
        print(f"  Subject: {subject[:60]}...")
        
        try:
            res = email_client.send_email(email, subject, body)
            if res.get("success"):
                sent_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                df.at[idx, "Status"] = "Sent"
                df.at[idx, "Sent At"] = sent_time
                sent_count += 1
                print(f"  ✓ Sent successfully at {sent_time}")
            else:
                df.at[idx, "Status"] = f"Error: {res.get('error')}"
                error_count += 1
                print(f"  ✗ Error sending: {res.get('error')}")
        except Exception as e:
            df.at[idx, "Status"] = f"Failed: {e}"
            error_count += 1
            print(f"  ✗ Exception: {e}")
            
        # Save local files after each send
        df.to_excel(TRACKER_XLSX, index=False)
        df.to_csv(TRACKER_CSV, index=False, encoding="utf-8-sig")
        
        # Update Google Sheet every 5 sends or on last
        if sent_count % 5 == 0 or idx == len(df) - 1:
            update_google_sheet(df)
            
        if sent_count >= batch_size:
            print(f"Reached batch limit of {batch_size} emails.")
            break
            
        delay = random.uniform(min_delay, max_delay)
        print(f"  Pacing delay: {delay:.1f}s...")
        time.sleep(delay)
        
    update_google_sheet(df)
    print(f"\n🎉 Campaign Finished: Sent {sent_count} emails, Errors {error_count}.")

if __name__ == "__main__":
    run_campaign()
