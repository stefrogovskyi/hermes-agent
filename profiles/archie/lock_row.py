import subprocess
import json
import sys

SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
SCRIPT = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"

def update_status(row, status):
    rng = f"D{row}"
    cmd = ["python3", SCRIPT, "sheets", "update", SHEET_ID, f"Блогпосты Сирейтс!{rng}", "--values", json.dumps([[status]])]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(f"Update D{row} to '{status}' stdout:", res.stdout)
    if res.returncode != 0:
        print(f"Update error: {res.stderr}", file=sys.stderr)
        return False
    
    # Verify
    cmd_get = ["python3", SCRIPT, "sheets", "get", SHEET_ID, f"Блогпосты Сирейтс!{rng}"]
    res_get = subprocess.run(cmd_get, capture_output=True, text=True)
    print(f"Verify D{row}:", res_get.stdout)
    return True

if __name__ == "__main__":
    update_status(169, "В процессе")
