import json
import subprocess

SHEET_ID = '1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k'
ROW_NUM = 357

with open('/opt/hermes/profiles/archie/subagent1_output.json', 'r', encoding='utf-8') as f:
    sub1_data = json.load(f)

new_title = sub1_data['title']

with open('/opt/hermes/profiles/archie/upload_result.json', 'r', encoding='utf-8') as f:
    upload_data = json.load(f)

web_view_link = upload_data.get('webViewLink')

# Update columns D, E, F for row 357
# D = Status ("Готово")
# E = Navo Title
# F = Navo Link / File Link
range_str = f"'Блогпосты Сирейтс'!D{ROW_NUM}:F{ROW_NUM}"
values = [["Готово", new_title, web_view_link]]

values_json = json.dumps(values)

cmd_update = [
    'python3',
    '/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py',
    'sheets', 'update',
    '--values', values_json,
    SHEET_ID, range_str
]

res_up = subprocess.run(cmd_update, capture_output=True, text=True)
print("UPDATE STDOUT:", res_up.stdout)
print("UPDATE STDERR:", res_up.stderr)

# Read back to verify
range_read = f"'Блогпосты Сирейтс'!A{ROW_NUM}:G{ROW_NUM}"
cmd_read = [
    'python3',
    '/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py',
    'sheets', 'get',
    SHEET_ID, range_read
]

res_read = subprocess.run(cmd_read, capture_output=True, text=True)
print("READ BACK STDOUT:", res_read.stdout)

read_data = json.loads(res_read.stdout)
print("VERIFIED ROW VALUES:", read_data)
