# -*- coding: utf-8 -*-
"""
build_and_deploy_vercel_kanban.py — Генерация обновленного 4-колоночного Канбан-борда и деплой на Vercel!
"""

import os, subprocess, json

HERMES_DIR = r"C:\Users\Stefan\AppData\Local\hermes"
vercel_dir = os.path.join(HERMES_DIR, "_vercel_kanban_dashboard")
os.makedirs(vercel_dir, exist_ok=True)

kanban_html = """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Stefan's Workstream — Interactive Kanban Board</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0B0F19;
      --card-bg: #151C2C;
      --card-border: #232D42;
      --text-main: #F8FAFC;
      --text-muted: #94A3B8;
      --accent-blue: #5FB3F9;
      --accent-green: #10B981;
      --accent-purple: #A855F7;
      --accent-amber: #F59E0B;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Plus Jakarta Sans', sans-serif; }
    body { background-color: var(--bg); color: var(--text-main); min-height: 100vh; padding: 24px; }
    header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid var(--card-border); }
    .title-group { display: flex; align-items: center; gap: 12px; }
    .title-badge { background: linear-gradient(135deg, #3B82F6, #10B981); color: #FFF; font-weight: 800; font-size: 14px; padding: 6px 12px; border-radius: 8px; }
    h1 { font-size: 22px; font-weight: 800; letter-spacing: -0.5px; }
    .status-pill { display: flex; align-items: center; gap: 8px; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.2); color: var(--accent-green); padding: 6px 12px; border-radius: 20px; font-size: 13px; font-weight: 600; }
    .pulse-dot { width: 8px; height: 8px; background: var(--accent-green); border-radius: 50%; box-shadow: 0 0 10px var(--accent-green); }
    
    .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
    @media (max-width: 1200px) { .grid { grid-template-columns: repeat(2, 1fr); } }
    @media (max-width: 600px) { .grid { grid-template-columns: 1fr; } }

    .column { background: rgba(21, 28, 44, 0.4); border: 1px solid var(--card-border); border-radius: 14px; padding: 16px; display: flex; flex-direction: column; gap: 12px; }
    .column-header { display: flex; justify-content: space-between; align-items: center; font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-muted); padding-bottom: 8px; border-bottom: 2px solid var(--card-border); }
    .col-count { background: var(--card-border); color: var(--text-main); font-size: 11px; padding: 2px 8px; border-radius: 10px; }

    .card { background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 10px; padding: 14px; transition: all 0.2s ease; cursor: pointer; }
    .card:hover { border-color: var(--accent-blue); transform: translateY(-2px); box-shadow: 0 8px 20px rgba(0,0,0,0.3); }
    .card-title { font-size: 14px; font-weight: 700; margin-bottom: 6px; line-height: 1.4; color: var(--text-main); }
    .card-desc { font-size: 12px; color: var(--text-muted); margin-bottom: 12px; line-height: 1.5; }
    .card-footer { display: flex; justify-content: space-between; align-items: center; font-size: 11px; }
    .tag { font-weight: 600; padding: 3px 8px; border-radius: 6px; }
    .tag-todo { background: rgba(245, 158, 11, 0.15); color: var(--accent-amber); }
    .tag-progress { background: rgba(95, 179, 249, 0.15); color: var(--accent-blue); }
    .tag-cron { background: rgba(168, 85, 247, 0.15); color: var(--accent-purple); }
    .tag-done { background: rgba(16, 185, 129, 0.15); color: var(--accent-green); }
    .assignee { font-weight: 600; color: var(--text-muted); }
  </style>
</head>
<body>

  <header>
    <div class="title-group">
      <span class="title-badge">HERMES V2</span>
      <h1>Stefan's Kanban Board — Personal Workstream</h1>
    </div>
    <div class="status-pill">
      <span class="pulse-dot"></span> 6 Hermes Cores Active (Vercel Live)
    </div>
  </header>

  <div class="grid">
    <!-- COL 1 -->
    <div class="column">
      <div class="column-header">
        <span>📋 TODO / BACKLOG</span>
        <span class="col-count">3</span>
      </div>

      <div class="card">
        <div class="card-title">💳 Monobank Merchant Acquiring Token</div>
        <div class="card-desc">Подключение X-Token ФОП Монобанка для реальных списаний в грн на сайте.</div>
        <div class="card-footer">
          <span class="tag tag-todo">BACKLOG</span>
          <span class="assignee">👤 Stefan / Callum</span>
        </div>
      </div>

      <div class="card">
        <div class="card-title">🛍️ Silpo Weekly Groceries Order</div>
        <div class="card-desc">Еженедельная автосборка корзины Сільпо через Playwright Chromium (>1,700 UAH).</div>
        <div class="card-footer">
          <span class="tag tag-todo">PENDING</span>
          <span class="assignee">🤖 Hermes</span>
        </div>
      </div>

      <div class="card">
        <div class="card-title">🇩🇪 Hetzner Cloud VPS Migration</div>
        <div class="card-desc">Перенос 6 профилей Гермеса и крон-задач на серваки Hetzner для 24/7 автономии.</div>
        <div class="card-footer">
          <span class="tag tag-todo">PLANNED</span>
          <span class="assignee">🤖 Hermes Cluster</span>
        </div>
      </div>
    </div>

    <!-- COL 2 -->
    <div class="column">
      <div class="column-header">
        <span>⚡ IN PROGRESS</span>
        <span class="col-count">3</span>
      </div>

      <div class="card">
        <div class="card-title">🌐 Avalanche 3-Tier Pipeline</div>
        <div class="card-desc">Развертывание 3 контуров (aavalanche.com, staging, dev) в GitHub репозитории.</div>
        <div class="card-footer">
          <span class="tag tag-progress">ACTIVE</span>
          <span class="assignee">💻 Callum Vance</span>
        </div>
      </div>

      <div class="card">
        <div class="card-title">🚀 AI Project Evaluation & Price Graduation</div>
        <div class="card-desc">ИИ-оценка сложности проекта (10 уровней), конвертация валюты по IP и оплата.</div>
        <div class="card-footer">
          <span class="tag tag-progress">ACTIVE</span>
          <span class="assignee">💻 Callum Vance</span>
        </div>
      </div>

      <div class="card">
        <div class="card-title">🔑 User Auth & Admin Panel</div>
        <div class="card-desc">Регистрация, вход, Google/Facebook OAuth, Личный Кабинет и таблица пользователей.</div>
        <div class="card-footer">
          <span class="tag tag-progress">ACTIVE</span>
          <span class="assignee">💻 Callum Vance</span>
        </div>
      </div>
    </div>

    <!-- COL 3 -->
    <div class="column">
      <div class="column-header">
        <span>🔄 RECURRING / CRON TASKS</span>
        <span class="col-count">4</span>
      </div>

      <div class="card">
        <div class="card-title">📺 YouTube Watch Later Sorter</div>
        <div class="card-desc">Ежедневный разбор в 23:00 с сопоставлением со 49 реальными плейлистами YouTube.</div>
        <div class="card-footer">
          <span class="tag tag-cron">DAILY 23:00</span>
          <span class="assignee">🤖 Hermes DM</span>
        </div>
      </div>

      <div class="card">
        <div class="card-title">🌾 Memory Harvest Cron</div>
        <div class="card-desc">Ежедневная автосборка фактов и кейсов памяти memory_v2.</div>
        <div class="card-footer">
          <span class="tag tag-cron">DAILY 02:00</span>
          <span class="assignee">🤖 Hermes</span>
        </div>
      </div>

      <div class="card">
        <div class="card-title">🌲 Pinecone Vector Sync</div>
        <div class="card-desc">Ежедневный векторный синтез эмбеддингов в Pinecone.</div>
        <div class="card-footer">
          <span class="tag tag-cron">DAILY 03:00</span>
          <span class="assignee">🤖 Hermes</span>
        </div>
      </div>

      <div class="card">
        <div class="card-title">🏢 DP World Careers Vacancies Poller</div>
        <div class="card-desc">Ежедневный мониторинг новых вакансий DP World через Oracle Cloud HCM API.</div>
        <div class="card-footer">
          <span class="tag tag-cron">DAILY 09:00</span>
          <span class="assignee">🤖 Hermes DM ONLY</span>
        </div>
      </div>
    </div>

    <!-- COL 4 -->
    <div class="column">
      <div class="column-header">
        <span>✅ COMPLETED / DONE</span>
        <span class="col-count">5</span>
      </div>

      <div class="card">
        <div class="card-title">🤖 100% Multi-Agent Hermes Profiles</div>
        <div class="card-desc">Все 6 агентов (Orchestrator, Callum, Richard, Alistair, Liz, Ben) работают на ядре Гермеса!</div>
        <div class="card-footer">
          <span class="tag tag-done">VERIFIED</span>
          <span class="assignee">🤖 6 Cores Live</span>
        </div>
      </div>

      <div class="card">
        <div class="card-title">🌍 8 Multilingual Language Clones</div>
        <div class="card-desc">100% отзеркаливание верстки на 8 языков (es, de, fr, it, uk, ru, zh, ar) без сброса сессий.</div>
        <div class="card-footer">
          <span class="tag tag-done">VERIFIED</span>
          <span class="assignee">💻 Callum Vance</span>
        </div>
      </div>

      <div class="card">
        <div class="card-title">📧 Dual Branded Email Mailer</div>
        <div class="card-desc">Двойная отправка писем админу на dr.reenforce@gmail.com с info@aavalanche.com.</div>
        <div class="card-footer">
          <span class="tag tag-done">VERIFIED</span>
          <span class="assignee">💻 Callum Vance</span>
        </div>
      </div>

      <div class="card">
        <div class="card-title">🗺️ Drive & Desktop File Organization</div>
        <div class="card-desc">Наведен полный порядок на Диске и Рабочем столе с памяткой README_FILE_STRUCTURE.md.</div>
        <div class="card-footer">
          <span class="tag tag-done">VERIFIED</span>
          <span class="assignee">📈 Alistair Sterling</span>
        </div>
      </div>

      <div class="card">
        <div class="card-title">🔎 Google Search Console SEO Setup</div>
        <div class="card-desc">Загружен sitemap.xml для 9 языков и robots.txt, закрыты noindex dev/staging.</div>
        <div class="card-footer">
          <span class="tag tag-done">VERIFIED</span>
          <span class="assignee">🤖 Hermes</span>
        </div>
      </div>
    </div>
  </div>

</body>
</html>
"""

open(os.path.join(vercel_dir, "index.html"), "w", encoding="utf-8").write(kanban_html)

vercel_json = {
  "version": 2,
  "name": "stefan-kanban-board",
  "builds": [
    { "src": "index.html", "use": "@vercel/static" }
  ],
  "routes": [
    { "src": "/(.*)", "dest": "/index.html" }
  ]
}

open(os.path.join(vercel_dir, "vercel.json"), "w", encoding="utf-8").write(json.dumps(vercel_json, indent=2))

print("✅ Generated HTML and vercel.json for Vercel deployment!")

# Deploy via npx vercel
cmd = f'npx vercel "{vercel_dir}" --prod --yes --name stefan-kanban-board'
print('Running Vercel deployment:', cmd)

res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
print("STDOUT:", res.stdout)
print("STDERR:", res.stderr)
