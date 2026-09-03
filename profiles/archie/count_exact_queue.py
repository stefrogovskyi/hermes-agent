import subprocess
import json

cmd = ['python3', '/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py', 'sheets', 'get', '1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k', "'Блогпосты Сирейтс'!A2:G23217"]
res = subprocess.run(cmd, capture_output=True, text=True)

try:
    data = json.loads(res.stdout)
except Exception as e:
    print(f"JSON load error: {e}")
    exit(1)

in_queue_count = 0
done_count = 0
in_progress_count = 0
error_count = 0

for idx, row in enumerate(data, start=2):
    url = row[1] if len(row) > 1 else ''
    status = row[3] if len(row) > 3 else ''
    
    if not url or not url.startswith('http'):
        continue
        
    if status in ['В очереди', '', None]:
        in_queue_count += 1
    elif status == 'Готово':
        done_count += 1
    elif status == 'В процессе':
        in_progress_count += 1
    elif status == 'Ошибка':
        error_count += 1

print(f"Total valid articles scanned: {len(data)}")
print(f"Total remaining 'В очереди': {in_queue_count}")
print(f"Total 'Готово': {done_count}")
print(f"Total 'В процессе': {in_progress_count}")
print(f"Total 'Ошибка': {error_count}")
