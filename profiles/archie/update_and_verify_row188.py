import subprocess
import json

sheet_id = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
google_api_script = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"

# Read draft for title and link
with open('/opt/hermes/profiles/archie/rewrite_draft.json', 'r') as f:
    draft = json.load(f)

new_title = draft['title']

with open('/opt/hermes/profiles/archie/upload_res.json', 'r') as f:
    upload_res = json.load(f)

web_view_link = upload_res['webViewLink']

# Update range D188:F188
# Column D = Готово, Column E = new_title, Column F = web_view_link
values = [["Готово", new_title, web_view_link]]
values_json = json.dumps(values)

cmd_update = [
    "python3", google_api_script, "sheets", "update",
    sheet_id, "'Блогпосты Сирейтс'!D188:F188",
    "--values", values_json
]

print("Executing update...")
res_update = subprocess.run(cmd_update, capture_output=True, text=True)
print("Update output:", res_update.stdout)

# Read back to verify
cmd_get = [
    "python3", google_api_script, "sheets", "get",
    sheet_id, "'Блогпосты Сирейтс'!A188:F188"
]

print("Reading back row 188...")
res_get = subprocess.run(cmd_get, capture_output=True, text=True)
print("Read back result:\n", res_get.stdout)

data = json.loads(res_get.stdout)
row = data[0] if data else []

print("Verified Row 188 Contents:")
print("Col A (Orig Title):", row[0] if len(row) > 0 else "")
print("Col B (Orig URL):", row[1] if len(row) > 1 else "")
print("Col C (Lang):", row[2] if len(row) > 2 else "")
print("Col D (Status):", row[3] if len(row) > 3 else "")
print("Col E (Navo Title):", row[4] if len(row) > 4 else "")
print("Col F (Doc Link):", row[5] if len(row) > 5 else "")
