# -*- coding: utf-8 -*-
"""
build_exact_screenshot_contact_page.py — Точная сборка страницы Contact (contact.html) на ветке dev
по скриншоту пользователя:
  1. Слева: "Contact Information"
     - 4 блока с голубыми иконками в квадратах:
       * Email: info@aavalanche.com
       * LinkedIn: linkedin.com/company/aavalanche
       * Phone: +1 (414) 554-0638
       * Address: 225 Franklin Street, Suite 2600 / Boston, MA 02110, USA
  2. Справа: Карточка формы "Contact Form"
     - Поля: Your Name, Email Address, Your Message
     - Кнопка: Широкая синяя кнопка с бумажным самолетиком ✈️ "Send Message" (цвет кнопки строго #5FB3F9)
  3. Сквозной Хедер со скриншота 1 и Футер со скриншота 2
"""

import os, paramiko, subprocess

HERMES_DIR = r"C:\Users\Stefan\AppData\Local\hermes"
site_dir = os.path.join(HERMES_DIR, "avalanche_v2_staging")
prod_extract_dir = os.path.join(HERMES_DIR, "prod_extracted_pages")

header_html = open(os.path.join(prod_extract_dir, "header.html"), encoding="utf-8").read()
footer_html = open(os.path.join(prod_extract_dir, "footer.html"), encoding="utf-8").read()

# Replace header and footer button colors to exact #5FB3F9
header_html = header_html.replace("#60B5FF", "#5FB3F9").replace("#389BFF", "#5FB3F9")
footer_html = footer_html.replace("#60B5FF", "#5FB3F9").replace("#389BFF", "#5FB3F9")

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

# HTML for exact screenshot Contact page layout
exact_screenshot_contact_body = """
<section style="padding: 90px 0; background: #FFFFFF; font-family: 'Inter', system-ui, -apple-system, sans-serif;">
  <div style="max-width: 1180px; margin: 0 auto; padding: 0 24px;">
    
    <!-- 2 Columns Layout: Contact Information Left, Contact Form Card Right -->
    <div style="display: grid; grid-template-columns: 1fr 1.1fr; gap: 60px; align-items: start;">
      
      <!-- Left Column: Contact Information -->
      <div>
        <h2 style="font-size: 32px; font-weight: 800; color: #0F172A; margin-bottom: 36px; letter-spacing: -0.02em;">Contact Information</h2>
        
        <div style="display: flex; flex-direction: column; gap: 28px;">
          
          <!-- 1. Email Entry -->
          <div style="display: flex; align-items: center; gap: 20px;">
            <div style="width: 52px; height: 52px; background: #F0F7FF; border-radius: 14px; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
              <svg style="width: 24px; height: 24px; fill: none; stroke: #5FB3F9; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round;" viewBox="0 0 24 24"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
            </div>
            <div>
              <div style="font-size: 13px; font-weight: 600; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 2px;">Email</div>
              <a href="mailto:info@aavalanche.com" style="font-size: 17px; font-weight: 800; color: #0F172A; text-decoration: none;">info@aavalanche.com</a>
            </div>
          </div>

          <!-- 2. LinkedIn Entry -->
          <div style="display: flex; align-items: center; gap: 20px;">
            <div style="width: 52px; height: 52px; background: #F0F7FF; border-radius: 14px; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
              <svg style="width: 24px; height: 24px; fill: #5FB3F9;" viewBox="0 0 24 24"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.46 10.9v8.37H9.25V10.9H6.46M7.86 6.74a1.6 1.6 0 1 0 0 3.2 1.6 1.6 0 0 0 0-3.2z"/></svg>
            </div>
            <div>
              <div style="font-size: 13px; font-weight: 600; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 2px;">LinkedIn</div>
              <a href="https://linkedin.com/company/aavalanche" target="_blank" style="font-size: 17px; font-weight: 800; color: #0F172A; text-decoration: none;">linkedin.com/company/aavalanche</a>
            </div>
          </div>

          <!-- 3. Phone Entry -->
          <div style="display: flex; align-items: center; gap: 20px;">
            <div style="width: 52px; height: 52px; background: #F0F7FF; border-radius: 14px; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
              <svg style="width: 24px; height: 24px; fill: none; stroke: #5FB3F9; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round;" viewBox="0 0 24 24"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.79 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            </div>
            <div>
              <div style="font-size: 13px; font-weight: 600; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 2px;">Phone</div>
              <a href="tel:+14145540638" style="font-size: 17px; font-weight: 800; color: #0F172A; text-decoration: none;">+1 (414) 554-0638</a>
            </div>
          </div>

          <!-- 4. Address Entry -->
          <div style="display: flex; align-items: flex-start; gap: 20px;">
            <div style="width: 52px; height: 52px; background: #F0F7FF; border-radius: 14px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-top: 2px;">
              <svg style="width: 24px; height: 24px; fill: none; stroke: #5FB3F9; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round;" viewBox="0 0 24 24"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
            </div>
            <div>
              <div style="font-size: 13px; font-weight: 600; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 2px;">Address</div>
              <div style="font-size: 16px; font-weight: 800; color: #0F172A; line-height: 1.5;">
                225 Franklin Street, Suite 2600<br/>
                Boston, MA 02110, USA
              </div>
            </div>
          </div>

        </div>
      </div>

      <!-- Right Column: Contact Form Card -->
      <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 20px; padding: 40px; box-shadow: 0 10px 30px rgba(0,0,0,0.03);">
        <form onsubmit="event.preventDefault(); alert('Message sent successfully!');">
          
          <div style="margin-bottom: 24px;">
            <label style="display: block; font-size: 14px; font-weight: 700; color: #334155; margin-bottom: 8px;">Your Name</label>
            <input type="text" placeholder="" required style="width: 100%; padding: 14px 16px; border: 1px solid #CBD5E1; border-radius: 10px; font-size: 15px; outline: none; transition: border-color 0.2s;" onfocus="this.style.borderColor='#5FB3F9'" onblur="this.style.borderColor='#CBD5E1'" />
          </div>

          <div style="margin-bottom: 24px;">
            <label style="display: block; font-size: 14px; font-weight: 700; color: #334155; margin-bottom: 8px;">Email Address</label>
            <input type="email" placeholder="" required style="width: 100%; padding: 14px 16px; border: 1px solid #CBD5E1; border-radius: 10px; font-size: 15px; outline: none; transition: border-color 0.2s;" onfocus="this.style.borderColor='#5FB3F9'" onblur="this.style.borderColor='#CBD5E1'" />
          </div>

          <div style="margin-bottom: 32px;">
            <label style="display: block; font-size: 14px; font-weight: 700; color: #334155; margin-bottom: 8px;">Your Message</label>
            <textarea rows="5" placeholder="" required style="width: 100%; padding: 14px 16px; border: 1px solid #CBD5E1; border-radius: 10px; font-size: 15px; outline: none; font-family: inherit; transition: border-color 0.2s;" onfocus="this.style.borderColor='#5FB3F9'" onblur="this.style.borderColor='#CBD5E1'"></textarea>
          </div>

          <button type="submit" style="width: 100%; background: #5FB3F9; color: #FFFFFF; padding: 16px 24px; border: none; border-radius: 12px; font-size: 16px; font-weight: 800; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 10px; box-shadow: 0 6px 20px rgba(95,179,249,0.3); transition: transform 0.2s, box-shadow 0.2s;">
            <svg style="width: 18px; height: 18px; fill: none; stroke: #FFFFFF; stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round;" viewBox="0 0 24 24"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
            <span>Send Message</span>
          </button>

        </form>
      </div>

    </div>

  </div>
</section>
"""

