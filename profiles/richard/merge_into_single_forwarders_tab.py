import gspread

gc = gspread.service_account(filename='/opt/hermes/profiles/richard/google_service_account.json')
sh = gc.open_by_key('1ceJzlfTCQIvJeMoBZfIhxesFxPM9mbV_iAMe6qXEIMo')

ws_fwd = sh.worksheet('🎯 Forwarders & NVOCC')
ws_b2 = sh.worksheet('🎯 Forwarders Batch 2 (101-200)')

batch1_rows = ws_fwd.get_all_values()
batch2_rows = ws_b2.get_all_values()[1:]

headers = batch1_rows[0]
batch1_data = batch1_rows[1:]

combined_rows = batch1_data + batch2_rows
print(f"Total combined leads: {len(combined_rows)}")

# Resize sheet to fit 250 rows and 25 columns
ws_fwd.resize(rows=250, cols=25)

# Clear and update
ws_fwd.clear()
ws_fwd.update(values=[headers] + combined_rows, range_name=f'A1', value_input_option='USER_ENTERED')
print("Successfully merged all 200 leads into '🎯 Forwarders & NVOCC'!")

try:
    sh.del_worksheet(ws_b2)
    print("Deleted Batch 2 tab.")
except Exception as e:
    print(f"Delete notice: {e}")
