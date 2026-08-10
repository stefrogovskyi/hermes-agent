import os, json, re

alistair_dir = r"C:\Users\Stefan\My Drive\Equity\My Biz\Partner companies\Navo\6. Departments\Alister Sterling\Alistair Hermes"
sys_p = os.path.join(alistair_dir, "system_prompt.md")
agents_p = os.path.join(alistair_dir, "AGENTS.md")
mem_p = os.path.join(alistair_dir, "alistair_memory.json")

clean_roster = """
ОФИЦИАЛЬНЫЙ СОСТАВ КОМАНДЫ NAVO (СТРОГИЕ ИМЕНА И НИКНЕЙМЫ):
В нашей компании работают СТРОГО и ИСКЛЮЧИТЕЛЬНО следующие коллеги:
1. @stefrogovskiy (или @Stefan) — Стефан Роговский, наш Босс и CEO компании Navo.
2. @lxxmng — Алексей, наш Tech Lead.
3. @thegaffermcp_bot — Гаффер (Gaffer), наш AI QA & MCP Agent (НИКОГДА НЕ НАЗЫВАЙ ЕГО ДЖОРДЖЕМ ИЛИ GEORGE!).
4. @callumvancebot — Каллум Вэнс, наш Full-Stack Engineer.
5. @richnavobot — Ричард Марлоу, наш Senior Sales Manager.
6. 8 Сейлз-Менеджеров: Катя Комарова, Катя Капустян, Саша Грабарчук, Андрей Городинский, Олег Червинский, Катя Кернеш, Лера Гулий, Лиля Ховрак.

СТРОГИЙ ЗАПРЕТ ПО ИМЕНАМ:
- В вашей команде НЕТ Лиз Харпер (Liz Harper). Вы с ней не знакомы! Удалить любые упоминания!
- В вашей команде НЕТ Джорджа (George), НЕТ Марии (Maria), НЕТ "Этеликс", "Цемен", "CPEVCoreBot".
Никогда не выдумывайте вымышленных коллег!
"""

# 1. Clean alistair_memory.json
if os.path.exists(mem_p):
    txt = open(mem_p, encoding='utf-8', errors='ignore').read()
    # Remove any keys/content containing 'liz', 'харпер', 'мария', 'этеликс', 'цемен', 'джордж'
    d = json.loads(txt)
    for k in list(d.keys()):
        val_str = str(d[k]).lower()
        if any(w in val_str for w in ['liz', 'харпер', 'мария', 'этеликс', 'цемен', 'cpevcorebot']):
            del d[k]
    with open(mem_p, 'w', encoding='utf-8') as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
        print("✅ Cleaned alistair_memory.json of Liz Harper & gibberish names!")

# 2. Update system_prompt.md
sys_txt = open(sys_p, encoding='utf-8', errors='ignore').read()
sys_txt = re.sub(r'ОФИЦИАЛЬНЫЙ СОСТАВ КОМАНДЫ NAVO.*?(?=\n\n|\Z)', '', sys_txt, flags=re.DOTALL)
sys_txt = clean_roster + "\n\n" + sys_txt.strip()
open(sys_p, "w", encoding='utf-8').write(sys_txt)
print("✅ Updated system_prompt.md with clean roster!")

# 3. Update AGENTS.md
agents_txt = open(agents_p, encoding='utf-8', errors='ignore').read()
agents_txt = re.sub(r'ОФИЦИАЛЬНЫЙ СОСТАВ КОМАНДЫ NAVO.*?(?=\n\n|\Z)', '', agents_txt, flags=re.DOTALL)
agents_txt = clean_roster + "\n\n" + agents_txt.strip()
open(agents_p, "w", encoding='utf-8').write(agents_txt)
print("✅ Updated AGENTS.md with clean roster!")
