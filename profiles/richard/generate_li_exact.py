import gspread

gc = gspread.service_account(filename='/opt/hermes/profiles/richard/google_service_account.json')
sh = gc.open_by_key('1ceJzlfTCQIvJeMoBZfIhxesFxPM9mbV_iAMe6qXEIMo')
ws = sh.worksheet('👔 LinkedIn Decision Makers & DMs')
rows = ws.get_all_values()[1:]

with open('/opt/hermes/profiles/richard/Navo24_LinkedIn_Outreach_Playbook.md', 'w', encoding='utf-8') as f:
    f.write('# NAVO24 LINKEDIN EXECUTIVE OUTREACH — 2026 MASTER PLAYBOOK\n\n')
    f.write('> 200 целевых ЛПР с точными именами и должностями.\n')
    f.write('> Формат сообщений: чистый мессенджер (без подписей), персональное обращение строго по имени человека (Hi {FirstName}).\n\n---\n\n')
    
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
        
        f.write(f"### #{idx}. {comp} — {dm_name} ({role})\n")
        f.write(f"- **Target DM:** **{dm_name}** | `{role}`\n")
        f.write(f"- **Company Website:** {web}\n")
        f.write(f"- **LinkedIn Direct Search:** [Search on LinkedIn]({li_search})\n")
        f.write(f"- **Product Focus:** {prod}\n")
        f.write(f"- **Context:** {context}\n\n")
        f.write(f"**1. Connect Note:**\n")
        f.write(f"```text\n{connect_note}\n```\n\n")
        f.write(f"**2. 1st Direct Message (Chat):**\n")
        f.write(f"```text\n{dm_msg}\n```\n\n")
        f.write("---\n\n")

print(f"Playbook saved with {len(rows)} exact DM entries!")
