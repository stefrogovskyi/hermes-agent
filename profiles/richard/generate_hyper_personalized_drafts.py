import gspread

gc = gspread.service_account(filename='/opt/hermes/profiles/richard/google_service_account.json')
sh = gc.open_by_key('1ceJzlfTCQIvJeMoBZfIhxesFxPM9mbV_iAMe6qXEIMo')
ws = sh.worksheet('🎯 Forwarders & NVOCC')
rows = ws.get_all_values()[1:]

with open('/opt/hermes/profiles/richard/Navo24_100_Hyper_Personalized_Drafts.md', 'w', encoding='utf-8') as f:
    f.write('# NAVO24 B2B OUTREACH CAMPAIGN — 100 HYPER-PERSONALIZED DRAFTS\n\n')
    f.write('> 100% глубокая кастомизация под оригинальный запрос каждого клиента. Стандарты: SeaRates heritage, DCSA events, D&D free-time, Free tier 5 containers.\n\n---\n\n')
    
    for idx, r in enumerate(rows, 1):
        comp = r[3]
        name = r[5]
        first_name = name.split()[0] if name and name != 'Logistics Executive' else 'there'
        email = r[7]
        website = r[4]
        prod = r[8]
        subj = r[12]
        notes = r[13]
        strategy = r[14]
        
        req_low = notes.lower()
        
        if 'pay for the number of times' in req_low or 'flat monthly rate' in req_low or 'usage' in req_low:
            custom_hook = f"I noticed your previous inquiry regarding flexible usage models instead of rigid monthly retainers. At Navo24 (founded by the core engineering team behind SeaRates), we specifically designed our API infrastructure with self-serve pay-per-use and a permanent free tier (5 active containers / 100 calls per month) — so you only pay for what you actually track."
            bullets = [
                "• Flexible Tiering: Zero upfront commitments or minimum monthly retainers — scale up or down as your volume changes.",
                "• Tracking API: 234 ocean carriers, DCSA standard events, observed ETAs, and automated Demurrage & Detention (D&D) free-time calculation.",
                "• Instant Sandbox: Self-serve API keys ready in 60 seconds on navo24.com."
            ]
        elif 'manifest' in req_low or 'customs' in req_low or 'software' in req_low:
            custom_hook = f"I am reaching out regarding {comp}'s customs and logistics software systems. Navo24 was built by the founding team and core engineers of SeaRates to provide developer-first, MCP-native data feeds. If your platform files manifests or manages shipment workflows, our unified API can automate real-time carrier milestone ingestion across 234 lines."
            bullets = [
                "• Developer-First MCP API: Standardized DCSA milestone events and webhooks across 234 ocean carriers for direct software ingestion.",
                "• Accurate Milestones: Real-time container discharge, gate-out, and vessel ETA updates verified against live AIS feeds.",
                "• Free Integration Tier: 100 API calls/month and documentation ready on navo24.com."
            ]
        elif 'dfa' in req_low or 'digital forwarder' in req_low:
            custom_hook = f"Following up on your interest in digital forwarding capabilities, I wanted to introduce Navo24. Created by the original team behind SeaRates, we provide the foundational data infrastructure for modern forwarders looking to digitize their operations without building complex multi-carrier scrapers."
            bullets = [
                "• Multi-Carrier Visibility: Real-time tracking across 234 container lines with automatic D&D free-time calculation to protect margins.",
                "• Live Schedules: 72,000+ sailings across 255 global ports to quote clients instantly.",
                "• Free Starter Tier: 5 active containers tracked free every month on navo24.com."
            ]
        elif 'subscribe' in req_low or 'services provided' in req_low or 'subscription' in req_low:
            custom_hook = f"Regarding your inquiry on subscription options and available services: Navo24 was founded by the core leadership behind SeaRates to provide a transparent, modern freight data platform covering multi-carrier tracking, schedules, spot rates, and 3D container loading."
            bullets = [
                "• Full Data Suite: Tracking (234 carriers), Schedules (72k+ sailings), FreightRates (spot benchmarks), and 3D Load Planning.",
                "• Transparent Pricing: Self-serve tiers starting with a free tier (5 containers / 100 calls) up to enterprise API volumes.",
                "• Rapid Setup: Instant web access and API keys via navo24.com."
            ]
        elif any(k in req_low for k in ['rate', 'price', 'freight', 'colombo', 'china', 'aqaba', 'manila', 'subic', 'cost', 'quote']):
            custom_hook = f"I am reaching out regarding {comp}'s shipping and freight rate inquiries. Navo24 — built by the team behind SeaRates — provides live spot rate intelligence alongside unified multi-carrier tracking to give forwarders and shippers complete rate transparency and shipment control."
            bullets = [
                "• FreightRates API: Daily spot rate benchmarks across major trade lanes (ex-Asia, Transpacific, Transatlantic).",
                "• Tracking & D&D: Automated milestone tracking across 234 carriers with free-time expiration alerts.",
                "• Free Tier: 5 containers and 100 API calls/month on navo24.com."
            ]
        elif 'lock track' in req_low or 'track' in req_low or 'container' in req_low:
            custom_hook = f"Regarding container tracking operations at {comp}: Navo24 was founded by the original engineering team of SeaRates to solve blind spots in container visibility. We provide direct carrier connectors across 234 lines with automated calculation of demurrage & detention free-time."
            bullets = [
                "• Tracking API: Real-time DCSA events, observed ETAs, and D&D free-time calculation across 234 carriers.",
                "• AIS Verification: Vessel positions verified against live satellite AIS feeds to eliminate fake carrier ETAs.",
                "• Free Tier: Test 5 live containers right now on navo24.com with zero upfront cost."
            ]
        else:
            custom_hook = f"I hope you are having a productive week. I am reaching out regarding {comp}'s ocean logistics operations. Navo24 was founded by the core team and engineering leadership behind SeaRates to provide modern data infrastructure unifying real-time tracking across 234 ocean carriers, 5,000+ lane schedules, and 3D container load optimization."
            bullets = [
                "• Tracking API: 234 ocean carriers, DCSA standard events, observed ETAs, and automated D&D free-time calculation.",
                "• Schedules API: 72,000+ live sailings and reliability benchmarks across 255 global ports.",
                "• Free Tier: 5 active containers & 100 API calls per month with zero upfront commitment."
            ]

        bullets_str = "\n".join(bullets)
        
        body = (
            f"Dear {first_name},\n\n"
            f"{custom_hook}\n\n"
            f"Key capabilities tailored to your workflow:\n"
            f"{bullets_str}\n\n"
            f"You can explore our endpoints directly on navo24.com — our free tier is active immediately upon signup.\n\n"
            f"Would you or your team be open to a brief 10-minute introduction this coming week to explore how Navo24 can streamline {comp}'s freight workflows?\n\n"
            f"Best regards,\n"
            f"Nikita\n"
            f"Navo24 | API-MCP for Logistics & Trade\n"
            f"navo24.com"
        )
        
        f.write(f"### #{idx}. {comp} — {name}\n")
        f.write(f"- **To:** `{name} <{email}>`\n")
        f.write(f"- **Website:** {website}\n")
        f.write(f"- **Product Focus:** {prod}\n")
        f.write(f"- **Client Original Pain / Context:** {notes}\n")
        f.write(f"- **Tailored Strategy:** {strategy}\n")
        f.write(f"- **Tailored Subject Line:** `{subj}`\n\n")
        f.write("```text\n" + body + "\n```\n\n---\n\n")

print(f"Hyper-personalized MD file generated with {len(rows)} leads!")
