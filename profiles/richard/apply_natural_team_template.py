import gspread

gc = gspread.service_account(filename='/opt/hermes/profiles/richard/google_service_account.json')
sh = gc.open_by_key('1ceJzlfTCQIvJeMoBZfIhxesFxPM9mbV_iAMe6qXEIMo')
ws = sh.worksheet('🎯 Forwarders & NVOCC')

rows = ws.get_all_values()

updated_rows = []
for idx, r in enumerate(rows[1:], 1):
    if idx > 100:
        comp = r[3]
        contact = r[7]
        first_name = contact.split()[0].title() if contact and contact != 'Logistics Operations Team' else 'Team'
        
        # Natural human tone based on top performing team emails
        # Subject: lower-case casual internal style
        domain_short = comp.replace(' Logistics', '').lower()
        subject = f"{domain_short} / container tracking"
        
        body = (
            f"Hi {first_name},\n\n"
            f"We built Navo24 to give forwarders direct tracking across 239 ocean lines, live satellite AIS positions, and predictive ETAs that account for actual port congestion (founded by the original team behind SeaRates).\n\n"
            f"You can test a couple of your active shipments on our free tier at https://trackingmcp.com/auth/signup to see how the data looks against your carrier updates.\n\n"
            f"Worth taking a look?\n\n"
            f"Best regards,\n\n"
            f"Nikita Kurudzhy\n"
            f"Account Executive\n"
            f"API-MCP for Logistics & Trade\n"
            f"Tel: +380 93 228 5150\n"
            f"Email: nikita@navo24.com\n"
            f"navo24.com"
        )
        r[16] = subject
        r[17] = body
    updated_rows.append(r)

ws.update(values=updated_rows, range_name='A2', value_input_option='USER_ENTERED')
print("Successfully applied natural team template to leads #101-#200 in Google Sheets!")
