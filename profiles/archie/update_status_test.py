import subprocess
import json

sheet_id = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
range_str = "Блогпосты Сирейтс!D132:D132"
values = json.dumps([["В процессе"]])

res = subprocess.run([
    "python3", "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py",
    "sheets", "update", sheet_id, range_str, "--values", values
], capture_output=True, text=True)

print("Update stdout:", res.stdout)
print("Update stderr:", res.stderr)

# Verify with get
res_get = subprocess.run([
    "python3", "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py",
    "sheets", "get", sheet_id, range_str
], capture_output=True, text=True)

print("Verification get stdout:", res_get.stdout)
