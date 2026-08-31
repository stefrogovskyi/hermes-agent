# Bot / Agent Self-Verification — concrete recipe

Goal: confirm a bot's real behaviour (answer + model/provider) WITHOUT asking
Stefan to message it and WITHOUT manually calling Telegram `getUpdates` (which
409-conflicts with the bot's own long-poll and eats its queue).

## Recipe: call the bot's logic in the same runtime

```python
import os, importlib.util

# 1) load the bot's own .env.local into os.environ (so NOUS_API_KEY etc. resolve)
here = r"C:\Users\Stefan\My Drive\Equity\My Biz\...\Richard Hermes"
for envf in (".env", ".env.local"):
    p = os.path.join(here, envf)
    if os.path.exists(p):
        for line in open(p, encoding="utf-8"):
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip().strip('"').strip("'")

# 2) import the bot module without running its main loop
spec = importlib.util.spec_from_file_location("rb", os.path.join(here, "richard_bot.py"))
rb = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(rb)   # may call bot_loop() on import -> wrap in try/except SystemExit
except SystemExit:
    pass

# 3) call its LLM entrypoint directly and inspect the answer
out = rb.llm_chat([{"role": "user", "content": "ping"}])
print(out["choices"][0]["message"].get("content"))
```

## To capture which model/provider actually answered

Monkeypatch the SDK client's `create` (or wrap `llm_chat`) to log `kwargs["model"]`
and the base URL before the call returns. This proves the bot really hit Nous/hy3
(and is not silently falling back to OpenRouter).

## Nous gotcha (critical)

A bare `urllib.request.urlopen` POST to `inference-api.nousresearch.com/v1/chat/completions`
returns **403** even with a valid key. Nous accepts requests ONLY via the OpenAI
SDK client:
```python
from agent.auxiliary_client import _resolve_nous_pool_runtime_api, _create_openai_client
creds = _resolve_nous_pool_runtime_api(force_refresh=False)
client = _create_openai_client(api_key=creds[0], base_url=creds[1])
resp = client.chat.completions.create(model="tencent/hy3:free", messages=[...])
```
If a bot 403s with urllib — switch its `llm_chat` to this SDK client. Do NOT treat
the 403 as a dead key (Hermes itself uses the SDK and works).
