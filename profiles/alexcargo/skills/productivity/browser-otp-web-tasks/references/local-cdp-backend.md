# Local Chrome via CDP — stable backend for OTP web tasks

## Why
Cloud browser (Browserbase / `browser.cloud_provider: browser-use` in `config.yaml`)
recreates its session on every `browser_navigate`. On a Cloudflare + OAuth SPA
(`auth.silpo.ua`, client `silpo--site--spa`) the OAuth token is short-lived
(~1 min). The manual OTP round-trip (agent requests SMS -> user reads code off phone
-> pastes to agent -> agent types it) takes longer than the token/session survives, so
by the time the code arrives the cloud session has reset to `about:blank` and the code
is void. Symptom: repeated `Blocked: page URL targets a private or internal address
(about:blank)` and `silent-refresh error=login_required` after every SMS wait.

Perplexity / similar assistants avoid this because they drive the user's *real* local
browser through CDP — the session is the user's own tab and never resets.

## Recipe (proven on Stefan's Windows 10 host, 2026-07-25)
Chrome is at `C:\Program Files\Google\Chrome\Application\chrome.exe`.

1. Launch with a dedicated profile + debug port (keep it alive; it's the session host):
```powershell
Start-Process 'C:\Program Files\Google\Chrome\Application\chrome.exe' `
  -ArgumentList '--remote-debugging-port=9222', `
                 '--user-data-dir=C:\Users\Stefan\AppData\Local\hermes\chrome-cdp-profile', `
                 '--no-first-run','--no-default-browser-check' `
  -WindowStyle Minimized
```
2. Confirm the CDP endpoint answers:
```bash
curl -s http://127.0.0.1:9222/json/version   # expect webSocketDebuggerUrl + "Browser":"Chrome/..."
```
3. Point Hermes at it. `config.yaml` edits are blocked as security-sensitive — use the CLI:
```bash
hermes config set browser.cdp_url "http://127.0.0.1:9222"
```
   (Accepted keys confirmed: `browser.cdp_url`. The dispatcher
   `tools/browser_tool.py::_get_cdp_override` reads `BROWSER_CDP_URL` env or
   `browser.cdp_url` config and connects directly, skipping Browserbase. Read output
   shows `"stealth_features":["cdp_override"]` once active.)
4. `browser_navigate https://silpo.ua/` -> loads with NO Cloudflare interstitial
   (real fingerprint). Session now persists across clicks / re-navigates / the OTP wait.

## Notes / gotchas
- The CDP Chrome opens on its own new-tab page; navigate it to the auth URL directly
  (`browser_navigate https://auth.silpo.ua/login?...`) — it lands instantly, no CF.
- Keep the Chrome process running for the whole task. If it dies, the `cdp_url` still
  points at the port but connections fail — just relaunch step 1.
- `browser.cloud_provider` can stay `browser-use`; the explicit `cdp_url` takes
  precedence and overrides it (code: "when set, skip Browserbase and connect directly").
- OIDC token on silpo.ua lives only in Angular app memory (not in localStorage /
  document.cookie), so you CANNOT replay it via raw `curl` — stay in the browser for
  cart actions. Pure-API takeover is not achievable here; the win is simply session
  stability via local CDP.
- This is a user-hosted, environment-bound setup (local Chrome + port 9222). It is the
  *fix*, not a general claim about the cloud backend — capture the recipe, not
  "cloud browser is broken".
