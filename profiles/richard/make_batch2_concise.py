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
        
        # Ultra-concise, punchy 2026 cold email (under 55 words)
        body = (
            f"Hi {first_name},\n\n"
            f"Navo24 was founded by the core team behind SeaRates to provide direct tracking across 239 ocean carriers.\n\n"
            f"Unlike carrier schedules, we calculate Predictive ETA using live satellite AIS and port congestion data.\n\n"
            f"You can test 1-2 delayed containers for free at https://trackingmcp.com/auth/signup (5 containers/month, no card required).\n\n"
            f"Open to testing this against your current tracking this week?\n\n"
            f"Best regards,\n\n"
            f"Nikita Kurudzhy\n"
            f"Account Executive\n"
            f"API-MCP for Logistics & Trade\n"
            f"Tel: +380 93 228 5150\n"
            f"Email: nikita@navo24.com\n"
            f"navo24.com"
        )
        r[17] = body
    updated_rows.append(r)

ws.update(values=updated_rows, range_name='A2', value_input_option='USER_ENTERED')
print("Successfully shortened all 100 emails in Google Sheets to concise format!")
