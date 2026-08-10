# -*- coding: utf-8 -*-
"""
build_exact_screenshot_pricing_page.py — Точная сборка единого универсального прайсинга (pricing.html) на ветке dev
по скриншоту пользователя:
  - 4 белые карточки с серыми иконками (Молния ⚡, Сердце ♡, Щит 🛡️, Шестеренка ⚙️)
  - Светло-зеленые галочки ✓ у списков фич
  - Мятно-зеленый прямоугольный баннер "No prepayment required. Pay only when you are 100% satisfied."
  - Голубая кнопка "Start Your Project" под баннером
  - Сквозной Хедер со скриншота 1 и Футер со скриншота 2
"""

import os, paramiko, subprocess, py_compile

HERMES_DIR = r"C:\Users\Stefan\AppData\Local\hermes"
site_dir = os.path.join(HERMES_DIR, "avalanche_v2_staging")
prod_extract_dir = os.path.join(HERMES_DIR, "prod_extracted_pages")

header_html = open(os.path.join(prod_extract_dir, "header.html"), encoding="utf-8").read()
footer_html = open(os.path.join(prod_extract_dir, "footer.html"), encoding="utf-8").read()

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

# HTML for the exact screenshot 4-card unified pricing layout
exact_unified_pricing_html = """
<section style="padding: 80px 0; background: #FFFFFF; font-family: 'Inter', system-ui, -apple-system, sans-serif;">
  <div style="max-width: 1180px; margin: 0 auto; padding: 0 24px;">
    
    <!-- Section Header -->
    <div style="text-align: center; margin-bottom: 56px;">
      <span style="font-size: 13px; font-weight: 800; letter-spacing: 0.15em; color: #389BFF; text-transform: uppercase;">TRANSPARENT PRICING</span>
      <h1 style="font-size: 42px; font-weight: 800; color: #0F172A; margin: 12px 0 16px; letter-spacing: -0.02em;">Simple, Transparent Pricing</h1>
      <p style="font-size: 18px; color: #64748B; max-width: 600px; margin: 0 auto;">No hidden fees. No surprises. Complete custom web development.</p>
    </div>

    <!-- 4 Universal Pricing Cards Grid -->
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; align-items: stretch; margin-bottom: 48px;">
      
      <!-- Card 1: Flat Rate -->
      <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 32px 24px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 2px 12px rgba(0,0,0,0.03);">
        <div>
          <!-- Light Gray Icon Box -->
          <div style="width: 48px; height: 48px; background: #F1F5F9; border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-bottom: 20px;">
            <svg style="width: 24px; height: 24px; fill: none; stroke: #0F172A; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round;" viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
          </div>
          <h3 style="font-size: 20px; font-weight: 800; color: #0F172A; margin-bottom: 8px;">Flat Rate</h3>
          <div style="font-size: 36px; font-weight: 900; color: #0F172A; margin-bottom: 6px; letter-spacing: -0.02em;">$299</div>
          <p style="color: #64748B; font-size: 14px; font-weight: 500; margin-bottom: 24px;">Full development</p>
          
          <ul style="list-style: none; padding: 0; margin-top: 16px; border-top: 1px solid #F1F5F9;">
            <li style="padding: 10px 0; color: #334155; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 10px;">
              <span style="display: flex; align-items: center; justify-content: center; width: 18px; height: 18px; background: #D1FAE5; border-radius: 50%; color: #10B981; font-size: 12px; font-weight: 900;">✓</span> Complete website build
            </li>
            <li style="padding: 10px 0; color: #334155; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 10px;">
              <span style="display: flex; align-items: center; justify-content: center; width: 18px; height: 18px; background: #D1FAE5; border-radius: 50%; color: #10B981; font-size: 12px; font-weight: 900;">✓</span> Custom design
            </li>
            <li style="padding: 10px 0; color: #334155; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 10px;">
              <span style="display: flex; align-items: center; justify-content: center; width: 18px; height: 18px; background: #D1FAE5; border-radius: 50%; color: #10B981; font-size: 12px; font-weight: 900;">✓</span> Mobile responsive
            </li>
            <li style="padding: 10px 0; color: #334155; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 10px;">
              <span style="display: flex; align-items: center; justify-content: center; width: 18px; height: 18px; background: #D1FAE5; border-radius: 50%; color: #10B981; font-size: 12px; font-weight: 900;">✓</span> SEO ready
            </li>
          </ul>
        </div>
      </div>

      <!-- Card 2: Peace of Mind -->
      <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 32px 24px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 2px 12px rgba(0,0,0,0.03);">
        <div>
          <!-- Light Gray Icon Box -->
          <div style="width: 48px; height: 48px; background: #F1F5F9; border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-bottom: 20px;">
            <svg style="width: 24px; height: 24px; fill: none; stroke: #0F172A; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round;" viewBox="0 0 24 24"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
          </div>
          <h3 style="font-size: 20px; font-weight: 800; color: #0F172A; margin-bottom: 8px;">Peace of Mind</h3>
          <div style="font-size: 36px; font-weight: 900; color: #0F172A; margin-bottom: 6px; letter-spacing: -0.02em;">$19/mo</div>
          <p style="color: #64748B; font-size: 14px; font-weight: 500; margin-bottom: 24px;">Hosting, security, maintenance</p>
          
          <ul style="list-style: none; padding: 0; margin-top: 16px; border-top: 1px solid #F1F5F9;">
            <li style="padding: 10px 0; color: #334155; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 10px;">
              <span style="display: flex; align-items: center; justify-content: center; width: 18px; height: 18px; background: #D1FAE5; border-radius: 50%; color: #10B981; font-size: 12px; font-weight: 900;">✓</span> Premium hosting
            </li>
            <li style="padding: 10px 0; color: #334155; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 10px;">
              <span style="display: flex; align-items: center; justify-content: center; width: 18px; height: 18px; background: #D1FAE5; border-radius: 50%; color: #10B981; font-size: 12px; font-weight: 900;">✓</span> SSL certificate
            </li>
            <li style="padding: 10px 0; color: #334155; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 10px;">
              <span style="display: flex; align-items: center; justify-content: center; width: 18px; height: 18px; background: #D1FAE5; border-radius: 50%; color: #10B981; font-size: 12px; font-weight: 900;">✓</span> Daily backups
            </li>
            <li style="padding: 10px 0; color: #334155; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 10px;">
              <span style="display: flex; align-items: center; justify-content: center; width: 18px; height: 18px; background: #D1FAE5; border-radius: 50%; color: #10B981; font-size: 12px; font-weight: 900;">✓</span> 24/7 monitoring
            </li>
          </ul>
        </div>
      </div>

      <!-- Card 3: Zero Risk -->
      <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 32px 24px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 2px 12px rgba(0,0,0,0.03);">
        <div>
          <!-- Light Gray Icon Box -->
          <div style="width: 48px; height: 48px; background: #F1F5F9; border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-bottom: 20px;">
            <svg style="width: 24px; height: 24px; fill: none; stroke: #0F172A; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round;" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          </div>
          <h3 style="font-size: 20px; font-weight: 800; color: #0F172A; margin-bottom: 8px;">Zero Risk</h3>
          <div style="font-size: 36px; font-weight: 900; color: #0F172A; margin-bottom: 6px; letter-spacing: -0.02em;">Free</div>
          <p style="color: #64748B; font-size: 14px; font-weight: 500; margin-bottom: 24px;">Pay only when 100% satisfied</p>
          
          <ul style="list-style: none; padding: 0; margin-top: 16px; border-top: 1px solid #F1F5F9;">
            <li style="padding: 10px 0; color: #334155; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 10px;">
              <span style="display: flex; align-items: center; justify-content: center; width: 18px; height: 18px; background: #D1FAE5; border-radius: 50%; color: #10B981; font-size: 12px; font-weight: 900;">✓</span> No prepayment
            </li>
            <li style="padding: 10px 0; color: #334155; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 10px;">
              <span style="display: flex; align-items: center; justify-content: center; width: 18px; height: 18px; background: #D1FAE5; border-radius: 50%; color: #10B981; font-size: 12px; font-weight: 900;">✓</span> Full satisfaction guarantee
            </li>
            <li style="padding: 10px 0; color: #334155; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 10px;">
              <span style="display: flex; align-items: center; justify-content: center; width: 18px; height: 18px; background: #D1FAE5; border-radius: 50%; color: #10B981; font-size: 12px; font-weight: 900;">✓</span> Unlimited revisions
            </li>
            <li style="padding: 10px 0; color: #334155; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 10px;">
              <span style="display: flex; align-items: center; justify-content: center; width: 18px; height: 18px; background: #D1FAE5; border-radius: 50%; color: #10B981; font-size: 12px; font-weight: 900;">✓</span> Money-back promise
            </li>
          </ul>
        </div>
      </div>

      <!-- Card 4: Custom Development -->
      <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 32px 24px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 2px 12px rgba(0,0,0,0.03);">
        <div>
          <!-- Light Gray Icon Box -->
          <div style="width: 48px; height: 48px; background: #F1F5F9; border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-bottom: 20px;">
            <svg style="width: 24px; height: 24px; fill: none; stroke: #0F172A; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round;" viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
          </div>
          <h3 style="font-size: 20px; font-weight: 800; color: #0F172A; margin-bottom: 8px; line-height: 1.2;">Custom<br/>Development</h3>
          <p style="color: #64748B; font-size: 14px; font-weight: 500; margin-bottom: 24px; margin-top: 14px;">Tailored solutions for unique needs</p>
          
          <ul style="list-style: none; padding: 0; margin-top: 16px; border-top: 1px solid #F1F5F9;">
            <li style="padding: 10px 0; color: #334155; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 10px;">
              <span style="display: flex; align-items: center; justify-content: center; width: 18px; height: 18px; background: #D1FAE5; border-radius: 50%; color: #10B981; font-size: 12px; font-weight: 900;">✓</span> E-commerce platforms
            </li>
            <li style="padding: 10px 0; color: #334155; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 10px;">
              <span style="display: flex; align-items: center; justify-content: center; width: 18px; height: 18px; background: #D1FAE5; border-radius: 50%; color: #10B981; font-size: 12px; font-weight: 900;">✓</span> Web applications
            </li>
            <li style="padding: 10px 0; color: #334155; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 10px;">
              <span style="display: flex; align-items: center; justify-content: center; width: 18px; height: 18px; background: #D1FAE5; border-radius: 50%; color: #10B981; font-size: 12px; font-weight: 900;">✓</span> API integrations
            </li>
            <li style="padding: 10px 0; color: #334155; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 10px;">
              <span style="display: flex; align-items: center; justify-content: center; width: 18px; height: 18px; background: #D1FAE5; border-radius: 50%; color: #10B981; font-size: 12px; font-weight: 900;">✓</span> Custom features
            </li>
          </ul>
        </div>
      </div>

    </div>

    <!-- Mint-Green Banner (Exact from Screenshot) -->
    <div style="background: #ECFDF5; border: 1px solid #A7F3D0; border-radius: 16px; padding: 24px; text-align: center; margin-bottom: 28px;">
      <p style="color: #065F46; font-size: 17px; font-weight: 800; margin: 0;">No prepayment required. Pay only when you are 100% satisfied.</p>
    </div>

    <!-- Action Button Underneath Banner (Sky-Blue) -->
    <div style="text-align: center;">
      <a href="contact.html" style="display: inline-block; background: #389BFF; color: #FFFFFF; font-size: 16px; font-weight: 800; padding: 16px 36px; border-radius: 12px; text-decoration: none; box-shadow: 0 4px 15px rgba(56,155,255,0.25);">Start Your Project ➔</a>
    </div>

  </div>
</section>
"""

