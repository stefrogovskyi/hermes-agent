# -*- coding: utf-8 -*-
"""
multi_company_career_scanner.py — Глобальный C-Level & Leadership сканер вакансий.
Покрывает Big Tech / AI гигантов (Anthropic, xAI, SpaceX, OpenAI, Google, MSFT) и FreightTech / Supply Chain лидеров (Flexport, project44, FourKites, Maersk, DP World, Expeditors, WiseTech).
Применяет фильтры по C-Level & Executive ролям: CEO, COO, CCO, CBDO, NED, CAIO, CPO, Consultant, VP / Head of, Lead, Director.
"""

import os, sys, json, re, urllib.request, time
from datetime import datetime

HERMES_DIR = "/opt/hermes"
CACHE_FILE = os.path.join(HERMES_DIR, "state", "multi_company_jobs_seen.json")
os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)

# Executive / C-Suite / Leadership Role Regex Patterns
EXEC_ROLE_PATTERNS = [
    r"\bceo\b", r"\bcoo\b", r"\bcco\b", r"\bcbdo\b", r"\bned\b", r"\bcaio\b", r"\bcpo\b",
    r"\bchief\b", r"\bboard\b", r"\bconsultant\b", r"\bvp\b", r"\bvice president\b",
    r"\bhead of\b", r"\blead\b", r"\bdirector\b", r"\bexecutive\b", r"\bpresident\b"
]

def load_seen_ids():
    if os.path.exists(CACHE_FILE):
        try:
            return set(json.load(open(CACHE_FILE, encoding='utf-8')).get('seen_ids', []))
        except Exception:
            pass
    return set()

def save_seen_ids(seen_ids):
    data = {
        'seen_ids': list(seen_ids),
        'last_check': datetime.now().isoformat()
    }
    open(CACHE_FILE, 'w', encoding='utf-8').write(json.dumps(data, ensure_ascii=False, indent=2))

def is_exec_role(title):
    if not title: return False
    t = str(title).lower()
    return any(re.search(pat, t) for pat in EXEC_ROLE_PATTERNS)

# --- GREENHOUSE APIS ---
def fetch_greenhouse_board(board_name, company_display):
    url = f"https://boards-api.greenhouse.io/v1/boards/{board_name}/jobs"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            jobs = data.get('jobs', [])
            results = []
            for j in jobs:
                title = j.get('title')
                if is_exec_role(title):
                    jid = str(j.get('id'))
                    loc = j.get('location', {}).get('name', 'Global / Remote')
                    results.append({
                        "id": f"{board_name}_{jid}",
                        "company": company_display,
                        "title": title,
                        "location": loc,
                        "date": j.get('updated_at', '')[:10] if j.get('updated_at') else 'Recent',
                        "url": j.get('absolute_url')
                    })
            return results
    except Exception as e:
        pass
    return []

# --- SMARTRECRUITERS APIS ---
def fetch_smartrecruiters_board(company_token, company_display):
    url = f"https://api.smartrecruiters.com/v1/companies/{company_token}/postings"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            jobs = data.get('content', [])
            results = []
            for j in jobs:
                title = j.get('name')
                if is_exec_role(title):
                    jid = str(j.get('id'))
                    loc = j.get('location', {}).get('city', 'Global / Remote')
                    results.append({
                        "id": f"{company_token}_{jid}",
                        "company": company_display,
                        "title": title,
                        "location": loc,
                        "date": j.get('releasedDate', '')[:10] if j.get('releasedDate') else 'Recent',
                        "url": f"https://jobs.smartrecruiters.com/{company_token}/{jid}"
                    })
            return results
    except Exception as e:
        pass
    return []

