# Windows Stealth & Group Trigger Rules for Telegram Persona Bots

## 1. Windowless Process Check (No tasklist.exe Popups)
Avoid calling `subprocess.run(["tasklist", ...])` in watchdog loops. On Windows Terminal, `tasklist.exe` can fail with `0x800700e8` (broken pipe) or flash a black console window. Use native Win32 API via `ctypes`:

```python
import ctypes

def is_process_alive(pid):
    if not pid or pid <= 0:
        return False
    try:
        # PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        h_proc = ctypes.windll.kernel32.OpenProcess(0x1000, False, int(pid))
        if h_proc:
            ctypes.windll.kernel32.CloseHandle(h_proc)
            return True
    except Exception:
        pass
    return False
```

## 2. Strict Regex Word Boundaries (`\b`)
Always wrap group trigger name regexes in `\b` boundaries:

```python
NAME_RE = re.compile(r"\b(liz|elizabeth|лиза)\b", re.IGNORECASE)
```

Without `\b`, substrings inside normal words (like `анализ`, `релиз`, `бензин`) will false-trigger group replies and cause bot spam.

## 3. Top-Level `.env.local` Auto-Loading
Ensure `.env.local` is parsed into `os.environ` at the very top of your script before initializing global constants (`MODEL = os.environ.get(...)`):

```python
_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env.local")
if os.path.exists(_env_path):
    for _line in open(_env_path, encoding="utf-8"):
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _k, _v = _line.split("=", 1)
            os.environ[_k.strip()] = _v.strip().strip("'\"")
```

## 4. OpenAI SDK vs Raw `urllib`
Always use the official `openai` SDK client (`OpenAI(api_key=..., base_url=...)`) when querying Nous or OpenRouter completions. Raw `urllib.request` calls to Nous endpoints return HTTP 403 Forbidden.
