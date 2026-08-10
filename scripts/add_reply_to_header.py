# -*- coding: utf-8 -*-
"""
add_reply_to_header.py — Внедрение явного заголовка Reply-To: Richard Marlowe <rich@navo24.com>
в richard_email.py для 100% гарантированной подстановки почты Ричарда при нажатии «Ответить» клиентом!
"""

import os, re

richard_dir = r"C:\Users\Stefan\My Drive\Equity\My Biz\Partner companies\Navo\6. Departments\Richard Marlowe\Richard Hermes"
email_p = os.path.join(richard_dir, "richard_email.py")

txt = open(email_p, encoding='utf-8', errors='ignore').read()

old_headers = """        msg["From"] = f"Richard Marlowe <{EMAIL_ADDRESS}>"
        msg["To"] = to_email"""

new_headers = """        msg["From"] = f"Richard Marlowe <{EMAIL_ADDRESS}>"
        msg["Reply-To"] = f"Richard Marlowe <{EMAIL_ADDRESS}>"
        msg["To"] = to_email"""

if old_headers in txt:
    txt = txt.replace(old_headers, new_headers)
    open(email_p, "w", encoding="utf-8").write(txt)
    print("✅ Successfully added Reply-To header to richard_email.py!")
else:
    print("⚠️ Pattern not matched directly, inspecting...")
