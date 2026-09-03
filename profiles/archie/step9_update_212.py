import json
import subprocess
import sys

SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
TAB = "Блогпосты Сирейтс"
PYTHON_BIN = sys.executable
CLI_SCRIPT = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"

row_num = 212
new_status = "Готово"
new_title = "Where Does Personal Data Go After You Ship Cargo?"
new_link = "https://docs.google.com/document/d/1Q7mG9gYA6WvyzIOdT3jpbwAiRTPaOkW4/edit?usp=drivesdk&ouid=100676658802001293117&rtpof=true&sd=true"

values = [[new_status, new_title, new_link]]
range_str = f"'{TAB}'!D{row_num}:F{row_num}"

cmd_update = [
    PYTHON_BIN, CLI_SCRIPT, "sheets", "update", SHEET_ID, range_str,
    "--values", json.dumps(values)
]

print("Updating sheet:", " ".join(cmd_update))
res_up = subprocess.run(cmd_update, capture_output=True, text=True)
print("UPDATE OUTPUT:", res_up.stdout)

# Confirm via sheets get
range_get = f"'{TAB}'!A{row_num}:F{row_num}"
cmd_get = [PYTHON_BIN, CLI_SCRIPT, "sheets", "get", SHEET_ID, range_get]
res_get = subprocess.run(cmd_get, capture_output=True, text=True)

print("GET CONFIRMATION OUTPUT:")
print(res_get.stdout)
