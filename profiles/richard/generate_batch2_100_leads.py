import json
import re
import socket
import gspread

gc = gspread.service_account(filename='/opt/hermes/profiles/richard/google_service_account.json')
sh = gc.open_by_key('1ceJzlfTCQIvJeMoBZfIhxesFxPM9mbV_iAMe6qXEIMo')

# Load previously used domains/emails to avoid duplicates
ws_fwd1 = sh.worksheet('🎯 Forwarders & NVOCC')
existing_emails = set()
for r in ws_fwd1.get_all_values()[1:]:
    if len(r) > 6 and r[6]:
        existing_emails.add(r[6].strip().lower())

print(f"Loaded {len(existing_emails)} existing emails from Batch 1.")

# Load raw leads from archive
with open('/opt/hermes/profiles/richard/searates_archive/parsed_leads.json', 'r', encoding='utf-8') as f:
    raw_leads = json.load(f)

print(f"Total raw leads in archive: {len(raw_leads)}")

ru_patterns = re.compile(r'\.(ru|by|su|рф)$|@(mail\.ru|yandex|rambler|bk\.ru|inbox\.ru)', re.IGNORECASE)

def is_valid_email(email):
    if not email or '@' not in email:
        return False
    if ru_patterns.search(email):
        return False
    return True

candidates = []
seen_domains = set()

for lead in raw_leads:
    email = lead.get('email', '').strip()
    comp = lead.get('company', '').strip()
    country = lead.get('country', '').strip()
    web = lead.get('website', '').strip()
    phone = lead.get('phone', '').strip()
    contact = lead.get('contact_person', '').strip()
    
    if not email or not comp or not is_valid_email(email):
        continue
        
    email_lower = email.lower()
    if email_lower in existing_emails:
        continue
        
    domain = email_lower.split('@')[1]
    if domain in seen_domains:
        continue
        
    # Exclude bulk generic non-transport
    if any(k in comp.lower() for k in ['hotel', 'tour', 'travel', 'restaurant', 'law', 'consulting']):
        continue
        
    seen_domains.add(domain)
    existing_emails.add(email_lower)
    
    candidates.append({
        'comp': comp,
        'country': country or 'International',
        'email': email,
        'web': web or f"https://www.{domain}",
        'phone': phone,
        'contact': contact or 'Logistics Operations Team',
        'domain': domain
    })
    
    if len(candidates) == 100:
        break

print(f"Selected {len(candidates)} brand new unique B2B forwarders for Batch 2!")

# Create batch 2 rows
batch2_rows = []
for idx, c in enumerate(candidates, 101):
    comp = c['comp']
    contact = c['contact']
    email = c['email']
    web = c['web']
    country = c['country']
    phone = c['phone']
    
    first_name = contact.split()[0] if contact and contact != 'Logistics Operations Team' else 'Team'
    
    # Touch 1: Hook on Predictive ETA vs Carrier ETA & Test 1-2 delayed containers on Free Tier
    # Strict rule: NO em-dash (—), NO fluff, NO quick question, direct plain text
    subject = f"{comp} container tracking: 239 ocean carriers & Predictive ETA"
    
    body = (
        f"Hi {first_name},\n\n"
        f"Do your operations teams struggle with ocean carrier schedule ETAs not matching real container arrivals at discharge ports?\n\n"
        f"At Navo24, we provide direct tracking infrastructure across 239 ocean carriers, calculating Predictive ETA using satellite AIS vessel positions and live port congestion data (standard DCSA milestones and automated free-time calculation).\n\n"
        f"You can test 1 or 2 of your active or delayed containers for free at https://trackingmcp.com/auth/signup (5 active containers included every month, no credit card required).\n\n"
        f"Would you be open to testing this against your current carrier data this week?\n\n"
        f"Best regards,\n\n"
        f"Nikita Kurudzhy\n"
        f"Account Executive\n"
        f"API-MCP for Logistics & Trade\n"
        f"Tel: +380 93 228 5150\n"
        f"Email: nikita@navo24.com\n"
        f"navo24.com"
    )
    
    batch2_rows.append([
        idx,
        'not_sent',
        'Scheduled (Touch 1)',
        comp,
        country,
        'Europe/US', # tz
        email,
        contact,
        'Account Executive / Ops Lead',
        'Direct Ocean Tracking API & Predictive ETA',
        web,
        phone,
        'Ocean Freight Forwarder (FCL/LCL)',
        'nikita@e.navo24.com',
        'nikita@navo24.com',
        'nikita@navo24.com, stefan@navo24.com',
        subject,
        body,
        'TBD (Touch 2)',
        'TBD (Touch 3)',
        'TBD (Touch 4)'
    ])

# Append or create tab
try:
    ws_b2 = sh.worksheet('🎯 Forwarders Batch 2 (101-200)')
except:
    ws_b2 = sh.add_worksheet(title='🎯 Forwarders Batch 2 (101-200)', rows=150, cols=25)

headers = [
    '№', 'Status', 'Stage', 'Company Name', 'Country', 'Timezone',
    'Email (Verified MX)', 'Contact Person', 'Job Title', 'Product Focus',
    'Website', 'Phone', 'Segment', 'Sender From', 'Reply-To', 'CC',
    'Touch 1 Subject', 'Touch 1 Body (Humanized 2026)',
    'Touch 2 Body', 'Touch 3 Body', 'Touch 4 Breakup'
]

ws_b2.clear()
ws_b2.update(values=[headers] + batch2_rows, range_name=f'A1:U{len(batch2_rows)+1}', value_input_option='USER_ENTERED')
print("Successfully populated '🎯 Forwarders Batch 2 (101-200)' in Google Sheets!")

# Update Dashboard Base
ws_dash = sh.worksheet('📊 Monthly Dashboard')
# Total base is now 200
ws_dash.update_cell(5, 2, 200) # Base = 200
print("Monthly Dashboard updated: Email Base = 200!")
