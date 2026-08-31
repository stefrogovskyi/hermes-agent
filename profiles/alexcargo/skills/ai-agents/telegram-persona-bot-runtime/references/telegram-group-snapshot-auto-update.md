# Telegram Persona Bot Runtime — Snapshot Auto-Update, Russian Declensions & Gemini Direct API

## 1. Quoted / Tagged Status Snapshots Auto-Update Rule
When a user tags or quotes a status report/release snapshot (e.g. from Gaffer or Sort It Bot listing `Shipped: 10 (task_A, task_B...)`) and says "update in tracker" ("обнови в трекере"):
- **NEVER** reply asking "which task ID?" or "give me specifics".
- **ALWAYS** immediately call `read_tracker_sheet` / `list_tasks`, parse the task names from the quoted snapshot, match them against the sheet, and execute `update_task` to set `percent: 100%` on each matched task.

## 2. Group Mention Regex for Russian Declensions
In Telegram groups, users address persona bots using Russian noun inflections (`Алистер`, `Алистера`, `Алистеру`, `Алистером`, `Алистере`).
- A strict regex like `re.compile(r"(алистер|alistair)")` will miss group messages from other team members.
- Always use declension-aware word-boundary regexes:
  ```python
  NAME_RE = re.compile(r"\b(алистер[а-я]*|alistair[a-z]*|allister|alister|алику?)\b", re.IGNORECASE)
  ```

## 3. Direct Google Gemini API Integration (`GEMINI_API_KEY`)
- When `GEMINI_API_KEY` or `GOOGLE_API_KEY` is present in the environment, call Google AI Studio's OpenAI-compatible endpoint directly at `https://generativelanguage.googleapis.com/v1beta/openai/` with `gemini-2.5-flash` / `gemini-1.5-flash`.
- Set `max_tokens=2048` in completion requests to prevent OpenRouter/Google from requesting maximum 65,535 token budgets that trigger credit errors.
- This avoids paid credits errors (404) on Nous Portal and rate limits (429) on OpenRouter free tiers.

## 4. Task ID Labeling in Sheet Output
- When returning sheet rows to the LLM, format each row with explicit `ID <number>` labels (e.g. `ID 4 | Task: ...`).
- This prevents LLMs from confusing ordinal list position (1st, 2nd, 3rd) with task IDs or inventing legacy formula prefixes (`a4`, `a5`).
