# Browser recon: discovering a site's hidden JSON API when curl is blocked

Validated 2026-08-17 on Maersk (Akamai + ATS migration) and Descartes (Cloudflare + WordPress).
Goal is NOT to scrape HTML long-term — it is to discover the real backend once, then call it
directly with curl/urllib in the recurring script. Browser stays out of the daily path (cheap + fast).

## Procedure

1. **Open the careers/search page in the browser tool** (headless Chrome via browser_exec).
   - Pitfall: `goto_url()`/`Page.navigate` can hang on Akamai redirect chains (CDP TimeoutError).
     Fallback that works: `js("location.href='<url>'")` then `time.sleep(10-15)` then `page_info()`.
2. **Log every XHR/fetch response** (Playwright variant: `page.on("response", ...)` filtered by
   `resource_type in ("xhr","fetch")`; print `status method url`). The jobs API stands out
   immediately (e.g. `200 GET https://api.maersk.com/careers/vacancies?...`).
   - browser_exec variant (no Playwright needed, works after the page already loaded):
     `js("JSON.stringify(performance.getEntriesByType('resource').filter(r=>['xmlhttprequest','fetch'].includes(r.initiatorType)).map(r=>r.name))")`
     — then filter for `/job|career|position|vacanc/i` and against `/analytic|gtm|sentry|cdn/i`.
2b. **Check iframes before XHR-hunting** — many boards are embedded widgets:
   `js("JSON.stringify(Array.from(document.querySelectorAll('iframe')).map(f=>f.src))")`.
   An src like `https://jobs.ashbyhq.com/{slug}?embed=js` hands you the ATS + slug directly
   (this is how the Grammarly→Superhuman rebrand was resolved: careers page redirected to
   superhuman.com, iframe src exposed Ashby slug `Superhuman%20Platform%20Inc`).
3. **Inspect the captured payload** — it often contains canonical job URLs pointing at the true ATS
   (Maersk payload had `maersk.wd3.myworkdayjobs.com/Maersk_Careers/job/...` → tenant `maersk.wd3`,
   site `Maersk_Careers`).
4. **Re-test the discovered endpoint with plain curl.** Two outcomes:
   - Works (Workday cxs did; WP REST did) → add to the recurring poller, browser no longer needed.
   - 401/blocked outside browser (api.maersk.com itself was 401) → don't fight it; use the
     upstream ATS endpoint found inside the payload instead.
5. **In-page fetch trick** for same-origin APIs: `js("(async()=>{const r=await fetch('/wp-json/...');
   return JSON.stringify(await r.json())})()")` — runs with the page's cookies/headers, bypasses
   Cloudflare that blocks external curl.

## WordPress careers sites (Descartes pattern)

- `/wp-json/wp/v2/types` → find custom post type (`job_listing`).
- `/wp-json/wp/v2/types/job_listing` → read `rest_base` (was `job-listings`, NOT the type name).
- `/wp-json/wp/v2/job-listings?per_page=100` → full list with `title.rendered`, `link`, `modified`.
  `X-WP-Total` header = total count. Often reachable by curl+Chrome-UA even when HTML is behind
  Cloudflare.
- Individual job links may 403 for curl while opening fine in a real browser — verify link liveness
  via the browser, don't judge by curl status.

## Signs a company silently migrated ATS

- Old documented endpoint suddenly 404/302-loops (Maersk Phenom `/widgets` → 404 "Page not found").
- Careers subdomain redirects to the main corporate domain.
- Fix = redo recon from step 1; never keep shipping "source unavailable" without re-checking.

## Headless-browser setup on a bare VPS (validated 2026-08-17, /opt/hermes VPS)

If browser_exec errors "browser-use CLI not found" or "BU_CDP_URL=...:9223 unreachable":

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
uv tool install browser-use
browser-use install-browser        # long: run in background with notify_on_complete
# uv installs to /root/.local/bin which browser_exec's environment may not have:
ln -sf /root/.local/bin/browser-use /usr/local/bin/browser-use
ln -sf /root/.local/bin/uvx /usr/local/bin/uvx
# start the automation Chrome the harness attaches to (path is chrome-linux64, NOT chrome-linux):
/root/.cache/ms-playwright/chromium-*/chrome-linux64/chrome --headless=new \
  --remote-debugging-port=9223 --user-data-dir=/opt/hermes/cache/browser-use/chrome-profile \
  --no-sandbox --disable-gpu --disable-dev-shm-usage about:blank &   # keep running (daemon)
curl -s http://127.0.0.1:9223/json/version   # verify CDP is up
```

First browser_exec call after Chrome start may still time out while the daemon connects — just retry once (`print(page_info())`).
