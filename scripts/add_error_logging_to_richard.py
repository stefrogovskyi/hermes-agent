# -*- coding: utf-8 -*-
import os, re

bot_p = r"C:\Users\Stefan\My Drive\Equity\My Biz\Partner companies\Navo\6. Departments\Richard Marlowe\Richard Hermes\richard_bot.py"
txt = open(bot_p, encoding='utf-8', errors='ignore').read()

old_except = """                    except Exception as e:
                        print("[Richard] agent error: %s" % e)
                        reply = ("Richard here — briefly lost the line to the desk. "
                                 "One moment, try that again?")"""

new_except = """                    except Exception as e:
                        import traceback
                        err_msg = f"[Richard] agent error: {e}\\n{traceback.format_exc()}"
                        print(err_msg)
                        try:
                            log_p = r"C:\\Users\\Stefan\\AppData\\Local\\hermes\\richard_agent_error.log"
                            with open(log_p, "a", encoding="utf-8") as f_err:
                                f_err.write(f"=== {time.strftime('%Y-%m-%d %H:%M:%S')} ===\\n{err_msg}\\n\\n")
                        except Exception:
                            pass
                        reply = ("Richard here — briefly lost the line to the desk. "
                                 "One moment, try that again?")"""

if old_except in txt:
    txt = txt.replace(old_except, new_except)
    open(bot_p, "w", encoding='utf-8').write(txt)
    print("✅ Added detailed error logging to richard_bot.py!")
else:
    print("⚠️ Pattern not matched directly, checking...")
