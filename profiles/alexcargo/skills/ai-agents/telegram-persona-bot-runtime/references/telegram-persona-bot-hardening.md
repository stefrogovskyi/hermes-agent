# Telegram Persona Bot — Hardening & Operational Patterns

### 1. Group Name Regex & Russian Declensions
When listening for persona name mentions in group chats, matching exact nominative form (e.g. `алистер`) fails on Russian declensions (`Алистера`, `Алистеру`, `Алистером`, `Алистера в группе`). Use word boundaries and suffix wildcards:
```python
NAME_RE = re.compile(
    r"\b(алистер[а-я]*|alistair[a-z]*|allister|alister|алику?)\b",
    re.IGNORECASE,
)
```

### 2. Snapshot & Status Report Auto-Update Rule
When the user quotes a status report / release snapshot (e.g. from Sort It Bot or Gaffer) and says "update in tracker":
1. Never ask "which task ID?" or "what details?". The task titles are in the quoted report.
2. Call `read_tracker_sheet` to fetch current tasks live from Google Sheets.
3. Match quoted task titles against sheet items and call `update_task` to set `percent: 100%`.
4. Report back the updated tasks clearly with task IDs and titles.

### 3. OpenRouter max_tokens Budget Trap
When calling OpenRouter with models like `google/gemini-2.5-flash`, omitting `max_tokens` causes OpenRouter to default to `max_tokens=65535`, triggering HTTP 402 budget errors even on low token usage. Always pass `max_tokens=2048` in request kwargs.

### 4. Direct Google Gemini API Integration
When using `GEMINI_API_KEY` for direct Google AI Studio access, use Google's OpenAI-compatible endpoint:
`https://generativelanguage.googleapis.com/v1beta/openai/`
Models: `gemini-2.5-flash`, `gemini-1.5-flash`.

### 5. Windows Console Unicode Protection
At script startup, reconfigure stdout/stderr to prevent emoji printing crashes under Windows codepages:
```python
import sys

if hasattr(sys.stdout, "reconfigure"):
  sys.stdout.reconfigure(encoding="utf-8", errors="replace")
  sys.stderr.reconfigure(encoding="utf-8", errors="replace")
```
