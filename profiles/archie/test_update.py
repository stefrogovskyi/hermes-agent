import subprocess
import json

SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
TAB_NAME = "Блогпосты Сирейтс"
CLI_PATH = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"

def update_cell(cell_ref, value):
    cmd = [
        "python3", CLI_PATH, "sheets", "update",
        "--values", json.dumps([[value]]),
        SHEET_ID, f"{TAB_NAME}!{cell_ref}"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error updating cell {cell_ref}: {res.stderr}")
        return False
    print(f"Successfully updated {cell_ref} to {value}, stdout: {res.stdout.strip()}")
    return True

update_cell("D347", "В процессе")
