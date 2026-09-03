import json
import subprocess

SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
API_SCRIPT = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"

row_num = 208
new_title = "Stop Cargo Delays: Practical Tactics for Reliable Freight"
doc_link = "https://docs.google.com/document/d/1Lvb9P5-JpRfJFIA_g3SJKh9ReKZ9tG4d/edit?usp=drivesdk&ouid=100676658802001293117&rtpof=true&sd=true"

# Update D208:F208
range_str = f"Блогпосты Сирейтс!D{row_num}:F{row_num}"
values_json = json.dumps([["Готово", new_title, doc_link]])

cmd_update = [
    "python3", API_SCRIPT, "sheets", "update", SHEET_ID, range_str, "--values", values_json
]

res_upd = subprocess.run(cmd_update, capture_output=True, text=True)
print("Update output:", res_upd.stdout)

# Read back range to confirm
cmd_get = [
    "python3", API_SCRIPT, "sheets", "get", SHEET_ID, range_str
]

res_get = subprocess.run(cmd_get, capture_output=True, text=True)
print("Readback output:", res_get.stdout)
