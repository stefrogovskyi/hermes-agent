# -*- coding: utf-8 -*-
"""
build_standalone_prebaked_kanbans.py — Двусторонняя персистентная система 6 Канбан-бордов с автоматическим слиянием новых карточек с localStorage.
"""

import os, json, subprocess

agents_config = {
    "hermes": {
        "title": "Hermes Stevenson — Interactive Kanban Board",
        "badge": "HERMES ORCHESTRATOR",
        "bg": "#0B0F19",
        "card_bg": "#151C2C",
        "accent": "#3B82F6",
        "accent_secondary": "#10B981",
        "vercel_name": "hermes-stevenson-kanban",
        "cards": [
            {"id": "card_1", "column_id": "todo", "title": "💳 Monobank Merchant Acquiring Token Integration", "desc": "Подключение X-Token ФОП Монобанка для реальных списаний в грн на сайте.", "assignee": "👤 Stefan / Callum", "tag": "BACKLOG", "tag_class": "tag-todo"},
            {"id": "card_2", "column_id": "todo", "title": "🛍️ Silpo Weekly Groceries Order Assembly", "desc": "Еженедельная автосборка корзины Сільпо через Playwright Chromium (>1,700 UAH).", "assignee": "🤖 Hermes", "tag": "PENDING", "tag_class": "tag-todo"},
            {"id": "card_3", "column_id": "completed", "title": "🇩🇪 Hetzner / Servarica Master Node 24/7 Migration", "desc": "Перенос 6 профилей Гермеса и крон-задач на серваки Servarica для 24/7 автономии.", "assignee": "🤖 Hermes Cluster", "tag": "VERIFIED", "tag_class": "tag-done"},
            {"id": "card_4", "column_id": "completed", "title": "🌐 Avalanche Agency 3-Tier Pipeline", "desc": "Синхронизация dev.aavalanche.com, staging и prod под управлением GitHub.", "assignee": "💻 Callum Vance", "tag": "VERIFIED", "tag_class": "tag-done"},
            {"id": "card_5", "column_id": "completed", "title": "🚀 AI Project Evaluation & 10-Point Price Graduation", "desc": "ИИ-оценка сложности проекта по 10 уровням, конвертация валюты по IP и модалка оплаты.", "assignee": "💻 Callum Vance", "tag": "VERIFIED", "tag_class": "tag-done"},
            {"id": "card_6", "column_id": "completed", "title": "🔑 User Auth, Personal Cabinet & Admin Panel", "desc": "Регистрация, вход, Google/Facebook OAuth, Личный Кабинет и таблица пользователей.", "assignee": "💻 Callum Vance", "tag": "VERIFIED", "tag_class": "tag-done"},
            {"id": "card_7", "column_id": "recurring", "title": "📺 YouTube Watch Later Daily Sorter", "desc": "Ежедневный разбор в 23:00 с сопоставлением со 49 реальными плейлистами YouTube.", "assignee": "🤖 Hermes DM", "tag": "DAILY 23:00", "tag_class": "tag-cron"},
            {"id": "card_8", "column_id": "recurring", "title": "🌾 Memory Harvest Cron", "desc": "Ежедневная автосборка фактов и кейсов памяти memory_v2 в 02:00 MSK.", "assignee": "🤖 Hermes", "tag": "DAILY 02:00", "tag_class": "tag-cron"},
            {"id": "card_9", "column_id": "recurring", "title": "🌲 Pinecone Vector Memory Sync", "desc": "Ежедневный векторный синтез эмбеддингов в Pinecone в 03:00 MSK.", "assignee": "🤖 Hermes", "tag": "DAILY 03:00", "tag_class": "tag-cron"},
            {"id": "card_10", "column_id": "recurring", "title": "🏢 Global C-Level & Leadership Career Scanner", "desc": "Ежедневный мониторинг 32 гигантов (AI, Tech, Freight) на C-Level роли в 09:00 MSK.", "assignee": "🤖 Hermes DM ONLY", "tag": "DAILY 09:00", "tag_class": "tag-cron"},
            {"id": "card_11", "column_id": "completed", "title": "🤖 100% Multi-Agent Hermes Profiles Cluster", "desc": "Все 6 агентов (Orchestrator, Callum, Richard, Alistair, Liz, Ben) работают на ядре Гермеса!", "assignee": "🤖 6 Cores Live", "tag": "VERIFIED", "tag_class": "tag-done"},
            {"id": "card_12", "column_id": "completed", "title": "🌍 8 Multilingual Language Clones", "desc": "100% отзеркаливание верстки на 8 языков (es, de, fr, it, uk, ru, zh, ar) без сброса сессий.", "assignee": "💻 Callum Vance", "tag": "VERIFIED", "tag_class": "tag-done"},
            {"id": "card_13", "column_id": "completed", "title": "📧 Dual Branded Email Mailer", "desc": "Двойная отправка писем админу на dr.reenforce@gmail.com с info@aavalanche.com.", "assignee": "💻 Callum Vance", "tag": "VERIFIED", "tag_class": "tag-done"},
            {"id": "card_14", "column_id": "completed", "title": "🗺️ Drive & Desktop File Organization", "desc": "Наведен полный порядок на Диске и Рабочем столе с памяткой README_FILE_STRUCTURE.md.", "assignee": "📈 Alistair Sterling", "tag": "VERIFIED", "tag_class": "tag-done"},
            {"id": "card_15", "column_id": "completed", "title": "🔎 Google Search Console SEO Setup", "desc": "Загружен sitemap.xml для 9 языков и robots.txt, закрыты noindex dev/staging.", "assignee": "🤖 Hermes", "tag": "VERIFIED", "tag_class": "tag-done"},
            {"id": "card_16", "column_id": "in_progress", "title": "📡 Telegram Userbot & Private Channel Listener", "desc": "24/7 Чтение сигналов из канала «Не повредит, Одесса» через сессию @stefrogovskiy с точным временем (ЧЧ:ММ).", "assignee": "🤖 Hermes Userbot", "tag": "ACTIVE 24/7", "tag_class": "tag-progress"},
            {"id": "card_17", "column_id": "completed", "title": "📚 MindCloud Universal API Reference Library", "desc": "Развернута и локализована оффлайн-база 3,122+ API / 75k+ эндпоинтов для всех 6 профилей.", "assignee": "🤖 Hermes Skill", "tag": "VERIFIED", "tag_class": "tag-done"},
            {"id": "card_18", "column_id": "completed", "title": "🛡️ Ecosystem 30s Timeout & Context Compression", "desc": "Включен 30s таймаут вызовов моделей и 25% авто-сжатие контекста во всех 6 профилях.", "assignee": "🤖 All Cores", "tag": "VERIFIED", "tag_class": "tag-done"},
            {"id": "card_19", "column_id": "in_progress", "title": "💬 Telegram Group Silence & Bot Loop Shield", "desc": "Правило require_mention: true, отсечение бот-бот перепалок и молчание в групповых чатах.", "assignee": "🤖 All Bots", "tag": "POLICY ACTIVE", "tag_class": "tag-progress"},
            {"id": "card_20", "column_id": "completed", "title": "🔄 Multi-Agent Bidirectional Vercel Sync", "desc": "Двусторонняя передача статусов, меток времени перемещений и комментариев через dev.aavalanche.com/kanban_api.php.", "assignee": "💻 Callum / Hermes", "tag": "VERIFIED", "tag_class": "tag-done"},
            {"id": "card_21", "column_id": "recurring", "title": "🔔 Daily Ecosystem Self-Heal & Audit (04:00 AM)", "desc": "Автоматическая проверка самочувствия всех 5 ботов, токенов и интеграций в 04:00 AM.", "assignee": "🤖 Hermes Watchdog", "tag": "DAILY 04:00", "tag_class": "tag-cron"},
            {"id": "card_22", "column_id": "recurring", "title": "📂 Daily Full Reality & Google Workspace Indexer", "desc": "Ежедневная дифференциальная индексация файлов и документов Google Диска в FTS5 базу.", "assignee": "🤖 Hermes Indexer", "tag": "DAILY 04:00", "tag_class": "tag-cron"},
            {"id": "card_23", "column_id": "recurring", "title": "📊 Daily 08:00 AM Kanban Review & Brief", "desc": "Ежедневный утренний сканер движений карточек и комментариев Стефана на 6 канбанах.", "assignee": "🤖 Hermes Brief", "tag": "DAILY 08:00", "tag_class": "tag-cron"}
        ]
    },
    "ben": {
        "title": "Ben Jett — Marketing & Growth Agency Kanban",
        "badge": "BEN GROWTH MARKETING",
        "bg": "#140A05",
        "card_bg": "#24130A",
        "accent": "#FF6B00",
        "accent_secondary": "#F59E0B",
        "vercel_name": "ben-kanban",
        "cards": [
            {"id": "c_b1", "column_id": "todo", "title": "🎯 Avalanche Agency PPC & Social Campaigns", "desc": "Запуск лидогенерационных кампаний в LinkedIn и Google Ads для B2B клиентов.", "assignee": "🚀 Ben Jett", "tag": "CAMPAIGN", "tag_class": "tag-todo"},
            {"id": "c_b2", "column_id": "in_progress", "title": "🔥 Avalanche Redesign Landing Conversion Test", "desc": "А/Б тестирование высокой конверсии обновленного темного лендинга.", "assignee": "🚀 Ben Jett", "tag": "TESTING", "tag_class": "tag-progress"},
            {"id": "c_b3", "column_id": "recurring", "title": "🤖 Ben Bot Watchdog Ping", "desc": "Автоматическая проверка доступности и пинг маркетинг-бота каждые 10 минут.", "assignee": "🚀 Ben Jett", "tag": "CRON 10M", "tag_class": "tag-cron"},
            {"id": "c_b4", "column_id": "completed", "title": "🔎 Google Search Console & Sitemap Indexing", "desc": "Загрузка мульти-язычных свайпов sitemap.xml и SEO-оптимизация.", "assignee": "🚀 Ben Jett", "tag": "VERIFIED", "tag_class": "tag-done"}
        ]
    },
    "richard": {
        "title": "Richard Marlowe — B2B Sales & Pipeline Kanban",
        "badge": "RICHARD SALES",
        "bg": "#0F172A",
        "card_bg": "#1E293B",
        "accent": "#F59E0B",
        "accent_secondary": "#10B981",
        "vercel_name": "richard-kanban",
        "cards": [
            {"id": "c_r1", "column_id": "todo", "title": "💼 $200k/day Rev Target Outreach", "desc": "Подготовка персональных КП по TrackingMCP & FreightRatesMCP для крупных логистических хабов.", "assignee": "💼 Richard Marlowe", "tag": "HIGH PRIORITY", "tag_class": "tag-todo"},
            {"id": "c_r2", "column_id": "in_progress", "title": "📊 SeaRates vs TrackingMCP Benchmark", "desc": "Авто-сравнение 10 трекинг-запросов между SeaRates и TrackingMCP раз в 3 дня.", "assignee": "💼 Richard Marlowe", "tag": "ACTIVE 3-DAY", "tag_class": "tag-progress"},
            {"id": "c_r3", "column_id": "recurring", "title": "🌐 Site & Inbound Email Scanner", "desc": "Сканирование входящей почты на info@aavalanche.com и запросов цен раз в 3 дня.", "assignee": "💼 Richard Marlowe", "tag": "CRON 3-DAY", "tag_class": "tag-cron"},
            {"id": "c_r4", "column_id": "completed", "title": "🔒 Token & Email Privacy Guardrail", "desc": "Фиксация персонального бота @richnavobot (8846249306) без CC/BCC дублей.", "assignee": "💼 Richard Marlowe", "tag": "VERIFIED", "tag_class": "tag-done"}
        ]
    },
    "callum": {
        "title": "Callum Vance — Engineering & Infrastructure Kanban",
        "badge": "CALLUM TECH LEAD",
        "bg": "#030712",
        "card_bg": "#111827",
        "accent": "#0EA5E9",
        "accent_secondary": "#6366F1",
        "vercel_name": "callum-kanban",
        "cards": [
            {"id": "c_c1", "column_id": "todo", "title": "💳 Monobank Acquiring X-Token Integration", "desc": "Интеграция эквайринга Монобанка для автоматической оплаты пакетов услуг.", "assignee": "💻 Callum Vance", "tag": "BACKLOG", "tag_class": "tag-todo"},
            {"id": "c_c2", "column_id": "in_progress", "title": "🚀 AI Project Evaluation & 10-Point Price Graduation", "desc": "ИИ-оценка сложности проекта по 10 уровням, конвертация валюты по IP и модалка оплаты.", "assignee": "💻 Callum Vance", "tag": "IN DEV", "tag_class": "tag-progress"},
            {"id": "c_c3", "column_id": "recurring", "title": "🔄 Git Autosync 3 Repos", "desc": "Авто-синхронизация репозиториев, скиллов и памяти каждые 30 минут.", "assignee": "💻 Callum Vance", "tag": "CRON 30M", "tag_class": "tag-cron"},
            {"id": "c_c4", "column_id": "completed", "title": "🌐 8 Multilingual Language Clones", "desc": "Полное версточное отзеркаливание сайта Avalanche на 8 языков без потери качества.", "assignee": "💻 Callum Vance", "tag": "VERIFIED", "tag_class": "tag-done"}
        ]
    },
    "alistair": {
        "title": "Alistair Sterling — Operations & Strategy Kanban",
        "badge": "ALISTAIR OPERATIONS",
        "bg": "#0D0914",
        "card_bg": "#181124",
        "accent": "#8B5CF6",
        "accent_secondary": "#EC4899",
        "vercel_name": "alistair-kanban",
        "cards": [
            {"id": "c_a1", "column_id": "todo", "title": "📈 Navo24 Growth Strategy $1B Valuation", "desc": "Разработка операционных регламентов для масштабирования 100 сделок/день по $2k.", "assignee": "📈 Alistair Sterling", "tag": "STRATEGY", "tag_class": "tag-todo"},
            {"id": "c_a2", "column_id": "in_progress", "title": "🔄 Navo24 24/7 Autonomous OODA Growth Cycle", "desc": "Ежедневный цикл анализа метрик, гипотез и роста в 06:00 AM.", "assignee": "📈 Alistair Sterling", "tag": "OODA ACTIVE", "tag_class": "tag-progress"},
            {"id": "c_a3", "column_id": "recurring", "title": "📊 Daily Kanban Sync (07:00)", "desc": "Утренний сверка статусов всех канбан-досок команд в 07:00 AM.", "assignee": "📈 Alistair Sterling", "tag": "DAILY 07:00", "tag_class": "tag-cron"},
            {"id": "c_a4", "column_id": "completed", "title": "🗺️ Drive & Desktop File Structure Audit", "desc": "Организация структуры Google Диска и ПК с памяткой README_FILE_STRUCTURE.md.", "assignee": "📈 Alistair Sterling", "tag": "VERIFIED", "tag_class": "tag-done"}
        ]
    },
    "liz": {
        "title": "Liz Harper — HR & Internal Comms Kanban",
        "badge": "LIZ HR & COMMS",
        "bg": "#120A0F",
        "card_bg": "#1F121A",
        "accent": "#F43F5E",
        "accent_secondary": "#FB7185",
        "vercel_name": "liz-kanban",
        "cards": [
            {"id": "c_l1", "column_id": "todo", "title": "👥 Digital & Human Team Synergy Handbook", "desc": "Создание руководства по совместной работе 10 людей и 10 цифровых агентов.", "assignee": "🤝 Liz Harper", "tag": "HR POLICY", "tag_class": "tag-todo"},
            {"id": "c_l2", "column_id": "in_progress", "title": "💬 Internal Telegram Comms & Onboarding", "desc": "Мониторинг климата в команде и настройка быстрых авто-ответов сотрудникам.", "assignee": "🤝 Liz Harper", "tag": "ACTIVE", "tag_class": "tag-progress"},
            {"id": "c_l3", "column_id": "recurring", "title": "🔔 Ecosystem Self-Heal & Team Health Check", "desc": "Проверка самочувствия и доступности всех 5 ботов команды в 04:00 AM.", "assignee": "🤝 Liz Harper", "tag": "DAILY 04:00", "tag_class": "tag-cron"},
            {"id": "c_l4", "column_id": "completed", "title": "📧 Dual Branded Email Mailer Setup", "desc": "Двойная отправка писем админам на dr.reenforce@gmail.com с брендовых почт.", "assignee": "🤝 Liz Harper", "tag": "VERIFIED", "tag_class": "tag-done"}
        ]
    }
}

