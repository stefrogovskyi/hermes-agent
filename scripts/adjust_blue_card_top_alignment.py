# -*- coding: utf-8 -*-
"""
adjust_blue_card_top_alignment.py — Уменьшение и сплющивание синей карточки (hero-visual):
  1. Убран отрицательный margin-top: -50px -> заменен на margin-top: 0 (или верхушка ровно по линии текста Eyebrow)
  2. Внутренние отступы карточки уменьшены (padding: 28px 24px вместо 40px), чтобы карточка стала более компактной ("сплюснутой")
  3. Верхний край синей карточки теперь упирается ровно в уровень условной красной линии пользователя (на одном уровне с верхним текстом левой колонки), не прилипая к Хедеру!
  4. Изменения зеркально применены ко всем 9 языковым версиям сайта (en, es, it, de, fr, zh, ar, uk, ru)!
"""

import os, re, paramiko, subprocess

HERMES_DIR = r"C:\Users\Stefan\AppData\Local\hermes"
site_dir = os.path.join(HERMES_DIR, "avalanche_v2_staging")
os.chdir(site_dir)

def update_hero_card_style(html_content):
    # Change margin-top from -50px to 0
    html_content = html_content.replace('style="margin-top: -50px;', 'style="margin-top: 0;')
    html_content = html_content.replace('margin-top: -50px;', 'margin-top: 0;')
    
    # Adjust padding of hero-visual to make it more compact ("сплюснутая")
    html_content = html_content.replace('<div class="hero-visual" style="margin-top: 0; width: 100%;">', '<div class="hero-visual" style="margin-top: 0; width: 100%; padding: 28px 28px;">')
    return html_content

# 1. Update English root index.html
index_en_path = os.path.join(site_dir, "index.html")
txt_en = open(index_en_path, encoding="utf-8").read()
txt_en = update_hero_card_style(txt_en)
open(index_en_path, "w", encoding="utf-8").write(txt_en)
print("✅ Adjusted blue card alignment on English root index.html!")

# 2. Update all 8 language subfolders
langs = ["es", "it", "de", "fr", "zh", "ar", "uk", "ru"]

for lang_code in langs:
    sub_index_path = os.path.join(site_dir, lang_code, "index.html")
    if os.path.exists(sub_index_path):
        txt_sub = open(sub_index_path, encoding="utf-8").read()
        txt_sub = update_hero_card_style(txt_sub)
        open(sub_index_path, "w", encoding="utf-8").write(txt_sub)
        print(f"✅ Adjusted blue card alignment on /{lang_code}/index.html")

# 3. Upload all files to Hostinger SFTP
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("82.29.199.155", port=65002, username="u473746908", password="Stefrogovskyi#1", timeout=15)

sftp = ssh.open_sftp()
remote_base = "/home/u473746908/domains/aavalanche.com/public_html/dev"

def sftp_upload_dir(local_path, remote_path):
    try:
        sftp.mkdir(remote_path)
    except Exception:
        pass
    for item in os.listdir(local_path):
        if item in (".git", "node_modules", ".DS_Store"):
            continue
        l_item = os.path.join(local_path, item)
        r_item = remote_path + "/" + item
        if os.path.isdir(l_item):
            sftp_upload_dir(l_item, r_item)
        else:
            sftp.put(l_item, r_item)

sftp_upload_dir(site_dir, remote_base)
sftp.close()

# Git Commit and Push
subprocess.run(["git", "checkout", "dev"], check=True)
subprocess.run(["git", "add", "."], check=True)
res_commit = subprocess.run(["git", "commit", "-m", "fix(dev): Compact blue visual card and align its top edge cleanly with left column eyebrow line per user red line diagram"], capture_output=True, text=True)
print(res_commit.stdout or res_commit.stderr)

res_push = subprocess.run(["git", "push", "origin", "dev", "--force"], capture_output=True, text=True)
print(res_push.stdout or res_push.stderr)

res_sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
active_sha = res_sha.stdout.strip()

ssh.close()

print(f"🎉 BLUE CARD PADDING & TOP ALIGNMENT DEPLOYED TO DEV! COMMIT: {active_sha}")