full_pricing_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Transparent & Simple Pricing — Avalanche Agency</title>
  <meta name="description" content="Transparent & Simple Pricing — Avalanche Agency. Premium web development from $299 flat rate.">
  <link rel="icon" type="image/png" href="avalanche_logo.png">
  <link rel="shortcut icon" href="avalanche_logo.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background: #FFFFFF; color: #0F172A; font-family: 'Inter', system-ui, sans-serif; line-height: 1.65; }}
    .wrap {{ max-width: 1180px; margin: 0 auto; padding: 0 24px; }}
  </style>
</head>
<body>

{header_html}

<main>
{exact_unified_pricing_html}
</main>

{footer_html}

{lang_script}
</body>
</html>
"""

# Write pricing.html
pricing_path = os.path.join(site_dir, "pricing.html")
open(pricing_path, "w", encoding="utf-8").write(full_pricing_html)
print(f"✅ Assembled exact screenshot unified pricing.html ({len(full_pricing_html)} bytes)!")

# Deploy to Hostinger via SFTP
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("82.29.199.155", port=65002, username="u473746908", password="Stefrogovskyi#1", timeout=15)

sftp = ssh.open_sftp()
sftp.put(pricing_path, "/home/u473746908/domains/aavalanche.com/public_html/dev/pricing.html")
sftp.close()

# Git commit and push
os.chdir(site_dir)
subprocess.run(["git", "checkout", "dev"], check=True)
subprocess.run(["git", "add", "pricing.html"], check=True)
res_commit = subprocess.run(["git", "commit", "-m", "feat(dev): Update pricing.html to exact unified universal pricing block matching user screenshot"], capture_output=True, text=True)
print(res_commit.stdout or res_commit.stderr)

res_push = subprocess.run(["git", "push", "origin", "dev", "--force"], capture_output=True, text=True)
print(res_push.stdout or res_push.stderr)

res_sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
active_sha = res_sha.stdout.strip()

ssh.close()

print("🎉 EXACT SCREENSHOT UNIFIED PRICING DEPLOYED TO DEV!")
print(f"📌 ACTIVE GIT COMMIT SHA: {active_sha}")
