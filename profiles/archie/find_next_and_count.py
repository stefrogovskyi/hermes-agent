import subprocess
import json
import sys

SHEET_ID = '1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k'
TAB_NAME = 'Блогпосты Сирейтс'

def get_sheet_range(sheet_id, range_name):
    cmd = [
        'python3',
        '/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py',
        'sheets',
        'get',
        sheet_id,
        range_name
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error fetching {range_name}: {res.stderr}", file=sys.stderr)
        return []
    try:
        data = json.loads(res.stdout)
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return data.get('values', [])
    except Exception as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        return []
    return []

def main():
    batch_size = 5000
    start_row = 2
    max_row = 23217
    
    first_target = None
    queue_count = 0
    
    current_start = start_row
    while current_start <= max_row:
        current_end = min(current_start + batch_size - 1, max_row)
        range_str = f"{TAB_NAME}!A{current_start}:G{current_end}"
        print(f"Fetching range {range_str}...")
        rows = get_sheet_range(SHEET_ID, range_str)
        
        if not rows:
            print(f"No rows returned for {range_str}")
            break
            
        for offset, row in enumerate(rows):
            row_num = current_start + offset
            
            # Extract fields
            title_orig = row[0].strip() if len(row) > 0 else ""
            link_orig = row[1].strip() if len(row) > 1 else ""
            lang = row[2].strip() if len(row) > 2 else ""
            status = row[3].strip() if len(row) > 3 else ""
            
            # Check valid link
            if not link_orig or not link_orig.startswith("http"):
                continue
                
            # Check if in queue (status == "В очереди" or status == "" or missing)
            if status in ["", "В очереди"] or not status:
                queue_count += 1
                if first_target is None:
                    first_target = {
                        "row_num": row_num,
                        "title_orig": title_orig,
                        "link_orig": link_orig,
                        "lang": lang,
                        "status": status
                    }
                    print(f"FOUND TARGET ROW {row_num}: {first_target}")
                    
        current_start += len(rows)
        if len(rows) < batch_size:
            # Reached end of sheet
            break

    print(f"\n--- SCAN RESULTS ---")
    print(f"First target row: {first_target}")
    print(f"Total remaining in queue: {queue_count}")

    # Save target info to json file
    with open('/opt/hermes/profiles/archie/target_info.json', 'w', encoding='utf-8') as f:
        json.dump({
            "first_target": first_target,
            "queue_count": queue_count
        }, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
