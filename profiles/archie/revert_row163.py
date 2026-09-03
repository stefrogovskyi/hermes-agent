import subprocess
import json

SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
TAB_NAME = "Блогпосты Сирейтс"
CLI_PATH = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"

row = 163
status = "В очереди"

cmd = [
    "python3", CLI_PATH, "sheets", "update",
    "--values", '[["В очереди"]]',
    SHEET_ID, f"'{TAB_NAME}'!D{row}"
]

res = subprocess.run(cmd, capture_output=True, text=True)
print("Revert row 163 output:", res.stdout, res.stderr)

read_cmd = [
    "python3", CLI_PATH, "sheets", "get",
    SHEET_ID, f"'{TAB_NAME}'!A{row}:D{row}"
]
res_read = subprocess.run(read_cmd, capture_output=True, text=True)
print("Read back row 163:", res_read.stdout)
