---
name: browser-task-automation
description: Automate Cloudflare/OAuth web tasks via cloud browser.
---

# Browser Task Automation (cloud browser / Browserbase)

Use this when the user asks you to operate a website through the browser tooling: log in, add items to a cart, fill a form, place an order, etc. — especially sites behind Cloudflare or with OAuth login.

## When to use
- "Order X from site Y", "add these to cart", "fill in this form", "log in and check".
- The site shows "Just a moment..." / Cloudflare challenge, or uses `auth.<domain>` OAuth.
- Login is OTP-SMS only and the user must relay the code.

## Core workflow
1. `browser_navigate` to the site (this first hit usually triggers a CF challenge).
2. Wait 10–18s, then `browser_snapshot` to confirm the page rendered.
3. Click through login. If OTP-SMS: click, ask user for the code, type it, click submit.
4. **Immediately after login, do ALL task actions in one continuous SPA session** (see pitfall below).
5. Stop before any final financial confirmation; report the cart/state to the user.

## 🔴 CRITICAL pitfall — session reset on browser_navigate
On Cloudflare-protected OAuth SPAs (silpo.ua is the canonical example), **every `browser_navigate` to a URL reloads the page and creates a NEW browser session_id**. The OAuth token (which lives only ~minutes) is bound to the old session, so the silent-renew iframe fails with `error=login_required` and you are logged out. Symptom: after a navigate, the header shows "Увійти" again, or snapshots return `about:blank` / "Blocked: page URL targets a private or internal address".

**Rule: after a successful login, NEVER call `browser_navigate` again.** Navigate only by SPA clicks:
- Menu buttons, category links, "Додати у кошик" — all are in-page clicks that keep the SPA session alive.
- If you must reach a known category, click "Всі товари" → the category link (do not paste a category URL).
- The token still expires in minutes, so do the whole task in one tight burst right after login. Do not insert long waits (e.g. waiting for an SMS) mid-task if you can avoid it.

## Technique — parse the snapshot, don't rely on the visual view
The accessibility snapshot is saved to a file (path printed in the snapshot result, e.g. `AppData/Local/hermes/cache/web/browser-snapshot-*.txt`). Grep it from the terminal to extract structured data instead of reading the visual page:
- Product names, weights, old/new prices, discount %.
- The `ref=` of each "Додати у кошик" button (so you can click it by ref without seeing it).
Use `scripts/extract_discounts.sh` to pull only products above a discount threshold (see references/ for the format that worked on silpo.ua).

## Technique — reverse-engineer hidden API endpoints via browser_console hooks
When you want to know what endpoint the SPA calls (login, cart, OTP verify, etc.) WITHOUT downloading CF-protected JS bundles (curl gets 0 bytes), use `browser_console` to install a network hook **while on the live page** — it inherits the page's cookies/origin, so Cloudflare doesn't block it.
1. Install an XHR+fetch capturer:
   ```js
   window.__cap = [];
   const oh = XMLHttpRequest.prototype.open;
   XMLHttpRequest.prototype.open = function(m,u,...a){ window.__cap.push(m+' '+u); return oh.call(this,m,u,...a); };
   const of = window.fetch;
   window.fetch = function(u,...a){ try{ window.__cap.push((a[0]&&a[0].method||'GET')+' '+ (typeof u==='string'?u:u.url)); }catch(e){} return of.apply(this,arguments); };
   ```
2. Perform the UI action (e.g. click "Увійти").
3. Read the captured URLs: `JSON.stringify(window.__cap.slice(-10))`.
This caught `POST https://auth.silpo.ua/api/v2/Login/ByPhone?returnUrl=...` on silpo.ua. Useful for understanding the flow; but see the pitfall below — you usually still can't replay it with curl.

## 🔴 Pitfall — the OIDC access_token lives ONLY in Angular app memory
You cannot extract a usable `Authorization: Bearer <token>` to drive the site via `curl`/terminal after login. On silpo.ua the token is NOT in `document.cookie`, `localStorage`, or `sessionStorage` (checked all three — empty of tokens). The Angular SPA holds it in RAM and attaches it to its own `fetch` calls, which a `browser_console` hook installed from outside does not intercept. **Therefore the entire post-login task must run inside the browser via SPA clicks — a hybrid "login in browser, then curl the API" phase is not achievable on this architecture.** Don't burn rounds trying to harvest the token; just stay in-browser.

## 🔴 Pitfall — signin-callback stuck on empty page is a hard dead-end
Sometimes, after a successful OTP code exchange, the URL reaches `.../signin-callback-angular.html?code=...` but the SPA never renders the home page (snapshot stays `element_count: 0`, `(empty page)`). The OAuth code WAS issued, but Angular's bootstrap didn't complete. **There is no recovery that preserves the session**: any `browser_navigate` (even to site root) creates a new session id → Cloudflare re-challenge → token death. Do NOT loop on snapshots hoping it renders. Options: retry the full OAuth flow once more (fresh OTP), or hand the task to the user's own stable browser session.

