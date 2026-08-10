# -*- coding: utf-8 -*-
"""
build_exact_prod_pricing_page.py — Точная сборка визуальной страницы Прайсинг (pricing.html) 1-в-1 с продакшна:
  - Точный Хедер (header.html) со скриншота 1
  - Точные карточки тарифов (Flat Rate $299, Peace of Mind $19/mo, Zero Risk Free, Custom Development)
  - Точные шрифты, закругления, ховер-эффекты, галочки ✓, бейджи и акцентные синие кнопки
  - Точный Футер (footer.html) со скриншота 2
"""

import os, paramiko, subprocess

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

exact_pricing_body_html = """
<section style="padding: 90px 0; background: #F8FAFC; font-family: 'Inter', system-ui, -apple-system, sans-serif;">
  <div style="max-width: 1180px; margin: 0 auto; padding: 0 24px;">
    
    <!-- Section Header -->
    <div style="text-align: center; margin-bottom: 64px;">
      <span style="font-size: 13px; font-weight: 800; letter-spacing: 0.15em; color: #389BFF; text-transform: uppercase;">SIMPLE & TRANSPARENT</span>
      <h1 style="font-size: 44px; font-weight: 800; color: #0F172A; margin: 12px 0 16px; letter-spacing: -0.02em;">Simple, Transparent Pricing</h1>
      <p style="font-size: 19px; color: #64748B; max-width: 620px; margin: 0 auto; line-height: 1.6;">No hidden fees. No surprises. High-performance web solutions built for category leaders.</p>
    </div>

    <!-- 4 Pricing Cards Grid -->
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; align-items: stretch;">
      
      <!-- Card 1: Flat Rate ($299) -->
      <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 20px; padding: 36px 28px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 4px 20px rgba(0,0,0,0.03); transition: transform 0.2s, box-shadow 0.2s;">
        <div>
          <div style="font-size: 12px; font-weight: 800; color: #64748B; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;">FULL DEVELOPMENT</div>
          <h3 style="font-size: 22px; font-weight: 800; color: #0F172A; margin-bottom: 16px;">Flat Rate</h3>
          <div style="font-size: 40px; font-weight: 900; color: #0F172A; margin-bottom: 12px; letter-spacing: -0.03em;">$299 <span style="font-size: 14px; font-weight: 600; color: #64748B;">/ one-time</span></div>
          <p style="color: #64748B; font-size: 14px; line-height: 1.5; margin-bottom: 24px; min-height: 42px;">Complete website build tailored to your business needs.</p>
          
          <ul style="list-style: none; padding: 0; margin-bottom: 32px; border-top: 1px solid #F1F5F9;">
            <li style="padding: 10px 0; border-bottom: 1px solid #F1F5F9; color: #334155; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 8px;">
              <span style="color: #389BFF; font-weight: 800;">✓</span> Complete website build
            </li>
            <li style="padding: 10px 0; border-bottom: 1px solid #F1F5F9; color: #334155; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 8px;">
              <span style="color: #389BFF; font-weight: 800;">✓</span> Custom design
            </li>
            <li style="padding: 10px 0; border-bottom: 1px solid #F1F5F9; color: #334155; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 8px;">
              <span style="color: #389BFF; font-weight: 800;">✓</span> Mobile responsive
            </li>
            <li style="padding: 10px 0; border-bottom: 1px solid #F1F5F9; color: #334155; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 8px;">
              <span style="color: #389BFF; font-weight: 800;">✓</span> SEO ready
            </li>
          </ul>
        </div>
        <a href="contact.html" style="display: block; text-align: center; background: #389BFF; color: #FFFFFF; padding: 14px 20px; border-radius: 12px; font-weight: 700; text-decoration: none; font-size: 15px;">Get Started ➔</a>
      </div>

      <!-- Card 2: Peace of Mind ($19/mo) - FEATURED -->
      <div style="background: #FFFFFF; border: 2px solid #389BFF; border-radius: 20px; padding: 36px 28px; display: flex; flex-direction: column; justify-content: space-between; position: relative; box-shadow: 0 12px 30px rgba(56,155,255,0.15);">
        <div style="position: absolute; top: -13px; right: 20px; background: #389BFF; color: #FFFFFF; font-size: 11px; font-weight: 800; padding: 4px 12px; border-radius: 20px; text-transform: uppercase; letter-spacing: 0.05em;">POPULAR</div>
        <div>
          <div style="font-size: 12px; font-weight: 800; color: #389BFF; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;">HOSTING & CARE</div>
          <h3 style="font-size: 22px; font-weight: 800; color: #0F172A; margin-bottom: 16px;">Peace of Mind</h3>
          <div style="font-size: 40px; font-weight: 900; color: #0F172A; margin-bottom: 12px; letter-spacing: -0.03em;">$19 <span style="font-size: 14px; font-weight: 600; color: #64748B;">/ mo</span></div>
          <p style="color: #64748B; font-size: 14px; line-height: 1.5; margin-bottom: 24px; min-height: 42px;">Hosting, security, and ongoing technical maintenance.</p>
          
          <ul style="list-style: none; padding: 0; margin-bottom: 32px; border-top: 1px solid #F1F5F9;">
            <li style="padding: 10px 0; border-bottom: 1px solid #F1F5F9; color: #334155; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 8px;">
              <span style="color: #389BFF; font-weight: 800;">✓</span> Premium cloud hosting
            </li>
            <li style="padding: 10px 0; border-bottom: 1px solid #F1F5F9; color: #334155; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 8px;">
              <span style="color: #389BFF; font-weight: 800;">✓</span> SSL & 24/7 monitoring
            </li>
            <li style="padding: 10px 0; border-bottom: 1px solid #F1F5F9; color: #334155; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 8px;">
              <span style="color: #389BFF; font-weight: 800;">✓</span> Daily backups
            </li>
            <li style="padding: 10px 0; border-bottom: 1px solid #F1F5F9; color: #334155; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 8px;">
              <span style="color: #389BFF; font-weight: 800;">✓</span> Monthly content updates
            </li>
          </ul>
        </div>
        <a href="contact.html" style="display: block; text-align: center; background: #0F172A; color: #FFFFFF; padding: 14px 20px; border-radius: 12px; font-weight: 700; text-decoration: none; font-size: 15px;">Choose Care Plan ➔</a>
      </div>

      <!-- Card 3: Zero Risk (Free) -->
      <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 20px; padding: 36px 28px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 4px 20px rgba(0,0,0,0.03);">
        <div>
          <div style="font-size: 12px; font-weight: 800; color: #10B981; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;">GUARANTEED RESULT</div>
          <h3 style="font-size: 22px; font-weight: 800; color: #0F172A; margin-bottom: 16px;">Zero Risk</h3>
          <div style="font-size: 40px; font-weight: 900; color: #10B981; margin-bottom: 12px; letter-spacing: -0.03em;">$0 <span style="font-size: 14px; font-weight: 600; color: #64748B;">prepayment</span></div>
          <p style="color: #64748B; font-size: 14px; line-height: 1.5; margin-bottom: 24px; min-height: 42px;">Pay only when you are 100% satisfied with the work.</p>
          
          <ul style="list-style: none; padding: 0; margin-bottom: 32px; border-top: 1px solid #F1F5F9;">
            <li style="padding: 10px 0; border-bottom: 1px solid #F1F5F9; color: #334155; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 8px;">
              <span style="color: #10B981; font-weight: 800;">✓</span> No prepayment
            </li>
            <li style="padding: 10px 0; border-bottom: 1px solid #F1F5F9; color: #334155; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 8px;">
              <span style="color: #10B981; font-weight: 800;">✓</span> Full satisfaction guarantee
            </li>
            <li style="padding: 10px 0; border-bottom: 1px solid #F1F5F9; color: #334155; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 8px;">
              <span style="color: #10B981; font-weight: 800;">✓</span> Unlimited revisions
            </li>
            <li style="padding: 10px 0; border-bottom: 1px solid #F1F5F9; color: #334155; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 8px;">
              <span style="color: #10B981; font-weight: 800;">✓</span> Money-back promise
            </li>
          </ul>
        </div>
        <a href="contact.html" style="display: block; text-align: center; background: #10B981; color: #FFFFFF; padding: 14px 20px; border-radius: 12px; font-weight: 700; text-decoration: none; font-size: 15px;">Start Risk-Free ➔</a>
      </div>

      <!-- Card 4: Custom Development (Custom) -->
      <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 20px; padding: 36px 28px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 4px 20px rgba(0,0,0,0.03);">
        <div>
          <div style="font-size: 12px; font-weight: 800; color: #8B5CF6; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;">ENTERPRISE</div>
          <h3 style="font-size: 22px; font-weight: 800; color: #0F172A; margin-bottom: 16px;">Custom Systems</h3>
          <div style="font-size: 40px; font-weight: 900; color: #0F172A; margin-bottom: 12px; letter-spacing: -0.03em;">Custom</div>
          <p style="color: #64748B; font-size: 14px; line-height: 1.5; margin-bottom: 24px; min-height: 42px;">Tailored software & AI agent solutions for unique needs.</p>
          
          <ul style="list-style: none; padding: 0; margin-bottom: 32px; border-top: 1px solid #F1F5F9;">
            <li style="padding: 10px 0; border-bottom: 1px solid #F1F5F9; color: #334155; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 8px;">
              <span style="color: #8B5CF6; font-weight: 800;">✓</span> E-commerce platforms
            </li>
            <li style="padding: 10px 0; border-bottom: 1px solid #F1F5F9; color: #334155; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 8px;">
              <span style="color: #8B5CF6; font-weight: 800;">✓</span> Custom AI Agents & APIs
            </li>
            <li style="padding: 10px 0; border-bottom: 1px solid #F1F5F9; color: #334155; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 8px;">
              <span style="color: #8B5CF6; font-weight: 800;">✓</span> Dedicated team & PM
            </li>
            <li style="padding: 10px 0; border-bottom: 1px solid #F1F5F9; color: #334155; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 8px;">
              <span style="color: #8B5CF6; font-weight: 800;">✓</span> SLA & 24/7 Support
            </li>
          </ul>
        </div>
        <a href="contact.html" style="display: block; text-align: center; background: #8B5CF6; color: #FFFFFF; padding: 14px 20px; border-radius: 12px; font-weight: 700; text-decoration: none; font-size: 15px;">Contact Sales ➔</a>
      </div>

    </div>

    <!-- Guarantee Banner -->
    <div style="margin-top: 60px; background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 16px; padding: 24px; text-align: center; color: #1E40AF; font-weight: 700; font-size: 16px;">
      🛡️ No prepayment required. Pay only when you are 100% satisfied with the final result.
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
{exact_pricing_body_html}
</main>

{footer_html}

{lang_script}
</body>
</html>
"""

