import subprocess
import json
import sys

sheet_id = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
range_d_f = "'Блогпосты Сирейтс'!D350:F350"

new_status = "Готово"
new_title = "Protecting Modern Logistics Through IT and Cybersecurity"
new_link = "https://docs.google.com/document/d/13D4vGcGjyqOfF4zo7kVgz_oe25oVtJbi/edit?usp=drivesdk&ouid=100676658802001293117&rtpof=true&sd=true"

values = [[new_status, new_title, new_link]]

# 1. Update range
cmd_update = [
    "python3",
    "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py",
    "sheets", "update",
    "--values", json.dumps(values),
    sheet_id, range_d_f
]

res_up = subprocess.run(cmd_update, capture_output=True, text=True)
print("Update response:", res_up.stdout)
if res_up.returncode != 0:
    print("Update error:", res_up.stderr)
    sys.exit(1)

# 2. Read back to confirm
range_get = "'Блогпосты Сирейтс'!A350:F350"
cmd_get = [
    "python3",
    "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py",
    "sheets", "get",
    sheet_id, range_get
]

res_get = subprocess.run(cmd_get, capture_output=True, text=True)
print("Read back row 350:", res_get.stdout)
