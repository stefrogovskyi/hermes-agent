---
name: ats-job-board-apis
description: Query real ATS job APIs; never fabricate vacancies.
category: research
tags:
  - jobs
  - careers
  - ats
  - scraping
  - api
---

# ATS Job Board APIs — честный мониторинг вакансий

Career/vacancy monitoring MUST use the official JSON APIs of the company's ATS. Never hand-write vacancy lists, URLs, or "match %" — a hardcoded/hallucinated digest was caught by the user (404s and fake IDs) and destroys trust.

## Endpoint cheat-sheet (all verified live 2026-08-17)

| ATS | Endpoint | Notes |
|---|---|---|
| Greenhouse | `GET https://boards-api.greenhouse.io/v1/boards/{slug}/jobs` | `jobs[].absolute_url` is the real link. Slugs: anthropic, spacex, flexport, project44, fourkites |
| Ashby | `GET https://api.ashbyhq.com/posting-api/job-board/{slug}` | `jobs[].jobUrl`. Slug: openai (740+ jobs). greenhouse/openai returns 0 — OpenAI moved to Ashby |
| Workday | `POST https://{tenant}.wd{N}.myworkdayjobs.com/wday/cxs/{tenant}/{site}/jobs` body `{"appliedFacets":{},"limit":20,"offset":N,"searchText":""}` | Paginate by offset until `total`. Job URL = `https://{host}/en-US/{site}{externalPath}`. HTTP 422 = wrong site name — brute-force site names (External, Careers, company name). Found: `manh.wd5` site `External`; `maersk.wd3` site `Maersk_Careers` (~1300 jobs) |
| WordPress careers site | `GET /wp-json/wp/v2/{rest_base}?per_page=100` | Find custom post type via `/wp-json/wp/v2/types` (e.g. `job_listing`), then its `rest_base` via `/wp-json/wp/v2/types/{type}` (e.g. `job-listings`). Descartes: `careers.descartes.com/wp-json/wp/v2/job-listings` — works with plain curl + Chrome UA even though the HTML site is behind Cloudflare. Job links may 403 for curl but open fine in a real browser — verify via browser, not status code |
| SmartRecruiters | `GET https://api.smartrecruiters.com/v1/companies/{slug}/postings?limit=100` | Job URL = `https://jobs.smartrecruiters.com/{slug}/{id}`. Slug: WiseTechGlobal |
| Lever | `GET https://api.lever.co/v0/postings/{slug}?mode=json` | |
| Oracle HCM | `GET https://{host}/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true&expand=all&finder=findReqs;siteNumber=CX_1,limit=50,sortBy=POSTING_DATES_DESC` | Used for DP World (`ehpv.fa.em2.oraclecloud.com`) |
| Comeet (widget) | Positions embedded in careers-page HTML: `<a class="comeet-position" href data-location>` + `comeet-position-name` | e.g. windward.ai/careers. Site 403s plain UA — send full Chrome User-Agent + Accept headers |
| DOU (Ukraine job board) | `GET https://jobs.dou.ua/vacancies/{slug}/feeds/` (RSS) | Item title = `"Role в Company, Город"` — split on ` в ` / last `, `. Verified slugs: epam-systems, globallogic, softserve, luxoft, dataart, ciklum, wix, genesis-technology-partners, skelar, grammarly. **TRAP**: `jobs.dou.ua/vacancies/feeds/?company=X` silently IGNORES the param — every "company" returns the identical global feed. Identical results across companies = dead param; find the per-company path (open the company's DOU page in a browser, read `link[type*=rss]`) |
| Workable | `GET https://apply.workable.com/api/v1/widget/accounts/{slug}?details=false` | Quick probe; 200 with `total:0` = account exists but posts elsewhere |
| Recruitee / BambooHR | `https://{slug}.recruitee.com/api/offers/` / `https://{slug}.bamboohr.com/careers/list` | Cheap probes for detection sweeps; BambooHR 302 = no account, 200 = check `meta.totalCount` |

## Detecting which ATS a company uses
1. `curl -sL <careers page> | grep -oiE "phenom|workday|greenhouse|lever|comeet|smartrecruiters|ashby|successfactors"`
2. Probe the standard endpoints above with the company slug variants.
3. Careers page unreachable to curl (Akamai/Cloudflare, redirect loops, 302/411)? Do **browser recon** — see `references/browser-api-recon.md`. Open the page in headless Chrome, log all XHR/fetch responses, and read which backend the site really calls. This is how Maersk was cracked: the old Phenom portal was dead, XHR log revealed `api.maersk.com/careers/vacancies` whose payload contained `maersk.wd3.myworkdayjobs.com` URLs → plain Workday cxs API works curl-side. Companies migrate ATS silently; a dead endpoint means "re-recon", not "impossible".

## Critical pitfalls
- **Fake-200 rikoshet pages**: Greenhouse job URL with an invented ID can still return HTTP 200 (board landing redirect). A 200 status does NOT prove the vacancy exists — verify the ID is present in the board's API listing.
- **Dedup**: keep a seen-store (`state/*_seen.json` of uids like `gh:slug:id`); report only NEW since last run. First run = baseline, show top-N relevant instead.
- **Relevance**: filter titles by role regex (chief/CxO/VP/head of/director/lead) and score by profile keywords — honest "matched keywords", never invented "99% Match".
- **Seniority traps in sales titles**: "Business Development **Representative**" (BDR/SDR) is a junior cold-calling role, NOT BizDev leadership. For senior-only ($5k+) filters, exclude `representative|SDR|BDR|junior|trainee|intern|QA|support|recruiter|talent` alongside the include regex.
- **Company rebrands break slugs silently**: Grammarly became Superhuman Platform Inc (2026) — grammarly.com/careers redirects to superhuman.com and the old Greenhouse slug is dead; the live board is Ashby slug `Superhuman%20Platform%20Inc` (embedded as `jobs.ashbyhq.com/...?embed=js` iframe). If a known company's board suddenly 404s/empties, follow the careers-page redirect in a browser and read the embed iframe src for the new ATS+slug.
- **"0 jobs" can be a true answer**: Google Careers Ukraine legitimately returned 0 openings — report the honest zero rather than silently dropping the company or padding with stale data.

## Rules for the LLM step of a vacancy cron (embed in prompt)
1. Use ONLY vacancies from script output; never invent titles/locations/URLs; never alter a URL by one character.
2. No invented match percentages; explain relevance in words.
3. Don't promise "auto-apply" — links open the posting, application is manual.
4. Nothing new → reply exactly `[SILENT]`.
5. Source failed → say so in one line, don't backfill with fabricated data.

## Verification before reporting to user
Spot-check 2-3 output URLs with `curl -s -o /dev/null -w "%{http_code}" -L` AND confirm IDs exist in the source API. Cloudflare-fronted links (Descartes) may 403 for curl yet open fine in a browser — for those verify via the browser tool. Working reference implementation: `/opt/hermes/scripts/executive_careers_poller.py` (v2, Greenhouse+Ashby+Workday+SmartRecruiters+Comeet+WP-REST+DOU RSS with shared seen-store and two independent sections: global executive + IT Ukraine senior-only).

## Support files
- `references/browser-api-recon.md` — headless-browser procedure for discovering a site's hidden JSON API when curl is blocked (Akamai/Cloudflare), incl. WordPress rest_base discovery and detecting silent ATS migrations.
