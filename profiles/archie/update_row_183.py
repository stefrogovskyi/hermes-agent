import subprocess
import json

SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
TAB_NAME = "Блогпосты Сирейтс"
SCRIPT_PATH = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"

ROW_NUM = 183
STATUS = "Готово"
NEW_TITLE = "German Truck Towing: Night, Holiday & Cost Guide"
FILE_LINK = "https://docs.google.com/document/d/1kWhSwpdZXiZI2aVN7xxRRHP7oMsLLQ9M/edit?usp=drivesdk&ouid=100676658802001293117&rtpof=true&sd=true"

def update_and_verify():
    cell_range = f"{TAB_NAME}!D{ROW_NUM}:F{ROW_NUM}"
    values = [[STATUS, NEW_TITLE, FILE_LINK]]
    
    cmd_update = [
        "python3", SCRIPT_PATH, "sheets", "update",
        SHEET_ID, cell_range,
        "--values", json.dumps(values)
    ]
    res = subprocess.run(cmd_update, capture_output=True, text=True)
    print("Update stdout:", res.stdout)
    if res.stderr:
        print("Update stderr:", res.stderr)

    # Readback
    cmd_get = [
        "python3", SCRIPT_PATH, "sheets", "get",
        SHEET_ID, cell_range
    ]
    res_get = subprocess.run(cmd_get, capture_output=True, text=True)
    print("Readback result:", res_get.stdout)

if __name__ == "__main__":
    update_and_verify()