def render_cards_html(cards, col_id):
    col_cards = [c for c in cards if c.get("column_id") == col_id]
    html = ""
    for c in col_cards:
        moved_str = f"<div style='font-size:10px; color:#64748B; margin-top:4px;'>🕒 Перемещено: {c.get('moved_at')}</div>" if c.get('moved_at') else ""
        comments_cnt = len(c.get('comments', []))
        comm_str = f"<span style='font-size:11px; color:#3B82F6;'>💬 {comments_cnt}</span>" if comments_cnt > 0 else ""
        
        html += f"""
        <div class="card" draggable="true" id="card-el-{c['id']}" ondragstart="handleDragStart(event, '{c['id']}')" onclick="openEditModal('{c['id']}')">
          <div class="card-title">{c['title']}</div>
          <div class="card-desc">{c['desc']}</div>
          {moved_str}
          <div class="card-footer">
            <span class="tag {c.get('tag_class', 'tag-todo')}">{c.get('tag', 'TASK')}</span>
            <span class="assignee">{c.get('assignee', '')} {comm_str}</span>
          </div>
        </div>
        """
    return html, len(col_cards)

def generate_standalone_html(agent, cfg):
    cards = cfg["cards"]
    
    todo_html, todo_cnt = render_cards_html(cards, "todo")
    prog_html, prog_cnt = render_cards_html(cards, "in_progress")
    rec_html, rec_cnt = render_cards_html(cards, "recurring")
    done_html, done_cnt = render_cards_html(cards, "completed")

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <meta http-equiv="Content-Language" content="ru">
  <meta name="google" content="notranslate">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{cfg['title']}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: {cfg['bg']};
      --card-bg: {cfg['card_bg']};
      --card-border: rgba(255, 255, 255, 0.12);
      --text-main: #F8FAFC;
      --text-muted: #94A3B8;
      --accent: {cfg['accent']};
      --accent-sec: {cfg['accent_secondary']};
      --accent-blue: #5FB3F9;
      --accent-green: #10B981;
      --accent-purple: #A855F7;
      --accent-amber: #F59E0B;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Plus Jakarta Sans', sans-serif; }}
    body {{ background-color: var(--bg); color: var(--text-main); min-height: 100vh; padding: 24px; padding-bottom: 40px; }}
    
    header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid var(--card-border); flex-wrap: wrap; gap: 12px; }}
    .title-group {{ display: flex; align-items: center; gap: 12px; }}
    .title-badge {{ background: linear-gradient(135deg, var(--accent), var(--accent-sec)); color: #FFF; font-weight: 800; font-size: 13px; padding: 6px 12px; border-radius: 8px; text-transform: uppercase; }}
    h1 {{ font-size: 20px; font-weight: 800; letter-spacing: -0.5px; }}
    
    .btn-header {{ background: var(--accent); color: #FFF; border: none; padding: 10px 20px; border-radius: 10px; font-weight: 800; cursor: pointer; font-size: 14px; box-shadow: 0 4px 14px rgba(0,0,0,0.4); transition: all 0.2s; }}
    .btn-header:hover {{ opacity: 0.9; transform: translateY(-1px); }}

    .grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }}
    @media (max-width: 1200px) {{ .grid {{ grid-template-columns: repeat(2, 1fr); }} }}
    @media (max-width: 600px) {{ .grid {{ grid-template-columns: 1fr; }} }}

    .column {{ background: rgba(255, 255, 255, 0.03); border: 1px solid var(--card-border); border-radius: 14px; padding: 16px; display: flex; flex-direction: column; gap: 12px; min-height: 600px; transition: background 0.2s; }}
    .column.drag-over {{ background: rgba(255, 255, 255, 0.08); border-color: var(--accent); }}
    .column-header {{ display: flex; justify-content: space-between; align-items: center; font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-muted); padding-bottom: 8px; border-bottom: 2px solid var(--card-border); }}
    .col-count {{ background: rgba(255, 255, 255, 0.1); color: var(--text-main); font-size: 11px; padding: 2px 8px; border-radius: 10px; }}

    .cards-container {{ display: flex; flex-direction: column; gap: 12px; min-height: 200px; }}

    .card {{ background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 10px; padding: 14px; transition: all 0.2s ease; cursor: grab; position: relative; }}
    .card:active {{ cursor: grabbing; opacity: 0.6; }}
    .card:hover {{ border-color: var(--accent); transform: translateY(-2px); box-shadow: 0 8px 20px rgba(0,0,0,0.3); }}
    .card-title {{ font-size: 14px; font-weight: 700; margin-bottom: 6px; line-height: 1.4; color: var(--text-main); }}
    .card-desc {{ font-size: 12px; color: var(--text-muted); margin-bottom: 12px; line-height: 1.5; }}
    .card-footer {{ display: flex; justify-content: space-between; align-items: center; font-size: 11px; margin-top: 8px; }}

    .tag {{ font-weight: 600; padding: 3px 8px; border-radius: 6px; }}
    .tag-todo {{ background: rgba(245, 158, 11, 0.15); color: var(--accent-amber); }}
    .tag-progress {{ background: rgba(95, 179, 249, 0.15); color: var(--accent-blue); }}
    .tag-cron {{ background: rgba(168, 85, 247, 0.15); color: var(--accent-purple); }}
    .tag-done {{ background: rgba(16, 185, 129, 0.15); color: var(--accent-green); }}

    /* MODALS */
    .modal-overlay {{ position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.85); backdrop-filter: blur(6px); display: none; justify-content: center; align-items: center; z-index: 10000; }}
    .modal-box {{ background: var(--card-bg); border: 1px solid var(--card-border); width: 90%; max-width: 600px; border-radius: 16px; padding: 24px; box-shadow: 0 20px 50px rgba(0,0,0,0.6); max-height: 90vh; overflow-y: auto; }}
    .modal-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }}
    .modal-close {{ background: none; border: none; color: var(--text-muted); font-size: 22px; cursor: pointer; }}
    
    .input-field {{ width: 100%; background: rgba(0,0,0,0.4); border: 1px solid var(--card-border); border-radius: 8px; padding: 12px; color: #FFF; font-size: 14px; outline: none; margin-bottom: 12px; }}
    .input-field:focus {{ border-color: var(--accent); }}
    
    .comment-item {{ background: rgba(255,255,255,0.05); padding: 8px 12px; border-radius: 8px; font-size: 12px; margin-bottom: 6px; }}
  </style>
</head>
<body>

  <header>
    <div class="title-group">
      <span class="title-badge">{cfg['badge']}</span>
      <h1>{cfg['title']}</h1>
    </div>
    <button class="btn-header" onclick="openNewModal()">+ Новая Задача</button>
  </header>

  <div class="grid" id="kanban-grid">
    <!-- COL 1 -->
    <div class="column" data-col="todo" ondragover="event.preventDefault();this.classList.add('drag-over');" ondragleave="this.classList.remove('drag-over');" ondrop="handleDrop(event,'todo',this)">
      <div class="column-header"><span>📋 TODO / BACKLOG</span><span class="col-count" id="cnt-todo">{todo_cnt}</span></div>
      <div class="cards-container" id="cards-todo">{todo_html}</div>
    </div>

    <!-- COL 2 -->
    <div class="column" data-col="in_progress" ondragover="event.preventDefault();this.classList.add('drag-over');" ondragleave="this.classList.remove('drag-over');" ondrop="handleDrop(event,'in_progress',this)">
      <div class="column-header"><span>⚡ IN PROGRESS</span><span class="col-count" id="cnt-in_progress">{prog_cnt}</span></div>
      <div class="cards-container" id="cards-in_progress">{prog_html}</div>
    </div>

    <!-- COL 3 -->
    <div class="column" data-col="recurring" ondragover="event.preventDefault();this.classList.add('drag-over');" ondragleave="this.classList.remove('drag-over');" ondrop="handleDrop(event,'recurring',this)">
      <div class="column-header"><span>🔄 RECURRING / CRON</span><span class="col-count" id="cnt-recurring">{rec_cnt}</span></div>
      <div class="cards-container" id="cards-recurring">{rec_html}</div>
    </div>

    <!-- COL 4 -->
    <div class="column" data-col="completed" ondragover="event.preventDefault();this.classList.add('drag-over');" ondragleave="this.classList.remove('drag-over');" ondrop="handleDrop(event,'completed',this)">
      <div class="column-header"><span>✅ COMPLETED / DONE</span><span class="col-count" id="cnt-completed">{done_cnt}</span></div>
      <div class="cards-container" id="cards-completed">{done_html}</div>
    </div>
  </div>

  <!-- NEW TASK MODAL -->
  <div class="modal-overlay" id="new-modal">
    <div class="modal-box">
      <div class="modal-header">
        <h2 style="font-size: 16px; font-weight: 800;">+ Добавить Задачу для {cfg['badge']}</h2>
        <button class="modal-close" onclick="closeNewModal()">✕</button>
      </div>
      <input type="text" id="new-title" class="input-field" placeholder="Название задачи">
      <textarea id="new-desc" class="input-field" rows="3" placeholder="Подробное описание задачи..."></textarea>
      <select id="new-col" class="input-field">
        <option value="todo">📋 TODO / BACKLOG</option>
        <option value="in_progress">⚡ IN PROGRESS</option>
        <option value="recurring">🔄 RECURRING / CRON</option>
        <option value="completed">✅ COMPLETED / DONE</option>
      </select>
      <button class="btn-header" style="width: 100%; margin-top: 8px;" onclick="createNewTask()">Создать и Поставить ➔</button>
    </div>
  </div>

  <!-- EDIT / COMMENT CARD MODAL -->
  <div class="modal-overlay" id="edit-modal">
    <div class="modal-box">
      <div class="modal-header">
        <h2 style="font-size: 16px; font-weight: 800;" id="edit-modal-title">Редактирование задачи</h2>
        <button class="modal-close" onclick="closeEditModal()">✕</button>
      </div>
      <input type="hidden" id="edit-card-id">
      <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 12px;" id="edit-card-moved-at"></div>
      
      <label style="font-size: 12px; font-weight: 700; color: var(--text-muted);">Заголовок:</label>
      <input type="text" id="edit-title" class="input-field">
      
      <label style="font-size: 12px; font-weight: 700; color: var(--text-muted);">Описание:</label>
      <textarea id="edit-desc" class="input-field" rows="3"></textarea>
      
      <label style="font-size: 12px; font-weight: 700; color: var(--text-muted);">💬 Комментарии:</label>
      <div id="edit-comments-list" style="margin-bottom: 12px;"></div>
      
      <div style="display: flex; gap: 8px;">
        <input type="text" id="edit-new-comment" class="input-field" placeholder="Добавить комментарий..." style="margin-bottom:0;">
        <button class="btn-header" style="white-space: nowrap;" onclick="addCommentToCard()">Отправить</button>
      </div>
      
      <button class="btn-header" style="width: 100%; margin-top: 16px;" onclick="saveCardEdits()">Сохранить изменения ➔</button>
    </div>
  </div>

  <script>
    const AGENT = '{agent}';
    const API_URL = 'https://dev.aavalanche.com/kanban_api.php?agent=' + AGENT;
    const DEFAULT_CARDS = {json.dumps(cards, ensure_ascii=False)};
    let currentState = {{ "cards": DEFAULT_CARDS, "activity": [] }};
    let draggedCardId = null;

    function mergeCards(serverCards, defaultCards) {{
      const map = new Map();
      // Add server/local cards first
      if (serverCards && Array.isArray(serverCards)) {{
        serverCards.forEach(c => map.set(c.id, c));
      }}
      // Merge missing default cards
      defaultCards.forEach(c => {{
        if (!map.has(c.id)) {{
          map.set(c.id, c);
        }}
      }});
      return Array.from(map.values());
    }}

    function getLocalState() {{
      try {{
        const raw = localStorage.getItem('kanban_state_v23_' + AGENT);
        if (!raw) return null;
        const parsed = JSON.parse(raw);
        if (parsed && parsed.cards) {{
          parsed.cards = mergeCards(parsed.cards, DEFAULT_CARDS);
          return parsed;
        }}
        return null;
      }} catch(e) {{ return null; }}
    }}

    function setLocalState(state) {{
      try {{
        localStorage.setItem('kanban_state_v23_' + AGENT, JSON.stringify(state));
        syncWithBackend(state);
      }} catch(e) {{}}
    }}

    async function syncWithBackend(state) {{
      try {{
        await fetch(API_URL, {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify(state)
        }});
      }} catch(e) {{}}
    }}

    async function fetchFromBackend() {{
      try {{
        const res = await fetch(API_URL);
        const data = await res.json();
        if (data && data.cards && data.cards.length > 0) {{
          data.cards = mergeCards(data.cards, DEFAULT_CARDS);
          currentState = data;
          setLocalState(currentState);
          renderBoard();
        }}
      }} catch(e) {{}}
    }}

    function renderBoard() {{
      if (!currentState || !currentState.cards) return;
      const cols = {{
        'todo': [],
        'in_progress': [],
        'recurring': [],
        'completed': []
      }};

      currentState.cards.forEach(c => {{
        if (cols[c.column_id]) cols[c.column_id].push(c);
      }});

      Object.keys(cols).forEach(colId => {{
        const container = document.getElementById('cards-' + colId);
        const countEl = document.getElementById('cnt-' + colId);
        if (!container) return;

        let cardsHtml = '';
        cols[colId].forEach(c => {{
          const movedStr = c.moved_at ? `<div style="font-size:10px; color:#64748B; margin-top:4px;">🕒 Перемещено: ${{c.moved_at}}</div>` : '';
          const commentsCnt = c.comments ? c.comments.length : 0;
          const commStr = commentsCnt > 0 ? `<span style="font-size:11px; color:#3B82F6;">💬 ${{commentsCnt}}</span>` : '';

          cardsHtml += `
            <div class="card" draggable="true" id="card-el-${{c.id}}" ondragstart="handleDragStart(event, '${{c.id}}')" onclick="openEditModal('${{c.id}}')">
              <div class="card-title">${{c.title}}</div>
              <div class="card-desc">${{c.desc}}</div>
              ${{movedStr}}
              <div class="card-footer">
                <span class="tag ${{c.tag_class || 'tag-todo'}}">${{c.tag || 'TASK'}}</span>
                <span class="assignee">${{c.assignee || AGENT}} ${{commStr}}</span>
              </div>
            </div>
          `;
        }});
        container.innerHTML = cardsHtml;
        if (countEl) countEl.innerText = cols[colId].length;
      }});
    }}

    function handleDragStart(e, cardId) {{
      draggedCardId = cardId;
      e.dataTransfer.setData('text/plain', cardId);
    }}

    function handleDrop(e, targetColId, colEl) {{
      e.preventDefault();
      colEl.classList.remove('drag-over');
      if (!draggedCardId || !currentState) return;

      const card = currentState.cards.find(c => c.id === draggedCardId);
      if (card && card.column_id !== targetColId) {{
        const nowStr = new Date().toLocaleString("ru-RU", {{ timeZone: "Europe/Kiev" }});
        const oldCol = card.column_id;
        card.column_id = targetColId;
        card.moved_at = nowStr;

        if (!currentState.activity) currentState.activity = [];
        currentState.activity.push({{
          action: "moved",
          card_id: card.id,
          title: card.title,
          from: oldCol,
          to: targetColId,
          timestamp: nowStr,
          user: "Stefan"
        }});

        setLocalState(currentState);
        renderBoard();
      }}
      draggedCardId = null;
    }}

    function openNewModal() {{ document.getElementById('new-modal').style.display = 'flex'; }}
    function closeNewModal() {{ document.getElementById('new-modal').style.display = 'none'; }}

    function openEditModal(cardId) {{
      const card = currentState.cards.find(c => c.id === cardId);
      if (!card) return;

      document.getElementById('edit-card-id').value = card.id;
      document.getElementById('edit-title').value = card.title;
      document.getElementById('edit-desc').value = card.desc;
      document.getElementById('edit-card-moved-at').innerText = card.moved_at ? '🕒 Последнее перемещение: ' + card.moved_at : '';

      const commList = document.getElementById('edit-comments-list');
      commList.innerHTML = '';
      if (card.comments && card.comments.length > 0) {{
        card.comments.forEach(cm => {{
          commList.innerHTML += `<div class="comment-item"><b>${{cm.author || 'Stefan'}}</b> (${{cm.timestamp}}): ${{cm.text}}</div>`;
        }});
      }} else {{
        commList.innerHTML = '<div style="font-size:12px; color:var(--text-muted);">Комментариев пока нет</div>';
      }}

      document.getElementById('edit-modal').style.display = 'flex';
    }}

    function closeEditModal() {{ document.getElementById('edit-modal').style.display = 'none'; }}

    function addCommentToCard() {{
      const cardId = document.getElementById('edit-card-id').value;
      const text = document.getElementById('edit-new-comment').value.trim();
      if (!text) return;

      const card = currentState.cards.find(c => c.id === cardId);
      if (card) {{
        if (!card.comments) card.comments = [];
        const nowStr = new Date().toLocaleString("ru-RU", {{ timeZone: "Europe/Kiev" }});
        card.comments.push({{ author: "Stefan", text: text, timestamp: nowStr }});
        
        document.getElementById('edit-new-comment').value = '';
        setLocalState(currentState);
        openEditModal(cardId);
        renderBoard();
      }}
    }}

    function saveCardEdits() {{
      const cardId = document.getElementById('edit-card-id').value;
      const card = currentState.cards.find(c => c.id === cardId);
      if (card) {{
        card.title = document.getElementById('edit-title').value.trim();
        card.desc = document.getElementById('edit-desc').value.trim();
        setLocalState(currentState);
        renderBoard();
        closeEditModal();
      }}
    }}

    function createNewTask() {{
      const title = document.getElementById('new-title').value.trim();
      const desc = document.getElementById('new-desc').value.trim();
      const col = document.getElementById('new-col').value;
      if (!title) return alert('Укажите название задачи!');

      const nowStr = new Date().toLocaleString("ru-RU", {{ timeZone: "Europe/Kiev" }});

      const newCard = {{
        id: 'card_' + Date.now(),
        column_id: col,
        title: title,
        desc: desc,
        assignee: AGENT,
        tag: 'NEW',
        tag_class: 'tag-todo',
        moved_at: nowStr,
        comments: []
      }};

      currentState.cards.push(newCard);
      setLocalState(currentState);
      renderBoard();
      closeNewModal();
      document.getElementById('new-title').value = '';
      document.getElementById('new-desc').value = '';
    }}

    // Check LocalStorage and Backend on load
    const local = getLocalState();
    if (local && local.cards && local.cards.length > 0) {{
      currentState = local;
      renderBoard();
    }} else {{
      setLocalState(currentState);
    }}
    
    // Fetch background updates from API
    fetchFromBackend();
  </script>
</body>
</html>
"""

# Build and Deploy for each agent
v_token = "vcp_2QMSKEwYW3Dg4vdKOTB8q7IRCr2uCEFWeXgVMDAr18jPnuhEKf0KYAYO"
v_team = "navo5"

for agent, cfg in agents_config.items():
    html_content = generate_standalone_html(agent, cfg)
    
    # Write to local vercel dir
    v_dir = f"/tmp/_vercel_kanban_{agent}"
    os.makedirs(v_dir, exist_ok=True)
    open(os.path.join(v_dir, "index.html"), "w", encoding="utf-8").write(html_content)
    
    v_json = {
        "version": 2,
        "builds": [{"src": "index.html", "use": "@vercel/static"}],
        "routes": [{"src": "/(.*)", "dest": "/index.html"}],
        "headers": [
            {
                "source": "/(.*)",
                "headers": [
                    {"key": "Content-Type", "value": "text/html; charset=utf-8"},
                    {"key": "Content-Language", "value": "ru"}
                ]
            }
        ]
    }
    open(os.path.join(v_dir, "vercel.json"), "w", encoding="utf-8").write(json.dumps(v_json, indent=2))
    
    # Deploy to Vercel
    cmd = f"VERCEL_TOKEN={v_token} vercel \"{v_dir}\" --prod --yes --scope {v_team}"
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    url = res.stdout.strip()
    print(f"✅ Deployed auto-merge {agent.upper()} ({len(cfg['cards'])} cards) -> Vercel: {url}")

    # Re-alias hermes-stevenson-kanban explicitly
    if agent == "hermes":
        cmd_a = f"VERCEL_TOKEN={v_token} vercel alias set {url} hermes-stevenson-kanban.vercel.app --scope {v_team}"
        subprocess.run(cmd_a, shell=True, capture_output=True, text=True)
        print("✅ Re-aliased hermes-stevenson-kanban.vercel.app")
    elif agent == "ben":
        cmd_b = f"VERCEL_TOKEN={v_token} vercel alias set {url} vercelkanbanben.vercel.app --scope {v_team}"
        subprocess.run(cmd_b, shell=True, capture_output=True, text=True)