## 🟢 BEST approach — attach to the user's OWN logged-in Chrome via CDP (bypasses Cloudflare entirely)
When the user is already logged into the site in their visible desktop Chrome, driving THAT browser is far more reliable than a fresh cloud/headless session: the persistent profile keeps auth cookies, so Cloudflare does NOT challenge and login is already done. Setup:
1. Relaunch the user's visible Chrome with a CDP port on the SAME profile (do this via a `.ps1` so it's clean on Windows):
   - Kill only the visible-profile Chrome (match cmdline on `Google\Chrome\User Data`, do NOT touch other CDP profiles).
   - Relaunch: `chrome.exe --remote-debugging-port=9223 --user-data-dir="C:\Users\<user>\AppData\Local\Google\Chrome\User Data" --restore-last-session`.
   - Warn the user first — this closes their current Chrome (tabs restore, session/cookies persist).
2. Point Hermes browser tools at it with the OFFICIAL CLI (NOT by editing config.yaml — that write is security-blocked):
   `python -m hermes_cli.main config set browser.cdp_url http://127.0.0.1:9223`
   The backend picks up the new endpoint on the next browser tool call; verify with `browser_navigate` → the real site title should render (no "Just a moment...").
3. Confirm the profile is logged in: on silpo.ua the header showed the user's name + delivery address instead of "Увійти".
- Pitfall: `--restore-last-session` may land on `chrome://intro/` instead of restoring tabs; just open the target URL yourself (browser_navigate now works here because cookies persist — the navigate-reset pitfall below applies to token-only cloud sessions, NOT to a logged-in persistent profile).
- Pitfall: the backend can silently fall back to Lightpanda/headless mid-task ("Chrome fallback requires Chromium… Unknown ref"). If a click fails that way, re-assert `config set browser.cdp_url http://127.0.0.1:9223` and confirm the target Chrome PID is still alive before continuing.
- Pitfall: `browser.cdp_url` alone is NOT enough — the engine must also be `chrome`. The default `config.yaml` ships `browser.engine: lightpanda` (and it can reset on restart). With engine=lightpanda the backend ignores your CDP URL and opens its own Lightpanda/headless instance, so every `browser_click` returns "Unknown ref" even though `browser_navigate` seemed to reach the site. Fix with the OFFICIAL CLI (do NOT hand-edit config.yaml — that write is security-blocked):
  `python -m hermes_cli.main config set browser.engine chrome`
  Then verify BOTH: `config get browser.engine` → `chrome` AND `config get browser.cdp_url` → `http://127.0.0.1:9223`. Only then does `browser_snapshot` show the REAL site (not Cloudflare). On silpo.ua this was the missing piece that turned silent no-op clicks into a working session.
- Direct CDP as a fallback: `Target.getTargets` / `Target.createTarget` over `ws://127.0.0.1:9223/...` (Python `websockets`) works, but `Accessibility.getAXTree` and `Page.captureSnapshot format:"aria"` are NOT supported in current Chrome-for-Testing builds — don't build a snapshotter on them; prefer the Hermes browser tools once cdp_url is pointed correctly.

## 🔴 Pitfall — "Додати у кошик" list/carousel buttons silently no-op (silpo.ua)
Clicking the "Додати у кошик" button in a product LIST, search results, or the "Ви замовляли"/recommended CAROUSEL frequently returns `success: true` but does NOT add the item — the cart badge stays put. The reliable add paths are:
- Open the product's own page, then click its add button; OR
- Once ONE unit is in the cart, use the in-cart "Збільшити кількість" (+) button to raise quantity — that always works.
Always re-open the cart and verify item count + subtotal after a batch of adds; do not trust the per-click `success` flag. If several adds "succeeded" but the cart shows only 1 item, they no-opped — redo via product page or quantity stepper.

## 🟢 MOST RELIABLE add path — JS click via browser_console, scoped to the article
When `browser_click` by ref no-ops OR the backend keeps falling back to Lightpanda ("Unknown ref eNNN"), stop fighting refs and drive the DOM directly through `browser_console` on the logged-in page. This proved the single most reliable add method on silpo.ua this session:
```js
(()=>{const a=[...document.querySelectorAll('article')].find(x=>x.innerText.includes('<PRODUCT NAME SUBSTRING>'));
 if(!a)return 'no article';
 const b=[...a.querySelectorAll('button')].find(x=>(x.getAttribute('aria-label')||'').includes('Додати'));
 if(!b)return 'nobtn (maybe already in cart)';
 b.click();return 'OK'})()
```
- Scope the button search to the matching `<article>` so you click the RIGHT product's add button (page-wide `querySelectorAll` grabs the first of ~47 identical "Додати у кошик" buttons).
- The add button on silpo.ua has NO visible text — match on `aria-label*="Додати"`, not `innerText`.
- To raise quantity: same pattern but match `aria-label*="Збільшити"` and `.click()` N times; to lower, `aria-label*="Зменшити"`.
- Read cart subtotal for verification without opening the cart: `document.body.innerText.match(/Кошик\s*\n?\s*([\d.,]+)\s*грн/)?.[1]` (returns a float).
- SPA re-renders are async: after a click, wrap the next read in `new Promise(r=>setTimeout(()=>r(...),1500-3500))` so the cart badge/subtotal has updated before you read it.

