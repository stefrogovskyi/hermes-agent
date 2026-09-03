import json, subprocess

def get_sheet_data(sheet_id, range_str):
    cmd = [
        "python3", "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py",
        "sheets", "get", sheet_id, range_str
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(res.stdout) if res.returncode == 0 else []

sheet_id = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"

for b_start in range(2, 23217 + 1, 5000):
    b_end = min(b_start + 4999, 23217)
    range_str = f"'Блогпосты Сирейтс'!A{b_start}:G{b_end}"
    data = get_sheet_data(sheet_id, range_str)
    for idx, row in enumerate(data):
        current_row_num = b_start + idx
        status = row[3].strip() if len(row) > 3 and row[3] else ""
        if status == "В процессе":
            print(f"Row {current_row_num} is 'В процессе': {row}")
