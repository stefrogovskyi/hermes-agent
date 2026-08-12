Richard (richnavobot): privacy OFF; SINGLE bot (token 8846249306). Sub-bots MUST NEVER fall back to Hermes token (8682188433). Watchdog verifies token isolation before spawn. Stefan DM(330656040)=client.
§
USER MODEL: agents=persistent ASSETS, not disposable. Upgradable standalone processes w/ file memory.
§
OP RULES & SELF-HEAL: Автономность при падении/обрыве/прерывании ([This response was interrupted...], [Response truncated], tool error, 403/503/gateway restart) = сама фиксация root-cause + авто-доделывание с точки остановки, 0 вопросов 'что дальше'. Перечитывать свои и системные сообщения об ошибках, устранять сразу. Long-task >30s = background+notify (главная сессия <20s).
§
ПАМЯТЬ V2: memory_v2/ (cases+principles+domains+recall.py+Pinecone+skill memory-recall). ПРАВИЛА Стефана: (1) гипотезу сначала ФАКТ, потом правка; (2) при любом падении сам зафиксируй+доделай, НЕ жди вопроса; (3) перечитывай свои сообщения, лови самоупоминание ошибки/падения и устраняй сразу. Cron: memory harvest 02:00, Pinecone sync 03:00.
§
USER: Стефан (COO Navo). MS To-Do = supremo@i.ua via Make webhook. Агенты: persistent процессы (Hermes, Richard, Liz, Alistair, Ben, Callum).
§
WORK STYLE: Stefan wants 24/7 autonomous proactive work on long-term tasks. Priority rule: if Stefan interjects with a question, pause background work, answer, then resume. No waiting for prompts.
§
КАНБАНЫ АГЕНТОВ: Все 6 Канбанов агентов хостятся ИСКЛЮЧИТЕЛЬНО НА VERCEL (https://<agent>-kanban.vercel.app). НИКОГДА НЕ ДЕПЛОИТЬ КАНБАНЫ НА ДОМЕНЕ AAVALANCHE.COM. Бэкенд API: https://dev.aavalanche.com/kanban_api.php.
§
YouTube WL: Playwright 23:00 daily; 'move'=deletion. DP World vacancies cron = Hermes Stevenson DM ONLY. DBs: WAL+busy_timeout 10s.
§
Hostinger: u473746908, SSH 82.29.199.155:65002. ФАЙЛЫ (Drive & ПК): С Google Диска — выкачивать напрямую через Drive API; с ПК (Anetta12/DESKTOP) — по Tailscale, если ПК включен, и высылать файлом в Telegram.
§
Navo24 unified API key (NAVO_API_KEY tmcp_live_...) covers all 5 Navo APIs. NO AGENT MAY IMPERSONATE STEFAN OR SEND MESSAGES FROM USER ACCOUNT. ALL BOTS WRITE ONLY FROM THEIR OWN BOT ACCOUNTS.
§
ФАЙЛЫ (Google Drive & ПК): При запросе любых файлов с Google Диска — выкачивать их напрямую через Google Drive API. При запросе файлов с ПК (Anetta12/DESKTOP) — выкачивать по Tailscale, если ПК включен, и отправлять файлом в Telegram.