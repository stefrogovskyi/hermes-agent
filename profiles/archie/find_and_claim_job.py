import subprocess
import json
import sys

SHEET_ID = '1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k'
GOOGLE_API = '/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py'

def get_range(range_name):
    cmd = ['python3', GOOGLE_API, 'sheets', 'get', SHEET_ID, range_name]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error fetching range {range_name}: {res.stderr}", file=sys.stderr)
        return None
    try:
        data = json.loads(res.stdout)
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return data.get('values', [])
        return []
    except Exception as e:
        print(f"Error parsing json for {range_name}: {e}\nRaw output: {res.stdout[:200]}", file=sys.stderr)
        return None

def update_cell(cell_range, values_json):
    cmd = ['python3', GOOGLE_API, 'sheets', 'update', SHEET_ID, cell_range, '--values', json.dumps(values_json)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error updating {cell_range}: {res.stderr}", file=sys.stderr)
        return False
    return True

def main():
    batch_size = 5000
    start_row = 2
    max_row = 23217
    
    target_row = None
    target_data = None
    
    total_queued = 0
    
    print("Scanning Google Sheet for queued items...")
    
    curr = start_row
    while curr <= max_row:
        end = min(curr + batch_size - 1, max_row)
        range_str = f"'Блогпосты Сирейтс'!A{curr}:G{end}"
        print(f"Fetching {range_str}...")
        rows = get_range(range_str)
        if rows is None:
            print("Failed to fetch range, stopping.")
            break
            
        for idx, row in enumerate(rows):
            actual_row_num = curr + idx
            
            title = row[0] if len(row) > 0 else ""
            link = row[1] if len(row) > 1 else ""
            lang = row[2] if len(row) > 2 else ""
            status = row[3].strip() if len(row) > 3 and row[3] else ""
            
            if not link or not link.startswith("http"):
                continue
                
            is_queued = status in ["В очереди", "", None]
            if is_queued:
                total_queued += 1
                if target_row is None:
                    target_row = actual_row_num
                    target_data = {
                        "row_num": actual_row_num,
                        "title": title,
                        "link": link,
                        "lang": lang,
                        "status": status
                    }
        
        curr = end + 1

    print(f"\nScan complete. Total queued articles found: {total_queued}")
    
    if target_row is None or target_data is None:
        print("RESULT: QUEUE_EMPTY")
        with open("/opt/hermes/profiles/archie/job_result.json", "w") as f:
            json.dump({"status": "QUEUE_EMPTY", "total_queued": 0}, f)
        return

    print(f"Target selected: Row {target_row} - '{target_data['title']}' ({target_data['lang']}) - {target_data['link']}")
    
    cell = f"'Блогпосты Сирейтс'!D{target_row}"
    success = update_cell(cell, [["В процессе"]])
    if success:
        print(f"Successfully claimed row {target_row} (status set to 'В процессе')")
        with open("/opt/hermes/profiles/archie/job_result.json", "w") as f:
            json.dump({
                "status": "CLAIMED",
                "target": target_data,
                "total_queued": total_queued
            }, f, ensure_ascii=False, indent=2)
    else:
        print(f"Failed to claim row {target_row}")

if __name__ == "__main__":
    main()
