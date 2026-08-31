# Telegram Persona Bot Runtime — LLM & Tool Calling Pitfalls & Fixes

## Overview
Captured lessons and reproduction recipes from live agent sessions (including Richard Marlowe / Navo24 persona bot).

---

## 1. Top-Level Model Constants vs `_load_env()` Sequence Pitfall

### Symptom
Bot crashes or falls back to an error stub (`"lost the line to the desk"`) during agent execution, even though `.env.local` contains valid API keys.

### Root Cause
Evaluating model constants at module import time BEFORE `_load_env()` is called:
```python
MODEL = os.environ.get("RICHARD_MODEL", "tencent/hy3:free")  # Evaluated BEFORE _load_env()!

def _load_env():
    # ... loads .env.local
```
At module load time, `os.environ.get("RICHARD_MODEL")` evaluates to the fallback default string (`"tencent/hy3:free"`). When `run_agent()` is invoked, it attempts requests against the dead/unauthorized model, fails after 3 retries (15-second delay), and throws an exception caught by the fallback error block.

### Fix
Execute `_load_env()` at the VERY TOP of the module before any `os.environ` evaluation, or evaluate `MODEL` dynamically inside `run_agent()`:
```python
_load_env()  # MUST RUN FIRST at module top-level!

MODEL = os.environ.get("RICHARD_MODEL", "gpt-4o-mini")
```

---

## 2. OpenAI `tool_calls` `null` Content Serialization Pitfall

### Symptom
When the bot calls a tool (e.g., `send_email`, `get_container_detail`), the 1st step succeeds, but on the 2nd step (when returning the tool output to the LLM) the API returns `HTTP Error 400 Bad Request: Invalid type for 'messages[1].content': expected a string, given null.`.

### Root Cause
In OpenAI API, assistant messages generated with `tool_calls` have `"content": null`. When the code appends `choice` back to `messages` as `messages.append(choice)` without converting `None` -> `""`, OpenAI rejects `"content": null` in subsequent turns.

### Fix
Normalize `choice` before appending to `messages` both in the main call AND inside the `while choice.get("tool_calls")` loop:
```python
choice = resp["choices"][0]["message"]
msg_to_append = {
    "role": choice.get("role", "assistant"),
    "content": choice.get("content") or ""  # Convert None -> ""!
}
if choice.get("tool_calls"):
    msg_to_append["tool_calls"] = choice["tool_calls"]

messages.append(msg_to_append)
```

---

## 3. `NameError` on Undefined Helper Classes (`_TypingTicker`)

### Symptom
Console run works fine when called without parameters, but when called from Telegram long-poll (`token` and `chat_id` present), `run_agent()` crashes with `NameError: name '_TypingTicker' is not defined`.

### Root Cause
`_TypingTicker` class definition was placed below `run_agent()` or omitted. When `token` and `chat_id` were passed, line 350 evaluated `_TypingTicker(token, chat_id)` and threw `NameError`.

### Fix
Define `_TypingTicker` class above `run_agent()`:
```python
import threading

class _TypingTicker:
    """Send 'typing' chat action to Telegram during long operations."""
    def __init__(self, token, chat_id, interval=4.0):
        self.token = token
        self.chat_id = chat_id
        self.interval = interval
        self._stop = threading.Event()
        self._thread = None

    def _loop(self):
        while not self._stop.is_set():
            try:
                tg_request("sendChatAction", self.token, {"chat_id": self.chat_id, "action": "typing"})
            except Exception:
                pass
            self._stop.wait(self.interval)

    def start(self):
        if not self._thread or not self._thread.is_alive():
            self._stop.clear()
            self._thread = threading.Thread(target=self._loop, daemon=True)
            self._thread.start()

    def stop(self):
        self._stop.set()
```

---

## 4. Isolated Background Environment vs Shell Terminal Pitfall

### Symptom
Running a test script directly in a terminal shell succeeds, but running the bot as a background process (`pythonw.exe` / `bot_watchdog.py`) causes the bot to fail or say "LLM key not configured".

### Root Cause
The terminal shell inherits exported host environment variables (`OPENAI_API_KEY`, etc.), whereas background process runners (`pythonw.exe`) execute in an isolated environment and rely EXCLUSIVELY on `.env.local` or `.env`.

### Fix
In `_load_env()`, explicitly load BOTH the host Hermes `.env` (`C:\Users\Stefan\AppData\Local\hermes\.env`) AND the bot's local `.env.local`:
```python
def _load_env():
    # Load host Hermes .env
    host_env = r"C:\Users\Stefan\AppData\Local\hermes\.env"
    if os.path.exists(host_env):
        with open(host_env, encoding="utf-8", errors="ignore") as fh:
            for line in fh:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip().strip('"').strip("'")

    # Load local .env.local
    here = os.path.dirname(os.path.abspath(__file__))
    for envf in (".env", ".env.local"):
        p = os.path.join(here, envf)
        if os.path.exists(p):
            with open(p, encoding="utf-8", errors="ignore") as fh:
                for line in fh:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        os.environ[k.strip()] = v.strip().strip('"').strip("'")
```

---

## 5. Explicit Tool Schema Registration Requirement

### Symptom
User asks the bot in Telegram: "Send an email to X", but the bot hallucinates: "It seems there was an error when attempting to send the email. Should I try again?"

### Root Cause
The bot script had `richard_email.py` available, but did NOT declare `send_email` in its `tools` schema array passed to `llm_chat(messages, tools)`. The LLM saw no `send_email` function in its schema and attempted to generate text pretending it tried.

### Fix
Explicitly append custom tool schemas (such as `send_email`) to `tools`:
```python
EMAIL_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "send_email",
        "description": "Send an email directly from rich@navo24.com to a client or team member",
        "parameters": {
            "type": "object",
            "properties": {
                "to_email": {"type": "string", "description": "Recipient email address"},
                "cc_email": {"type": "string", "description": "Optional CC email address"},
                "subject": {"type": "string", "description": "Email subject line"},
                "body_html": {"type": "string", "description": "Email body text/HTML"}
            },
            "required": ["to_email", "subject", "body_html"]
        }
    }
}

tools = (nc.tool_schemas() or []) + [EMAIL_TOOL_SCHEMA]
```