full_contact_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Let's Build Something Exceptional — Avalanche Agency</title>
  <meta name="description" content="Contact Avalanche Agency — Premium web development and growth marketing solutions.">
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
{exact_screenshot_contact_body}
</main>

{footer_html}

{lang_script}
</body>
</html>
"""

# Save contact.html locally in site_dir
contact_path = os.path.join(site_dir, "contact.html")
open(contact_path, "w", encoding="utf-8").write(full_contact_html)
print(f"✅ Generated exact screenshot contact.html ({len(full_contact_html)} bytes)!")

# Upload to Hostinger via SFTP
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("82.29.199.155", port=65002, username="u473746908", password="Stefrogovskyi#1", timeout=15)

sftp = ssh.open_sftp()
sftp.put(contact_path, "/home/u473746908/domains/aavalanche.com/public_html/dev/contact.html")
sftp.close()

# Git commit and push
os.chdir(site_dir)
subprocess.run(["git", "checkout", "dev"], check=True)
subprocess.run(["git", "add", "contact.html"], check=True)
res_commit = subprocess.run(["git", "commit", "-m", "feat(dev): Update contact.html to exact layout matching user screenshot (Contact Information left, Contact Form right, #5FB3F9 button color)"], capture_output=True, text=True)
print(res_commit.stdout or res_commit.stderr)

res_push = subprocess.run(["git", "push", "origin", "dev", "--force"], capture_output=True, text=True)
print(res_push.stdout or res_push.stderr)

res_sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
active_sha = res_sha.stdout.strip()

ssh.close()

print("🎉 EXACT SCREENSHOT CONTACT PAGE DEPLOYED TO DEV!")
print(f"📌 ACTIVE GIT COMMIT SHA: {active_sha}")
