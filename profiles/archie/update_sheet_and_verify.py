import subprocess
import json

SHEET_ID = '1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k'
GOOGLE_API = '/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py'
ROW_NUM = 344

new_title = "SeaRates Product Updates: Week 36, 2024"
web_link = "https://docs.google.com/document/d/1yMmftiNs0YuPkDn1hMfcSZRH4qdiDSVZ/edit?usp=drivesdk&ouid=100676658802001293117&rtpof=true&sd=true"

# Update D344:F344
cell_range = f"'Блогпосты Сирейтс'!D{ROW_NUM}:F{ROW_NUM}"
values = [["Готово", new_title, web_link]]

cmd = ['python3', GOOGLE_API, 'sheets', 'update', SHEET_ID, cell_range, '--values', json.dumps(values)]
print("Executing update command:", " ".join(cmd))
res = subprocess.run(cmd, capture_output=True, text=True)
print("Update output:", res.stdout)
if res.returncode != 0:
    print("Update error:", res.stderr)

# Verify readback
get_cmd = ['python3', GOOGLE_API, 'sheets', 'get', SHEET_ID, f"'Блогпосты Сирейтс'!A{ROW_NUM}:F{ROW_NUM}"]
get_res = subprocess.run(get_cmd, capture_output=True, text=True)
print("\nVerifying readback for row", ROW_NUM)
print(get_res.stdout)
