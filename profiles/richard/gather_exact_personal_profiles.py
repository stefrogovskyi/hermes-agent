import json
import time
import re
import urllib.parse
from playwright.sync_api import sync_playwright
import gspread

gc = gspread.service_account(filename='/opt/hermes/profiles/richard/google_service_account.json')
sh = gc.open_by_key('1ceJzlfTCQIvJeMoBZfIhxesFxPM9mbV_iAMe6qXEIMo')
ws_fwd = sh.worksheet('🎯 Forwarders & NVOCC')
fwd_rows = ws_fwd.get_all_values()[1:]

verified_leads = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    )
    
    for idx, r in enumerate(fwd_rows[:30], 1):
        comp = r[3].strip()
        web = r[10].strip()
        contact_hint = r[7].strip()
        
        # 1 query per company
        q = f'site:linkedin.com/in "{comp}" logistics'
        search_url = f"https://search.brave.com/search?q={urllib.parse.quote(q)}"
        
        found = None
        try:
            page.goto(search_url, timeout=7000)
            links = page.eval_on_selector_all('a', 'els => els.map(e => ({href: e.href, text: e.innerText}))')
            for item in links:
                href = item['href']
                text = item['text']
                if 'linkedin.com/in/' in href and 'translate' not in href and 'dir/' not in href:
                    clean = href.split('?')[0].rstrip('/')
                    clean_text = text.replace(' | LinkedIn', '').replace(' - LinkedIn', '').strip()
                    if len(clean_text) > 4 and 'LinkedIn' not in clean_text and 'Sign In' not in clean_text:
                        parts = clean_text.split(' - ')
                        dm_name = parts[0].strip()
                        dm_title = parts[1].strip() if len(parts) > 1 else 'Logistics & Supply Chain Leader'
                        found = {
                            'comp': comp,
                            'web': web,
                            'dm_name': dm_name,
                            'dm_title': dm_title,
                            'profile_url': clean
                        }
                        print(f"[{idx}] FOUND: {dm_name} ({comp}) -> {clean}")
                        break
        except Exception as e:
            pass
            
        if found:
            verified_leads.append(found)
        time.sleep(0.3)
        
    browser.close()

with open('/opt/hermes/profiles/richard/verified_handpicked_dms.json', 'w', encoding='utf-8') as f:
    json.dump(verified_leads, f, indent=2, ensure_ascii=False)

print(f"\nSaved {len(verified_leads)} live profiles to disk!")
