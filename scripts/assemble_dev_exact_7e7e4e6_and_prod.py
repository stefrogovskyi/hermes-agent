# -*- coding: utf-8 -*-
"""
assemble_dev_exact_7e7e4e6_and_prod.py — Точная сборка dev:
  - index.html СТРОГО из коммита 7e7e4e6
  - Все остальные ресурсы и продакшн-ассеты 1-в-1 с боевого сервера (/public_html/)
"""

import os, subprocess, paramiko

site_dir = r"C:\Users\Stefan\AppData\Local\hermes\avalanche_v2_staging"
os.chdir(site_dir)

TARGET_COMMIT = "7e7e4e6"

# 1. Checkout dev branch and get index.html from commit 7e7e4e6
subprocess.run(["git", "checkout", "dev"], check=True)

res = subprocess.run(["git", "show", f"{TARGET_COMMIT}:index.html"], capture_output=True, text=True)
index_7e7e4e6_content = res.stdout

assert index_7e7e4e6_content, f"Failed to read index.html from commit {TARGET_COMMIT}!"

# Write index.html locally
open(os.path.join(site_dir, "index.html"), "w", encoding="utf-8").write(index_7e7e4e6_content)
print(f"✅ Local index.html set to exact content of commit {TARGET_COMMIT} ({len(index_7e7e4e6_content)} bytes)!")

# 2. Git Commit & Push to GitHub origin/dev
subprocess.run(["git", "add", "index.html"], check=True)
res_commit = subprocess.run(["git", "commit", "-m", f"feat(dev): Restore main page index.html to exact commit {TARGET_COMMIT}"], capture_output=True, text=True)
print(res_commit.stdout or res_commit.stderr)

res_push = subprocess.run(["git", "push", "origin", "dev", "--force"], capture_output=True, text=True)
print(res_push.stdout or res_push.stderr)

# Get current active Git commit SHA
res_sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
active_sha = res_sha.stdout.strip()

# 3. Deploy to Hostinger /public_html/dev/
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("82.29.199.155", port=65002, username="u473746908", password="Stefrogovskyi#1", timeout=15)

# First ensure all production assets from public_html/ are copied to public_html/dev/
cmd_copy_prod_assets = "cp -r /home/u473746908/domains/aavalanche.com/public_html/assets /home/u473746908/domains/aavalanche.com/public_html/images /home/u473746908/domains/aavalanche.com/public_html/favicon.png /home/u473746908/domains/aavalanche.com/public_html/logo.png /home/u473746908/domains/aavalanche.com/public_html/logo.jpeg /home/u473746908/domains/aavalanche.com/public_html/logo-full.jpeg /home/u473746908/domains/aavalanche.com/public_html/use.txt /home/u473746908/domains/aavalanche.com/public_html/dev/"
ssh.exec_command(cmd_copy_prod_assets)

# SFTP upload index.html from commit 7e7e4e6
sftp = ssh.open_sftp()
remote_index = "/home/u473746908/domains/aavalanche.com/public_html/dev/index.html"
sftp.put(os.path.join(site_dir, "index.html"), remote_index)

# Also ensure avalanche_logo.png exists in /dev/
logo_local = os.path.join(site_dir, "avalanche_logo.png")
if os.path.exists(logo_local):
    sftp.put(logo_local, "/home/u473746908/domains/aavalanche.com/public_html/dev/avalanche_logo.png")

sftp.close()

# Verify MD5 hash of index.html on Hostinger dev
stdin, stdout, stderr = ssh.exec_command("md5sum /home/u473746908/domains/aavalanche.com/public_html/dev/index.html")
print("Hostinger dev index.html MD5:\n", stdout.read().decode("utf-8"))

ssh.close()

print("🎉 DEPLOYMENT TO HOSTINGER DEV COMPLETE!")
print(f"📌 ACTIVE GIT COMMIT SHA: {active_sha}")
