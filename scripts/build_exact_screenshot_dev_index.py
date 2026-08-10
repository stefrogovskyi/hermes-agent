# -*- coding: utf-8 -*-
"""
build_exact_screenshot_dev_index.py — Точная сборка главной страницы на ветке dev:
  - Хедер 1-в-1 как на скриншоте 1 (белый фон, логотип AA, ссылки Services/Pricing/About/Contact, кнопка выбора языка Union Jack + EN + chevron v)
  - Тело страницы из avalanche-v2-preview.surge.sh
  - Футер 1-в-1 как на скриншоте 2 (темный фон #0F172A, логотип AA Avalanche Agency, бостонский адрес 225 Franklin St, info@aavalanche.com, телефон +1 414 554-0638, LinkedIn, copyright 2026)
"""

import os, re, subprocess, paramiko, py_compile

HERMES_DIR = r"C:\Users\Stefan\AppData\Local\hermes"
site_dir = os.path.join(HERMES_DIR, "avalanche_v2_staging")
preview_file = os.path.join(HERMES_DIR, "surge_preview.html")

if not os.path.exists(preview_file):
    preview_file = "surge_preview.html"

preview_html = open(preview_file, encoding="utf-8").read()

# Extract CSS styles from surge_preview.html
style_match = re.search(r'(<style>.*?</style>)', preview_html, re.DOTALL)
preview_style = style_match.group(1) if style_match else ""

# Extract main body sections from surge_preview.html
hero_match = re.search(r'(<header class="hero">.*?</header>)', preview_html, re.DOTALL)
hero_html = hero_match.group(1) if hero_match else ""

sections = re.findall(r'(<section.*?>.*?</section>)', preview_html, re.DOTALL)
main_sections_html = "\n\n".join(sections)
main_body_combined = f"{hero_html}\n\n{main_sections_html}"

