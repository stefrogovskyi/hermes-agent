import urllib.request
import urllib.parse
import re
import json

def enrich_business_email(name, city, phone=None):
    clean_phone_str = re.sub(r'[^\d]', '', str(phone or ''))[-10:]
    queries = [
        f'"{name}" "{city}" email',
        f'"{name}" {clean_phone_str} "@gmail.com" OR "@yahoo.com" OR "@outlook.com"' if clean_phone_str else None,
        f'"{name}" "sunbiz" OR "opencorporates" OR "yelp" email'
    ]
    
    found_emails = set()
    for q in queries:
        if not q: continue
        try:
            url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(q)}"
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
            )
            with urllib.request.urlopen(req, timeout=7) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
                emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', html)
                for em in emails:
                    em_lower = em.lower()
                    if not any(bad in em_lower for bad in ['duckduckgo', 'example', 'domain', '.png', '.jpg', 'wixpress', 'sentry', 'rating', 'schema.org', 'support@', 'info@yelp', 'abuse@']):
                        found_emails.add(em)
        except Exception:
            pass
            
    return list(found_emails)[0] if found_emails else ""
