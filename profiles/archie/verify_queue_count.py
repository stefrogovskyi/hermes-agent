import subprocess
import json

SHEET_ID = '1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k'
ranges = [
    "'Блогпосты Сирейтс'!A2:G5000",
    "'Блогпосты Сирейтс'!A5001:G10000",
    "'Блогпосты Сирейтс'!A10001:G15000",
    "'Блогпосты Сирейтс'!A15001:G20000",
    "'Блогпосты Сирейтс'!A20001:G23217"
]

remaining_in_queue = 0
done_count = 0
in_progress_count = 0
error_count = 0
invalid_count = 0

for r_idx, r in enumerate(ranges):
    cmd = ['python3', '/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py', 'sheets', 'get', SHEET_ID, r]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error fetching {r}: {res.stderr}")
        continue
    data = json.loads(res.stdout)
    if isinstance(data, dict):
        values = data.get('values', [])
    elif isinstance(data, list):
        values = data
    else:
        values = []
        
    for row in values:
        url = row[1].strip() if len(row) > 1 else ''
        status = row[3].strip() if len(row) > 3 else ''
        
        if not url or not url.startswith('http'):
            invalid_count += 1
            continue
            
        if status in ['В очереди', ''] or not status:
            remaining_in_queue += 1
        elif status == 'Готово':
            done_count += 1
        elif status == 'В процессе':
            in_progress_count += 1
        elif status == 'Ошибка':
            error_count += 1

print(f"REMAINING IN QUEUE: {remaining_in_queue}")
print(f"DONE: {done_count}")
print(f"IN PROGRESS: {in_progress_count}")
print(f"ERROR: {error_count}")
print(f"INVALID / SKIPPED: {invalid_count}")

with open('/opt/hermes/profiles/archie/queue_stats.json', 'w', encoding='utf-8') as f:
    json.dump({
        'remaining_in_queue': remaining_in_queue,
        'done_count': done_count,
        'in_progress_count': in_progress_count,
        'error_count': error_count,
        'invalid_count': invalid_count
    }, f, ensure_ascii=False, indent=2)
