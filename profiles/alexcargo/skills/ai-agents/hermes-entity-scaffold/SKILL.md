---
name: hermes-entity-scaffold
description: >-
  Scaffold or clone a Hermes Stevenson entity (virtual employee / AI agent) on
  Stefan's Windows host. Use when the user says "create entity X, copy
  capabilities/skills/connectors from Y" but write a fresh description/JD/role/
  persona; or "clone this bot with a different character". Covers copying the
  programmatic shell verbatim, rebranding the runtime identity tokens while
  keeping 100% of the logic identical, authoring the new persona files,
  registering in entities/registry.json + entities/<id>.md, and verifying on
  this Windows machine. This is the orchestrator's (Hermes Stevenson) entity
  lifecycle, distinct from generic agent-building skills.
---

# Hermes Entity Scaffold (clone / create)

Hermes Stevenson is Stefan's Chief Orchestrator. Entities (agents, VEs, connectors)
are registered in `…\Enlight Group\Stefan Rogovskyi\Hermes Stevenson\entities\registry.json`
plus an `entities/<id>.md` card (blank template: `entities/TEMPLATE.md`).

A recurring task: **"create entity X, copy all programmatic capabilities/skills/
connectors from entity Y, but give it a different description, job description,
role, and character."** The correct approach is to clone the *runtime shell* 1:1
and rebrand only identity tokens — NOT to hand-rewrite the bot. Then author the
persona from scratch.

## When to use
- "Создай сущность <имя>, скопируй возможности/скиллы/коннекторы из <другой>."
- "Clone <bot> but with a different personality / JD / role."
- Any new member of the Enlight Group / Navo entity roster.

