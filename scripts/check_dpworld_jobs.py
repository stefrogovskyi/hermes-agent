import os
import json
import urllib.request
from datetime import datetime

HERMES_HOME = os.environ.get("HERMES_HOME", "/opt/hermes")
CACHE_DIR = os.path.join(HERMES_HOME, "cache")
os.makedirs(CACHE_DIR, exist_ok=True)
CACHE_FILE = os.path.join(CACHE_DIR, 'dpworld_seen_jobs.json')

API_URL = 'https://ehpv.fa.em2.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true&expand=all&finder=findReqs;siteNumber=CX_1,limit=50,sortBy=POSTING_DATES_DESC'

def fetch_jobs():
    req = urllib.request.Request(API_URL, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        items = data.get('items', [])
        if items:
            return items[0].get('requisitionList', [])
    return []

def main():
    seen_ids = set()
    is_first_run = not os.path.exists(CACHE_FILE)

    if not is_first_run:
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                saved_data = json.load(f)
                seen_ids = set(saved_data.get('seen_ids', []))
        except Exception as e:
            seen_ids = set()

    jobs = fetch_jobs()
    if not jobs:
        print("Не удалось получить данные о вакансиях DP World.")
        return

    new_jobs = []
    current_all_ids = set(seen_ids)

    for r in jobs:
        job_id = str(r.get('Id'))
        current_all_ids.add(job_id)
        if is_first_run:
            # На первом запуске берем вакансии за текущую/последнюю дату (например 2026-08-05 или за последние 24ч)
            posted_date = r.get('PostedDate', '')
            # Берем самую свежую дату в списке
            top_date = jobs[0].get('PostedDate', '')
            if posted_date == top_date:
                new_jobs.append(r)
        else:
            if job_id not in seen_ids:
                new_jobs.append(r)

    # Сохраняем обновленный список ID
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump({'seen_ids': list(current_all_ids), 'last_check': datetime.now().isoformat()}, f, ensure_ascii=False, indent=2)

    if new_jobs:
        if is_first_run:
            print(f"### 📋 DP World Careers — Вакансии (Первичный срез на {datetime.now().strftime('%d.%m.%Y')}):\n")
        else:
            print(f"### 🆕 Обнаружены новые вакансии DP World ({len(new_jobs)}):\n")

        for r in new_jobs:
            job_id = r.get('Id')
            title = r.get('Title')
            date = r.get('PostedDate')
            loc = r.get('PrimaryLocation', 'Не указано')
            category = r.get('Category', '')
            job_url = f"https://ehpv.fa.em2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/{job_id}"
            
            line = f"- **[{title}]({job_url})**\n  📍 Location: `{loc}` | 📅 Posted: `{date}`"
            if category:
                line += f" | 🏷️ Category: `{category}`"
            print(line + "\n")
    else:
        print("Новых вакансий DP World за прошедшие сутки не обнаружено.")

if __name__ == '__main__':
    main()
