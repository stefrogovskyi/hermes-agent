import os
import json
import time
import re
import urllib.request
import urllib.error
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SPREADSHEET_ID = "1INt0_J996CYbuiKxndLtfpCfMEDdgYcuLUaO-xMbDIk"
TOKEN_PATH = "/opt/hermes/google_token.json"

SMTP_SERVER = "smtp.hostinger.com"
SMTP_PORT = 465
SMTP_USER = "contact@aavalanche.com"
SMTP_PASS = "ContactAA#12345"
REPLY_TO = "ben.jett.ava@hotmail.com"

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

def send_cold_email(to_email, company_name, city, niche, sender_name="Ben Jett | Avalanche Agency"):
    if not to_email or "@" not in to_email:
        return False
    subject = f"Question regarding {company_name} in {city} / Online bookings"
    html_content = f"""
    <div style="font-family: 'Segoe UI', Helvetica, Arial, sans-serif; font-size: 15px; color: #222; line-height: 1.6;">
        <p>Hi there,</p>
        <p>I came across <strong>{company_name}</strong> on Google Maps in {city} and was impressed by your stellar customer reviews.</p>
        <p>I noticed you don't currently have a direct website or automated booking system attached to your profile. Many potential customers looking for {niche} in {city} end up going to competitors who take bookings online 24/7.</p>
        <p>At <strong>Avalanche Agency</strong>, we build high-converting websites with built-in <strong>24/7 AI Sales Assistants</strong> that automatically capture leads and book appointments straight into your schedule in under 48 hours.</p>
        <p>Would you be open to a quick 2-minute live demo customized for <strong>{company_name}</strong>?</p>
        <br>
        <p>Best regards,<br>
        <strong>Ben Jett</strong><br>
        Chief Marketing Officer<br>
        <a href="https://aavalanche.com/ai-sales-agent" style="color: #0066cc; text-decoration: none;">Avalanche Agency &amp; Enlight Group</a><br>
        📍 225 Franklin St, Boston, MA 02110<br>
        🌐 <a href="https://aavalanche.com">aavalanche.com</a>
        </p>
    </div>
    """
    msg = MIMEMultipart("alternative")
    msg['Subject'] = subject
    msg['From'] = formataddr((str(Header(sender_name, 'utf-8')), SMTP_USER))
    msg['To'] = to_email
    msg['Reply-To'] = REPLY_TO
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, [to_email], msg.as_string())
            print(f"✅ Email sent successfully to {to_email} ({company_name})")
            return True
    except Exception as e:
        print(f"❌ Error sending email to {to_email}: {e}")
        return False

def dispatch_batch(limit=5, delay_seconds=5):
    with open(TOKEN_PATH) as f:
        token_data = json.load(f)
    creds = Credentials.from_authorized_user_info(token_data)
    service = build('sheets', 'v4', credentials=creds)

    res = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range="'Leads Pipeline'!A1:O50").execute()
    rows = res.get('values', [])
    if not rows or len(rows) <= 1:
        print("No leads to process.")
        return []

    results = []
    processed = 0

    for idx, r in enumerate(rows[1:], start=2):
        if len(r) >= 6:
            lid = r[0]
            niche = r[2]
            city = r[3]
            company = r[4]
            phone = r[5]
            status = r[11] if len(r) > 11 else "New"
            pitch = r[12] if len(r) > 12 else ""
            email = r[13] if len(r) > 13 and "@" in str(r[13]) else ""

            # Only process if status is not already sent
            if "Sent" not in status and phone and phone != "N/A":
                print(f"[{processed+1}/{limit}] Contacting {company} ({phone})...")
                
                clean_phone = re.sub(r'[^\d]', '', str(phone))
                if len(clean_phone) == 10:
                    clean_phone = "1" + clean_phone

                # Send WhatsApp
                wa_res = send_wa(clean_phone, pitch)
                wa_ok = wa_res.get('success', False)

                # Send Email if present
                email_ok = False
                if email:
                    email_ok = send_cold_email(email, company, city, niche)

                status_parts = []
                if wa_ok:
                    status_parts.append("WhatsApp Sent ✅")
                else:
                    err_msg = wa_res.get('error', 'Failed')
                    status_parts.append(f"WA Failed ({err_msg[:25]})")

                if email:
                    status_parts.append("Email Sent ✅" if email_ok else "Email Failed ❌")

                final_status = " | ".join(status_parts)
                now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

                service.spreadsheets().values().update(
                    spreadsheetId=SPREADSHEET_ID,
                    range=f"'Leads Pipeline'!L{idx}:N{idx}",
                    valueInputOption='RAW',
                    body={'values': [[final_status, pitch, f"Processed: {now_str}"]]}
                ).execute()

                results.append({
                    "id": lid,
                    "company": company,
                    "phone": phone,
                    "status": final_status
                })

                processed += 1
                if processed >= limit:
                    break

                if delay_seconds > 0:
                    print(f"Waiting {delay_seconds}s before next contact...")
                    time.sleep(delay_seconds)

    return results

if __name__ == "__main__":
    import sys
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    delay = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    res = dispatch_batch(count, delay)
    print(json.dumps(res, indent=2, ensure_ascii=False))
