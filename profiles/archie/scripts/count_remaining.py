import subprocess
import json

SHEET_ID = '1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k'
CHUNK_SIZE = 5000
TOTAL_ROWS = 23217

queue_count = 0

for start in range(2, TOTAL_ROWS + 1, CHUNK_SIZE):
    end = min(start + CHUNK_SIZE - 1, TOTAL_ROWS)
    rng = f"'Блогпосты Сирейтс'!A{start}:D{end}"
    cmd = ['python3', '/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py', 'sheets', 'get', SHEET_ID, rng]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        data = json.loads(res.stdout)
        for row in data:
            r = row + [''] * (4 - len(row))
            url = r[1].strip()
            status = r[3].strip()
            if url and url.startswith('http') and status in ['В очереди', '', None]:
                queue_count += 1

print(f"Exact remaining queue count: {queue_count}")
