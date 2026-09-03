import subprocess
import json

cli_path = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"
sheet_id = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
range_str = "'Блогпосты Сирейтс'!D315:F315"

new_title = "SeaRates System Release Notes: Week 48, 2024 Updates"
file_link = "https://docs.google.com/document/d/1vnAO6_YugLkMyb8OJTyoF015M7FoOqVf/edit?usp=drivesdk&ouid=100676658802001293117&rtpof=true&sd=true"

values = [["Готово", new_title, file_link]]

cmd = [
    "python3", cli_path, "sheets", "update",
    sheet_id, range_str,
    "--values", json.dumps(values)
]

res = subprocess.run(cmd, capture_output=True, text=True)
print("Update returncode:", res.returncode)
print("Update output:", res.stdout)
if res.stderr:
    print("Update stderr:", res.stderr)
