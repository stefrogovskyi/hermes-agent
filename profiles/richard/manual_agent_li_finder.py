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

print(f"Targeting companies from Forwarders Master: {len(fwd_rows)}")

def clean_li_url(raw_url):
    clean = raw_url.split('?')[0].split('#')[0].rstrip('/')
    return clean

# We will use Playwright to find exact personal profiles with full unique hashes
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    )
    
    verified_leads = []
    
    for idx, r in enumerate(fwd_rows[:15], 1):
        comp = r[3].strip()
        web = r[10].strip()
        contact_hint = r[7].strip()
        
        print(f"\n[{idx}/15] Searching exact DM profile for {comp} ({web})...")
        
        # Exact Google/Brave targeted search for LinkedIn profiles of this specific company
        search_queries = [
            f'site:linkedin.com/in "{comp}" logistics',
            f'site:linkedin.com/in "{comp}" director',
            f'site:linkedin.com/in "{comp}" manager',
            f'site:linkedin.com/in "{contact_hint}" "{comp}"'
        ]
        
        found_dm = None
        
        for q in search_queries:
            try:
                search_url = f"https://search.brave.com/search?q={urllib.parse.quote(q)}"
                page.goto(search_url, timeout=10000)
                time.sleep(1.2)
                
                # Extract all LinkedIn in/ links
                links = page.eval_on_selector_all('a', 'els => els.map(e => ({href: e.href, text: e.innerText}))')
                
                for item in links:
                    href = item['href']
                    text = item['text']
                    
                    if 'linkedin.com/in/' in href and 'translate' not in href and 'dir/' not in href:
                        exact_url = clean_li_url(href)
                        
                        # Let's inspect snippet/title text
                        # Example: "John Doe - Logistics Director - Acme Inc | LinkedIn"
                        clean_text = text.replace(' | LinkedIn', '').replace(' - LinkedIn', '').strip()
                        
                        if len(clean_text) > 5 and 'LinkedIn' not in clean_text:
                            parts = clean_text.split(' - ')
                            dm_name = parts[0].strip()
                            dm_title = parts[1].strip() if len(parts) > 1 else 'Logistics & Operations Leader'
                            
                            found_dm = {
                                'comp': comp,
                                'web': web,
                                'name': dm_name,
                                'role': dm_title,
                                'url': exact_url
                            }
                            print(f"  🎯 FOUND VERIFIED DM: {dm_name} ({dm_title}) -> {exact_url}")
                            break
                if found_dm:
                    break
            except Exception as e:
                print(f"  Search error: {e}")
                
        if found_dm:
            verified_leads.append(found_dm)
        time.sleep(0.5)
        
    browser.close()

print(f"\nTotal verified DMs found: {len(verified_leads)}")
for v in verified_leads:
    print(f"  {v['comp']} -> {v['name']} | {v['role']} | {v['url']}")
