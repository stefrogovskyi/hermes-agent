# Upwork Official MCP Setup & CLI Reference

## MCP Endpoint
- **URL:** `https://mcp.upwork.com/mcp`
- **Protocol:** Model Context Protocol (MCP) over Streamable HTTP Transport
- **Auth:** OAuth 2.1 PKCE with Dynamic Client Registration

## CLI Client (`upwork-cli`)
Installed location:
- Source & modules: `/opt/hermes/profiles/ben/tools/upwork-cli`
- Global executable: `/usr/local/bin/upwork`
- Config & tokens: `~/.upwork-cli/tokens.json` (mode 0600)

### Headless Authentication Workflow (Remote VPS)
```bash
# 1. In src/mcp.js, ensure callback server listens on fixed port 8765:
server.listen(8765, '0.0.0.0', () => { ... })

# 2. Run login in background:
node bin/upwork.js login

# 3. Present the printed authorization URL to user:
# https://www.upwork.com/ab/account-security/oauth2/authorize?response_type=code&client_id=...&redirect_uri=http%3A%2F%2F127.0.0.1%3A8765%2Fcallback&resource=https%3A%2F%2Fmcp.upwork.com%2Fmcp

# 4. After user authorizes in browser, browser attempts redirect to:
# http://127.0.0.1:8765/callback?code=<AUTH_CODE>

# 5. User pastes redirect URL into chat. Run curl on VPS:
curl -s "http://127.0.0.1:8765/callback?code=<AUTH_CODE>"
# Output: Authorized ✓
# The CLI background process writes tokens to ~/.upwork-cli and exits 0.
```

### Essential Commands & Proven Syntax

```bash
# Check accounts & role
upwork whoami

# Check full freelancer activity dashboard (connects balance, contracts, invites, matching jobs)
upwork get_freelancer_dashboard check

# Search marketplace jobs (filter by query, limit, table view)
upwork find_jobs search -p query="AI agent" -p limit=10 --table

# Get full details of a job posting (CRITICAL: pass --json to avoid float64 type mismatch)
upwork find_jobs --json '{"action":"get","params":{"id":"<JOB_ID_STRING>"}}'

# List active contracts & milestones
upwork list_contracts search
upwork list_milestones -p contract_id="<CONTRACT_ID>"

# Create draft proposal
upwork manage_proposals create -p job_id="<JOB_ID>" -p cover_letter="<TEXT>" -p rate=75

# Confirm draft proposal (consumes connects)
upwork confirm proposal <DRAFT_ID>

# Real-time messages
upwork messages list_rooms
upwork messages send_message -p room_id="<ROOM_ID>" -p body="<TEXT>"
```
