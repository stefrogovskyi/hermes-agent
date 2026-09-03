#!/opt/hermes/hermes-agent/venv/bin/python3
import os
import sys
import json
import time
import re
import random
import datetime
import urllib.request
import urllib.parse
import smtplib
import imaplib
import email.utils
import uuid
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.path.append('/opt/hermes/profiles/ben/scripts')
from pitch_variations import generate_varied_pitch
from email_enrichment import enrich_business_email
from query_generator import get_dynamic_queries

TARGET_SUCCESSFUL_CONTACTS = 20

RAPIDAPI_KEY = "dc10dbe6c5mshaf1dd8c079adf40p1787fejsna128fe7f65c3"
RAPIDAPI_HOST = "google-map-places-new-v2.p.rapidapi.com"
OUTSCRAPER_API_KEY = "NjliMDZjYzYzOGM1NGFjYThmNzU2ZWNlNDIxYzE5MjF8ZjBiYmVlZjYwNQ"
SPREADSHEET_ID = "1INt0_J996CYbuiKxndLtfpCfMEDdgYcuLUaO-xMbDIk"
TOKEN_PATH = "/opt/hermes/google_token.json"

SMTP_SERVER = "smtp.hostinger.com"
SMTP_PORT = 465
SMTP_USER = "contact@aavalanche.com"
SMTP_PASS = "ContactAA#12345"
REPLY_TO = "ben.jett.ava@hotmail.com"

SIGNATURE_HTML = """
<br><br>
<table cellpadding="0" cellspacing="0" border="0" style="font-family: Tahoma, sans-serif; font-size: 10pt; color: #000000; line-height: 1.25;">
  <tr>
    <td>
      <!-- Name and Title -->
      <div style="font-weight: bold; font-size: 12pt; margin-bottom: 2px;">Ben Jett</div>
      <div style="margin-bottom: 4px;">Account Executive</div>

      <!-- Icon Image -->
      <div style="margin-bottom: 4px;">
        <img src="https://bit.ly/3UdEHji" alt="Logo" width="178" style="display: block; border: 0; height: auto;" />
      </div>

      <!-- Contact Details -->
      <div>Web &amp; Marketing Services</div>
      <div>+1 302 401 9315</div>
      <div>
        <a href="mailto:contact@aavalanche.com" style="color: #1d4ed8; text-decoration: underline;">contact@aavalanche.com</a>
      </div>
      <div>225 Franklin Street, Suite 2600,</div>
      <div>Boston, MA 02110, USA</div>
      <div>
        <a href="https://www.aavalanche.com" style="color: #1d4ed8; text-decoration: underline;">www.aavalanche.com</a>
      </div>
    </td>
  </tr>
</table>
"""

SIGNATURE_TEXT = """
--
Ben Jett
Account Executive
Avalanche Agency | Web & Marketing Services
+1 302 401 9315
contact@aavalanche.com
225 Franklin Street, Suite 2600, Boston, MA 02110, USA
www.aavalanche.com
"""

def get_sheets_service():
    with open(TOKEN_PATH) as f:
        token_data = json.load(f)
    creds = Credentials.from_authorized_user_info(token_data)
    return build('sheets', 'v4', credentials=creds)

def search_places_outscraper(query, limit=20):
    try:
        url = f"https://api.app.outscraper.com/maps/search-v3?query={urllib.parse.quote(query)}&limit={limit}&async=false"
        headers = {
            "X-API-KEY": OUTSCRAPER_API_KEY
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=35) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            results = data.get('data', [])
            if not results or len(results) == 0:
                return []
            
            raw_places = results[0]
            normalized = []
            for item in raw_places:
                site = item.get('site') or item.get('website') or ""
                normalized.append({
                    'id': item.get('place_id') or item.get('google_id') or str(uuid.uuid4()),
                    'displayName': {'text': item.get('name', '')},
                    'formattedAddress': item.get('full_address') or item.get('address') or f"{item.get('city', '')}, {item.get('state', '')}",
                    'nationalPhoneNumber': item.get('phone', ''),
                    'rating': item.get('rating', 0),
                    'userRatingCount': item.get('reviews', 0),
                    'websiteUri': site if site and site.lower() != 'none' else None
                })
            print(f"[Outscraper] Successfully retrieved {len(normalized)} places for '{query}'")
            return normalized
    except Exception as e:
        print(f"[Outscraper Error] '{query}': {e}")
        return []

