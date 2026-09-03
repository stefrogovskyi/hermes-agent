import json
import time
import requests
import gspread
from datetime import datetime, timezone

SPREADSHEET_ID = "1ceJzlfTCQIvJeMoBZfIhxesFxPM9mbV_iAMe6qXEIMo"
RESEND_API_KEY = "re_HYSmY1vz_JDgFN8YzffnTeT6mR2YnSufo"

SIGNATURE_HTML = """<div style="margin-top: 24px; font-family: Tahoma, Arial, sans-serif; font-size: 13px; color: #334155; line-height: 1.4; text-align: left;">
  <b>Nikita Kurudzhy</b><br>
  <b>Account Executive</b><br>
  <div style="margin: 8px 0 10px 0;">
    <img src="https://navo24.com/favicon.ico" alt="navo" style="height: 28px; width: auto; display: block;" border="0">
  </div>
  API-MCP for Logistics & Trade<br>
  +380 93 228 5150<br>
  <a href="mailto:nikita@navo24.com" style="color: #2563eb; text-decoration: underline;">nikita@navo24.com</a><br>
  30 St Mary Axe, London, EC3A 8BF<br>
  <a href="https://www.navo24.com" style="color: #2563eb; text-decoration: underline;">www.navo24.com</a>
</div>"""

gc = gspread.service_account(filename='/opt/hermes/profiles/richard/google_service_account.json')
sh = gc.open_by_key(SPREADSHEET_ID)
ws = sh.worksheet('🎯 Forwarders & NVOCC')

rows = ws.get_all_values()
batch2_leads = rows[101:] # rows from 102 to 201 (leads 101 to 200)

print(f"Loaded {len(batch2_leads)} leads for Batch 2 dispatch.")

sent_count = 0
errors_count = 0
today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

for idx, r in enumerate(batch2_leads, 101):
    row_num = idx + 1 # 1-based row index in Google Sheet
    comp = r[3].strip()
    email = r[6].strip()
    contact = r[7].strip()
    subject = r[16].strip()
    body_text = r[17].strip()
    
    if not email or "@" not in email:
        print(f"Row {row_num}: Invalid email '{email}' for {comp} — skipping.")
        continue
        
    paragraphs = [p.strip() for p in body_text.split("\n\n") if p.strip()]
    cleaned_paras = [f"<p>{p.replace(chr(10), '<br>')}</p>" for p in paragraphs if not p.lower().startswith("best")]
    
    html_content = f"""<div style="font-family: Arial, sans-serif; font-size: 14px; color: #1e293b; line-height: 1.6; max-width: 600px; text-align: left;">
{"\n".join(cleaned_paras)}

<p>Best regards,</p>

{SIGNATURE_HTML}
</div>"""

    to_formatted = f"{contact} <{email}>" if contact and contact != 'Logistics Operations Team' else email
    
    payload = {
        "from": "Nikita Kurudzhy <nikita@e.navo24.com>",
        "to": [to_formatted],
        "cc": ["Nikita Kurudzhy <nikita@navo24.com>", "Stefan Rogovskiy <stefan@navo24.com>"],
        "reply_to": "nikita@navo24.com",
        "subject": subject,
        "html": html_content
    }
    
    try:
        res = requests.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {RESEND_API_KEY}", "Content-Type": "application/json"},
            json=payload,
            timeout=12
        )
        if res.status_code == 200:
            sent_count += 1
            res_id = res.json().get("id")
            print(f"[{sent_count}/100] ✅ Sent to {contact} ({comp}) <{email}> | Resend: {res_id}")
            
            # Update Sheet Row Status
            ws.update_cell(row_num, 2, 'sent')
            ws.update_cell(row_num, 3, f'Touch 1 Sent ({today_str})')
        else:
            errors_count += 1
            print(f"❌ Error for {email} ({comp}) -> HTTP {res.status_code}: {res.text}")
    except Exception as e:
        errors_count += 1
        print(f"❌ Exception for {email}: {e}")
        
    time.sleep(0.5) # Polite dispatch delay

# Update Dashboard
ws_dash = sh.worksheet('📊 Monthly Dashboard')
ws_dash.update_cell(5, 3, 200) # Sent = 200
print(f"\n🎉 Finished Batch 2: Sent {sent_count}, Errors {errors_count}. Monthly Dashboard updated!")
