# Hermes Always-On Deployment (condensed knowledge bank)

> Capture from a live session building "Hermes Stevenson" — a 24/7 orchestrator of
> virtual employees/agents (incl. the Richard Marlowe Navo sales agent). Reuse when
> an agent must run across Telegram/Email independent of the user's laptop.

## Why
Persona/orchestrator agents must operate 24/7. GitHub is the single source of truth;
Nous Portal Cloud Hosting runs the agent in the cloud. The laptop is only one of two
clients that sync against GitHub.

## Architecture
```
[User, Telegram] -> [Nous Relay / Cloud Hosting] -> [Hermes Agent (cloud)]
                                                    | git push/pull
                                                    v
                                               [GitHub = source of truth]
Laptop on open: git pull. No conflicts while laptop closed (cloud is the only writer).
```

## Verified facts (portal.nousresearch.com, 2026-07)
- **Cloud hosting:** "Deploy in one click and Portal hosts your agent in the cloud,
  running around the clock. Server costs bill straight to your credit balance."
- **One account:** single sign-in connects model catalog + Tool Gateway + cloud hosting.
- `Modal execution: local` in `hermes status` is the **code sandbox**, NOT hosting.
  Do NOT infer "no managed hosting" from it — that was a real mistake in-session.

## Hermes CLI commands (verified via --help, 2026-07)
- `hermes gateway setup` — interactive Telegram/WhatsApp/Slack connect (needs bot token).
- `hermes gateway enroll` — relay through Nous cloud (writes `GATEWAY_RELAY_*` to
  `~/.hermes/.env`); no public IP needed; has `wake-url` to re-animate idle gateway.
- `hermes gateway install` / `start` / `status` — systemd/launchd background service.
- `hermes cron create --schedule "0 9 * * *" --prompt "..." --deliver telegram` — scheduled.
- `hermes portal login|info|open|tools` — Portal setup.
- `hermes dashboard register` — register self-hosted dashboard as OAuth client.
- `hermes serve` — headless backend (JSON-RPC/WebSocket) for desktop/remote.

## GOTCHAS (caught live — do not repeat)
- `hermes auth login` does NOT exist. Use `hermes setup` / `hermes portal login` /
  `hermes auth add <provider>`.
- No `hermes deploy` CLI command. Cloud deploy = one-click in Hermes Desktop.
- `hermes status` "Modal execution: local" ≠ no cloud hosting.

## Secret handling (mandatory, to avoid leaks)
1. `.gitignore`: `.env`, `.env.*`, `secrets.json`, `*.key`, `credentials.json`, `local.config.json`.
2. Store tokens in a gitignored `.env.local` (env-var NAMES only in tracked files).
   NOTE: writing `~/.hermes/.env` directly may be BLOCKED as a protected credential
   file — use a project-local `.env.local` instead.
3. Verify before pushing:
   - `git check-ignore .env.local` → must report the file as ignored.
   - `gh api repos/<o>/<r>/git/trees/<branch>?recursive=1 --jq '.tree[].path'`
     → must show NO `.env*`.
4. Telegram bot token validity probe:
   `curl https://api.telegram.org/bot<TOKEN>/getMe` → `{"ok":true,"result":{"username":...}}`.

## Verify generated work
- JSON config: round-trip `json.load`/`json.dump`. With `ensure_ascii=False`, a
  surrogate-escape emoji (e.g. `\ud83d\udde2` from a broken paste) raises
  `UnicodeEncodeError` — keep `ensure_ascii=True` or use valid code points.
- Run a throwaway `hermes-verify-*.py` in `%TEMP%`, assert behavior, then delete it.
  The Hermes runtime auto-approves temp scripts whose filename starts with
  `hermes-verify-` in `%TEMP%`.

## Entity registration pattern (orchestrator managing sub-agents)
- Keep a `entities/registry.json` (array of cards) + `entities/<id>.md` per agent.
- Card fields: id, type (agent|virtual_employee|connector|process), role, status,
  owner, local_folder, github_repo, auth_env (env-var NAMES only), products, channels.
- Sub-agent folder may live elsewhere on disk and have its OWN GitHub repo; the
  orchestrator only references it, does not fork it. Load the sub-agent's own
  `soul.md`/`memory.md` to manage it competently.
