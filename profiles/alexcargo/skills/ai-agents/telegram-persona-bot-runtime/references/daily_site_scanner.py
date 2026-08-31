# -*- coding: utf-8 -*-
"""
daily_site_scanner.py — keep a Telegram persona bot's KB fresh by scanning product sites.
Stdlib-only. Run via cron (every 3 days per owner pref): `python daily_site_scanner.py`.
Use --dry-run to eyeball LLM output before writing.

KEY LESSONS (from live runs):
- Product FACTS clients ask about (price/tier/rate/limit) MUST go to Agents.md (agents_md_add),
  NOT only to the news log — the bot reads Agents.md at runtime, not the news file.
- Regex-extract prices from the page and pass as a hint so the classifier never drops a number.
- Forbid fabricated dates in the LLM output; the news file header stamps the real scan date.
- To re-seed after a refactor, delete memory/site_snapshots.json (next run treats all as changed).
"""
import os, re, sys, time, json, urllib.request, urllib.error

# load .env.local (NOUS_API_KEY etc.) like the bot does
_here = os.path.dirname(os.path.abspath(__file__))
for _envf in (".env", ".env.local"):
    _p = os.path.join(_here, _envf)
    if os.path.exists(_p):
        for _line in open(_p, encoding="utf-8"):
            _line = _line.strip()
            if not _line or _line.startswith("#") or "=" not in _line:
                continue
            _k, _v = _line.split("=", 1)
            _k, _v = _k.strip(), _v.strip().strip('"').strip("'")
            if _k and _k not in os.environ:
                os.environ[_k] = _v

SITES = {
    "navo24": "https://navo24.com/",
    "trackingmcp": "https://trackingmcp.com/",
    "schedulesmcp": "https://schedulesmcp.com/",
    "loadingmcp": "https://loadingmcp.com/",
    "freightratesmcp": "https://freightratesmcp.com/",
}
MEM_DIR = os.path.join(_here, "memory")
SNAP_FILE = os.path.join(MEM_DIR, "site_snapshots.json")
NEWS_FILE = os.path.join(MEM_DIR, "product_news.md")
AGENTS_FILE = os.path.join(_here, "Agents.md")
NOUS_BASE = os.environ.get("NOUS_BASE_URL", "https://inference-api.nousresearch.com/v1").rstrip("/")
NOUS_URL = NOUS_BASE + "/chat/completions"
MODEL = os.environ.get("RICHARD_MODEL", "tencent/hy3:free")
UA = {"User-Agent": "Mozilla/5.0 (compatible; RichardScanner/1.0)"}


def _http_get(url, timeout=40):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="ignore")


def _strip_html(html):
    html = re.sub(r"(?is)<(script|style).*?</\1>", " ", html)
    html = re.sub(r"(?is)<!--.*?-->", " ", html)
    text = re.sub(r"(?s)<[^>]+>", " ", html)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"&[a-z]+;", " ", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)
    return text.strip()


def _hash(s):
    import hashlib
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


def load_snaps():
    if os.path.exists(SNAP_FILE):
        try:
            return json.load(open(SNAP_FILE, encoding="utf-8"))
        except Exception:
            pass
    return {}