# 1. EXACT HEADER FROM SCREENSHOT 1
exact_header_html = """
<nav style="position: sticky; top: 0; z-index: 1000; background: #FFFFFF; border-bottom: 1px solid #E2E8F0; font-family: 'Inter', system-ui, sans-serif;">
  <div class="wrap nav-in" style="display: flex; align-items: center; justify-content: space-between; padding: 14px 24px; max-width: 1180px; margin: 0 auto;">
    
    <!-- Logo Left -->
    <div class="brand">
      <a href="/index.html" style="text-decoration: none; display: flex; align-items: center; gap: 10px;">
        <img src="/avalanche_logo.png" alt="Avalanche Agency" style="height: 36px; width: auto;" />
      </a>
    </div>

    <!-- Center Navigation Links -->
    <div class="desktop-nav" style="display: flex; align-items: center; gap: 32px;">
      <a href="/services.html" style="color: #334155; text-decoration: none; font-weight: 600; font-size: 15px;">Services</a>
      <a href="/pricing.html" style="color: #334155; text-decoration: none; font-weight: 600; font-size: 15px;">Pricing</a>
      <a href="/about.html" style="color: #334155; text-decoration: none; font-weight: 600; font-size: 15px;">About</a>
      <a href="/contact.html" style="color: #334155; text-decoration: none; font-weight: 600; font-size: 15px;">Contact</a>
    </div>

    <!-- Language Selector Pill Button Right -->
    <div class="desktop-nav" style="display: flex; align-items: center; gap: 16px;">
      <div style="position: relative; display: inline-block;">
        <button onclick="toggleLangDropdown()" style="display: flex; align-items: center; gap: 8px; background: #F8FAFC; color: #0F172A; border: 1px solid #E2E8F0; padding: 7px 16px; border-radius: 20px; font-size: 14px; font-weight: 700; cursor: pointer; outline: none;">
          <svg style="width:20px;height:14px;border-radius:2px;vertical-align:middle;display:inline-block;" viewBox="0 0 60 40"><rect fill="#012169" width="60" height="40"/><path d="M0,0 L60,40 M60,0 L0,40" stroke="#fff" stroke-width="6"/><path d="M0,0 L60,40 M60,0 L0,40" stroke="#C8102E" stroke-width="4"/><path d="M30,0 V40 M0,20 H60" stroke="#fff" stroke-width="10"/><path d="M30,0 V40 M0,20 H60" stroke="#C8102E" stroke-width="6"/></svg>
          <span>EN</span>
          <span style="font-size: 10px; color: #64748B;">▼</span>
        </button>

        <div id="lang-menu" style="display: none; position: absolute; right: 0; top: 46px; background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.12); padding: 8px; width: 180px; z-index: 1001;">
          <div onclick="navigateToLang('en')" style="display:flex;align-items:center;gap:10px;padding:8px 12px;cursor:pointer;border-radius:6px;" onmouseover="this.style.background='#F1F5F9'" onmouseout="this.style.background='transparent'">
            <svg style="width:20px;height:14px;border-radius:2px;" viewBox="0 0 60 40"><rect fill="#012169" width="60" height="40"/><path d="M0,0 L60,40 M60,0 L0,40" stroke="#fff" stroke-width="6"/><path d="M0,0 L60,40 M60,0 L0,40" stroke="#C8102E" stroke-width="4"/><path d="M30,0 V40 M0,20 H60" stroke="#fff" stroke-width="10"/><path d="M30,0 V40 M0,20 H60" stroke="#C8102E" stroke-width="6"/></svg>
            <span style="font-size:14px;font-weight:600;color:#0F172A;">English (EN)</span>
          </div>
          <div onclick="navigateToLang('es')" style="display:flex;align-items:center;gap:10px;padding:8px 12px;cursor:pointer;border-radius:6px;" onmouseover="this.style.background='#F1F5F9'" onmouseout="this.style.background='transparent'">
            <svg style="width:20px;height:14px;border-radius:2px;" viewBox="0 0 60 40"><rect fill="#AA151B" width="60" height="40"/><rect fill="#F1BF00" y="10" width="60" height="20"/></svg>
            <span style="font-size:14px;font-weight:600;color:#0F172A;">Español (ES)</span>
          </div>
          <div onclick="navigateToLang('it')" style="display:flex;align-items:center;gap:10px;padding:8px 12px;cursor:pointer;border-radius:6px;" onmouseover="this.style.background='#F1F5F9'" onmouseout="this.style.background='transparent'">
            <svg style="width:20px;height:14px;border-radius:2px;" viewBox="0 0 60 40"><rect fill="#009246" width="20" height="40"/><rect fill="#fff" x="20" width="20" height="40"/><rect fill="#CE2B37" x="40" width="20" height="40"/></svg>
            <span style="font-size:14px;font-weight:600;color:#0F172A;">Italiano (IT)</span>
          </div>
          <div onclick="navigateToLang('fr')" style="display:flex;align-items:center;gap:10px;padding:8px 12px;cursor:pointer;border-radius:6px;" onmouseover="this.style.background='#F1F5F9'" onmouseout="this.style.background='transparent'">
            <svg style="width:20px;height:14px;border-radius:2px;" viewBox="0 0 60 40"><rect fill="#002395" width="20" height="40"/><rect fill="#fff" x="20" width="20" height="40"/><rect fill="#ED2939" x="40" width="20" height="40"/></svg>
            <span style="font-size:14px;font-weight:600;color:#0F172A;">Français (FR)</span>
          </div>
          <div onclick="navigateToLang('de')" style="display:flex;align-items:center;gap:10px;padding:8px 12px;cursor:pointer;border-radius:6px;" onmouseover="this.style.background='#F1F5F9'" onmouseout="this.style.background='transparent'">
            <svg style="width:20px;height:14px;border-radius:2px;" viewBox="0 0 60 40"><rect fill="#000" width="60" height="13.33"/><rect fill="#DD0000" y="13.33" width="60" height="13.33"/><rect fill="#FFCE00" y="26.66" width="60" height="13.33"/></svg>
            <span style="font-size:14px;font-weight:600;color:#0F172A;">Deutsch (DE)</span>
          </div>
          <div onclick="navigateToLang('zh')" style="display:flex;align-items:center;gap:10px;padding:8px 12px;cursor:pointer;border-radius:6px;" onmouseover="this.style.background='#F1F5F9'" onmouseout="this.style.background='transparent'">
            <svg style="width:20px;height:14px;border-radius:2px;" viewBox="0 0 60 40"><rect fill="#DE2910" width="60" height="40"/><g fill="#FFDE00"><polygon points="10,6 11.5,11 17,11 12.7,14.5 14.2,19.5 10,16 5.8,19.5 7.3,14.5 3,11 8.5,11"/></g></svg>
            <span style="font-size:14px;font-weight:600;color:#0F172A;">中文 (ZH)</span>
          </div>
          <div onclick="navigateToLang('ar')" style="display:flex;align-items:center;gap:10px;padding:8px 12px;cursor:pointer;border-radius:6px;" onmouseover="this.style.background='#F1F5F9'" onmouseout="this.style.background='transparent'">
            <svg style="width:20px;height:14px;border-radius:2px;" viewBox="0 0 60 40"><rect fill="#007A3D" width="60" height="13.33"/><rect fill="#fff" y="13.33" width="60" height="13.33"/><rect fill="#000" y="26.66" width="60" height="13.33"/><polygon fill="#CE1126" points="0,0 0,40 20,20"/></svg>
            <span style="font-size:14px;font-weight:600;color:#0F172A;">العربية (AR)</span>
          </div>
          <div onclick="navigateToLang('uk')" style="display:flex;align-items:center;gap:10px;padding:8px 12px;cursor:pointer;border-radius:6px;" onmouseover="this.style.background='#F1F5F9'" onmouseout="this.style.background='transparent'">
            <svg style="width:20px;height:14px;border-radius:2px;" viewBox="0 0 60 40"><rect fill="#005BBB" width="60" height="20"/><rect fill="#FFD500" y="20" width="60" height="20"/></svg>
            <span style="font-size:14px;font-weight:600;color:#0F172A;">Українська (UK)</span>
          </div>
          <div onclick="navigateToLang('ru')" style="display:flex;align-items:center;gap:10px;padding:8px 12px;cursor:pointer;border-radius:6px;" onmouseover="this.style.background='#F1F5F9'" onmouseout="this.style.background='transparent'">
            <svg style="width:20px;height:14px;border-radius:2px;" viewBox="0 0 60 40"><rect fill="#fff" width="60" height="13.33"/><rect fill="#0039A6" y="13.33" width="60" height="13.33"/><rect fill="#D52B1E" y="26.66" width="60" height="13.33"/></svg>
            <span style="font-size:14px;font-weight:600;color:#0F172A;">Русский (RU)</span>
          </div>
        </div>
      </div>
    </div>

  </div>
</nav>
"""

