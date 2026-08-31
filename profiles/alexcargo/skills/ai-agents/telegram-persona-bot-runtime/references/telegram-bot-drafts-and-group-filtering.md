# Telegram Persona Bot: Email Draft Cleaning & Group Filtering Guidelines

## 1. Email Draft Cleaner (`_clean_draft_body_text`)
When a Telegram persona bot prepares an email draft for user approval in chat:
- **Problem:** Raw LLM outputs frequently include system meta-prompts or confirmation wrappers (e.g., `Вот черновик ответа клиенту:`, `---`, `Тема: ...`, `Черновик готов. Отправляем?`). If approved directly, these wrapper phrases get sent to the customer in the email body.
- **Fix:** Always pass raw draft text through an explicit cleaning function (`_clean_draft_body_text`) before saving to JSON or calling `send_email_direct`.
- **Implementation:**
  ```python
  def _clean_draft_body_text(raw_text):
      if not raw_text:
          return ""
      lines = raw_text.splitlines()
      cleaned = []
      for line in lines:
          l_str = line.strip()
          if l_str.startswith("Вот черновик") or l_str.startswith("Тема:") or l_str == "---":
              continue
          if l_str.startswith("Черновик готов") or l_str.startswith("Отправляем?") or 'Напиши "Отправляй"' in l_str:
              break
          cleaned.append(line)
      res = "\n".join(cleaned).strip()
      return res if res else raw_text
  ```

## 2. Group Chat Bot-Filtering & Meta-Silence Suppression
When a persona bot operates in Telegram group chats:
- **Problem 1 (Bot Chatter Trigger):** Automated broadcasts from other bots (e.g., task dumps from `The Gaffer`) containing domain keywords trigger the persona bot to evaluate `should_reply() = True`.
- **Fix 1:** Check `msg.get("from", {}).get("is_bot")`. If `True`, immediately skip (`continue`) unless explicitly `@mentioned` or replying to a message from the persona bot.
- **Problem 2 (Meta-Silence Commentary Leak):** The LLM generates text explaining why it is staying quiet (e.g., `"No @mention of me — staying quiet in the group as I should."`), and the code posts it to the group chat.
- **Fix 2:** Implement a Meta-Silence Suppressor in the flush/send loop:
  ```python
  meta_patterns = ["no @mention", "staying quiet", "staying out of the group", "won't post", "no tag", "не упомянули", "не обращались", "молчу"]
  if chat_type != "private" and any(p in (reply or "").lower() for p in meta_patterns):
      print("[Bot] Suppressing meta-silence reply in group")
      continue
  ```

## 3. Strict Recipient Delivery (No Unrequested Auto-CC)
- Never inject default automatic CCs (e.g. to personal Gmail addresses) unless explicitly requested by the user per conversation. Keep email routing strict to specified recipients.