## Source material (this host)
A working reference agent lives at
`…\Partner companies\Navo\6. Departments\Alister Sterling\Alistair Hermes\`:
`alistair_bot.py` (Telegram runtime, stdlib, long-polling, pid-lock, 3-tier memory),
`tasktracker_client.py` (tool client: add/update/delete/list/sync/status),
`agent.config.json`, `soul.md`, `system_prompt.md`, `Agents.md`, `memory.md`,
`tools.md`, `README.md`, `.env.local`, `.gitignore`, `run_alistair.bat`,
`Alistair_Bot.vbs`, `alistair_watchdog.py`.

### Converting an Entity / Bot into a 100% Full-Scale Hermes Profile (--profile <name>)
To elevate a Virtual Employee or Telegram bot from a lightweight bot script (`<name>_bot.py`) into a full-scale, autonomous Hermes Agent core (with its own isolated `config.yaml`, `memories/`, `skills/`, `cron/`, SQLite DB, and full tool capability):

1. **Create Profile Directory**: `C:\Users\Stefan\AppData\Local\hermes\profiles\<name>\` with `memories/`, `skills/`, `cron/`, `platforms/pairing/`.
2. **Migrate Memory & Persona**: Read `soul.md`, `system_prompt.md`, and historical `memory.md` / `json` from the entity's Google Drive folder (`registry.json` path). Combine into `profiles/<name>/memories/MEMORY.md` and write owner info into `memories/USER.md`.
3. **Master API Keys Inheritance**: Copy ALL master API keys (`GEMINI_API_KEY`, `GONKA24_API_KEY`, `OPENROUTER_API_KEY`, `NOUS_API_KEY`, `OPENAI_API_KEY`) from `C:\Users\Stefan\AppData\Local\hermes\.env` directly into `profiles/<name>/.env` alongside `TELEGRAM_BOT_TOKEN=<token>`, preventing `RuntimeError: No LLM provider configured`.
4. **Pre-seed Owner Auto-Pairing (Zero-Friction Startup)**: Write `profiles/<name>/platforms/pairing/telegram-approved.json` pre-seeded with Stefan Rogovskiy's Telegram ID (`330656040`, `"user_name": "Stefan Rogovskiy"`) and team members (Robert/Alexey `1022586369`, Eugene Karavan `363779334`, Sort It Bot `8806090295`) so the new profile recognizes authorized users IMMEDIATELY without asking for pairing codes (`DY5H7CRF`) or `hermes pairing approve`.
5. **Configure Group Mention Triggers & Fallback Chain**: Write `profiles/<name>/config.yaml` setting `google/gemini-3.6-flash` (`google`) as primary, direct `openai` (`gpt-4o-mini`, `gpt-4o`), `gonka24` (`minimax-m2.7`, `kimi-k2.6`), and the complete 14-item fallback chain (`gonka24` + `openrouter` + `nous`). Set `telegram.group_response_mode: mention` and `group_trigger_keywords` with all name aliases across languages and declensions (e.g. `Каллум`, `Каллума`, `Callum`, `Ричард`, `Ричарда`, `Алистер`, `Лиз`, `Бен`) so the bot responds in group chats ONLY when @mentioned, directly replied/quoted to, or called by name. Set persona voice (`ash`, `echo`, `fable`, `nova`, `onyx`) and append the autonomous execution prompt to `system_prompt_append`.
6. **Neutralize Old Bot Script & Watchdogs**:
   - Rename old script `<name>_bot.py` -> `<name>_bot.py.disabled` and `<name>_watchdog.py` -> `<name>_watchdog.py.disabled` on Google Drive so background processes cannot restart them.
   - Remove `<name>` from `bot_configs` in `C:\Users\Stefan\AppData\Local\hermes\scripts\bot_watchdog.py`.
   - Force kill old running bot processes (`<name>_bot.py` PID) and clean old lock files in `entities/`.
7. **Launch Real Hermes Gateway**:
   - Run `"C:\Users\Stefan\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes.exe" --profile <name> gateway run` silently using `subprocess.Popen` or VBS launcher (`CREATE_NO_WINDOW` `0x08000000`) with environment variable `HERMES_PROFILE=<name>`.
   - Create `run_<name>_hermes_verified.vbs` in `AppData\Local\hermes\scripts\`.
8. **Verify Live Process**: Verify via `psutil` that `hermes.exe` with `--profile <name>` is active and polling Telegram.
9. **User Confirmation Rule**: ALWAYS ask for explicit user confirmation before executing destructive, file-deleting, or final mutating actions. Never act automatically on pure questions.
10. **Impersonation Security Guardrail**: ALL agents and bots MUST write ONLY via their official Bot API tokens on their own behalf. NEVER post or send messages as Stefan / user account under any circumstances.
11. **1-Click Inception Prompt Template 2.0**:
```text
Гермес, выполни 100% авто-конверсию бота [ИМЯ_БОТА: callum / richard / alistair / liz / ben] в Полноценный Автономный Профиль Гермеса на ядре Hermes Agent под ключ за один запуск:
1. 📂 ИЗОЛИРОВАННАЯ СТРУКТУРА ПРОФИЛЯ: Создай папки C:\Users\Stefan\AppData\Local\hermes\profiles\[ИМЯ_БОТА]\ с memories/, skills/, cron/, platforms/pairing/.
2. 🧠 БЕСШОВНАЯ МИГРАЦИЯ ПАМЯТИ И «ДУШИ»: Прочитай soul.md, system_prompt.md, memory.md и *.json с Google Диска. Запиши в profiles/[ИМЯ_БОТА]/memories/MEMORY.md и USER.md.
3. 🔑 КЛЮЧИ API И АВТО-ПЕРИНГ СТЕФАНА (БЕЗ КОДОВ): Извлеки TELEGRAM_BOT_TOKEN из .env.local старого бота. Скопируй ВСЕ мастер-ключи API (GEMINI_API_KEY, GONKA24_API_KEY, OPENROUTER_API_KEY, NOUS_API_KEY, OPENAI_API_KEY) в profiles/[ИМЯ_БОТА]/.env. Запиши Стефана (330656040) и команду в profiles/[ИМЯ_БОТА]/platforms/pairing/telegram-approved.json. Создай profiles/[ИМЯ_БОТА]/config.yaml с базовой моделью google/gemini-3.6-flash, провайдерами google/openai/gonka24 и полной мастер-цепочкой из 14 фолбеков, голосом и group_response_mode: mention + group_trigger_keywords.
4. 🛑 БЛОКИРОВКА СТАРОГО ДВИЖКА И WATCHDOG: Заверши processes [ИМЯ_БОТА]_bot.py и [ИМЯ_БОТА]_watchdog.py по PID. Переименуй в .disabled на Google Диске. Исключи бота из bot_watchdog.py и удали lock-файлы.
5. 🚀 ЗАПУСК НАСТОЯЩЕГО ИСПОЛНЯЕМОГО ФАЙЛА ГЕРМЕСА: Запусти "hermes.exe" --profile [ИМЯ_БОТА] gateway run в фоновом режиме CREATE_NO_WINDOW с HERMES_PROFILE=[ИМЯ_БОТА] и создай run_[ИМЯ_БОТА]_hermes_verified.vbs.
6. 🔍 ВЕРИФИКАЦИЯ: Проверь через psutil, что запущен hermes.exe с флагом --profile [ИМЯ_БОТА] и опрашивает Телеграм.
```

## Procedure (verified on this host)
1. **Read the source fully** (bot, client, config, persona files, registry entry).
2. **Copy the client VERBATIM**: `cp tasktracker_client.py <new>/`. Never hand-edit it.
3. **Rebrand the runtime** (copy `alistair_bot.py` → `<new>_bot.py`, then replace
   identity tokens ONLY — program logic stays identical):
   - `@qubicpmbot` → `@<newhandle>` (mention regex + `BOT_USERNAME`)
   - name regex `(алистер|alistair|allister|alister)` → the new name's forms,
     e.g. `(лиз|элизабет|елизавета|liz|harper|elizabeth|лиза|lisa)`
   - `ALISTAIR_MODEL`→`<NEW>_MODEL`, `ALISTAIR_SYSTEM`→`<NEW>_SYSTEM`,
     `ALISTAIR_STUB_MESSAGE`→`<NEW>_STUB_MESSAGE`, `ALISTAIR_SELFTEST`→`<NEW>_SELFTEST`
   - `"----alistairvoice"`/`"----alistairboundary"` → `lizvoice`/`lizboundary`
   - `"alistair.lock"`→`liz.lock`, `"alistair_memory.json"`→`liz_memory.json`
   - `[Alistair]` log tag → `[<New>]`; fallback system-prompt string; error phrases
   - Keep the provenance note "shell copied 1:1 from Alistair" — it's accurate.
   Do the replacements via `execute_code` with a literal Windows path; MSYS paths
   passed to `python <script>` get mangled (see Host pitfalls).
4. **Author the NEW persona files** (the different part): `system_prompt.md`,
   `soul.md`, `Agents.md`, `memory.md`, `tools.md`, `README.md`, `agent.config.json`,
   `.env.local` (stub values), `.gitignore`, `run_<new>.bat`, `<New>_Bot.vbs`,
   `<new>_watchdog.py`. Mirror structure; rewrite content for the new role/JD.
5. **Register**: add entry to `registry.json` `entities[]` + create `entities/<id>.md`
   card. Bump `meta.count`/`active`, set `last_updated`. Set `managed_by`:
   `hermes_stevenson`, `owner`: `stefan`. Copy `capabilities`/`auth_env` verbatim
   from the source entity; note in `note` that the shell was cloned.
   **Registry field schema for isolation + routing** (added 2026-07-26, the Liz/Ben
   multi-agent frame work) — put these on BOTH the registry entry AND `entities/<id>.md`:
   - `project_scope`: array of projects/brands the agent may act within. Route a
     task to the agent ONLY if it falls inside `project_scope`. e.g. Liz →
     `["Enlight Group"]`; Richard → `["Navo"]`; Ben → `["Enlight Group","Avalanche Agency"]`.
   - `company` / `group` (for directors): e.g. Ben `company:"Avalanche Agency"`,
     `group:"Enlight Group"` — makes clear he is director of the SUBSIDIARY, not
     "director of Enlight Group" as a whole. Avoid the ambiguous phrasing.
   - `coordinates`: array of sub-agent ids this agent may direct (coordinator role).
     Liz → `["ben_jett"]`. Empty/none for leaf agents.
   - `excludes`: array of agents/projects the agent must NOT know or touch (e.g. Liz
     `excludes:["Navo","richard","alistair"]`). Mirror this in the agent's own
     `system_prompt.md` (generic clause — see step 6 depersonalization: never NAME
     the excluded siblings).
   - `coordinated_by` / `managed_by`: who routes to / oversees this agent.
   - In `registry.json` `meta`, add a `routing_policy` block: the orchestrator's own
     rule set ("call Liz ONLY for HR/people inside Enlight Group; Richard/Alistair are
     outside her frame; if task is outside every agent's scope → escalate to Stefan").
   **Orchestrator duty:** when delegating, YOU hold the ramka too — a personnel
   request in Enlight → Liz; Avalanche ops → Ben; Navo sales → Richard. This explicit
   per-agent frame is what stops "context soup" as the roster grows.
   NOTE: the orchestrator has NO programmatic API to call an agent's bot directly yet;
   delegation today is conceptual (routing in chat + editing the agent's files). True
   programmatic handoff = a future queue/bridge — don't claim it works.
6. **ISOLATION (default, unless user says "shared")**: a cloned entity must NOT be
   acquainted with its siblings. When the user says "изолируй от <других агентов>"
   or the new entity lives in a different brand/roster, strip every shared
   linkage so the clone has its OWN token, storage, and keys:
   - **Storage**: set `TASKTRACKER_BACKEND=stub` → its own local `tasktracker_store.json`.
     Do NOT inherit `GOOGLE_SHEETS_ID`, `TRACKER_TAB`, or the source's shared Sheet.
     Neutralize the `salesloop` backend branch in the verbatim client:
     `if b == "salesloop": b = "stub"` so it can never read the sibling's kanban.
   - **Keys**: do NOT copy `SALESLOOP_API_KEY`/`SALESLOOP_TOKEN`/`TASKTRACKER_REST_BASE`
     from the source `.env.local`. Keep only Stefan's *global infra* keys
     (`NOUS_API_KEY`, `OPENAI_API_KEY`) — those are host resources, not "acquaintances".
   - **OWNER_MAP**: the verbatim client carries a legacy alias map that maps names to
     sibling handles (`richnavobot`, `qubicpmbot`, `thegaffermcp_bot`, `lxxmng`).
     For an isolated clone, REWRITE `OWNER_MAP` to the new entity's own roster
     (e.g. Enlight directors) and set `DEFAULT_OWNER` to Stefan (@stefrogovskiy).
     This was previously "leave it alone" — that guidance is ONLY safe when the
     clone is meant to share the source's kanban. If isolated, strip it.
   - Reflect isolation in the persona docs (`Agents.md`, `memory.md`, `tools.md`,
     `agent.config.json`, registry `note`) — say "own local store",
     "no shared Sheet / external kanban".
   - **DEPERSONALIZE the isolation clause — do NOT enumerate sibling names**
     (LESSON, Liz/Ben 2026-07-25). The old pattern wrote a `system_prompt.md`
     isolation block that LISTED the forbidden entities ("ты НЕ знакома с Navo,
     SeaRates, Ричардом (@richnavobot), Алистером (@qubicpmbot), Гаффером
     (@thegaffermcp_bot), @lxxmng…"). Result: when a user asked about those, the
     bot **quoted the whole list back** in its refusal — the exact leak isolation
     was meant to prevent. Correct clause is GENERIC: "ты — отдельная сущность
     <Brand>; других проектов/ботов/трекеров в твоей картине мира НЕ существует;
     если вопрос вне твоей зоны — коротко скажи 'это вне моей зоны' БЕЗ упоминания
     каких-либо названий, ников или ID чужих задач." Never name Navo / SeaRates /
     Gaffer / QubicPM / sibling @handles anywhere in prompt or docs.
7. **Adapt command list + /help to the JD** (user correction): the bot's `HELP_TEXT`
   and any slash-command list must be rewritten for the new role, not copied from
   the source. For a CPO: tasks become "кадровые задачи", bullets become
   "отвечать на HR-вопросы (люди, команды, онбординг, мотивация, культура)",
   "помнить директоров и связи между бизнесами". Mirror the source's HELP_TEXT
   *structure*; replace the content with role-specific lines.
8. **Launch + auto-start (the job is "live", not "written")**: when the user says
   "запускай / имплементируй и запускай", don't stop at file creation:
   - Write real keys into `.env.local` (bot token from the user; pull global
     `NOUS_API_KEY`/`OPENAI_API_KEY` from the source entity's `.env.local` via the
     masked terminal read — never print values).
   - Launch the bot (background process) and confirm `stub=False` in the log +
     a live LLM self-test returns a branded, non-stub answer.
   - **24/7 — the proven trio (NO admin rights needed)**:
     1. **Self-heal (crash recovery):** Task Scheduler task `<New>SelfHeal` every 5 min
        running `wscript.exe //nologo <scripts>\<new>_selfheal_launcher.vbs` → launches
        `<new>_watchdog.py` (checks the LOCAL-disk pid-lock; relaunches the bot detached
        if dead). Register: `schtasks /create /tn <New>SelfHeal /tr "wscript.exe //nologo
        <scripts>\<new>_selfheal_launcher.vbs" /sc minute /mo 5 /ru <HOST>\<user>`.
        Verify: `schtasks /query /tn <New>SelfHeal` → `Status: Ready`, `Last Result: 0`.
     2. **Logon autostart (instant-on, NO admin):** a `/sc onlogon` Task Scheduler task
        FAILS with "Access is denied" on this host (medium-integrity, not elevated). The
        working no-elevation fallback is a **VBS launcher in the user Startup folder**:
        `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\<New>Startup.vbs`
        (windowless, `oShell.Run "...", 0, False`) that runs `start_<new>.bat`, which does
        `start "" /min /d "<bot folder>" "<python>" <new>_bot.py`. The pid-lock makes a
        duplicate launch harmless. Don't fight the onlogon denial — use the Startup folder.
     3. Watchdog + self-heal together guarantee 24/7 even after power-off (login brings
        it up; the 5-min tick relaunches if it dies).
   - **PROVE 24/7 before done (kill-and-restart test):** after launch, `taskkill /PID
     <pid> /F`, sleep 2, confirm `alive_count=0`, run the watchdog launcher, sleep 8,
     confirm a NEW pid in `<new>.lock` and the log shows "bot started, polling...".
     Only then is self-heal verified. `LizHarperStartup`/`LizHarperSelfHeal` is the template
     (see references/isolation_playbook.md).
