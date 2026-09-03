import os
import json
import time
import re
import urllib.request
import urllib.error
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SPREADSHEET_ID = "1INt0_J996CYbuiKxndLtfpCfMEDdgYcuLUaO-xMbDIk"
TOKEN_PATH = "/opt/hermes/google_token.json"

def send_wa(phone, text):
    url = "http://localhost:3050/send-message"
    data = json.dumps({"phone": phone, "message": text}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        try:
            return json.loads(body)
        except Exception:
            return {"error": f"HTTP {e.code}: {body}"}
    except Exception as e:
        return {"error": str(e)}

def dispatch_next_leads(count=5):
    with open(TOKEN_PATH) as f:
        token_data = json.load(f)
    creds = Credentials.from_authorized_user_info(token_data)
    service = build('sheets', 'v4', credentials=creds)

    res = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range="'Leads Pipeline'!A1:O50").execute()
    rows = res.get('values', [])
    if not rows or len(rows) <= 1:
        print("No leads.")
        return []

    results = []
    processed = 0
    for idx, r in enumerate(rows[1:], start=2):
        if len(r) >= 13:
            company = r[4]
            phone = r[5]
            status = r[11]
            pitch = r[12]
            
            if "New" in status and phone and phone != "N/A":
                print(f"[{processed+1}/{count}] Contacting {company} ({phone})...")
                res_send = send_wa(phone, pitch)
                print(f"Response: {res_send}")
                
                if res_send.get('success'):
                    new_status = "Sent via WhatsApp ✅"
                else:
                    err = res_send.get('error', 'Not on WhatsApp')
                    new_status = f"Failed/No WA ({err[:20]})"
                
                service.spreadsheets().values().update(
                    spreadsheetId=SPREADSHEET_ID,
                    range=f"'Leads Pipeline'!L{idx}",
                    valueInputOption='RAW',
                    body={'values': [[new_status]]}
                ).execute()
                
                results.append({"company": company, "phone": phone, "status": new_status})
                processed += 1
                if processed >= count:
                    break
                time.sleep(4)
    return results

if __name__ == "__main__":
    import sys
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    dispatch_next_leads(count)
