import gspread

gc = gspread.service_account(filename='/opt/hermes/profiles/richard/google_service_account.json')
sh = gc.open_by_key('1ceJzlfTCQIvJeMoBZfIhxesFxPM9mbV_iAMe6qXEIMo')
ws = sh.worksheet('🎯 Forwarders & NVOCC')
rows = ws.get_all_values()[1:]

with open('/opt/hermes/profiles/richard/Navo24_Humanized_2026_Campaign.md', 'w', encoding='utf-8') as f:
    f.write('# NAVO24 B2B OUTREACH — 2026 HUMANIZED MASTER PLAYBOOK\n\n')
    f.write('> Построено на основе исследований Lavender, Belkins (5.5M писем), Gong (85M писем) и Josh Braun.\n')
    f.write('> Стандарты: 40–65 слов, строчные темы (internal lowercase), 0% AI-клише, Zero-friction interest-based CTA.\n\n---\n\n')
    
    for r in rows:
        idx = r[0]
        comp = r[3]
        country = r[4]
        window = r[5]
        name = r[7]
        title = r[8]
        email = r[9]
        website = r[10]
        context = r[11]
        prod = r[12]
        subj = r[13]
        t1 = r[14]
        t2 = r[15]
        t3 = r[16]
        t4 = r[17]
        
        f.write(f"### #{idx}. {comp} — {name}\n")
        f.write(f"- **To:** `{name} <{email}>` ({title})\n")
        f.write(f"- **Country & Window:** {country} | `{window}`\n")
        f.write(f"- **Website:** {website}\n")
        f.write(f"- **Product Focus:** {prod}\n")
        f.write(f"- **Original Context:** {context}\n")
        f.write(f"- **2026 Subject Line:** `{subj}`\n\n")
        f.write(f"**✉️ Touch #1 (Initial Pitch — ~50 words):**\n```text\n{t1}\n```\n\n")
        f.write(f"**✉️ Touch #2 (Follow-up #1 — D&D Pain Killer):**\n```text\n{t2}\n```\n\n")
        f.write(f"**✉️ Touch #3 (Follow-up #2 — Schedules & 3D):**\n```text\n{t3}\n```\n\n")
        f.write(f"**✉️ Touch #4 (Breakup — Low friction):**\n```text\n{t4}\n```\n\n")
        f.write("---\n\n")

print(f"Saved {len(rows)} correctly indexed leads to Markdown!")
