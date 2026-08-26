# Domain: Executive Career Scanner

## Target Companies
- **Big Tech & Frontier AI:** OpenAI, Anthropic, xAI, SpaceX, Google / DeepMind, Microsoft, Amazon, Oracle, Tesla.
- **FreightTech & Logistics Leaders:** DP World, Maersk, MSC, Flexport, Freightos, iContainers, FourKites, project44, Windward, E2open / WiseTech, Cargofy, Manhattan Associates, Descartes Systems, Kuehne + Nagel, DHL Global Forwarding / Supply Chain, DSV Global Transport, DB Schenker, Expeditors International.

## Target Leadership Roles
- Executive & C-Level: CEO, COO, CCO, CBDO, CAIO (Chief AI Officer), CPO (Chief Product Officer), NED (Non-Executive Director / Board Member).
- Leadership: Consultant, VP, Head of, Lead, Director.

## Inspection Strategy
- Scan both official company career portals (ATS / career websites) and LinkedIn job boards daily at 09:00 UTC.
- Scraper Integration: `/opt/hermes/scripts/executive_careers_poller.py` with custom modules for Big Tech (Amazon `amazon.jobs`, Google, Microsoft, Tesla headless WAF bypass).
- Skill: `big-tech-career-scanner` (`/opt/hermes/skills/research/big-tech-career-scanner/SKILL.md`).
- Case: `2026-08-25_big_tech_career_scanner_integration.md`.

## Execution & Data Integrity Rule
- Strictly use scraped job postings from official APIs (Greenhouse/Ashby/Workday/SmartRecruiters/Comeet/WP-REST/Oracle HCM/DOU RSS).
- NEVER fabricate job vacancies, company names, links, or match scores ("99% Match").
- Every URL must be copied byte-for-byte from API output.
- If a source fails or is blocked (⚠️ in script output), report it transparently in the final digest.
