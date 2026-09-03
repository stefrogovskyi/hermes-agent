import gspread

gc = gspread.service_account(filename='/opt/hermes/profiles/richard/google_service_account.json')
sh = gc.open_by_key('1ceJzlfTCQIvJeMoBZfIhxesFxPM9mbV_iAMe6qXEIMo')

# 1. Update Monthly Dashboard: Sent = 100
ws_dash = sh.worksheet('📊 Monthly Dashboard')
ws_dash.update_cell(5, 3, 100) # Row 5, Col C (Sent)
print("Monthly Dashboard updated: Personal Email Sent = 100")

# 2. Update Forwarders tab: Status = 'sent' / 'Touch 1 Sent'
ws_fwd = sh.worksheet('🎯 Forwarders & NVOCC')
rows = ws_fwd.get_all_values()
num_leads = len(rows) - 1

# Batch update status column (Col B / Col 2) to 'sent'
cell_updates = []
for row_idx in range(2, num_leads + 2):
    cell_updates.append({
        'range': f'B{row_idx}',
        'values': [['sent']]
    })

ws_fwd.batch_update(cell_updates)
print(f"Forwarders Tab updated: {num_leads} leads marked as 'sent'!")
