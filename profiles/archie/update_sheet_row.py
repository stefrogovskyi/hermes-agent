import subprocess
import json

python_bin = "python3"
script = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"
sheet_id = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
sheet_name = "Блогпосты Сирейтс"
row_num = 326

new_title = "SeaRates Release Notes: Week 43, 2024"
web_view_link = "https://docs.google.com/document/d/1vhKrc6zv3D5VPKCfTJuOnhoKaDqtXGM8/edit?usp=drivesdk&ouid=100676658802001293117&rtpof=true&sd=true"

# Update D326:F326
range_str = f"'{sheet_name}'!D{row_num}:F{row_num}"
values = [["Готово", new_title, web_view_link]]

cmd = [python_bin, script, "sheets", "update", "--values", json.dumps(values), sheet_id, range_str]
res = subprocess.run(cmd, capture_output=True, text=True)
print("Update output:", res.stdout)
print("Update stderr:", res.stderr)

# Read back row D326:F326 to verify actual on-disk/sheet values
read_cmd = [python_bin, script, "sheets", "get", sheet_id, range_str]
res_read = subprocess.run(read_cmd, capture_output=True, text=True)
print("Read back output:", res_read.stdout)
