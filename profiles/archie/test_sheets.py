import subprocess
import sys

SHEET_ID = '1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k'
SCRIPT_PATH = '/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py'

cmd = [
    'python3', SCRIPT_PATH,
    'sheets', 'get', SHEET_ID, "Блогпосты Сирейтс!A1:G5"
]
res = subprocess.run(cmd, capture_output=True, text=True)
print("Returncode:", res.returncode)
print("Stdout:", res.stdout[:1000])
print("Stderr:", res.stderr)
