# Domain: Operations & Infrastructure

## Agent Kanbans Architecture
- Host: Vercel (`https://<agent>-kanban.vercel.app` / Hermes: `https://hermes-stevenson-kanban.vercel.app`).
- Legacy URL Cleanup: `https://aavalanche.com/kanban/hermes/` and `https://hermes-kanban.vercel.app/` deprecated and removed.
- Backend API: `https://dev.aavalanche.com/kanban_api.php`.
- Bi-directional sync: Dragging cards, updating comments, and status changes on Vercel reflect back to state.db and agent task tracking.

## Telegram Userbot Parser Infrastructure
- Account session: `@stefrogovskiy` (`/opt/hermes/stefan_userbot.session`).
- Active parsing targets: Channel "Не повредит, Одесса" with precise timestamps (HH:MM).
- Safe auth method: Direct `.session` file import without interactive SMS/OTP codes in chat.

## Aeon Stevenson Framework (@aeondeskbot)
- Host/Engine: Native Aeon (`stefrogovskyi/aeon`) running in GitHub Actions cloud runners (Serverless / Cron Polling).
- Purpose: Background task automation, CI/CD skill execution (`/run <skill>`), self-healing scripts, auto-reviewing PRs.
- Telegram Commands: `/status`, `/harness`, `/run <skill>`, `/cancel`.
