#!/usr/bin/env python3
"""
Upwork Radar — AI Opportunity Scanner for Stefan Rogovskiy (Avalanche Agency & Enlight Group)
Monitors high-value freelance & agency jobs matching core domain themes:
- Logistics, Shipping & Freight
- International Trade & Customs
- AI, LLMs & RAG
- Autonomous Agents & Multi-Agent Systems
- Robotics & Hardware Automation
- Workflow Automation (n8n, Make, Zapier, Python)
- Full-Stack Tech & Integrations
"""

import subprocess
import json
import sqlite3
import os
import datetime
import re
import sys

DB_PATH = "/opt/hermes/profiles/ben/data/upwork_radar.db"

PRIORITY_SEARCH_TERMS = [
    '("autonomous agent" OR "AI agent" OR "agentic AI" OR "LLM RAG")',
    '("logistics software" OR "freight automation" OR "shipping tracking" OR "supply chain")',
    '("robotics" OR "ROS" OR "n8n" OR "workflow automation")',
    '("international trade" OR "customs automation" OR "inventory RFID")'
]

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS seen_jobs (
            job_id TEXT PRIMARY KEY,
            title TEXT,
            url TEXT,
            budget REAL,
            job_type TEXT,
            client_country TEXT,
            client_spend TEXT,
            created_at TEXT,
            alerted_at TEXT,
            score INTEGER
        )
    """)
    conn.commit()
    conn.close()

def is_job_seen(job_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM seen_jobs WHERE job_id = ?", (str(job_id),))
    res = cur.fetchone()
    conn.close()
    return res is not None

def mark_job_seen(job_id, title, url, budget, job_type, client_country, client_spend, score):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    now_str = datetime.datetime.now().isoformat()
    cur.execute("""
        INSERT OR REPLACE INTO seen_jobs 
        (job_id, title, url, budget, job_type, client_country, client_spend, created_at, alerted_at, score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (str(job_id), title, url, budget, job_type, client_country, client_spend, now_str, now_str, score))
    conn.commit()
    conn.close()

def fetch_jobs_for_query(query, limit=5):
    cmd = ["/usr/local/bin/upwork", "find_jobs", "search", "-p", f"query={query}", "-p", f"limit={limit}", "--json"]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if res.returncode == 0:
            data = json.loads(res.stdout)
            return data.get("jobs", [])
    except Exception as e:
        print(f"Error fetching query '{query}': {e}", file=sys.stderr)
    return []

def get_job_full_details(job_id):
    payload = json.dumps({"action": "get", "params": {"id": str(job_id)}})
    cmd = ["/usr/local/bin/upwork", "find_jobs", "--json", payload]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if res.returncode == 0:
            return json.loads(res.stdout)
    except Exception as e:
        print(f"Error getting details for {job_id}: {e}", file=sys.stderr)
    return None

def calculate_score(job, details=None):
    score = 50
    title = (job.get("title") or "").lower()
    desc = (job.get("description_snippet") or "").lower()
    full_text = title + " " + desc
    
    # Only filter out strictly offline or irrelevant physical sales jobs
    negative_terms = [
        "real estate agent", "travel agent", "insurance agent", 
        "door to door", "physical retail", "cosmetic beauty salon"
    ]
    for neg in negative_terms:
        if neg in title:
            return 0  # Disqualify only physical offline jobs

    # Priority keywords bonus
    high_value_keywords = [
        "autonomous", "ai agent", "llm", "rag", "langchain", "crewai",
        "logistics", "freight", "shipping", "supply chain", "customs",
        "robotics", "ros", "n8n", "make.com", "workflow automation", "rfid",
        "python", "scraper", "scraping", "api", "data entry", "virtual assistant"
    ]
    for kw in high_value_keywords:
        if kw in full_text:
            score += 10
            
    # Budget evaluation: All budgets are welcome since agents execute at ~0 marginal cost!
    b_val = 0.0
    try:
        b_val = float(job.get("budget", 0) or 0)
    except:
        pass
        
    if job.get("job_type") == "fixed":
        if b_val >= 5000:
            score += 40
        elif b_val >= 1000:
            score += 25
        elif b_val >= 200:
            score += 15
        else:
            # Low fixed price is great for quick automated delivery & rapid 5-star review accumulation!
            score += 10
    elif job.get("job_type") == "hourly":
        score += 20
        
    # Client stats
    client = job.get("client", {})
    if client.get("verification_status") == "VERIFIED":
        score += 15
        
    country = client.get("country", "")
    tier1_countries = ["United States", "USA", "United Kingdom", "Canada", "Australia", "Germany", "Switzerland", "United Arab Emirates"]
    if any(c.lower() in country.lower() for c in tier1_countries):
        score += 15
        
    return score

