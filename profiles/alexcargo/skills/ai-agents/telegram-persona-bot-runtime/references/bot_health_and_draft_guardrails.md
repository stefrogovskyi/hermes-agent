# Bot Health Check & Draft Approval Guardrails

## 1. Real Semantic LLM Health Check vs Fake PID Check
Never rely on `psutil.pid_exists(pid)` alone for bot health checks. A Python OS process can remain alive in Task Manager while returning `401 Unauthorized`, `403 Forbidden`, or template "stub/setup" error messages due to an invalid/expired API key or dead model endpoint.

- **Rule:** A valid health check MUST execute a **real semantic LLM test query** (e.g. `run_agent("ping test")`).
- **Verification:** Inspect the returned text: if it is empty, contains "mode/setup" error strings, or throws HTTP errors, treat the bot as DOWN, repair its credentials/model endpoints, and trigger a restart.

## 2. Email Draft Approval Hard Guardrail
When a Telegram sales/support bot (like Richard Marlowe) drafts an email response for human approval before sending:
- **Hard Guardrail:** Execute the draft generation LLM call with `tools=None` (no tool calls passed).
- This physically prevents the LLM from executing a `send_email` tool call during draft generation. The email MUST ONLY be sent when the user explicitly approves it via Telegram ("Отправляй" / "Да" / "OK") inside a dedicated deterministic handler.

## 3. Microsoft To-Do & Make.com Webhook Integration
When connecting Microsoft To-Do for personal Microsoft accounts (`@i.ua` / `@hotmail.com` / `@gmail.com`):
- Avoid custom Azure App Registrations that fail on single-tenant / personal account restrictions.
- Use a Make.com scenario: `Custom Webhook` -> `Microsoft To Do (List Tasks)` -> `Webhook Response (200, {{body}})`. Make handles OAuth natively using its pre-approved Microsoft App Registration.
- Hermes simply queries the Make Webhook URL (`MAKE_TODO_WEBHOOK_URL`) to receive clean tasks JSON.
