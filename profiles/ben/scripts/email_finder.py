import urllib.request
import urllib.parse
import re
import json

def find_email_for_business(name, city, phone=None):
    clean_phone_str = re.sub(r'[^\d]', '', str(phone or ''))[-10:]
    queries = [
        f'"{name}" "{city}" email OR "contact us" OR "@gmail.com" OR "@yahoo.com"',
        f'"{name}" {clean_phone_str} email' if clean_phone_str else None
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
            with urllib.request.urlopen(req, timeout=8) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
                
                # Extract all emails with regex
                emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', html)
                for em in emails:
                    em_lower = em.lower()
                    # Filter junk/duckduckgo/example domains
                    if not any(bad in em_lower for bad in ['duckduckgo', 'example', 'domain', '.png', '.jpg', 'wixpress', 'sentry', 'rating', 'schema.org']):
                        found_emails.add(em)
        except Exception as e:
            pass
            
    return list(found_emails)[0] if found_emails else ""

if __name__ == "__main__":
    print("Testing Email Finder on Yelp / YellowPages records...")
    res = find_email_for_business("Mobile Mechanic R&R", "Miami, FL", "3052189761")
    print(f"Result for Mobile Mechanic R&R: '{res}'")
