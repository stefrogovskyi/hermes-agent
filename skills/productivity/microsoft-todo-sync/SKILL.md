---
name: microsoft-todo-sync
description: Use when syncing MS To-Do tasks via Graph or Make webhook.
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Microsoft, To-Do, Tasks, Graph-API, Productivity]
---

# Microsoft To-Do & Task Synchronization Skill

Use this skill when managing, listing, creating, completing, or synchronizing Microsoft To-Do tasks and custom task lists across personal Microsoft accounts (MSA) or work accounts.

## Core Capabilities

1. **Direct Microsoft Graph API (Device Code / Native OAuth Flow)**:
   - Zero-latency bidirectional sync (read lists, fetch tasks, add/complete tasks).
   - Direct personal account endpoints require an active Entra tenant or CLI token.
   - Token storage: `/opt/hermes/auth_ms_todo.json`.

2. **Make.com Webhook Middleware**:
   - Webhook URL stored in `.env` as `MAKE_TODO_WEBHOOK_URL`.
   - Uses verified Microsoft enterprise credentials to bridge personal `live.com` / `outlook.com` accounts without Entra tenant errors.
   - Pair with `Webhook Response` module for synchronous JSON return.

## Direct Microsoft Graph Quick Reference (PowerShell & Python)

### Method A: Microsoft.Graph PowerShell SDK (Direct Windows WAM Authentication — Recommended)

On Windows endpoints, `Connect-MgGraph` authenticates personal accounts (`live.com` / `outlook.com`) via Windows Web Account Manager (WAM) without requiring custom Azure App registrations or developer subscriptions.

```powershell
# 1. Install & Connect
Install-Module Microsoft.Graph.Users, Microsoft.Graph.Authentication -Scope CurrentUser -Repository PSGallery -Force
Connect-MgGraph -Scopes "Tasks.ReadWrite" -ContextScope CurrentUser -NoWelcome

# 2. Query Lists & Tasks via Graph REST
(Invoke-MgGraphRequest -Method GET -Uri "https://graph.microsoft.com/v1.0/me/todo/lists").value | Select-Object id, displayName

# 3. Create a Task
$body = @{
    title = "New Task"
    importance = "high"
    dueDateTime = @{ dateTime = (Get-Date).AddDays(1).ToString("yyyy-MM-ddTHH:mm:ss"); timeZone = "UTC" }
} | ConvertTo-Json
Invoke-MgGraphRequest -Method POST -Uri "https://graph.microsoft.com/v1.0/me/todo/lists/<list_id>/tasks" -Body $body -ContentType "application/json"
```

### Method B: Remote Execution via Base64 EncodedCommand (SSH / Tailscale)

When querying Windows PowerShell remotely from a Linux orchestrator (Hermes VPS) over SSH, avoid string escaping and parser corruption by executing via Base64 Unicode EncodedCommand:

```python
import subprocess, base64, json

ps_script = """
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Connect-MgGraph -Scopes 'Tasks.ReadWrite' -ContextScope CurrentUser -NoWelcome -ErrorAction SilentlyContinue
(Invoke-MgGraphRequest -Method GET -Uri 'https://graph.microsoft.com/v1.0/me/todo/lists').value | ConvertTo-Json -Depth 4
"""
encoded = base64.b64encode(ps_script.encode('utf-16le')).decode('ascii')
cmd = ['ssh', '-o', 'StrictHostKeyChecking=no', 'Stefan@100.79.157.46', 'powershell', '-NoProfile', '-EncodedCommand', encoded]
res = subprocess.run(cmd, capture_output=True, text=True)
lists = json.loads(res.stdout)
```

### Method C: Operations Reference (Graph API REST)

```python
# 1. List Task Folders
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
res = requests.get("https://graph.microsoft.com/v1.0/me/todo/lists", headers=headers)
lists = res.json().get("value", [])

# 2. Create Task
payload = {
    "title": "Task title",
    "importance": "high",
    "dueDateTime": {"dateTime": "2026-08-30T18:00:00", "timeZone": "UTC"}
}
requests.post(f"https://graph.microsoft.com/v1.0/me/todo/lists/{list_id}/tasks", json=payload, headers=headers)
```

## Pitfalls & Best Practices

- **Direct Graph REST with Custom Filters in PowerShell**:
  - In PowerShell, queries with `$filter` parameters like `https://graph.microsoft.com/v1.0/me/todo/lists/<id>/tasks?$filter=status ne 'completed'` require escaping the `$` in strings (or in Remote Base64 scriptblocks: `?`$filter=...`) to prevent PowerShell from parsing `$filter` as an empty variable.
  - When querying Tasks properties, ensure `id`, `title`, `importance`, `status`, and `dueDateTime` are extracted directly from the items.
- **Avoid Manual Multi-Branch Automation Fatigue**:
  - Do NOT ask the user to manually configure complex multi-node visual routers (like Make.com Routers with aggregators and filters) during interactive chat, especially late at night. If utilizing Make.com, prefer a flat 3-node sequence (`Webhook -> Module -> Webhook Response`) or import a pre-configured scenario. Always offer terminal/CLI commands first when the user requests command-line approaches.
- **PowerShell Graph SDK for Windows Personal Accounts**:
  - When Azure CLI (`az`) fails to persist session without active Azure subscriptions, use Microsoft.Graph PowerShell SDK:
    `Install-Module Microsoft.Graph.Users -Scope CurrentUser -Repository PSGallery -Force; Connect-MgGraph -Scopes "Tasks.ReadWrite" -ContextScope Process`
- **Microsoft Personal Account (`live.com` / MSA) Restrictions**:
  - `AADSTS16000` / `first party consent`: Microsoft restricts personal consumer accounts from consenting to arbitrary 1st-party client IDs or creating Azure App registrations outside an Entra tenant.
  - Azure App Registration for Personal Accounts requires an existing Entra ID tenant (M365 Developer sandbox qualifications have become strict).
  - When direct personal account OAuth is blocked by Microsoft tenant policies, **Make.com acting as a pre-consented OAuth bridge is the standard zero-friction path** because Make uses verified multi-tenant enterprise credentials.
- **Make.com Webhook Response Behavior**:
  - A Make.com Custom Webhook without an executed `Webhook Response` module returns a generic `Accepted` (HTTP 200). To return actual lists or tasks synchronously to the caller, the scenario must conclude with a `Webhook Response` module configured with Status `200` and Body mapped to the aggregated JSON array.
- **Azure CLI Interactive Login Trap with Personal Accounts (`NoneType.get`)**:
  - Running interactive `az login --allow-no-subscriptions` with a pure personal Microsoft account (`live.com` / `outlook.com` with no Azure subscriptions) causes Azure CLI's subscription selector to throw an unhandled `AttributeError: 'NoneType' object has no attribute 'get'`.
  - **Fix**: Always use device code flag: `az login --use-device-code --allow-no-subscriptions`. This bypasses the interactive browser tenant picker and cleanly authenticates MSA accounts without subscriptions.
- **Search-Backend Fallback Pattern**:
  - When external metered scrapers/search engines (e.g. Firecrawl) hit credit limits (`Payment Required`), switch search backend seamlessly to local multi-provider engines (`ddgs` / DuckDuckGo engine or Playwright headless Chromium) without stalling conversation flow.
