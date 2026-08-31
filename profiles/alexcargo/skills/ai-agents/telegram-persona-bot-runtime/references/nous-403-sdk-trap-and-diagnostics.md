# Nous inference 403 + local-bot diagnostics — hard-won lessons

Two traps cost a full debugging session on the Richard Marlowe / Navo bot. Both
recur for any local Python bot that reuses Hermes' Nous (tencent/hy3:free) key.

## TRAP 1 — Raw `urllib` to Nous inference returns 403 even with a valid key

**Symptom:** bot's `run_agent` falls into the exception handler and replies with a
stub like "Richard here — briefly lost the line to the desk." Log shows
`HTTP Error 403: Forbidden` on every model (hy3, poolside, stepfun…).

**Wrong conclusion (do NOT make it):** "the Nous key / endpoint is dead, Hermes must
be silently falling back to OpenRouter." This is a false deduction. If the orchestrator
(Hermes) is still answering on its default model and did NOT announce a provider switch,
it is still on `tencent/hy3:free` via Nous. A standalone `urllib.request` POST to
`https://inference-api.nousresearch.com/v1/chat/completions` with the same key returns
403 — but the OpenAI SDK call with the same key returns a real answer. Nous only accepts
the request shape the SDK produces (certain headers / formatting that raw urllib misses).

**Correct fix:** make the local bot call Nous through the SAME client Hermes uses, do not
re-implement the HTTP call. In `richard_bot.py` (or any sibling bot) replace the raw
`urllib` POST with:

```python
import sys
sys.path.insert(0, r"C:\Users\Stefan\AppData\Local\hermes\hermes-agent")
from agent.auxiliary_client import (_resolve_nous_pool_runtime_api,
                                    _create_openai_client)
creds = _resolve_nous_pool_runtime_api(force_refresh=False)   # (api_key, base_url)
if creds and creds[0]:
    key, base_url = creds
    client = _create_openai_client(api_key=key, base_url=base_url)
    resp = client.chat.completions.create(model=model, messages=messages, timeout=120)
    msg = resp.choices[0].message
    return {"choices": [{"message": {"content": msg.content or "",
                                     "tool_calls": msg.tool_calls}}]}
```

`_resolve_nous_pool_runtime_api` auto-refreshes the agent_key from the Nous pool, so the
bot stays live without copying a static (soon-expired) token. Keep OpenRouter as a
secondary fallback (Hermes config.yaml lists `fallback_providers: openrouter`), but the
primary path is the SDK call above.

**Verification recipe (run from the bot's own folder so `.env.local` loads):**
```python
import os, importlib.util
here=os.getcwd()
for envf in ('.env','.env.local'):
    p=os.path.join(here,envf)
    if os.path.exists(p):
        for line in open(p,encoding='utf-8'):
            line=line.strip()
            if not line or line.startswith('#') or '=' not in line: continue
            k,v=line.split('=',1); k=k.strip(); v=v.strip().strip('"').strip("'")
            if k: os.environ[k]=v
spec=importlib.util.spec_from_file_location("rb","richard_bot.py")
rb=importlib.util.module_from_spec(spec)
try: spec.loader.exec_module(rb)
except SystemExit: pass
print(rb.llm_chat([{"role":"user","content":"ping"}]))
```
If this prints a real completion (not a stub), the bot is healthy.

## TRAP 2 — Manual `getUpdates` for diagnostics silently eats the bot's queue

**Symptom:** you run a one-off `getUpdates` via the Telegram API to "check if messages
arrive", and afterwards the bot stops answering in private chat ("lost the line").

**Why:** Telegram long-polling is single-consumer per token. A manual `getUpdates`
with `offset=-1` consumes the pending update and advances the offset; the bot's own
poller never sees that message. Worse, a concurrent manual `getUpdates` returns
`409 Conflict` against the bot's own poller, and the two fight over the queue.

**Rule:** NEVER call `getUpdates` by hand against a bot that is currently running its
own poller. To diagnose, either (a) kill the bot first, then probe, or (b) just send the
bot a message and read ITS log file — do not touch the API. The log (e.g.
`richard_run.log`) shows `[stefan/pm] <chat_id>` when it received your message and the
`agent error:` / `403` lines if generation failed.

## Reasoning discipline (Stefan's correction, apply to all debugging)

When the orchestrator is clearly still working on its default model (it would announce a
provider/model switch per standing rules but did not), infer the KEY AND MODEL ARE FINE.
The bug is in the local bot's CALL CODE, not the credential. Do not "prove" a key is dead
with a crude raw-HTTP test that the real client would pass — verify HOW the working
process actually sends the request (OpenAI SDK) before concluding the provider is down.
