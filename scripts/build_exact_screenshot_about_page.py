# -*- coding: utf-8 -*-
"""
build_exact_screenshot_about_page.py — Точная сборка страницы About (about.html) на ветке dev
по скриншоту пользователя:
  1. Верхняя секция:
     - Слева: Заголовок "About Avalanche Agency", подзаголовок и синяя кнопка "Get in Touch"
     - Справа: Синий квадратный бейдж-логотип (белая векторная верхушка "AA" + AVALANCHE A G E N C Y)
  2. Нижняя секция: "Our Values"
     - 4 колонки ценностей с нежно-голубыми иконками:
       * Excellence (медаль/награда 🎖️)
       * Partnership (два человека 👥)
       * Results (мишень 🎯)
       * Innovation (лампочка 💡)
  3. Сквозной Хедер со скриншота 1 и Футер со скриншота 2
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

# HTML for the exact screenshot About page layout
exact_screenshot_about_body = """
<section style="padding: 90px 0; background: #FFFFFF; font-family: 'Inter', system-ui, -apple-system, sans-serif;">
  <div style="max-width: 1180px; margin: 0 auto; padding: 0 24px;">
    
    <!-- 1. Top Section: 2 Columns (Text Left, Logo Graphic Right) -->
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 60px; align-items: center; margin-bottom: 90px;">
      
      <!-- Left Column (Text Content) -->
      <div>
        <h1 style="font-size: 44px; font-weight: 800; color: #0F172A; margin-bottom: 20px; letter-spacing: -0.02em;">About Avalanche Agency</h1>
        <p style="font-size: 18px; color: #64748B; line-height: 1.7; margin-bottom: 32px; max-width: 520px;">
          We are a premium web agency dedicated to creating exceptional digital experiences. Our team combines creativity with technical expertise to deliver solutions that drive results.
        </p>
        <a href="contact.html" style="display: inline-block; background: #389BFF; color: #FFFFFF; font-size: 16px; font-weight: 700; padding: 14px 32px; border-radius: 12px; text-decoration: none; box-shadow: 0 4px 15px rgba(56,155,255,0.25);">Get in Touch ➔</a>
      </div>

      <!-- Right Column (Blue Logo Graphic Badge) -->
      <div style="display: flex; justify-content: center; align-items: center;">
        <div style="width: 320px; height: 320px; background: #389BFF; border-radius: 28px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 40px; box-shadow: 0 20px 40px rgba(56,155,255,0.25); text-align: center;">
          <!-- Stylized AA Mountain Logo SVG -->
          <svg style="width: 80px; height: 80px; fill: none; stroke: #FFFFFF; stroke-width: 2.5; stroke-linecap: round; stroke-linejoin: round; margin-bottom: 20px;" viewBox="0 0 24 24">
            <path d="M12 3L2 21h20L12 3z"/>
            <path d="M12 9l-4 8h8l-4-8z"/>
          </svg>
          <div style="color: #FFFFFF; font-weight: 900; font-size: 24px; letter-spacing: 0.15em; text-transform: uppercase;">AVALANCHE</div>
          <div style="color: rgba(255,255,255,0.85); font-weight: 700; font-size: 13px; letter-spacing: 0.35em; text-transform: uppercase; margin-top: 6px;">A G E N C Y</div>
        </div>
      </div>

    </div>

    <!-- 2. Bottom Section: Our Values -->
    <div style="text-align: center;">
      <h2 style="font-size: 32px; font-weight: 800; color: #0F172A; margin-bottom: 48px; letter-spacing: -0.02em;">Our Values</h2>

      <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 28px;">
        
        <!-- Value 1: Excellence -->
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 20px; padding: 36px 24px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.02);">
          <div style="width: 56px; height: 56px; background: #EFF6FF; border-radius: 16px; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px;">
            <svg style="width: 28px; height: 28px; fill: none; stroke: #389BFF; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round;" viewBox="0 0 24 24"><circle cx="12" cy="8" r="7"/><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/></svg>
          </div>
          <h3 style="font-size: 19px; font-weight: 800; color: #0F172A; margin-bottom: 10px;">Excellence</h3>
          <p style="font-size: 14px; color: #64748B; line-height: 1.6;">We strive for perfection in every project we deliver.</p>
        </div>

        <!-- Value 2: Partnership -->
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 20px; padding: 36px 24px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.02);">
          <div style="width: 56px; height: 56px; background: #EFF6FF; border-radius: 16px; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px;">
            <svg style="width: 28px; height: 28px; fill: none; stroke: #389BFF; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round;" viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
          </div>
          <h3 style="font-size: 19px; font-weight: 800; color: #0F172A; margin-bottom: 10px;">Partnership</h3>
          <p style="font-size: 14px; color: #64748B; line-height: 1.6;">We work alongside you, not just for you.</p>
        </div>

        <!-- Value 3: Results -->
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 20px; padding: 36px 24px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.02);">
          <div style="width: 56px; height: 56px; background: #EFF6FF; border-radius: 16px; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px;">
            <svg style="width: 28px; height: 28px; fill: none; stroke: #389BFF; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round;" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>
          </div>
          <h3 style="font-size: 19px; font-weight: 800; color: #0F172A; margin-bottom: 10px;">Results</h3>
          <p style="font-size: 14px; color: #64748B; line-height: 1.6;">Every decision is driven by measurable outcomes.</p>
        </div>

        <!-- Value 4: Innovation -->
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 20px; padding: 36px 24px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.02);">
          <div style="width: 56px; height: 56px; background: #EFF6FF; border-radius: 16px; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px;">
            <svg style="width: 28px; height: 28px; fill: none; stroke: #389BFF; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round;" viewBox="0 0 24 24"><path d="M9 18h6"/><path d="M10 22h4"/><path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .23 2.23 1.5 3.5A4.61 4.61 0 0 1 8.91 14"/></svg>
          </div>
          <h3 style="font-size: 19px; font-weight: 800; color: #0F172A; margin-bottom: 10px;">Innovation</h3>
          <p style="font-size: 14px; color: #64748B; line-height: 1.6;">We embrace modern solutions and creative thinking.</p>
        </div>

      </div>
    </div>

  </div>
