# -*- coding: utf-8 -*-
"""
add_email_inbox_poller_thread.py — Внедрение фонового треда опроса почты (_email_inbox_poller) в richard_bot.py.
При получении нового письма Ричард автономно формирует Черновик ответа через LLM и присылает Стефану в Telegram на утверждение!
"""

import os

richard_dir = r"C:\Users\Stefan\My Drive\Equity\My Biz\Partner companies\Navo\6. Departments\Richard Marlowe\Richard Hermes"
bot_p = os.path.join(richard_dir, "richard_bot.py")

txt = open(bot_p, encoding='utf-8', errors='ignore').read()

poller_code = """
import ms_graph_mail as msgraph
import threading

def _email_inbox_poller(token, stefan_chat_id, interval=60):
    \"\"\"Фоновый поток постоянного вычитания входящей почты rich@navo24.com через MS Graph API.\"\"\"
    print("[Richard] Starting MS Graph Inbox Poller thread (interval 60s)...", flush=True)
    seen_msg_ids = set()

    while True:
        try:
            msgs = msgraph.fetch_unread_messages_graph()
            for m in msgs:
                msg_id = m.get("id")
                if not msg_id or msg_id in seen_msg_ids:
                    continue
                seen_msg_ids.add(msg_id)

                from_addr = m.get("from", "Клиент")
                subject = m.get("subject", "Без темы")
                body = m.get("body", "")

                print(f"[Richard] 📬 NEW INCOMING EMAIL FROM {from_addr} | Subject: {subject}", flush=True)

                # Генерация черновика ответа через run_agent
                prompt = (f"Нам пришло входящее письмо от клиента!\\n"
                          f"От кого: {from_addr}\\n"
                          f"Тема: {subject}\\n"
                          f"Текст письма клиента: «{body}»\\n\\n"
                          f"Сформируй профессиональный, вежливый, коммерческий B2B ответ от имени Richard Marlowe (rich@navo24.com).\\n"
                          f"Учти наши официальные цены: Free tier (€0, 5 конт), Starter (€39/мес, 25 конт), PAYG (€3/конт), Business (~€0.60/конт).\\n"
                          f"Сформулируй ГОТОВЫЙ ДРАФТ ОТВЕТА КЛИЕНТУ.")

                draft_reply = run_agent(prompt, system=RICHARD_SYSTEM)

                # Сохраняем черновик в файловую систему
                draft_id = f"draft_{int(time.time())}"
                remail.save_draft_for_approval(draft_id, from_addr, f"Re: {subject}", draft_reply, body)

                # Отправляем уведомление Стефану в Telegram
                notify_text = (f"📬 <b>ВХОДЯЩЕЕ ПИСЬМО И ГОТОВЫЙ ЧЕРНОВИК ОТВЕТА!</b>\\n\\n"
                               f"👤 <b>От кого:</b> {from_addr}\\n"
                               f"📌 <b>Тема:</b> {subject}\\n"
                               f"💬 <b>Вопрос клиента:</b> «{body}»\\n\\n"
                               f"✍️ <b>ЧЕРНОВИК ОТВЕТА РИЧАРДА:</b>\\n"
                               f"{draft_reply}\\n\\n"
                               f"-----------------------------------\\n"
                               f"<i>Напиши 'Отправляй' или закомментируй правки для отправки клиенту.</i>")

                tg_send_message(token, stefan_chat_id, notify_text)
        except Exception as e:
            print(f"[Richard] _email_inbox_poller error: {e}", flush=True)

        time.sleep(interval)
"""

if "_email_inbox_poller" not in txt:
    # Insert right before bot_loop definition
    if "def bot_loop(" in txt:
        txt = txt.replace("def bot_loop(", poller_code + "\n\ndef bot_loop(")
        
        # Start thread inside bot_loop
        old_start = 'print("[Richard] starting bot loop for %s..." % bot_name)'
        new_start = ('print("[Richard] starting bot loop for %s..." % bot_name)\n'
                     '        # Start Email Poller Thread\n'
                     '        st_chat = os.environ.get("STEFAN_CHAT_ID", "330656040")\n'
                     '        t_poller = threading.Thread(target=_email_inbox_poller, args=(token, st_chat), daemon=True)\n'
                     '        t_poller.start()\n')
        txt = txt.replace(old_start, new_start)
        
        open(bot_p, "w", encoding="utf-8").write(txt)
        print("✅ Successfully injected _email_inbox_poller thread into richard_bot.py!")
    else:
        print("⚠️ Pattern def bot_loop not found!")
else:
    print("Poller thread already present in richard_bot.py")