# 2. EXACT FOOTER FROM SCREENSHOT 2
exact_footer_html = """
<footer style="background: #0F172A; color: #94A3B8; padding: 50px 0 30px; font-family: 'Inter', system-ui, sans-serif; border-top: 1px solid #1E293B;">
  <div style="max-width: 1180px; margin: 0 auto; padding: 0 24px;">
    
    <!-- Top Section -->
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 20px; padding-bottom: 30px;">
      
      <!-- Logo Left -->
      <div style="display: flex; align-items: center; gap: 12px;">
        <img src="/avalanche_logo.png" alt="Avalanche Agency" style="height: 38px; width: auto; border-radius: 8px;" />
        <span style="color: #FFFFFF; font-weight: 800; font-size: 20px; letter-spacing: -0.02em;">Avalanche Agency</span>
      </div>

      <!-- Address Center -->
      <div style="display: flex; align-items: center; gap: 8px; color: #94A3B8; font-size: 14px;">
        <svg style="width: 16px; height: 16px; fill: currentColor;" viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
        <span>225 Franklin Street, Suite 2600, Boston, MA 02110, USA</span>
      </div>

      <!-- Contact Right -->
      <div style="display: flex; align-items: center; gap: 20px; color: #94A3B8; font-size: 14px;">
        <!-- LinkedIn -->
        <a href="https://linkedin.com" target="_blank" style="color: #FFFFFF; text-decoration: none; display: flex; align-items: center;">
          <svg style="width: 18px; height: 18px; fill: currentColor;" viewBox="0 0 24 24"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.46 10.9v8.37H9.25V10.9H6.46M7.86 6.74a1.6 1.6 0 1 0 0 3.2 1.6 1.6 0 0 0 0-3.2z"/></svg>
        </a>
        <!-- Email -->
        <a href="mailto:info@aavalanche.com" style="color: #94A3B8; text-decoration: none;">info@aavalanche.com</a>
        <!-- Phone -->
        <div style="display: flex; align-items: center; gap: 6px;">
          <svg style="width: 16px; height: 16px; fill: currentColor;" viewBox="0 0 24 24"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
          <a href="tel:+14145540638" style="color: #94A3B8; text-decoration: none;">+1 (414) 554-0638</a>
        </div>
      </div>

    </div>

    <!-- Divider Line -->
    <div style="border-top: 1px solid #1E293B; margin-bottom: 24px;"></div>

    <!-- Bottom Section -->
    <div style="text-align: center; font-size: 13px; color: #64748B;">
      2026 Avalanche Agency. All rights reserved.
    </div>

  </div>
</footer>
"""

