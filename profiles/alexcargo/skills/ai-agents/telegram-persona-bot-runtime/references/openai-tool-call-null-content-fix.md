# OpenAI Tool Call Null-Content Normalization Pitfall

## Problem
When using OpenAI models (`gpt-4o-mini`, `gpt-4o`) with tool calling enabled, OpenAI returns `message.content = None` on assistant messages that contain `tool_calls`.

If `choice` is appended directly to `messages` without normalizing `content`:
```python
messages.append(choice) # content is None!
```
The subsequent `llm_chat()` call in multi-turn or tool execution loops fails with:
```
HTTP Error 400: Invalid type for 'messages[N].content': expected a string, given null.
```
In Telegram agent bots, this exception is caught in the bot loop and triggers fallback/stub error messages (e.g. *"Richard here — briefly lost the line to the desk. One moment, try that again?"*).

## Solution / Fix
Always normalize `choice.content` before appending to `messages` — both before the loop and inside the `while choice.get("tool_calls")` loop:

```python
msg_to_append = {
    "role": choice.get("role", "assistant"),
    "content": choice.get("content") or ""
}
if choice.get("tool_calls"):
    msg_to_append["tool_calls"] = choice["tool_calls"]

messages.append(msg_to_append)
```
