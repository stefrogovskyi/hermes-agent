import gspread

gc = gspread.service_account(filename='/opt/hermes/profiles/richard/google_service_account.json')
sh = gc.open_by_key('1ceJzlfTCQIvJeMoBZfIhxesFxPM9mbV_iAMe6qXEIMo')
ws = sh.worksheet('👔 LinkedIn Decision Makers & DMs')
rows = ws.get_all_values()[1:]

with open('/opt/hermes/profiles/richard/Navo24_LinkedIn_Outreach_Playbook.md', 'w', encoding='utf-8') as f:
    f.write('# NAVO24 LINKEDIN EXECUTIVE OUTREACH — 2026 MASTER PLAYBOOK\n\n')
    f.write('> 200 целевых ЛПР с ПРЯМЫМИ ссылками на их персональные профили в LinkedIn (https://www.linkedin.com/in/...).\n\n---\n\n')
    
    for r in rows:
        idx = r[0]
        comp = r[2]
        web = r[3]
        dm_name = r[4]
        role = r[5]
        direct_in_url = r[6]
        cn = r[10]
        dm = r[11]
        
        f.write(f"### #{idx}. {comp} — {dm_name}\n")
        f.write(f"- **Target DM:** **{dm_name}** | `{role}`\n")
        f.write(f"- **Company Website:** {web}\n")
        f.write(f"- **👤 Direct Personal LinkedIn Profile:** {direct_in_url}\n")
        f.write(f"- **Product Focus:** Direct Ocean Tracking API & Predictive ETA\n\n")
        f.write(f"**1. Connect Note:**\n```text\n{cn}\n```\n\n")
        f.write(f"**2. 1st Direct Message (Chat):**\n```text\n{dm}\n```\n\n")
        f.write("---\n\n")

print(f"LinkedIn Playbook cleanly refreshed with {len(rows)} exact personal profile entries!")
