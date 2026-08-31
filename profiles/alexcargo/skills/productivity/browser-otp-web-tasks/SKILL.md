---
name: browser-otp-web-tasks
description: Automate SMS-OTP logins on Cloudflare-protected SPA sites.
---

# Browser OTP Web Tasks

Driving a real logged-in session on a bot-protected single-page app on the user's behalf: shopping carts, bookings, portal forms. The agent operates the browser; the user supplies the OTP and the final confirm. Proven on silpo.ua grocery ordering.

## Hard boundaries (state these up front, once)
- **OTP / SMS codes**: the agent CANNOT receive them. The user reads the code off their phone and pastes it into chat. Every login round-trip is collaborative.
- **Final money/commit step** (pay, place order, submit irreversible form): STOP before it. Show the user the review state and let THEM press the last button, unless they have explicitly pre-authorized the agent to complete it.
- Never ask for or store passwords in plaintext. OTP-only sites sidestep this — prefer them.

## The OTP login handshake (proven on silpo.ua)
1. `browser_navigate` to site root. Expect a Cloudflare interstitial (`title: "Just a moment..."`, `element_count: 0`). NOT a failure.
2. **Wait and re-navigate**: `terminal sleep 8-15` then navigate again. Cloudflare usually clears after one short pause. SPA may return `snapshot: (empty page)` for a beat — re-`browser_snapshot` once to let it render.
3. Click "Sign in" / "Увійти". Usually hands off to a separate auth origin in an iframe (e.g. `auth.silpo.ua/login?...`). If the header click lands you on `about:blank`-blocked state, **navigate directly to the auth iframe URL** captured from `frame_tree` — it's a first-class page you can drive.
4. Phone field often demands full international format. "Must be N digits" = it wants the country code, no `+`, no separators (Ukraine: `380XXXXXXXXX`, 12 digits — NOT `0XX...`).
5. Submit → SMS sent → tell the user "SMS sent to <masked number>, paste the code". They reply with it.
6. Type code into OTP box, click Continue. Success = URL changes to OAuth callback (`.../signin-callback...?code=...`). Navigate to site root; verify by the account name / delivery address in the header.

## Pitfalls (each cost real time)
- **Cloudflare re-challenge wipes the session.** Hard-navigating mid-task can trigger a NEW Cloudflare check → NEW browser session id → dropped auth cookies → back to logged-out "Увійти". **Avoid direct-URL navigation once logged in.** Move via in-page menu clicks (menu → category). If you must hard-navigate, expect to re-auth.
- **Guessing category/deep URLs 404s** AND risks the re-challenge above. Use the site's own nav elements from the snapshot; don't hand-craft `/category/<slug>` URLs.
- **`about:blank` frame blocks** `browser_click`/`browser_type`/`browser_console` ("targets a private or internal address"). Recover by `browser_navigate` back to the real page URL, then redo the field.
- **OTP expires on reload.** If the page reloaded between "user sent code" and your type action, the old code is dead — the site re-issues a fresh SMS. Ask for the new code and SAY why; never silently type a stale one.
- Snapshots on these SPAs are huge (1000+ elements). Prefer targeted refs from the compact snapshot; use `full=true` sparingly.

## Proactive status reporting (STANDING USER RULE — do not violate)
Stefan was left waiting >10 min during a silent session slip and only found out it broke by asking. Rule for ALL long / interactive / background tasks:
- The moment ANYTHING stalls — session dropped, Cloudflare loop, process died, blocked frame, waiting on the user — **message the user immediately** with what happened and what you need. Never go silent behind a broken step.
- On multi-minute background work, send unprompted progress pings (e.g. a 10-min status cron) so the user isn't left guessing.
- When you re-issue an OTP or reset a flow, explicitly say the previous code is void.

## Backend stability: PREFER LOCAL CHROME OVER CLOUD BROWSERBASE (critical)
manual OTP wait. Root cause: the cloud session is recreated on each `browser_navigate`
(new session id) and Cloudflare re-challenges it, invalidating the short-lived OAuth
token. On a CF+OAuth SPA (silpo.ua, ~1-min OTP token) this makes the OTP handshake
unwinnable — you request SMS, the user pastes the code, but by then the cloud session
has reset to `about:blank` and the code is void. ~10 rounds lost to this.

**Fix (Hermes): drive the user's REAL local Chrome via CDP — same model Perplexity
uses, and it survives the wait.** Steps proven on Stefan's Windows host:
1. Launch Chrome with remote debugging:
   `Start-Process 'C:\Program Files\Google\Chrome\Application\chrome.exe' -ArgumentList '--remote-debugging-port=9222','--user-data-dir=C:\Users\Stefan\AppData\Local\hermes\chrome-cdp-profile','--no-first-run','--no-default-browser-check' -WindowStyle Minimized`
   Verify: `curl -s http://127.0.0.1:9222/json/version` returns `webSocketDebuggerUrl`.
2. Point Hermes at it (do NOT hand-edit config.yaml — blocked as security-sensitive;
   use the CLI):
   `hermes config set browser.cdp_url "http://127.0.0.1:9222"`
   (Code path `tools/browser_tool.py:_get_cdp_override` then SKIPS Browserbase and
   connects to the CDP endpoint; navigate output shows `"stealth_features":["cdp_override"]`.)
3. Now `browser_navigate` / clicks are stable — no Cloudflare challenge (real fingerprint),
   session persists across the OTP round-trip. Re-navigate freely; the `about:blank` /
   re-challenge pitfalls below only apply to the cloud backend.

If you are on the cloud backend and see repeated `about:blank` after an OTP wait:
switch to local CDP before burning more codes. Reference `references/local-cdp-backend.md`.

## Verification before handing back
- Confirm login is real (header shows the user's name + saved delivery address) before building the cart.
- Before the final stop, summarize the review state (items, quantities, total vs. any minimum, delivery slot) so the user can sanity-check, then hand off the last click.
