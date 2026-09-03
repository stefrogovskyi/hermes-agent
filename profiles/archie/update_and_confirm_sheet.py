import subprocess
import json
import sys

SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
TAB_NAME = "Блогпосты Сирейтс"
PYTHON_CLI = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"

row_num = 161
new_title = "Hidden Shipyard Risks That Freeze Supply Chains"
web_view_link = "https://docs.google.com/document/d/1cK1VKNoJphRltYQj8Cx9KPyqIjJS3dxl/edit?usp=drivesdk&ouid=100676658802001293117&rtpof=true&sd=true"

def update_row():
    # Update range D161:F161
    range_str = f"'{TAB_NAME}'!D{row_num}:F{row_num}"
    values = [["Готово", new_title, web_view_link]]
    values_json = json.dumps(values)
    
    cmd = ["python3", PYTHON_CLI, "sheets", "update", SHEET_ID, range_str, "--values", values_json]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Update error: {res.stderr}")
        return False
    print("Update stdout:", res.stdout)
    return True

def confirm_readback():
    range_str = f"'{TAB_NAME}'!A{row_num}:F{row_num}"
    cmd = ["python3", PYTHON_CLI, "sheets", "get", SHEET_ID, range_str]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Readback error: {res.stderr}")
        return None
    data = json.loads(res.stdout)
    print("Readback data:", data)
    return data

if __name__ == "__main__":
    if update_row():
        confirm_readback()
