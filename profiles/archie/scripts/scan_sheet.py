import subprocess
import json

SHEET_ID = '1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k'
CHUNK_SIZE = 5000
TOTAL_ROWS = 23217

all_rows = []
for start in range(2, TOTAL_ROWS + 1, CHUNK_SIZE):
    end = min(start + CHUNK_SIZE - 1, TOTAL_ROWS)
    rng = f"'Блогпосты Сирейтс'!A{start}:G{end}"
    print(f"Fetching {rng}...")
    cmd = ['python3', '/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py', 'sheets', 'get', SHEET_ID, rng]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error fetching {rng}: {res.stderr}")
        break
    data = json.loads(res.stdout)
    print(f"Fetched {len(data)} rows.")
    all_rows.extend(data)

print(f"Total rows fetched: {len(all_rows)}")

first_queued = None
queue_count = 0

for i, row in enumerate(all_rows, start=2):
    r = row + [''] * (6 - len(row))
    orig_title = r[0].strip()
    url = r[1].strip()
    lang = r[2].strip()
    status = r[3].strip()
    
    if not url or not url.startswith('http'):
        continue
    
    if status in ['В очереди', '', None]:
        queue_count += 1
        if first_queued is None:
            first_queued = (i, orig_title, url, lang, status)

print(f"First queued row: {first_queued}")
print(f"Total in queue: {queue_count}")

if first_queued:
    with open('/opt/hermes/profiles/archie/first_queued.json', 'w', encoding='utf-8') as f:
        json.dump({
            'row_num': first_queued[0],
            'orig_title': first_queued[1],
            'url': first_queued[2],
            'lang': first_queued[3],
            'status': first_queued[4],
            'queue_count': queue_count
        }, f, ensure_ascii=False, indent=2)
