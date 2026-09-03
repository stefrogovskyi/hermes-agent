import gspread

gc = gspread.service_account(filename='/opt/hermes/profiles/richard/google_service_account.json')
sh = gc.open_by_key('1ceJzlfTCQIvJeMoBZfIhxesFxPM9mbV_iAMe6qXEIMo')
ws_fol = sh.worksheet('🔄 Follow-ups & Active Trials')

rows = ws_fol.get_all_values()
if len(rows) > 2:
    # Update Source Channel column (index 9, Column J) and Owner
    ws_fol.update_cell(2, 10, 'Navo Outbound Email Campaign (Assigned to Nikita)')
    ws_fol.update_cell(3, 10, 'Navo Outbound Email Campaign (Assigned to Nikita)')
    print("Source channel clarified in CRM!")
