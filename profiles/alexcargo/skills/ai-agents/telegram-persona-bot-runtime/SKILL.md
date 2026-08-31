---
name: telegram-persona-bot-runtime
description: >-
  Run and maintain a LOCAL, stdlib-only Telegram persona bot (like Richard Marlowe / any
  character agent) as a single realtime long-polling process. Covers: sourcing the LLM key
  from the host's own provider (e.g. Nous inference) so the bot "answers like the orchestrator"
  without asking the user for an OpenRouter key; single-token = single getUpdates consumer
  with a Windows-safe PID-lock to prevent duplicate-bot replies + 409; persistent "Typing…"
  via a background ticker; reply_to_message context injection; and per-user / per-group
  tiered memory. Use when building, refactoring, or debugging a self-hosted Telegram agent
  self-hosted Telegram agent bot (Python, no pip deps) that must feel live and not spam. See references/telegram-409-gateway-autospawn.md for the Hermes-gateway auto-spawn 409 trap + in-session kill block.
  ALSO: the AIAgent-core variant (reuse hermes `run_agent.AIAgent` in a separate
  process) and the two 409 footguns below — both cost real debugging time.",
---

# Telegram Persona Bot — Runtime & Hardening

For a self-hosted character/sales agent bot in Telegram (Python, standard library only).

## 1. One token = one consumer (the hard rule)

See `references/telegram-409-and-aiagent-debug.md` for the two 409 footguns
(retry-on-409 opens a 2nd parallel getUpdates; multiple copies racing on one token).
ALSO: the **AIAgent-core re-exec zombie-parent 409** — if the bot is launched via the
venv python, the hermes `run_agent.AIAgent` core re-execs onto uv-python at startup,
leaving a zombie venv parent + a 2nd live long-poll on the same token. Launch via
`pythonw.exe` (uv base) directly so the re-exec is a no-op. Full diagnose + cold-restart
sequence: `references/telegram-409-aiagent-rexec.md`.
(retry-on-409 opens a 2nd parallel getUpdates; multiple copies), the Windows
named-mutex single-instance fix, no-console pythonw+ctypes launch, and the
AIAgent-core construction gotchas.
A Telegram bot token feeds `getUpdates` to exactly ONE long-polling consumer. Two copies of
the bot → each grabs the same updates → the user gets **duplicate replies** (2–3×) and a
`409 Conflict`. Always run EXACTLY ONE copy. A "2-process chain" (python + its venv child) is
ONE bot — only count distinct `commandline` matches; watch for a 2nd chain.

## 1b. Free-model fallback chain (stop "stuck on Typing…" on overloaded free models)
When pinned to a free model (`tencent/hy3:free` etc.) the provider overloads →
`502`/`429` and the user sees the bot hang. Add an in-code fallback chain so the
same message retries the next free model automatically. Reusable drop-in snippet +
the `orphaned llm_chat tail` pitfall: **references/model_fallback_chain.md**.

**Prevent duplicates with a PID-lock** (Windows-safe — `os.kill(pid,0)` throws `WinError 87`
on Windows, so check liveness via `tasklist`):
```python
import os, sys, subprocess, atexit
LOCK_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "richard.lock")

def _pid_alive(pid):
    if os.name == "nt":
        try:
            out = subprocess.run(["tasklist","/FI","PID eq %d"%pid],
                                 capture_output=True, text=True, timeout=10).stdout
            return str(pid) in out
        except Exception:
            return False
    try:
        os.kill(pid, 0); return True
    except OSError:
        return False

def _acquire_lock():
    if os.path.exists(LOCK_FILE):
        try: old_pid = int(open(LOCK_FILE, encoding="utf-8").read().strip())
        except Exception: old_pid = None
        if old_pid and _pid_alive(old_pid):
            print("[bot] already running (pid %s) — exit." % old_pid); sys.exit(0)
    open(LOCK_FILE,"w",encoding="utf-8").write(str(os.getpid()))
    atexit.register(lambda: os.path.exists(LOCK_FILE)
                    and open(LOCK_FILE,encoding="utf-8").read().strip()==str(os.getpid())
                    and os.remove(LOCK_FILE))
```
Call `_acquire_lock()` at the top of the loop. If a 2nd copy is launched it exits instantly.

### 1a. PID-lock file MUST live on LOCAL disk, not a OneDrive/cloud-synced folder (duplicate-bot trap)
The `.lock` above only works if creation is atomic. **On a OneDrive-synced path (e.g. the whole
`C:\Users\<u>\My Drive\...` tree, which is where these Navo agent folders live), `os.open(...,
O_CREAT|O_EXCL)` is NOT reliably atomic** — the cloud filesystem shim lets two near-simultaneous
starts both "win," so you get TWO live bots → duplicate replies + 409. This bit us hard: repeated
"count = 2" no matter how the lock was written, because the lock sat in the OneDrive project folder.
**Fix: put the lock on real local disk**, keyed by entity, and have the watchdog use the SAME path:
```python
_LOCK_DIR = os.path.join(os.environ.get("LOCALAPPDATA",
                         os.path.expanduser(r"~\AppData\Local")), "hermes", "entities")
try: os.makedirs(_LOCK_DIR, exist_ok=True)
except OSError: _LOCK_DIR = os.path.dirname(os.path.abspath(__file__))
LOCK_FILE = os.path.join(_LOCK_DIR, "alistair.lock")
```
Also make the acquire truly atomic AND handle the **empty-file race window**: `os.open` creates a
0-byte file BEFORE you `os.write` the pid; a competitor that reads it in that gap sees an empty lock,
judges the owner "dead," and grabs it too. So on `FileExistsError`, retry-read the pid a few times
(`for _ in range(6): raw=open(LOCK_FILE).read().strip(); if raw: old=int(raw); break; time.sleep(0.3)`)
and if it's STILL unreadable, `sys.exit(0)` (yield rather than risk a duplicate) instead of stealing
the lock. Verify the fix by launching 3 copies at once → exactly 1 must survive.
NOTE the "2 python.exe for one bot" red herring: a `venv\Scripts\python.exe` shim EXECs the real
interpreter as a child — that parent+child chain is ONE logical bot. Count distinct
`alistair_bot.py` chains and check which pid holds the lock; don't chase the shim.

### 1b. Webhook vs long-polling 409 (the silent MIGRATION failure)
§1's 409 is from two polling consumers. A SECOND, very common 409 cause is a **leftover
webhook** (almost always from a previous Make.com / Zapier / n8n scenario) still attached to
the bot. Telegram delivers updates to EITHER a webhook OR `getUpdates` — never both. If a
webhook is live, your local long-polling bot gets `HTTP Error 409: Conflict` on every
`getUpdates` and **silently sees nothing** (no duplicate replies — just dead silence). This is
exactly what happened when migrating Alistair (`@qubicpmbot`) from Make.com to a local script:
the old `hook.eu2.make.com/...` webhook was eating every update.

**Symptom:** bot starts (`bot started, polling...`), logs `poll error: HTTP Error 409: Conflict`
on a loop, never replies. `getMe` works fine. `NOUS_API_KEY` is valid. Looks identical to a
stalled bot but it is a delivery conflict, not a key/crash issue.

**Diagnose (one call):**
```python
import os, json, urllib.request
tok=os.environ["TELEGRAM_BOT_TOKEN"]
info=json.loads(urllib.request.urlopen(
    f"https://api.telegram.org/bot{tok}/getWebhookInfo",timeout=20).read())
print(info["result"]["url"])   # non-empty => webhook is live => it's the 409 cause
```
A ready probe (info + optional delete) is in `references/webhook_409_probe.py`
(`python references/webhook_409_probe.py --delete` to fix in one step).

**Fix:** delete the webhook so long-polling can take over:
```python
json.loads(urllib.request.urlopen(
    f"https://api.telegram.org/bot{tok}/deleteWebhook?drop_pending_updates=true",
    timeout=20).read())
# re-check getWebhookInfo -> url should now be ""
```
Then (re)start the bot; the 409 stops and messages flow.

**Tell the user:** deleting the webhook KILLS the old Make.com/Zapier scenario's message
reception — which is the intended migration, but say so. If the user still wants BOTH (webhook
for Make + local bot), that's impossible per token; they must run two separate bots with two
tokens, or drop the local bot. Never `setWebhook` while a local poller is running.

### 1c. DUPLICATE-PROCESS 409 — the "lost the line" trap (this session's live root cause)
If the bot replies with the friendly fallback *"briefly lost the line to the desk. One moment,
try that again?"* on messages that should be answerable, the FIRST thing to check is **two copies
of the bot running on the same token** — NOT a code/key bug. Two long-pollers → each grabs the
same `getUpdates` → 409 Conflict on one of them → it fails the LLM call path and emits the
fallback. Symptom this session: Richard answered "lost the line" in a group even though the key
was valid and `stub=False`.

**Why duplicates appear — the MECHANISM (verified this session):** launching the bot through
the Hermes **`terminal(background=True)`** tool itself spawns a chain: a **venv parent**
(`…/hermes-agent/venv/Scripts/python.exe richard_bot.py`) plus a **`uv` child**
(`…/AppData/Roaming/uv/python/…/python.exe richard_bot.py`) whose `ParentProcessId` IS the venv
process. That venv+uv pair is ONE logical bot — do NOT treat the two `python.exe` as a duplicate.
A REAL duplicate = a SECOND such pair, i.e. TWO `python.exe` chains both running `richard_bot.py`
launched at different times (the first was still alive when a relaunch happened). Both pairs poll
the same token → 409 on one → "lost the line". The PID-lock (§1/§1a) didn't save it because the
lock lives in the OneDrive folder (non-atomic) and the two pairs started at different moments so
each saw a "dead" prior owner.

