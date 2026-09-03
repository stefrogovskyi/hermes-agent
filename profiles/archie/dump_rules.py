with open('/opt/hermes/profiles/archie/cache/terminal-output/out-1788160440-3216452-28a0.log', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find("Cтрого соблюдай ВСЕ 11 ПРАВИЛ:")
if idx != -1:
    print(text[idx:idx+3500])
