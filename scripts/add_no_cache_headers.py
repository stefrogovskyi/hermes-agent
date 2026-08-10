# -*- coding: utf-8 -*-
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("82.29.199.155", port=65002, username="u473746908", password="Stefrogovskyi#1", timeout=15)

htaccess_no_cache = """<IfModule mod_rewrite.c>
  RewriteEngine On
  Header set X-Robots-Tag "noindex, nofollow"
  Header set Cache-Control "no-cache, no-store, must-revalidate"
  Header set Pragma "no-cache"
  Header set Expires "0"

  # Direct static page mappings
  RewriteRule ^contact(\\.html)?$ contact.html [L,QSA]
  RewriteRule ^about(\\.html)?$ about.html [L,QSA]
  RewriteRule ^pricing(\\.html)?$ pricing.html [L,QSA]
  RewriteRule ^services(\\.html)?$ services.html [L,QSA]

  # Allow direct access to physical static files
  RewriteCond %{REQUEST_FILENAME} -f [OR]
  RewriteCond %{REQUEST_FILENAME} -d
  RewriteRule ^ - [L]
</IfModule>
"""

ssh.exec_command('echo "' + htaccess_no_cache + '" > /home/u473746908/domains/aavalanche.com/public_html/dev/.htaccess')
ssh.close()

print("✅ Added strict no-cache headers to /dev/.htaccess!")
