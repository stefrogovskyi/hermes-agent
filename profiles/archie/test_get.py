import json, subprocess

cmd = [
    "python3", "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py",
    "sheets", "get", "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k", "'Блогпосты Сирейтс'!A2:G5"
]
res = subprocess.run(cmd, capture_output=True, text=True)
print("STDOUT:", res.stdout[:500])
