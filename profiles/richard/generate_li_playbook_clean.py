import gspread

gc = gspread.service_account(filename='/opt/hermes/profiles/richard/google_service_account.json')
sh = gc.open_by_key('1ceJzlfTCQIvJeMoBZfIhxesFxPM9mbV_iAMe6qXEIMo')
ws = sh.worksheet('👔 LinkedIn Decision Makers & DMs')
rows = ws.get_all_values()[1:]

with open('/opt/hermes/profiles/richard/Navo24_LinkedIn_Outreach_Playbook.md', 'w', encoding='utf-8') as f:
    f.write('# NAVO24 LINKEDIN EXECUTIVE OUTREACH — 2026 MASTER PLAYBOOK\n\n')
    f.write('> 200 целевых ЛПР с рабочими ссылками на страницы компаний и X-Ray поиском профилей.\n\n---\n\n')
    
    for r in rows:
        idx = r[0]
        comp = r[2]
        web = r[3]
        comp_li = r[4]
        role = r[6]
        dm_name = r[7]
        xray = r[8]
        prod = r[9]
        cn = r[10]
        dm = r[11]
        
        f.write(f"### #{idx}. {comp} — {dm_name} ({role})\n")
        f.write(f"- **Target Role:** `{role}` ({dm_name})\n")
        f.write(f"- **Company Website:** {web}\n")
        f.write(f"- **🏢 Company Page on LinkedIn:** [Open Company on LinkedIn]({comp_li})\n")
        f.write(f"- **🎯 Find Exact Profiles (Google X-Ray):** [Search Real Profiles on LinkedIn]({xray})\n")
        f.write(f"- **Product Focus:** {prod}\n\n")
        f.write(f"**1. Connect Note:**\n```text\n{cn}\n```\n\n")
        f.write(f"**2. 1st Direct Message (Chat):**\n```text\n{dm}\n```\n\n")
        f.write("---\n\n")

print(f"LinkedIn Playbook cleanly refreshed with {len(rows)} entries!")
