import subprocess
import json

SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
TAB_NAME = "Блогпосты Сирейтс"
SCRIPT_PATH = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"

def set_status(row_num, status):
    cell_range = f"{TAB_NAME}!D{row_num}"
    values_json = json.dumps([[status]])
    cmd = [
        "python3", SCRIPT_PATH, "sheets", "update",
        SHEET_ID, cell_range, "--values", values_json
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(f"Update response: {res.stdout}")
    if res.stderr:
        print(f"Stderr: {res.stderr}")

    # Verify back
    check_cmd = [
        "python3", SCRIPT_PATH, "sheets", "get",
        SHEET_ID, cell_range
    ]
    check_res = subprocess.run(check_cmd, capture_output=True, text=True)
    print(f"Verified value back: {check_res.stdout}")

if __name__ == "__main__":
    set_status(183, "В процессе")
