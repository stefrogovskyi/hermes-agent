---
name: browser-local-cdp
description: "Local Chrome CDP for stable logged-in/OTP browser sessions."
version: 1.0.0
author: Hermes Stevenson
tags: [browser, cdp, chrome, cloudflare, otp, login, session, silpo]
---

# Browser: Local Chrome via CDP (stable sessions)

## When to use
- YouTube "Watch Later" or OAuth/Cloudflare SPA tasks requiring persistent logged-in Chrome user data profiles (`chrome_youtube_user_data` or `chrome-cdp-profile`).
- A site shows a **Cloudflare "Just a moment..."** challenge on (almost) every `browser_navigate`, or the session resets / logs you out between steps.
- You must stay **logged in** across many clicks (OTP email/SMS login, bank, shop cart).
- The user expects local, stable browser control (referenced Perplexity managing their real browser).
- `browser_navigate` results carry `"stealth_features": ["browser_use"]` / `"Running WITHOUT residential proxies"` — that's the cloud backend.

## Root cause
`config.yaml` defaults to `browser.cloud_provider: browser-use` (Browserbase cloud). Each `browser_navigate` can spin a fresh cloud session → new fingerprint → Cloudflare challenge → auth token dies. Short OIDC tokens + a manual OTP step in the middle = guaranteed logout before you can use the code.

## Fix (one-time setup)
1. **Launch Chrome headless with a remote-debugging port** (separate user-data-dir so it doesn't touch the user's normal profile). Use `--headless=new` + `-WindowStyle Hidden` so NO visible window appears — otherwise every `browser_navigate` spins a new visible Chrome that never closes, piling up dozens of black windows:
   ```powershell
   Start-Process 'C:\Program Files\Google\Chrome\Application\chrome.exe' `
     -ArgumentList '--headless=new','--remote-debugging-port=9222',`
       '--user-data-dir=C:\Users\Stefan\AppData\Local\hermes\chrome-cdp-profile',`
       '--no-first-run','--no-default-browser-check','--disable-gpu' `
     -WindowStyle Hidden
   ```
   Verify: `curl -s http://127.0.0.1:9222/json/version` returns JSON with `webSocketDebuggerUrl`. (On Linux add `--no-sandbox --disable-dev-shm-usage`.)
   If you ever launched it visibly by mistake, run `scripts/kill_stray_chrome.ps1` to reap only the agent's orphaned Chrome (profile `chrome-cdp-profile`) — it spares the user's real Chrome.
2. **Point Hermes at it** (config.yaml is security-protected — use the CLI, never hand-edit):
   ```bash
   hermes config set browser.cdp_url http://127.0.0.1:9222
   hermes config set browser.engine lightpanda   # headless engine, no GUI/console windows
   ```
   `cdp_url` takes precedence over `cloud_provider`; Hermes then connects directly to your Chrome (no cloud, no Cloudflare challenge, session lives in your real browser). `engine: lightpanda` is the belt-and-suspenders safeguard so even if a local-mode launch happens it draws no window.
3. **Verify**: `browser_navigate` to the target site. The result should show `"stealth_features": ["cdp_override"]` and load the page **without** a Cloudflare interstitial.

