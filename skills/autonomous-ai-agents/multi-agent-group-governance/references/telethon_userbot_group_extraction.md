# Telethon User Session Group Extractor

Recipe for scanning closed Telegram groups on behalf of an authorized user session without creating new auth sessions or tripping flood limits.

## Configuration & Credentials
- **Session DB:** `/opt/hermes/stefan_userbot.session`
- **Identity:** Stefan Rogovskiy (`@stefrogovskiy`, ID: `330656040`)
- **API Credentials:** `api_id = 31246421`, `api_hash = "e96f7e4b8785d721deb761c55e2c8252"`

## Known Navo Channel / Group IDs
- **Navo Core Group:** `-1004451177709`
- **Navo Tech geeks:** `-1004328290471`

## Python Extraction Script Template
```python
import asyncio
import json
from telethon import TelegramClient

api_id = 31246421
api_hash = "e96f7e4b8785d721deb761c55e2c8252"
session_path = "/opt/hermes/stefan_userbot.session"
group_id = -1004451177709  # Navo

async def scan():
    client = TelegramClient(session_path, api_id, api_hash)
    await client.connect()
    if not await client.is_user_authorized():
        raise RuntimeError("Userbot session is not authorized!")

    entity = await client.get_entity(group_id)
    messages = []
    async for msg in client.iter_messages(entity, limit=2000):
        if msg.text:
            messages.append({
                "id": msg.id,
                "date": msg.date.strftime("%Y-%m-%d %H:%M"),
                "sender_id": msg.sender_id,
                "text": msg.text
            })

    with open("/tmp/extracted_messages.json", "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(scan())
```

## Performance & Safety Best Practices
1. **Never call unbounded `get_dialogs()`**: User accounts with hundreds of channels will hit 20-30s asyncio timeouts. Pass `limit=100` or target the exact entity ID directly via `client.get_entity(group_id)`.
2. **Read-Only**: Strictly enforce `iter_messages` queries. Do not call `send_message`, `delete_messages`, or modify membership without explicit interactive confirmation.
