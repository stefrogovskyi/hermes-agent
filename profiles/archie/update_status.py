import subprocess
import json
import sys

GOOGLE_API = '/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py'
SPREADSHEET_ID = '1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k'
SHEET_NAME = 'Блогпосты Сирейтс'

def update_cell(range_str, value):
    values_json = json.dumps([[value]])
    cmd = ['python3', GOOGLE_API, 'sheets', 'update', SPREADSHEET_ID, range_str, '--values', values_json]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error updating {range_str}: {res.stderr}")
        sys.exit(1)
    print(f"Updated {range_str} to '{value}': {res.stdout.strip()}")

if __name__ == '__main__':
    row_num = int(sys.argv[1])
    status = sys.argv[2]
    rng = f"'{SHEET_NAME}'!D{row_num}"
    update_cell(rng, status)
