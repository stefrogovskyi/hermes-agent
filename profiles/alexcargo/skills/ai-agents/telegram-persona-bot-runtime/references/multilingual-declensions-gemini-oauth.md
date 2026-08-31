# Multilingual Declensions, Direct Gemini API, and Google OAuth Token Diagnostics

### 1. Multilingual Russian Declension Name Triggers in Telegram Group Chats
When a Telegram persona bot operates in multilingual or Russian-speaking group chats, users address the bot using Russian noun declensions (e.g. `Алистер`, `Алистера`, `Алистеру`, `Алистером`, `Алистере`, `Алику`).
- **Pitfall**: A strict regex like `r"(алистер|alistair)"` fails on declensions like `Алистера` or `Алистеру`, causing the bot to ignore group mentions from team members.
- **Fix**: Use regex with Russian declension wildcards and word boundaries:
  ```python
  NAME_RE = re.compile(r"\b(алистер[а-я]*|alistair[a-z]*|allister|alister|алику?)\b", re.IGNORECASE)
  ```

### 2. Direct Google Gemini API Endpoint & OpenRouter `max_tokens` Gotcha
- **Direct Google AI Studio API**: Google provides an OpenAI-compatible endpoint at `https://generativelanguage.googleapis.com/v1beta/openai/`. Use `OpenAI(api_key=GEMINI_API_KEY, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")` with model `gemini-2.5-flash` for direct, instant Google inference.
- **OpenRouter `max_tokens` Gotcha**: OpenRouter defaults `max_tokens` to `65535` if omitted when calling `google/gemini-2.5-flash`, which triggers OpenRouter credit limit 402/429 errors (`This request requires more credits...`). Always set `max_tokens=2048` or `4096` in `kwargs` for OpenRouter calls.

### 3. Google Workspace OAuth `invalid_grant` Token Diagnostic
- When a local bot agent uses Google Sheets API (`google_token.json`) and the `refresh_token` becomes revoked or expired, API calls return `HTTP 400: Bad Request (invalid_grant: Token has been expired or revoked)`.
- **Symptom**: The bot cannot read live sheet data, falls back to static LLM responses, and hallucinates task lists.
- **Fix**: Direct the user to re-authorize via Google OAuth consent URL (`https://accounts.google.com/o/oauth2/v2/auth?...`), exchange the authorization code for a fresh token, and save to `google_token.json`.
