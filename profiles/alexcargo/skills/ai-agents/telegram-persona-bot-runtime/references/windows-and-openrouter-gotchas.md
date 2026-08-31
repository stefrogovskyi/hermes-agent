# Windows Console, Russian Declensions & OpenRouter Gemini Gotchas (2026-07-31)

### 1. Windows Console Unicode/Emoji Encoding Crash
When Python stdlib bots or long-polling daemons print log messages or message excerpts containing emojis (e.g. 🗓️, 💡, 📊) to `stdout`/`stderr` on Windows, Python's default console encoding (`charmap`/`cp1251`) throws a fatal `UnicodeEncodeError`.
**Fix:** Add `sys.stdout.reconfigure` protection at script startup:
```python
import sys
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
```

### 2. Russian Telegram Group Name Declensions in `NAME_RE`
When an AI bot in a Telegram group is configured to listen for mentions of its name in text (e.g. `NAME_RE`), matching only the exact nominative name (`алистер` or `alistair`) causes the bot to ignore group messages written in Russian oblique cases (*«Алистера», «Алистеру», «Алистером», «Алистере»*).
**Fix:** Use regex matching with stem suffix wildcards and word boundaries:
```python
NAME_RE = re.compile(r"\b(алистер[а-я]*|alistair[a-z]*|allister|alister|алику?)\b", re.IGNORECASE)
```

### 3. OpenRouter Gemini `max_tokens` HTTP 402 Gotcha
Omitting `max_tokens` when invoking Google Gemini models (`google/gemini-2.5-flash`) via OpenRouter using OpenAI-compatible SDK defaults `max_tokens` to `65535`. OpenRouter evaluates the prompt budget against 65k tokens and rejects the call with HTTP 402 ("requires more credits... requested up to 65535 tokens") even when the account has sufficient balance for a normal response.
**Fix:** Always explicitly pass `max_tokens=2048` or `max_tokens=4096` in `kwargs` for OpenRouter model calls:
```python
kwargs = {
    "model": model,
    "messages": messages,
    "timeout": 120,
    "max_tokens": 2048  # Prevents OpenRouter 65k max_tokens credit rejection
}
```