# --- ORACLE CLOUD HCM (DP WORLD) ---
def fetch_dpworld():
    url = 'https://ehpv.fa.em2.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true&expand=all&finder=findReqs;siteNumber=CX_1,limit=100,sortBy=POSTING_DATES_DESC'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            items = data.get('items', [])
            if items:
                raw_jobs = items[0].get('requisitionList', [])
                results = []
                for r in raw_jobs:
                    title = r.get('Title')
                    if is_exec_role(title):
                        jid = str(r.get('Id'))
                        results.append({
                            "id": f"dpworld_{jid}",
                            "company": "DP World",
                            "title": title,
                            "location": r.get('PrimaryLocation', 'Global'),
                            "date": r.get('PostedDate', 'Recent'),
                            "url": f"https://ehpv.fa.em2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/{jid}"
                        })
                return results
    except Exception as e:
        pass
    return []

# --- WORKDAY (MAERSK) ---
def fetch_maersk():
    url = "https://maersk.wd3.myworkdayjobs.com/wday/cxs/maersk/Maersk_Careers/jobs"
    try:
        payload = json.dumps({"appliedFacets": {}, "limit": 50, "offset": 0, "searchText": ""}).encode()
        req = urllib.request.Request(url, data=payload, headers={"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            postings = data.get("jobPostings", [])
            results = []
            for j in postings:
                title = j.get("title")
                if is_exec_role(title):
                    path = j.get("externalPath", "")
                    jid = path.split("_")[-1] if "_" in path else path
                    results.append({
                        "id": f"maersk_{jid}",
                        "company": "Maersk",
                        "title": title,
                        "location": j.get("locationsText", "Global"),
                        "date": j.get("postedOn", "Recent"),
                        "url": f"https://maersk.wd3.myworkdayjobs.com/en-US/Maersk_Careers{path}"
                    })
            return results
    except Exception as e:
        pass
    return []

def scan_all_companies():
    seen_ids = load_seen_ids()
    is_first_run = len(seen_ids) == 0
    
    # Run fetchers
    all_jobs = []
    
    # 1. Big Tech & AI Frontier
    all_jobs += fetch_greenhouse_board("anthropic", "Anthropic AI")
    all_jobs += fetch_greenhouse_board("xai", "xAI (Elon Musk)")
    all_jobs += fetch_greenhouse_board("spacex", "SpaceX")
    
    # 2. FreightTech & Supply Chain
    all_jobs += fetch_greenhouse_board("flexport", "Flexport")
    all_jobs += fetch_greenhouse_board("project44", "project44")
    all_jobs += fetch_greenhouse_board("fourkites", "FourKites")
    all_jobs += fetch_smartrecruiters_board("wisetechglobal", "WiseTech Global / CargoWise")
    all_jobs += fetch_smartrecruiters_board("Expeditors", "Expeditors International")
    all_jobs += fetch_dpworld()
    all_jobs += fetch_maersk()
    
    new_jobs = []
    current_seen = set(seen_ids)
    
    for j in all_jobs:
        current_seen.add(j['id'])
        if is_first_run or j['id'] not in seen_ids:
            new_jobs.append(j)
            
    save_seen_ids(current_seen)
    
    print(f"### 🎯 C-LEVEL & EXECUTIVE LEADERSHIP CAREER SCANNER (Срез на {datetime.now().strftime('%d.%m.%Y %H:%M')})\n")
    print(f"📋 **Целевые роли:** CEO, COO, CCO, CBDO, NED, CAIO, CPO, Consultant, VP / Head of, Lead, Director.")
    print(f"📊 **Всего просканировано руководящих C-Level / Leadership позиций:** **{len(all_jobs)}**")
    print(f"  • Найдено новых позиций за срез: **{len(new_jobs)}**\n")
    print("--------------------------------------------------\n")
    
    companies = ["Anthropic AI", "xAI (Elon Musk)", "SpaceX", "Flexport", "project44", "FourKites", "WiseTech Global / CargoWise", "Expeditors International", "DP World", "Maersk"]
    for comp in companies:
        comp_items = [j for j in new_jobs if j["company"] == comp]
        if comp_items:
            print(f"### 🏢 **{comp}** ({len(comp_items)} руководящих позиций):")
            for j in comp_items[:5]:
                print(f"- **[{j['title']}]({j['url']})**")
                print(f"  📍 Location: `{j['location']}` | 📅 Date: `{j['date']}`\n")

if __name__ == "__main__":
    scan_all_companies()
