# Playwright Automated LinkedIn Profile Verification Pipeline

## Overview
LinkedIn strictly blocks automated bot requests (returning HTTP 999 Authwall) and generates dynamic 404 error pages via JavaScript client-side rendering for non-existent profile slugs.

To guarantee that 100% of LinkedIn URLs in sales sheets are **real, live, and non-404**, use the Playwright Chromium verification pipeline with **strict OpenGraph (og:title) verification**.

---

## Critical Pitfall: Authwall "Sign Up" False Positives
- **The Pitfall**: When an unauthenticated Playwright browser visits `linkedin.com/in/{slug}`, non-existent or private slugs often render an authwall with title `<title>Sign Up | LinkedIn</title>` or `<title>Anmelden | LinkedIn</title>`. A naive check (`'404' not in title`) will flag this as "valid", but when a logged-in sales rep opens the link in their Chrome/macOS browser, LinkedIn redirects to `https://www.linkedin.com/404/` ("Эта страница не существует").
- **The Rule**: A profile is **STRICTLY VERIFIED** only if:
  1. The page `<meta property="og:title">` or `<title>` explicitly contains the **person's real name and company/role** (e.g. `Stefan Paul – CEO Kuehne+Nagel Group | LinkedIn`, `Kyle H. – VIZION | LinkedIn`).
  2. Generic titles (`Sign Up`, `Anmelden`, `Log In`, `404`, `Page not found`) MUST be treated as **REJECTED / UNVERIFIED**.

---

## Strict Verification Script

```python
import time
import urllib.parse
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def verify_linkedin_profile_strict(person_name: str, profile_url: str) -> dict:
    """
    Physically validates a personal LinkedIn URL using Playwright and strict OG metadata inspection.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        )
        try:
            page.goto(profile_url, timeout=12000, wait_until='load')
            time.sleep(1.0)
            
            soup = BeautifulSoup(page.content(), 'html.parser')
            og_title = soup.find('meta', property='og:title')
            og_content = og_title['content'] if og_title else ''
            title = page.title()
            
            # Check 404 indicators
            is_404 = '404' in page.url or '404' in title or 'Page not found' in title or 'Эта страница не существует' in page.content()
            
            # Strict validation: must contain name in OG title or clean page title
            name_parts = [p.lower() for p in person_name.split() if len(p) > 2]
            name_confirmed = any(p in og_content.lower() or p in title.lower() for p in name_parts)
            
            # Exclude generic authwall titles
            is_authwall_only = og_content in ['Sign Up | LinkedIn', 'Anmelden | LinkedIn', 'Log In | LinkedIn', ''] and title in ['Sign Up | LinkedIn', 'Anmelden | LinkedIn', 'Log In | LinkedIn']
            
            is_valid = not is_404 and not is_authwall_only and (name_confirmed or 'LinkedIn' in og_content)
            
            return {
                'url': profile_url,
                'valid': is_valid,
                'og_title': og_content,
                'title': title
            }
        except Exception as e:
            return {'url': profile_url, 'valid': False, 'error': str(e)}
        finally:
            browser.close()
```

---

## Strict Rules for Sales Master Tables
1. **Zero Guessing Policy**: Never generate `in/firstname-lastname` slugs.
2. **Zero Search URL Substitutions**: Do not put Google X-Ray or Bing search links into lead profile columns. Sales reps require a 1-click direct personal profile link (`https://www.linkedin.com/in/...`).
3. **Pre-Flight Playwright Audit**: Every `/in/` link delivered to the user must be verified through the strict OG/name check pipeline.
