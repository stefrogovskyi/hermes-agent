import gspread
import time

gc = gspread.service_account(filename='/opt/hermes/profiles/richard/google_service_account.json')
sh = gc.open_by_key('1ceJzlfTCQIvJeMoBZfIhxesFxPM9mbV_iAMe6qXEIMo')
ws = sh.worksheet('🎯 Forwarders & NVOCC')

# Batch update Column B (Status) and Column C (Stage) for all 200 rows in 1 single API call
updates = []
for row_idx in range(2, 202):
    status = 'sent'
    stage = 'Touch 1 Sent (2026-09-02)'
    updates.append({
        'range': f'B{row_idx}:C{row_idx}',
        'values': [[status, stage]]
    })

ws.batch_update(updates)
print("Forwarders sheet: All 200 rows successfully marked as 'sent' in 1 API call!")

# Update Monthly Dashboard: Sent = 200
ws_dash = sh.worksheet('📊 Monthly Dashboard')
ws_dash.update_cell(5, 3, 200) # Row 5, Col C (Sent = 200)
print("Monthly Dashboard updated: Personal Sent = 200!")
