import os
import json
import urllib.request
import urllib.parse
import re
import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import sys
sys.path.append('/opt/hermes/profiles/ben/scripts')
try:
    from email_sender import send_cold_email
except ImportError:
    pass

RAPIDAPI_KEY = "dc10dbe6c5mshaf1dd8c079adf40p1787fejsna128fe7f65c3"
RAPIDAPI_HOST = "google-map-places-new-v2.p.rapidapi.com"
SPREADSHEET_ID = "1INt0_J996CYbuiKxndLtfpCfMEDdgYcuLUaO-xMbDIk"
TOKEN_PATH = "/opt/hermes/google_token.json"

TARGET_QUERIES = [
    ("Auto Repair & Body", "Miami, FL", "auto repair in Miami FL"),
    ("Auto Detailing & Ceramic", "Miami, FL", "car detailing in Miami FL"),
    ("Brake & Transmission", "Fort Lauderdale, FL", "auto repair in Fort Lauderdale FL"),
    ("Dental & Orthodontics", "Boston, MA", "dental clinic in Boston MA"),
    ("Cosmetic Dentistry", "Cambridge, MA", "cosmetic dentist in Cambridge MA"),
    ("Roofing Contractors", "Tampa, FL", "roofing contractor in Tampa FL"),
    ("HVAC & Cooling", "Orlando, FL", "hvac repair in Orlando FL"),
    ("Plumbing Services", "Houston, TX", "emergency plumber in Houston TX"),
    ("Immigration & Legal", "Miami, FL", "immigration attorney in Miami FL"),
    ("Medical Spa & Wellness", "Scottsdale, AZ", "medical spa in Scottsdale AZ"),
]

def get_sheets_service():
    with open(TOKEN_PATH) as f:
        token_data = json.load(f)
    creds = Credentials.from_authorized_user_info(token_data)
    return build('sheets', 'v4', credentials=creds)

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
        with urllib.request.urlopen(req, timeout=15) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            return res.get('places', [])
    except Exception as e:
        print(f"Error querying '{query}': {e}")
        return []

def clean_phone(phone_str):
    if not phone_str:
        return ""
    digits = re.sub(r'[^\d]', '', str(phone_str))
    if len(digits) == 10:
        digits = "1" + digits
    return digits

def generate_pitch(name, city, niche, rating):
    if "Auto" in niche or "Tire" in niche:
        return f"Hi {name}! Saw your high {rating}★ rating on Google Maps in {city}. You don't have an official booking website, missing out on high-ticket service bookings. We build fast, high-converting websites + 24/7 AI Receptionists for auto shops in 48h ($490). Would you like to see a quick 2-minute live demo for {name}?"
    elif "Dental" in niche or "MedSpa" in niche:
        return f"Hello {name}! Found your practice on Google Maps in {city} ({rating}★). You currently don't have a direct online patient intake system. We build modern medical landing pages with 24/7 AI booking bots in 48 hours ($490). Could I share a quick prototype customized for {name}?"
    else:
        return f"Hi {name}! Noticed your top-rated business on Google Maps in {city}. You're missing a direct website, losing valuable leads to competitors. We build custom websites + 24/7 AI Sales Assistants in 48h ($490). Would you like to check out a live concept?"

def run_leadgen(target_count=20):
    service = get_sheets_service()
    
    # Get existing
    existing_res = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range="'Leads Pipeline'!E:F").execute()
    existing_rows = existing_res.get('values', [])
    existing_set = set()
    for row in existing_rows:
        if len(row) > 0:
            existing_set.add(row[0].strip().lower())
        if len(row) > 1:
            existing_set.add(clean_phone(row[1]))

    new_leads = []
    for niche, city, query in TARGET_QUERIES:
        if len(new_leads) >= target_count:
            break
        print(f"Searching for: {query}...")
        places = search_places(query)
        
        for p in places:
            name = p.get('displayName', {}).get('text', '').strip()
            website = p.get('websiteUri', '')
            phone = p.get('nationalPhoneNumber', '')
            cleaned_phone = clean_phone(phone)
            rating = p.get('rating', '5.0')
            reviews = p.get('userRatingCount', 0)
            addr = p.get('formattedAddress', city)

            has_no_site = False
            if not website:
                has_no_site = True
            elif any(domain in website for domain in ['facebook.com', 'instagram.com', 'search.app', 'google.com', 'yelp.com']):
                has_no_site = True

            if has_no_site and name and name.lower() not in existing_set and (not cleaned_phone or cleaned_phone not in existing_set):
                existing_set.add(name.lower())
                if cleaned_phone:
                    existing_set.add(cleaned_phone)
                
                pitch = generate_pitch(name, city, niche, rating)
                encoded_msg = urllib.parse.quote(pitch)
                
                wa_link = f'https://wa.me/{cleaned_phone}?text={encoded_msg}' if cleaned_phone else ''
                wa_formula = f'=HYPERLINK("{wa_link}", "💬 Send WhatsApp")' if cleaned_phone else 'No Phone'
                
                call_link = f'tel:+{cleaned_phone}' if cleaned_phone else ''
                call_formula = f'=HYPERLINK("{call_link}", "📞 Call Now")' if cleaned_phone else 'No Phone'

                lead_row = [
                    f"LD-{datetime.datetime.now().strftime('%m%d')}-{len(existing_set)+1:03d}",
                    datetime.date.today().strftime("%Y-%m-%d"),
                    niche,
                    city,
                    name,
                    phone or "N/A",
                    wa_formula,
                    call_formula,
                    str(rating),
                    str(reviews),
                    addr,
                    "New / Qualified",
                    pitch,
                    "$490",
                    "Ben Jett"
                ]
                new_leads.append(lead_row)
                if len(new_leads) >= target_count:
                    break

    if new_leads:
        print(f"Adding {len(new_leads)} new leads to Google Sheets...")
        service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range="'Leads Pipeline'!A2",
            valueInputOption='USER_ENTERED',
            insertDataOption='INSERT_ROWS',
            body={'values': new_leads}
        ).execute()
        print("✅ Done!")

if __name__ == "__main__":
    run_leadgen(20)