9. **Verify before declaring done** (steps in references/entity_clone_playbook.md +
   references/isolation_playbook.md).

## Host pitfalls (Windows / Hermes desktop host)
- `python3` is NOT on PATH — use `python` (uv cpython 3.11).
- Bare MSYS paths (`/c/Users/...`) passed to `python "<script>"` get mangled into
  `C:\c\...`. Either `cd` into the folder and use relative names, or call from
  `execute_code` with a literal `r"C:/Users/..."` path. (General MSYS/`python3`
  gotchas also covered by `windows-skill-runner`.)
- `read_file` on `.env.local` is BLOCKED by a secret guard. To see its keys, use
  terminal: `sed -E 's/=.*/=<value>/' "$F/.env.local"` — never print values.
- `search_files` is unreliable on these OneDrive paths; use `terminal` `ls`/`grep`.
- The verbatim client carries a legacy owner-alias map (incl. `alistair`→
  `@qubicpmbot`). It is harmless ONLY when the clone shares the source's kanban.
  When the entity is ISOLATED (step 6), REWRITE `OWNER_MAP` to the new roster and
  set `DEFAULT_OWNER` to Stefan — a cloned CPO must never map a name to a sibling
  agent's Telegram handle. (See step 6.)

## Keep the roster in sync
Known entities (also in `hermes-stevenson` skill + registry.json):
hermes_stevenson (orchestrator), richard (`richnavobot`), alistair (`qubicpmbot`),
liz_harper (`@lizharperbot`, CPO Enlight Group — shell cloned from Alistair),
ben_jett (`@benjettbot`, Director Avalanche Agency / Enlight Group — shell cloned
from Alistair; 2026-07-24),
callum_vance (`@callumvancebot`, Full-Stack Engineer Navo sites/apps — 2026-07-30;
accepts dev commands from Stefan `330656040`, Tech Lead Алексей `1022586369`, or Orchestrator).

