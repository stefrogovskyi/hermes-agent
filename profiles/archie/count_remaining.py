import subprocess
import json

cmd = [
    'python3', '/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py',
    'sheets', 'get', '1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k', "'Блогпосты Сирейтс'!A2:G23217"
]

res = subprocess.run(cmd, capture_output=True, text=True)
data = json.loads(res.stdout)

queue_count = 0
for idx, row in enumerate(data, start=2):
    link = row[1] if len(row) > 1 else ''
    status = row[3] if len(row) > 3 else ''
    
    if not link or not link.startswith('http'):
        continue
        
    st_clean = status.strip()
    if st_clean in ['В очереди', '']:
        queue_count += 1

print(f"EXACT REMAINING IN QUEUE: {queue_count}")
