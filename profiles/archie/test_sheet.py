import subprocess
import json

python_bin = "python3"
script = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"
sheet_id = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
sheet_name = "Блогпосты Сирейтс"

# Let's test reading A2:G100 to see format returned by google_api.py
cmd = [python_bin, script, "sheets", "get", "--spreadsheet-id", sheet_id, "--range", f"'{sheet_name}'!A1:G10"]
res = subprocess.run(cmd, capture_output=True, text=True)
print("Returncode:", res.returncode)
print("Stdout snippet:", res.stdout[:1000])
print("Stderr snippet:", res.stderr[:1000])