# JS for Language Dropdown
lang_script = """
<script>
  function toggleLangDropdown() {
    var menu = document.getElementById('lang-menu');
    if (menu) {
      menu.style.display = (menu.style.display === 'none' || menu.style.display === '') ? 'block' : 'none';
    }
  }

  function navigateToLang(langCode) {
    var currentPath = window.location.pathname;
    var cleanPath = currentPath.replace(/^\/(es|it|de|fr|zh|ar|uk|ru)\//, '/');
    if (cleanPath === '' || cleanPath === '/') cleanPath = '/index.html';

    if (langCode === 'en') {
      window.location.href = cleanPath;
    } else {
      window.location.href = '/' + langCode + cleanPath;
    }
  }

  document.addEventListener('click', function(e) {
    var menu = document.getElementById('lang-menu');
    var btn = e.target.closest('button');
    if (menu && menu.style.display === 'block' && (!btn || !btn.onclick || btn.onclick.toString().indexOf('toggleLangDropdown') === -1)) {
      if (!e.target.closest('#lang-menu')) {
        menu.style.display = 'none';
      }
    }
  });
</script>
"""

# Assemble new index.html
new_index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Avalanche Agency — Premium Web & Marketing</title>
  <meta name="description" content="Premium Web Solutions for Modern Businesses. Custom web development, infrastructure, content, and growth marketing.">
  <link rel="icon" type="image/png" href="/avalanche_logo.png">
  <link rel="shortcut icon" href="/avalanche_logo.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  {preview_style}
</head>
<body>

{exact_header_html}

<!-- MAIN BODY CONTENT FROM AVALANCHE-V2-PREVIEW.SURGE.SH -->
<main>
{main_body_combined}
</main>

{exact_footer_html}

{lang_script}
</body>
</html>
"""

# Write index.html
open(os.path.join(site_dir, "index.html"), "w", encoding="utf-8").write(new_index_html)
print(f"✅ Successfully written index.html with EXACT Screenshot 1 Header + Main Body + EXACT Screenshot 2 Footer ({len(new_index_html)} bytes)!")

# Commit and Push to GitHub origin/dev
os.chdir(site_dir)
subprocess.run(["git", "checkout", "dev"], check=True)
subprocess.run(["git", "add", "index.html"], check=True)
res_commit = subprocess.run(["git", "commit", "-m", "feat(dev): Update main body from surge preview, keeping exact white header (Screenshot 1) and exact dark footer (Screenshot 2) untouched"], capture_output=True, text=True)
print(res_commit.stdout or res_commit.stderr)

res_push = subprocess.run(["git", "push", "origin", "dev"], capture_output=True, text=True)
print(res_push.stdout or res_push.stderr)

# Upload to Hostinger via SFTP
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("82.29.199.155", port=65002, username="u473746908", password="Stefrogovskyi#1", timeout=15)

sftp = ssh.open_sftp()
remote_index = "/home/u473746908/domains/aavalanche.com/public_html/dev/index.html"
sftp.put(os.path.join(site_dir, "index.html"), remote_index)
sftp.close()

# Get current Git commit SHA
res_sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
active_sha = res_sha.stdout.strip()

ssh.close()
print(f"🎉 DEPLOYED TO HOSTINGER: {remote_index}")
print(f"📌 ACTIVE GIT COMMIT SHA: {active_sha}")
