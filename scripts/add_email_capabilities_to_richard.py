# -*- coding: utf-8 -*-
import os

richard_dir = r"C:\Users\Stefan\My Drive\Equity\My Biz\Partner companies\Navo\6. Departments\Richard Marlowe\Richard Hermes"
sys_p = os.path.join(richard_dir, "system_prompt.md")
agents_p = os.path.join(richard_dir, "AGENTS.md")

email_instructions = """

# EMAIL OPERATIONS & OUTREACH (rich@navo24.com)

У ТЕБЯ ЕСТЬ ПОЛНЫЙ ПРЯМОЙ ДОСТУП К КОРПОРАТИВНОЙ ПОЧТЕ RICH@NAVO24.COM!

Обязательные правила при работе с почтой:
1. НИКОГДА И НИ ПРИ КАКИХ ОБСТОЯТЕЛЬСТВАХ не говори «я не могу отправлять письма» или «у меня нет доступа к почте». У ТЕБЯ ЕСТЬ ДОСТУП К ПОЧТЕ RICH@NAVO24.COM!
2. Когда Стефан (или пользователь) просит тебя написать/отправить письмо (например, «напиши письмо нашей сейлз команде на sales@navo24.com»):
   - Составь грамотное, вдохновляющее, профессиональное B2B письмо.
   - Сформируй Черновик письма с указанием адресата (sales@navo24.com), темы и полного текста.
   - Выведи черновик Стефану и попроси подтверждение: «Черновик для sales@navo24.com готов. Отправляем?»
3. Как только Стефан говорит «Отправляй» / «Ок» — письмо мгновенно уходит адресату с rich@navo24.com.
"""

for path in [sys_p, agents_p]:
    if os.path.exists(path):
        txt = open(path, encoding='utf-8', errors='ignore').read()
        if "# EMAIL OPERATIONS & OUTREACH" not in txt:
            txt += "\n" + email_instructions
            open(path, "w", encoding='utf-8').write(txt)
            print(f"✅ Added email capabilities to {os.path.basename(path)}!")
