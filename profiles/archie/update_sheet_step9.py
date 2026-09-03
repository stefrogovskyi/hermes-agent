import subprocess, json, sys

sheet_id = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
row_num = 165
range_update = f"Блогпосты Сирейтс!D{row_num}:F{row_num}"

new_status = "Готово"
new_title = "SeaRates Platform Updates: Week 40, 2025"
new_link = "https://docs.google.com/document/d/1uvwZRlNv2DpChVfWaJMmtmTujmMxFBR9/edit?usp=drivesdk&ouid=100676658802001293117&rtpof=true&sd=true"

values = [[new_status, new_title, new_link]]

# Update sheet
update_cmd = [
    "python3",
    "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py",
    "sheets",
    "update",
    sheet_id,
    range_update,
    "--values",
    json.dumps(values)
]

res = subprocess.run(update_cmd, capture_output=True, text=True)
print("Update response:", res.stdout)
if res.returncode != 0:
    print("Update error:", res.stderr)
    sys.exit(1)

# Read back to verify
read_cmd = [
    "python3",
    "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py",
    "sheets",
    "get",
    sheet_id,
    f"Блогпосты Сирейтс!A{row_num}:F{row_num}"
]

res_read = subprocess.run(read_cmd, capture_output=True, text=True)
print("Readback response:", res_read.stdout)

data = json.loads(res_read.stdout)
print("VERIFIED ROW CONTENT:", data)
