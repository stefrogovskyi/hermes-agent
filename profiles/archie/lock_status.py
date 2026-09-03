import subprocess
import json

SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
TAB = "Блогпосты Сирейтс"
GOOGLE_API = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"

ROW = 309
RANGE_D = f"{TAB}!D{ROW}"

# Update D309 to "В процессе"
vals = json.dumps([["В процессе"]])
cmd = ["python3", GOOGLE_API, "sheets", "update", SHEET_ID, RANGE_D, "--values", vals]
res = subprocess.run(cmd, capture_output=True, text=True)
print("Update output:", res.stdout, res.stderr)

# Verify read back
cmd_get = ["python3", GOOGLE_API, "sheets", "get", SHEET_ID, RANGE_D]
res_get = subprocess.run(cmd_get, capture_output=True, text=True)
print("Read back status:", res_get.stdout)