## Verification pitfalls (real, hit on the Ben Jett clone — 2026-07-24)
The ad-hoc verify script must avoid three false negatives or it reports failures
that aren't real:
1. **`importlib` + relative import.** Importing `<new>_bot.py` via
   `spec_from_file_location` FAILS on `import tasktracker_client as tt`
   (`ModuleNotFoundError`) unless `tasktracker_client.py`'s folder is on `sys.path`.
   The launcher's `cd /d` hides this at runtime. In verify, either `os.chdir(<new>/)`
   or `sys.path.insert(0, <new>/)` before loading the module.
2. **Force stub mode.** The live host already has a real `NOUS_API_KEY`, so
   `run_agent(text)` takes the LLM path and a "stub reply Ben-branded" check FAILS.
   In verify, override `os.environ["NOUS_API_KEY"] = "stub-ABC"` to force the
   stub branch before asserting the branded fallback message.
3. **Provenance ≠ self-identity leak.** `grep "Alistair"` will ALWAYS hit the
   legitimate provenance docstring (`"скопирована 1:1 из бота Алистера Стерлинга
   (Navo PM)"`) — that is correct and must stay. Only flag genuine self-identity
   leaks where Ben calls HIMSELF "Alistair Sterling, AI project manager at Navo" /
   "Alistair (Navo PM) is in setup" / "Alistair here". Assert `found == []` on
   THAT narrowed pattern, not on the bare name "Alistair".

## References
- `references/entity_clone_playbook.md` — full step list + an ad-hoc verification
  recipe (py_compile, stub CLI, SELFTEST runtime, grep for leftover tokens).
- `references/isolation_playbook.md` — isolation (own storage/keys/OWNER_MAP),
  /help→JD adaptation, launch + live verification, and Task Scheduler 24/7
  self-heal recipe (the Liz Harper / Enlight pattern).
- `references/retroactive_scrub.md` — make an ALREADY-DEPLOYED bot forget sibling
  projects (Navo/SeaRates/Gaffer/etc.): where leaked names hide, the scrub pass,
  and the depersonalized-isolation fix that stops refusal-time name quoting.