def save_snaps(snaps):
    os.makedirs(MEM_DIR, exist_ok=True)
    json.dump(snaps, open(SNAP_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def extract_prices(text):
    found = []
    for m in re.finditer(r"(?i)(?:€|EUR|USD|\$|евро|usd)?\s*(\d{2,4})\s*(?:евро|eur|usd|\$|/mo|per month|в месяц|мес)?", text):
        token = m.group(0).strip()
        if re.search(r"(19|20)\d{2}", token) or "%" in token:
            continue
        if token and token not in found:
            found.append(token)
    return found[:8]


def llm_analyze(site, old_text, new_text):
    sys_p = (
        "You are Richard Marlowe's knowledge curator. A Navo website was scanned. "
        "Extract product knowledge to keep Richard competent with clients. Output STRICT JSON only:\n"
        "{\"changed\": true/false, "
        "\"summary\": \"1-3 sentences in Russian: what is notable on this Navo site\", "
        "\"agents_md_add\": \"ALL concrete product facts to append to Agents.md: prices, rates, tiers, carrier counts, reliability %, free-tier limits, integrations, features. Russian/English, 1-5 sentences. Include any EUR/USD amounts found. If none new, empty.\", "
        "\"news_add\": \"short update line for the news log in Russian (1-2 sentences, NO date), or empty\"}\n"
        "Focus: prices, tiers, rates, carrier counts, reliability, FAQ, integrations, free-tier limits. "
        "If truly nothing notable, changed=false, all empty.\n"
        "CRITICAL: do NOT invent or include any dates in news_add — the system stamps the real scan date. "
        "ALWAYS surface prices/tiers you find into agents_md_add."
    )
    prices = extract_prices(new_text)
    price_hint = ("\n[Prices/tiers detected on page: %s]" % ", ".join(prices)) if prices else ""
    user = "SITE: %s%s\n\n--- PAGE TEXT (first 3500 chars) ---\n%s" % (site, price_hint, new_text[:3500])
    payload = {"model": MODEL, "messages": [
        {"role": "system", "content": sys_p},
        {"role": "user", "content": user}]}
    headers = {"Authorization": "Bearer %s" % os.environ["NOUS_API_KEY"], "Content-Type": "application/json"}
    req = urllib.request.Request(NOUS_URL, data=json.dumps(payload).encode(), headers=headers, method="POST")
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                raw = json.loads(r.read().decode("utf-8"))["choices"][0]["message"].get("content", "")
            m = re.search(r"\{.*\}", raw, re.S)
            if m:
                return json.loads(m.group(0))
        except Exception as e:
            print("[scan] llm err %s" % e)
            time.sleep(2)
    return {"changed": False, "summary": "", "agents_md_add": "", "news_add": ""}


def append_news(line):
    os.makedirs(MEM_DIR, exist_ok=True)
    stamp = time.strftime("%Y-%m-%d")
    block = "\n- **%s**: %s" % (stamp, line.strip())
    cur = ""
    if os.path.exists(NEWS_FILE):
        cur = open(NEWS_FILE, encoding="utf-8").read()
    if "## 🆕 Product & Site Updates" not in cur:
        cur = cur.rstrip() + "\n\n## 🆕 Product & Site Updates (auto from daily scan)\n"
    with open(NEWS_FILE, "w", encoding="utf-8") as f:
        f.write(cur.rstrip() + block + "\n")


def append_agents(text):
    if not text or not os.path.exists(AGENTS_FILE):
        return
    cur = open(AGENTS_FILE, encoding="utf-8").read()
    stamp = time.strftime("%Y-%m-%d")
    block = "\n\n## 🧠 Auto-update from scan (%s)\n%s\n" % (stamp, text.strip())
    with open(AGENTS_FILE, "w", encoding="utf-8") as f:
        f.write(cur.rstrip() + block)


def main(dry_run=False):
    print("[scan] start %s%s" % (time.strftime("%Y-%m-%d %H:%M"), " (DRY RUN)" if dry_run else ""))
    snaps = load_snaps()
    updates = []
    for name, url in SITES.items():
        try:
            html = _http_get(url)
            text = _strip_html(html)
            h = _hash(text)
            old = snaps.get(name, {})
            if old.get("hash") == h:
                print("[scan] %s unchanged" % name)
                continue
            print("[scan] %s CHANGED" % name)
            res = llm_analyze(name, old.get("text", ""), text)
            if res.get("changed") and (res.get("agents_md_add") or res.get("news_add")):
                if not dry_run:
                    if res.get("agents_md_add"):
                        append_agents(res["agents_md_add"])
                    if res.get("news_add"):
                        append_news(res["news_add"])
                else:
                    print("   [dry] agents_md_add: %s" % res.get("agents_md_add", "")[:80])
                    print("   [dry] news_add: %s" % res.get("news_add", "")[:80])
                updates.append("%s: %s" % (name, res.get("summary", "")))
            snaps[name] = {"hash": h, "ts": time.strftime("%Y-%m-%d"), "text": text[:2000]}
        except Exception as e:
            print("[scan] %s error: %s" % (name, e))
    if not dry_run:
        save_snaps(snaps)
    if updates:
        print("[scan] %d site(s) updated:" % len(updates))
        for u in updates:
            print("  - %s" % u)
    else:
        print("[scan] no material changes")
    print("[scan] done")


if __name__ == "__main__":
    if not os.environ.get("NOUS_API_KEY") or os.environ.get("NOUS_API_KEY", "").startswith("stub-"):
        print("[scan] NOUS_API_KEY missing/stub — cannot analyze. Exit.")
        sys.exit(1)
    DRY = "--dry-run" in sys.argv
    main(dry_run=DRY)
