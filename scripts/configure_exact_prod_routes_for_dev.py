# -*- coding: utf-8 -*-
"""
configure_exact_prod_routes_for_dev.py — Настройка навигационных ссылок на главной dev (index.html)
на прямые роуты /dev/services, /dev/pricing, /dev/about, /dev/contact
с перенаправлением .htaccess, чтобы React-приложение отображало ТОЧНЫЕ ПРОДАКШН-СТРАНИЦЫ.
"""

import os, re, subprocess, paramiko, py_compile

site_dir = r"C:\Users\Stefan\AppData\Local\hermes\avalanche_v2_staging"
os.chdir(site_dir)
index_path = os.path.join(site_dir, "index.html")

txt = open(index_path, encoding="utf-8").read()

# Update navigation links to point to React production routes /dev/services, /dev/pricing, /dev/about, /dev/contact
txt = txt.replace('href="services.html"', 'href="/dev/services"')
txt = txt.replace('href="pricing.html"', 'href="/dev/pricing"')
txt = txt.replace('href="about.html"', 'href="/dev/about"')
txt = txt.replace('href="contact.html"', 'href="/dev/contact"')
txt = txt.replace('href="/services.html"', 'href="/dev/services"')
txt = txt.replace('href="/pricing.html"', 'href="/dev/pricing"')
txt = txt.replace('href="/about.html"', 'href="/dev/about"')
txt = txt.replace('href="/contact.html"', 'href="/dev/contact"')

open(index_path, "w", encoding="utf-8").write(txt)
print(f"✅ Updated navigation links in index.html to /dev/services, /dev/pricing, /dev/about, /dev/contact!")

# Commit and Push to GitHub origin/dev
subprocess.run(["git", "checkout", "dev"], check=True)
subprocess.run(["git", "add", "index.html"], check=True)
res_commit = subprocess.run(["git", "commit", "-m", "fix(dev): Point menu links to exact React production routes (/dev/services, /dev/pricing, /dev/about, /dev/contact)"], capture_output=True, text=True)
print(res_commit.stdout or res_commit.stderr)

res_push = subprocess.run(["git", "push", "origin", "dev", "--force"], capture_output=True, text=True)
print(res_push.stdout or res_push.stderr)

# Get current Git commit SHA
res_sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
active_sha = res_sha.stdout.strip()

# Deploy to Hostinger via SSH/SFTP
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("82.29.199.155", port=65002, username="u473746908", password="Stefrogovskyi#1", timeout=15)

# Upload updated index.html
sftp = ssh.open_sftp()
sftp.put(os.path.join(site_dir, "index.html"), "/home/u473746908/domains/aavalanche.com/public_html/dev/index.html")
sftp.close()

# Remove static html files in /dev/ so they don't override React SPA routes
ssh.exec_command("rm -f /home/u473746908/domains/aavalanche.com/public_html/dev/services.html /home/u473746908/domains/aavalanche.com/public_html/dev/pricing.html /home/u473746908/domains/aavalanche.com/public_html/dev/about.html /home/u473746908/domains/aavalanche.com/public_html/dev/contact.html")

# Configure SPA .htaccess in /dev/.htaccess
htaccess_spa = """<IfModule mod_rewrite.c>
  RewriteEngine On
  Header set X-Robots-Tag "noindex, nofollow"
  RewriteBase /dev/
  
  # Allow direct access to physical static assets and images
  RewriteCond %{REQUEST_FILENAME} -f [OR]
  RewriteCond %{REQUEST_FILENAME} -d
  RewriteRule ^ - [L]

  # Rewrite all React routes (/dev/services, /dev/pricing, /dev/about, /dev/contact) to /dev/index.html
  RewriteRule . /dev/index.html [L]
</IfModule>
"""

ssh.exec_command('echo "' + htaccess_spa + '" > /home/u473746908/domains/aavalanche.com/public_html/dev/.htaccess')

ssh.close()

print(f"🎉 DEV DEPLOYED WITH EXACT PROD REACT ROUTES!")
print(f"📌 ACTIVE GIT COMMIT SHA: {active_sha}")
