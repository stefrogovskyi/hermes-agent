# Telegram Persona Bot — Runtime Pitfalls & Direct Gemini API Routing

This reference captures key runtime gotchas and debugging patterns discovered when operating Telegram persona bots (such as Alistair, Richard, Liz, Ben, Callum) on Windows hosts.

---

## 1. Russian Name Declensions in Group Mention Regex

When a persona bot is added to Telegram working groups, users will address it using Russian declensions (*«Алистера», «Алистеру», «Алистером», «Алистере», «Алику»*). An exact string match regex like `r"алистер|alistair"` will cause the bot to silently ignore group messages addressed to it.

- **Pitfall:** `NAME_RE = re.compile(r"(алистер|alistair|allister|alister)", re.IGNORECASE)` ignores declensions like `Алистера`, `Алистеру`, `Алистером`.
- **Fix Pattern:** Use word boundaries with Russian suffix wildcard:
  ```python
  NAME_RE = re.compile(r"\b(алистер[а-я]*|alistair[a-z]*|allister|alister|алику?)\b", re.IGNORECASE)
  ```

---

## 2. Windows Console Emoji Encoding Crash (`charmap` codec error)

On Windows hosts, long-lived background Python processes logging or printing emojis (🗓️, 💡, 📊, 🚀) to `stdout` or `stderr` crash with `UnicodeEncodeError: 'charmap' codec can't encode character...` when stdout defaults to CP1251/CP1252.

- **Fix Pattern:** Reconfigure `sys.stdout` and `sys.stderr` to UTF-8 with `errors='replace'` at the very top of every bot script:
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

## 3. Direct Google Gemini API Endpoint via OpenAI SDK

Google AI Studio exposes a native, OpenAI-compatible endpoint at `https://generativelanguage.googleapis.com/v1beta/openai/`.

- **Configuration:**
  - Base URL: `https://generativelanguage.googleapis.com/v1beta/openai/`
  - Key: `GEMINI_API_KEY` or `GOOGLE_API_KEY`
  - Models: `gemini-2.5-flash`, `gemini-1.5-flash`
- **Benefits:** Direct Google connection bypasses third-party rate limits (e.g. Nous / OpenRouter free tier limits) and eliminates 404/400 provider errors with instant <1s response times.

### OpenRouter `max_tokens` Gotcha for Gemini
When routing Gemini models through OpenRouter instead of direct Google API, OpenRouter defaults `max_tokens` to `65535` if omitted. This triggers a `402 Payment Required / Insufficient Credits` error on OpenRouter free tier.
- **Fix:** Always set `max_tokens: 2048` explicitly in `kwargs`:
  ```python
  kwargs = {"model": "google/gemini-2.5-flash", "messages": messages, "timeout": 120, "max_tokens": 2048}
  ```
