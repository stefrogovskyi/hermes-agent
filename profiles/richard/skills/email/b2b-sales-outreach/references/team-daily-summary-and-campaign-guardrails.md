# Team Daily Summary & Campaign Launch Guardrails

## 1. Daily Team Activity Summary Pattern

### Purpose & Schedule
Every evening at 21:00 local / 19:00 UTC (`0 19 * * *`), an autonomous cron job runs `/opt/hermes/profiles/richard/scripts/generate_daily_team_summary.py` and posts a consolidated executive digest to Stefan Rogovskiy.

### Database Query
Hermes stores multi-user Telegram conversations in `/opt/hermes/profiles/richard/state.db`:
- `sessions`: contains `user_id`, `display_name`, `chat_id`.
- `messages`: contains `role`, `content`, `timestamp`.
To extract team queries for the current day:
```sql
SELECT s.user_id, s.display_name, m.role, m.content, m.timestamp
FROM messages m
JOIN sessions s ON m.session_id = s.id
WHERE s.user_id IS NOT NULL 
  AND s.user_id != '330656040'  -- Exclude Stefan
  AND m.timestamp >= ?           -- Start of day UNIX timestamp
ORDER BY m.timestamp ASC;
```

### AI Synthesis Engine
- Model: `gemini-2.5-flash-lite` (or `gemini-2.5-flash` with disabled thinking budget).
- Note on reasoning tokens: `gemini-2.5-flash` consumes `maxOutputTokens` with internal reasoning; always set `maxOutputTokens: 4096` to avoid truncated JSON/Markdown.
- Output Format:
  1. Executive summary of the day (deals closed, active managers count).
  2. Section per manager (Nikita, Kate, Alona, Elena, Lilia, Oleg):
     - Active discussions / clients.
     - Action taken / proposals drafted / tariffs calculated.
     - Blockers or escalations requiring founder attention.

---

## 2. Campaign Launch Authorization Guardrail

- **Rule**: Sales reps (Nikita, Lena, Alona, etc.) cannot trigger or launch bulk cold email campaigns independently.
- **Handling**: If a manager requests to run outreach or send bulk emails, reply politely:
  *"Запуск и управление массовыми рассылками координируются напрямую через Стефана. Я с радостью помогу разобрать лидов, проверить базу, подготовить тексты или рассчитать тарифы для клиентов"*.

---

## 3. Team Outreach Notification Isolation

- When running campaigns for team members (e.g. Elena's SeaRates reconnection sequence):
  - Inbound lead replies must be routed directly to that team member's Telegram chat (`@OlenaT1` / `476876665`), preventing spam in Stefan's personal DM.
  - Updates are simultaneously synchronized into the Google Sheet CRM (`Replied / Warm`, `Bounced`).