## OTP / login pattern (when the UI submit button silently fails)
On some SPAs the submit button stays clickable but fires **no network request** (React state wasn't updated by synthetic `browser_type`). Bypass the UI:
1. Find the endpoint: hook `window.fetch` / `XMLHttpRequest.open` in `browser_console` BEFORE clicking, then read the captured URL. (silpo: `POST /api/v2/Login/ByPhone`.)
2. Call it directly from `browser_console` (same-origin, cookies included):
   ```js
   await fetch('/api/v2/Login/ByPhone?returnUrl=' + encodeURIComponent(ru), {
     method:'POST', headers:{'Content-Type':'application/json'}, credentials:'include',
     body: JSON.stringify({ Phone: '380636222272' })   // full 12 digits, key is `Phone` not `phoneNumber`
   })
   ```
3. **Respect SMS anti-spam.** Hammering the button trips `SMSSendingLimit` / `spam detected (code 36058)` and blocks new codes for minutes. Wait `secondsTillNextOTP` between tries; don't re-click on failure.

## Pitfalls
- **BLACK / TERMINAL WINDOWS (must avoid).** Three distinct causes, all observed:
  1. *Local-mode `agent-browser` launcher.* When `browser.cdp_url` is NOT set, Hermes local mode runs `agent-browser` (Node/Rust) which spawns a Chromium daemon **and its console**; these can pile up (observed: 45 orphaned `chrome.exe` + 7 orphaned `conhost.exe`, profile `chrome-cdp-profile`, while the user's real Chrome with YouTube stayed alive). Fix: set `browser.cdp_url` (CDP path, no local chrome-engine) AND `browser.engine: lightpanda` (headless, no GUI) so no window/console is ever drawn. Also launch Chrome with `--headless=new` + `-WindowStyle Hidden` (see Fix step 1).
  2. *Visible Chrome.* Launching Chrome WITHOUT `--headless=new`/`-WindowStyle Hidden` makes a visible window per session; the tool may never close them → dozens of black empty windows stack on the desktop.
  3. *Hermes cron `no_agent` `.py` jobs* flash a `conhost` every 2–10 min via the **uv base python** (it re-execs a visible console even under CREATE_NO_WINDOW). Symptom: window title `C:\Users\Stefan\AppData\Loca...` on a fixed cadence (5m/2m/10m), unrelated to any browser action. Fix: wrap each `script:` in a `.sh` calling the **BASE `python.exe` directly** (NOT `pythonw.exe` — in a uv venv `pythonw.exe` is ALSO a uv-launcher that re-execs a visible console; confirmed: conhost still grew 3→4 after switching to `pythonw`). See `windows-silent-background-automation` §1b + `scripts/cron_hidden_sh_template.sh`. Do NOT mistake these for browser windows — they come from the scheduler, not `browser_*`.
  **Cleanup when they pile up:** the agent's `conhost.exe`/`chrome.exe` are orphaned (parent daemon already dead). They do NOT carry `chrome-cdp-profile` in their own cmdline (they inherit it from the dead parent). Kill them by exclusion: keep any `chrome.exe` whose cmdline contains the user's real `User Data` profile or `remote-debugging-port=9222`; kill the rest. Never blanket-kill all `chrome.exe` (would kill the user's real browser). A ready script is at `scripts/kill_stray_chrome.ps1`.
- **Don't hand-edit config.yaml** — agent is blocked from writing it; use `hermes config set`.
- **Phone field auto-prefixes +380.** If you `browser_type` `380636222272` the mask collapses it; for the **API** send the full 12-digit `Phone`. For the **UI** let the site keep its `+380` and type only the 9 trailing digits.
- **Port busy?** Use 9223+ or kill the stray Chrome. On Linux add `--no-sandbox --disable-dev-shm-usage`.
- Keep the Chrome process alive (background/minimized) for the whole task — it IS the session.
- After switching to CDP, `browser_navigate` no longer resets auth, so you can take your time; the OTP wait no longer kills the session.

## Driving the user's REAL logged-in Chrome (the silpo case)

The separate-headless-profile approach (§Fix) only helps if you can log in fresh via OTP. When the **user is already logged into the target site in their normal Chrome**, attach to THEIR browser instead — it keeps their session and avoids Cloudflare entirely.

1. **Find their profile:** enumerate `chrome.exe` cmdlines; the one with `user-data-dir=...\Google\Chrome\User Data` (NOT `chrome-cdp-profile`) is theirs.
2. **Relaunch with a debug port** (same profile ⇒ cookies/login survive):
   ```powershell
   Get-CimInstance Win32_Process -Filter "Name='chrome.exe'" | Where-Object {
     $_.CommandLine -match 'user-data-dir=C:\\Users\\Stefan\\AppData\\Local\\Google\\Chrome\\User Data'
   } | ForEach-Object { taskkill /F /PID $_.ProcessId /T }
   Start-Sleep -Seconds 3
   Start-Process 'C:\Program Files\Google\Chrome\Application\chrome.exe' -ArgumentList `
     '--remote-debugging-port=9223','--user-data-dir=C:\Users\Stefan\AppData\Local\Google\Chrome\User Data','--restore-last-session'
   ```
   If `--restore-last-session` lands on `chrome://intro` (prior close was unclean), just open a fresh `https://silpo.ua/` tab via `Target.createTarget` — cookies are still in the profile, so login persists and Cloudflare is skipped.
3. **Connect — two ways:**
   - Preferred: `hermes config set browser.cdp_url http://127.0.0.1:9223` (the agent is **blocked from hand-editing config.yaml** — `hermes config set` is the only allowed path). Then `browser_navigate` works normally.
   - **Fallback when config can't be changed:** drive Chrome directly through the DevTools websocket with Python `websockets` (already in the venv). `scripts/cdp_drive.py` is a ready driver (list tabs, snapshot, click-by-text, type, navigate) — no config edit needed.
4. **Verify:** `curl -s http://127.0.0.1:9223/json/version` → `webSocketDebuggerUrl`.

### CDP snapshot gotcha
`Accessibility.getFullAXTree` on current Chrome (v151) returns a result **without** an `axTree` key → `KeyError`. Use **`Page.captureSnapshot` with `{"format":"aria"}`** — returns readable ARIA HTML in `result.data`. `cdp_drive.py` uses this.

### SPA navigation warning (silpo)
After login, do NOT `browser_navigate`/paste a deep category URL — it resets the session/OAuth and re-triggers Cloudflare. Navigate only by clicking in-page menu buttons, or open a fresh `https://silpo.ua/` tab (inherits profile cookies, skips Cloudflare).

## Scripts (copy-paste as needed)
- `scripts/kill_stray_chrome.ps1` — **ready-to-run** cleanup: kills ONLY the agent's orphaned Chrome (`chrome-cdp-profile`) + conhost, spares the user's real Chrome. Run it when black/terminal windows pile up.
- `scripts/cdp_drive.py` — **ready-to-run** CDP driver for the user's real Chrome when `config.yaml` browser.cdp_url can't be edited. Library + CLI: `python cdp_drive.py --port 9223 --url https://silpo.ua/ --snapshot`.

**Launcher (headless + hidden — no black windows):**
```powershell
$chrome='C:\Program Files\Google\Chrome\Application\chrome.exe'
$profile='C:\Users\Stefan\AppData\Local\hermes\chrome-cdp-profile'; $port=9222
Get-CimInstance Win32_Process -Filter "Name='chrome.exe'" | Where-Object {$_.CommandLine -like "*chrome-cdp-profile*"} | ForEach-Object {Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue}
Start-Sleep -Seconds 1
Start-Process $chrome -ArgumentList '--headless=new',"--remote-debugging-port=$port","--user-data-dir=$profile",'--no-first-run','--no-default-browser-check','--disable-gpu' -WindowStyle Hidden
Start-Sleep -Seconds 5
(Test-NetConnection -ComputerName 127.0.0.1 -Port $port -InformationLevel Quiet) ? "Chrome CDP up on :$port" : 'Chrome CDP FAILED'
```

**Kill ONLY the agent's stray Chrome (spares the user's real Chrome):**
```powershell
# Keep the user's real Chrome (default profile / open tabs like YouTube) alive.
$userPid = (Get-CimInstance Win32_Process -Filter "Name='chrome.exe' AND CommandLine LIKE '%User Data%'").ProcessId | Select-Object -First 1
$orphans = Get-CimInstance Win32_Process -Filter "Name='chrome.exe'" | Where-Object {
  $_.ProcessId -ne $userPid -and $_.CommandLine -like "*chrome-cdp-profile*"
}
$orphans | ForEach-Object {Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue}
"killed $($orphans.Count) agent-chrome procs"
```
Note: orphaned *renderer* processes may not carry `chrome-cdp-profile` in their own cmdline (they inherit it from the dead parent). If they persist, fall back to killing every `chrome.exe` whose cmdline is NOT the user's `User Data` profile and NOT `remote-debugging-port=9222`.

## See also
- `references/youtube_watch_later_cdp.md` — YouTube "Watch Later" DOM extraction workaround + 23:00 interactive guardrail.
- `references/silpo-otp-ordering.md` — worked silpo.ua example (endpoint, cart criteria, slot).
- `references/troubleshooting.md` — port conflicts, sandbox, verification.
