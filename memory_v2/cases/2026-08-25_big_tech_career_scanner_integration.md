# Case: Big Tech Executive Career Scanner Integration

- **Date:** 2026-08-25
- **Category:** research / business
- **Status:** SUCCESS
- **Domain Link:** `career_scanner.md`

## Problem & Context
The daily executive career scanner initially covered FreightTech and specific AI labs via Greenhouse/Ashby/Workday APIs, but lacked coverage for major Big Tech leaders (Google, Microsoft, Amazon, Tesla) due to custom career portals and anti-bot protection (Cloudflare WAF).

## Solution & Implementation
1. **API & Portal Scrapers:** Integrated native API endpoints and targeted scrapers into `/opt/hermes/scripts/executive_careers_poller.py`:
   - **Amazon:** Native `amazon.jobs` API integration.
   - **Google:** `careers.google.com` API / structure poller.
   - **Microsoft:** `jobs.careers.microsoft.com` API parser.
   - **Tesla:** Headless browser scraper handling Akamai/Cloudflare Bot Management on career endpoints.
2. **Skill Registration:** Authoring and registering `/opt/hermes/skills/research/big-tech-career-scanner/SKILL.md` to guide Big Tech career monitoring workflows.
3. **Data Integrity Standard:** Enforced zero-hallucination policy (verifiable real job URLs, accurate match details, transparent reporting of failed endpoints with ⚠️).

## Verification
- Poller tested against Amazon, Google, Microsoft, and Tesla endpoints.
- Incorporated into the daily 09:00 UTC Career Scanner cron run delivering updates directly to Stefan's Telegram DM.
