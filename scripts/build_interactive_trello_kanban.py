# -*- coding: utf-8 -*-
"""
build_interactive_trello_kanban.py —
  1. Создание бэкенда kanban_api.php и развертывание на dev.aavalanche.com / staging.aavalanche.com
  2. Генерация фронтенда Trello-style интерактивного Канбан-борда со всеми карточками, комментариями и таймлайном
  3. Деплой на Vercel под именем hermes-stevenson-kanban (https://hermes-stevenson-kanban.vercel.app)
"""

import os, subprocess, json, paramiko

HERMES_DIR = r"C:\Users\Stefan\AppData\Local\hermes"
vercel_dir = os.path.join(HERMES_DIR, "_vercel_interactive_kanban")
os.makedirs(vercel_dir, exist_ok=True)

# 1. CREATE BACKEND PHP API FOR REAL-TIME COMMENTING & TASK INTAKE
kanban_api_php = """<?php
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit(0);
}

$db_file = __DIR__ . '/kanban_store.json';

// Initial state if json file doesn't exist
if (!file_exists($db_file)) {
    $initial_data = [
        "updated_at" => date("c"),
        "columns" => [
            "todo" => "📋 TODO / BACKLOG",
            "in_progress" => "⚡ IN PROGRESS",
            "recurring" => "🔄 RECURRING / CRON",
            "completed" => "✅ COMPLETED / DONE"
        ],
        "cards" => [
            [
                "id" => "card_1",
                "column_id" => "todo",
                "title" => "💳 Monobank Merchant Acquiring Token Integration",
                "desc" => "Подключение X-Token ФОП Монобанка для реальных списаний в грн на сайте.",
                "assignee" => "👤 Stefan / Callum",
                "tag" => "BACKLOG",
                "tag_class" => "tag-todo",
                "comments" => [
                    ["id" => "c1", "author" => "🤖 Hermes Stevenson", "time" => "2026-08-07 15:00", "text" => "Ожидаем X-Token из кабинета web.monobank.ua для боевых проверок."]
                ]
            ],
            [
                "id" => "card_2",
                "column_id" => "todo",
                "title" => "🛍️ Silpo Weekly Groceries Order Assembly",
                "desc" => "Еженедельная автосборка корзины Сільпо через Playwright Chromium (>1,700 UAH).",
                "assignee" => "🤖 Hermes",
                "tag" => "PENDING",
                "tag_class" => "tag-todo",
                "comments" => []
            ],
            [
                "id" => "card_3",
                "column_id" => "todo",
                "title" => "🇩🇪 Hetzner Cloud VPS Migration",
                "desc" => "Перенос 6 профилей Гермеса и крон-задач на серваки Hetzner для 24/7 автономии.",
                "assignee" => "🤖 Hermes Cluster",
                "tag" => "PLANNED",
                "tag_class" => "tag-todo",
                "comments" => []
            ],
            [
                "id" => "card_4",
                "column_id" => "in_progress",
                "title" => "🌐 Avalanche Agency 3-Tier Pipeline",
                "desc" => "Синхронизация dev.aavalanche.com, staging и prod под управлением GitHub.",
                "assignee" => "💻 Callum Vance",
                "tag" => "ACTIVE",
                "tag_class" => "tag-progress",
                "comments" => [
                    ["id" => "c2", "author" => "💻 Callum Vance", "time" => "2026-08-07 14:00", "text" => "Все 3 контура активны, x-robots-tag закрыл dev и staging от индексации."]
                ]
            ],
            [
                "id" => "card_5",
                "column_id" => "in_progress",
                "title" => "🚀 AI Project Evaluation & 10-Point Price Graduation",
                "desc" => "ИИ-оценка сложности проекта по 10 уровням, конвертация валюты по IP и модалка оплаты.",
                "assignee" => "💻 Callum Vance",
                "tag" => "ACTIVE",
                "tag_class" => "tag-progress",
                "comments" => []
            ],
            [
                "id" => "card_6",
                "column_id" => "in_progress",
                "title" => "🔑 User Auth, Personal Cabinet & Admin Panel",
                "desc" => "Регистрация, вход, Google/Facebook OAuth, Личный Кабинет и таблица пользователей.",
                "assignee" => "💻 Callum Vance",
                "tag" => "ACTIVE",
                "tag_class" => "tag-progress",
                "comments" => []
            ],
            [
                "id" => "card_7",
                "column_id" => "recurring",
                "title" => "📺 YouTube Watch Later Daily Sorter",
                "desc" => "Ежедневный разбор в 23:00 с сопоставлением со 49 реальными плейлистами YouTube.",
                "assignee" => "🤖 Hermes DM",
                "tag" => "DAILY 23:00",
                "tag_class" => "tag-cron",
                "comments" => []
            ],
            [
                "id" => "card_8",
                "column_id" => "recurring",
                "title" => "🌾 Memory Harvest Cron",
                "desc" => "Ежедневная автосборка фактов и кейсов памяти memory_v2 в 02:00 MSK.",
                "assignee" => "🤖 Hermes",
                "tag" => "DAILY 02:00",
                "tag_class" => "tag-cron",
                "comments" => []
            ],
            [
                "id" => "card_9",
                "column_id" => "recurring",
                "title" => "🌲 Pinecone Vector Memory Sync",
                "desc" => "Ежедневный векторный синтез эмбеддингов в Pinecone в 03:00 MSK.",
                "assignee" => "🤖 Hermes",
                "tag" => "DAILY 03:00",
                "tag_class" => "tag-cron",
                "comments" => []
            ],
            [
                "id" => "card_10",
                "column_id" => "recurring",
                "title" => "🏢 DP World Careers Vacancies Poller",
                "desc" => "Ежедневный мониторинг новых вакансий DP World в 09:00 MSK.",
                "assignee" => "🤖 Hermes DM ONLY",
                "tag" => "DAILY 09:00",
                "tag_class" => "tag-cron",
                "comments" => []
            ],
            [
                "id" => "card_11",
                "column_id" => "completed",
                "title" => "🤖 100% Multi-Agent Hermes Profiles Cluster",
                "desc" => "Все 6 агентов (Orchestrator, Callum, Richard, Alistair, Liz, Ben) работают на ядре Гермеса!",
                "assignee" => "🤖 6 Cores Live",
                "tag" => "VERIFIED",
                "tag_class" => "tag-done",
                "comments" => [
                    ["id" => "c3", "author" => "🤖 Hermes Stevenson", "time" => "2026-08-07 16:00", "text" => "Все 6 профилей полностью запущены, автономия включена."]
                ]
            ],
            [
                "id" => "card_12",
                "column_id" => "completed",
                "title" => "🌍 8 Multilingual Language Clones",
                "desc" => "100% отзеркаливание верстки на 8 языков (es, de, fr, it, uk, ru, zh, ar) без сброса сессий.",
                "assignee" => "💻 Callum Vance",
                "tag" => "VERIFIED",
                "tag_class" => "tag-done",
                "comments" => []
            ],
            [
                "id" => "card_13",
                "column_id" => "completed",
                "title" => "📧 Dual Branded Email Mailer",
                "desc" => "Двойная отправка писем админу на dr.reenforce@gmail.com с info@aavalanche.com.",
                "assignee" => "💻 Callum Vance",
                "tag" => "VERIFIED",
                "tag_class" => "tag-done",
                "comments" => []
            ],
            [
                "id" => "card_14",
                "column_id" => "completed",
                "title" => "🗺️ Drive & Desktop File Organization",
                "desc" => "Наведен полный порядок на Диске и Рабочем столе с памяткой README_FILE_STRUCTURE.md.",
                "assignee" => "📈 Alistair Sterling",
                "tag" => "VERIFIED",
                "tag_class" => "tag-done",
                "comments" => []
            ],
            [
                "id" => "card_15",
                "column_id" => "completed",
                "title" => "🔎 Google Search Console SEO Setup",
                "desc" => "Загружен sitemap.xml для 9 языков и robots.txt, закрыты noindex dev/staging.",
                "assignee" => "🤖 Hermes",
                "tag" => "VERIFIED",
                "tag_class" => "tag-done",
                "comments" => []
            ]
        ]
    ];
    file_put_contents($db_file, json_encode($initial_data, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT));
}

$state = json_decode(file_get_contents($db_file), true);

// GET METHOD: Return full state
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    echo json_encode($state, JSON_UNESCAPED_UNICODE);
    exit;
}

// POST METHOD: Add Task, Add Comment, or Move Task
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $input = json_decode(file_get_contents('php_input://input'), true) ?? $_POST;
    $action = $input['action'] ?? '';

    if ($action === 'add_comment') {
        $card_id = $input['card_id'] ?? '';
        $author = $input['author'] ?? '👤 Stefan Rogovskiy';
        $text = trim($input['text'] ?? '');

        if ($card_id && $text) {
            foreach ($state['cards'] as &$card) {
                if ($card['id'] === $card_id) {
                    $new_comment = [
                        'id' => 'c_' . time() . '_' . rand(100, 999),
                        'author' => $author,
                        'time' => date('Y-m-d H:i'),
                        'text' => $text
                    ];
                    $card['comments'][] = $new_comment;
                    break;
                }
            }
            $state['updated_at'] = date('c');
            file_put_contents($db_file, json_encode($state, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT));
            echo json_encode(['status' => 'success', 'message' => 'Comment added!'], JSON_UNESCAPED_UNICODE);
            exit;
        }
    }

    if ($action === 'add_task') {
        $title = trim($input['title'] ?? '');
        $desc = trim($input['desc'] ?? '');
        $col_id = $input['column_id'] ?? 'todo';
        $assignee = $input['assignee'] ?? '👤 Stefan';

        if ($title) {
            $new_card = [
                'id' => 'card_' . time(),
                'column_id' => $col_id,
                'title' => $title,
                'desc' => $desc,
                'assignee' => $assignee,
                'tag' => 'NEW TASK',
                'tag_class' => ($col_id === 'in_progress' ? 'tag-progress' : ($col_id === 'recurring' ? 'tag-cron' : ($col_id === 'completed' ? 'tag-done' : 'tag-todo'))),
                'comments' => [
                    ['id' => 'c_init', 'author' => '🤖 Hermes Stevenson', 'time' => date('Y-m-d H:i'), 'text' => 'Новая задача принята в обработку.']
                ]
            ];
            $state['cards'][] = $new_card;
            $state['updated_at'] = date('c');
            file_put_contents($db_file, json_encode($state, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT));
            echo json_encode(['status' => 'success', 'card' => $new_card], JSON_UNESCAPED_UNICODE);
            exit;
        }
    }

    if ($action === 'move_task') {
        $card_id = $input['card_id'] ?? '';
        $target_col = $input['target_column_id'] ?? '';

        if ($card_id && $target_col) {
            foreach ($state['cards'] as &$card) {
                if ($card['id'] === $card_id) {
                    $card['column_id'] = $target_col;
                    $card['tag_class'] = ($target_col === 'in_progress' ? 'tag-progress' : ($target_col === 'recurring' ? 'tag-cron' : ($target_col === 'completed' ? 'tag-done' : 'tag-todo')));
                    break;
                }
            }
            $state['updated_at'] = date('c');
            file_put_contents($db_file, json_encode($state, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT));
            echo json_encode(['status' => 'success'], JSON_UNESCAPED_UNICODE);
            exit;
        }
    }

    echo json_encode(['status' => 'error', 'message' => 'Invalid action'], JSON_UNESCAPED_UNICODE);
    exit;
}
"""

