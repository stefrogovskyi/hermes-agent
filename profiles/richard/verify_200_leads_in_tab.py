import gspread

gc = gspread.service_account(filename='/opt/hermes/profiles/richard/google_service_account.json')
sh = gc.open_by_key('1ceJzlfTCQIvJeMoBZfIhxesFxPM9mbV_iAMe6qXEIMo')

# Re-read and build 200 leads cleanly
with open('/opt/hermes/profiles/richard/searates_archive/parsed_leads.json', 'r', encoding='utf-8') as f:
    raw = json.load(f)

# Let's inspect rows in ws_fwd
ws_fwd = sh.worksheet('🎯 Forwarders & NVOCC')
rows = ws_fwd.get_all_values()
print(f"Total rows in Forwarders sheet: {len(rows)}")
print(f"Row 1 (Header): {rows[0][:5]}")
print(f"Row 101 (Lead #100): {rows[100][:5]}")
if len(rows) > 101:
    print(f"Row 102 (Lead #101): {rows[101][:5]}")
    print(f"Row 201 (Lead #200): {rows[200][:5]}")
