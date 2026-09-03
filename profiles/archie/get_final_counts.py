import subprocess
import json

SHEET_ID = '1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k'
GOOGLE_API = '/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py'

def get_range(range_name):
    cmd = ['python3', GOOGLE_API, 'sheets', 'get', SHEET_ID, range_name]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        return []
    try:
        data = json.loads(res.stdout)
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return data.get('values', [])
        return []
    except Exception as e:
        return []

counts = {
    "total_valid": 0,
    "done": 0,
    "queued": 0,
    "in_progress": 0,
    "error": 0,
    "other": 0
}

batch_size = 5000
curr = 2
max_row = 23217

while curr <= max_row:
    end = min(curr + batch_size - 1, max_row)
    range_str = f"'Блогпосты Сирейтс'!A{curr}:D{end}"
    rows = get_range(range_str)
    
    for row in rows:
        link = row[1] if len(row) > 1 else ""
        status = row[3].strip() if len(row) > 3 and row[3] else ""
        
        if not link or not link.startswith("http"):
            continue
            
        counts["total_valid"] += 1
        if status == "Готово":
            counts["done"] += 1
        elif status in ["В очереди", "", None]:
            counts["queued"] += 1
        elif status == "В процессе":
            counts["in_progress"] += 1
        elif status == "Ошибка":
            counts["error"] += 1
        else:
            counts["other"] += 1
            
    curr = end + 1

print("FINAL QUEUE STATS:")
print(json.dumps(counts, indent=2))
