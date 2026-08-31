# Gemini API, Group Mention Declensions & Windows Stdout Gotchas for Telegram Persona Bots

This reference documents 4 critical pitfalls and solutions discovered during Telegram persona bot runtime operations on Windows hosts:

---

### 1. Direct Google Gemini API Integration (`https://generativelanguage.googleapis.com/v1beta/openai/`)
When using Google Gemini models (`gemini-2.5-flash`, `gemini-1.5-flash`) for persona bots:
- Routing through Nous Portal or OpenRouter free tiers often encounters 404 model-slug deprecations or 429 rate limits (20 req/min).
- **Solution:** Use Google's official OpenAI-compatible endpoint with direct `GEMINI_API_KEY`:
  ```python
  from openai import OpenAI

  g_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
  if g_key:
      client = OpenAI(
          api_key=g_key,
          base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
      )
      resp = client.chat.completions.create(
          model="gemini-2.5-flash",
          messages=messages,
          max_tokens=2048,
          timeout=120
      )
  ```
- **Max Tokens Pitfall:** OpenRouter defaults `max_tokens` to `65535` if omitted, triggering `HTTP 402 / 429 Payment Required` on free tier accounts. ALWAYS pass `max_tokens=2048` or `4096` explicitly in `kwargs`.

---

### 2. Russian Declensions in Telegram Group Mention Regex
In Telegram group chats, team members mention bots using Russian inflections and declensions (e.g. *«Алистера»*, *«Алистеру»*, *«Алистером»*, *«Алистере»*).
- **Pitfall:** Using exact string match `r"(алистер|alistair)"` causes the bot to ignore group messages from colleagues when they decline the bot's name grammatically.
- **Solution:** Use regex word boundaries with Russian suffix wildcard matching:
  ```python
  NAME_RE = re.compile(r"\b(алистер[а-я]*|alistair[a-z]*|allister|alister|алику?)\b", re.IGNORECASE)
  ```

---

### 3. Windows Console `charmap` Unicode stdout Crash
When running Python stdlib long-polling Telegram bots on Windows hosts:
- Printing log messages containing emojis (🗓️, 💡, 📊, 🚀) causes a fatal `UnicodeEncodeError: 'charmap' codec can't encode character...` crash in standard Windows Command Prompt / PowerShell.
- **Solution:** Force UTF-8 re-configuration for `stdout` and `stderr` at the top of the main bot script:
  ```python
  import sys
  if hasattr(sys.stdout, 'reconfigure'):
      try:
          sys.stdout.reconfigure(encoding='utf-8', errors='replace')
          sys.stderr.reconfigure(encoding='utf-8', errors='replace')
      except Exception:
          pass
  ```

---

### 4. OAuth2 Google Sheets Token Expiry (`invalid_grant`)
When the bot uses Google Sheets API for task tracker operations (`tasktracker_client.py`):
- If `google_token.json` gets revoked or expires, Sheets API calls fail with `HTTP Error 400: Bad Request (invalid_grant)`.
- Without error handling, LLM receives `400` errors, lacks live sheet context, and falls back to hallucinated dummy responses.
- **Solution:** Catch `HTTPError` in `_g_token()`, alert the admin to re-run the OAuth consent link (`https://accounts.google.com/o/oauth2/v2/auth?...&access_type=offline&prompt=consent`), exchange code for fresh `google_token.json`, and resume live Sheet reading.
