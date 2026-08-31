---
name: claude-code-oauth
description: >-
  Connect a PAID Claude account (Pro/Max subscription) to Claude Code on Windows via
  browserless OAuth, when the Desktop app can't complete login. Use when the owner wants to
  run Claude Code under their subscription (not burn an API key) for heavy design/agent tasks,
  or when `claude auth login` fails to open a browser in a sandbox/headless host.
---

# Claude Code — browserless OAuth for a paid subscription

The owner has a **Claude Pro/Max subscription** and wants Claude Code to run under it (not via
a paid API key). On a sandboxed/headless Windows host the Desktop app can't complete the browser
OAuth, but the **CLI** can emit a manual OAuth URL that you (or the owner) finish in a real browser.

## Steps (verified this session)
1. Check current state:
   `claude auth status` -> `{"loggedIn": false, ...}` if not connected.
2. Launch the login in SIMPLE mode (no TUI needed) and capture the URL it prints:
   `env CLAUDE_CODE_SIMPLE=1 claude auth login --claudeai --email you@example.com`
   (or just `claude auth login --claudeai`). It prints:
   `Opening browser to sign in… If the browser didn't open, visit: https://claude.com/cai/oauth/authorize?...`
3. **Open that URL in the user's own browser** (on the same machine). Because the subscription was
   already consented once, the redirect returns almost instantly to
   `https://platform.claude.com/oauth/code/success?app=claude-code` — a "Build something great /
   You're all set up for Claude Code" page. **No code paste needed** — the live `claude auth login`
   process receives the redirect and prints `Login successful.`
4. If the process already exited before the browser step (timeout), re-run step 2 in a
   **persistent background process** (`terminal(background=True)`) so it stays alive to catch the
   redirect, then open the URL. The FIRST run's `code` is single-use (PKCE) — never reuse a code
   from a dead process; always take the URL from the CURRENT run.

## Confirm
`claude auth status` -> `{"loggedIn": true, "authMethod": "claude.ai", "email": "...", "subscriptionType": "pro"}`

## Owner rules to carry
- **Don't invoke Claude without an explicit separate command.** Default working model for Hermes is
  `tencent/hy3:free` via Nous; Claude (Pro sub) and 405B are reserved for heavy tasks (e.g. the
  Avalanche redesign) ONLY when the owner says so. (This is a memory rule, but the skill exists so
  you CAN use it on request.)
- OAuth uses the **subscription**, not the API key — no token spend. Don't also set
  `ANTHROPIC_API_KEY` unless the owner wants API billing.
- `claude auth login --console` switches to **API billing** (Console) instead of the subscription —
  do NOT use that unless asked.

## Pitfalls
- `claude login` (no subcommand) prints "Not logged in · Please run /login" and exits — use
  `claude auth login --claudeai`.
- A prior (expired) OAuth `code` from a killed process will NOT work (PKCE verifier lost). Always
  take the URL from the CURRENT run.
- The Desktop app's own login fails in sandbox; the CLI path above is the working alternative.
- `claude auth status` shows `apiProvider: firstParty` and `authMethod: claude.ai` when on the
  subscription — that's the goal (not `console`).

## Non-interactive file generation (the permission gate — ROOT CAUSE)
When you run Claude Code to **generate/write files** (e.g. `claude -p "write index.html to <path>"`
for a design task), it will HANG on a write-permission prompt and never save the file. This is NOT
something to work around by doing the task yourself — **fix the root cause**.
- Cause: by default Claude Code asks approve for writes outside its cwd; in non-interactive (`-p`)
  mode there is no one to click "approve", so it stalls and prints "needs your permission approval".
- Fix: launch with `--dangerously-skip-permissions` (and `--add-dir <dir>` so it can see/write the
  target folder). Example that actually writes the file:
  `claude -p "$(cat prompt.txt)" --model claude-opus-4-6 --add-dir "C:/.../Design" --dangerously-skip-permissions`
- **Owner rule (correction from Stefan):** never tell the user "I'm fighting the code" or substitute
  your own output for the agent's. Pro-OAuth Claude must just WORK — investigate WHY it stalled and
  unblock it. The flag above is the unblock. Do NOT pad the session with "Claude got stuck" narrations.
- Note: `--dangerously-skip-permissions` is safe here because the owner explicitly authorized it for
  his own machine/subscription; it only bypasses the local write-confirm dialog, not any remote auth.
