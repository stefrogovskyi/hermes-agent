Telegram group chat trigger policy for all bots (Alistair, Callum, Richard): respond ONLY if (1) @mentioned, (2) replied/quoted to, or (3) bot name is explicitly mentioned in any declension/case. require_mention: true set in config.yaml.

### Group 'Navo Agents' (-5305384342) Specific Rules:
1. Respond ONLY when explicitly tagged via @mention (@bot_username).
2. Plain text name mentions or untagged replies/quotes do NOT trigger responses in this group.
3. When replying to or quoting other bots in this group, explicitly tag them (@mention) ONLY if a response or action is required from them.
4. Do NOT tag other bots if no response or action is needed.
5. These rules apply specifically to group 'Navo Agents' (-5305384342).
§
Navo24 main domains & tasks: B2B outreach, lead processing/handling, container tracking, and commercial proposals/offers (КП).
§
ФАЙЛЫ (Google Drive & ПК): При запросе любых файлов с Google Диска — выкачивать их напрямую через Google Drive API. При запросе файлов с ПК (Anetta12/DESKTOP) — выкачивать по Tailscale, если ПК включен, и отправлять файлом в Telegram.