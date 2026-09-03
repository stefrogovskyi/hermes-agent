import sys
import subprocess
import json

GOOGLE_API = '/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py'
SHEET_ID = '1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k'

def get_range(rng):
    cmd = [sys.executable, GOOGLE_API, 'sheets', 'get', SHEET_ID, f'Блогпосты Сирейтс!{rng}']
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        return None
    try:
        return json.loads(res.stdout)
    except Exception:
        return None

batch_size = 5000
start_row = 2
max_row = 23217

queue_count = 0

for b_start in range(start_row, max_row + 1, batch_size):
    b_end = min(b_start + batch_size - 1, max_row)
    rng = f'A{b_start}:G{b_end}'
    rows = get_range(rng)
    if not rows or not isinstance(rows, list):
        continue
    
    for idx, r in enumerate(rows):
        if not isinstance(r, list):
            continue
        while len(r) < 7:
            r.append('')
        col_a, col_b, col_c, col_d = r[0], r[1], r[2], r[3]
        
        status = col_d.strip()
        link = col_b.strip()
        
        if link and (link.startswith('http://') or link.startswith('https://')):
            if status in ['В очереди', '', 'In queue', 'Pending']:
                queue_count += 1

print(f"Remaining in queue: {queue_count}")