def search_places(query):
    url = f"https://{RAPIDAPI_HOST}/v1/places:searchText"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.nationalPhoneNumber,places.rating,places.userRatingCount,places.websiteUri",
        "x-rapidapi-host": RAPIDAPI_HOST,
        "x-rapidapi-key": RAPIDAPI_KEY
    }
    payload = {
        "textQuery": query,
        "maxResultCount": 20
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            places = res.get('places', [])
            if places:
                return places
            print(f"[RapidAPI] No places returned for '{query}', trying Outscraper fallback...")
            return search_places_outscraper(query)
    except Exception as e:
        print(f"[RapidAPI 429/Error] '{query}': {e} -> Auto-switching to Outscraper fallback...")
        return search_places_outscraper(query)

def clean_phone(phone_str):
    if not phone_str:
        return ""
    digits = re.sub(r'[^\d]', '', str(phone_str))
    if len(digits) == 10:
        digits = "1" + digits
    return digits

def send_wa(phone, text):
    if not text or len(text) < 50 or "Custom pitch" in text:
        return {"error": "Invalid pitch text"}
    url = "http://localhost:3050/send-message"
    data = json.dumps({"phone": phone, "message": text}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {"error": str(e)}

def send_cold_email(to_email, company_name, city, niche, rating):
    if not to_email or "@" not in to_email:
        return False

    subject = f"Question regarding {company_name} in {city} / Online bookings"
    pitch_text = generate_varied_pitch(company_name, city, niche, str(rating))
    
    html_body = pitch_text.replace("\n\n", "</p><p>").replace("\n", "<br>")
    
    html_content = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family: Tahoma, 'Segoe UI', Arial, sans-serif; font-size: 10pt; color: #222; line-height: 1.5;">
    <p>{html_body}</p>
    {SIGNATURE_HTML}
</body>
</html>
"""
    msg = MIMEMultipart("alternative")
    msg['Subject'] = str(Header(subject, 'utf-8'))
    msg['From'] = formataddr((str(Header("Ben Jett | Avalanche Agency", 'utf-8')), SMTP_USER))
    msg['To'] = to_email
    msg['Reply-To'] = REPLY_TO
    msg['Date'] = email.utils.formatdate(localtime=True)
    msg['Message-ID'] = f"<{uuid.uuid4()}@aavalanche.com>"
    msg['X-Mailer'] = "Avalanche Mailer v1.0"
    
    part1 = MIMEText(pitch_text + "\n" + SIGNATURE_TEXT, 'plain', 'utf-8')
    part2 = MIMEText(html_content, 'html', 'utf-8')
    msg.attach(part1)
    msg.attach(part2)
    
    raw_message = msg.as_string().encode('utf-8')

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, [to_email], raw_message)

        try:
            imap = imaplib.IMAP4_SSL("imap.hostinger.com", 993)
            imap.login(SMTP_USER, SMTP_PASS)
            imap.append('INBOX.Sent', '\\Seen', imaplib.Time2Internaldate(time.time()), raw_message)
            imap.logout()
        except Exception:
            pass

        return True
    except Exception as e:
        print(f"Error sending email to {to_email}: {e}")
        return False

def main():
    print(f"=== Starting LeadGen & Outreach Job at {datetime.datetime.now()} ===")
    print(f"🎯 Target Goal: Exactly {TARGET_SUCCESSFUL_CONTACTS} DELIVERED contacts (WA or Email)")
    
    service = get_sheets_service()
    
    existing_res = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range="'Leads Pipeline'!A1:P500").execute()
    existing_rows = existing_res.get('values', [])
    existing_set = set()
    total_existing = len(existing_rows) - 1 if len(existing_rows) > 0 else 0
    
    for row in existing_rows:
        if len(row) > 4:
            existing_set.add(row[4].strip().lower())
        if len(row) > 5:
            existing_set.add(clean_phone(row[5]))

    today_str = datetime.date.today().strftime("%Y-%m-%d")
    already_delivered_today = 0
    for row in existing_rows:
        if len(row) > 11 and len(row) > 1 and row[1] == today_str:
            if "Sent ✅" in row[11]:
                already_delivered_today += 1

    needed_contacts = max(0, TARGET_SUCCESSFUL_CONTACTS - already_delivered_today)
    print(f"📊 Already delivered today ({today_str}): {already_delivered_today}/{TARGET_SUCCESSFUL_CONTACTS}")
    print(f"🎯 Contacts remaining to reach target today: {needed_contacts}")

    if needed_contacts == 0:
        print("🎉 Today's goal of 20 delivered contacts is already achieved!")
        return

    # Dynamic query generator spanning 500 combinations across all US regions
    queries_to_run = get_dynamic_queries()

    successful_contacts = 0
    total_processed = 0

    for niche, city, query in queries_to_run:
        if successful_contacts >= needed_contacts:
            break

        print(f"\n🔎 Scanning: '{query}' (Progress this session: {successful_contacts}/{needed_contacts})")
        places = search_places(query)

        for p in places:
            if successful_contacts >= needed_contacts:
                break

            name = p.get('displayName', {}).get('text', '').strip()
            website = p.get('websiteUri', '')
            phone = p.get('nationalPhoneNumber', '')
            cleaned_phone = clean_phone(phone)
            rating = p.get('rating', 'N/A')
            reviews = p.get('userRatingCount', 0)
            addr = p.get('formattedAddress', city)

            has_no_site = False
            if not website:
                has_no_site = True
            elif any(domain in website.lower() for domain in ['facebook.com', 'instagram.com', 'search.app', 'google.com', 'yelp.com', 'yellowpages.com']):
                has_no_site = True

            if has_no_site and name and name.lower() not in existing_set and (not cleaned_phone or cleaned_phone not in existing_set):
                existing_set.add(name.lower())
                if cleaned_phone:
                    existing_set.add(cleaned_phone)

                total_processed += 1
                lead_id = f"LD-{datetime.datetime.now().strftime('%m%d')}-{total_existing + total_processed:03d}"

                found_email = enrich_business_email(name, city, cleaned_phone)
                pitch = generate_varied_pitch(name, city, niche, str(rating))
                encoded_msg = urllib.parse.quote(pitch)

                wa_link = f'https://wa.me/{cleaned_phone}?text={encoded_msg}' if cleaned_phone else ''
                wa_formula = f'=HYPERLINK("{wa_link}", "💬 Send WhatsApp")' if cleaned_phone else 'No Phone'
                call_link = f'tel:+{cleaned_phone}' if cleaned_phone else ''
                call_formula = f'=HYPERLINK("{call_link}", "📞 Call Now")' if cleaned_phone else 'No Phone'

                print(f"[{total_processed}] Qualifying '{name}' ({city}) | Phone: {phone} | Rating: {rating}★ | Email: {found_email or 'None'}")

                wa_ok = False
                email_ok = False
                status_parts = []

                if cleaned_phone:
                    wa_res = send_wa(cleaned_phone, pitch)
                    if wa_res.get('success'):
                        wa_ok = True
                        status_parts.append("WA Sent ✅")
                    else:
                        err = wa_res.get('error', 'Failed')
                        status_parts.append(f"WA: {err[:20]}")
                else:
                    status_parts.append("WA: No Phone")

                if found_email:
                    email_ok = send_cold_email(found_email, name, city, niche, rating)
                    if email_ok:
                        status_parts.append("Email Sent ✅")
                    else:
                        status_parts.append("Email Failed ❌")

                is_contact_delivered = (wa_ok or email_ok)
                final_status = " | ".join(status_parts)
                now_str = datetime.datetime.now().strftime("%H:%M")

                phone_val = f"'{phone}" if phone and str(phone).startswith('+') else (phone or "N/A")
                lead_row = [
                    lead_id,
                    datetime.date.today().strftime("%Y-%m-%d"),
                    niche,
                    city,
                    name,
                    phone_val,
                    wa_formula,
                    call_formula,
                    str(rating),
                    str(reviews),
                    addr,
                    f"{final_status} ({now_str})",
                    pitch,
                    found_email or "",
                    "$490",
                    "Ben Jett"
                ]

                service.spreadsheets().values().append(
                    spreadsheetId=SPREADSHEET_ID,
                    range="'Leads Pipeline'!A2",
                    valueInputOption='USER_ENTERED',
                    insertDataOption='INSERT_ROWS',
                    body={'values': [lead_row]}
                ).execute()

                if is_contact_delivered:
                    successful_contacts += 1
                    print(f"  🎉 SUCCESS ({already_delivered_today + successful_contacts}/{TARGET_SUCCESSFUL_CONTACTS}): Delivered outreach to {name} via {final_status}!")
                    
                    if (already_delivered_today + successful_contacts) < TARGET_SUCCESSFUL_CONTACTS:
                        sleep_interval = random.randint(120, 150)
                        print(f"  ⏳ Waiting {sleep_interval}s (~2 min) before next contact...")
                        time.sleep(sleep_interval)
                else:
                    print(f"  ⚠️ Outreach undelivered for {name} ({final_status}). Continuing search for next reachable target...")
                    time.sleep(2)

    print(f"\n========================================================")
    print(f"🚀 Mission Complete! Total Successful Contacts Delivered Today: {already_delivered_today + successful_contacts}/{TARGET_SUCCESSFUL_CONTACTS}")
    print(f"========================================================")

if __name__ == "__main__":
    main()
