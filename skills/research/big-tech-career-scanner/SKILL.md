---
name: big-tech-career-scanner
description: "Scan Big Tech & AI executive roles via official APIs."
version: 1.0.0
author: Stefan Rogovskiy & Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [careers, executive, big-tech, jobs, recruiting, amazon, ai]
    category: research
    related_skills: [ats-job-board-apis]
---

# Big Tech & AI Executive Career Scanner

Scan official ATS endpoints (Greenhouse, Ashby, Workday, SmartRecruiters, Amazon Jobs API) for C-Level, VP, Director, and Head of leadership roles across Big Tech, Frontier AI, and FreightTech companies.

## When to Use

Use this skill whenever:
- The user asks to scan, monitor, or check executive/leadership vacancies at Big Tech (Amazon, OpenAI, Anthropic, SpaceX), FreightTech (Maersk, Flexport, p44), or IT Ukraine ($5k+).
- Running daily automated 09:00 career briefs.
- Researching current hiring trends in AI, Operations, and GTM leadership.

## Monitored Companies (12+ Sources)
- **Big Tech & Cloud:** Amazon / AWS
- **AI Frontier:** OpenAI, Anthropic
- **DeepTech & Aerospace:** SpaceX
- **FreightTech & Logistics:** Maersk, Flexport, project44, FourKites, WiseTech Global, Manhattan Associates, Windward, Descartes
- **IT Ukraine ($5k+ Senior/Lead/BizDev):** GitLab, Superhuman/Grammarly, Genesis, SKELAR, EPAM, SoftServe, etc.

## Usage

### Run on-demand scan
```bash
/opt/hermes/hermes-agent/venv/bin/python3 /opt/hermes/scripts/executive_careers_poller.py
```

### Output format
- Outputs deduplicated new vacancies to `/opt/hermes/executive_vacancies_found.json`
- Preserves seen state in `/opt/hermes/state/exec_careers_seen.json`
- Each vacancy contains verified title, location, category, matched keywords, and direct clickable apply URL.