# Upload kanban_api.php to Hostinger via SSH
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('82.29.199.155', port=65002, username='u473746908', password='Stefrogovskyi#1')

sftp = ssh.open_sftp()
dev_dir = '/home/u473746908/domains/aavalanche.com/public_html/dev'

with sftp.open(f'{dev_dir}/kanban_api.php', 'w') as f:
    f.write(kanban_api_php)

sftp.close()
ssh.close()

print("✅ Uploaded backend kanban_api.php to dev.aavalanche.com/kanban_api.php!")

# 2. GENERATE INTERACTIVE TRELLO-STYLE FRONTEND HTML FOR VERCEL
trello_html = """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Hermes Stevenson — Interactive Trello Kanban Board</title>
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
      --accent-red: #EF4444;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Plus Jakarta Sans', sans-serif; }
    body { background-color: var(--bg); color: var(--text-main); min-height: 100vh; padding: 24px; }
    
    header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid var(--card-border); }
    .title-group { display: flex; align-items: center; gap: 12px; }
    .title-badge { background: linear-gradient(135deg, #3B82F6, #10B981); color: #FFF; font-weight: 800; font-size: 13px; padding: 6px 12px; border-radius: 8px; }
    h1 { font-size: 22px; font-weight: 800; letter-spacing: -0.5px; }
    
    .btn-primary { background: #3B82F6; color: #FFF; border: none; padding: 10px 18px; border-radius: 8px; font-weight: 700; cursor: pointer; font-size: 13px; transition: all 0.2s; }
    .btn-primary:hover { background: #2563EB; transform: translateY(-1px); }

    .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
    @media (max-width: 1200px) { .grid { grid-template-columns: repeat(2, 1fr); } }
    @media (max-width: 600px) { .grid { grid-template-columns: 1fr; } }

    .column { background: rgba(21, 28, 44, 0.4); border: 1px solid var(--card-border); border-radius: 14px; padding: 16px; display: flex; flex-direction: column; gap: 12px; min-height: 600px; }
    .column-header { display: flex; justify-content: space-between; align-items: center; font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-muted); padding-bottom: 8px; border-bottom: 2px solid var(--card-border); }
    .col-count { background: var(--card-border); color: var(--text-main); font-size: 11px; padding: 2px 8px; border-radius: 10px; }

    .card { background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 10px; padding: 14px; transition: all 0.2s ease; cursor: pointer; position: relative; }
    .card:hover { border-color: var(--accent-blue); transform: translateY(-2px); box-shadow: 0 8px 20px rgba(0,0,0,0.3); }
    .card-title { font-size: 14px; font-weight: 700; margin-bottom: 6px; line-height: 1.4; color: var(--text-main); }
    .card-desc { font-size: 12px; color: var(--text-muted); margin-bottom: 12px; line-height: 1.5; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
    .card-footer { display: flex; justify-content: space-between; align-items: center; font-size: 11px; }
    
    .comment-count { display: flex; align-items: center; gap: 4px; color: var(--accent-blue); font-weight: 600; }

    .tag { font-weight: 600; padding: 3px 8px; border-radius: 6px; }
    .tag-todo { background: rgba(245, 158, 11, 0.15); color: var(--accent-amber); }
    .tag-progress { background: rgba(95, 179, 249, 0.15); color: var(--accent-blue); }
    .tag-cron { background: rgba(168, 85, 247, 0.15); color: var(--accent-purple); }
    .tag-done { background: rgba(16, 185, 129, 0.15); color: var(--accent-green); }

    /* MODAL STYLING */
    .modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.75); backdrop-filter: blur(4px); display: none; justify-content: center; align-items: center; z-index: 1000; }
    .modal-box { background: #151C2C; border: 1px solid var(--card-border); width: 90%; max-width: 650px; border-radius: 16px; padding: 24px; max-height: 90vh; overflow-y: auto; box-shadow: 0 20px 50px rgba(0,0,0,0.5); }
    .modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
    .modal-close { background: none; border: none; color: var(--text-muted); font-size: 20px; cursor: pointer; }
    .modal-close:hover { color: #FFF; }
    
    .timeline { margin-top: 20px; border-top: 1px solid var(--card-border); padding-top: 16px; }
    .timeline-title { font-size: 14px; font-weight: 700; margin-bottom: 12px; color: var(--accent-blue); }
    .comment-item { background: #0B0F19; border: 1px solid var(--card-border); border-radius: 8px; padding: 12px; margin-bottom: 10px; }
    .comment-header { display: flex; justify-content: space-between; font-size: 12px; font-weight: 700; color: var(--accent-blue); margin-bottom: 6px; }
    .comment-time { font-weight: 400; color: var(--text-muted); font-size: 11px; }
    .comment-text { font-size: 13px; color: var(--text-main); line-height: 1.4; }

    .add-comment-box { margin-top: 16px; display: flex; gap: 8px; }
    .input-field { flex: 1; background: #0B0F19; border: 1px solid var(--card-border); border-radius: 8px; padding: 10px 12px; color: #FFF; font-size: 13px; outline: none; }
    .input-field:focus { border-color: var(--accent-blue); }
  </style>
</head>
<body>

  <header>
    <div class="title-group">
      <span class="title-badge">TRELLO MODE</span>
      <h1>Hermes Stevenson — Interactive Kanban Board</h1>
    </div>
    <button class="btn-primary" onclick="openNewTaskModal()">+ Добавить Задачу</button>
  </header>

  <div class="grid" id="kanban-grid">
    <!-- Columns loaded dynamically -->
  </div>

  <!-- CARD DETAIL & COMMENT MODAL -->
  <div class="modal-overlay" id="card-modal">
    <div class="modal-box">
      <div class="modal-header">
        <h2 id="modal-card-title" style="font-size: 18px; font-weight: 800;">Card Title</h2>
        <button class="modal-close" onclick="closeModal()">✕</button>
      </div>
      <p id="modal-card-desc" style="font-size: 13px; color: var(--text-muted); margin-bottom: 16px; line-height: 1.5;"></p>
      
      <div style="display: flex; gap: 12px; margin-bottom: 20px; font-size: 12px;">
        <div><strong>Исполнитель:</strong> <span id="modal-card-assignee" style="color: var(--accent-blue);"></span></div>
        <div><strong>Статус:</strong> <span id="modal-card-tag" class="tag"></span></div>
      </div>

      <div class="timeline">
        <div class="timeline-title">💬 Хронология Событий & Комментарии</div>
        <div id="modal-comments-list">
          <!-- Comments -->
        </div>

        <div class="add-comment-box">
          <input type="text" id="new-comment-input" class="input-field" placeholder="Напишите комментарий или задачу для Гермеса..." onkeydown="if(event.key==='Enter') submitComment()">
          <button class="btn-primary" onclick="submitComment()">Отправить ➔</button>
        </div>
      </div>
    </div>
  </div>

  <!-- NEW TASK MODAL -->
  <div class="modal-overlay" id="new-task-modal">
    <div class="modal-box">
      <div class="modal-header">
        <h2>+ Создать Новую Задачу</h2>
        <button class="modal-close" onclick="closeNewTaskModal()">✕</button>
      </div>
      <div style="display: flex; flex-direction: column; gap: 12px; margin-top: 12px;">
        <input type="text" id="task-title-input" class="input-field" placeholder="Название задачи">
        <textarea id="task-desc-input" class="input-field" rows="3" placeholder="Подробное описание задачи..."></textarea>
        <select id="task-col-select" class="input-field">
          <option value="todo">📋 TODO / BACKLOG</option>
          <option value="in_progress">⚡ IN PROGRESS</option>
          <option value="recurring">🔄 RECURRING / CRON</option>
          <option value="completed">✅ COMPLETED / DONE</option>
        </select>
        <button class="btn-primary" style="margin-top: 12px;" onclick="submitNewTask()">Создать и Поставить Агентам ➔</button>
      </div>
    </div>
  </div>

  <script>
    const API_URL = 'https://dev.aavalanche.com/kanban_api.php';
    let currentState = null;
    let activeCardId = null;

    async function fetchState() {
      try {
        const res = await fetch(API_URL);
        currentState = await res.json();
        renderBoard();
        if (activeCardId) {
          const activeCard = currentState.cards.find(c => c.id === activeCardId);
          if (activeCard) renderModalComments(activeCard);
        }
      } catch (err) {
        console.error('API Fetch error:', err);
      }
    }

    function renderBoard() {
      if (!currentState) return;
      const grid = document.getElementById('kanban-grid');
      grid.innerHTML = '';

      const cols = {
        'todo': { title: '📋 TODO / BACKLOG', cards: [] },
        'in_progress': { title: '⚡ IN PROGRESS', cards: [] },
        'recurring': { title: '🔄 RECURRING / CRON', cards: [] },
        'completed': { title: '✅ COMPLETED / DONE', cards: [] }
      };

      currentState.cards.forEach(card => {
        if (cols[card.column_id]) cols[card.column_id].cards.push(card);
      });

      Object.keys(cols).forEach(colId => {
        const col = cols[colId];
        const colEl = document.createElement('div');
        colEl.className = 'column';
        
        let cardsHtml = '';
        col.cards.forEach(c => {
          const cCount = (c.comments || []).length;
          cardsHtml += `
            <div class="card" onclick="openCardModal('${c.id}')">
              <div class="card-title">${c.title}</div>
              <div class="card-desc">${c.desc}</div>
              <div class="card-footer">
                <span class="tag ${c.tag_class}">${c.tag}</span>
                <div style="display: flex; gap: 8px; align-items: center;">
                  ${cCount > 0 ? `<span class="comment-count">💬 ${cCount}</span>` : ''}
                  <span class="assignee">${c.assignee}</span>
                </div>
              </div>
            </div>
          `;
        });

        colEl.innerHTML = `
          <div class="column-header">
            <span>${col.title}</span>
            <span class="col-count">${col.cards.length}</span>
          </div>
          ${cardsHtml}
        `;
        grid.appendChild(colEl);
      });
    }

    function openCardModal(cardId) {
      activeCardId = cardId;
      const card = currentState.cards.find(c => c.id === cardId);
      if (!card) return;

      document.getElementById('modal-card-title').innerText = card.title;
      document.getElementById('modal-card-desc').innerText = card.desc;
      document.getElementById('modal-card-assignee').innerText = card.assignee;
      document.getElementById('modal-card-tag').innerText = card.tag;
      document.getElementById('modal-card-tag').className = 'tag ' + card.tag_class;

      renderModalComments(card);
      document.getElementById('card-modal').style.display = 'flex';
    }

    function renderModalComments(card) {
      const list = document.getElementById('modal-comments-list');
      list.innerHTML = '';
      const comments = card.comments || [];
      if (comments.length === 0) {
        list.innerHTML = '<div style="font-size: 12px; color: var(--text-muted); text-align: center; padding: 12px;">Пока нет комментариев. Напишите первый задача появится здесь!</div>';
        return;
      }
      comments.forEach(cm => {
        const item = document.createElement('div');
        item.className = 'comment-item';
        item.innerHTML = `
          <div class="comment-header">
            <span>${cm.author}</span>
            <span class="comment-time">${cm.time}</span>
          </div>
          <div class="comment-text">${cm.text}</div>
        `;
        list.appendChild(item);
      });
    }

    async function submitComment() {
      const input = document.getElementById('new-comment-input');
      const text = input.value.trim();
      if (!text || !activeCardId) return;

      try {
        await fetch(API_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            action: 'add_comment',
            card_id: activeCardId,
            author: '👤 Stefan Rogovskiy',
            text: text
          })
        });
        input.value = '';
        fetchState();
      } catch (err) {
        console.error('Error submitting comment:', err);
      }
    }

    function openNewTaskModal() {
      document.getElementById('new-task-modal').style.display = 'flex';
    }
    function closeNewTaskModal() {
      document.getElementById('new-task-modal').style.display = 'none';
    }

    async function submitNewTask() {
      const title = document.getElementById('task-title-input').value.trim();
      const desc = document.getElementById('task-desc-input').value.trim();
      const colId = document.getElementById('task-col-select').value;

      if (!title) return;

      try {
        await fetch(API_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            action: 'add_task',
            title: title,
            desc: desc,
            column_id: colId,
            assignee: '👤 Stefan'
          })
        });
        closeNewTaskModal();
        fetchState();
      } catch (err) {
        console.error('Error adding task:', err);
      }
    }

    function closeModal() {
      document.getElementById('card-modal').style.display = 'none';
      activeCardId = null;
    }

    fetchState();
    setInterval(fetchState, 5000);
  </script>
</body>
</html>
"""

open(os.path.join(vercel_dir, "index.html"), "w", encoding="utf-8").write(trello_html)

vercel_json = {
  "version": 2,
  "name": "hermes-stevenson-kanban",
  "builds": [
    { "src": "index.html", "use": "@vercel/static" }
  ],
  "routes": [
    { "src": "/(.*)", "dest": "/index.html" }
  ]
}

open(os.path.join(vercel_dir, "vercel.json"), "w", encoding="utf-8").write(json.dumps(vercel_json, indent=2))

# Deploy to Vercel
cmd = f'npx vercel "{vercel_dir}" --prod --yes --name hermes-stevenson-kanban'
print('Deploying interactive Trello Kanban to Vercel:', cmd)

res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
print("STDOUT:", res.stdout)
print("STDERR:", res.stderr)
