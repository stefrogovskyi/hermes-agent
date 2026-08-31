# Telegram Bot Resilience & Single-Consumer Pattern

This reference documents the resilience architecture implemented for Telegram persona bots (Richard, Liz, Alistair, Ben, Callum).

## 1. Top-Level `.env.local` Auto-Loader
Ensure `.env.local` is parsed into `os.environ` BEFORE reading model environment variables (`RICHARD_MODEL`, `LIZ_MODEL`, `ALISTAIR_MODEL`, `BEN_MODEL`, `CALLUM_MODEL`), avoiding fallback to dead model defaults (`tencent/hy3:free`).

## 2. OpenAI SDK Integration
Raw `urllib` HTTP requests to `https://inference-api.nousresearch.com/v1/chat/completions` fail with `403 Forbidden`. Always use the official `openai.OpenAI` client with Nous pool resolution and OpenRouter fallback (`OPENROUTER_API_KEY`).

## 3. Strict Word Boundaries (`\b`)
Regex triggers must use strict word boundaries:
`NAME_RE = re.compile(r"\b(лиз|элизабет|liz|lisa)\b", re.IGNORECASE)`
This prevents false positive triggers on words like *анализ*, *релиз*, *абонемент*, *бензин*.

## 4. Win32 `ctypes` Silent PID Checking
Avoid `tasklist.exe` calls in `pythonw` background processes which can trigger Windows Terminal `0x800700e8` popups. Use:
```python
import ctypes
def pid_alive(pid):
    h = ctypes.windll.kernel32.OpenProcess(0x1000, False, int(pid))
    if h:
        ctypes.windll.kernel32.CloseHandle(h)
        return True
    return False
```

## 5. Duplicate Auto-Exit on 409
If `409 Conflict` is encountered during `getUpdates`, log `[Bot] 409 Conflict detected — exiting` and call `sys.exit(0)`. The second duplicate process exits immediately, leaving exactly ONE healthy long-polling consumer.

## 6. Typing Ticker (`_TypingTicker`)
Run a background daemon thread that sends `sendChatAction(chat_id, "typing")` every 4 seconds while `llm_chat()` generates responses, preventing silent idle appearances on long reasoning turns (>5s).

## 7. Message Chunking and Fallback
Split responses longer than 4000 chars and retry sending without `parse_mode` if Markdown syntax parsing fails.
