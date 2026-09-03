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
        
        # Injected SeaRates pedigree cleanly without em-dash
        body = (
            f"Hi {first_name},\n\n"
            f"Do your operations teams struggle with ocean carrier schedule ETAs not matching real container arrivals at discharge ports?\n\n"
            f"Navo24 was founded by the original core team and engineering leadership behind SeaRates to provide direct tracking infrastructure across 239 ocean carriers. We calculate Predictive ETA using satellite AIS vessel tracking and live port congestion data (standard DCSA milestones and automated free-time calculation).\n\n"
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
        r[17] = body # Update Column R (Touch 1 Body)
    updated_rows.append(r)

ws.update(values=updated_rows, range_name='A2', value_input_option='USER_ENTERED')
print("Successfully injected SeaRates pedigree into leads #101-#200 in Google Sheets!")
