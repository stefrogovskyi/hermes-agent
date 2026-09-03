import subprocess
import json
import sys

SHEET_ID = '1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k'
CLI = '/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py'

def get_range(rng):
    res = subprocess.run(['python3', CLI, 'sheets', 'get', SHEET_ID, rng], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error getting {rng}: {res.stderr}")
        return None
    try:
        return json.loads(res.stdout)
    except Exception as e:
        print(f"JSON parse error for {rng}: {e}, stdout: {res.stdout[:200]}")
        return None

if __name__ == '__main__':
    data = get_range("'Блогпосты Сирейтс'!A1:G10")
    print("First 10 rows:", json.dumps(data, ensure_ascii=False, indent=2))
