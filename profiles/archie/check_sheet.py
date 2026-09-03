import subprocess
import json

SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
TAB_NAME = "Блогпосты Сирейтс"
CLI_PATH = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"

def read_sheet_range(range_str):
    cmd = [
        "python3", CLI_PATH, "sheets", "get",
        SHEET_ID, range_str
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error reading range {range_str}: {res.stderr}")
        return None
    try:
        data = json.loads(res.stdout)
        return data
    except Exception as e:
        print(f"JSON parse error: {e}, output: {res.stdout[:500]}")
        return None

if __name__ == "__main__":
    data = read_sheet_range(f"'{TAB_NAME}'!A2:G5001")
    if isinstance(data, list):
        print("Success fetching range. Rows returned:", len(data))
        for i, row in enumerate(data[:10]):
            print(f"Row {i+2}: {row}")
    elif isinstance(data, dict):
        print("Success fetching range. Keys:", data.keys())
        rows = data.get("values", [])
        print("Rows returned:", len(rows))
        for i, row in enumerate(rows[:10]):
            print(f"Row {i+2}: {row}")
