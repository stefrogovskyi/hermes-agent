# Case: 2026-08-08 — Standalone Interactive Vercel Kanban Board per Hermes Profile

## Symptom / Request
Stefan requested an updated, interactive Trello-style Kanban board for Hermes Stevenson deployed on Vercel (`hermes-stevenson-kanban.vercel.app`). Key requirements included interactive card popups with event timeline/comment history, global Escape key listener for closing modals, auto-refresh interval, and self-contained serverless API storage.

Additionally, Stefan clarified a core architecture rule:
"Я не уверен что этот канбан должен быть привязан к домену Аваланч, также он не должен быть связан с Каллумом. У каждого профиля будет свой канбан, пока работаем лишь над канбаном Гермеса"

## Root Cause / Context
Initial setup tied the board API to Avalanche agency domain or shared backend assets across profiles. Each Hermes profile represents a distinct agent/virtual employee with its own tasks, state, and dashboard.

## Solution & Verification
1. Created self-contained Vercel Serverless deployment for `hermes-stevenson-kanban.vercel.app`.
2. Backend API implemented directly on Vercel at `/api/kanban` (self-contained JSON storage, 0 external domain dependency).
3. Added interactive features:
   - Click card to open modal popup with "💬 Event History & Comments" section.
   - Global `Escape` key event listener for modal window dismissal.
   - Auto-refresh mechanism for real-time task updates.
4. Verified deployment via `web_extract` on `https://hermes-stevenson-kanban.vercel.app/api/kanban` (HTTP 200).

## Core Principles & Lessons
- **Profile Isolation for Dashboards/Kanban**: Every Hermes profile (Hermes, Callum, Alistair, etc.) must have its own isolated Kanban board / dashboard. Never couple agent task boards to shared organizational domains or other sub-agent profiles unless explicitly directed.
- **Self-Contained Serverless Architecture**: Vercel Serverless `/api/kanban` provides simple, standalone hosting without requiring external database servers for lightweight board state.
