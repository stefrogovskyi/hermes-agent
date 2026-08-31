# Entity clone — isolation, launch & 24/7 auto-start (playbook)

Companion to SKILL.md steps 6–8. Concrete recipe used for **Liz Harper**
(CPO, Enlight Group) cloned from Alistair Sterling (Navo PM), 2026-07-24.
Proven live: Liz answered via LLM, isolation verified (own store, no SalesLoop/
shared Sheet), kept alive by `LizHarperSelfHeal` Task Scheduler task.

## A. Isolation (the clone must not know its siblings)

Goal: clone has its OWN token, storage, keys; never touches the source's
kanban/Sheet; never maps a name to a sibling handle.

1. **`.env.local` for the clone** — pull global infra keys from the source entity's
   `.env.local` (masked terminal read, never print values), but DROP shared keys:
   - KEEP: `NOUS_API_KEY`, `NOUS_BASE_URL`, `LIZ_MODEL`(=source `ALISTAIR_MODEL`),
     `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `STEFAN_CHAT_ID`.
   - SET: `TELEGRAM_BOT_TOKEN` = the clone's own token (from user),
     `LIZ_ADMIN_IDS` (=source admin id), `TASKTRACKER_BACKEND=stub`,
     `LIZ_STUB_MESSAGE` = "<Name> is waking up…".
   - DROP (do NOT copy): `GOOGLE_SHEETS_ID`, `TRACKER_TAB`, `SALESLOOP_API_KEY`,
     `SALESLOOP_TOKEN`, `SALESLOOP_URL`, `TASKTRACKER_REST_BASE`.
2. **Client `tasktracker_client.py`** (verbatim copy, then 2 surgical edits):
   - Neutralize sibling kanban: in `list_tasks()`, change
     `if b == "salesloop": return get_task_status(params)` →
     `if b == "salesloop": b = "stub"`.
   - Rewrite `OWNER_MAP` to the clone's roster (Enlight directors → their
     `@handles`), set `DEFAULT_OWNER = "@stefrogovskiy"`. Remove `richnavobot`,
     `qubicpmbot`, `thegaffermcp_bot`, `lxxmng` entries and the "Гаффер" comment.
   - Update tool-schema descriptions: drop "SalesLoop API (Gaffer kanban)" /
     "Gaffer kanban (SalesLoop)" → "local Enlight people tracker".
3. **Persona docs**: in `Agents.md` §2 (storage), §6 (integrations), `memory.md`
   (working files), `tools.md`, `agent.config.json` (`integrations.task_tracker`),
   and registry `note` — state explicitly: own local `tasktracker_store.json`,
   `backend=stub`, NO SalesLoop, NO shared Sheet, "Лиз не знакома с Ричардом и
   Алистером". Keep the provenance line "shell copied 1:1 from Alistair" — it's
   accurate and must stay.
4. **Verify isolation**: `grep -niE "richnavobot|qubicpmbot|thegaffermcp|gaffer"`
   on the clone folder — only the intentional provenance note may remain. Confirm
   `.env.local` has no `SALESLOOP_*`/`GOOGLE_SHEETS_ID`. Confirm a test `add_task`
   writes to the clone's own `tasktracker_store.json`, not a shared Sheet.

## B. Adapt /help to the JD

Rewrite the bot's `HELP_TEXT` block (in `<new>_bot.py`) for the role. Keep the
source's *structure* (4 slash commands + "Кроме заготовленных команд я могу:" +
bullets), replace content. For a CPO the bullets became:
- отвечать на рабочие HR-вопросы (люди, команды, онбординг, мотивация, культура)
- вести кадровую таблицу задач
- уточнять статусы и прогресс по людям и командам
- помнить директоров и связи между бизнесами Enlight Group
- говорить голосом / видеть изображения / поддержать диалог
Also change `/list` label to "Показать текущие кадровые задачи".

## C. Launch + live verification

1. Clear any stale pid-lock: `del "%LOCALAPPDATA%\hermes\entities\<new>.lock"`.
2. Kill any prior clone process if re-launching.
3. Launch background: `python <new>_bot.py >> <new>_run.log 2>&1` (use
   `terminal(background=true)`, NOT `&` in a foreground cmd).
4. Confirm in `<new>_run.log`: `[<New>] bot started, polling Telegram... stub=False`.
5. Live self-test (forces the runtime's `run_agent` path with real keys):
   `set LIZ_SELFTEST=Привет, <имя>, кто директор Avalanche?` then
   `python <new>_bot.py`. Expect a branded, role-correct, non-"setup mode" answer.

## D. 24/7 auto-start (Task Scheduler)

Pattern proven for Liz (use `<New>` = e.g. `Liz`):
1. **Launcher** `C:\Users\Stefan\AppData\Local\hermes\scripts\start_<new>.bat`:
   `set PYTHON=C:\Users\Stefan\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe`
   + `start "" /min /d "<clone_folder>" "%PYTHON%" <new>_bot.py`. (Liz is
   stdlib-only → `python`, not `uv run`; Richard/Alistair use `uv run`.)
2. **Self-heal launcher** `…\scripts\<new>_selfheal_launcher.vbs`: hidden
   `wscript` that runs `"<PYTHON>" "<clone_folder>\<new>_watchdog.py"`.
3. **Self-heal task** (the keeper — works without elevation):
   `schtasks /create /tn "<New>SelfHeal" /tr "wscript.exe //nologo <path>\<new>_selfheal_launcher.vbs" /sc minute /mo 5 /ru "DESKTOP-MST5PT7\Stefan" /f`
   The watchdog checks the pid-lock; if the bot is dead it relaunches. Every 5 min
   = self-healing 24/7.
4. **Logon task** (optional, often needs elevation):
   `schtasks /create /tn "<New>Startup" /tr "<path>\start_<new>.bat" /sc onlogon /rl LIMITED /f`
   → frequently returns "ERROR: Access is denied." on this host. If it fails, the
   5-min self-heal (step 3) alone is sufficient; don't block on the logon task.
5. **Verify**: `schtasks /query /tn "<New>SelfHeal"` returns the task; a live
   `tasklist /FI "PID eq <pid_from_lock>"` shows `python.exe` alive; the bot answers
   a live message.

## E. Verification pitfalls (false negatives that waste a turn)
- `import` of the bot module for unit checks fails on `import tasktracker_client as tt`
  unless the clone folder is on `sys.path` — `os.chdir(<clone>/)` or
  `sys.path.insert(0, <clone>/)` first.
- `wmic` may be absent from the tool's `python` PATH → wrap in `cmd /c wmic ...`
  or use `tasklist /FI "PID eq N"`.
- A live LLM self-test proves the answer is real; "stub=False" in the log is the
  prerequisite. Don't assert "stub reply" when the host has a real `NOUS_API_KEY`.
- `grep "Alistair"` hits the legitimate provenance docstring — that's correct, not
  a self-identity leak. Only flag genuine self-identity where the clone calls
  ITSELF by the source's name ("Alistair Sterling, AI project manager at Navo" /
  "Alistair (Navo PM) is in setup" / "Alistair here").
