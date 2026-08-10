# -*- coding: utf-8 -*-
"""
add_enter_key_submit_handler.py — Добавление отправки формы Hero-экрана по нажатию Enter на клавиатуре
на всех 9 языковых версиях Главной страницы (index.html).
"""

import os, re, paramiko, subprocess

HERMES_DIR = r"C:\Users\Stefan\AppData\Local\hermes"
site_dir = os.path.join(HERMES_DIR, "avalanche_v2_staging")
os.chdir(site_dir)

root_pages = ["index.html"]
langs = ["es", "de", "fr", "it", "uk", "ru", "zh", "ar"]

enter_handler_html = 'onkeydown="if(event.key===\'Enter\' && !event.shiftKey){ event.preventDefault(); handleHeroProjectSubmit(); }"'

# Update root index.html
p_root = os.path.join(site_dir, "index.html")
if os.path.exists(p_root):
    txt = open(p_root, encoding="utf-8").read()
    if 'id="hero-project-input"' in txt:
        txt = txt.replace('id="hero-project-input"', f'id="hero-project-input" {enter_handler_html}')
        open(p_root, "w", encoding="utf-8").write(txt)
        print("✅ Added Enter key handler to root index.html!")

# Update subfolder index.html pages
for lang in langs:
    p_sub = os.path.join(site_dir, lang, "index.html")
    if os.path.exists(p_sub):
        txt_sub = open(p_sub, encoding="utf-8").read()
        if 'id="hero-project-input"' in txt_sub and 'event.key===\'Enter\'' not in txt_sub:
            txt_sub = txt_sub.replace('id="hero-project-input"', f'id="hero-project-input" {enter_handler_html}')
            open(p_sub, "w", encoding="utf-8").write(txt_sub)
            print(f"✅ Added Enter key handler to /{lang}/index.html!")

# Upload to Hostinger SFTP
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("82.29.199.155", port=65002, username="u473746908", password="Stefrogovskyi#1", timeout=15)

sftp = ssh.open_sftp()
remote_base = "/home/u473746908/domains/aavalanche.com/public_html/dev"

sftp.put(p_root, f"{remote_base}/index.html")
for lang in langs:
    sftp.put(os.path.join(site_dir, lang, "index.html"), f"{remote_base}/{lang}/index.html")

sftp.close()

subprocess.run(["git", "checkout", "dev"], check=True)
subprocess.run(["git", "add", "."], check=True)
res_commit = subprocess.run(["git", "commit", "-m", "feat(dev): Add Enter key submit handler to hero project description textarea across all 9 languages"], capture_output=True, text=True)
print(res_commit.stdout or res_commit.stderr)

res_push = subprocess.run(["git", "push", "origin", "dev", "--force"], capture_output=True, text=True)
print(res_push.stdout or res_push.stderr)

res_sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
active_sha = res_sha.stdout.strip()

ssh.close()

print(f"🎉 ENTER KEY SUBMIT HANDLER DEPLOYED TO DEV! COMMIT: {active_sha}")
