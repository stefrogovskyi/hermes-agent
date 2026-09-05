# Case: Anthropic Corporate Claude Long-Term OAuth Setup Token Architecture & Sentry Remote MCP Integration

**Date:** 2026-09-04  
**Profiles involved:** `callum`, `default` (Hermes)  
**Domains:** `ai_infra`, `agent_club`

---

## 1. Context & Request
Stefan explored connecting Navo24's corporate Anthropic Claude account (`claude.ai` Team/Enterprise) to the agent cluster (Callum, Alistair, Hermes) so agents can use Claude 3.7 / 3.5 Sonnet as their reasoning core with full tool-calling and long contexts, without requiring per-token credit balances ($0 on `console.anthropic.com` API balance). He also asked about integrating Sentry monitoring into Callum via Claude vs direct agent MCP.

---

## 2. Technical Analysis & Architecture Differences
1. **Web Session Key vs API Key vs OAuth Setup Token:**
   - **`console.anthropic.com` API Keys:** Charge per million input/output tokens. A company account with $0 on API balance returns HTTP 402/insufficient credits, even with active $30/month seats on `claude.ai`.
   - **`claude.ai` Web Session Tokens (`sessionKey`):** Rapidly expire, reject programmatic tool execution, and lack rate-limit guarantees.
   - **Anthropic OAuth Setup Token (`sk-ant-oat-...`):** Generated via `npx @anthropic-ai/claude-code setup-token`. Operates under the user's flat-rate Claude subscription, lasts 1 year, and supports CLI/agent tooling without touching the API dollar balance.
2. **License Assignment Prerequisite:**
   - In `claude.ai/admin-settings/members`, an Admin account with subscription marked as **`Unassigned`** CANNOT issue an active OAuth setup token.
   - The user must first assign themselves a **Standard** or **Premium** seat in the admin console before initiating authorization.
3. **Sentry Remote MCP (`mcp.sentry.dev`):**
   - Routing Sentry queries through web Claude introduces lag, loss of execution autonomy, and fragile OAuth tunneling.
   - Direct connection via Sentry Remote MCP (`mcp.sentry.dev`) with an internal integration auth token (`sntrys_...`) placed in `profiles/callum/.env` enables Callum to query stack traces, identify file lines, and prepare GitHub PR patches autonomously.

---

## 3. Standard Operating Procedure

### Generating the 1-Year Claude OAuth Setup Token:
1. Verify license in `claude.ai/admin-settings/members`: ensure status is `Standard` or `Premium` (not `Unassigned`).
2. Run on local terminal or server:
   ```bash
   npx @anthropic-ai/claude-code setup-token
   ```
3. Authenticate via browser selecting `stefan@navo24.com` and the `Navo24` organization.
4. Copy the resulting `sk-ant-oat-...` token into `profiles/<agent>/.env` as `CLAUDE_CODE_OAUTH_TOKEN`.

### Connecting Sentry Remote MCP:
1. Generate User Auth Token or Internal Integration Token in Sentry (`project:read`, `event:read`, `issue:read`).
2. Add token to `profiles/callum/.env` (never commit to Git).
3. Connect Callum's runtime to `mcp.sentry.dev` for direct issue inspection, stack trace triage, and automated patch creation.

---

## 4. Key Rules
- Never attempt to use raw web cookies or `sessionKey` for headless server agents.
- For flat-rate corporate Claude usage across agents, use `sk-ant-oat-...` with an assigned paid seat.
- Prefer direct Remote MCP servers (`mcp.sentry.dev`, `trackingmcp`, `freightratesmcp`) over indirect web UI wrappers.
