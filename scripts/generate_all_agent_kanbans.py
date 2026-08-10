# -*- coding: utf-8 -*-
"""
generate_all_agent_kanbans.py — Генерация и развертывание 6 интерактивных Канбан-бордов со спасенным от откатов Drag-and-Drop state persistence!
"""

import os, json, paramiko, subprocess

agents_config = {
    "hermes": {
        "title": "Hermes Stevenson — Main Orchestration Kanban",
        "badge": "HERMES ORCHESTRATOR",
        "bg": "#0B0F19",
        "card_bg": "#151C2C",
        "accent": "#3B82F6",
        "accent_secondary": "#10B981",
        "cards": [
            {"id": "c_h1", "column_id": "todo", "title": "🛍️ Silpo Weekly Groceries Order", "desc": "Еженедельная автосборка корзины Сільпо через Playwright Chromium (>1,700 UAH).", "assignee": "🤖 Hermes", "tag": "PENDING", "tag_class": "tag-todo"},
            {"id": "c_h2", "column_id": "in_progress", "title": "🖥️ Servarica Master Node 24/7 Autonomy", "desc": "Полный перенос 6 профилей Гермеса и вочдогов на Серварику.", "assignee": "🤖 Hermes Cluster", "tag": "ACTIVE", "tag_class": "tag-progress"},
            {"id": "c_h3", "column_id": "recurring", "title": "📺 YouTube Watch Later Sorter", "desc": "Ежедневный разбор в 23:00 со 49 реальными плейлистами YouTube.", "assignee": "🤖 Hermes DM", "tag": "DAILY 23:00", "tag_class": "tag-cron"},
            {"id": "c_h4", "column_id": "completed", "title": "🤖 100% Multi-Agent Profiles Cluster", "desc": "Все 6 агентов (Hermes, Callum, Richard, Alistair, Liz, Ben) запущены и изолированы.", "assignee": "🤖 6 Cores Live", "tag": "VERIFIED", "tag_class": "tag-done"}
        ]
    },
    "richard": {
        "title": "Richard Marlowe — B2B Sales & Pipeline Kanban",
        "badge": "RICHARD SALES",
        "bg": "#0F172A",
        "card_bg": "#1E293B",
        "accent": "#F59E0B",
        "accent_secondary": "#10B981",
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
        "cards": [
            {"id": "c_c1", "column_id": "todo", "title": "💳 Monobank Acquiring X-Token Integration", "desc": "Интеграция эквайринга Монобанка для автоматической оплаты пакетов услуг.", "assignee": "💻 Callum Vance", "tag": "BACKLOG", "tag_class": "tag-todo"},
            {"id": "c_c2", "column_id": "in_progress", "title": "🚀 AI Project Evaluation & 10-Level Pricing", "desc": "Автоматическая ИИ-оценка сложности проекта и конвертация валют по Geo-IP.", "assignee": "💻 Callum Vance", "tag": "IN DEV", "tag_class": "tag-progress"},
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
        "cards": [
            {"id": "c_l1", "column_id": "todo", "title": "👥 Digital & Human Team Synergy Handbook", "desc": "Создание руководства по совместной работе 10 людей и 10 цифровых агентов.", "assignee": "🤝 Liz Harper", "tag": "HR POLICY", "tag_class": "tag-todo"},
            {"id": "c_l2", "column_id": "in_progress", "title": "💬 Internal Telegram Comms & Onboarding", "desc": "Мониторинг климата в команде и настройка быстрых авто-ответов сотрудникам.", "assignee": "🤝 Liz Harper", "tag": "ACTIVE", "tag_class": "tag-progress"},
            {"id": "c_l3", "column_id": "recurring", "title": "🔔 Ecosystem Self-Heal & Team Health Check", "desc": "Проверка самочувствия и доступности всех 5 ботов команды в 04:00 AM.", "assignee": "🤝 Liz Harper", "tag": "DAILY 04:00", "tag_class": "tag-cron"},
            {"id": "c_l4", "column_id": "completed", "title": "📧 Dual Branded Email Mailer Setup", "desc": "Двойная отправка писем админам на dr.reenforce@gmail.com с брендовых почт.", "assignee": "🤝 Liz Harper", "tag": "VERIFIED", "tag_class": "tag-done"}
        ]
    },
    "ben": {
        "title": "Ben Jett — Marketing & Growth Agency Kanban",
        "badge": "BEN GROWTH MARKETING",
        "bg": "#140A05",
        "card_bg": "#24130A",
        "accent": "#FF6B00",
        "accent_secondary": "#F59E0B",
        "cards": [
            {"id": "c_b1", "column_id": "todo", "title": "🎯 Avalanche Agency PPC & Social Campaigns", "desc": "Запуск лидогенерационных кампаний в LinkedIn и Google Ads для B2B клиентов.", "assignee": "🚀 Ben Jett", "tag": "CAMPAIGN", "tag_class": "tag-todo"},
            {"id": "c_b2", "column_id": "in_progress", "title": "🔥 Avalanche Redesign Landing Conversion Test", "desc": "А/Б тестирование высокой конверсии обновленного темного лендинга.", "assignee": "🚀 Ben Jett", "tag": "TESTING", "tag_class": "tag-progress"},
            {"id": "c_b3", "column_id": "recurring", "title": "🤖 Ben Bot Watchdog Ping", "desc": "Автоматическая проверка доступности и пинг маркетинг-бота каждые 10 минут.", "assignee": "🚀 Ben Jett", "tag": "CRON 10M", "tag_class": "tag-cron"},
            {"id": "c_b4", "column_id": "completed", "title": "🔎 Google Search Console & Sitemap Indexing", "desc": "Загрузка мульти-язычных свайпов sitemap.xml и SEO-оптимизация.", "assignee": "🚀 Ben Jett", "tag": "VERIFIED", "tag_class": "tag-done"}
        ]
    }
}

# Connect to Hostinger to deploy HTMLs and Seed Data
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("82.29.199.155", port=65002, username="u473746908", password="Stefrogovskyi#1", timeout=15)
sftp = ssh.open_sftp()

def generate_html(agent, cfg):
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{cfg['title']}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: {cfg['bg']};
      --card-bg: {cfg['card_bg']};
      --card-border: rgba(255, 255, 255, 0.1);
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
    body {{ background-color: var(--bg); color: var(--text-main); min-height: 100vh; padding: 24px; }}
    
    header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid var(--card-border); }}
    .title-group {{ display: flex; align-items: center; gap: 12px; }}
    .title-badge {{ background: linear-gradient(135deg, var(--accent), var(--accent-sec)); color: #FFF; font-weight: 800; font-size: 13px; padding: 6px 12px; border-radius: 8px; text-transform: uppercase; }}
    h1 {{ font-size: 20px; font-weight: 800; letter-spacing: -0.5px; }}
    
    .btn-primary {{ background: var(--accent); color: #FFF; border: none; padding: 10px 18px; border-radius: 8px; font-weight: 700; cursor: pointer; font-size: 13px; transition: all 0.2s; }}
    .btn-primary:hover {{ opacity: 0.9; transform: translateY(-1px); }}

    .grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }}
    @media (max-width: 1200px) {{ .grid {{ grid-template-columns: repeat(2, 1fr); }} }}
    @media (max-width: 600px) {{ .grid {{ grid-template-columns: 1fr; }} }}

    .column {{ background: rgba(255, 255, 255, 0.03); border: 1px solid var(--card-border); border-radius: 14px; padding: 16px; display: flex; flex-direction: column; gap: 12px; min-height: 600px; transition: background 0.2s; }}
    .column.drag-over {{ background: rgba(255, 255, 255, 0.08); border-color: var(--accent); }}
    .column-header {{ display: flex; justify-content: space-between; align-items: center; font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-muted); padding-bottom: 8px; border-bottom: 2px solid var(--card-border); }}
    .col-count {{ background: rgba(255, 255, 255, 0.1); color: var(--text-main); font-size: 11px; padding: 2px 8px; border-radius: 10px; }}

    .card {{ background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 10px; padding: 14px; transition: all 0.2s ease; cursor: grab; position: relative; }}
    .card:active {{ cursor: grabbing; opacity: 0.6; }}
    .card:hover {{ border-color: var(--accent); transform: translateY(-2px); box-shadow: 0 8px 20px rgba(0,0,0,0.3); }}
    .card-title {{ font-size: 14px; font-weight: 700; margin-bottom: 6px; line-height: 1.4; color: var(--text-main); }}
    .card-desc {{ font-size: 12px; color: var(--text-muted); margin-bottom: 12px; line-height: 1.5; }}
    .card-footer {{ display: flex; justify-content: space-between; align-items: center; font-size: 11px; }}

    .tag {{ font-weight: 600; padding: 3px 8px; border-radius: 6px; }}
    .tag-todo {{ background: rgba(245, 158, 11, 0.15); color: var(--accent-amber); }}
    .tag-progress {{ background: rgba(95, 179, 249, 0.15); color: var(--accent-blue); }}
    .tag-cron {{ background: rgba(168, 85, 247, 0.15); color: var(--accent-purple); }}
    .tag-done {{ background: rgba(16, 185, 129, 0.15); color: var(--accent-green); }}

    /* MODALS */
    .modal-overlay {{ position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.8); backdrop-filter: blur(4px); display: none; justify-content: center; align-items: center; z-index: 1000; }}
    .modal-box {{ background: var(--card-bg); border: 1px solid var(--card-border); width: 90%; max-width: 600px; border-radius: 16px; padding: 24px; box-shadow: 0 20px 50px rgba(0,0,0,0.5); }}
    .modal-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }}
    .modal-close {{ background: none; border: none; color: var(--text-muted); font-size: 20px; cursor: pointer; }}
    
    .input-field {{ width: 100%; background: rgba(0,0,0,0.3); border: 1px solid var(--card-border); border-radius: 8px; padding: 10px 12px; color: #FFF; font-size: 13px; outline: none; margin-bottom: 10px; }}
    .input-field:focus {{ border-color: var(--accent); }}
  </style>
</head>
<body>

  <header>
    <div class="title-group">
      <span class="title-badge">{cfg['badge']}</span>
      <h1>{cfg['title']}</h1>
    </div>
    <button class="btn-primary" onclick="openNewModal()">+ Новая Задача</button>
  </header>

  <div class="grid" id="kanban-grid">
    <!-- Columns loaded dynamically -->
  </div>

  <!-- NEW TASK MODAL -->
  <div class="modal-overlay" id="new-modal">
    <div class="modal-box">
      <div class="modal-header">
        <h2 style="font-size: 16px;">+ Добавить Задачу для {cfg['badge']}</h2>
        <button class="modal-close" onclick="closeNewModal()">✕</button>
      </div>
      <input type="text" id="new-title" class="input-field" placeholder="Название задачи">
      <textarea id="new-desc" class="input-field" rows="3" placeholder="Описание задачи..."></textarea>
      <select id="new-col" class="input-field">
        <option value="todo">📋 TODO / BACKLOG</option>
        <option value="in_progress">⚡ IN PROGRESS</option>
        <option value="recurring">🔄 RECURRING / CRON</option>
        <option value="completed">✅ COMPLETED / DONE</option>
      </select>
      <button class="btn-primary" style="width: 100%; margin-top: 8px;" onclick="createNewTask()">Поставить Задачу ➔</button>
    </div>
  </div>

  <script>
    const AGENT = '{agent}';
    const API_URL = 'https://aavalanche.com/kanban_api.php?agent=' + AGENT;
    let currentState = null;
    let draggedCardId = null;

    // 1. LOCAL STORAGE & API DUAL PERSISTENCE
    function getLocalState() {{
      try {{
        const raw = localStorage.getItem('kanban_state_' + AGENT);
        return raw ? JSON.parse(raw) : null;
      }} catch(e) {{ return null; }}
    }}

    function setLocalState(state) {{
      try {{
        localStorage.setItem('kanban_state_' + AGENT, JSON.stringify(state));
      }} catch(e) {{}}
    }}

    async function fetchState() {{
      const cached = getLocalState();
      if (cached && cached.cards) {{
        currentState = cached;
        renderBoard();
      }}
      try {{
        const res = await fetch(API_URL);
        const serverState = await res.json();
        if (serverState && serverState.cards && serverState.cards.length > 0) {{
          // Merge or adopt server state if valid
          if (!cached || !cached.cards || cached.cards.length === 0) {{
            currentState = serverState;
            setLocalState(currentState);
            renderBoard();
          }}
        }}
      }} catch(err) {{
        console.warn('API sync warning:', err);
      }}
    }}

    function renderBoard() {{
      if (!currentState) return;
      const grid = document.getElementById('kanban-grid');
      grid.innerHTML = '';

      const cols = {{
        'todo': {{ title: '📋 TODO / BACKLOG', cards: [] }},
        'in_progress': {{ title: '⚡ IN PROGRESS', cards: [] }},
        'recurring': {{ title: '🔄 RECURRING / CRON', cards: [] }},
        'completed': {{ title: '✅ COMPLETED / DONE', cards: [] }}
      }};

      currentState.cards.forEach(c => {{
        if (cols[c.column_id]) cols[c.column_id].cards.push(c);
      }});

      Object.keys(cols).forEach(colId => {{
        const col = cols[colId];
        const colEl = document.createElement('div');
        colEl.className = 'column';
        colEl.setAttribute('data-col', colId);
        colEl.ondragover = e => {{ e.preventDefault(); colEl.classList.add('drag-over'); }};
        colEl.ondragleave = () => colEl.classList.remove('drag-over');
        colEl.ondrop = e => handleDrop(e, colId, colEl);

        let cardsHtml = '';
        col.cards.forEach(c => {{
          cardsHtml += `
            <div class="card" draggable="true" ondragstart="handleDragStart(event, '${{c.id}}')">
              <div class="card-title">${{c.title}}</div>
              <div class="card-desc">${{c.desc}}</div>
              <div class="card-footer">
                <span class="tag ${{c.tag_class || 'tag-todo'}}">${{c.tag || 'TASK'}}</span>
                <span class="assignee">${{c.assignee || AGENT}}</span>
              </div>
            </div>
          `;
        }});

        colEl.innerHTML = `
          <div class="column-header">
            <span>${{col.title}}</span>
            <span class="col-count">${{col.cards.length}}</span>
          </div>
          ${{cardsHtml}}
        `;
        grid.appendChild(colEl);
      }});
    }}

    // DRAG AND DROP HANDLERS
    function handleDragStart(e, cardId) {{
      draggedCardId = cardId;
      e.dataTransfer.setData('text/plain', cardId);
    }}

    async function handleDrop(e, targetColId, colEl) {{
      e.preventDefault();
      colEl.classList.remove('drag-over');
      if (!draggedCardId || !currentState) return;

      const card = currentState.cards.find(c => c.id === draggedCardId);
      if (card && card.column_id !== targetColId) {{
        card.column_id = targetColId;
        
        // 1. IMMEDIATELY PERSIST LOCALLY (No rollback possible)
        setLocalState(currentState);
        renderBoard();

        // 2. PERSIST TO SERVER API IN BACKGROUND
        try {{
          await fetch('https://aavalanche.com/kanban_api.php', {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({{ agent: AGENT, action: 'move_card', card_id: draggedCardId, new_column_id: targetColId }})
          }});
        }} catch(err) {{
          console.warn('Server sync error (saved locally):', err);
        }}
      }}
      draggedCardId = null;
    }}

    function openNewModal() {{ document.getElementById('new-modal').style.display = 'flex'; }}
    function closeNewModal() {{ document.getElementById('new-modal').style.display = 'none'; }}

    async function createNewTask() {{
      const title = document.getElementById('new-title').value.trim();
      const desc = document.getElementById('new-desc').value.trim();
      const col = document.getElementById('new-col').value;
      if (!title) return alert('Укажите название задачи!');

      const newCard = {{
        id: 'card_' + Date.now(),
        column_id: col,
        title: title,
        desc: desc,
        assignee: AGENT,
        tag: 'NEW',
        tag_class: 'tag-todo'
      }};

      if (!currentState.cards) currentState.cards = [];
      currentState.cards.push(newCard);
      
      // Save local & render
      setLocalState(currentState);
      renderBoard();
      closeNewModal();
      document.getElementById('new-title').value = '';
      document.getElementById('new-desc').value = '';

      // Sync server
      try {{
        await fetch('https://aavalanche.com/kanban_api.php', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ agent: AGENT, action: 'add_card', column_id: col, title: title, desc: desc, assignee: AGENT }})
        }});
      }} catch(e) {{}}
    }}

    fetchState();
  </script>
