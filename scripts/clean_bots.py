import os, re

targets = [
    r'C:\Users\Stefan\My Drive\Equity\My Biz\Partner companies\Navo\6. Departments\Richard Marlowe\Richard Hermes\richard_bot.py',
    r'C:\Users\Stefan\My Drive\Equity\My Biz\My companies\Enlight Group\Enlight Board\Liz Harper\Liz Harper Hermes\liz_harper_bot.py',
    r'C:\Users\Stefan\My Drive\Equity\My Biz\Partner companies\Navo\6. Departments\Alister Sterling\Alistair Hermes\alistair_bot.py',
    r'C:\Users\Stefan\My Drive\Equity\My Biz\My companies\Enlight Group\Avalanche Agency\Team\Ben Jett\Ben Jett Hermes\ben_jett_bot.py',
]

for path in targets:
    if os.path.exists(path):
        lines = open(path, encoding='utf-8').readlines()
        clean_lines = []
        for line in lines:
            if 'except urllib.error.HTTPError' in line or 'if e.code == 409:' in line or 'sys.exit(0)' in line:
                if 'def bot_loop' not in line and 'while True:' not in line:
                    continue
            clean_lines.append(line)
        open(path, 'w', encoding='utf-8').writelines(clean_lines)
        print('Cleaned misplaced excepts in:', path)
