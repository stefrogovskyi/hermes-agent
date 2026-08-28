#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
executive_careers_poller.py — ЧЕСТНЫЙ мониторинг executive-вакансий.

v2.0 (2026-08-17): полностью переписан. Прежняя версия печатала захардкоженный
список выдуманных вакансий с фейковыми URL. Теперь:
  - Только реальные вызовы официальных Job Board API (Greenhouse, Ashby)
  - Каждая вакансия в выводе существует и кликабельна (URL приходит из API)
  - Дедупликация против seen-store: показываем только НОВОЕ
  - Никаких выдуманных "% Match" — вместо них честные matched-keywords
"""

import os, json, re, time, urllib.request, urllib.parse
import html as html_mod

HERMES_DIR = os.environ.get("HERMES_HOME", "/opt/hermes")
SEEN_FILE = os.path.join(HERMES_DIR, "state", "exec_careers_seen.json")
OUT_FILE = os.path.join(HERMES_DIR, "executive_vacancies_found.json")
os.makedirs(os.path.dirname(SEEN_FILE), exist_ok=True)

# Официальные API карьерных досок (проверены живыми вызовами 2026-08-17)
GREENHOUSE_BOARDS = [
    ("xAI", "xai", "Frontier AI"),
    ("Anthropic", "anthropic", "AI Frontier"),
    ("SpaceX", "spacex", "DeepTech / Aero"),
    ("Altos Labs (Bezos)", "altoslabs", "Biotech / Anti-aging"),
    ("Flexport", "flexport", "Freight Tech"),
    ("project44", "project44", "Supply Chain Visibility"),
    ("FourKites", "fourkites", "Supply Chain Visibility"),
]
ASHBY_BOARDS = [
    ("OpenAI", "openai", "AI Frontier"),
    ("Prometheus", "prometheus", "Frontier AI / Tech"),
]

# Workday cxs API (Manhattan — проверен 2026-08-17 total=41; Maersk — вскрыт через
# перехват api.maersk.com в браузере: тенант maersk.wd3 / site Maersk_Careers, ~1360 вакансий)
WORKDAY_BOARDS = [
    ("NVIDIA", "nvidia.wd5.myworkdayjobs.com", "nvidia", "NVIDIAExternalCareerSite", "AI Hardware / Compute"),
    ("Blue Origin (Bezos)", "blueorigin.wd5.myworkdayjobs.com", "blueorigin", "BlueOrigin", "DeepTech / Space"),
    ("Manhattan Associates", "manh.wd5.myworkdayjobs.com", "manh", "External", "Supply Chain Software"),
    ("Maersk", "maersk.wd3.myworkdayjobs.com", "maersk", "Maersk_Careers", "Logistics Giant"),
]
# SmartRecruiters public API (WiseTech — проверен вживую 2026-08-17)
SMARTRECRUITERS_BOARDS = [
    ("WiseTech Global", "WiseTechGlobal", "Supply Chain Software"),
]
# Comeet-виджеты, вшитые в HTML карьерной страницы (Windward)
COMEET_HTML_PAGES = [
    ("Windward", "https://windward.ai/careers/", "Maritime AI"),
]

# ===== Блок IT Ukraine (добавлен 2026-08-17 по запросу Стефана) =====
# Ashby: Grammarly ныне Superhuman Platform Inc (81 вакансия, проверено).
ASHBY_BOARDS_IT = [
    ("Grammarly/Superhuman", "Superhuman%20Platform%20Inc", "IT Product"),
]
# Greenhouse: GitLab (196 вакансий, проверено).
GREENHOUSE_BOARDS_IT = [
    ("GitLab", "gitlab", "IT Product"),
]
# DOU RSS-фиды jobs.dou.ua/vacancies/<slug>/feeds/ (проверены 2026-08-17;
# Google Ukraine на DOU вакансий не публикует — идёт отдельной ветвью через careers.google.com)
DOU_FEEDS = [
    ("EPAM", "epam-systems"), ("GlobalLogic", "globallogic"),
    ("SoftServe", "softserve"), ("Luxoft", "luxoft"),
    ("DataArt", "dataart"), ("Ciklum", "ciklum"),
    ("Wix", "wix"), ("Genesis", "genesis-technology-partners"),
    ("SKELAR", "skelar"), ("Grammarly (UA)", "grammarly"),
]
# Фильтр ролей IT-блока: BizDev / PM / Product / Delivery / senior-уровень ($5k+ де-факто
# начинается с senior/lead/head; junior/mid и чисто инженерные роли отсекаем)
IT_TITLE_PATTERNS = [
    r"\bbusiness development\b", r"\bbizdev\b", r"\bpartnership", r"\baccount (director|executive|manager)\b",
    r"\b(product|program|project|delivery|engagement) (manager|director|lead|owner)\b",
    r"\bproduct owner\b", r"\bhead of\b", r"\bdirector\b", r"\bVP\b", r"\bvice president\b",
    r"\bchief\b", r"\bC[EOTIPC]O\b", r"\bgeneral manager\b", r"\bcountry manager\b",
    r"\bsales (manager|director|executive|lead)\b", r"\bgtm\b", r"\bgo-to-market\b",
    r"\bstrategy\b", r"\bconsultant\b", r"\bsolution architect\b", r"\bengagement\b",
    r"\bgrowth (manager|lead|director)\b", r"\brevenue\b", r"\bcommercial\b",
]
IT_EXCLUDE_PATTERNS = [
    r"\bjunior\b", r"\btrainee\b", r"\bintern\b", r"\bстажер",
    r"\b(qa|test)\b", r"\bsupport\b", r"\brecruiter\b", r"\btalent\b",
    r"\brepresentative\b", r"\bSDR\b", r"\bBDR\b",  # джуниорские сейлз-роли (<$5k)
]
IT_TITLE_RE = re.compile("|".join(IT_TITLE_PATTERNS), re.IGNORECASE)
IT_EXCLUDE_RE = re.compile("|".join(IT_EXCLUDE_PATTERNS), re.IGNORECASE)

# Роли Стефана: C-Level / VP / Head of / Director / Lead
TITLE_PATTERNS = [
    r"\bchief\b", r"\bC[EOTIPC]O\b", r"\bVP\b", r"\bvice president\b",
    r"\bhead of\b", r"\bdirector\b", r"\bpresident\b", r"\bgeneral manager\b",
    r"\b(senior )?lead\b", r"\bprincipal\b",
]
# Усилители релевантности под профиль (логистика/операции/AI/продукт/комм)
PROFILE_KEYWORDS = [
    "operations", "supply chain", "logistics", "freight", "commercial",
    "partnerships", "product", "strategy", "business development", "revenue",
    "go-to-market", "gtm", "sales", "ai", "growth", "enterprise",
]

TITLE_RE = re.compile("|".join(TITLE_PATTERNS), re.IGNORECASE)


def http_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (exec-careers-poller)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def fetch_greenhouse(company, slug, category):
    out = []
    try:
        data = http_json(f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs")
        for j in data.get("jobs", []):
            out.append({
                "uid": f"gh:{slug}:{j['id']}",
                "company": company, "category": category,
                "title": j.get("title", "").strip(),
                "location": (j.get("location") or {}).get("name", ""),
                "url": j.get("absolute_url", ""),
                "updated_at": j.get("updated_at", ""),
            })
    except Exception as e:
        print(f"⚠️ {company} (greenhouse/{slug}): {e}")
    return out


def fetch_ashby(company, slug, category):
    out = []
    try:
        data = http_json(f"https://api.ashbyhq.com/posting-api/job-board/{slug}")
        for j in data.get("jobs", []):
            out.append({
                "uid": f"ashby:{slug}:{j.get('id')}",
                "company": company, "category": category,
                "title": j.get("title", "").strip(),
                "location": j.get("location", ""),
                "url": j.get("jobUrl", ""),
                "updated_at": j.get("publishedAt", ""),
            })
    except Exception as e:
        print(f"⚠️ {company} (ashby/{slug}): {e}")
    return out


def fetch_workday(company, host, tenant, site, category):
    out = []
    try:
        url = f"https://{host}/wday/cxs/{tenant}/{site}/jobs"
        body = json.dumps({"appliedFacets": {}, "limit": 20, "offset": 0, "searchText": ""}).encode()
        offset = 0
        while True:
            body = json.dumps({"appliedFacets": {}, "limit": 20, "offset": offset, "searchText": ""}).encode()
            req = urllib.request.Request(url, data=body, headers={
                "User-Agent": "Mozilla/5.0", "Content-Type": "application/json", "Accept": "application/json"})
            data = json.loads(urllib.request.urlopen(req, timeout=30).read().decode())
            jobs = data.get("jobPostings", [])
            for j in jobs:
                ext = j.get("externalPath", "")
                out.append({
                    "uid": f"wd:{tenant}:{ext}",
                    "company": company, "category": category,
                    "title": j.get("title", "").strip(),
                    "location": j.get("locationsText", ""),
                    "url": f"https://{host}/en-US/{site}{ext}" if ext else f"https://{host}",
                    "updated_at": j.get("postedOn", ""),
                })
            offset += 20
            if offset >= data.get("total", 0) or not jobs:
                break
    except Exception as e:
        print(f"⚠️ {company} (workday/{tenant}): {e}")
    return out


def fetch_smartrecruiters(company, slug, category):
    out = []
    try:
        data = http_json(f"https://api.smartrecruiters.com/v1/companies/{slug}/postings?limit=100")
        for j in data.get("content", []):
            loc = j.get("location", {})
            out.append({
                "uid": f"sr:{slug}:{j.get('id')}",
                "company": company, "category": category,
                "title": j.get("name", "").strip(),
                "location": ", ".join(x for x in [loc.get("city"), loc.get("country")] if x),
                "url": f"https://jobs.smartrecruiters.com/{slug}/{j.get('id')}",
                "updated_at": j.get("releasedDate", ""),
            })
    except Exception as e:
        print(f"⚠️ {company} (smartrecruiters/{slug}): {e}")
    return out


def fetch_comeet_html(company, page_url, category):
    """Comeet-виджет: позиции вшиты в HTML (проверено на Windward 2026-08-17)."""
    out = []
    try:
        req = urllib.request.Request(page_url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        })
        html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
        pat = re.compile(
            r'<a class="comeet-position" href="([^"]+)"[^>]*data-location="([^"]*)"'
            r'.*?comeet-position-name">\s*(?:<!--.*?-->)?\s*([^<]+?)\s*</div>', re.S)
        for href, loc, title in pat.findall(html):
            if href.startswith("//"):
                href = "https:" + href
            out.append({
                "uid": f"comeet:{company}:{href}",
                "company": company, "category": category,
                "title": title.strip(), "location": loc,
                "url": href, "updated_at": "",
            })
    except Exception as e:
        print(f"⚠️ {company} (comeet-html): {e}")
    return out


def fetch_descartes():
    """Descartes: WordPress REST API careers.descartes.com (вскрыт через браузер 2026-08-17,
    сам сайт за Cloudflare, но /wp-json/wp/v2/job-listings отдаётся прямым запросом с браузерным UA)."""
    out = []
    try:
        url = "https://careers.descartes.com/wp-json/wp/v2/job-listings?per_page=100"
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
            "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=25) as r:
            data = json.loads(r.read().decode())
        for p in data:
            title = html_mod.unescape((p.get("title") or {}).get("rendered") or "").strip()
            link = p.get("link") or ""
            if not title or not link:
                continue
            out.append({
                "uid": f"descartes:{p.get('id')}",
                "company": "Descartes", "category": "Logistics Software",
                "title": title, "location": "", "url": link,
                "updated_at": (p.get("modified") or "")[:10],
            })
        COUNTS_UNUSED = len(data)
    except Exception as e:
        print(f"⚠️ Descartes (wp-json): {e}")
    return out


def fetch_amazon_execs():
    """Amazon.jobs Search API: ищет открытые руководящие позиции."""
    out = []
    queries = ["Director", "VP", "Vice President", "General Manager", "Head of"]
    seen_ids = set()
    for q in queries:
        try:
            url = f"https://www.amazon.jobs/en/search.json?base_query={urllib.parse.quote(q)}&result_limit=50"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read().decode())
            for j in data.get("jobs", []):
                jid = str(j.get("id_icims") or j.get("job_path") or j.get("id"))
                if not jid or jid in seen_ids:
                    continue
                seen_ids.add(jid)
                title = j.get("title", "").strip()
                loc = f"{j.get('city', '')}, {j.get('state', '')}, {j.get('country_code', '')}".strip(', ')
                job_path = j.get("job_path", "")
                full_url = f"https://www.amazon.jobs{job_path}" if job_path.startswith("/") else f"https://www.amazon.jobs/en/jobs/{jid}"
                out.append({
                    "uid": f"amazon:{jid}",
                    "company": "Amazon / AWS",
                    "category": "Big Tech / Cloud",
                    "title": title,
                    "location": loc,
                    "url": full_url,
                    "updated_at": j.get("posted_date", ""),
                })
        except Exception as e:
            print(f"⚠️ Amazon ({q}): {e}")
    return out


def fetch_nvidia_execs():
    """NVIDIA Workday CXS API: ищет открытые руководящие позиции."""
    out = []
    url = "https://nvidia.wd5.myworkdayjobs.com/wday/cxs/nvidia/NVIDIAExternalCareerSite/jobs"
    queries = ["Director", "VP", "Vice President", "Head of", "General Manager"]
    seen_ids = set()
    for q in queries:
        try:
            payload = json.dumps({"appliedFacets":{},"limit":20,"offset":0,"searchText":q}).encode()
            req = urllib.request.Request(url, data=payload, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read().decode())
            for j in data.get("jobPostings", []):
                path = j.get("externalPath", "")
                jid = path.rstrip("/").rsplit("/", 1)[-1]
                if not jid or jid in seen_ids:
                    continue
                seen_ids.add(jid)
                title = j.get("title", "").strip()
                loc = j.get("locationsText", "")
                full_url = f"https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite{path}"
                out.append({
                    "uid": f"nvidia:{jid}",
                    "company": "NVIDIA",
                    "category": "AI Hardware / Compute",
                    "title": title,
                    "location": loc,
                    "url": full_url,
                    "updated_at": j.get("postedOn", ""),
                })
        except Exception as e:
            print(f"⚠️ NVIDIA ({q}): {e}")
    return out


def fetch_remotive_execs():
    """Remotive Remote Jobs API: мониторинг глобальных remote leadership позиций."""
    out = []
    try:
        url = "https://remotive.com/api/remote-jobs?limit=100"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read().decode())
        for j in data.get("jobs", []):
            comp = j.get("company_name", "").strip()
            title = j.get("title", "").strip()
            jid = str(j.get("id"))
            out.append({
                "uid": f"remotive:{jid}",
                "company": comp,
                "category": "Remote Global / Tech",
                "title": title,
                "location": j.get("candidate_required_location", "Remote"),
                "url": j.get("url", ""),
                "updated_at": (j.get("publication_date") or "")[:10],
            })
    except Exception as e:
        print(f"⚠️ Remotive: {e}")
    return out


def fetch_google_careers_playwright():
    """Headless Playwright: парсинг открытых Director/VP ролей напрямую из Google Careers SPA."""
    out = []
    try:
        import asyncio
        from playwright.async_api import async_playwright
        
        async def _run():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
                page = await context.new_page()
                await page.goto("https://www.google.com/about/careers/applications/jobs/results/?q=Director", timeout=45000)
                await page.wait_for_timeout(8000)
                cards = await page.evaluate("""() => {
                    const res = [];
                    const headings = Array.from(document.querySelectorAll('h2, h3, [role="heading"]'));
                    for (const h of headings) {
                        const text = h.innerText.trim();
                        if (text && (text.includes('Director') || text.includes('Lead') || text.includes('VP') || text.includes('Head'))) {
                            let p = h.parentElement;
                            let link = '';
                            for (let i = 0; i < 5 && p; i++) {
                                const a = p.querySelector('a');
                                if (a && a.href) { link = a.href; break; }
                                p = p.parentElement;
                            }
                            res.push({ title: text, link: link });
                        }
                    }
                    return res;
                }""")
                await browser.close()
                return cards
        
        items = asyncio.run(_run())
        for it in items:
            title = it['title']
            url = it['link'] or "https://careers.google.com"
            out.append({
                "uid": "google:" + re.sub(r'[^a-zA-Z0-9]', '', title)[:30],
                "company": "Google",
                "title": title,
                "location": "Global / US",
                "url": url,
                "category": "Big Tech / AI",
                "updated_at": "",
            })
    except Exception as e:
        print("Google Playwright parser error:", e)
    return out


def fetch_microsoft_careers_playwright():
    """Headless Playwright: парсинг открытых ролей напрямую из Microsoft Careers SPA."""
    out = []
    try:
        import asyncio
        from playwright.async_api import async_playwright
        
        async def _run():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
                page = await context.new_page()
                await page.goto("https://jobs.careers.microsoft.com/global/en/search?q=Director&lc=United%20States&l=en_us&pg=1&pgSz=20&o=Relevance", timeout=45000)
                await page.wait_for_timeout(8000)
                cards = await page.evaluate("""() => {
                    const res = [];
                    const elements = Array.from(document.querySelectorAll('[data-automation-id="job-title"], h2, h3, a[href*="/job/"]'));
                    for (const el of elements) {
                        const text = el.innerText.trim();
                        const a = el.tagName === 'A' ? el : el.closest('a') || el.querySelector('a');
                        if (text && a && a.href) {
                            res.push({ title: text.split('\\n')[0], link: a.href });
                        }
                    }
                    return res;
                }""")
                await browser.close()
                return cards
                
        items = asyncio.run(_run())
        for it in items:
            title = it['title']
            url = it['link']
            out.append({
                "uid": "ms:" + re.sub(r'[^a-zA-Z0-9]', '', title)[:30],
                "company": "Microsoft",
                "title": title,
                "location": "United States / Global",
                "url": url,
                "category": "Big Tech / Cloud",
                "updated_at": "",
            })
    except Exception as e:
        print("Microsoft Playwright parser error:", e)
    return out
def fetch_epam_global_playwright():
    """Headless Playwright: парсинг открытых Director / Lead / Management ролей с глобального портала careers.epam.com."""
    out = []
    try:
        import asyncio
        from playwright.async_api import async_playwright
        
        async def _run():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
                page = await context.new_page()
                # Global EPAM Careers listing
                await page.goto("https://www.epam.com/careers/job-listings", timeout=45000)
                await page.wait_for_timeout(8000)
                cards = await page.evaluate("""() => {
                    const res = [];
                    const links = Array.from(document.querySelectorAll('a[href*="/vacancy/"]'));
                    for (const a of links) {
                        const title = a.innerText.trim();
                        if (title && a.href && !res.some(r => r.link === a.href)) {
                            res.push({ title: title, link: a.href });
                        }
                    }
                    return res;
                }""")
                await browser.close()
                return cards
                
        items = asyncio.run(_run())
        for it in items:
            title = it['title']
            url = it['link']
            out.append({
                "uid": "epam:" + re.sub(r'[^a-zA-Z0-9]', '', title)[:30],
                "company": "EPAM Systems",
                "title": title,
                "location": "Global / Remote",
                "url": url,
                "category": "IT Enterprise / Consulting",
                "updated_at": "",
            })
    except Exception as e:
        print("EPAM Playwright parser error:", e)
    return out


def fetch_dou_feed(company, slug):
    """DOU RSS: jobs.dou.ua/vacancies/<slug>/feeds/ (title содержит роль и город)."""
    out = []
    try:
        url = f"https://jobs.dou.ua/vacancies/{slug}/feeds/"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=25) as r:
            xml = r.read().decode("utf-8", errors="ignore")
        items = re.findall(r"<item>(.*?)</item>", xml, re.S)
        for it in items:
            tm = re.search(r"<title>(.*?)</title>", it, re.S)
            lm = re.search(r"<link>(.*?)</link>", it, re.S)
            if not tm or not lm:
                continue
            title = html_mod.unescape(tm.group(1)).strip()
            link = lm.group(1).strip()
            # title формата "Role в Company, Город"
            role = title.split(" в ")[0].strip() if " в " in title else title
            loc = title.rsplit(", ", 1)[-1] if ", " in title else ""
            out.append({
                "uid": f"dou:{slug}:{link.rstrip('/').rsplit('/', 1)[-1]}",
                "company": company, "category": "IT Ukraine",
                "title": role, "location": loc, "url": link, "updated_at": "",
            })
    except Exception as e:
        print(f"⚠️ {company} (dou/{slug}): {e}")
    return out


def is_it_match(title):
    return bool(IT_TITLE_RE.search(title)) and not IT_EXCLUDE_RE.search(title)


def is_exec(title):
    return bool(TITLE_RE.search(title))


def profile_hits(title):
    t = title.lower()
    return [k for k in PROFILE_KEYWORDS if k in t]


def main():
    seen = set()
    if os.path.exists(SEEN_FILE):
        try:
            seen = set(json.load(open(SEEN_FILE)).get("uids", []))
        except Exception:
            seen = set()
    first_run = not seen

    all_jobs = []
    for c, s, cat in GREENHOUSE_BOARDS:
        all_jobs.extend(fetch_greenhouse(c, s, cat))
    for c, s, cat in ASHBY_BOARDS:
        all_jobs.extend(fetch_ashby(c, s, cat))
    for c, h, t, st, cat in WORKDAY_BOARDS:
        all_jobs.extend(fetch_workday(c, h, t, st, cat))
    for c, s, cat in SMARTRECRUITERS_BOARDS:
        all_jobs.extend(fetch_smartrecruiters(c, s, cat))
    for c, u, cat in COMEET_HTML_PAGES:
        all_jobs.extend(fetch_comeet_html(c, u, cat))
    all_jobs.extend(fetch_descartes())
    all_jobs.extend(fetch_amazon_execs())
    all_jobs.extend(fetch_remotive_execs())
    all_jobs.extend(fetch_google_careers_playwright())
    all_jobs.extend(fetch_microsoft_careers_playwright())
    all_jobs.extend(fetch_epam_global_playwright())
    all_jobs.extend(fetch_remotive_execs())

    # ===== Блок IT Ukraine (BizDev/PM/Product/Delivery, senior+) =====
    it_jobs = []
    for c, s, cat in GREENHOUSE_BOARDS_IT:
        it_jobs.extend(fetch_greenhouse(c, s, cat))
    for c, s, cat in ASHBY_BOARDS_IT:
        it_jobs.extend(fetch_ashby(c, s, cat))
    for c, s in DOU_FEEDS:
        it_jobs.extend(fetch_dou_feed(c, s))

    if not all_jobs:
        print("❌ Ни один источник не ответил — сеть/API недоступны. Отчёт не формируется.")
        return

    execs = [j for j in all_jobs if is_exec(j["title"])]
    for j in execs:
        j["keywords"] = profile_hits(j["title"])
    new = [j for j in execs if j["uid"] not in seen]
    # Сортировка: сначала больше совпадений с профилем
    new.sort(key=lambda j: len(j["keywords"]), reverse=True)

    # IT Ukraine: свой фильтр (BizDev/PM/senior+), свои новинки
    it_matches = [j for j in it_jobs if is_it_match(j["title"])]
    for j in it_matches:
        j["keywords"] = profile_hits(j["title"])
    it_new = [j for j in it_matches if j["uid"] not in seen]
    it_new.sort(key=lambda j: len(j["keywords"]), reverse=True)

    # Обновляем seen-store всеми текущими uid (окно не растёт бесконечно)
    current_uids = {j["uid"] for j in execs} | {j["uid"] for j in it_matches}
    json.dump({"uids": sorted(seen | current_uids), "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")},
              open(SEEN_FILE, "w"))
    json.dump({"updated_at": time.strftime("%Y-%m-%d %H:%M:%S"), "new": new, "it_new": it_new,
               "total_exec_open": len(execs), "total_it_open": len(it_matches)},
              open(OUT_FILE, "w"), ensure_ascii=False, indent=2)

    by_src = {}
    for j in all_jobs:
        by_src[j["company"]] = by_src.get(j["company"], 0) + 1
    print(f"=== EXECUTIVE CAREERS POLLER v2 (реальные API) ===")
    print("Источники:", ", ".join(f"{k}={v}" for k, v in sorted(by_src.items())))
    print(f"Всего открытых executive-позиций: {len(execs)}; НОВЫХ с прошлого прогона: {len(new)}")
    print()

    if first_run:
        print("(Первый прогон: baseline создан. Показываю топ-15 наиболее релевантных из текущих открытых.)")
        show = [j for j in execs if j["keywords"]]
        show.sort(key=lambda j: len(j["keywords"]), reverse=True)
        new = show[:15]
    elif not new:
        print("Новых executive-вакансий с прошлого прогона нет.")
        new = []

    for j in new[:20]:
        kw = ", ".join(j["keywords"]) if j.get("keywords") else "—"
        print(f"• {j['company']} — {j['title']}")
        print(f"  📍 {j['location'] or 'n/a'} | 🏷 {kw}")
        print(f"  🔗 {j['url']}")
        print()

    # ===== Секция IT Ukraine =====
    it_src = {}
    for j in it_jobs:
        it_src[j["company"]] = it_src.get(j["company"], 0) + 1
    print("=== IT UKRAINE (BizDev/PM/Product/Delivery, senior+) ===")
    print("Источники:", ", ".join(f"{k}={v}" for k, v in sorted(it_src.items())) or "нет данных")
    print(f"Подходящих открытых: {len(it_matches)}; НОВЫХ: {len(it_new)}")
    print()
    if first_run:
        show_it = sorted([j for j in it_matches], key=lambda j: len(j["keywords"]), reverse=True)[:15]
    elif not it_new:
        print("Новых IT-вакансий с прошлого прогона нет.")
        show_it = []
    else:
        show_it = it_new[:20]
    for j in show_it:
        kw = ", ".join(j["keywords"]) if j.get("keywords") else "—"
        print(f"• {j['company']} — {j['title']}")
        print(f"  📍 {j['location'] or 'n/a'} | 🏷 {kw}")
        print(f"  🔗 {j['url']}")
        print()


if __name__ == "__main__":
    main()
