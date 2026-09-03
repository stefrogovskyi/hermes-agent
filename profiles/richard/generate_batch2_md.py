import gspread

gc = gspread.service_account(filename='/opt/hermes/profiles/richard/google_service_account.json')
sh = gc.open_by_key('1ceJzlfTCQIvJeMoBZfIhxesFxPM9mbV_iAMe6qXEIMo')
ws = sh.worksheet('🎯 Forwarders & NVOCC')
rows = ws.get_all_values()[1:]

batch2_rows = rows[100:]

with open('/opt/hermes/profiles/richard/Navo24_Batch2_100_Outreach_Campaign.md', 'w', encoding='utf-8') as f:
    f.write('# NAVO24 BATCH 2: 100 B2B OUTREACH EMAILS (#101 - #200)\n\n')
    f.write('> СТРОГИЙ КОНТРОЛЬ: SEARATES FOUNDING TEAM PEDIGREE, БЕЗ ДЛИННОГО ТИРЕ (—), ХУК НА PREDICTIVE ETA VS CARRIER ETA, ОНБОРДИНГ ЧЕРЕЗ TRACKINGMCP.COM/AUTH/SIGNUP.\n\n---\n\n')
    
    for r in batch2_rows:
        idx = r[0]
        status = r[1]
        comp = r[3]
        email = r[6]
        contact = r[7]
        web = r[10]
        phone = r[11]
        sender = r[13]
        reply_to = r[14]
        cc = r[15]
        subj = r[16]
        body = r[17]
        
        f.write(f'### #{idx}. {comp}\n')
        f.write(f'- **To:** `{contact} <{email}>`\n')
        f.write(f'- **From:** `{sender}`\n')
        f.write(f'- **Reply-To:** `{reply_to}` | **CC:** `{cc}`\n')
        f.write(f'- **Website:** {web} | **Phone:** {phone}\n')
        f.write(f'- **Subject:** `{subj}`\n\n')
        f.write(f'```text\n{body}\n```\n\n')
        f.write('---\n\n')

print(f"Batch 2 MD file written successfully with {len(batch2_rows)} leads!")
