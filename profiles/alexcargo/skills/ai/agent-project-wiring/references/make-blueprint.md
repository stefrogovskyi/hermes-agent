# Make.com blueprint notes (used for richard-marlowe Retell->LLM->Navo->Telegram)

## Module map
- `gateway:CustomWebHook` (x2): one for Retell call events, one for Navo
  monitoring events (e.g. container.free_time_warning).
- `http:ActionSendData` (POST): call the LLM (OpenRouter/Nous) with
  `response_format: json_object` so it returns structured `{action, ref, message}`.
- `http:ActionSendData` (POST): call Navo REST API (Bearer `{{env.NAVO_API_KEY}}`).
- `telegram:sendMessage`: post follow-up / alert to `{{env.TELEGRAM_CHAT_ID}}`.

## CRITICAL gotcha — blueprint export scope
A Make blueprint exports MODULE STRUCTURE + mapping ONLY. It does NOT export
connections (API keys / tokens / bot auth) for security. After import you MUST
recreate connections once:
- Telegram bot connection (@BotFather token)
- Environment variables in the scenario: NOUS_API_KEY, NAVO_API_KEY, TELEGRAM_CHAT_ID
- Retell webhook: paste the Make-generated Webhook URL into Retell's
  call-event destination.
- Navo webhook: paste the second Make Webhook URL into Navo's event endpoint.

## Why Make over n8n
User has Make experience and prefers it. Make's visual editor + env-var
`{{env.*}}` pattern is low-friction for this. n8n is fine too but not chosen here.

## Extension point
The Navo HTTP module is hardcoded to `get_container_detail`. For a real
build, branch on `{{2.body.action}}`: if `rate` → POST
`freightratesmcp.com/api/v1/get_lane_rate`; if `container` → tracking; else skip.
See make_setup.md in the project folder for the full import walkthrough.