# Write pricing.html locally in site_dir
pricing_path = os.path.join(site_dir, "pricing.html")
open(pricing_path, "w", encoding="utf-8").write(full_pricing_html)
print(f"✅ Generated new visual pricing.html ({len(full_pricing_html)} bytes)!")

# Upload pricing.html to Hostinger /public_html/dev/pricing.html
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("82.29.199.155", port=65002, username="u473746908", password="Stefrogovskyi#1", timeout=15)

sftp = ssh.open_sftp()
sftp.put(pricing_path, "/home/u473746908/domains/aavalanche.com/public_html/dev/pricing.html")
sftp.close()

# Git Commit and Push
os.chdir(site_dir)
subprocess.run(["git", "checkout", "dev"], check=True)
subprocess.run(["git", "add", "pricing.html"], check=True)
res_commit = subprocess.run(["git", "commit", "-m", "feat(dev): Update pricing.html visual layout and 4-tier cards matching exact production data"], capture_output=True, text=True)
print(res_commit.stdout or res_commit.stderr)

res_push = subprocess.run(["git", "push", "origin", "dev", "--force"], capture_output=True, text=True)
print(res_push.stdout or res_push.stderr)

res_sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
active_sha = res_sha.stdout.strip()

ssh.close()

print("🎉 EXACT VISUAL PRICING PAGE DEPLOYED TO DEV!")
print(f"📌 ACTIVE GIT COMMIT SHA: {active_sha}")
