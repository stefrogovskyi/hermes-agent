---
name: ai-agent-persona-build
description: >
  Build a knowledge-rich, persona-driven AI agent (sales / support / consultant / role)
  as a folder of companion files — soul.md, Agents.md, tools.md, system_prompt.md,
  agent.config.json — plus channel and automation wiring. Use when the user wants a
  durable agent with a defined personality, deep product/domain knowledge, exact
  tool-call contracts, and Telegram / WhatsApp / email / voice integrations.
---

# ai-agent-persona-build

Scaffold a persona/role-driven AI agent as a set of companion files, not a single
prompt. The agent should *sound like a specific person* and *call real APIs*.
Use when the user says "create an AI agent for [company/role]" with personality,
knowledge, and integrations in scope.

## When to use
- "Create an AI agent / sales-manager / support rep for [company]" with a name and persona.
- Building a B2B agent that must demonstrate domain expertise and call live tools.
- Producing a reusable agent the user will extend later (add products, competitors, channels).

## Output: the file set (build all of these)
1. **`soul.md`** — personality core: identity, character core, voice/tone samples
   (good vs bad), values, emotional intelligence, boundaries. The "who", not the tasks.
2. **`Agents.md`** — operational: roles (A–F style), full product knowledge,
   competitive intelligence (honest, with comparison tables), scenario playbooks,
   KPIs, hard guardrails. The "muscles".
3. **`tools.md`** — exact call contracts: every MCP/REST/webhook tool with JSON
   request/response examples, auth headers, error handling, and "honest empty"
   states (e.g. show "no carrier data", never fake movement). The "hands".
4. **`system_prompt.md`** — the compiled single-focus system prompt
   (soul + agents + tools condensed) fed to the LLM core.
5. **`agent.config.json`** — machine-readable: channels
   (telegram/whatsapp/email/voice/desktop), integrations (API keys as env refs,
   webhook events), tool list, playbooks, guardrails, KPIs. **Validate JSON.**
6. **Automation blueprint** — channel orchestration (see Pitfalls re: tooling).
7. **`SKILL.md`** (optional, for Hermes) — let the agent self-load from chat.

## Workflow
1. **Research first.** `web_extract` the company site; `web_search` competitors.
   Capture *measured* numbers (carriers, lanes, freshness) and competitor product
   lists — that is the substance. Do not invent; cite the source site.
2. **Write persona (soul) before specs** — tone samples keep everything consistent.
3. **Product + competitive in Agents.md** — honest comparison tables; name each
   competitor's strengths; state your differentiators without arrogance.
