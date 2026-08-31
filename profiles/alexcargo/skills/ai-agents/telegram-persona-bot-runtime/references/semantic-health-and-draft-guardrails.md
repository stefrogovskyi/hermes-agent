# Semantic LLM Health Checks, Draft Guardrails & Persistent Tracking

## 1. Real Semantic LLM Health Check
Never rely solely on `psutil.pid_exists(pid)`. A running Python process can be alive in Task Manager while returning 401/403/404 errors or stencil failure messages ("LLM key not connected" / "lost the line").
Watchdogs (`bot_watchdog.py`) MUST execute a real semantic LLM test message (`run_agent('ping')`) and inspect the text output. If the response contains a stencil error, the watchdog must auto-heal credentials and restart the bot.

## 2. Hard Guardrails for Telegram Approval Drafts
When an agent polls external channels (e.g. MS Graph email inbox) to compose draft responses for user approval in Telegram:
- **ALWAYS pass `tools=None` during draft generation.**
- Without `tools=None`, the LLM may execute `send_email` tool calls during draft generation, sending the email to the customer BEFORE the user confirms.
- Email sending (`send_email_direct`) MUST ONLY be executed inside the Telegram approval command handler (`_check_and_execute_draft_approval`) AFTER the user explicitly replies "Отправляй", "Да", or "Ок".

## 3. Persistent Message Tracking
Do NOT add existing inbox messages to an in-memory `seen_msg_ids` set at startup. This causes unnotified incoming messages to be skipped forever across bot restarts.
Store processed message IDs in a persistent disk file (`processed_email_ids.json`). Only append a message ID AFTER the Telegram notification has successfully been delivered to the user.