def generate_cover_letter(title, desc, screening_questions, contract_type):
    # Professional cover letter in Stefan's proven voice
    pitch = (
        f"Hi there,\n\n"
        f"Stefan Rogovskiy here — Lead at Avalanche Agency and FreightWeb (part of Enlight Group). "
        f"I saw your posting for '{title}' and our team has direct, hands-on experience building exactly this.\n\n"
        f"Why we are uniquely qualified:\n"
        f"• Domain Expertise: We specialize in Log-Tech (freight, maritime shipping, GPS/RFID tracking, API integrations) "
        f"and Autonomous AI Systems (LLM orchestration, multi-agent workflows, process automation).\n"
        f"• End-to-End Delivery: We don't just write theory — we audit existing code, architect scalable workflows, and build rock-solid production software.\n"
        f"• Proven Track Record: 50+ enterprise and startup implementations, with measurable speed and revenue gains.\n\n"
        f"We are ready to start with an immediate code audit / discovery session to outline a concrete timeline and deliverables.\n\n"
        f"Best regards,\nStefan Rogovskiy\nAvalanche Agency"
    )
    
    q_answers = []
    if screening_questions:
        for idx, q in enumerate(screening_questions, 1):
            clean_q = re.sub(r'<[^>]+>', '', q).strip()
            ans = "Extensive production experience across our 50+ delivered projects (details & case studies available on our website aavalanche.com)."
            if "github" in clean_q.lower() or "website" in clean_q.lower():
                ans = "Website: https://aavalanche.com | GitHub / Portfolio can be shared upon interview."
            elif "framework" in clean_q.lower():
                ans = "Python (FastAPI, PyTorch, LangChain), Node.js, React/Next.js, Tailwind, Docker, PostgreSQL."
            elif "qa" in clean_q.lower() or "test" in clean_q.lower():
                ans = "Rigorous CI/CD pipelines, unit/integration testing, end-to-end automated flows, and staging regression suites."
            q_answers.append(f"**Q{idx}: {clean_q}**\n👉 *{ans}*")
            
    return pitch, q_answers

def scan_marketplace():
    init_db()
    qualified_jobs = []
    
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Starting Upwork Marketplace Scan...")
    
    for term in PRIORITY_SEARCH_TERMS:
        jobs = fetch_jobs_for_query(term, limit=4)
        for job in jobs:
            jid = str(job.get("id"))
            if is_job_seen(jid):
                continue
                
            score = calculate_score(job)
            if score < 75:  # Filter out low quality/irrelevant
                continue
                
            details = get_job_full_details(jid)
            if not details:
                continue
                
            posting = details.get("data", {}).get("marketplaceJobPosting", {})
            full_desc = posting.get("content", {}).get("description", "")
            screening_q = details.get("screening_questions", [])
            terms = posting.get("contractTerms", {})
            ctype = terms.get("contractType", "FIXED")
            
            title = job.get("title", "")
            url = job.get("url", f"https://www.upwork.com/jobs/~02{jid}")
            budget_val = 0.0
            try:
                budget_val = float(job.get("budget", 0) or 0)
            except:
                pass
            client = job.get("client", {})
            country = client.get("country", "Unknown")
            spend = client.get("total_spent", "$0")
            
            mark_job_seen(jid, title, url, budget_val, ctype, country, spend, score)
            
            cover_letter, answers = generate_cover_letter(title, full_desc, screening_q, ctype)
            connects_cost = details.get("connects_cost", 16)
            
            tier = "💎 High-Ticket Project" if (budget_val >= 1000 or (ctype == "HOURLY" and budget_val == 0)) else "⚡️ Fast Agent-Delivery (Quick 5★ Review)"
            qualified_jobs.append({
                "id": jid,
                "title": title,
                "tier": tier,
                "url": url,
                "budget": f"${budget_val:,.0f}" if budget_val > 0 else (ctype if ctype == "HOURLY" else "Negotiable"),
                "type": ctype,
                "country": country,
                "spend": spend,
                "score": score,
                "connects": connects_cost,
                "screening_questions": answers,
                "cover_letter": cover_letter
            })
            
    return qualified_jobs

if __name__ == "__main__":
    jobs = scan_marketplace()
    if not jobs:
        sys.exit(0)
        
    print(f"🎯 Upwork Radar: Найдено {len(jobs)} новых релевантных заказов!\n")
    for idx, j in enumerate(jobs, 1):
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"#{idx} {j['tier']} [{j['score']} pts]")
        print(f"🎯 {j['title']}")
        print(f"🔗 Ссылка: {j['url']}")
        print(f"💰 Бюджет: {j['budget']} ({j['type']}) | 🌍 Клиент: {j['country']} (Траты: {j['spend']}) | 🪙 Отклик: {j['connects']} connects")
        if j['screening_questions']:
            print(f"\n❓ Вопросы заказчика:")
            for q in j['screening_questions']:
                print(f"  {q}")
        print(f"\n📝 Готовый Cover Letter:")
        print(f"```\n{j['cover_letter']}\n```")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
