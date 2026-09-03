import json
import subprocess

SHEET_ID = '1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k'
API_SCRIPT = '/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py'
range_str = 'Блогпосты Сирейтс!D208'
values_json = json.dumps([['В процессе']])
cmd_update = ['python3', API_SCRIPT, 'sheets', 'update', SHEET_ID, range_str, '--values', values_json]
res = subprocess.run(cmd_update, capture_output=True, text=True)
print('Update output:', res.stdout, res.stderr)
