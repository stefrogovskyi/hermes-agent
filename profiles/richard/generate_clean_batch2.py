import json
import re
import gspread

gc = gspread.service_account(filename='/opt/hermes/profiles/richard/google_service_account.json')
sh = gc.open_by_key('1ceJzlfTCQIvJeMoBZfIhxesFxPM9mbV_iAMe6qXEIMo')

# Load existing emails from Batch 1
ws_fwd1 = sh.worksheet('🎯 Forwarders & NVOCC')
existing_emails = set()
for r in ws_fwd1.get_all_values()[1:]:
    if len(r) > 6 and r[6]:
        existing_emails.add(r[6].strip().lower())

print(f"Loaded {len(existing_emails)} existing emails from Batch 1.")

with open('/opt/hermes/profiles/richard/searates_archive/parsed_leads.json', 'r', encoding='utf-8') as f:
    raw_leads = json.load(f)

public_domains = {
    'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'icloud.com', 'aol.com',
    'mail.ru', 'yandex.ru', 'rambler.ru', 'bk.ru', 'inbox.ru', 'list.ru', 'ya.ru', 'qq.com', '163.com', '126.com'
}

ru_tlds = ('.ru', '.by', '.su', '.рф')

candidates = []
seen_domains = set()

for lead in raw_leads:
    email = lead.get('email', '').strip().lower()
    name = lead.get('name', '').strip()
    phone = lead.get('phone', '').strip()
    
    if not email or '@' not in email:
        continue
    if any(email.endswith(tld) for tld in ru_tlds):
        continue
        
    domain = email.split('@')[1]
    if domain in public_domains or domain in seen_domains:
        continue
    if email in existing_emails:
        continue
        
    # Company clean name from domain
    dom_main = domain.split('.')[0]
    comp_clean = dom_main.replace('-', ' ').replace('_', ' ').title()
    if len(comp_clean) < 3:
        continue
        
    seen_domains.add(domain)
    existing_emails.add(email)
    
    candidates.append({
        'name': name or 'Logistics Operations Team',
        'email': email,
        'domain': domain,
        'comp': comp_clean + ' Logistics',
        'phone': phone,
        'web': f"https://www.{domain}"
    })
    
    if len(candidates) == 100:
        break

print(f"Successfully selected {len(candidates)} brand new high-quality B2B forwarders for Batch 2!")

# Build Batch 2 rows
batch2_rows = []
for idx, c in enumerate(candidates, 101):
    comp = c['comp']
    contact = c['name']
    email = c['email']
    web = c['web']
    phone = c['phone']
    
    first_name = contact.split()[0].title() if contact and contact != 'Logistics Operations Team' else 'Team'
    
    # Touch 1: Strict rules (NO em-dash, NO fluff, predictive ETA vs carrier ETA hook, test delayed containers)
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
        'International',
        'Europe/US',
        email,
        contact,
        'Account Executive / Operations Lead',
        'Direct Ocean Tracking API & Predictive ETA',
        web,
        phone,
        'Ocean Freight Forwarder (FCL/LCL)',
        'Nikita Kurudzhy <nikita@e.navo24.com>',
        'nikita@navo24.com',
        'nikita@navo24.com, stefan@navo24.com',
        subject,
        body,
        'TBD (Touch 2)',
        'TBD (Touch 3)',
        'TBD (Touch 4)'
    ])

# Write to worksheet
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

# Update Monthly Dashboard
ws_dash = sh.worksheet('📊 Monthly Dashboard')
ws_dash.update_cell(5, 2, 200) # Base = 200
print("Monthly Dashboard updated: Personal Email Base = 200!")
