import json
import subprocess
import sys

SHEET_ID = '1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k'
SCRIPT_PATH = '/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py'

row_idx = 269
rng = f"Блогпосты Сирейтс!D{row_idx}:D{row_idx}"
values_json = json.dumps([["В процессе"]])

cmd = [
    'python3', SCRIPT_PATH,
    'sheets', 'update', SHEET_ID, rng, '--values', values_json
]
res = subprocess.run(cmd, capture_output=True, text=True)
print("Returncode:", res.returncode)
print("Stdout:", res.stdout)
print("Stderr:", res.stderr)
