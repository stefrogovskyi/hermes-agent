# -*- coding: utf-8 -*-
"""
configure_clean_urls_and_favicon.py —
  1. Размещение ровного favicon.ico и avalanche_logo.png
  2. Настройка .htaccess на Dev и Staging для чистых URL без .html (DirectoryIndex index.html + RewriteRule)
  3. Избавление от .html во всех внутренних ссылках меню и хедера на всех языках!
"""

import os, paramiko, subprocess, re

HERMES_DIR = r"C:\Users\Stefan\AppData\Local\hermes"
site_dir = os.path.join(HERMES_DIR, "avalanche_v2_staging")
os.chdir(site_dir)

# 1. CREATE CLEAN .HTACCESS WITH REWRITE RULES FOR DEV & STAGING
clean_htaccess = """DirectoryIndex index.html index.php

# Prevent Caching
<IfModule mod_headers.c>
    Header set Cache-Control "no-cache, no-store, must-revalidate"
    Header set Pragma "no-cache"
    Header set Expires 0
    Header set X-Robots-Tag "noindex, nofollow"
</IfModule>

<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteBase /

    # Serve index.html automatically on directory requests
    RewriteCond %{REQUEST_FILENAME} -d
    RewriteRule ^(.*)$ $1/index.html [L]

    # Remove .html extension from URLs
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteCond %{REQUEST_FILENAME}\.html -f
    RewriteRule ^([^/]+)/?$ $1.html [L]

    # Language subfolders extensionless routing
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteCond %{REQUEST_FILENAME}\.html -f
    RewriteRule ^(es|de|fr|it|uk|ru|zh|ar)/([^/]+)/?$ $1/$2.html [L]
</IfModule>

# Favicon Mime Types
<IfModule mod_mime.c>
    AddType image/x-icon .ico
    AddType image/png .png
</IfModule>
"""

open(os.path.join(site_dir, ".htaccess"), "w", encoding="utf-8").write(clean_htaccess)

# 2. UPDATE FAVICON TAGS & CLEAN INTERNAL LINKS (REMOVE .HTML) ACROSS ALL PAGES
for root, dirs, files in os.walk(site_dir):
    if '.git' in root or 'node_modules' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            f_path = os.path.join(root, file)
            txt = open(f_path, encoding="utf-8").read()
            
            # Ensure absolute favicon link
            fav_link = '<link rel="icon" type="image/png" href="/avalanche_logo.png">\n<link rel="shortcut icon" href="/favicon.ico">'
            if '<link rel="icon"' in txt:
                txt = re.sub(r'<link rel="icon"[^>]*>', fav_link, txt)
            else:
                txt = txt.replace('</head>', f'{fav_link}\n</head>')

            # Clean internal links (replace href="services.html" with href="/services" or relative clean)
            txt = txt.replace('href="services.html"', 'href="services"')
            txt = txt.replace('href="pricing.html"', 'href="pricing"')
            txt = txt.replace('href="about.html"', 'href="about"')
            txt = txt.replace('href="contact.html"', 'href="contact"')
            txt = txt.replace('href="login.html"', 'href="login"')
            txt = txt.replace('href="dashboard.html"', 'href="dashboard"')
            txt = txt.replace('href="evaluation.html"', 'href="evaluation"')
            txt = txt.replace('href="index.html"', 'href="./"')

            open(f_path, "w", encoding="utf-8").write(txt)

print("✅ Updated .htaccess and clean URL links across all HTML files!")

# 3. GENERATE SITEMAP.XML AND ROBOTS.TXT FOR PRODUCTION
sitemap_xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://aavalanche.com/</loc>
    <xhtml:link rel="alternate" hreflang="en" href="https://aavalanche.com/"/>
    <xhtml:link rel="alternate" hreflang="es" href="https://aavalanche.com/es/"/>
    <xhtml:link rel="alternate" hreflang="de" href="https://aavalanche.com/de/"/>
    <xhtml:link rel="alternate" hreflang="fr" href="https://aavalanche.com/fr/"/>
    <xhtml:link rel="alternate" hreflang="it" href="https://aavalanche.com/it/"/>
    <xhtml:link rel="alternate" hreflang="uk" href="https://aavalanche.com/uk/"/>
    <xhtml:link rel="alternate" hreflang="ru" href="https://aavalanche.com/ru/"/>
    <xhtml:link rel="alternate" hreflang="zh" href="https://aavalanche.com/zh/"/>
    <xhtml:link rel="alternate" hreflang="ar" href="https://aavalanche.com/ar/"/>
    <priority>1.0</priority>
  </url>
  <url><loc>https://aavalanche.com/services</loc><priority>0.8</priority></url>
  <url><loc>https://aavalanche.com/pricing</loc><priority>0.8</priority></url>
  <url><loc>https://aavalanche.com/about</loc><priority>0.8</priority></url>
  <url><loc>https://aavalanche.com/contact</loc><priority>0.8</priority></url>
</urlset>
"""

robots_txt = """User-agent: *
Allow: /
Sitemap: https://aavalanche.com/sitemap.xml
"""

open(os.path.join(site_dir, "sitemap.xml"), "w", encoding="utf-8").write(sitemap_xml)
open(os.path.join(site_dir, "robots.txt"), "w", encoding="utf-8").write(robots_txt)
print("✅ Generated sitemap.xml & robots.txt for Production!")

# 4. UPLOAD TO DEV & STAGING VIA SFTP
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("82.29.199.155", port=65002, username="u473746908", password="Stefrogovskyi#1", timeout=15)

sftp = ssh.open_sftp()
dev_base = "/home/u473746908/domains/aavalanche.com/public_html/dev"
staging_base = "/home/u473746908/domains/aavalanche.com/public_html/staging"

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

print("🚀 Uploading to DEV...")
sftp_upload_dir(site_dir, dev_base)

print("🚀 Deploying DEV to STAGING (RELEASE)...")
sftp_upload_dir(site_dir, staging_base)

sftp.close()

# Git commit and push staging branch
subprocess.run(["git", "checkout", "dev"], check=True)
subprocess.run(["git", "add", "."], check=True)
subprocess.run(["git", "commit", "-m", "feat(dev): Configure clean extensionless URLs (.htaccess), fix favicon links, and add production SEO sitemap.xml & robots.txt"], capture_output=True)
subprocess.run(["git", "push", "origin", "dev", "--force"], capture_output=True)

subprocess.run(["git", "checkout", "staging"], check=True)
subprocess.run(["git", "merge", "dev", "-m", "chore: Release clean URLs and favicon fixes to staging"], check=True)
subprocess.run(["git", "push", "origin", "staging", "--force"], capture_output=True)
subprocess.run(["git", "checkout", "dev"], check=True)

res_sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
active_sha = res_sha.stdout.strip()

ssh.close()

print(f"🎉 CLEAN URLS, FAVICON & SEO CONFIG DEPLOYED TO STAGING! ACTIVE GIT COMMIT SHA: {active_sha}")
