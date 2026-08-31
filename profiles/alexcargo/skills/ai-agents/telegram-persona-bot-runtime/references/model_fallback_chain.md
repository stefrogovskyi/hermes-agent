# Model Fallback Chain for stdlib Telegram Persona Bots

## Why
When a bot is pinned to a free model (e.g. `tencent/hy3:free`), providers overload
and return `502` / `429` / timeouts. The Telegram user then sees the bot "stuck on
Typing…" forever or a `model provider failed after retries` error. The fix is an
in-bot fallback chain that retries the SAME user message against the next free model
in a shared list — no gateway restart, no user action.

## Pattern (drop-in)
Add near the bot's `MODEL = os.environ.get("..._MODEL", "tencent/hy3:free")` line:

```python
# ---- Model fallback chain (free models only) ----
# On primary-model failure (502/429/timeout) try the next free Nous model.
# List is hot-reloaded from free_models.json (refreshed daily by refresh_free_models.py);
# falls back to this static set if the file is missing.
_FREE_MODELS_FILE = r"C:\Users\Stefan\AppData\Local\hermes\scripts\free_models.json"
_fb_cache = None
_fb_mtime = 0.0
def _load_fallback_models():
    global _fb_cache, _fb_mtime
    try:
        mt = os.path.getmtime(_FREE_MODELS_FILE)
    except Exception:
        mt = 0.0
    if _fb_cache is None or mt != _fb_mtime:
        try:
            with open(_FREE_MODELS_FILE, encoding="utf-8") as _f:
                _lst = json.load(_f)
            if isinstance(_lst, list) and _lst:
                _fb_cache = _lst
                _fb_mtime = mt
        except Exception:
            pass
    if _fb_cache:
        return _fb_cache
    return ["poolside/laguna-s-2.1:free", "stepfun/step-3.7-flash:free",
            "poolside/laguna-xs-2.1:free"]
```

Replace the bot's `llm_chat(messages, tools=None)`:

```python
def llm_chat(messages, tools=None):
    models = [MODEL] + [m for m in _load_fallback_models() if m != MODEL]
    last = None
    for model in models:
        try:
            token = _fresh_nous_token()      # keep existing token-refresh helper
            headers = {"Authorization": "Bearer %s" % token,
                       "Content-Type": "application/json"}
            payload = {"model": model, "messages": messages}
            if tools:
                payload["tools"] = tools
                payload["tool_choice"] = "auto"
            return _http_json(OPENROUTER_URL, headers=headers, body=payload)
        except urllib.error.HTTPError as e:
            last = e
            if e.code == 401:
                print("[bot] LLM 401 — re-reading fresh token from auth.json")
                time.sleep(1)
                continue
            print("[bot] model %s failed: %s; trying next" % (model, e))
            raise
        except Exception as e:
            last = e
            print("[bot] model %s failed: %s; trying next" % (model, e))
    raise last
```

## PITFALL: orphaned `llm_chat` tail when patching
When replacing an existing `llm_chat` whose body ends with a `for attempt in
range(2): ... raise` loop, the old tail (`time.sleep(1) / continue / raise /
raise last`) is NOT part of your `old_string`, so it remains and causes
`IndentationError: unexpected indent`. After patching, `py_compile` the file and
delete the dangling lines (everything after the new `raise last`).

## Shared list refresher (cron, no_agent)
`refresh_free_models.py` (in `hermes/scripts/`) queries
`https://inference-api.nousresearch.com/v1/models`, keeps only `:free` ids, writes
`free_models.json` with `tencent/hy3:free` first. Run daily (e.g. `0 4 * * *`) so
new free models (e.g. `ling-3.0-flash:free`) are picked up automatically without
asking the user. The API key is read from Liz's `.env.local` NOUS_API_KEY.

## Only the gateway needs `fallback_providers` in config.yaml
Hermes itself (Desktop + Telegram) uses `fallback_providers:` (a top-level list of
`{provider, model}` in `config.yaml`) for the same purpose. The bots above are
separate stdlib programs and need this in-code chain instead — they do NOT read
`config.yaml` fallback_providers.