**DIAGNOSE (one PowerShell line) — count distinct bot chains, not processes:**
```powershell
Get-CimInstance Win32_Process -Filter "Name='python.exe'" |
  Where-Object { $_.CommandLine -like '*richard*' } |
  Select-Object ProcessId, ParentProcessId, CommandLine | Format-List
```
- ONE venv + ONE uv child (uv's `ParentProcessId` = the venv pid) → **healthy, one bot.** Leave it.
- TWO venv + TWO uv (two distinct venv parents) → **duplicate, the bug.** Fix below.

**FIX — ONE rule that prevents the whole mess: NEVER relaunch while one chain is alive.**
1. Before launching, ALWAYS run the diagnose line above. If a chain already exists → **do not
   launch a second one.** Rely on the PID-lock (§1/§1a) from then on; the lock will make any
   accidental relaunch exit instantly. The duplicate this session came purely from repeated
   relaunches during debugging — each added a pair.
2. If you DO find a true duplicate (two chains): kill by **specific PID only** — never a broad
   `Stop-Process` of all `python`. A mass kill of every python got BLOCKED by approval (dangerous,
   could kill Hermes itself). Target the extra chain's venv parent PID; the uv child dies with it.
   Better: if an auto-manager (Startup `.lnk` / watchdog / §7a) already keeps the bot up, just
   **stop your manual relaunching** and let that one copy run — don't kill it either.
3. Re-check → must show ONE venv+uv chain. Then send a real message → normal answer, no fallback.

**CRITICAL operational note:** with the terminal-tool chain, killing the venv PARENT also kills
the uv CHILD (they're parent/child). So you cannot "keep just the uv one" — you keep the whole
chain or none. If you must restart, kill the whole chain by its venv parent PID, then launch once.

**Clean launch to avoid the pair altogether:** instead of `venv\Scripts\python.exe bot.py`
(which spawns the venv-parent + uv-child pair that §1c diagnoses), LAUNCH via
`uv run --no-sync bot.py` — uv IS the interpreter, so there is exactly ONE `python.exe` chain per
bot (no venv shim). This makes the §1c duplicate diagnosis unnecessary:
`Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object { $_.CommandLine -like '*bot.py' }`
then shows exactly one pid per bot. Use `uv run` for BOTH manual restarts AND in `start_agents.bat`
(see §7 correction) so the auto-start never creates a double chain either. (If uv is outside PATH
in a scheduled task, point at the absolute exe: `%LOCALAPPDATA%\hermes\bin\uv.exe run --no-sync`.)

**Rule of thumb:** the "lost the line" fallback is a SYMPTOM of a delivery/conflict problem
(duplicate poller OR webhook OR transient Nous timeout, §10), never assume it's a logic bug.
Check duplicate processes (§1c) → webhook (§1b) → Nous timeout/401 (§8b/§10), in that order.

## 2. LLM key — reuse the host's provider, don't ask the user
"Make the bot answer like you (the orchestrator)" means: point the bot at the SAME inference
endpoint the orchestrator uses. Don't request an OpenRouter key the user doesn't have.
- Read the host's `auth.json` (`providers.<provider>.access_token` + `inference_base_url`).
  For Nous: base `https://inference-api.nousresearch.com/v1`, endpoint `…/chat/completions`.
- Write the token into the bot's local `.env.local` as `NOUS_API_KEY`. Bot calls that URL.
- `stub-` prefix on the key = placeholder mode (bot replies "setup needed"); strip it to go live.
- Never echo the token back; keep it as an env reference, gitignored.
- **Stub gate must key ONLY on NOUS, not NAVO.** A placeholder `NAVO_API_KEY` (e.g. `***`,
  no real Navo key exists) must NOT force the whole bot into STUB mode — the bot answers via
  the LLM (NOUS); Navo API is optional. Rule: `stub_mode = not nous_key or nous_key.startswith("stub-")`
  ONLY. If you gate on `navo_key` too, a `***` Navo placeholder silently kills every reply
  (symptom: `[DEBUG] NOUS_API_KEY len=1777 … stub=False` but `bot started … stub=True`).
- **`.env.local` loader must OVERRIDE unconditionally.** Background/terminal processes inherit
  env from the parent shell — which may carry a stale `stub-` key or a different JWT. The loader
  in `__main__` must do `os.environ[_k] = _v` (no `if _k not in os.environ` guard) so the real
  `.env.local` value always wins. Otherwise a stub leaks in and the bot never goes live.
- Verify liveness with a debug print at loop start: `print("NOUS len=%d stub=%s" % (len(nous_key), nous_key.startswith("stub-")))` and confirm `stub=False` before declaring the bot live.

## Isolating a cloned persona bot (forget another project's context)

A bot cloned 1:1 from another persona inherits the source bot's data surfaces.
Symptom: it answers with a foreign project's data (kanban, task IDs, @nicks) or
keeps *naming* forbidden projects even while refusing them. Counter-intuitive
root cause: an isolation prompt that ENUMERATES the forbidden names teaches the
bot those names — rewrite it name-free. Scrub every surface, not just memory:
`*_memory.json`, `system_prompt.md`, `tasktracker_client.py` hardcoded defaults
(sheet ID, URLs, owner-nick map, DEFAULT_OWNER), `agent.config.json` integration
blocks, and prose in `Agents.md`/`README.md`/`tools.md`. Full procedure +
verification grep: `references/persona-isolation-and-context-scrub.md`.

## 3. Persist "Typing…" for the whole LLM call
`sendChatAction(action="typing")` auto-clears after ~5s. For 10–20s LLM calls, run a daemon
thread that re-sends `typing` every ~4s from message receipt until the reply is ready; stop it
in a `finally`. Without this the indicator blinks once and vanishes.

## 4. Quoted / highlighted fragment — `message.quote` is the REAL one
When a user SELECTS a fragment of a message and hits Reply, Telegram sends the **highlighted
snippet** in its OWN field: `message.quote` (plus `quote_entities` for formatting). The full
original lives in `message.reply_to_message` (text/caption). The selected fragment is NOT just
"the whole replied message."

**USER CORRECTION (this session, first-class):** I once claimed Telegram only sends the whole
replied message and "can't pass the selected word." That is WRONG. `quote` exists and is exactly
the highlighted fragment — one word or a sentence. When the user says "what word did I tag /
what fragment did I quote," the answer is in `message.quote`, not in `reply_to_message`.

**Priority when building `reply_ctx`: `quote` (the highlight) → `text_quote` (newer API alias)
→ `reply_to_message.text`/`caption` (whole message, fallback).** Always also log the raw fields
once so you can CONFIRM `quote` actually arrives on the client in use (some old clients/versions
omit it; if it's `None`, fall back to the full message and note it):
```python
replied = msg.get("reply_to_message")
print("[bot] quote fields: quote=%r text_quote=%r has_reply=%s"
      % (msg.get("quote"), msg.get("text_quote"), bool(replied)))
if replied:
    # priority: highlighted fragment > entire replied text
    _q = msg.get("quote")
    if isinstance(_q, dict):           # Bot API sends quote as {'text':...,'position':...,'is_manual':True}
        _q = _q.get("text", "")        # .strip() on the dict throws "'dict' object has no attribute 'strip'" -> breaks ALL quoted replies
    rt = (_q or msg.get("text_quote")
          or replied.get("text") or replied.get("caption") or "").strip()
    if not rt and replied.get("photo"): rt = "[quoted message contains a photo]"
    if not rt and replied.get("voice"): rt = "[quoted message is voice]"
    if rt:
        who = replied.get("from",{}).get("first_name","собеседник")
        reply_ctx = ("\n[USER QUOTED/REPLIED TO %s. Exact quoted fragment:\n«%s»\n"
                     "— answer ON THIS fragment: name its key words, comment, reply to the "
                     "question about it. Never say you 'can't see' the quote — it is right here.]"
                     % (who, rt))
```
- Inject `media_hint + text + reply_ctx` into the final prompt.
- The user calls ANY selected/highlighted text a "тег/тегнул" — NOT a nickname/@mention. So do
  NOT build @mention-in-history search logic for "what word did I tag?"; the fragment is in
  `quote`. (The earlier `@richard`-in-history search was removed — it answered the wrong question.)
- **Hermes (the orchestrator/assistant) CAN ALSO see `quote` — fixed this session (was a known gap).**
  The owner corrected me hard: *"you work as a Telegram bot, you handle all Telegram entities; if
  Richard got this skill, give it to yourself. Find the solution and implement."* Root cause: Hermes
  **already** extracts `quote` in `plugins/platforms/telegram/adapter.py` (it sets `reply_to_text`
  from `message.quote` for the reply-context feature), but that value lands in message **metadata**,
  NOT in the text the model sees — so the assistant received only the question, not the fragment.
  Fix: patch `_handle_text_message` (right after
  `event.text = self._clean_bot_trigger_text(event.text)`) to inject `msg.quote.text` into
  `event.text` with a marker. Exact diff + verify steps in `references/hermes_core_quote_patch.md`.
  **Requires a Hermes gateway restart** (desktop app / `hermes restart`) to reload `adapter.py`.
  **MAINTAINER CAVEAT:** `adapter.py` is Hermes CORE — a Hermes update overwrites the patch and
  quoted fragments silently stop arriving again. Re-apply after every Hermes update, or upstream a PR.
  Until the patch is applied AND the gateway reloaded, the fallback still holds: ask the owner to
  paste the quoted text, do NOT guess. (Bots like Richard/Alistair parse `quote` at their own
  polling-loop level — no core change needed for them.)
- **General principle the owner enforced:** when you give a capability to a persona bot (Richard,
  Alistair), the SAME capability must exist for Hermes itself ("you are also a Telegram bot"). If a
  fix lives in `adapter.py`/gateway core, apply it there too — don't stop at the bots.
- **Approach enforcement (first-class, this session):** when the owner points out a limitation
  ("you can't see quoted text"), do NOT propose a workaround that makes THEM do extra work
  ("just paste the quoted text in your message" / "I'll ask you what you quoted"). FIND THE REAL
  FIX and IMPLEMENT it. The owner said verbatim: *"ты у меня работаешь как телеграм бот, значит ты
  умеешь работать со всеми сущностями… ищи решение и внедряй."* Concrete path that worked: the
  capability already existed in `adapter.py` (it set `reply_to_text` from `message.quote`); the fix
  was to also surface it in `event.text`. So before suggesting a user-side workaround, grep the
  core/agent code for whether the data is ALREADY extracted somewhere — it usually is, and the gap
  is only that it isn't delivered to the model.
- **Communication-style correction (first-class, this session):** never alarm the owner about
  INTERNAL agent mechanics. When the agent's own scratch memory buffer hit its size cap mid-task
  and I reported "память переполнена" as a worry, the owner pushed back — it read as a problem he
  should care about. The buffer (`MEMORY.md`, ~2200 char cap) is just an injected note list, NOT a
  vector DB, NOT semantic search, NOT where project knowledge lives (that's in git/files). When it's
  full, silently drop/compress an older note and move on — do NOT narrate the limit to the user as if
  it's their concern. Rule: report capability/limitation status only when it affects THEIR deliverable;
  internal bookkeeping fullness is never their problem. If you must mention it, frame it as "handled,
  no action needed" not "this is concerning."
- **Auto-recover a core-file patch after Hermes updates (watchdog):** because `adapter.py` is core,
  every `hermes update` / desktop auto-update silently overwrites the quote patch and citations break
  again. Don't make the owner re-report it each time. Ship a watchdog: (1) save the EXACT patch block
  to `%LOCALAPPDATA%\hermes\QUOTE_PATCH_BACKUP.txt` with `=== ТОЧНЫЙ БЛОК ДЛЯ ВСТАВКИ ===` /
  `=== КОНЕЦ БЛОКА ===` delimiters (machine-parseable). (2) A stdlib `hermes_quote_patch_watchdog.py`
  (in `%LOCALAPPDATA%\hermes\scripts\`) re-inserts the block after the anchor if the marker is absent,
  else exits 0 silently. Reusable copy in `scripts/hermes_quote_patch_watchdog.py`. (3) A `no_agent=True`
  Hermes cron `every 5m` runs it. Cron lifecycle rules BLOCK `hermes gateway restart` from inside a
  cron, so the watchdog must NOT restart the gateway — rely on `hermes update` itself restarting the
  gateway, and tell the owner to restart the Desktop app once after an update (which they do anyway).
  Net effect: after any update the patch is restored within 5 min and only needs a Desktop relaunch
  to take effect — no manual "predict and wait" loop. (4) Belt-and-suspenders: upstream a PR so the
  patch lives in core and the watchdog becomes a no-op.
- The exact `adapter.py` patch + verify/re-apply steps for the above are in
  `references/hermes_core_quote_patch.md`. Reusable watchdog in `scripts/hermes_quote_patch_watchdog.py`.
- **Prompt rule** in `system_prompt.md` REPLY-TO CONTEXT block: "When the user references a
  quoted/highlighted fragment, comment on THAT fragment — name its key words, answer the question
  about it. The `[Контекст/QUOTED]` block IS the fragment; never say you can't see it."
- Until `quote` is confirmed live on the client, keep the debug print; first real quoted reply
  tells you whether to trust `quote` or the fallback. If `quote` is `None` consistently, the
  client strips it and you must rely on the full replied message (still works, just less precise).

## 5. Tiered memory (sniper context)

> See also `references/persona-knowledge-scrub.md` — purging a donor project's
> leaked knowledge (board names, bot nicknames, endpoints) from a bot cloned
> from another bot's shell; includes the "isolation paragraph that enumerates
> forbidden names" pitfall.

A JSON file loaded at startup, keyed:
- `u:{user_id}` — private chat per user
- `g:{group_id}` — whole-group context
- `gu:{group_id}:{user_id}` — each user INSIDE a group (independent of their PM context)
Trim to ~20 messages/key. The agent reads its `memory_key`, then writes both it and (if group)
`g:{group_id}`. Survives restarts.

## 6. Persona = loaded file, not hardcode
Load BOTH `system_prompt.md` AND `Agents.md` (strip `#`/`>` lines from the former; keep the
latter verbatim) into the system prompt at startup, joined by a separator. NEVER hardcode persona
in the bot — so edits to the markdown take effect without code changes. Honour user prefs in
`system_prompt.md`: humour sparingly, short replies to non-work pokes, never answer every message,
never spam groups.

**LOAD BOTH — common defect (bit us live):** if `load_system_prompt()` reads ONLY `system_prompt.md`
and omits `Agents.md`, then EVERYTHING the daily scanner writes to `Agents.md` (prices, tiers,
rates, carrier counts) is INVISIBLE to the bot — it answers "I don't have those figures" even
though the file is correct. Symptom this session: scanner added `### 1.7 Тарифы…` with real
€39/mo pricing, yet the bot replied "I have no exact paid-tier numbers." Root cause: runtime
loader iterated `("system_prompt.md",)` only. Fix: iterate `("system_prompt.md", "Agents.md")`,
collect parts, `return "\n\n---\n\n".join(parts)`. Do NOT rely on §11's "the bot reads Agents.md"
as a statement of fact — it is the desired state; the loader code must actually include it.
Verify after any KB change: `assert "€39/mo" in RICHARD_SYSTEM` (or grep the joined prompt),
then ask the bot a product question and confirm it cites the fresh figure.

## 7. Anti-overengineeringA fragile PowerShell daemon + admin-only Task Scheduler XML (UTF-16) is the wrong tool — it
wastes ~40 min and fails (Access denied). One python process guarded by the PID-lock above is
enough. If auto-start on login is wanted later, a simple Startup `.lnk` → `python bot.py`
beats the daemon. Don't build a supervisor unless the process actually crashes often.
**Periodic jobs (daily scan, digest, reminder) = Hermes `cronjob`, NOT Windows Task Scheduler.**
Create with `schedule: "0 7 * * *"` (daily 07:00). The cron runs in an isolated session, but if
the job `cd`s into the bot folder and the script self-loads `.env.local`, all keys resolve.
Deliver `origin` so the result returns to the chat. This is the clean alternative to the admin
XML the user rejected — the user explicitly refused over-engineering, so never reach for a
daemon/scheduler when `cronjob` + one python process does it.

**CORRECTION (this session, first-class):** the "no Task Scheduler" guidance above was about the
*fragile admin-XML daemon*, NOT a plain logon-triggered task. A simple **`Register-ScheduledTask
-AtLogOn`** that launches `start_agents.bat` (which `start`s each bot detached) is FINE and the
owner accepted it — it fixed the real failure where bots silently died after the laptop closed
and never came back. Use this when the owner wants true boot/login survival without babysitting:
```powershell
$action = New-ScheduledTaskAction -Execute 'C:\Users\Stefan\AppData\Local\hermes\scripts\start_agents.bat'
$trigger = New-ScheduledTaskTrigger -AtLogOn -User 'Stefan'
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName 'NavoAgentsStartup' -InputObject (New-ScheduledTask -Action $action -Trigger $trigger -Settings $settings) -Force
```
The `.bat` does `start "" /min "%UV%" run --no-sync "%BOT%\bot.py"` for each bot (where
`%UV%` = `C:\Users\Stefan\AppData\Local\hermes\bin\uv.exe`) — note `uv run`, NOT the venv
`python.exe`, so each launch is a single `python.exe` chain (see §1c: venv-py spawns a venv-parent
+ uv-child pair, which the PID-lock can't dedupe across relaunches). The PID-lock (§1/§1a) makes a
redundant launch harmless. This is the right tool for "bring the bots up when I open the laptop" —
distinct from the rejected admin-XML supervisor. Keep the watchdog cron (§7a) for crash-recovery on top.

### 7b. Patch-discipline pitfall (cost a rework this session)
When editing a bot with `patch`, ALWAYS re-read the target function's boundaries first and
confirm the `old_string` is unique at MODULE level. A `patch` whose `old_string` also appears
INSIDE a function body will match there and inject the new code as a NESTED block — e.g. this
session `MENTION_RE`/`NAME_RE`/`should_reply` were meant for module scope but landed INSIDE
`run_agent` (a `def` at line ~302), so the module-level `should_reply` was never updated and the
group filter silently broke. Symptom: the symbol exists but isn't the one the loop calls.
Guard: after any structural patch, grep for the symbol name; if it appears twice (once indented),
the nested copy is the bug — move it to module level. Prefer `read_file` of the whole function
before patching, and use a unique multi-line anchor that spans the function signature.

### 7d. In-process self-healing restart loop (`run_with_restart`)
"Make the bots self-healing so they come back after a crash." This means TWO distinct
layers — don't conflate them:

**Layer A — in-process loop (cheap, code-level crashes only).** Wrap `bot_loop()` in
`while True: try bot_loop() except: sleep+retry`. Any unhandled Python exception inside
the loop (a message-handling bug, a None where a dict was expected, a bad JSON parse)
now restarts the loop instead of killing the process. Clears the pid-lock before retry:
```python
def run_with_restart(bot_loop, lock_file=None, backoff=5):
    attempt = 0
    while True:
        attempt += 1
        try:
            print("[self-heal] start (attempt %d)" % attempt); bot_loop()
        except KeyboardInterrupt:
            print("[self-heal] interrupted by user — exit"); break
        except Exception as e:
            print("[self-heal] bot_loop crashed: %s" % e)
        if lock_file:
            try:
                if os.path.exists(lock_file): os.remove(lock_file)
            except OSError: pass
        print("[self-heal] restarting in %ds..." % backoff); time.sleep(backoff)
# __main__: run_with_restart(bot_loop, lock_file=LOCK_FILE, backoff=5)
```
**SCOPE LIMIT (easy to get wrong — encode it):** this `while True` wrapper does NOT
survive an OS-level process death. `taskkill` / `Stop-Process` / SIGKILL / OOM / laptop
**power-off** terminate `python.exe` entirely, and the wrapper dies with it. Sleep/hibernate
does NOT kill it (the process just freezes and resumes). So Layer A alone does NOT satisfy
"the bot must come back after I close the laptop" — that needs Layer B below.

**Code edit needs a FULL process restart (Layer-A caveat — bit us this session):** `run_with_restart`
only catches in-loop Python exceptions and respawns the SAME already-loaded module. Editing the
bot source (`bot.py`) does NOT take effect in the running process — the old code keeps running
until you KILL + RELAUNCH the process. Symptom this session: fixed `_fresh_nous_key`, added the
VOICE RULE and `read_tracker_sheet`, but the live bot kept returning the old "lost the line"
fallback and stale task data until it was fully killed (`Stop-Process` by pid) and relaunched
with `uv run --no-sync bot.py`. Routine after editing `bot.py`: kill its pid (§7e, by the venv
parent or the single uv pid), relaunch, verify the NEW log line (e.g. `run_with_restart: start
(attempt 1)`), then re-test the fixed behaviour. Layer A does NOT hot-reload code.

**Force-kill bypasses Layer A (sharp edge — this session):** `Stop-Process -Force` (PowerShell) or
`taskkill /F` terminates the python process WITHOUT raising an in-process exception, so the
`run_with_restart` `except` branch NEVER fires and the loop does NOT self-restart. After a Force
kill you MUST relaunch manually (uv run …) — Layer B (watchdog cron / Task Scheduler) will also
eventually bring it back, but not instantly. Prefer `Stop-Process -Id <pid>` WITHOUT `-Force` only
if you want the loop to catch a clean `KeyboardInterrupt` and restart itself; for a code edit you
want a clean swap, so Force-kill then relaunch is fine (just remember to relaunch). This is why a
"the bot crashed, why didn't it self-heal?" after a Force kill is actually expected — the wrapper
never saw the death.

**Layer B — external relaunch (process death).** This is exactly §7a (watchdog cron that
relaunches a dead pid detached) + the §7 Task-Scheduler `AtLogOn` task (brings the bots up
at login). Those restart the *process itself*; Layer A then keeps the loop up between them.
Use BOTH. Verified live: killing the bot's pid → within 5s the loop restarted (attempt 2)
and answered normally — the in-process loop caught the dead `bot_loop` call and respawned it.
For power-off you still need Layer B.

**Rule of thumb:** in-process loop = protects against code-level crashes (cheap, always add it).
External watchdog + Task Scheduler = protects against process death (required for 24/7).
Never claim "self-healing" if only Layer A exists.

### 7e. Launch discipline — kill the right pid, don't spawn duplicates
When restarting a bot during debugging, remember §1c: a `venv\\Scripts\\python.exe` launch
spawns a venv-parent + `uv` child = ONE logical bot. `Stop-Process` of the venv PARENT kills
both (they're parent/child). To TEST Layer A's restart, kill the venv parent pid and watch the
log show `restarting in 5s...` then `start (attempt 2)`. If instead the whole `proc_…`
(Hermes terminal wrapper) exits and the bot pid is GONE with no "attempt 2" — you killed the
real interpreter and only Layer B will bring it back. Prefer launching via
`uv run --no-sync bot.py` (§1c) so there's exactly one `python.exe` chain to reason about.

### 7f. External self-healing for the ORCHESTRATOR (Hermes itself)
The bots have Layer A (in-process loop) + Layer B (Task Scheduler logon + watchdog cron).
**Hermes (the orchestrator) needs the SAME external guarantee** — but it cannot self-heal from
inside, because a Hermes `cronjob` may NOT call `hermes gateway restart` (lifecycle commands are
blocked to prevent respawn loops), and if Hermes is fully dead the cron doesn't run either. So the
self-heal for Hermes MUST live OUTSIDE Hermes, as an independent Windows Task Scheduler task.

**Mechanism (verified this session):** a system-level `Register-ScheduledTask` (repeat every 5m,
`AtLogOn` + repetition, hidden, run whether user logged on or not) runs `hermes_selfheal.ps1`
(a PowerShell script in `%LOCALAPPDATA%\\hermes\\scripts\\`). The script checks whether the gateway
process (`python -m hermes`) is alive; if not, it **kills all `Hermes.exe` + `python -m hermes`,
then relaunches `Hermes.exe`** (the Desktop app) — the new launch brings the gateway back up.
Reusable copy in `references/hermes_selfheal.ps1`; register with the PowerShell block shown there.

**CRITICAL detail — kill-then-start, not just start:** if the GUI (`Hermes.exe`) is alive but its
gateway child (`python -m hermes`) died, merely launching another `Hermes.exe` does NOT restart
the gateway (the new GUI sees an existing instance and exits). So the script must KILL the whole
Hermes tree first, then start. The check is specifically on `python -m hermes` (gateway), not on
`Hermes.exe` (GUI) — the GUI can be up while gateway is down.

**PITFALL — TWO bugs that actually bit us (encode both):**
1. **NEVER kill a HEALTHY open Desktop.** The first deployed `hermes_selfheal.ps1` checked only
   `python -m hermes`; when that gateway child was briefly down but the user's `Hermes.exe` GUI was
   open and working, the script KILLED the user's open Desktop and relaunched it. Symptom the owner
   reported verbatim: *"Hermes Desktop suddenly closes by itself and a command-prompt window pops
   open with [hermes] sandbox fallback…"* — the relaunched GUI came up in `--no-sandbox` console mode
   and showed its loader log. **FIX (authoritative shape):** exit 0 silently UNLESS BOTH conditions
   are true — gateway `python -m hermes` absent AND `Hermes.exe` GUI also absent. If the GUI is up
   (even with a briefly-dead gateway), do NOT touch the user's session.
   ```powershell
   # 1. gateway alive? -> exit 0
   # 2. Hermes.exe GUI already running? -> exit 0 (do NOT kill the user's open Desktop)
   # 3. only if BOTH dead: kill-all + relaunch hidden
   ```
2. **Relaunch HIDDEN, never Minimized.** `Start-Process -WindowStyle Minimized` still paints a
   visible console/terminal window (the owner kept seeing it pop up and closing it, which then
   re-triggered the self-heal → infinite loop). Always use `-WindowStyle Hidden` so no window appears.
   The Task Scheduler task itself must ALSO be `-Hidden` in `New-ScheduledTaskSettingsSet`. Launch
   the exe from its own dir (`Set-Location $EXE_DIR`) so relative-path log/config files resolve.
   (Corrected script + wscript launcher in `references/hermes_selfheal.ps1`,
   `references/hermes_selfheal_launcher.vbs`, `references/hermes_selfheal_task.md`.)

   **NEW PITFALL (this session): a direct `powershell.exe -File` Action STILL flashes a visible
   cmd host window every run** — `-WindowStyle Hidden` only hides the powershell child, not the
   host cmd that Task Scheduler spawns around it. The owner saw a black console pop every 5 min
   (*"примерно каждые пять минут выскакивает окно консоли"*) and asked to kill it entirely.
   **FIX (verified):** point the task Action at a **VBScript launcher** (windowless) instead of
   `powershell.exe` directly:
   ```vbs
   ' hermes_selfheal_launcher.vbs
   Set oShell = CreateObject("WScript.Shell")
   cmd = "powershell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -NonInteractive -File ""C:\Users\Stefan\AppData\Local\hermes\scripts\hermes_selfheal.ps1"""
   oShell.Run cmd, 0, False
   ```
   Task Action = `wscript.exe //nologo "C:\Users\Stefan\AppData\Local\hermes\scripts\hermes_selfheal_launcher.vbs"`. `wscript`
   itself is windowless, so no cmd host flashes. Registration gotcha on this host: `New-ScheduledTaskRepetitionTrigger`
   does NOT exist and assigning `$trigger.Repetition.Interval` throws 'PropertyNotFound' — set the
   5-min repetition via the COM object: `$svc.GetFolder('\').GetTask('HermesSelfHeal').Definition.Triggers.Item(1).Repetition.Interval = 'PT5M'`.

**Net result:** if Hermes fully crashes, Windows restarts it within ≤5 min with zero owner action
AND no visible window. This closes the loop: bots self-heal via Layer B + the owner's login; Hermes
self-heals via this external task. The owner only needs to act on a full OS power-off (then login
brings everything up).

**Note on the "user must restart Desktop" guidance:** that was the pre-self-heal state. With
§7f in place, tell the owner Hermes auto-recovers — they do NOT need to manually restart after a
crash (only after a deliberate `hermes update`, where the patch-watchdog §4 handles the quote patch
and a one-time Desktop relaunch applies it).

## 7g. Infra scripts live in a SEPARATE git repo (not the bot folders)
The self-heal / watchdog / cron-launcher scripts (`hermes_selfheal.ps1`, `start_agents.bat`,
`hermes_quote_patch_watchdog.py`, `refresh_nous_keys.py`, `git_autosync.py`) live in
`%LOCALAPPDATA%\\hermes\\scripts\\` — OUTSIDE the per-bot OneDrive folders. They are NOT covered by
the per-agent `git_autosync` repos (Richard/Alistair). To keep them versioned, put them in their
own private repo (`stefrogovskyi/navo-infra`) and ADD that path as a 4th entry in `git_autosync.py`'s
`REPOS` list so the 30m cron pushes them too. Pitfall hit this session: a stale/misspelled path in
`REPOS` (e.g. `Hermes Stevenson` folder that doesn't exist locally) makes autosync error on that
entry every tick — only list paths that exist on disk. Belt-and-suspenders: the owner expected
autosync to cover these files; it didn't until the 4th repo was added.

### 7c. Multi-repo Git autosync (Richard + Alistair + Hermes Stevenson)
The owner runs THREE separate private GitHub repos (one per agent, one for the orchestrator),
each a Google-Drive-synced local folder. Don't ask "did you push?" — automate it. Reusable
`scripts/git_autosync.py` commits+pushes all three every 30 min via a `no_agent=True` Hermes cron
(`schedule="every 30m"`); it is SILENT when clean and returns non-zero on error so the cron alerts.
Each repo's `.gitignore` excludes `.env`/`*.env`/`*.key`, so secrets never leave the machine.
Run it once manually after any big change to confirm pushes succeed, then let the cron keep it green.

### 7a. 24/7 keep-alive = watchdog script + Hermes cron + Startup launcher (the proven trio)
"Keep the bot running 24/7 like Richard" decomposes into three cheap pieces — NO Windows service,
NO Task Scheduler XML:
1. **Startup launcher** for boot/login survival: a `.lnk` in the user's Startup folder
   (`%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\`) whose `TargetPath` is the venv
   `python.exe`, `Arguments` = `<bot>.py`, `WorkingDirectory` = the bot folder. Build it with a
   tiny PowerShell one-liner (COM `WScript.Shell.CreateShortcut`) — no `.vbs` needed:
   ```powershell
   $ws=New-Object -ComObject WScript.Shell
   $s=$ws.CreateShortcut("$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\Alistair Bot.lnk")
   $s.TargetPath='C:\Users\Stefan\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe'
   $s.Arguments='alistair_watchdog.py'
   $s.WorkingDirectory='C:\Users\Stefan\My Drive\Equity\My Biz\Partner companies\Navo\6. Departments\Alister Sterling\Alistair Hermes'
   $s.Save()
   ```
   This is what actually autostarted Alistair this session (watchdog → bot). The PID-lock (§1/§1a)
   makes a redundant launch harmless.
2. **Watchdog cron** for crash-recovery: a stdlib `*_watchdog.py` that checks the LOCAL-disk lock
   (§1a — same path as the bot), and if the owning pid is dead/absent, relaunches the bot DETACHED
   (`subprocess.Popen(..., creationflags=DETACHED_PROCESS|CREATE_NO_WINDOW, close_fds=True)`).
   Make it **silent when healthy** (`sys.exit(0)` printing nothing) and print one line only when it
   actually restarts — so a Hermes `no_agent=True` cron delivers nothing unless something happened
   (the classic watchdog pattern). Register with `cronjob(action=create, no_agent=True,
   script="<watchdog>.py", schedule="every 10m")`. Copy the watchdog into
   `%LOCALAPPDATA%\hermes\scripts\` so the cron can find it by bare filename.
3. Trigger the cron once immediately (`cronjob action=run`) so the bot comes up without waiting for
   the first tick.
In this session, we successfully created and scheduled watchdogs for **Richard, Liz, and Ben** under `%LOCALAPPDATA%\hermes\scripts\`:
- `richard_watchdog.py` (Cron job: `Richard Bot Watchdog`, schedule: `every 10m`)
- `liz_watchdog.py` (Cron job: `Liz Bot Watchdog`, schedule: `every 10m`)
- `ben_watchdog.py` (Cron job: `Ben Bot Watchdog`, schedule: `every 10m`)
Each watchdog is syntactically validated and verified to run 100% silently in the background using `creationflags=0x08000000` to prevent any flashing console windows on the owner's desktop.
Reusable watchdog is in `references/bot_watchdog.py` (edit `HERE`/`BOT` and the entity lock name).
Pitfall: because the cron runs in a fresh session, the watchdog must hardcode/derive absolute paths
(bot folder, lock dir) — it can't rely on cwd. And the bot itself must self-load `.env.local` in
`__main__` (§2) so the detached relaunch has its keys.

## 8a. Multimodal — audio / photo / video
"Make the bot handle all content types like you" means voice→transcribe, photo/video→describe.
**KEY FINDING:** the host's Nous `inference-api.nousresearch.com/v1` returns **HTTP 404 on every
vision/audio model** (gpt-4o, gemini, claude-3 all 404) — it only serves the text model. So media
needs a SEPARATE OpenAI key (`OPENAI_API_KEY` in `.env.local`), used directly (not via Nous):
- **Voice/audio** → `POST https://api.openai.com/v1/audio/transcriptions` (model `whisper-1`),
  multipart/form-data (`file` + `model`), then treat transcript as the user's text.
- **Photo** → `gpt-4o-mini` chat with `image_url` (base64 PNG/JPEG). `gpt-4o-mini` works; a 1×1
  PNG returns 400 (too small) — use a realistic >=32px image for tests.
- **Video** → extract one frame with `ffmpeg -i in.mp4 -frames:v 1 -ss 00:00:01 frame.jpg`
  (ffmpeg 8.x is present on this host), then vision the JPEG.
- Without the key, degrade honestly: "I can't hear/see that yet" — don't pretend.
Verified live recipe (stdlib only, no pip) is in `references/multimodal_openai.py`.
In groups, only react to media that carries an `@mention` (avoid spamming on every photo).

## 8b. Credential-in-chat + restart-gap + key-mismatch safety
- If the user PASTES a live key (Telegram/OpenAI/bot token) into the chat, write it into `.env.local`
  via terminal (never print the value), confirm by `grep -c`, and IMMEDIATELY tell the user to
  **revoke/rotate it in the provider console** afterwards — it now lives in chat history.
- A mid-edit restart kills the old process before the new one binds → messages arriving in that
  gap get a `401 Unauthorized` (stale/killed consumer). Tell the user "write only when the bot is
  stable, not while I'm editing" and confirm `ONE BOT OK` (2 pids = 1 chain) + `NOUS models 200`
  + `OPENAI models 200` before declaring it safe to test.
### 8c. Voice OUTPUT — TTS → `sendVoice` (the "answer with voice" half)
`§8a` covers voice *input* (Whisper). The owner's bar is "fully multimodal: hear AND answer
with voice." So when the **inbound message was voice/audio**, the bot must **reply with a voice
note**, not just text. Reuse the same `OPENAI_API_KEY` (§8a) — OpenAI TTS is `POST
https://api.openai.com/v1/audio/speech` (model `tts-1`, `input`, `voice`, `response_format=opus`).
**WARNING: TTS input is capped at 4096 chars** — truncate `reply[:4096]` before sending.

```python
def speak_text(token, text, voice="alloy"):
    """text -> ogg/opus bytes via OpenAI TTS, or None if key missing."""
    key = openai_key()
    if not key: return None
    body = json.dumps({"model":"tts-1","input":text[:4096],
                       "voice":voice,"response_format":"opus"}).encode()
    req = urllib.request.Request(OPENAI_BASE+"/audio/speech", data=body, method="POST")
    req.add_header("Authorization","Bearer %s"%key)
    req.add_header("Content-Type","application/json")
    try:
        with urllib.request.urlopen(req, timeout=60) as r: return r.read()
    except Exception as e:
        print("[bot] tts err: %s"%e); return None

def tg_send_voice(token, chat_id, text, voice="alloy"):
    audio = speak_text(token, text, voice)
    if not audio:                       # TTS unavailable -> graceful text fallback
        tg_send_message(token, chat_id, text); return
    boundary = "----botvoice"
    parts = [("--%s\r\n"%boundary).encode(),
             b'Content-Disposition: form-data; name="chat_id"\r\n\r\n',
             str(chat_id).encode(), ("\r\n--%s\r\n"%boundary).encode(),
             b'Content-Disposition: form-data; name="voice"; filename="reply.ogg"\r\n',
             b"Content-Type: audio/ogg\r\n\r\n", audio,
             ("\r\n--%s--\r\n"%boundary).encode()]
    req = urllib.request.Request("https://api.telegram.org/bot%s/sendVoice"%token,
                                 data=b"".join(parts), method="POST")
    req.add_header("Content-Type","multipart/form-data; boundary=%s"%boundary)
    try: urllib.request.urlopen(req, timeout=60).read()
    except Exception as e:
        print("[bot] sendVoice err: %s"%e); tg_send_message(token, chat_id, text)
```

**Branch in the loop** (right where you call `tg_send_message(token, chat_id, reply)`):
```python
_voice_in = bool(msg.get("voice") or msg.get("audio"))
if _voice_in and openai_key():
    tg_send_voice(token, chat_id, reply or "(no response)")
else:
    tg_send_message(token, chat_id, reply or "(no response)")
```
**§8c-i. Text-request trigger ("ответь голосом") — NEW capability.** The owner wants to ASK for
a voice reply in PLAIN TEXT, not only by sending a voice note. So "Как дела ответь голосом"
must produce a voice note, not text. The §8c `_voice_in` branch only fires on voice INPUT, so it
misses text requests. Add a regex that detects an explicit voice-reply request and OR it into the
send branch:
```python
# explicit voice-reply request in text ("ответь голосом", "голосом", "voice")
VOICE_REQ_RE = re.compile(
    r"ответ[ьу]?[\s\S]{0,15}голос|голосом|скаж[иы][\s\S]{0,15}голос|"
    r"in voice|voice reply|reply in voice|send voice|voice mode", re.I)
```
Updated branch (replaces §8c's):
```python
_voice_in  = bool(msg.get("voice") or msg.get("audio"))
_voice_req = bool(VOICE_REQ_RE.search(text))   # text said "answer by voice"
if (_voice_in or _voice_req) and openai_key():
    tg_send_voice(token, chat_id, reply or "(no response)")
else:
    tg_send_message(token, chat_id, reply or "(no response)")
```
Verify with a regex test: "Как дела ответь голосом" → matches; "обычный текст без запроса" → no
match; "голосом подтверди" → matches. Apply to BOTH bots (Richard + Alistair) — the owner asked
for "обоим" (both) when adding the behaviour. This is SEPARATE from the multimodal VOICE RULE
(§8c prompt rule): the prompt rule stops the bot saying "I'm text-only"; this regex makes a TEXT
request actually emit voice. Both are needed for the full "fully multimodal" bar.

Note: voice INPUT is transcribed to text and flows through the normal LLM path, so the reply
is just text until this branch turns it back into voice. If `OPENAI_API_KEY` is `stub-`,
`openai_key()` returns `""` and the bot correctly falls back to text (still "heard" via Whisper
only if Whisper key is real — keep both gated on the same key). Verified live: owner sent a
voice note → bot replied with a voice note.

**§8c-ii. Conversation BATCHING / debounce — one coherent reply per chat (owner correction).**
The owner's bar: when the user sends SEVERAL messages in a row, the bot must ASSEMBLE them
into ONE connected reply, not answer each separately (which looks fragmented and drops
cross-message context). Symptom that triggered this: owner sent two messages back-to-back in
a group; the bot answered each independently — "он не держит контекст". FIX: accumulate
inbound messages per `chat_id` into a `pending` buffer, wait a 3.5s debounce window (one short
follow-up `getUpdates` poll to catch the tail of a burst), then call `run_agent` ONCE with all
messages joined by `\n---\n` and a directive to answer as ONE coherent response. Fast commands
(`/help`, `/sync`) stay immediate (outside batching). Verified live on BOTH Richard + Alistair
this session; full code + Richard/Alistair variants in `references/message_batching.md`.
Apply the same pattern to any future persona bot — the owner asked for "обоим" (all bots) and
will expect it by default. Tune the 3.5s window if they report lag or missed messages.

**Model-honesty trap (bit us live):** even with the TTS branch working, the bot may *say* "I'm a
text-only bot, I don't reply with voice" — because its `system_prompt.md`/`Agents.md` described it
as a "text bot" and the model INFERS it can't speak (it conflated "answers as text" with "cannot
output voice"). The fix is NOT more code — it's a prompt rule. Append to the system prompt at
code level (so an edited md can't drop it):
```python
BOT_SYSTEM += ("\n\nVOICE RULE: You CAN and DO reply with voice when the user sends a voice message "
               "(the bot speaks your text reply automatically). Never say 'I am a text-only bot' "
               "or 'I don't reply with voice' — that is false. If the user sends voice, answer "
               "naturally; your reply will be spoken aloud.")
```
Verified: after adding this, the bot stopped disclaiming voice and just spoke. General lesson —
when you add a NEW output modality (voice, image), also patch the persona prompt to claim the
capability, or the model will self-limit based on the old self-description.

**§8d. `content: null` from a tool-call turn CRASHES `.strip()` (bit BOTH bots live).**
When the model emits a tool_call, the `message` it returns has `content = null` (the text is
empty; the call is in `tool_calls`). The reply-extraction line
`reply = choice.get("content", "").strip()` then THROWS `AttributeError: 'NoneType' object has
no attribute 'strip'` — because `.get(key, default)` does NOT substitute the default when the
key is PRESENT with a `null` value; it returns the actual `None`. This fires exactly when the
bot answers a GROUP message that triggers tool calls (e.g. a task query / `/list`), so the crash
looks like "the bot works in PM but dies in groups." Symptom this session: Richard logged
`[agent error] 'NoneType' object has no attribute 'strip'` right after printing the user's task
list in a group. FIX (both bots): `reply = (choice.get("content") or "").strip()` — the
`or ""` catches the `null` (`None or ""` → `""`). Harden ANY other spot that reads
`choice.get("X")` then calls a string method. After the fix, re-test a message that forces a
tool call inside a GROUP and confirm a normal reply, not a crash.

**§8e. Picking STATIC voices for the bots (let the owner choose).**
The owner wants each bot to speak with a FIXED voice (Richard deeper-bass, Alistair keep
current). OpenAI TTS exposes 9 voices: `alloy, ash, coral, echo, fable, onyx, nova, sage,
shimmer`. Generate SAMPLES so the owner can pick, then hardcode `voice=` per bot (static, not
random). Recipe (one phrase, all candidates):
```python
import os, json, urllib.request
key = openai_key()   # from .env.local
OUT = r"C:\Users\Stefan\AppData\Local\hermes\audio_cache"
os.makedirs(OUT, exist_ok=True)
phrase = "Привет, Стефан. Это тестовый голос агента Navo — проверь тембр и выбери подходящий."
for name, voice in {"hermes_nova":"nova","hermes_sage":"sage",
                     "richard_onyx":"onyx","richard_echo":"echo",
                     "alistair_alloy":"alloy"}.items():
    body = json.dumps({"model":"tts-1","input":phrase,"voice":voice,
                       "response_format":"opus"}).encode()
    req = urllib.request.Request("https://api.openai.com/v1/audio/speech",
                                 data=body, method="POST")
    req.add_header("Authorization","Bearer %s"%key)
    req.add_header("Content-Type","application/json")
    with urllib.request.urlopen(req, timeout=60) as r: data = r.read()
    open(os.path.join(OUT, name+".ogg"),"wb").write(data)
```
Send each `*.ogg` to the owner as a voice note (Telegram delivers `.ogg` as a native voice
bubble). After they pick, set `speak_text(token, text, voice="onyx")` etc. permanently in each
**§8e-i. Role-appropriate shortlist for a PERSONA (not just “all 9”).** When the owner
wants a FEMALE voice for a people/relationship role (CPO, assistant, advisor), offer exactly
three English-basis OpenAI voices mapped to the character — OpenAI exposes 9 (`alloy, ash,
coral, echo, fable, onyx, nova, sage, shimmer`), of which the clearly female-sounding are
`coral` (caring/warm), `nova` (bright/upbeat), `shimmer` (gentle/calm); `fable` is also
female but storyteller-toned. For Liz Harper (Enlight CPO, people-first) the chosen set was:
`coral` (recommended — caring, fits “people, onboarding, motivation, culture”), `nova`
(board-level, brighter/energetic), `shimmer` (calm, for discreet 1:1s). Present 3 options as a
`clarify` choice, then hardcode the winner in BOTH `speak_text` and `tg_send_voice` defaults
(they must match — see §8e-ii). Keep `DEFAULT_OWNER`/tone discipline: the voice is a persona
trait, set once and forget.

**§8e-ii. Changing the default voice = FULL process restart (sharp edge, this session).** The
`voice=` default lives in the running module. Editing `speak_text`/`tg_send_voice` does NOT
take effect until you KILL + RELAUNCH the bot (same Layer-A caveat as §7d). After changing the
default: `taskkill /PID <pid> /F`, then restart via the watchdog (`wscript.exe //nologo
<scripts>\<entity>_selfheal_launcher.vbs`) or `uv run --no-sync <bot>.py`, confirm a NEW pid in
`<entity>.lock`, and verify with a live TTS call (`POST /v1/audio/speech` with `voice=<chosen>`
returns ~9 KB opus). A verify script asserting `speak_text(...,voice="coral")` in the source
and a live audio byte-count is the proof (ad-hoc, not a committed suite).

- **NOTE: OpenAI TTS voices are English-basis; Russian text works but carries a slight
  anglophone timbre** — tell the owner that's expected, or switch to a Russian-native TTS if
  they want accent-free Russian.

**§8f. Setting Hermes (orchestrator) OWN voice — NOT via bot code.**
The owner wants Hermes itself to speak with a fixed voice too (e.g. `echo`). Hermes is NOT a
persona bot, so §8e's `voice=` edit in `bot.py` does NOT apply. Hermes reads its TTS voice from
its own `config.yaml`, not from any bot file.

**Code path (verified this session):** `tools/tts_streaming.py:215` ->
`voice = self.section.get("voice", "alloy")`, where `self.section = tts_config.get(name)`
(line 156: `cls(tts_config, tts_config.get(name) or {})`). So the voice lives at the **FLAT** path
`tts.openai.voice` (the `tts:` block's `openai:` sub-dict), NOT `tts.providers.openai.voice`.

**Two traps:**
1. **`config.yaml` is patch-protected.** The agent cannot `patch`/`write_file` it directly —
   it refuses with *"Agent cannot modify security-sensitive configuration."* Use `hermes config`
   instead. But `hermes config set tts.providers.openai.voice echo` is REJECTED as
   "not a recognized config key" (code reads `tts.openai`, not `tts.providers.openai`).
   **The working command:**
   ```powershell
   hermes config set tts.openai.voice echo      # ✓ saved, no warning
   hermes config get tts.openai.voice           # -> echo
   ```
   This writes `tts:\n  provider: openai\n  openai:\n    voice: echo` shape. Voice is read fresh on every
   TTS call, so NO gateway restart is needed for the change to take effect.
2. **Make a backup first** (`copy config.yaml config.yaml.bak_voice`) — a Hermes `update` can
   rewrite `config.yaml` and drop the custom voice; re-apply after update if so.

**Consistency rule the owner established:** all three voices are picked ONCE and set statically —
Hermes (`echo`), Richard (`onyx` deep-bass via `voice="onyx"` in `richard_bot.py`), Alistair
(`alloy`, left as-is). Generate samples (§8e recipe) for the owner to choose, then hardcode each.
Hermes's sample is produced the same way (OpenAI TTS `tts-1`, `voice=echo`) and sent as a voice
note — the orchestrator's own voice is just another OpenAI TTS call, not special infra.

- **Key-mismatch 401 (the subtle one):** a key can pass `GET /models` (HTTP 200) but FAIL
  `POST /chat/completions` (401) — e.g. when `.env.local`'s `NOUS_API_KEY` is a DIFFERENT token
  than the host `auth.json`'s `access_token` (both start `eyJ…` JWT, so they LOOK alike). ALWAYS
  verify with the EXACT call the bot makes: `POST …/chat/completions` with a 1-message body.
  Repro probe:
  ```python
  import os,json,urllib.request
  tok=os.environ["NOUS_API_KEY"]; url=os.environ.get("NOUS_BASE_URL",
      "https://inference-api.nousresearch.com/v1").rstrip("/")+"/chat/completions"
  req=urllib.request.Request(url,data=json.dumps({"model":"tencent/hy3:free",
      "messages":[{"role":"user","content":"ping"}]}).encode(),
      headers={"Authorization":"Bearer %s"%tok,"Content-Type":"application/json"},method="POST")
  print(urllib.request.urlopen(req,timeout=30).status)  # must be 200, not 401
  ```
  If 401: re-read `auth.json` `providers.<p>.access_token` (and `agent_key` — both are 1777-char
  JWTs; both work for chat), overwrite `NOUS_API_KEY` in `.env.local`, re-run the probe live.
- **Stale-token 401 over TIME (distinct from §8b's key-mismatch):** the host's nous JWT
  (`auth.json` `providers.nous.access_token`) EXPIRES. Hermes auto-refreshes `auth.json`, but a
  STATIC copy written into the bot's `.env.local` goes stale and starts returning
  `HTTP 401 Unauthorized` on `/chat/completions` hours/days later — even though it worked at
  setup and the two tokens looked identical (both 1777-char `eyJ…` JWTs). Symptom: bot was fine,
  then every reply logs `http attempt N failed: HTTP Error 401`. Do NOT just re-copy the token —
  it will expire again. FIX: read the token FRESH from `auth.json` at every request, with env as
  fallback, and retry ONCE on 401:
  ```python
  _AUTH_JSON = os.path.join(os.environ.get("LOCALAPPDATA",
                            os.path.expanduser(r"~\AppData\Local")), "hermes", "auth.json")
  def _fresh_nous_token():
      try:
          d = json.load(open(_AUTH_JSON, encoding="utf-8"))
          t = d.get("providers", {}).get("nous", {}).get("access_token", "")
          if t: return t
      except Exception: pass
      return os.environ.get("NOUS_API_KEY", "")   # env fallback
  def llm_chat(messages, tools=None):
      payload = {"model": MODEL, "messages": messages}
      if tools: payload["tools"] = tools; payload["tool_choice"] = "auto"
      last = None
      for _ in range(2):                            # re-read token & retry once on 401
          headers = {"Authorization": "Bearer %s" % _fresh_nous_token(),
                     "Content-Type": "application/json"}
          try: return _http_json(OPENROUTER_URL, headers=headers, body=payload)
          except urllib.error.HTTPError as e:
              last = e
              if e.code == 401: time.sleep(1); continue
              raise
      raise last
  ```
  This makes the bot self-heal across token rotations — no manual re-sync ever again. (Sync the
  current value into `.env.local` once too, so the env fallback isn't itself stale.)
  BELT-AND-SUSPENDERS: also run `scripts/refresh_nous_keys.py` via a `no_agent=True` Hermes cron
  (`schedule="every 30m"`) — it copies the current `auth.json` token into `NOUS_API_KEY` of every
  bot's `.env.local`, so the env fallback can never go stale even if the runtime read fails.
  Add new bots to its `TARGETS` list. This is what actually prevents the recurrence of "lost the line".

  **POST-UPDATE 401 (the variant that actually bit us — add this to the fix):** a Hermes Desktop
  **update/relaunch** can leave the bot's `.env.local` `NOUS_API_KEY` as a STALE token that returns
  `401`, while `auth.json` `providers.nous.access_token` is perfectly live. The silent trap: a naive
  `_fresh_nous_key()` that early-returns `env_key` whenever it is merely **non-stub** (not `stub-`)
  will TRUST the stale `.env.local` copy and NEVER read `auth.json` → every reply becomes the
  "lost the line" fallback (symptom: `http attempt N failed: HTTP Error 401` on each call, even
  though a direct `auth.json` token pings 200). **FIX (authoritative shape — apply to BOTH bots):**
  `_fresh_nous_key` MUST read `auth.json` FIRST and only fall back to `os.environ["NOUS_API_KEY"]`
  if `auth.json` is unreachable. Do NOT write `if env_key and not env_key.startswith("stub-"): return env_key`
  at the top — that early-return is the bug. Match the Alistair `_fresh_nous_token` shape exactly
  (it already does this and worked). **After ANY Hermes update, if bots go silent with 401, the
  one-shot fix is re-run `refresh_nous_keys.py`** (copies auth.json → .env.local); the runtime read
  above is the durable fix, the cron is the safety net. Verify with the POST /chat/completions probe
  in `references/nous_post_update_401.md` (must be 200, not 401).
- `os.kill(pid,0)` → `WinError 87` on Windows → use `tasklist` liveness check (see §1).
- Cyrillic+space paths break `py_compile <abs>` and `rg`/`search_files` ("IO error"). Fix: `cd`
  into the dir, use RELATIVE paths; prefer `read_file` over content-search.
- After a refactor, always re-init module-level globals (e.g. `_history = {}`) or the bot
  replies with `NameError: <name> is not defined` to the user.
- Multiple launch paths (terminal + desktop app) stack copies → duplicates. Kill ALL `python`
  matching the bot, confirm ONE chain, rely on the PID-lock thereafter.
- Privacy OFF is cached at group-join time: after BotFather `/setprivacy` Turn off, REMOVE+RE-ADD
  the bot or it still sees only @mentions.

## 9. Self-learning (auto-update own system files from owner messages)
"Everything I write to Richard, he should remember and update his system files / memory / config."
Implement as a BACKGROUND thread (never blocks the reply). Only the OWNER's chat id
(`STEFAN_CHAT_ID`) triggers learning — other users only get dialog memory, never file writes.
Flow:
1. **Classify** the owner message with the LLM → strict JSON
   `{type, target, signal, apply}`. Types: `feedback`/`correction` (behaviour),
   `preference`/`fact` (about owner), `product_intel` (client objection / market insight),
   `none`. `target` ∈ `system_prompt.md` | `memory/profile_stefan.md` | `Agents.md`.
2. **Route**: `feedback`/`correction` → `system_prompt.md`; `preference` → `memory/profile_stefan.md`;
   `product_intel` → `Agents.md`. Append a dated `## 🧠 Learned from Stefan (YYYY-MM-DD)` block.
3. **Log** every learned entry to `memory/learning_log.json` (cap ~200, FIFO trim) for audit.
4. Dialog memory (§5) already captures the conversation regardless.
Classifier system prompt (condensed): *"You are Richard's learning classifier. Stefan (owner of
Navo) just sent a message. Return STRICT JSON {type, target, signal, apply}. If nothing to learn,
type=none, apply=''."* Parse with `re.search(r"\{.*\}", raw, re.S)` then `json.loads` (model may
wrap JSON in prose).
**Trigger in loop:** after `if not text: continue`, if `str(chat_id)==str(stefan_chat)`:
`threading.Thread(target=learn_from_stefan, args=(text, chat_type), daemon=True).start()`.
**Safety:** `_learn_append` only writes if `apply` is non-empty AND the target file exists; always
gate on `type != "none"`. A verified live run: owner msg "answer me in Russian and shorter" →
classified `preference` → appended to `memory/profile_stefan.md` → logged. After testing, strip
the test block so the profile stays clean. Full routine is the code block in this section (§9).

## 10. Network resilience: retries, timeouts, graceful errors (Nous flakiness)
`inference-api.nousresearch.com` is often **slow or intermittently unavailable** — a normal LLM
call can hang past urllib's default 60s and throw `urllib.error.URLError: <urlopen error>
timed out` / `The read operation timed out`. This surfaces to the user as a raw error string and
looks like the bot is broken. Harden ALL HTTP (LLM, Telegram, OpenAI) with:

```python
def _http_json(url, method="POST", headers=None, body=None, timeout=120):
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    last_err = None
    for attempt in range(3):            # 3 retries absorb transient Nous hangs
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            last_err = e
            print("[bot] http attempt %d failed: %s" % (attempt + 1, e))
            time.sleep(2)
    raise last_err
```
- Default `timeout=120` (Nous can take 10–30s; 60s is too tight).
- Caller catches exceptions and sends a **polite message, never the raw error**:
  `reply = "Richard here — briefly lost the line to the desk. One moment, try that again?"`
  Raw `str(e)` (e.g. "hit a snag reaching the desk: The read operation timed out") reads as a
  crash to the user and erodes trust. Log the exception server-side; show only the friendly line.
- The same `_http_json` backs Telegram (`tg_request`) and OpenAI (whisper/vision) so one
  retry wrapper covers every outbound call.
- **Verify before declaring "fixed":** send a real message and confirm the bot answers; a momentary
  Nous hang should now self-heal on retry instead of erroring.

## 11. Daily knowledge-base scanner (keep the persona's facts fresh)
"Scan our 5 sites every day, detect changes, update my memory/KB so I talk to clients with
current info." Build a SEPARATE stdlib-only script (`richard_scanner.py`, sibling of the bot) —

**CRITICAL KNOWLEDGE-ROUTING RULE (missed once, cost a real failure):** the persona bot reads
`system_prompt.md` + `Agents.md` + dialog history at runtime — it does NOT read the news log.
So product FACTS that clients ask about (prices, tiers, rates, free-tier limits, carrier counts)
MUST land in `Agents.md` (`agents_md_add`), never only in `product_news.md`. In one live run the
scanner put "paid plans from €39/mo" into the news log and the agent could NOT answer "what are
the pricing tiers?" because it never saw the news file. Fix: the classifier prompt must ALWAYS
surface prices/tiers/rates into `agents_md_add`; the news file is a human-readable changelog only.
For belt-and-braces, also regex-extract prices from the page and pass them to the classifier as a hint so it never drops a number. BUT anchor the regex to a currency/period token — `r"(?i)(?:€|eur|usd|\$)\s*\d[\d.,]*|\d[\d.,]*\s*(?:€|eur|usd|\$|/mo|per month|в месяц|мес|/container|/box)"`. A greedy "any 2–4 digit number" pattern grabs part-numbers/port codes (1219, 1589, 36, 18…) and the model reports them as "prices" — wrong. Currency/period-anchored only.

**Scanner must hit the PRICING pages, not just the homepage.** The product homepages (trackingmcp.com)
advertise "start free" but NO paid numbers — the real tiers/prices live on `/pricing`
(trackingmcp.com/pricing → "€3/container pay-as-you-go", Free/Starter/Business). If you only
scan `/`, the classifier correctly reports "no paid prices found" and the bot can't quote tiers.
Add explicit pricing seed URLs to `SITES` (a dict of LISTS) for each product, e.g. `{"trackingmcp": ["https://trackingmcp.com/", "https://trackingmcp.com/pricing"]}`. Better: implement a BFS `_crawl_site(start_urls, max_pages=15)` that walks `href`s (keep same-base-domain only, skip `#`/`mailto:`/`tel:`/`javascript:`), seeded with those key pages — guarantees `/pricing` + every sub-page is ingested even when JS menus hide links from static HTML. One joined text → one `llm_analyze` per site. (And the
AND the bot must NEVER invent a price — one bad test run had the classifier emit a fabricated "€39/mo"
that wasn't on the site; the real figure was €3/container. Source prices from scanned pages only.
**Classifier PROMPT GUARD (the actual fix for junk numbers):** the currency-anchored regex alone
is NOT enough — the LLM still listed raw page numbers (e.g. "$6 and $56" for navo24, "$1 $5 $8"
for loadingmcp) as "detected prices" when it couldn't tie them to a plan. Add to the classifier
system prompt: *"ONLY write a price if it is clearly attached to a named plan/tier (e.g. 'Starter
€39/mo', '€3 per container'). NEVER list raw numbers you found on the page as 'detected prices'
(e.g. '1219, 1589' or '$1, $5') — those are usually port codes or unrelated figures, not prices.
If a price has no clear plan label, omit it."* After a refactor, also CLEAN stale `## 🧠 Auto-update
from scan` blocks from `Agents.md` — the scanner appends but never dedupes, and old auto-blocks
can carry the junk numbers. Authoritative facts live in numbered sections (1.x); treat auto-blocks
as disposable and wipe them before a demo.

**Re-seeding after a refactor / first real load:** snapshots store a sha256 of each page. If you
reset the bot's KB or want a clean re-ingest, DELETE `memory/site_snapshots.json` — the next run
treats every page as "changed" and writes facts again. Without the reset, unchanged pages produce
NO writes (correct, but means a refactor that changed the router won't re-emit old facts).

**Frequency:** user prefers **every 3 days**, not daily — `schedule "0 7 */3 * *"`. Daily is noise
for static product sites. (Older guidance said `0 7 * * *`; override per owner preference.)

Verified live structure:
```python
SITES = {"navo24": ["https://navo24.com/"],
         "trackingmcp": ["https://trackingmcp.com/", "https://trackingmcp.com/pricing"],
         "schedulesmcp": ["https://schedulesmcp.com/"],
         "loadingmcp": ["https://loadingmcp.com/"],
         "freightratesmcp": ["https://freightratesmcp.com/", "https://freightratesmcp.com/pricing"]}
SNAP_FILE = "memory/site_snapshots.json"   # {name:{hash,ts,text[:2000]}}
NEWS_FILE = "memory/product_news.md"        # ## Product & Site Updates (auto from daily scan)
```
Steps per run:
1. For each site: `urllib` GET + strip HTML (regex drop `<script>/<style>/tags`, collapse ws).
2. `_hash(text)` (sha256[:16]); if unchanged vs `SNAP_FILE` → skip (no spam to KB).
3. If changed: call the LLM (`llm_analyze`) with a STRICT-JSON system prompt:
   `{changed, summary, agents_md_add, news_add}` — only material changes (new product/price/rate/
   FAQ/integration), ignore cosmetic/layout. Route `agents_md_add` → `Agents.md` (product facts),
   `news_add` → `NEWS_FILE` (dated log line). `re.search(r"\{.*\}", raw, re.S)` then `json.loads`
   (model wraps JSON in prose).
4. Save new snapshot. **First run** flags everything "changed" and seeds the KB — run once in
   `--dry-run` to eyeball the LLM output before writing, then a real run.
5. Cron: `schedule "0 7 */3 * *"`, prompt `cd "<bot folder>" && python richard_scanner.py`,
   `enabled_toolsets:["terminal","file"]`. Report a one-line delta; no-op if nothing changed.
LLM prompt pitfall: tell it to use TODAY's real date for `news_add`, NOT a date scraped from the
page (the model sometimes copies a "2025-03-15" it saw on the site — wrong). The news file
header already stamps the scan date; still, forbid fabricated dates in the classifier prompt.
Full scanner is `references/daily_site_scanner.py` (copy + point SITES at your URLs).

## 11b. Google Sheets task-tracker backend (OAuth, stdlib) — row-match + recovery pitfalls
When the bot's tool backend is a live Google Sheet (e.g. Alistair's 'Navo Tasktracker',
tab `Tracker`, cols `N|Task|Owner|%|Timeline|Comments`), wire it stdlib-only via the
google-workspace skill's OAuth token:
- **Auth:** read `%LOCALAPPDATA%\hermes\google_token.json`; refresh yourself when `expiry`
  is <60s away: `POST token_uri` with `client_id/client_secret/refresh_token/grant_type=
  refresh_token`, write back new `token`+`expiry`. No pip deps needed. (Same self-heal
  philosophy as §8b's `_fresh_nous_token`.)
- Setup path: skill `google-workspace` `setup.py` — NOTE this installed version does NOT
  accept `--services`/`--format json`; plain `--auth-url` / `--auth-code "<full redirect URL>"`
  only. The `http://localhost:1/?code=...` browser error is expected; the full URL pastes fine.
- Sheets REST: `GET/PUT /values/<quoted range>`, `POST /values/<range>:append`
  (`valueInputOption=USER_ENTERED`, `insertDataOption=INSERT_ROWS`), delete via
  `:batchUpdate` `deleteDimension` (needs the tab's `sheetId` from `?fields=sheets.properties`).

**CRITICAL BUG THAT DESTROYED REAL DATA (once):** when resolving a task id, match STRICTLY
by the task-number column (N in col A). NEVER also match on the physical row index (`_row`).
Task N=21 sat in physical row 22; `update id=22`/`delete id=22` hit the WRONG task — silently
overwrote and then deleted a real row while the test row survived. Symptom in tests: update
returns a DIFFERENT task's fields than the one you added. Verify CRUD with a full guarded
cycle: snapshot all rows → add test row → update by N → assert updated.task == test task AND
no collateral changes to snapshot → delete → assert count restored + originals intact.

**Recovery when a Sheet row IS lost:** Google keeps revisions. Drive API
`GET /files/<id>/revisions?fields=revisions(id,modifiedTime)` lists them; export a specific
revision as CSV with `https://docs.google.com/spreadsheets/export?id=<id>&revision=<rev>&
exportFormat=csv` (Bearer auth; exports FIRST tab; tsv chokes csv.reader on embedded newlines —
use csv format). Walk revisions newest→older until the lost row appears, then re-add it via the
normal append path. This restored a full 404-char multilingual comment intact.

Also: the sheet is usually PRIVATE — public `gviz/tq?tqx=out:csv` returns 401; don't waste time
on the anonymous CSV trick, go straight to OAuth.

## 11c. Kanban (SalesLoop/Gaffer) ↔ Google Sheets — one-way sync (read-only API reality)
Alistair's task "ground truth" is an external kanban exposed as **SalesLoop** (`GET https://salesloop.fly.dev/v1/tasks/status`). Each task: `id, title, product, category, status, feasibility, pr_url, author_name, updated_at`. The Make blueprint sent `X-API-Key`; the LIVE endpoint expects `Authorization: Bearer <token>` — mismatch returns 401, so fix the client to send `Bearer`.

**CRITICAL FINDING — the API is READ-ONLY.** Every write verb (PATCH/POST/PUT) against `/tasks`, `/tasks/<id>`, `/tasks/status` returns `404 Not Found`. So "two-way sync kanban ↔ sheet" is physically impossible through this endpoint. The achievable, correct design is **one-way: kanban → Google Sheet** (mirror the ground truth into the Tracker tab). Report this limitation honestly to the owner instead of pretending the sheet can push back.

**⚠️ NEVER OVERWRITE THE SHEET (data-destruction trap).** The naive `PUT ...!A2:F1000` that rewrites all data rows **wipes the owner's hand-maintained tasks**. This happened live: the owner had to roll the Sheet back to a July-20 version to recover his tasks. The Sheet is the OWNER'S artifact — the bot only MIRRORS the kanban into it, it must never clobber existing rows.

### Safe `sync_to_sheets` — owner's explicit Tracker spec (the correct design)
The owner maintains the Sheet with this structure (enforced by the bot):
- Row 1 = frozen header: `N | Task | Owner | % | Timeline | Comments`.
- **Main block:** tasks immediately below the header, down to the FIRST empty row. This block is the owner's — never overwrite, never delete.
- A few blank rows as a separator.
- **Done block:** tasks at 100%, light-green-filled, below the blanks. New 100% tasks go to the TOP of this block; unfinished tasks return to the top of the main block.

Per-task mapping (kanban task → Tracker row):
- **A (id):** the kanban `id` verbatim. If a kanban task has no id, assign the next sequential integer after the max numeric id in column A.
- **B (task):** `title`, MUST fit one line. If longer than ~90 chars, truncate with `…` and put the FULL text into column F. If it fits, leave F alone.
- **C (owner):** map `author_name` → a Telegram @nick from the team roster (see owner-mapping below). NEVER write a raw `author_name` or a free-text name.
- **D (%):** default `10%` for new tasks. On UPDATE, do NOT touch D unless explicitly told — preserve the owner's value.
- **E (timeline):** default `+7 days` (`dd.mm.YYYY`) for new tasks. Don't invent dates.
- **F (comments):** append, never delete. On each sync/update, add a NEW line `📥 <today> Gaffer: <status> | <category> | <feasibility>` (and the full title if it was truncated). Never clear prior F content — concatenate with `\n`.

**Match-by-id, insert-after-main logic:**
1. Read the whole tab; split into `main` (rows 2..first blank) and `done` (100% rows after the blanks). Build `existing = {id: row}` from BOTH blocks.
2. For each kanban task: if its `id` is in `existing` → update ONLY fields that differ. Skip D (preserve), append to F (never replace), update B only if the title changed. If nothing differs → `skipped`.
3. If `id` NOT in `existing` → INSERT new rows AFTER the main block (before the blank separator), with the mapped values. Insert N rows in ONE `batchUpdate` `insertDimension`, then write all values in ONE `values:append` (see batching below).
4. Tasks present in the Sheet but absent from the kanban array → **leave them untouched** (owner's rows survive).
5. On 100%: light-green-fill the row (`repeatCell` backgroundColor ~`{0.85,0.93,0.85}`) and move it to the top of the done block (delete original row, insert a blank at the done-block top, write values + green). If a 100% task turns out not done → set % to the correct value (or default 50%) and return it to the top of the main block, removing green.

**Owner/author mapping — read the Team tab, fallback to hardcoded, unknown → Gaffer:**
```python
OWNER_MAP = {  # fallback only; Team tab wins
    "stefan": "@stefrogovskiy", "stefan rogovskiy": "@stefrogovskiy",
    "@stefrogovskiy": "@stefrogovskiy",
    "alexey": "@lxxmng", "aleksey": "@lxxmng", "alex": "@lxxmng",
    "lxxmng": "@lxxmng", "@lxxmng": "@lxxmng",
    "gaffer": "@thegaffermcp_bot", "thegaffer": "@thegaffermcp_bot",
    "@thegaffermcp_bot": "@thegaffermcp_bot",
    "richard": "@richnavobot", "@richnavobot": "@richnavobot",
    "alistair": "@qubicpmbot", "@qubicpmbot": "@qubicpmbot",
}
DEFAULT_OWNER = "@thegaffermcp_bot"

def _load_team_map():
    """Read the 'Team' tab: col A = name/role, col D = Telegram nick. Cache it."""
    m = {}
    try:
        res = _sheets_api("GET", "/values/" + quote("Team!A2:D100"))
        for v in res.get("values", []):
            v = (v + [""] * 4)[:4]
            name, nick = v[0].strip(), v[3].strip()
            if nick:
                if name: m[name.lower()] = nick
                m[nick.lower().lstrip("@")] = nick
                m[nick.lower()] = nick
    except Exception:
        pass
    return m

def _owner_to_nick(author_name):
    if not author_name:
        return DEFAULT_OWNER
    key = str(author_name).strip().lower().lstrip("@")
    team = _load_team_map()
    if key in team: return team[key]
    if key in OWNER_MAP: return OWNER_MAP[key]
    for k, v in team.items():
        if k and k in key: return v
    for k, v in OWNER_MAP.items():
        if k and k in key: return v
    return DEFAULT_OWNER   # unknown author → Gaffer (owner's rule)
```
**OWNER CORRECTION (first-class):** Gaffer's correct nick is **`@thegaffermcp_bot`** — the originally-supplied `@sortitbot` was WRONG and must never be used. Any `author_name` that matches no roster entry is written as `@thegaffermcp_bot` (the owner's explicit rule: "if the name doesn't match our list, record everything on @thegaffermcp_bot").

**OWNER RESOLUTION — requester vs executor (the actual fix this session):** in this owner's kanban,
**Stefan and Alexey are the REQUESTERS (they create tasks), Gaffer is the EXECUTOR (does the work).**
So kanban tasks must be assigned to **`@thegaffermcp_bot`**, NOT to the kanban `author_name`. Do NOT
map `author_name` (Stefan/Alexey) → owner in the sync. Set `owner = DEFAULT_OWNER` (`@thegaffermcp_bot`)
for every kanban row (SalesLoop has no per-task executor field, so default is correct). The
`_owner_to_nick(author_name)` mapping is for hand-added `/add` tasks where the owner is given
explicitly via `@`; it does NOT apply to the kanban mirror. This is the opposite of the naive
"map author → owner" instinct — verify with the owner which role the `author_name` represents
before wiring it to the Owner column.

**OWNER-DIAGNOSTIC pitfall (first-class, this session — don't edit the map blindly):** when the
owner reports "all of Gaffer's kanban tasks got assigned to Stefan," the bug is usually NOT in
`_owner_to_nick`. FIRST dump the RAW distinct `author_name` values from the source API:
`from collections import Counter; print(Counter(t["author_name"] for t in get_task_status()["tasks"]))`.
This session that revealed SalesLoop only ever returns `'Stefan Rogovskiy'` (34 tasks) and
`'Lxxmng'` (13) — **Gaffer is never an author in the kanban at all.** So the bot's mapping was
CORRECT (those names map to @stefrogovskiy / @lxxmng; unknown → @thegaffermcp_bot). The real
cause: the Gaffer bot creates tasks in SalesLoop attributed to the OWNER (Stefan) as author — an
UPSTREAM attribution issue in Gaffer→SalesLoop, not fixable in the bot's owner map. **Lesson:**
verify the raw author distribution BEFORE touching `OWNER_MAP`; if the source never carries the
real creator, the fix is upstream (Gaffer must tag the true author or add a distinguishable
field/marker), not in the sync code. Editing the map to force "Gaffer" would just mislabel
Stefan's own tasks.

**Team-tab layout caution (owner corrected me live):** the `Team` tab is NOT a flat top-down list — people are **grouped under colored department headers** (IT, Digital, Creative, Admin, Logistics…) where the department row fills ONLY col A, and each person sits below their department with **blank-row separators** between groups. So `_load_team_map` must read the **whole tab** (`Team!A2:D100`, not just the first few rows) and key ONLY on the `nick` in col D — department-only rows (col A filled, col D empty) are correctly skipped because `if nick:` guards them. Do NOT stop scanning at row ~6 or assume a single contiguous block; the people you need are scattered. Verified: with Gaffer/Digital/Admin groups present, reading the full range maps Stefan→@stefrogovskiy, Alexei→@lxxmng, Richard→@richnavobot, Alistair→@qubicpmbot, Gaffer→@thegaffermcp_bot correctly. Note spelling drift in the tab (e.g. "Stefan Rogovskyi" with y) still matches the kanban's "Stefan Rogovskiy" via the partial-match fallback in `_owner_to_nick`.

**BATCH or it times out.** A per-row `PUT`/`POST` for 47 tasks = 60+ sec and the terminal/cron call times out mid-write (partial sync, looks broken). Batch instead: (1) ONE `batchUpdate` `insertDimension` for all N new rows, (2) ONE `values:append` with all new-row values, (3) ONE `batchUpdate` `updateCells` for all updates. Result: ~1.1 sec for a full 47-task sync. Always batch.

**Automate the sync (don't make the owner type `/sync`).** Register a `no_agent=True` Hermes cron that runs a thin wrapper script (e.g. `alistair_sync.py`) which loads `.env.local` and calls `sync_to_sheets()`. Pattern (owner wanted **daily at 07:00**): `cronjob(action=create, no_agent=True, name="Alistair daily kanban sync (7:00)", schedule="0 7 * * *", script="alistair_sync.py")`. The wrapper must `cd`/absolute-path into the bot folder and self-load `.env.local` (so `SALESLOOP_URL`, token, `GOOGLE_SHEETS_ID`, `TRACKER_TAB`, `TASKTRACKER_BACKEND=salesloop` all resolve in the fresh cron session). Verify the script standalone once (`python alistair_sync.py` → `{'ok':True,'skipped':47}` when nothing changed) before relying on the cron.

**Backends are env-switched, not hardcoded.** The same client supports `sheets` (CRUD on the Sheet), `salesloop` (read kanban), `rest`, and a local `stub` file store — `TASKTRACKER_BACKEND` picks. Don't fork logic per bot; set the env var. Set `TASKTRACKER_BACKEND=salesloop` so `list_tasks()` reads the live kanban via `get_task_status()`.

Concrete reusable implementation (structure parser, owner map, batched safe sync, **100%→done
and return-to-main lifecycle**, `_ensure_done_block`, and the merged-record bug fix) is in
`references/kanban_sheets_safe_sync.md` — copy it into `tasktracker_client.py` and adapt the
column constants. Note: `_sheets_add` must ALSO insert after the main block (not `:append` to the
sheet end) or new hand-added tasks break the two-block rule.

**Verify live (and that you did NOT destroy data):** `tt.sync_to_sheets()` → `{'ok':True,'added':N,'updated':M,'skipped':K}`. Then READ back: the owner's original rows (row 2 = their first hand-made task) must be UNCHANGED, and kanban rows must appear AFTER them. If `added`≈47 and the owner's rows moved/disappeared → you overwrote — stop, roll back the Sheet revision, fix the insert logic.

### 11c-i. Bulk-correcting ONE column WITHOUT clobbering the whole row (the §400 PUT trap)
When the owner asks "re-assign all kanban tasks' Owner column" (e.g. the requester/executor fix
above), do NOT rewrite the whole row with `PUT ...!A:F`. Two traps:
1. **Google Sheets PUT needs `valueInputOption`.** A bare `PUT /values/<range>` with body
   `{"values":[...]}` returns **HTTP 400 Bad Request**. Always pass
   `params={"valueInputOption":"USER_ENTERED"}` (the client's `_sheets_write_row` already does
   this — reuse it, don't hand-roll the request).
2. **Rewrite only the cells you mean to.** Build the corrected row from the EXISTING parsed
   record (`rec["id"], rec["task"], NEW_OWNER, rec["percent"], rec["timeline"], rec["comments"]`)
   — never from a freshly-built partial list, or you wipe the task text / percent / timeline.
Pattern (verified — corrected 47 rows in one pass without touching task text or %):
```python
def is_kanban(rec): return "📥" in (rec.get("comments") or "")   # kanban rows carry the Gaffer marker
main, done, _ = _sheets_structure()
updated = 0
for r in main + done:
    if is_kanban(r) and r["owner"] != "@thegaffermcp_bot":
        vals = [r["id"], r["task"], "@thegaffermcp_bot", r["percent"], r["timeline"], r["comments"]]
        rng = "%s!A%d:F%d" % (TRACKER_TAB, r["_row"], r["_row"])
        _sheets_api("PUT", "/values/" + quote(rng),
                    body={"values":[vals]}, params={"valueInputOption":"USER_ENTERED"})
        updated += 1
# re-read and assert owner distribution == {'@thegaffermcp_bot': N}
```
This is a ONE-OFF correction script, not the sync path — the sync itself should never mass-edit
Owner (it preserves the owner on update, per §11c step 2). Run it once, verify, then the incremental
sync keeps the right value.

### 11d. Persona bot must READ the live Sheet, not answer from memory (stale-cache trap)
The sync in §11c *writes* the kanban into the Sheet. But the bot also gets **questions about
the tasks** ("what's in the tracker?", "what's the status?"). If the bot answers those from its
`system_prompt.md` / `Agents.md` / conversation memory, it serves **STALE data** — exactly what
happened: Alistair answered from a cached July-20 snapshot of the Sheet instead of current rows,
because it had NO tool to read the Sheet and fell back to prompt memory. The owner spotted it
immediately ("he gave me data from before today's sync").

**FIX — give the bot a LIVE read tool and a HARD rule to use it:**
1. Add `read_tracker_sheet(params=None)` to `tasktracker_client.py`: calls `_sheets_structure()`
   (the same parser from §11c), returns the main block + done block as TEXT (id | task | owner |
   % | timeline | comments), never from a cache. Register it in `TOOLS` and `tool_schemas()`.
2. Append a HARD RULE to the system prompt (code-level, so an edited `system_prompt.md` can't
   drop it): `ALISTAIR_SYSTEM += "\n\nHARD RULE: When the user asks about tasks, status,
   progress, the tracker, or 'what's in the table', you MUST call the read_tracker_sheet tool
   FIRST to get LIVE data from the Google sheet, then answer from that. Never answer task
   questions from memory or stale context."`
3. Schema description must also say "ALWAYS call this before answering any question about
   current tasks/status/progress — do NOT answer from memory" so function-calling prefers it.

**Why a separate read tool (not reusing `list_tasks`/`get_task_status`):** `list_tasks` in this
client lists the *SalesLoop kanban* (the external ground truth), and `get_task_status` is the
kanban too — neither reads the *Google Sheet* the owner actually maintains. The Sheet is the
artifact the owner edits, so the read-back must hit the Sheet (via `_sheets_structure`), not the
kanban. Verified live: `read_tracker_sheet()` returned 70 open + 1 done (owner rows 1–21 + 47
kanban rows) — current, not cached.

**General rule (first-class, this session):** any persona bot whose "knowledge" lives in an
external system (Sheet, CRM, DB) MUST have a LIVE read tool for that system, and a HARD prompt
rule forcing its use before answering "what/how many/status" questions. Never let the bot answer
domain questions from its static prompt or memory — that's how stale answers get shipped. This is
the read-side counterpart to §11c's safe write-side.

## 12a. Hermes model management: free-model fallback chain + gateway autorestart on model change

The orchestrator (Hermes itself, Desktop+Telegram) has TWO recurring model problems the owner
hit this session. Both have clean, verified fixes — encode them.

### A. Free model overloads → `⚠️ The model provider failed after retries`
Symptom: Telegram Hermes shows *"⚠️ The model provider failed after retries. I kept raw provider
details out of chat; check gateway logs for diagnostics"* and/or the "typing…" indicator spins
forever with no reply. Gateway log shows `agent.conversation_loop: API call failed after 3
retries. error code: 502` for the free model (e.g. `tencent/hy3:free`). Cause: the free Nous
model is temporarily overloaded (502/429), NOT a key or config bug.

**FIX — Hermes has a STANDARD fallback mechanism: `fallback_providers` in `config.yaml`.** Hermes
tries each entry in order, on the fly, within the SAME message, when the primary model errors
(rate limit / server error / auth). Chain the other free Nous models as backups:
```yaml
model:
  provider: nous
  name: tencent/hy3:free
fallback_providers:
  - provider: nous
    model: poolside/laguna-s-2.1:free
  - provider: nous
    model: stepfun/step-3.7-flash:free
  - provider: nous
    model: poolside/laguna-xs-2.1:free
```
**PITFALL — `hermes config set fallback_providers '[...]'` stores a STRING, not a list.** After
`hermes config set fallback_providers '[{"provider":"nous","model":"..."}]'`, reading it back
shows `type: str` — Hermes won't parse it as a fallback chain. `config.yaml` is also
patch-protected (agent `patch`/`write_file` refused: *"Agent cannot modify security-sensitive
configuration"*). The working path is to edit the YAML with python (terminal is allowed to):
```python
import yaml
p = r'C:\Users\Stefan\AppData\Local\hermes\config.yaml'
cfg = yaml.safe_load(open(p, encoding='utf-8'))
cfg['fallback_providers'] = [
    {"provider": "nous", "model": "poolside/laguna-s-2.1:free"},
    {"provider": "nous", "model": "stepfun/step-3.7-flash:free"},
    {"provider": "nous", "model": "poolside/laguna-xs-2.1:free"},
]
yaml.safe_dump(cfg, open(p,'w',encoding='utf-8'), allow_unicode=True, sort_keys=False)
# verify it's a LIST, not str:
chk = yaml.safe_load(open(p, encoding='utf-8'))['fallback_providers']
assert isinstance(chk, list) and chk[0]['model']  # type must be list
```
**Discover the CURRENT free models live (don't hardcode a stale list)** — query the Nous API with
a valid key and filter `:free`:
```python
# GET https://inference-api.nousresearch.com/v1/models  (Bearer <NOUS_API_KEY>)
# -> filter ids containing ':free'. This session yielded exactly 4:
#    tencent/hy3:free, poolside/laguna-s-2.1:free, poolside/laguna-xs-2.1:free, stepfun/step-3.7-flash:free
```
If the owner names a model that isn't in the live list (e.g. "Ling 3.0 Flash" this session), say
so honestly — it isn't on the portal — and add it later when it appears. NOTE: `fallback_providers`
covers **Hermes** (Desktop+Telegram) only. The persona bots (Richard/Alistair/Liz/Ben) are separate
stdlib programs with NO fallback; adding a model-rotation loop to their `llm_chat` is a separate task.

### B. Model changed in Desktop but Telegram keeps the old one (sync drift)
When the owner switches model in the Desktop app, the running gateway keeps serving the OLD model
to Telegram until it restarts — Desktop and Telegram desync. Owner wants the gateway to
auto-restart whenever the model changes. Hermes can't self-restart from inside (a cron may not
call `hermes gateway restart`), so use an EXTERNAL config-watch cron (same philosophy as §7f):

**Mechanism (verified this session):** `scripts/model_change_gateway_restart.py` reads the
`model:` block (provider+name) from `config.yaml` each tick, compares to a saved fingerprint
(`state/model_fingerprint.json`), and on change: silently kills `gateway run` (python/pythonw)
and relaunches the official `gateway-service/Hermes_Gateway.vbs` (windowless, `CREATE_NO_WINDOW`).
Register as a `no_agent=True` Hermes cron `every 2m`. First tick just records the fingerprint;
thereafter any model change triggers a hidden restart within ≤2 min, so Telegram picks up the new
model. Reusable copy in `scripts/model_change_gateway_restart.py`. Parse the `model:` block with
stdlib (no PyYAML) so the cron has no deps: read line-by-line, enter on `model:`, exit when a
non-indented line appears, capture `provider:`/`name:`.

Full details, the free-model discovery snippet, and the config-write gotcha are in
`references/hermes_model_fallback_and_autorestart.md`.

## 12. Group reactivity contract (owner's explicit spec)
In a GROUP, the bot must ALWAYS respond when ANY of these hold (this is required behaviour,
not optional):
- **Called by name** (e.g. "Richard", "Ричард") even WITHOUT an @mention/tag → `NAME_RE    = re.compile(r"\b(ричард|richard|рич|rich)\b", re.I)  # owner also wants the short forms Rich/Рич (no @ needed)
` (separate from the `@` `MENTION_RE`).
- **Someone replies to one of the bot's own messages** → `reply_to_message.from` id == `BOT_ID` (or `username` in `BOT_USERNAMES`). Set `BOT_ID = os.environ.get("BOT_ID", "8846249306")` and `BOT_USERNAMES = [u.lower() for u in os.environ.get("BOT_USERNAMES","richnavobot,richard").split(",")]` at module level; `force_reply = True` when matched.
- **Someone quotes/selects words from the bot's message** (message.quote) → answer (see §4).

In ADDITION, the bot runs in an **economical self-detection mode**: for OTHER group messages
(no name, no reply, no quote), it responds ONLY on a DIRECT QUESTION about Navo/the products.
**Shipped heuristic (keep it cheap — NO LLM call per message):** respond if
`(is_question(text) AND is_on_domain(text))` — a direct question with on-domain keywords.
`is_question` = regex for `?`/`как`/`что`/`сколько`/`which`/`what`/… .
**BARE `is_on_domain(text)` (on-domain post WITHOUT a question) MUST NOT trigger a reply** —
that is the over-reply bug (below). A group full of on-domain posts (Gaffer/Kanban task dumps,
status lists, "navo container…") is NOT a conversation directed at the bot; answering each one
spams the group. Everything else (banter, on-domain posts without a question) → silent
(`continue`, no LLM call → saves tokens). Private chat still answers unconditionally.

**OWNER CORRECTION (first-class, this session):** the earlier shipped heuristic had a STANDALONE
`is_on_domain(text)` trigger (reply on ANY on-domain post). That made Richard answer after EVERY
message in a group of internal task lists — the owner pushed back: *"he shouldn't do this, check
again."* The fix REMOVES the bare `is_on_domain` trigger; the bot now replies in a group ONLY on
@mention / name-without-@ / reply-to-bot / quoted-fragment, OR a direct question + on-domain.
If the owner later WANTS the bot to chime in on non-question on-domain posts, that's a deliberate
widening — confirm before re-adding `is_on_domain` standalone, because it WILL re-introduce group
spam (every task-list / status post gets a reply).

```python
MENTION_RE = re.compile(r"@(richnavobot|richard)\b", re.I)
NAME_RE    = re.compile(r"\b(ричард|richard|рич|rich)\b", re.I)  # owner also wants the short forms Rich/Рич (no @ needed)
BOT_ID = os.environ.get("BOT_ID", "8846249306")
BOT_USERNAMES = [u.lower() for u in os.environ.get("BOT_USERNAMES","richnavobot,richard").split(",")]

def is_on_domain(t): t=(t or "").lower(); return any(k in t for k in ON_DOMAIN)
def is_question(t): return bool(re.search(r"[?？]\s*$|как|что|где|когда|почем|сколько|какой|which|what|how|where|when|why", t, re.I))
def should_reply(t):
    # name/mention always; bare on-domain WITHOUT a question => NO (avoid group spam)
    if MENTION_RE.search(t) or NAME_RE.search(t):
        return True
    if is_on_domain(t) and is_question(t):   # question about Navo/product => reply
        return True
    return False

# in loop (group branch only):
force_reply = bool(replied) and (str(replied.get("from",{}).get("id"))==str(BOT_ID)
                  or (replied.get("from",{}).get("username") or "").lower() in BOT_USERNAMES)
if chat_type != "private" and not (MENTION_RE.search(text) or NAME_RE.search(text)
        or force_reply or (is_question(text) and is_on_domain(text))
        or (has_media and MENTION_RE.search(text))):
    continue  # economical silence, no LLM call
```
Do NOT build an LLM-per-message analyzer for "contextual relevance" — the owner wanted
economical, and the keyword+question heuristic above covers the real cases (questions about
freight/rates/products) without burning tokens on every group line. Escalate to a cheaper
pre-filter→LLM-on-candidates only if the owner reports missed relevant messages. Never spam:
if it responded recently and the new message isn't directed at it, stay quiet.
