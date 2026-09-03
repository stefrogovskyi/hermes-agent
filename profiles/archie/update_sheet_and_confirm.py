import json
import subprocess

SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
TAB_NAME = "Блогпосты Сирейтс"
SCRIPT = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"

row_num = 330
new_title = "SeaRates Week 41, 2024: Logistics Map Updates & More"
doc_link = "https://docs.google.com/document/d/17diLBShI7JxWwcizJqUpG3gfOVj_qwG7/edit?usp=drivesdk&ouid=100676658802001293117&rtpof=true&sd=true"
status = "Готово"

# Update D330:F330
values = [[status, new_title, doc_link]]
values_json = json.dumps(values)

cmd_update = [
    "python3", SCRIPT, "sheets", "update", SHEET_ID,
    f"{TAB_NAME}!D{row_num}:F{row_num}",
    "--values", values_json
]

print("Executing update...")
res_update = subprocess.run(cmd_update, capture_output=True, text=True)
print("Update stdout:", res_update.stdout)

# Read back row to confirm
cmd_get = [
    "python3", SCRIPT, "sheets", "get", SHEET_ID,
    f"{TAB_NAME}!A{row_num}:F{row_num}"
]

print("Reading back row to confirm...")
res_get = subprocess.run(cmd_get, capture_output=True, text=True)
print("Readback stdout:", res_get.stdout)
