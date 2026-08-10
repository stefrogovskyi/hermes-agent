# -*- coding: utf-8 -*-
"""
add_playlist_recommendations_to_yt_cron.py — Добавление авто-рекомендаций плейлистов к каждому видео в 23:00 вестнике YouTube Watch Later.
"""

import os, sys, json, re, html

HERMES_DIR = r"C:\Users\Stefan\AppData\Local\hermes"
script_p = os.path.join(HERMES_DIR, "scripts", "youtube_playlist_sorter.py")

txt = open(script_p, encoding="utf-8").read()

# Add playlist recommendation classifier helper function
recommendation_func = """
def recommend_playlist_for_video(title, channel):
    t = (title + " " + channel).lower()
    
    if any(k in t for k in ['гитара', 'guitar', 'chords', 'аккорды', 'пианино', 'piano', 'музыка', 'music', 'song', 'трек', 'соло']):
        return '🎵 Музыка / Гитара / Пианино'
    elif any(k in t for k in ['юнг', 'психолог', 'сознание', 'мышление', 'мозг', 'философ', 'разум', 'алкоголь', 'смысл']):
        return '🧠 Психология & Саморазвитие'
    elif any(k in t for k in ['логистик', 'shipping', 'sea', 'freight', 'port', 'контейнер', 'searates', 'navo', 'маритим']):
        return '⚓ Логистика & Мореплавание'
    elif any(k in t for k in ['ai', 'ии', 'python', 'code', 'программирован', 'github', 'agent', 'claude', 'gpt', 'upwork', 'freelance']):
        return '💻 ИИ & Кодинг & Бизнес'
    elif any(k in t for k in ['политик', 'экономик', 'илларионов', 'интервью', 'новости', 'история']):
        return '🌐 Аналитика & Экономика'
    else:
        return '📁 Общие Заметки & Избранное'
"""

# Insert helper function before run_interactive_night_check
if 'def recommend_playlist_for_video' not in txt:
    txt = txt.replace("def run_interactive_night_check():", recommendation_func.strip() + "\n\n" + "def run_interactive_night_check():")

# Update formatting loop to include recommendation line
old_loop = """    for v in videos:
        title_esc = html.escape(v['title'])
        chan_esc = html.escape(v['channel'])
        dur_esc = html.escape(v['duration'])
        lines.append(f"<b>{v['num']}.</b> {title_esc}")
        lines.append(f"   ⏱ Длительность: <code>{dur_esc}</code> | Канал: <i>{chan_esc}</i>\\n")"""

new_loop = """    for v in videos:
        title_esc = html.escape(v['title'])
        chan_esc = html.escape(v['channel'])
        dur_esc = html.escape(v['duration'])
        rec_pl = recommend_playlist_for_video(v['title'], v['channel'])
        v['recommended_playlist'] = rec_pl
        
        lines.append(f"<b>{v['num']}.</b> {title_esc}")
        lines.append(f"   ⏱ Длительность: <code>{dur_esc}</code> | Канал: <i>{chan_esc}</i>")
        lines.append(f"   💡 <b>Рекомендация:</b> в <code>{rec_pl}</code>\\n")"""

txt = txt.replace(old_loop, new_loop)

# Update prompt line
old_prompt = "✍️ <b>Ответь мне, что сделать по номерам</b> (например: <i>«1 в Guitar, 2 суммаризируй, 3 в Piano, 4 удалить»</i>). Без твоей команды ничего не трогаю!"
new_prompt = "✍️ <b>Напиши «Да»</b> (или <i>«1 да, 2 в Музыку, 3 удалить»</i>), чтобы я распределил видео по этим рекомендованным плейлистам!"

txt = txt.replace(old_prompt, new_prompt)

open(script_p, "w", encoding="utf-8").write(txt)
print("✅ Updated youtube_playlist_sorter.py with automatic playlist recommendations!")