</body>
</html>
"""

# Deploy all 6 agent HTMLs & seed JSONs
for agent, cfg in agents_config.items():
    html = generate_html(agent, cfg)
    
    # 1. Hostinger paths
    hostinger_dir = f"/home/u473746908/domains/aavalanche.com/public_html/kanban/{agent}"
    ssh.exec_command(f"mkdir -p {hostinger_dir}")
    
    with sftp.file(f"{hostinger_dir}/index.html", "w") as f:
        f.write(html)
        
    # Seed initial json on hostinger if missing
    json_path = f"/home/u473746908/domains/aavalanche.com/public_html/kanban_store_{agent}.json"
    try:
        sftp.stat(json_path)
    except IOError:
        seed_data = {
            "updated_at": "2026-08-10T10:00:00Z",
            "agent": agent,
            "columns": {"todo": "📋 TODO / BACKLOG", "in_progress": "⚡ IN PROGRESS", "recurring": "🔄 RECURRING / CRON", "completed": "✅ COMPLETED / DONE"},
            "cards": cfg["cards"]
        }
        with sftp.file(json_path, "w") as f:
            f.write(json.dumps(seed_data, indent=2, ensure_ascii=False))

    # 2. Vercel deployment directory
    v_dir = f"/tmp/_vercel_kanban_{agent}"
    os.makedirs(v_dir, exist_ok=True)
    open(os.path.join(v_dir, "index.html"), "w", encoding="utf-8").write(html)
    v_json = {"version": 2, "name": f"{agent}-kanban", "builds": [{"src": "index.html", "use": "@vercel/static"}], "routes": [{"src": "/(.*)", "dest": "/index.html"}]}
    open(os.path.join(v_dir, "vercel.json"), "w", encoding="utf-8").write(json.dumps(v_json, indent=2))
    
    print(f"✅ Generated & uploaded Kanban for {agent.upper()}")

sftp.close()
ssh.close()
print("All 6 agent Kanban boards generated and uploaded to Hostinger!")
