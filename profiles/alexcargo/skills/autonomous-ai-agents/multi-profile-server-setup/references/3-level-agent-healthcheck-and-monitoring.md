# 3-Level Sub-Agent Health Check & Real-Time Monitoring

## The Problem
Running `systemctl is-active hermes-<agent>.service` alone is insufficient to determine if a sub-agent is responsive. A gateway process can remain in state `active (running)` while:
1. Being stuck in an infinite network reconnect loop (`httpx.ReadTimeout` / `telegram.error.TimedOut`).
2. Silently rejecting user messages due to authorization mismatch (`Blocked unauthorized user <ID> in chat <ID>`).
3. Being rate-limited or hitting a Telegram long-polling socket crash without triggering a systemd process exit.

## 3-Level Health Check Protocol

Whenever auditing agent status or verifying cluster health, execute all 3 levels:

### Level 1: Operating System & Systemd
Check if the daemon is active and inspect memory/CPU usage:
```bash
systemctl is-active hermes-<profile>.service
systemctl status hermes-<profile>.service --no-pager
```

### Level 2: Telegram API & Queue Audit
Query Telegram Bot API directly to ensure the bot token is active and incoming messages are being consumed (queue should be 0):
```python
import urllib.request, json

bot_token = "<TELEGRAM_BOT_TOKEN>"
# 1. Verify getMe
me = json.loads(urllib.request.urlopen(f"https://api.telegram.org/bot{bot_token}/getMe").read().decode())
print("Bot username:", me.get("result", {}).get("username"))

# 2. Check pending update queue
webhook = json.loads(urllib.request.urlopen(f"https://api.telegram.org/bot{bot_token}/getWebhookInfo").read().decode())
pending = webhook.get("result", {}).get("pending_update_count", 0)
print(f"Pending updates queue: {pending}")
# If pending > 0 and not decreasing, gateway long-polling has stalled.
```

### Level 3: Journalctl Gateway Log Parsing
Search recent logs for failure indicators:
```bash
journalctl -u hermes-<profile>.service -n 50 --no-pager | grep -E "Blocked unauthorized user|TimedOut|reconnecting|Restart-loop breaker|Exception|error"
```

## Remediation Workflow
If an agent fails Level 2 or Level 3:
1. Check `platforms/pairing/telegram-approved.json` format:
   ```json
   {
     "330656040": {
       "user_name": "Stefan Rogovskiy",
       "approved_at": 1786135940.447417
     }
   }
   ```
2. Restart the systemd service to clear dead network sockets:
   ```bash
   systemctl restart hermes-<profile>.service
   ```
3. Re-verify Level 2 (`pending_update_count == 0`) after 3 seconds.