4. **tools.md** — give exact tool names + JSON. This is what makes the agent operate.
5. **Compile to system_prompt.md** so an LLM runs from one file.
6. **Wire channels + automation** (Make.com — see Pitfalls).
7. **Make the Telegram bot ANSWER AS the persona** (see below — the #1 failure is a
   bot that is "connected" yet still greets as the default "Hermes Agent from Nous
   Research" and hallucinates the OS).
8. **Verify** generated code (see Pitfalls).

## Making a Telegram bot answer AS the persona (not default Hermes Agent)
A bot that is "connected" but replies with the stock "I'm Hermes Agent…" greeting
is NOT wired. The persona must be injected into the system prompt the gateway uses.

- **Hermes gateway reads the system prompt from `~/.hermes/config.yaml`** at
  startup (`gateway/run.py` → `_load_ephemeral_system_prompt()`): it checks env
  `HERMES_EPHEMERAL_SYSTEM_PROMPT` first, then falls back to config key
  `agent.system_prompt`. So:
  - `hermes config set agent.system_prompt "<system_prompt.md text>"` then
    `hermes gateway restart`. The key shows a "not a recognized config key"
    warning but the gateway DOES read it (`cfg_get(cfg,"agent","system_prompt")`).
  - Compress `system_prompt.md` into one string (no YAML multiline needed; a
    single quoted line is fine). State name/role/owner/voice/guardrails + entity
    pointers.
- **Verify it took:** send a message in Telegram ("Расскажи о себе"), then
  `hermes logs` should show `Sending response (NNN chars) to <chat_id>` with no
  "Blocked unauthorized user" and no default-persona text. If it still answers as
  default Hermes Agent or hallucinates the OS, the prompt is NOT applied to that
  session — fall back to the env var or a `/skill <name>` load.
- **Chat authorization:** gateway blocks unknown chats with
  `Blocked unauthorized user <chat_id>`; until paired it silently drops messages.
  Check `hermes pairing list`; if needed `hermes pairing approve telegram <code>`
  after the user triggers a pairing prompt. (`/pair` may not exist — look for
  `/approve` among registered bot commands via `getMyCommands`.)
- A **local standalone bot** (`python telegram_bot.py`, long-polling, stdlib-only)
  is a valid alternative to the gateway for a single persona bot — see the 409
  pitfall below and `references/telegram-bot-wiring.md`.

## Group behavior in Telegram (read-all, reply-selectively)

When the bot joins a GROUP (not a DM), design behavior explicitly. Common user
intent: "see the whole group context, but don't answer every message — only reply
on mention or when the topic is clearly in your job description; never spam."

- **Privacy mode OFF** is mandatory to see all messages (BotFather → `/setprivacy`
  → Turn off). CRITICAL: after toggling privacy, **remove and re-add the bot to
  the group** — Telegram caches privacy at join time and won't update otherwise.
- **Read-all / reply-selectively** via gateway config (Hermes):
  `telegram: { allowed_chats: [...], group_allowed_chats: [...],
  require_mention: true, observe_unmentioned_group_messages: true }`.
  `observe_unmentioned_group_messages` = bot sees everything; `require_mention` =
  only replies when directly addressed (mention or reply-to-bot).
- **Answer instantly (realtime), not on a schedule**, unless the user explicitly
  wants batch reading. Realtime is the default for "reply when asked." A separate
  hourly sweep conflicts with a realtime bot on the same token (see pitfalls).
- **Personality for non-work chatter:** edit `system_prompt.md` to add (a) a
  light persona touch (e.g. "a dash of British humour — sparingly"; most replies
  stay straight) and (b) a NON-WORK CHATTER rule: respond only when addressed
  directly, don't answer every poke (occasionally is fine), keep it 1–2 sentences,
  never spam unprompted. These are *preferences* — write them into the system
  prompt body, not just memory.
- **No group_id filter unless asked:** to let the bot work in ANY group it's
  added to, do not hardcode a single `GROUP_CHAT_ID`; read all chats the token
  receives.
- **Personal escalation channel:** keep `STEFAN_CHAT_ID` (or owner DM) only for
  private escalations (price-out-of-policy, contracts, finances) — group messages
  are NOT restricted to admin-only.
- Full recipe + `.env` pattern + diff-only `getUpdates` offset mechanics:
  `references/telegram-group-behavior.md`.

## Pitfalls
- **Reconstructing FROM a Make.com export?** Never paste the blueprint into chat —
  a Make `*.blueprint.json` is ~1.5 MB / 366k tokens (real logic is only ~5-10%)
  and Hermes refuses it (`context injection refused: … exceeds the 50% hard limit`).
  Put it in a folder, parse the flow in Python (jq is usually absent on Windows),
  dump prompts/params to a small `_extracted_logic.txt`, then read THAT. Full
  recipe: `references/make-blueprint-to-entity.md`.
- **Large file writes / skill edits can stall the stream mid-call.** A ~700-line
  bot written via one `write_file` timed out. Write the header, then append blocks
  with `cat >> file <<'PYEOF' … PYEOF` in separate `terminal` calls (< ~8K tokens
  each); split big `skill_manage` edits into small patches the same way.
- **Automation tooling: prefer Make.com.** This user has Make.com experience and,
  mid-build, asked to swap an n8n workflow for Make.com ("вместо n8n может лучше
  возьмем Мейк.ком, у меня с ним есть опыт"). Default to **Make.com** for
  Zapier/Make/n8n-class automation unless told otherwise. Note: a Make blueprint
  exports only *module structure + mapping*; **connections** (API keys/tokens) are
  NOT exported for security and must be re-created once per scenario (Settings →
  Connections, or scenario Environment variables).
- **Non-ASCII in files generated via `execute_code`:** `json.dump(obj, f,
  ensure_ascii=False)` raises `UnicodeEncodeError: 'utf-8' codec can't encode
  characters ... surrogates not allowed` if the string carries surrogate-pair
  escapes such as `\ud83d\udde2` (from broken emoji pastes) — even when the rest
  is valid. Fix: use full valid code points (`\U0001F4DE`), or keep
  `ensure_ascii=True`. Always round-trip `json.load` to validate before reporting
  success.
- **Verify generated code; don't trust the write success.** Write a throwaway
  harness that imports the generated module and exercises guards/mocks; assert
  behavior (unknown-tool raises, missing-param raises, missing-key raises, CLI
  JSON-coerces, agent loop invokes the tool). The Hermes runtime auto-approves
  temp scripts whose filename starts with `hermes-verify-` in `%TEMP%`. Run it,
  then delete it. (A `.py` written via `execute_code` may land in the sandbox,
  not the target Windows path — write FINAL files with the `write_file` tool,
  generate/validate with `execute_code`.)
- **Honesty is a feature, not a tone choice.** Encode "honest competitor
  comparison" and "never fabricate ETA/data — show 'no data' as itself" as HARD
  guardrails. B2B freight/logistics buyers distrust hype; the Navo site's own
  "we'll tell you when another tool is the better fit" framing converts.
- **Free tier / self-serve beats sales-cycle framing** when selling dev/API
  products — lead with "try it on your own boxes, 5 free, no card".
- **One spine, composable:** design products so each stands alone but shares a
  data layer (adopt one, add the rest later). Mirrors how a shipment is actually
  booked and is an easy sell.
- **Verify infra/CLI claims before asserting impossibility.** A session went wrong
  when `Modal execution: local` in `hermes status` was read as "no managed cloud
  hosting" — but Nous Portal **Cloud Hosting** is real (portal.nousresearch.com:
  "Deploy in one click and Portal hosts your agent in the cloud, running around the
  clock"). Inspect `hermes <cmd> --help` and `web_extract` the vendor portal/docs
  before claiming a limitation. Concrete gotchas: `hermes auth login` does **not**
  exist (use `hermes setup` / `hermes portal login` / `hermes auth add`); there is
  **no** `hermes deploy` CLI command — cloud deploy is one-click in Hermes Desktop.
- **Do NOT spawn a separate "watcher" / observer bot to read group context.**
  A user mid-build challenged: "why can't Richard just re-read the group himself
  hourly — why add a separate watcher bot? I don't want to multiply bots in the
  group." He was right: the agent's OWN token is the only consumer it needs. A
  second bot reading the same group is redundant and doubles privacy/config work.
  Use the persona bot's own token for both reading and replying.
- **Realtime vs scheduled-sweep are MUTUALLY EXCLUSIVE on one token.** Telegram
  delivers each update to exactly ONE `getUpdates` consumer. If a long-polling
  realtime bot holds the token, a separate hourly-sweep script calling
  `getUpdates` gets nothing (or 409). Decide deliberately: (a) realtime bot =
  instant replies, single process, no sweep; or (b) sweep-only = no realtime bot.
  When the user says "answer immediately, don't wait for the hourly sweep," that
  means realtime wins and the sweep MUST be disabled. See
  `references/telegram-group-behavior.md`.
- **Telegram long-polling: ONLY ONE process per bot — avoid `409 Conflict`.**
  Telegram allows a single `getUpdates` stream per bot. Running the bot twice
  (two `terminal(background=true)` launches, or a manual launch + an auto-spawn)
  makes the two fight: `HTTP Error 409: Conflict`, messages bounce between them,
  replies become flaky. Symptom: bot is "connected" but answers intermittently or
  not at all. Fix recipe: (1) enumerate all runners
  `Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object {
  $_.CommandLine -like '*richard*' }` (or your bot's script name); (2) kill them
  ALL (`Stop-Process -Id <pid> -Force` — note: in git-bash use `/F /PID`, NOT
  `//F`); (3) wait, confirm ZERO; (4) launch EXACTLY ONE; (5) confirm a single
  parent→child chain (2 procs for venv→uv is normal = one bot). When checking
  process count from a script, do NOT spawn a second `richard_bot.py` self-test
  inside the checker — it briefly inflates the count and looks like a duplicate.
  Also: a `background=true` terminal launch creates a deep bash→bash→python chain;
  repeated launches accumulate orphans, so always kill-all-then-one. Detail and a
  stub-mode pattern for placeholder keys: `references/telegram-bot-wiring.md`.

## Orchestrator variant (fleet manager)

When the user wants a *meta-agent* that manages many sub-agents / virtual employees
(rather than one persona for one role), extend the base file set with a fleet layer:

- **`entities/registry.json`** — array of all managed entities (agents, virtual
  employees, connectors, processes) with `id, type, role, status, channels` + a `meta`
  block (count / active / paused / archived). One source of truth for "who exists".
- **`entities/TEMPLATE.md`** — card template for a new entity (id, role, system prompt,
  tools, boundaries, KPIs). Copy per entity.
- **`processes/index.json`** — array of recurring workflows (trigger, status,
  owner_entity, escalates_to) + `meta` block.
- **`processes/TEMPLATE.md`** — process template (steps, inputs/outputs, error handling).
- **`memory/state.json`** — runtime state: active tasks, escalations, `needs_decision`,
  `channel_health` (e.g. `telegram: "disconnected"`), append-only `log`. Read on every
  wake-up.
- **`connectors/` + `channels/`** — README stubs documenting technical connectors
  (Make.com, runtime) and user-facing channels (Telegram, Email, desktop).

Orchestrator build rules:
- Secrets (bot tokens, IMAP/SMTP, API keys) live in `agent.config.json` as **env var
  names only** (`TELEGRAM_BOT_TOKEN`, `EMAIL_IMAP_PASS`, …) — never plaintext. Real
  values sit in the host env / secret store.
- Mark channels/connectors `enabled: false` + `pending` until the user supplies creds;
  track needs in `pending_connectors` and a README.
- "Always-on" across reboots = a `cron` entry (e.g. daily digest) that `deliver`s to the
  user's priority channel; the runtime (Hermes) keeps it alive when the machine is off.
- On wake-up read `agent.config.json` → `memory/state.json` → `entities/registry.json`,
  then reply in the channel the message arrived on.
- The orchestrator *is* a persona agent — reuse `soul.md` / `Agents.md` / `tools.md` /
  `system_prompt.md` from the base build; it just also manages others.
Scaffold: `templates/orchestrator-folder.md`. Pattern notes: `references/orchestrator-pattern.md`.

## References
- `references/make-blueprint-to-entity.md` — REVERSE build: reconstruct a running
  local entity 1:1 FROM a Make.com `*.blueprint.json` export (parse flow in Python,
  extract prompts to a file since the raw 1.5 MB/366k-token export overflows chat,
  map modules→tools, verify in stub mode, register + private GitHub with leak-check).
  Also covers the chunked-write workaround for large files and the MSYS-mktemp path gotcha.
- `references/navo-richard-marlowe.md` — condensed Navo24 product + SeaRates/
  competitor knowledge bank from the Richard Marlowe build. Reuse if extending that
  agent or any ocean-freight sales agent.
- `templates/orchestrator-folder.md` — copy-ready folder scaffold for an orchestrator
  (registry / processes / memory / connectors / channels) + JSON starter contents.
- `references/orchestrator-pattern.md` — when to build an orchestrator vs a single
  persona agent, entity model, env-only secrets, always-on via cron.
- `references/hermes-always-on-deployment.md` — condensed 24/7 architecture: Nous
  Portal Cloud Hosting (one-click, no VPS) + Hermes `gateway`/`enroll`/`cron`/
  `portal` commands, `.gitignore`/`.env.local` secret hygiene, and the verify
  recipe (git check-ignore + gh api tree + Telegram getMe probe).
- `references/telegram-bot-wiring.md` — concrete recipes for (a) making a Hermes
  gateway bot answer AS the persona via `agent.system_prompt`, and (b) running a
  standalone stdlib `telegram_bot.py` (long-polling) with a single-process /
  no-409 rule and a stub-mode pattern for placeholder NOUS/NAVO keys.
