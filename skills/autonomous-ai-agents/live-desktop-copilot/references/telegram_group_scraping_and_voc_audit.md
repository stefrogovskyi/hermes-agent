# Telethon User-Session Group Scraping & Archive Audits

## Overview
When auditing, parsing, or extracting customer reviews, support tickets, and chat histories from large Telegram groups under an authorized user session (`Telethon`).

## Proven Architecture & Best Practices

### 1. Handling Accounts with Thousands of Dialogs (3,000+ Chats)
- Calling bare `get_dialogs()` on massive user accounts causes RPC timeouts (15–30s+).
- Always use asynchronous stream iteration with batch limit or filter on the fly:
  ```python
  async for d in client.iter_dialogs():
      if any(k in (d.name or "").lower() for k in ["searates", "navo"]):
          print(f"ID: {d.id} | Title: {d.name} | Type: {d.entity.__class__.__name__}")
  ```

### 2. The Legacy Chat vs. Supergroup Migration Boundary
- Telegram groups often migrate from legacy basic groups (`Chat` with negative short IDs, e.g. `-576992469`) to modern supergroups/megagroups (`Channel` with `-100...` IDs, e.g. `-1002456364059`).
- If an investigation covers historical records (e.g. from 2019/2021 to 2026), **both entities must be identified and scanned**. Scanning only the current supergroup loses the earlier years of history.

### 3. Resilient Bulk Extraction to JSON
- Stream messages directly to disk in JSON format rather than holding everything in RAM:
  ```python
  all_msgs = []
  count = 0
  async for m in client.iter_messages(entity):
      count += 1
      if m.text:
          all_msgs.append({
              "id": m.id,
              "date": m.date.strftime("%Y-%m-%d %H:%M:%S"),
              "sender_id": m.sender_id,
              "text": m.text
          })
      if count % 1000 == 0:
          print(f"Progress: {count} messages...")
  ```

### 4. High-Signal VOC & Feedback Filter Patterns
When searching thousands of messages for client reviews and feedback:
- **Direct quotes & Forwarded emails:** Filter by quotes (`"`, `«`, `»`, `>`), email prefixes (`Re:`, `Fwd:`, `Dear customer`), or phrases like `"фидбек от клиента"`, `"клиент написал"`, `"feedback from"`.
- **Social Proof / Praise:** `"works like charm"`, `"happy about"`, `"recommendation internally"`, `"доволен"`.
- **Churn / Discontent:** `"reason for not renewing"`, `"coverage"`, `"not responsive"`, `"high and unreliable rates"`.
