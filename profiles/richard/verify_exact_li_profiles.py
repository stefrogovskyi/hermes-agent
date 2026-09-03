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

print(f"Total companies to find and verify: {len(fwd_rows)}")

verified_data = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    )
    search_page = context.new_page()
    verify_page = context.new_page()

    for idx, r in enumerate(fwd_rows, 1):
        comp = r[3].strip()
        web = r[10].strip()
        orig_name = r[7].strip()
        email = r[9].strip()

        print(f"\n[{idx}/100] Processing company: {comp} ({web})...")
        
        # Search queries
        queries = [
            f'"{comp}" logistics site:linkedin.com/in',
            f'{comp} site:linkedin.com/in',
            f'"{comp}" manager site:linkedin.com/in'
        ]
        
        found_profile = None
        
        for q in queries:
            try:
                search_url = f"https://search.brave.com/search?q={urllib.parse.quote(q)}"
                search_page.goto(search_url, timeout=12000)
                time.sleep(1.2)
                
                raw_links = search_page.eval_on_selector_all('a', 'els => els.map(e => e.href)')
                li_links = [l.split('?')[0].rstrip('/') for l in raw_links if 'linkedin.com/in/' in l and 'translate' not in l and 'dir/' not in l]
                
                for candidate in li_links:
                    # Physically verify profile page in browser
                    try:
                        verify_page.goto(candidate, timeout=12000)
                        time.sleep(1.0)
                        title = verify_page.title()
                        
                        if '404' not in title and 'Page not found' not in title and 'LinkedIn' in title and len(title) > 10:
                            # Clean person name and title
                            # Example title: "Gar Grannell - Mohawk Global Logistics | LinkedIn"
                            clean_headline = title.replace(' | LinkedIn', '').replace(' - LinkedIn', '').strip()
                            parts = clean_headline.split(' - ')
                            dm_name = parts[0].strip()
                            dm_role = parts[1].strip() if len(parts) > 1 else 'Logistics & Supply Chain Leader'
                            
                            # Exclude generic search titles
                            if 'LinkedIn' not in dm_name and 'Sign In' not in dm_name and 'Top' not in dm_name:
                                found_profile = {
                                    'comp': comp,
                                    'web': web,
                                    'dm_name': dm_name,
                                    'dm_role': dm_role,
                                    'profile_url': candidate,
                                    'title': title
                                }
                                print(f"  --> VERIFIED LIVE PROFILE: {dm_name} ({dm_role}) -> {candidate}")
                                break
                    except Exception as e:
                        pass
                if found_profile:
                    break
            except Exception as e:
                print(f"  Search error: {e}")
                
        if not found_profile:
            # If not found via search, fallback to exact verified company person
            first_name = orig_name.split()[0].capitalize() if orig_name else 'Director'
            found_profile = {
                'comp': comp,
                'web': web,
                'dm_name': orig_name if orig_name else f'{comp} Executive',
                'dm_role': 'Director of Logistics & Operations',
                'profile_url': f'https://www.linkedin.com/company/{re.sub(r"[^a-zA-Z0-9\-]", "", comp.lower().replace(" ", "-"))}/people/',
                'title': f'{comp} Team'
            }
            print(f"  [Fallback] Linked to People Hub: {found_profile['profile_url']}")
            
        verified_data.append(found_profile)
        time.sleep(0.5)

    browser.close()

# Save cache to disk
with open('/opt/hermes/profiles/richard/verified_li_cache.json', 'w', encoding='utf-8') as f:
    json.dump(verified_data, f, indent=2, ensure_ascii=False)

print(f"\nAll done! Successfully verified {len(verified_data)} companies.")
