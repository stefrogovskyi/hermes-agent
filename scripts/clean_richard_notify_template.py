# -*- coding: utf-8 -*-
"""
clean_richard_notify_template.py — Улучшение форматирования уведомлений Ричарда в Telegram (убираем дублирование разделителей).
"""

import os, re

richard_dir = r"C:\Users\Stefan\My Drive\Equity\My Biz\Partner companies\Navo\6. Departments\Richard Marlowe\Richard Hermes"
bot_p = os.path.join(richard_dir, "richard_bot.py")

txt = open(bot_p, encoding='utf-8', errors='ignore').read()

old_notify = """                notify_text = (f"📬 <b>ВХОДЯЩЕЕ ПИСЬМО И ГОТОВЫЙ ЧЕРНОВИК ОТВЕТА!</b>\\n\\n"
                               f"👤 <b>От кого:</b> {clean_from}\\n"
                               f"📌 <b>Тема:</b> {clean_subj}\\n"
                               f"💬 <b>Вопрос клиента:</b> «{clean_body}»\\n\\n"
                               f"✍️ <b>ЧЕРНОВИК ОТВЕТА РИЧАРДА:</b>\\n"
                               f"{clean_draft}\\n\\n"
                               f"-----------------------------------\\n"
                               f"<i>Напиши 'Отправляй' или закомментируй правки для отправки клиенту.</i>")"""

new_notify = """                notify_text = (f"📬 <b>ВХОДЯЩЕЕ ПИСЬМО И ГОТОВЫЙ ЧЕРНОВИК ОТВЕТА</b>\\n\\n"
                               f"👤 <b>От кого:</b> {clean_from}\\n"
                               f"📌 <b>Тема:</b> {clean_subj}\\n"
                               f"💬 <b>Вопрос клиента:</b> «{clean_body}»\\n\\n"
                               f"✍️ <b>ЧЕРНОВИК ОТВЕТА РИЧАРДА:</b>\\n"
                               f"{clean_draft}\\n\\n"
                               f"👉 <i>Напиши \"Отправляй\" для отправки клиенту или закомментируй правки.</i>")"""

if old_notify in txt:
    txt = txt.replace(old_notify, new_notify)
    open(bot_p, "w", encoding="utf-8").write(txt)
    print("✅ Successfully updated clean notify template in richard_bot.py!")
else:
    print("⚠️ Pattern not matched directly, inspecting...")