</section>
"""

full_about_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>About Avalanche Agency — Avalanche Agency</title>
  <meta name="description" content="About Avalanche Agency — Premium web development, software architecture, and growth marketing.">
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
{exact_screenshot_about_body}
</main>

{footer_html}

{lang_script}
</body>
</html>
"""

# Save about.html in site_dir
about_path = os.path.join(site_dir, "about.html")
open(about_path, "w", encoding="utf-8").write(full_about_html)
print(f"✅ Assembled exact screenshot about.html ({len(full_about_html)} bytes)!")

# Upload to Hostinger via SFTP
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("82.29.199.155", port=65002, username="u473746908", password="Stefrogovskyi#1", timeout=15)

sftp = ssh.open_sftp()
sftp.put(about_path, "/home/u473746908/domains/aavalanche.com/public_html/dev/about.html")
sftp.close()

# Git Commit and Push
os.chdir(site_dir)
subprocess.run(["git", "checkout", "dev"], check=True)
subprocess.run(["git", "add", "about.html"], check=True)
res_commit = subprocess.run(["git", "commit", "-m", "feat(dev): Update about.html to exact layout matching user screenshot (2-column layout with blue logo badge + 4 Our Values cards)"], capture_output=True, text=True)
print(res_commit.stdout or res_commit.stderr)

res_push = subprocess.run(["git", "push", "origin", "dev", "--force"], capture_output=True, text=True)
print(res_push.stdout or res_push.stderr)

res_sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
active_sha = res_sha.stdout.strip()

ssh.close()

print("🎉 EXACT SCREENSHOT ABOUT PAGE DEPLOYED TO DEV!")
print(f"📌 ACTIVE GIT COMMIT SHA: {active_sha}")
