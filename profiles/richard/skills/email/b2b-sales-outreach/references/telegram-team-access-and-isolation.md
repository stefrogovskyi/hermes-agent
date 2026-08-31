# Telegram Team Authorization, Slash Commands & Session Isolation Architecture

Master reference for opening Telegram access to team members while guaranteeing absolute session isolation, admin protection, and seamless user interaction.

## 1. Dual-Layer Allowlisting (`.env` + `config.yaml`)

The Hermes Gateway authorization layer (`gateway/authz_mixin.py`) checks both environment variables and adapter configuration:
- `/opt/hermes/profiles/<profile>/.env`: Must specify `TELEGRAM_ALLOWED_USERS=<id1>,<id2>,...` or `*`. If `.env` contains only a single user ID, all other team members will be rejected with `Unauthorized user` at the platform level before entering the agent loop.
- `/opt/hermes/profiles/<profile>/config.yaml`: Must specify `platforms.telegram.allow_from` with all numeric Telegram User IDs and usernames.

## 2. Non-Admin Slash Command Permissions (`/start` Button Fix)

When non-admin team members press the standard Telegram **«Start»** button, Telegram sends a `/start` slash command. By default, slash commands are restricted to `allow_admin_from`.

To allow team members to start and interact with the agent without encountering `Access denied: /start is restricted to administrators`:
- Configure `user_allowed_commands` in `config.yaml` under `platforms.telegram`:
  ```yaml
  platforms:
    telegram:
      user_allowed_commands:
        - start
        - help
        - status
        - new
        - clear
        - info
  ```

## 3. Admin Privilege Protection (`allow_admin_from`) & Delivery Targeting

- Always pin `platforms.telegram.allow_admin_from: ['<Admin_User_ID>']` to the owner (Stefan Rogovskiy: `330656040`).
- Prevents non-admin team members from invoking admin commands (`/set`, `/config`) or reconfiguring agent parameters.
- Set `platforms.telegram.home_channel: { platform: 'telegram', chat_id: '<Admin_User_ID>' }` so all cron jobs, notifications, and daily briefings route strictly to the administrator's private DM chat.

## 4. Independent Session Routing & Tone Modes

- **Session Isolation**: Each Telegram user receives an isolated session key (`agent:main:telegram:dm:<USER_ID>`). Inbound messages from team members never interrupt, flush, or contaminate the active admin session.
- **Administrator (Stefan - `330656040`)**: `OPERATIONS CONSOLE` mode (infrastructure, builds, deployments, audits, mass outreach controls).
- **Sales Team Members (Nikita `@nikita51155` / `nikita@navo24.com`, Oleg `8081511707` / `oleg.chervinskyi@navo24.com`, Alona `345948971` / `alyona.holubova@navo24.com`, Kate `149598904` / `ekaterina.kapustian@navo24.com`, Liliia `lilia.k@navo24.com`)**: `SENIOR SALES MENTOR & ASSISTANT` mode.
  * Dedicated context profiles stored in `/opt/hermes/profiles/richard/team/<username>.md` (e.g. `/opt/hermes/profiles/richard/team/nikita.md`).
  * Richard assists team members with customized commercial offers (КП), freight rate calculations, ocean carrier tracking / DCSA inquiries, objection handling against competitors (SeaRates, project44, Vizion, Terminal49), and multilingual email drafting.
  * Guardrails: NEVER expose server `.env` files, API keys, system paths, or administrative configurations to team members. All conversations with colleagues remain strictly isolated from Stefan's admin session.

## 5. Daily Interactions Cron Report

- Nightly summary scheduled at 22:00 Kyiv time (`0 19 * * *` UTC).
- Queries `/opt/hermes/profiles/richard/state.db` for the last 24 hours of messages from team IDs and delivers a concise 3-part brief (Who spoke, Core topic, Outcome/Action items) directly to the administrator.
