# Case: Microsoft To-Do Integration via Make.com Webhook

## Summary
- **Date**: 2026-08-03
- **Domain**: personal / business
- **Context**: Connecting Stefan's personal Microsoft account (`supremo@i.ua`) to Hermes without tenant/OAuth scope conflicts.

## Solution & Method
- Integrated via Make.com scenario webhook (`fetch_todo_from_make_webhook.py`).
- Make.com handles personal OAuth authentication for MS To-Do, exposing a secure JSON payload endpoint to Hermes.
- Poller extracts tasks across multiple To-Do lists and task groups.

## Key Lesson
- Using Make.com as an OAuth middleware bridge is ideal for personal accounts when local Azure App registrations face tenant mismatch errors.
