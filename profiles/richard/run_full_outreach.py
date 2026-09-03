import pandas as pd
import requests, time, os, json, datetime

RESEND_API_KEY = "re_HYSmY1vz_JDgFN8YzffnTeT6mR2YnSufo"
file_path = "/opt/hermes/profiles/richard/cache/documents/doc_4c307c778c3f_Customers.xlsx"
log_path = "/opt/hermes/profiles/richard/customers_outreach_log.json"
progress_log = "/opt/hermes/profiles/richard/customers_outreach_full.log"

df = pd.read_excel(file_path)
subject = "Important Update: Digital Logistics Portfolio Transition & Navo24 Technology"

def get_body_html(customer_name):
    clean_name = str(customer_name).strip() if pd.notna(customer_name) and str(customer_name).strip() else "Partner"
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.6; color: #1e293b; background-color: #ffffff; margin: 0; padding: 0; }}
  .container {{ max-width: 620px; margin: 0 auto; padding: 24px 20px; }}
  p {{ margin: 0 0 16px 0; }}
  a {{ color: #2563eb; text-decoration: underline; }}
  .highlight-box {{ background-color: #f8fafc; border-left: 4px solid #3b82f6; padding: 14px 16px; margin: 18px 0; border-radius: 0 6px 6px 0; }}
  .signature {{ margin-top: 28px; padding-top: 18px; border-top: 1px solid #e2e8f0; font-family: Tahoma, Arial, sans-serif; font-size: 13px; color: #334155; line-height: 1.4; }}
</style>
</head>
<body>
<div class="container">
  <p>Dear {clean_name},</p>

  <p>My name is Richard, contacting you on behalf of <b>Navo24</b>, the project founded by core SeaRates team to supporting the clients with digital logistics technology in the age of AI and automation.</p>

  <p>We know some of our ex-SeaRates customers received a notification, some didn't, but this email is to notify you on the landscape on behalf of ex-SeaRates team. According to the recent internal corporate decisions on business strategy consolidation and brand aggregation, the suspension of Digital brands portfolio, including SeaRates and DFA was announced.</p>

  <p>Since many of SeaRates services and products has already started giving bad response due to cease of fueling, you can see the trajectory where eventually all products and services soon will no longer be available under SeaRates.</p>

  <div class="highlight-box">
    <p style="margin: 0;"><b>Regarding Subscriptions & Refunds:</b><br>
    If you have an active paid subscription (API, web-access, web-integration etc), we recommend contacting respective SeaRates team looking after refunds - contacts mentioned on SeaRates website in the top notification under your login.</p>
  </div>

  <p>Next, let me share you briefly the Navo intro. It was founded by the leadership team standing behind SeaRates as a next step of evolution in service provision boosted with AI power and grounded on experience and skills of SeaRates team. You can find full information at <a href="https://navo24.com" target="_blank">navo24.com</a>, where we are actively updating the roadmap, mission and vision now. For the service provision and products, please visit our developer portal <a href="https://navo24.com/developers/" target="_blank">https://navo24.com/developers/</a>.</p>

  <p>Please also note Navo is not connected to other individuals, brands and products declaring any kind of connection to SeaRates.</p>

  <p>We would be happy to arrange a demo and provide you with test access to Navo24. Please feel free to contact us at <a href="mailto:sales@navo24.com">sales@navo24.com</a>, and our team will be happy to assist you.</p>

  <p>If you were already contacted by your Navo24 account manager, please keep the communication going — and we are thankful for your trust!</p>

  <div class="signature">
    <b>Richard Marlowe</b><br>
    <b>Connections Manager</b><br>
    <div style="margin: 8px 0 10px 0;">
      <img src="https://bit.ly/4hLg86T" alt="navo" style="height: 35px; width: auto; display: block;" border="0">
    </div>
    API-MCP for Logistics & Trade<br>
    +44 203 440 9800<br>
    <a href="mailto:rich@navo24.com" style="color: #2563eb; text-decoration: underline;">rich@navo24.com</a><br>
    30 St Mary Axe, London, EC3A 8BF<br>
    <a href="https://www.navo24.com" style="color: #2563eb; text-decoration: underline;">www.navo24.com</a>
  </div>
</div>
</body>
</html>
"""

# Load existing sent logs
sent_emails = set()
if os.path.exists(log_path):
    try:
        with open(log_path, "r") as f:
            existing = json.load(f)
            for item in existing:
                if item.get("success") and item.get("email"):
                    sent_emails.add(item.get("email").strip().lower())
    except Exception as e:
        print(f"Error reading existing log: {e}")

total_customers = len(df)
print(f"[{datetime.datetime.utcnow().isoformat()}] Starting outreach. Total rows: {total_customers}, Already sent: {len(sent_emails)}")

success_count = len(sent_emails)
error_count = 0

all_records = df.to_dict(orient="records")

for idx, row in enumerate(all_records, 1):
    raw_email = row.get("Email")
    if pd.isna(raw_email) or not str(raw_email).strip():
        continue
    
    email = str(raw_email).strip()
    if email.lower() in sent_emails:
        continue
    
    name = str(row["Name"]).strip() if pd.notna(row.get("Name")) and str(row.get("Name")).strip() else "Partner"
    
    payload = {
        "from": "Richard Marlowe <rich@e.navo24.com>",
        "to": [email],
        "cc": ["support@navo24.com"],
        "reply_to": "sales@navo24.com",
        "subject": subject,
        "html": get_body_html(name)
    }
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            r = requests.post(
                "https://api.resend.com/emails",
                headers={"Authorization": f"Bearer {RESEND_API_KEY}", "Content-Type": "application/json"},
                json=payload,
                timeout=20
            )
            
            if r.status_code in [200, 201, 202]:
                res_data = r.json()
                email_id = res_data.get("id", "N/A")
                success_count += 1
                sent_emails.add(email.lower())
                print(f"[{datetime.datetime.utcnow().strftime('%H:%M:%S')}] [{idx}/{total_customers}] OK {name} <{email}> | ID: {email_id}", flush=True)
                break
            elif r.status_code == 429:
                print(f"[{idx}/{total_customers}] Rate limit 429 hit. Sleeping 3s...", flush=True)
                time.sleep(3)
            else:
                print(f"[{idx}/{total_customers}] Error {r.status_code}: {r.text}", flush=True)
                if attempt == max_retries - 1:
                    error_count += 1
        except Exception as e:
            print(f"[{idx}/{total_customers}] Exception on {email}: {e}", flush=True)
            if attempt == max_retries - 1:
                error_count += 1
            time.sleep(2)
    
    # 0.8s interval between emails for smooth sending
    time.sleep(0.8)

print(f"\n[{datetime.datetime.utcnow().isoformat()}] OUTREACH COMPLETED! Total sent successfully: {success_count}/{total_customers} (Errors: {error_count})", flush=True)
