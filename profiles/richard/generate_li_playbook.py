import gspread

gc = gspread.service_account(filename='/opt/hermes/profiles/richard/google_service_account.json')
sh = gc.open_by_key('1ceJzlfTCQIvJeMoBZfIhxesFxPM9mbV_iAMe6qXEIMo')
ws = sh.worksheet('👔 LinkedIn Decision Makers & DMs')
rows = ws.get_all_values()[1:]

with open('/opt/hermes/profiles/richard/Navo24_LinkedIn_Outreach_Playbook.md', 'w', encoding='utf-8') as f:
    f.write('# NAVO24 LINKEDIN EXECUTIVE OUTREACH PLAYBOOK\n\n')
    f.write('> Подготовлено для Nikita (@nikita51155). 200 целевых ЛПР (1-2 ЛПР на каждую компанию: Operations / Supply Chain / CTO).\n\n---\n\n')
    
    for r in rows:
        idx = r[0]
        st = r[1]
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
        f.write(f"- **Target DM:** {dm_name}\n")
        f.write(f"- **Website:** {web}\n")
        f.write(f"- **LinkedIn Direct Search:** [Search on LinkedIn]({li_search})\n")
        f.write(f"- **Product Focus:** {prod}\n")
        f.write(f"- **Context & Strategy:** {context}\n\n")
        f.write(f"**1. Connect Note (Инвайт <= 300 симв.):**\n")
        f.write(f"```text\n{connect_note}\n```\n\n")
        f.write(f"**2. 1st Direct Message (После принятия инвайта):**\n")
        f.write(f"```text\n{dm_msg}\n```\n\n")
        f.write("---\n\n")

print(f"LinkedIn Playbook saved with {len(rows)} entries!")
