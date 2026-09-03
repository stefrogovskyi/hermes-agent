import subprocess
import json
import sys

SHEET_ID = '1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k'
TAB = 'Блогпосты Сирейтс'
GOOGLE_API = '/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py'

row_num = 175
status = "Готово"
new_title = "Shipping Container History and Future Outlook"
file_url = "https://docs.google.com/document/d/17vmUr_W0G6NvqtshQhW5NEE6FXZ7RtYQ/edit?usp=drivesdk&ouid=100676658802001293117&rtpof=true&sd=true"

def update_row():
    # Range for D175:F175
    rng = f"{TAB}!D{row_num}:F{row_num}"
    values = json.dumps([[status, new_title, file_url]])
    
    cmd = ['python3', GOOGLE_API, 'sheets', 'update', SHEET_ID, rng, '--values', values]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error updating row: {res.stderr}", file=sys.stderr)
        return False
        
    print(f"Update response: {res.stdout}")
    
    # Read back full row A175:F175 to verify
    rng_full = f"{TAB}!A{row_num}:F{row_num}"
    cmd_get = ['python3', GOOGLE_API, 'sheets', 'get', SHEET_ID, rng_full]
    res_get = subprocess.run(cmd_get, capture_output=True, text=True)
    if res_get.returncode == 0:
        data = json.loads(res_get.stdout)
        print("\nReadback confirmation for row 175:")
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return True
    else:
        print(f"Readback failed: {res_get.stderr}", file=sys.stderr)
        return False

if __name__ == "__main__":
    update_row()
