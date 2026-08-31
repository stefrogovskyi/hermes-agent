# Telegram Bot Resilience & Multi-Provider Architecture (2026 Update)

## 1. Primary & Fallback LLM Completion Chain (`llm_chat`)
To prevent `401 Unauthorized`, `429 Rate Limit`, or `404 Not Found` from dropping persona bots or triggering stub responses:

```python
def _get_active_llm_keys():
    or_k = os.environ.get("OPENROUTER_API_KEY", "")
    g_k = os.environ.get("GEMINI_API_KEY", "")
    return or_k, g_k

def llm_chat(messages, tools=None):
    or_k, g_k = _get_active_llm_keys()
    
    # 1. Primary Fast Endpoint: Google Gemini 2.5 Flash API (0.3s response time)
    if g_k:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={g_k}"
            contents = []
            for m in messages:
                role = "user" if m.get("role") in ("user", "system") else "model"
                contents.append({"role": role, "parts": [{"text": m.get("content", "")}]})
                
            body = json.dumps({"contents": contents}).encode("utf-8")
            req = urllib.request.Request(url, data=body, method="POST")
            req.add_header("Content-Type", "application/json")
            
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                if text and "lost the line" not in text:
                    return text.strip()
        except Exception as e:
            print(f"[LLMChat] Gemini 2.5 Flash failed: {e}")

    # 2. Backup Chain: OpenRouter
    openrouter_models = [
        "google/gemma-4-31b-it:free",
        "meta-llama/llama-3.3-70b-instruct:free",
        "google/gemma-4-26b-a4b-it:free",
        "nvidia/nemotron-3-nano-30b-a3b:free"
    ]
    
    if or_k:
        for model in openrouter_models:
            url = "https://openrouter.ai/api/v1/chat/completions"
            body = json.dumps({
                "model": model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1000
            }).encode("utf-8")
            
            req = urllib.request.Request(url, data=body, method="POST")
            req.add_header("Authorization", f"Bearer {or_k}")
            req.add_header("Content-Type", "application/json")
            
            try:
                with urllib.request.urlopen(req, timeout=20) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                    if content and "lost the line" not in content:
                        return content.strip()
            except Exception as e:
                print(f"[LLMChat] OpenRouter model {model} failed: {e}")

    raise RuntimeError("All LLM providers failed.")
```

## 2. SQLite Database Concurrency (`journal_mode=WAL`)
To avoid `session storage could not be written` / `database is locked` during concurrent cron job runs:
Set `PRAGMA journal_mode=WAL;` and `PRAGMA busy_timeout=10000;` on all `.db` files under `AppData\Local\hermes`.

## 3. Single-Instance Enforcer
Ensure `_acquire_lock()` checks `ctypes.windll.kernel32.OpenProcess` against `<bot>.lock` and avoids matching watchdog script names in `psutil.process_iter()`.
