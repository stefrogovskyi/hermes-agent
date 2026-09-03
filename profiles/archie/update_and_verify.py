import subprocess
import json

SHEET_ID = '1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k'
CLI = '/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py'

row_num = 351
title_navo = "Colocation Infrastructure for Logistics and Shipping Operations"
link_navo = "https://docs.google.com/document/d/1hLLVLtRecWP0OVgpws48xpR0NZSjpuky/edit?usp=drivesdk&ouid=100676658802001293117&rtpof=true&sd=true"

values = [["Готово", title_navo, link_navo]]

rng = f"'Блогпосты Сирейтс'!D{row_num}:F{row_num}"

res = subprocess.run(['python3', CLI, 'sheets', 'update', '--values', json.dumps(values), SHEET_ID, rng], capture_output=True, text=True)
print("Update response:", res.stdout)
if res.stderr:
    print("Update stderr:", res.stderr)

# Read back to confirm
res_get = subprocess.run(['python3', CLI, 'sheets', 'get', SHEET_ID, f"'Блогпосты Сирейтс'!A{row_num}:G{row_num}"], capture_output=True, text=True)
print("Read back row 351:", res_get.stdout)
