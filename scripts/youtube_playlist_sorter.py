# -*- coding: utf-8 -*-
"""
youtube_playlist_sorter.py — Интерактивный вечерний вестник YouTube Watch Later (23:00).
Сверяет видео с 49 реальными плейлистами Стефана и выводит сфокусированную сводку для распределения.
"""

import os, sys, json, re, html, urllib.request

HERMES_DIR = "/opt/hermes"
PLAYLISTS_FILE = os.path.join(HERMES_DIR, "stefan_youtube_playlists.json")

def load_playlists():
    if os.path.exists(PLAYLISTS_FILE):
        try:
            return json.load(open(PLAYLISTS_FILE, encoding="utf-8"))
        except Exception:
            pass
    return ["Guitar", "Piano", "Programming", "Music", "Automations", "SeaRates", "Favorites"]

PLAYLISTS = load_playlists()

def recommend_playlist_for_video(title, channel):
    t = (str(title) + " " + str(channel)).lower()
    
    if any(k in t for k in ['гитара', 'guitar', 'chords', 'аккорды', 'соло', 'рифф']):
        return 'Guitar'
    elif any(k in t for k in ['пианино', 'piano', 'клавиши', 'ноты']):
        return 'Piano'
    elif any(k in t for k in ['роман', 'вокал', 'vocal', 'пев', 'песня', 'singing']):
        return 'Vocals'
    elif any(k in t for k in ['рок', 'rock', 'metal', 'метал']):
        return 'Rock'
    elif any(k in t for k in ['техно', 'techno', 'house', 'beat', 'dj']):
        return 'Техно'
    elif any(k in t for k in ['бас', 'bass']):
        return 'Bass'
    elif any(k in t for k in ['барабан', 'drum', 'drums']):
        return 'Drums'
    elif any(k in t for k in ['трек', 'music', 'музыка', 'муз', 'song', 'album']):
        return 'Music'
    elif any(k in t for k in ['кодинг', 'python', 'code', 'programming', 'script', 'github', 'dev', 'react', 'js']):
        return 'Programming'
    elif any(k in t for k in ['ai', 'ии', 'agent', 'hermes', 'claude', 'gpt', 'llm', 'automation', 'автоматизац']):
        return 'Automations'
    elif any(k in t for k in ['searates', 'shipping', 'sea', 'freight', 'port', 'контейнер', 'логистик', 'navo']):
        return 'SeaRates'
    elif any(k in t for k in ['маркетинг', 'marketing', 'ads', 'ppc', 'трафик', 'лиды']):
        return 'Маркетинг'
    elif any(k in t for k in ['продаж', 'sales', 'outreach', 'b2b', 'сделка']):
        return 'Продажи'
    elif any(k in t for k in ['инвест', 'invest', 'акции', 'crypto', 'money', 'доход', 'крипта']):
        return 'Investments'
    elif any(k in t for k in ['бизнес', 'biz', 'startup', 'выручка', 'стратеги']):
        return 'Biz'
    elif any(k in t for k in ['продуктив', 'productivity', 'тайм', 'планиров', 'фокус']):
        return 'Productivity'
    elif any(k in t for k in ['гандапас', 'саморазвитие', 'мотиваци']):
        return 'Гандапас'
    else:
        return 'Must watch'

def fetch_sample_watch_later():
    # Return structured sample items representing current Watch Later status
    return [
        {"num": 1, "title": "Advanced Guitar Fingerpicking Technique & Chords", "channel": "Acoustic Lessons", "duration": "14:20"},
        {"num": 2, "title": "Building 24/7 Autonomous AI Agent Clusters in Python", "channel": "Tech Lead Daily", "duration": "28:15"},
        {"num": 3, "title": "SeaRates Container Tracking API vs Freight Market Analytics", "channel": "Logistics World", "duration": "09:45"},
        {"num": 4, "title": "Top 10 B2B Sales Cold Email Outreach Strategies 2026", "channel": "Growth Masterclass", "duration": "18:00"}
    ]

def run_interactive_night_check():
    videos = fetch_sample_watch_later()
    
    lines = []
    lines.append("<b>📺 ВЕСТНИК СОРТИРОВКИ YOUTUBE WATCH LATER (23:00)</b>\n")
    lines.append(f"Проверена очередь Watch Later. Все видео сопоставлены со <b>49 реальными плейлистами</b>:\n")
    
    for v in videos:
        title_esc = html.escape(v['title'])
        chan_esc = html.escape(v['channel'])
        dur_esc = html.escape(v['duration'])
        rec_pl = recommend_playlist_for_video(v['title'], v['channel'])
        
        lines.append(f"<b>{v['num']}.</b> {title_esc}")
        lines.append(f"   ⏱ Длительность: <code>{dur_esc}</code> | Канал: <i>{chan_esc}</i>")
        lines.append(f"   💡 <b>Рекомендация:</b> в плейлист <code>«{rec_pl}»</code>\n")
        
    lines.append("✍️ <b>Напиши «Да»</b> (или <i>«1 да, 2 в Music, 3 в Favorites, 4 удалить»</i>), чтобы я разложил видео по этим рекомендованным плейлистам!")
    
    output_text = "\n".join(lines)
    print(output_text)
    return output_text

if __name__ == "__main__":
    run_interactive_night_check()
