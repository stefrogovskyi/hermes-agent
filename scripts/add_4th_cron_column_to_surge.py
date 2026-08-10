# -*- coding: utf-8 -*-
"""
add_4th_cron_column_to_surge.py — Добавление 4-й колонки "🔄 RECURRING / CRON TASKS" на Канбан-доску Surge.sh.
"""

import os, subprocess, base64

HERMES_DIR = r"C:\Users\Stefan\AppData\Local\hermes"
site_dir = os.path.join(HERMES_DIR, "avalanche_v2_staging")
os.chdir(site_dir)

# Base64 logo for Surge
logo_p = os.path.join(site_dir, "avalanche_logo.png")
b64_logo = ""
if os.path.exists(logo_p):
    b64_logo = "data:image/png;base64," + base64.b64encode(open(logo_p, "rb").read()).decode('utf-8')

kanban_4col_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Stefan Rogovskiy & Navo Team — Project Kanban Board</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background: #0F172A; color: #F8FAFC; font-family: 'Inter', system-ui, sans-serif; line-height: 1.5; min-height: 100vh; padding: 30px 20px; }}
    .wrap {{ max-width: 1400px; margin: 0 auto; }}
    header {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 1px solid #1E293B; }}
    .logo-badge {{ display: flex; align-items: center; gap: 14px; text-decoration: none; color: #FFFFFF; }}
    .logo-badge img {{ height: 42px; border-radius: 10px; }}
    .kanban-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }}
    .column {{ background: #1E293B; border: 1px solid #334155; border-radius: 16px; padding: 18px; min-height: 600px; display: flex; flex-direction: column; gap: 14px; }}
    .col-header {{ display: flex; align-items: center; justify-content: space-between; padding-bottom: 12px; border-bottom: 2px solid #334155; margin-bottom: 6px; }}
    .col-title {{ font-size: 14px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; display: flex; align-items: center; gap: 8px; }}
    .col-count {{ background: #334155; color: #F8FAFC; font-size: 12px; font-weight: 800; padding: 2px 8px; border-radius: 12px; }}
    .task-card {{ background: #0F172A; border: 1px solid #334155; border-radius: 12px; padding: 16px; transition: transform 0.2s, border-color 0.2s; box-shadow: 0 4px 12px rgba(0,0,0,0.2); }}
    .task-card:hover {{ transform: translateY(-2px); border-color: #5FB3F9; }}
    .task-tag {{ display: inline-block; font-size: 11px; font-weight: 800; text-transform: uppercase; padding: 3px 8px; border-radius: 6px; margin-bottom: 8px; }}
    .tag-purple {{ background: rgba(139,92,246,0.15); color: #A78BFA; border: 1px solid rgba(139,92,246,0.3); }}
    .tag-blue {{ background: rgba(95,179,249,0.15); color: #5FB3F9; border: 1px solid rgba(95,179,249,0.3); }}
    .tag-yellow {{ background: rgba(234,179,8,0.15); color: #EAB308; border: 1px solid rgba(234,179,8,0.3); }}
    .tag-green {{ background: rgba(16,185,129,0.15); color: #10B981; border: 1px solid rgba(16,185,129,0.3); }}
    .task-title {{ font-size: 14px; font-weight: 700; color: #F8FAFC; margin-bottom: 6px; }}
    .task-desc {{ font-size: 12px; color: #94A3B8; margin-bottom: 10px; line-height: 1.4; }}
    .task-footer {{ display: flex; align-items: center; justify-content: space-between; font-size: 11px; color: #64748B; font-weight: 600; pt-8px; border-top: 1px solid #1E293B; }}
  </style>
</head>
<body>

<div class="wrap">
  
  <header>
    <div class="logo-badge">
      <img src="{b64_logo}" alt="Avalanche">
      <div>
        <h1 style="font-size: 22px; font-weight: 800;">Stefan Rogovskiy & Navo Team Workstream</h1>
        <div style="font-size: 13px; color: #94A3B8;">Live Interactive Project Kanban Board • Autonomous Hermes Execution</div>
      </div>
    </div>

    <div style="background: #1E293B; border: 1px solid #334155; border-radius: 10px; padding: 8px 16px; font-size: 13px; font-weight: 700; color: #10B981;">
      ✓ Active Hermes Sync
    </div>
  </header>

  <div class="kanban-grid">
    
    <!-- 1. TODO / BACKLOG COLUMN -->
    <div class="column">
      <div class="col-header">
        <div class="col-title" style="color: #EAB308;">📋 TODO / BACKLOG</div>
        <div class="col-count">2</div>
      </div>

      <div class="task-card">
        <span class="task-tag tag-yellow">PAYMENTS</span>
        <div class="task-title">💳 Monobank Real Acquiring Token Integration</div>
        <div class="task-desc">Connect X-Token FOP from web.monobank.ua for live credit card and Apple/Google Pay transactions.</div>
        <div class="task-footer"><span>ID: #TASK-101</span><span>Priority: High</span></div>
      </div>

      <div class="task-card">
        <span class="task-tag tag-yellow">AUTOMATION</span>
        <div class="task-title">🛍️ Silpo Weekly Groceries Order Assembly</div>
        <div class="task-desc">Automated weekly basket compilation (>1,700 UAH) via Playwright Chromium / CDP.</div>
        <div class="task-footer"><span>ID: #TASK-102</span><span>Priority: Medium</span></div>
      </div>
    </div>

    <!-- 2. IN PROGRESS COLUMN -->
    <div class="column">
      <div class="col-header">
        <div class="col-title" style="color: #389BFF;">⚡ IN PROGRESS</div>
        <div class="col-count">3</div>
      </div>

      <div class="task-card" style="border-color: #389BFF;">
        <span class="task-tag tag-blue">INFRASTRUCTURE</span>
        <div class="task-title">🌐 Avalanche 3-Tier Pipeline Architecture</div>
        <div class="task-desc">Continuous deployment across dev.aavalanche.com, staging.aavalanche.com, and production.</div>
        <div class="task-footer"><span>ID: #TASK-201</span><span style="color:#389BFF;">Active</span></div>
      </div>

      <div class="task-card" style="border-color: #389BFF;">
        <span class="task-tag tag-blue">AI ENGINE</span>
        <div class="task-title">🚀 AI Project Evaluation & 10-Point Price Graduation</div>
        <div class="task-desc">Real-time NLP project complexity analyzer ($9+$5/mo to $99+$50/mo) and IP-currency converter.</div>
        <div class="task-footer"><span>ID: #TASK-202</span><span style="color:#389BFF;">Active</span></div>
      </div>

      <div class="task-card" style="border-color: #389BFF;">
        <span class="task-tag tag-blue">USER PORTAL</span>
        <div class="task-title">🔑 User Auth, Cabinet, My Orders & Admin Users Table</div>
        <div class="task-desc">SQLite authentication, Google/Facebook OAuth, My Orders tab, and Admin management registry.</div>
        <div class="task-footer"><span>ID: #TASK-203</span><span style="color:#389BFF;">Active</span></div>
      </div>
    </div>

    <!-- 3. RECURRING / CRON TASKS COLUMN (4TH COLUMN) -->
    <div class="column" style="border-color: #8B5CF6;">
      <div class="col-header" style="border-bottom-color: #8B5CF6;">
        <div class="col-title" style="color: #A78BFA;">🔄 RECURRING / CRON TASKS</div>
        <div class="col-count">4</div>
      </div>

      <div class="task-card" style="border-color: rgba(139,92,246,0.4);">
        <span class="task-tag tag-purple">CRON 23:00 MSK</span>
        <div class="task-title">📺 YouTube Watch Later Sorter</div>
        <div class="task-desc">Daily digest and playlist categorization via Playwright & YouTube API.</div>
        <div class="task-footer"><span>ID: #CRON-01</span><span style="color:#A78BFA;">Daily 23:00</span></div>
      </div>

      <div class="task-card" style="border-color: rgba(139,92,246,0.4);">
        <span class="task-tag tag-purple">CRON 02:00 MSK</span>
        <div class="task-title">🌾 Memory Harvest Cron</div>
        <div class="task-desc">Daily session memory harvesting and cases extraction into memory_v2.</div>
        <div class="task-footer"><span>ID: #CRON-02</span><span style="color:#A78BFA;">Daily 02:00</span></div>
      </div>

      <div class="task-card" style="border-color: rgba(139,92,246,0.4);">
        <span class="task-tag tag-purple">CRON 03:00 MSK</span>
        <div class="task-title">🌲 Pinecone Vector Memory Sync</div>
        <div class="task-desc">Automated vector embedding synchronization for unlimited fast semantic recall.</div>
        <div class="task-footer"><span>ID: #CRON-03</span><span style="color:#A78BFA;">Daily 03:00</span></div>
      </div>

      <div class="task-card" style="border-color: rgba(139,92,246,0.4);">
        <span class="task-tag tag-purple">WEEKLY CRON</span>
        <div class="task-title">🛍️ Silpo Basket Weekly Auto-Assembly</div>
        <div class="task-desc">Weekly grocery basket compilation (>1,700 UAH) via Playwright Chromium.</div>
        <div class="task-footer"><span>ID: #CRON-04</span><span style="color:#A78BFA;">Weekly</span></div>
      </div>
    </div>

    <!-- 4. COMPLETED / DONE COLUMN -->
    <div class="column">
      <div class="col-header">
        <div class="col-title" style="color: #10B981;">✅ COMPLETED / DONE</div>
        <div class="col-count">3</div>
      </div>

      <div class="task-card">
        <span class="task-tag tag-green">LOCALIZATION</span>
        <div class="task-title">🌍 8 Multilingual Language Clones</div>
        <div class="task-desc">100% mirrored HTML/CSS clones for es, de, fr, it, uk, ru, zh, ar with persistent auth session.</div>
        <div class="task-footer"><span>ID: #TASK-301</span><span style="color:#10B981;">✓ Done</span></div>
      </div>

      <div class="task-card">
        <span class="task-tag tag-green">EMAIL SYSTEM</span>
        <div class="task-title">📧 Dual Branded Email Mailer</div>
        <div class="task-desc">Automated HTML email confirmations for clients and instant alert notifications to dr.reenforce@gmail.com.</div>
        <div class="task-footer"><span>ID: #TASK-302</span><span style="color:#10B981;">✓ Done</span></div>
      </div>

      <div class="task-card">
        <span class="task-tag tag-green">SEO & ROUTING</span>
        <div class="task-title">🔗 Clean URLs (.htaccess) & Dynamic IP Currency</div>
        <div class="task-desc">Extensionless URLs without .html, sitemap.xml, robots.txt, and IP-based local currency converter.</div>
        <div class="task-footer"><span>ID: #TASK-303</span><span style="color:#10B981;">✓ Done</span></div>
      </div>
    </div>

  </div>

</div>

</body>
</html>
"""

surge_dir = os.path.join(HERMES_DIR, "_surge_kanban_standalone")
os.makedirs(surge_dir, exist_ok=True)
open(os.path.join(surge_dir, "index.html"), "w", encoding="utf-8").write(kanban_4col_html)

# Publish to Surge.sh
surge_token = "82bd19e64bbf196940cf4c78cf9f835a"
domain_name = "stefan-kanban.surge.sh"

cmd_surge = f'npx surge "{surge_dir}" --domain {domain_name} --token {surge_token}'
res = subprocess.run(cmd_surge, shell=True, capture_output=True, text=True)
print("STDOUT:", res.stdout)
print("STDERR:", res.stderr)

print(f"🎉 4-COLUMN KANBAN BOARD PUBLISHED TO SURGE.SH!")
print(f"👉 LIVE LINK: https://{domain_name}")
