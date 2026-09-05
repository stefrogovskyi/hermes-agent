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

### Method A: Cloud Sync Considerations (MSA Personal Accounts vs Enterprise)

> ⚠️ **CRITICAL MSA RESTRICTION**: Microsoft Personal Accounts (`live.com`, `outlook.com`, `@i.ua`, `@gmail.com` linked MSAs) STRICTLY block 1st-party Client IDs with Device Code Flow (`AADSTS16000` / `first party consent` / `invalid_request`). NEVER suggest Device Code Flow with standard client IDs for personal MSA accounts.

For 24/7 headless cloud sync on personal accounts:
1. **Periodic Desktop Poller (Recommended default)**: Linux orchestrator polls the Windows desktop via Tailscale SSH + Base64 PowerShell when online, saving local JSON snapshots (`/opt/hermes/state/ms_todo_full_snapshot.json`) via cron every 30m so tasks remain accessible offline.
2. **Custom Azure App Registration**: Register an App ID in Azure Portal with "Personal Microsoft accounts only" and NativeClient redirect URI (`https://login.microsoftonline.com/common/oauth2/nativeclient`) to generate a permanent OAuth2 refresh token.
3. **Power Automate Cloud Flow Caveat**: Power Automate HTTP Request triggers and Premium To-Do connectors fail on personal MSA accounts with tenant mismatch error: `Selected user account does not exist in tenant 'Microsoft Services' and cannot access application '6204c1d1-4712-4c46-a7d9-3ed63d992682'`. Do not suggest Power Automate Cloud Flows for personal Microsoft accounts without an M365 Business tenant.

### Method B: Microsoft.Graph PowerShell SDK (Direct Windows WAM Authentication)

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

### Method B: Remote Execution & Background Windows Task Dumper (SSH / Tailscale)

When Windows WAM session is authenticated by the user in PowerShell, other headless background processes (SSH/cron) may not share the interactive security context directly without explicitly running under the user profile.

To achieve continuous background synchronization without user friction:
1. **Background Windows Scheduled Task (`HermesTodoDumper`)**:
   Register a hidden scheduled task on the Windows desktop that runs every 30 minutes to dump all lists and tasks to a stable local JSON file:
   ```powershell
   # auto_dump_todo.ps1
   $ErrorActionPreference = 'SilentlyContinue'
   Import-Module Microsoft.Graph.Authentication, Microsoft.Graph.Users -ErrorAction SilentlyContinue

   $lists = (Invoke-MgGraphRequest -Method GET -Uri "https://graph.microsoft.com/v1.0/me/todo/lists" -ErrorAction SilentlyContinue).value
   if ($lists) {
       $all = @()
       foreach ($l in $lists) {
           $tasks = (Invoke-MgGraphRequest -Method GET -Uri "https://graph.microsoft.com/v1.0/me/todo/lists/$($l.id)/tasks" -ErrorAction SilentlyContinue).value
           if ($tasks) {
               foreach ($t in $tasks) {
                   $all += [PSCustomObject]@{ List = $l.displayName; Title = $t.title; Status = $t.status; Importance = $t.importance }
               }
           }
       }
       $all | ConvertTo-Json -Depth 4 | Set-Content "C:\Users\Stefan\AppData\Local\hermes\todo_live.json" -Encoding UTF8
   }
   ```
2. **Scheduled Task Registration & Invisible Execution**:
   > ⚠️ **WINDOWS TERMINAL POPUP BUG**: On Windows 11 where Windows Terminal is default terminal handler, triggering `powershell.exe -WindowStyle Hidden` via Task Scheduler still briefly spawns an interactive Windows Terminal window that can hang or steal user focus.
   > **Fix**: Always launch through `wscript.exe` running a `.vbs` wrapper (`WindowStyle = 0`). See `references/windows_touchpad_and_terminal_troubleshooting.md` for full Windows 11 gesture freeze and terminal overlay prevention guides.
   ```vbs
   ' run_todo_silent.vbs
   Set WshShell = CreateObject("WScript.Shell")
   WshShell.Run "powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File ""C:\Users\Stefan\AppData\Local\hermes\auto_dump_todo.ps1""", 0, False
   ```
   ```powershell
   $action = New-ScheduledTaskAction -Execute "wscript.exe" -Argument '"C:\Users\Stefan\AppData\Local\hermes\scripts\run_todo_silent.vbs"'
   $trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 30)
   $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -Hidden -Priority 7
   Register-ScheduledTask -TaskName "HermesTodoDumper" -Action $action -Trigger $trigger -Settings $settings -Force
   ```
3. **Linux Cron Poller (`pull_todo_from_pc.py` every 30m)**:
   Pulls `C:\Users\Stefan\AppData\Local\hermes\todo_live.json` via Tailscale SSH (`Stefan@100.79.157.46`) directly into `/opt/hermes/state/ms_todo_live_snapshot.json` so the orchestrator retains an up-to-date snapshot 24/7 even when the desktop goes offline.
   - **UTF-8 BOM Stripping**: PowerShell `Set-Content -Encoding UTF8` emits a UTF-8 BOM (`\ufeff`), which crashes Python `json.loads` (`Unexpected UTF-8 BOM`). Always strip `\ufeff` before parsing or use `encoding='utf-8-sig'`.
   - **Zero User Disruption Requirement**: Always run dumps on the Windows host completely hidden via `wscript.exe` running a `.vbs` wrapper (`WindowStyle = 0`). Black terminal windows / popup consoles must NEVER appear to the user.

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
  - `AADSTS16000` / `first party consent` / `The application is a first party application, the user does not have consent, and users are not permitted to consent to first party applications`: Microsoft STRICTLY blocks personal consumer accounts from consenting to 1st-party Client IDs (e.g. Office client `d3590ed6-52b3-4102-aeff-aad2292ab01c`) via Device Code Flow (`initiate_device_flow`). **NEVER suggest or attempt Device Code Flow with standard client IDs for personal MSA accounts** — it fails 100% of the time with `invalid_request`.
  - Working alternatives for personal accounts:
    1. Custom Azure App Registration (App ID with Personal Accounts scope + native redirect).
    2. Direct Windows WAM authentication over PowerShell SDK on the user's desktop.
    3. Make.com webhook bridge (requires `Webhook Response` module for sync return).
    4. Multimodal extraction via screenshot/vision or voice note from mobile when desktop is offline.
- **Make.com Webhook Response Behavior**:
  - A Make.com Custom Webhook without an executed `Webhook Response` module returns a generic `Accepted` (HTTP 200). To return actual lists or tasks synchronously to the caller, the scenario must conclude with a `Webhook Response` module configured with Status `200` and Body mapped to the aggregated JSON array.
- **Azure CLI Interactive Login Trap with Personal Accounts (`NoneType.get`)**:
  - Running interactive `az login --allow-no-subscriptions` with a pure personal Microsoft account (`live.com` / `outlook.com` with no Azure subscriptions) causes Azure CLI's subscription selector to throw an unhandled `AttributeError: 'NoneType' object has no attribute 'get'`.
  - **Fix**: Always use device code flag: `az login --use-device-code --allow-no-subscriptions`. This bypasses the interactive browser tenant picker and cleanly authenticates MSA accounts without subscriptions.
- **Search-Backend Fallback Pattern**:
  - When external metered scrapers/search engines (e.g. Firecrawl) hit credit limits (`Payment Required`), switch search backend seamlessly to local multi-provider engines (`ddgs` / DuckDuckGo engine or Playwright headless Chromium) without stalling conversation flow.
