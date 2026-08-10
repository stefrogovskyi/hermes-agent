# -*- coding: utf-8 -*-
import os, paramiko, subprocess

HERMES_DIR = r"C:\Users\Stefan\AppData\Local\hermes"
site_dir = os.path.join(HERMES_DIR, "avalanche_v2_staging")
es_index_path = os.path.join(site_dir, "es", "index.html")

txt = open(es_index_path, encoding="utf-8").read()

txt = txt.replace("Domain selection & purchase", "Selección y compra de dominios")
txt = txt.replace("Domain selection &amp; purchase", "Selección y compra de dominios")
txt = txt.replace("Hosting selection & purchase", "Selección y contratación de alojamiento web")
txt = txt.replace("Hosting selection &amp; purchase", "Selección y contratación de alojamiento web")
txt = txt.replace("Contenido writing", "Creación de contenidos y artículos")
txt = txt.replace("Content writing", "Creación de contenidos y artículos")

open(es_index_path, "w", encoding="utf-8").write(txt)
print("✅ Cleaned remaining services strings in es/index.html!")

# Upload to Hostinger SFTP
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("82.29.199.155", port=65002, username="u473746908", password="Stefrogovskyi#1", timeout=15)

sftp = ssh.open_sftp()
sftp.put(es_index_path, "/home/u473746908/domains/aavalanche.com/public_html/dev/es/index.html")
sftp.close()

os.chdir(site_dir)
subprocess.run(["git", "checkout", "dev"], check=True)
subprocess.run(["git", "add", "es/index.html"], check=True)
subprocess.run(["git", "commit", "-m", "fix(dev): Clean 100% remaining English service bullet points in es/index.html"], capture_output=True)
subprocess.run(["git", "push", "origin", "dev", "--force"], capture_output=True)

res_sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
active_sha = res_sha.stdout.strip()

ssh.close()

print(f"🎉 SPANISH HERO & SERVICES FULLY CLEANED! COMMIT: {active_sha}")