## 🟢 On a logged-in PERSISTENT profile, URL navigation is SAFE (contrast with cloud sessions)
The `browser_navigate`/`location.href` session-reset pitfall applies to token-only cloud/headless sessions. On the user's OWN Chrome via CDP (logged-in persistent profile), navigating by URL — `location.href='https://silpo.ua/search?find=балик'` or `browser_navigate` to a category — works fine: cookies persist, no re-login, no CF challenge. This makes `/search?find=<term>` the fastest way to reach a specific product to add. Verify the slug though: guessed category slugs 404 ("сторінка пішла за покупками"); get the real href by reading the category link's `.href` from the "Всі товари" menu first.

## 🔴 Pitfall — cooked-food ("Готові страви") timeslot restriction
Prepared/cooked items (pizza, kulinariya) cannot be delivered same-day — the cart shows an alert like "смаколики ще не будуть готові / не доставимо в обраний час". Select a NEXT-DAY timeslot when the cart contains готові страви, or the order can't be placed.

## Anti-bot / Cloudflare
- First load often shows "Just a moment..." — sleep 10–18s, then snapshot; it usually passes.
- Longer pauses BETWEEN clicks reduce block risk (user guidance). Pauses do NOT prevent the `browser_navigate` session reset — only avoiding navigate does.
- Browserbase free plan runs WITHOUT residential proxies → detection is more aggressive. If you keep getting challenges, note it; a Scale plan proxy would help but isn't required for most tasks.
- Static JS/CSS assets behind CF often return 0 bytes to `curl` (even with UA/Referer). Don't try to download bundles with curl — drive them through the browser or use web_extract. The OIDC `.well-known/openid-configuration` endpoint IS reachable via curl, though.

## OTP-SMS relay pattern (no bot can read the user's SMS)
- Drive the browser to the login/phone step, type the number, click send.
- Tell the user "SMS sent to +XXX… send me the code" and STOP.
- When the user relays the code, type it into the field and click submit immediately (codes are valid ~5 min).
- If a session reset happens while waiting, you'll need a FRESH code — tell the user the old one is dead and ask for the new one. Never silently retry an expired code.

## 🔴 Proactivity pitfall (from a real failure this session)
If the session crashes, the site blocks you, the token slips, or ANY step fails mid-task — **report to the user IMMEDIATELY**. Do not go silent and wait for them to ask. Silence >10 min on a broken process is unacceptable. On long tasks, send intermediate status updates on your own (~10 min cadence) even if nothing changed.

## Verification
- After each "Додати у кошик" click, snapshot and check the cart badge (e.g. "1" + subtotal) in the header to confirm the add landed. Clicks sometimes no-op after a silent reset — re-click if the cart didn't move.
- Before final confirm/payment, dump the cart contents and total and hand control back to the user.

## Support files
- `references/silpo_case.md` — condensed knowledge bank from the silpo.ua run (endpoints, OTP flow, CF behavior, discount findings).
- `scripts/extract_discounts.sh` — grep a snapshot file for products with discount ≥ threshold.
- `templates/relaunch_chrome_cdp.ps1` — relaunch the user's visible Chrome (same profile) with a CDP port so Hermes browser tools can attach to their logged-in session.

## Fast API Bypass for Oracle HCM / Candidate Experience Job Portals
When inspecting career portals built on Oracle Cloud Candidate Experience (`.../hcmUI/CandidateExperience/en/sites/<site_id>/jobs...`):
- Avoid heavy HTML parsing/scraping. The frontend calls an underlying REST API directly:
  `GET https://<domain>/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true&expand=all&finder=findReqs;siteNumber=<site_id>,limit=50,sortBy=POSTING_DATES_DESC`
- Response schema: `items[0].requisitionList[]` containing `Id`, `Title`, `PostedDate`, `PrimaryLocation`, etc.
- Direct Job URL pattern: `https://<domain>/hcmUI/CandidateExperience/en/sites/<site_id>/job/<Id>`.

## Cron Job Script Path & Delivery Gotcha
When scheduling recurring tasks via `cronjob(action='create')`:
- `script` parameter MUST be a **relative path** to `~/.hermes/scripts/` (e.g. `check_jobs.py`), NOT an absolute path like `C:/Users/...`.
- For desktop/GUI/TUI sessions, pass `deliver='all'` or explicit target channel so reports reach Telegram/destinations instead of defaulting to silent `deliver='local'`.

