# -*- coding: utf-8 -*-
"""
configure_oci_credentials.py — Конфигурация OCI API доступа в ~/.oci/config для управления VPS на Oracle Cloud.
"""

import os, sys, shutil

USER_HOME = r"C:\Users\Stefan"
OCI_DIR = os.path.join(USER_HOME, ".oci")
DOWNLOADS_DIR = os.path.join(USER_HOME, "Downloads")

pem_file = os.path.join(DOWNLOADS_DIR, "dr.reenforce@gmail.com-2026-08-04T05_50_04.129Z.pem")
target_pem = os.path.join(OCI_DIR, "oci_api_key.pem")
target_cfg = os.path.join(OCI_DIR, "config")

os.makedirs(OCI_DIR, exist_ok=True)

if os.path.exists(pem_file):
    shutil.copy(pem_file, target_pem)
    print(f"✅ Copied PEM key to {target_pem}")

cfg_content = """[DEFAULT]
user=ocid1.user.oc1..aaaaaaaaaohle7a7oafj3s52kgv7ojxl3yomwm6nt5relwozac5owi5lfufq
fingerprint=40:21:62:52:88:fe:30:25:f0:50:06:4a:64:79:96:ab
tenancy=ocid1.tenancy.oc1..aaaaaaaarr4jv2c5ftwaqq5xea2kt5f34val5kpsdss2e7o32byb5ybinhyq
region=uk-london-1
key_file=C:\\Users\\Stefan\\.oci\\oci_api_key.pem
"""

open(target_cfg, "w", encoding="utf-8").write(cfg_content)
print(f"✅ Created OCI Config at {target_cfg}")
