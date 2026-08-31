# Dynamic Pool Resolver & Model Fallbacks

## 1. Dynamic Pool Token Resolution
Never rely on a static `NOUS_API_KEY` hardcoded in `.env.local` for standalone bots or background scanner scripts (`richard_scanner.py`, `alistair_bot.py`, etc.). Static keys expire or hit HTTP 401/403. Instead, resolve the fresh pool token dynamically:

```python
import sys, os
sys.path.insert(0, r"C:\Users\Stefan\AppData\Local\hermes\hermes-agent")
from agent.auxiliary_client import (_resolve_nous_pool_runtime_api, _create_openai_client)

creds = _resolve_nous_pool_runtime_api(force_refresh=False)
if creds and creds[0]:
    key, base_url = creds
    client = _create_openai_client(api_key=key, base_url=base_url)
```

Always pair this with an OpenRouter API key fallback (`OPENROUTER_API_KEY` with `openrouter/free`) in case the Nous pool endpoint fails.

## 2. Deprecated / 403 Model Recovery
When a model like `tencent/hy3:free` or similar free tier returns HTTP 403 Forbidden / 404 Not Found:
1. Update `ALISTAIR_MODEL` / `RICHARD_MODEL` in `.env.local` to an active working fallback model (e.g. `poolside/laguna-s-2.1:free`).
2. Restart the bot process via its watchdog script (`alistair_watchdog.py`).
