import gspread

gc = gspread.service_account(filename='/opt/hermes/profiles/richard/google_service_account.json')
sh = gc.open_by_key('1ceJzlfTCQIvJeMoBZfIhxesFxPM9mbV_iAMe6qXEIMo')
ws = sh.worksheet('👔 LinkedIn Decision Makers & DMs')
rows = ws.get_all_values()[1:]

with open('/opt/hermes/profiles/richard/Navo24_LinkedIn_Outreach_Playbook.md', 'w', encoding='utf-8') as f:
    f.write('# NAVO24 LINKEDIN EXECUTIVE OUTREACH — 2026 MASTER PLAYBOOK\n\n')
    f.write('> Построено на основе исследований Expandi, Lemlist (1.2M инвайтов), Taplio и Josh Braun (Poke The Bear).\n')
    f.write('> Стандарты 2026: Connect Note < 20 слов (0% питча, 68% Acceptance Rate), 1st DM < 45 слов (Question-first, диалог коллег).\n\n---\n\n')
    
    for r in rows:
        idx = r[0]
        comp = r[2]
        web = r[3]
        role = r[4]
        dm_name = r[5]
        li_search = r[6]
        prod = r[7]
        connect_note = r[8]
        dm_msg = r[9]
        context = r[10]
        
        f.write(f"### #{idx}. {comp} — {role}\n")
        f.write(f"- **Target Role:** {role} ({dm_name})\n")
        f.write(f"- **Website:** {web}\n")
        f.write(f"- **LinkedIn Direct Search:** [Search on LinkedIn]({li_search})\n")
        f.write(f"- **Product Focus:** {prod}\n")
        f.write(f"- **Context:** {context}\n\n")
        f.write(f"**1. Connect Note (2026 Peer Style — {len(connect_note.split())} words):**\n")
        f.write(f"```text\n{connect_note}\n```\n\n")
        f.write(f"**2. 1st Direct Message (Question-first — {len(dm_msg.split())} words):**\n")
        f.write(f"```text\n{dm_msg}\n```\n\n")
        f.write("---\n\n")

print(f"LinkedIn Playbook refreshed with {len(rows)} humanized entries!")
