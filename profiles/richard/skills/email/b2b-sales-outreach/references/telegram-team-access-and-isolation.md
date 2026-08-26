# Telegram Team Authorization & Session Isolation Architecture

Master reference for opening Telegram access to team members while guaranteeing absolute session isolation and admin protection.

## 1. Core Principles

1. **Dual-Layer Allowlisting (`.env` + `config.yaml`)**:
   - The Hermes Gateway authorization layer (`gateway/authz_mixin.py`) checks both environment variables and adapter configuration.
   - `/opt/hermes/profiles/<profile>/.env`: Must specify `TELEGRAM_ALLOWED_USERS=<id1>,<id2>,...` or `*`. If `.env` contains only a single user ID, all other team members will be rejected with `Unauthorized user` at the platform level.
   - `/opt/hermes/profiles/<profile>/config.yaml`: Must specify `platforms.telegram.allow_from` with all numeric Telegram User IDs and usernames.

2. **Admin Privilege Protection (`allow_admin_from`)**:
   - Always pin `platforms.telegram.allow_admin_from: ['<Admin_User_ID>']` to the owner (Stefan Rogovskiy: `330656040`).
   - Prevents non-admin team members from invoking admin commands (`/new`, `/set`, `/config`, `/stop`) or reconfiguring agent parameters.

3. **Fixed Delivery Target (`home_channel`)**:
   - Set `platforms.telegram.home_channel: { platform: 'telegram', chat_id: '<Admin_User_ID>' }`.
   - Ensures all scheduled cron jobs, notifications, and daily briefings route strictly to the administrator's private DM chat.

4. **Independent Session Routing (Anti-Contamination)**:
   - Each Telegram user communicating in private messages receives an isolated session key (`agent:main:telegram:dm:<USER_ID>`).
   - Inbound messages from team members NEVER interrupt, flush, or contaminate the active admin session.

5. **Operational Modes by Audience**:
   - **Administrator (Stefan)**: `OPERATIONS CONSOLE` mode (infrastructure, builds, deployments, audits, mass outreach controls).
   - **Team Members (Oleg, Alexey, etc.)**: `DOMAIN EXPERT / SALES` mode (B2B sales strategy, API capabilities, client handling, lead qualification).
