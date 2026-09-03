import subprocess
import json

SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
TAB = "Блогпосты Сирейтс"
GOOGLE_API = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"

ROW = 309
RANGE_DEF = f"{TAB}!D{ROW}:F{ROW}"

new_title = "Decarbonizing Roll-on/Roll-off Freight: Modern Clean Technologies and Fleet Compliance"
file_link = "https://docs.google.com/document/d/149vuWfHsXciz_yMT9OysFphgL9COIdHf/edit?usp=drivesdk&ouid=100676658802001293117&rtpof=true&sd=true"

vals = json.dumps([["Готово", new_title, file_link]])

cmd_update = ["python3", GOOGLE_API, "sheets", "update", SHEET_ID, RANGE_DEF, "--values", vals]
res_up = subprocess.run(cmd_update, capture_output=True, text=True)
print("Update output:", res_up.stdout, res_up.stderr)

cmd_get = ["python3", GOOGLE_API, "sheets", "get", SHEET_ID, f"{TAB}!A{ROW}:F{ROW}"]
res_get = subprocess.run(cmd_get, capture_output=True, text=True)
print("Read back row 309:", res_get.stdout)
