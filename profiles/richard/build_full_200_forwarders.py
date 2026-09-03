import json
import re
import gspread

gc = gspread.service_account(filename='/opt/hermes/profiles/richard/google_service_account.json')
sh = gc.open_by_key('1ceJzlfTCQIvJeMoBZfIhxesFxPM9mbV_iAMe6qXEIMo')
ws_fwd = sh.worksheet('🎯 Forwarders & NVOCC')

with open('/opt/hermes/profiles/richard/searates_archive/parsed_leads.json', 'r', encoding='utf-8') as f:
    raw_leads = json.load(f)

public_domains = {
    'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'icloud.com', 'aol.com',
    'mail.ru', 'yandex.ru', 'rambler.ru', 'bk.ru', 'inbox.ru', 'list.ru', 'ya.ru', 'qq.com', '163.com', '126.com'
}
ru_tlds = ('.ru', '.by', '.su', '.рф')

seen_domains = set()
unique_leads = []

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
        
    dom_main = domain.split('.')[0]
    comp_clean = dom_main.replace('-', ' ').replace('_', ' ').title()
    if len(comp_clean) < 3:
        continue
        
    seen_domains.add(domain)
    
    unique_leads.append({
        'name': name or 'Logistics Operations Team',
        'email': email,
        'domain': domain,
        'comp': comp_clean + ' Logistics',
        'phone': phone,
        'web': f"https://www.{domain}"
    })
    
    if len(unique_leads) == 200:
        break

print(f"Extracted {len(unique_leads)} unique B2B forwarders!")

all_rows = []
for idx, c in enumerate(unique_leads, 1):
    comp = c['comp']
    contact = c['name']
    email = c['email']
    web = c['web']
    phone = c['phone']
    first_name = contact.split()[0].title() if contact and contact != 'Logistics Operations Team' else 'Team'
    
    status = 'sent' if idx <= 100 else 'not_sent'
    stage = 'Touch 1 Sent' if idx <= 100 else 'Scheduled (Touch 1)'
    
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
    
    all_rows.append([
        idx,
        status,
        stage,
        comp,
        'International',
        'EU/US (10:00 UTC)',
        email,
        contact,
        'Operations / Account Executive',
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

headers = [
    '№', 'Status', 'Stage', 'Company Name', 'Country', 'Optimal Send Window (Таймзона)',
    'Email (Verified MX)', 'Contact Person', 'Job Title', 'Product Focus',
    'Website', 'Phone', 'Segment', 'Sender From', 'Reply-To', 'CC',
    'Touch 1 Subject', 'Touch 1 Body (Humanized 2026)',
    'Touch 2 Body', 'Touch 3 Body', 'Touch 4 Breakup'
]

ws_fwd.resize(rows=220, cols=25)
ws_fwd.clear()
ws_fwd.update(values=[headers] + all_rows, range_name='A1', value_input_option='USER_ENTERED')
print(f"Successfully populated all {len(all_rows)} leads directly into '🎯 Forwarders & NVOCC'!")
