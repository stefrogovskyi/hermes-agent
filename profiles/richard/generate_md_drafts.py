import json
import gspread

gc = gspread.service_account(filename='/opt/hermes/profiles/richard/google_service_account.json')
sh = gc.open_by_key('1ceJzlfTCQIvJeMoBZfIhxesFxPM9mbV_iAMe6qXEIMo')
ws = sh.worksheet('🎯 Forwarders & NVOCC')
rows = ws.get_all_values()[1:]

with open('/opt/hermes/profiles/richard/Navo24_100_Outreach_Campaign_Drafts.md', 'w', encoding='utf-8') as f:
    f.write('# NAVO24 B2B OUTREACH CAMPAIGN — 100 VERIFIED LEADS & DRAFTS\n\n')
    f.write('> Подготовлено для Nikita (@nikita51155). Стандарты Navo24: SeaRates heritage, DCSA events, D&D free-time, Free tier 5 containers.\n\n---\n\n')
    
    for idx, r in enumerate(rows, 1):
        comp = r[2]
        name = r[4]
        first_name = name.split()[0] if name and name != 'Logistics Executive' else 'there'
        email = r[6]
        website = r[7]
        prod = r[8]
        notes = r[13]
        
        subject = f"{first_name}, direct ocean tracking & carrier feeds for {comp} — Navo24"
        
        body = (
            f"Dear {first_name},\n\n"
            f"I hope you are having a productive week.\n\n"
            f"I am reaching out regarding {comp}'s ocean shipping and logistics visibility. "
            f"Navo24 was founded by the core team and engineering leadership behind SeaRates to provide "
            f"modern, developer-first data infrastructure unifying real-time tracking across 234 ocean carriers, "
            f"5,000+ lane schedules, and 3D container load optimization.\n\n"
            f"Given your operations in global logistics, our platform delivers direct carrier feeds designed to eliminate blind spots:\n"
            f"• Tracking API: 234 ocean carriers, DCSA standard events, observed ETAs, and automated Demurrage & Detention (D&D) free-time calculation.\n"
            f"• Schedules API: 72,000+ live sailings and reliability benchmarks across 255 global ports.\n"
            f"• Free Tier: 5 active containers & 100 API calls per month with zero upfront commitment.\n\n"
            f"You can test our endpoints directly on navo24.com with instant self-serve access.\n\n"
            f"Would you or your team be open to a brief 10-minute introduction this coming week to explore how Navo24 can streamline {comp}'s tracking workflows?\n\n"
            f"Best regards,\n"
            f"Nikita\n"
            f"Navo24 | API-MCP for Logistics & Trade\n"
            f"navo24.com"
        )
        
        f.write(f"### #{idx}. {comp} — {name}\n")
        f.write(f"- **To:** `{name} <{email}>`\n")
        f.write(f"- **Website:** {website}\n")
        f.write(f"- **Product Interest:** {prod}\n")
        f.write(f"- **Original Context:** {notes}\n")
        f.write(f"- **Subject:** `{subject}`\n\n")
        f.write("```text\n" + body + "\n```\n\n---\n\n")

print(f"Generated {len(rows)} drafts cleanly!")
