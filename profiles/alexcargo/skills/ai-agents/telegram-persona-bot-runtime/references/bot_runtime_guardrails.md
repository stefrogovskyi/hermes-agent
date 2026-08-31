# Bot Runtime Guardrails & Hardening (Email Draft Cleaning, Group Silence, Cron Scripts)

## 1. Email Draft Meta-Prompt Cleaning
When generating draft replies for emails, LLM outputs often contain intro/outro meta-phrases (`Вот черновик ответа:`, `Черновик готов. Отправляем?`).
- **Rule:** Always run `_clean_draft_body_text()` before saving or sending the email body so clients never receive wrapper prompt strings.
- **Rule:** Never add automatic CC copies to personal email addresses (`dr.reenforce@gmail.com`) when emailing clients unless explicitly requested for that email.

## 2. Group Chat Meta-Commentary Suppressor
When a bot is triggered in a Telegram group by domain keywords without an explicit `@mention`, the LLM may output meta-commentary like `"No @mention of me — staying quiet in the group."` and post it into the chat.
- **Rule:** Filter out messages from other bots (`user.get("is_bot")`) in group chats unless explicitly tagged or replied to.
- **Filter:** Suppress any LLM response in group chats containing meta-silence phrases (`"no @mention"`, `"staying quiet"`, `"не упомянули"`, `"молчу"`) before calling `tg_send_message`.

## 3. Cron & Script Autoreggers (`no_agent=True`)
Cron jobs that execute long-running background scripts (watchdogs, OCI auto-provisioners) MUST set `no_agent=True` and `deliver="local"`. Running them as LLM-agent sessions causes API timeouts and unnecessary error alerts in Telegram.

## 4. SQLite Session & Database Locks
Parallel background jobs and main session storage can conflict on SQLite database locks (`session storage could not be written`).
- **Fix:** Converting all SQLite database files to `PRAGMA journal_mode=WAL;` and `PRAGMA busy_timeout=10000;` solves concurrent reader/writer locks permanently.
