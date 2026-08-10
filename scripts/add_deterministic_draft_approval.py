# -*- coding: utf-8 -*-
"""
add_deterministic_draft_approval.py — Детерминированный перехват команд 'Отправляй' / 'Да' / 'Ок' в richard_bot.py.
При получении 'Отправляй' или 'Да' бота НЕ спрашивает LLM, а СРАЗУ считывает сохраненный черновик
и мгновенно отправляет письмо клиенту через send_email_direct!
"""

import os, re

richard_dir = r"C:\Users\Stefan\My Drive\Equity\My Biz\Partner companies\Navo\6. Departments\Richard Marlowe\Richard Hermes"
bot_p = os.path.join(richard_dir, "richard_bot.py")

txt = open(bot_p, encoding='utf-8', errors='ignore').read()

approval_handler_code = """
def _check_and_execute_draft_approval(user_text, chat_id, token):
    \"\"\"Детерминированный перехват 'Отправляй' / 'Да' / 'Ок' / 'Send' с мгновенной отправкой черновика.\"\"\"
    text_clean = user_text.lower().strip()
    approval_triggers = ["отправляй", "отправь", "да", "ок", "ok", "send", "отправляй!", "да!"]
    
    is_approval = False
    for tr in approval_triggers:
        if text_clean == tr or text_clean.startswith(tr + " ") or text_clean.startswith(tr + "\n"):
            is_approval = True
            break
            
    if not is_approval:
        return False

    # Check for pending draft in drafts dir
    drafts_dir = os.path.join(here, "drafts")
    if not os.path.exists(drafts_dir):
        return False

    # Find latest json draft
    import glob
    draft_files = sorted(glob.glob(os.path.join(drafts_dir, "*.json")), key=os.path.getmtime, reverse=True)
    if not draft_files:
        return False

    latest_draft_path = draft_files[0]
    try:
        data = json.loads(open(latest_draft_path, encoding="utf-8").read())
        if data.get("status") == "PENDING_STEFAN_APPROVAL":
            to_e = data.get("to_email")
            subj = data.get("subject", "Navo24 Message")
            body = data.get("body_text") or data.get("body_html") or ""
            in_reply = data.get("in_reply_to")
            quoted = data.get("customer_query")

            print(f"[Richard] 🚀 STEFAN APPROVED DRAFT! Sending to {to_e}...", flush=True)
            ok, err = remail.send_email_direct(to_e, subj, body, body, in_reply_to=in_reply, quoted_html=quoted)

            if ok:
                data["status"] = "APPROVED_AND_SENT"
                data["sent_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
                open(latest_draft_path, "w", encoding="utf-8").write(json.dumps(data, indent=2, ensure_ascii=False))
                
                # Delete or archive draft
                try:
                    os.remove(latest_draft_path)
                except Exception:
                    pass

                reply_msg = f"🚀 <b>ПИСЬМО УСПЕШНО ОТПРАВЛЕНО КЛИЕНТУ!</b>\\n\\n📥 <b>Кому:</b> {to_e}\\n📌 <b>Тема:</b> {subj}"
                tg_send_message(token, chat_id, reply_msg)
                return True
            else:
                reply_msg = f"❌ Ошибка отправки письма: {err}"
                tg_send_message(token, chat_id, reply_msg)
                return True
    except Exception as e:
        print(f"[Richard] draft approval handler err: {e}", flush=True)

    return False
"""

if "_check_and_execute_draft_approval" not in txt:
    # Insert right before bot_loop definition
    if "def bot_loop(" in txt:
        txt = txt.replace("def bot_loop(", approval_handler_code + "\n\ndef bot_loop(")
        
        # Inject check inside bot_loop right after user_text processing
        old_flush_loop = """                for _cid, _items in pending.items():
                    _texts = [it["full_text"] for it in _items]"""
                    
        new_flush_loop = """                for _cid, _items in pending.items():
                    _texts = [it["full_text"] for it in _items]
                    _combined_text = "\\n".join(_texts)
                    
                    # 🚀 FAST-PATH: Детерминированный перехват 'Отправляй' / 'Да'
                    if _check_and_execute_draft_approval(_combined_text, _cid, token):
                        continue"""

        txt = txt.replace(old_flush_loop, new_flush_loop)
        
        open(bot_p, "w", encoding="utf-8").write(txt)
        print("✅ Successfully injected deterministic draft approval handler into richard_bot.py!")
    else:
        print("⚠️ Pattern def bot_loop not found!")
else:
    print("Approval handler already present in richard_bot.py")
