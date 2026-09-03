#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
send_weekly_sales_testimonial_reminder.py — Richard Marlowe (Navo24)
Weekly Monday morning email reminder to individual Sales Team members:
- alyona.holubova@navo24.com (Алёна)
- ekaterina.kapustian@navo24.com (Екатерина)
- lilia.k@navo24.com (Лилия)
- nikita@navo24.com (Никита)
- oleg.chervinskyi@navo24.com (Олег)

CC: stefan@navo24.com, lxxmng@navo24.com
Addressed personally to each team member by first name.
"""

import os
import sys
import json
import random
import requests
from datetime import datetime, timezone

RESEND_API_KEY = os.getenv("RESEND_API_KEY", "re_HYSmY1vz_JDgFN8YzffnTeT6mR2YnSufo")

SALES_TEAM = [
    {"first_name": "Алёна", "full_name": "Алёна Голубова", "email": "alyona.holubova@navo24.com"},
    {"first_name": "Екатерина", "full_name": "Екатерина Капустян", "email": "ekaterina.kapustian@navo24.com"},
    {"first_name": "Лилия", "full_name": "Лилия", "email": "lilia.k@navo24.com"},
    {"first_name": "Никита", "full_name": "Никита", "email": "nikita@navo24.com"},
    {"first_name": "Олег", "full_name": "Олег Червинский", "email": "oleg.chervinskyi@navo24.com"},
]

QUOTES = [
    (
        "«Требуется 20 лет, чтобы создать репутацию, и 5 минут, чтобы ее разрушить. Если вы подумаете об этом, вы будете делать все по-другому. Лучшая реклама — это искренний голос довольного клиента.»",
        "Уоррен Баффет"
    ),
    (
        "«Если вы сделаете клиента несчастным в реальном мире, он расскажет 6 друзьям. Если вы сделаете его счастливым в цифровом мире — он расскажет 6 000 человек. Превращайте благодарность клиентов в наше главное оружие.»",
        "Джефф Безос"
    ),
    (
        "«Ваш самый недовольный клиент — это ваш лучший источник обучения, а ваш самый благодарный клиент — это ваш лучший менеджер по продажам.»",
        "Билл Гейтс"
    ),
    (
        "«Люди не покупают товары и услуги. Они покупают отношения, истории и магию надежности. Когда клиент говорит „спасибо“, это лучший момент зафиксировать эту магию на видео или письмом.»",
        "Сет Годин"
    ),
    (
        "«Вы можете получить в жизни все, что хотите, если просто поможете достаточному количеству других людей получить то, чего хотят они. Довольный клиент — это подтверждение выполненной миссии.»",
        "Зиг Зиглар"
    ),
    (
        "«Превосходный сервис — это не случайность, а системная привычка. Спросите себя прямо сейчас: кто из клиентов недавно почувствовал нашу настоящую заботу?»",
        "Рон Кауфман"
    ),
    (
        "«Сделайте клиента главным героем вашей общей истории. Когда клиент побеждает благодаря вашему продукту — его отзыв вдохновляет сотни новых партнеров.»",
        "Дональд Миллер"
    ),
    (
        "«Продажи — это не навязывание, а построение доверительных мостов. А самый прочный кирпич в этом мосту — реальный отзыв человека, который уже получил результат.»",
        "Брайан Трейси"
    )
]

TRIGGER_POOL = [
    # Общие впечатления и партнерство
    "Кто из твоих клиентов недавно искренне поблагодарил за простоту работы, вежливое общение или быстрый человеческий сервис?",
    "Кто из пользователей отметил, насколько наша платформа сэкономила время их операционной команды и логистов?",
    "С кем из партнеров у тебя сложились теплые отношения после плавного перехода со старых громоздких платформ?",
    
    # Служба заботы и поддержка
    "Кто недавно оценил молниеносную реакцию в духе «Стоп... вы уже всё починили?!»?",
    "Кому из клиентов мы помогли решить нестандартную техническую задачу или сложный кейс без бюрократии?",
    
    # Качество данных и Tracking
    "Кто из твоих клиентов недавно хвалил глубину и точность трекинга по 234 морским линиям или DCSA-событиям?",
    "Какой клиент недавно избежал непредвиденных расходов на демередж и детеншен (D&D) благодаря нашим честным наблюдаемым ETA?",
    "Кто отметил удобство живой карты AIS с отображением реального положения судов в море?",
    
    # Schedules & Routes
    "Кто из экспедиторов остался доволен поиском надежных расписаний по 255 портам и 72 000+ рейсов?",
    "Кому модуль расписаний помог спланировать оптимальную цепочку поставок и избежать задержек в хабах?",
    
    # FreightRates & Прозрачность ставок
    "Кто из импортеров или торговых домов отметил честность и прозрачность спот-ставок ex-Asia (без заманух и скрытых наценок)?",
    "Кому из клиентов ежедневные тренды фрахтовых ставок помогли выгодно договориться о букинге?",
    
    # Loading 3D & Оптимизация загрузки
    "Кто из пользователей 3D калькулятора загрузки контейнеров поделился восторгом от наглядности укладки по CTU Code?",
    "Кому наш 3D-модуль помог компактно упаковать сборный груз и сэкономить на заказе лишнего контейнера?",
    
    # AirTracking
    "Кто из мультимодальных экспедиторов оценил трекинг авиагрузов по AWB в едином окне с морскими перевозками?",
    
    # Разработчики, API & MCP
    "Кто из IT-специалистов или CTO похвалил легкость интеграции нашего REST API / Webhooks?",
    "Кто из AI-энтузиастов подключил наши MCP-серверы к Claude / Cursor / n8n и оценил работу автономных агентов?",
    "Кто из пользователей бесплатного Free Tier (5 контейнеров / 100 вызовов) уже готов перейти на полноценный тариф?"
]

def generate_email_content(member, week_num, quote_text, quote_author, selected_triggers):
    subject = f"🌟 {member['first_name']}, сейлз-фокус недели: Собираем отзывы и истории успеха наших клиентов"
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"></head>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.6; color: #1e293b; margin: 0; padding: 20px; background-color: #ffffff;">
        <div style="max-width: 620px; margin: 0 auto; text-align: left;">
            <p style="font-size: 17px; font-weight: 700; color: #0A2540; margin-bottom: 12px;">
                Доброе утро, {member['first_name']}! 🚀
            </p>
            
            <p>
                Понедельник — отличное время не только для открытия новых сделок, но и для превращения твоих довольных клиентов в наше главное конкурентное оружие: <b>публичные отзывы (testimonials), кейсы и искренние рекомендации</b>.
            </p>
            
            <div style="background-color: #f8fafc; border-left: 4px solid #2060DF; padding: 14px 18px; margin: 18px 0; border-radius: 4px;">
                <p style="margin: 0; font-style: italic; color: #334155; font-size: 14.5px;">
                    {quote_text}
                </p>
                <p style="margin: 6px 0 0 0; font-weight: 600; font-size: 13px; color: #64748b;">
                    — {quote_author}
                </p>
            </div>
            
            <p style="font-weight: 600; color: #0A2540; margin-top: 18px; margin-bottom: 8px;">
                🎯 Вспомни, кто из твоих клиентов недавно получил отличный опыт:
            </p>
            <ul style="padding-left: 20px; margin-top: 0; color: #334155;">
                <li style="margin-bottom: 6px;">{selected_triggers[0]}</li>
                <li style="margin-bottom: 6px;">{selected_triggers[1]}</li>
                <li style="margin-bottom: 6px;">{selected_triggers[2]}</li>
                <li style="margin-bottom: 6px;">Кто из твоих контактов готов дать короткий комментарий для navo24.com или записать 30-секундное видео?</li>
            </ul>
            
            <p style="font-weight: 600; color: #0A2540; margin-top: 18px; margin-bottom: 8px;">
                💡 Простой скрипт обращения к клиенту:
            </p>
            <div style="background-color: #ffffff; border: 1px solid #e2e8f0; padding: 12px 16px; border-radius: 6px; font-size: 13.5px; color: #475569;">
                <i>«[Имя], спасибо за доверие и отличную совместную работу! Мы сейчас обновляем блок отзывов и историй успеха на navo24.com. Будем невероятно признательны, если сможешь черкнуть 2–3 предложения о твоем опыте работы с Navo24 (качестве данных, сервисе, точности расписаний или удобстве платформы) либо записать короткое видео. Могу ли я подготовить для тебя черновик отзыва на согласование?»</i>
            </div>
            
            <p style="margin-top: 20px;">
                Давай на этой неделе превратим минимум <b>1–2 довольных клиентов</b> в мощные социальные доказательства нашего качества!
            </p>
            
            <p style="margin-top: 24px; color: #64748b; font-size: 13.5px; border-top: 1px solid #e2e8f0; padding-top: 12px;">
                С уважением и отличной продуктивной недели,<br>
                <b>Richard Marlowe</b><br>
                Connections & Sales Operations | Navo24
            </p>
        </div>
    </body>
    </html>
    """
    return subject, html

def send_all_reminders():
    week_num = datetime.now(timezone.utc).isocalendar()[1]
    quote_text, quote_author = random.choice(QUOTES)
    selected_triggers = random.sample(TRIGGER_POOL, 3)
    
    sent_count = 0
    results = []
    
    for member in SALES_TEAM:
        subject, html_body = generate_email_content(member, week_num, quote_text, quote_author, selected_triggers)
        to_address = f"{member['full_name']} <{member['email']}>"
        
        payload = {
            "from": "Richard Marlowe <rich@e.navo24.com>",
            "to": [to_address],
            "cc": ["Stefan Rogovskiy <stefan@navo24.com>", "Alexei Shatunov <lxxmng@navo24.com>"],
            "reply_to": "sales@navo24.com",
            "subject": subject,
            "html": html_body
        }
        
        try:
            r = requests.post(
                "https://api.resend.com/emails",
                headers={"Authorization": f"Bearer {RESEND_API_KEY}", "Content-Type": "application/json"},
                json=payload,
                timeout=15
            )
            if r.status_code == 200:
                res_id = r.json().get("id")
                results.append(f"✅ {member['first_name']} ({member['email']}) -> Resend ID: {res_id}")
                sent_count += 1
            else:
                results.append(f"❌ {member['first_name']} ({member['email']}) -> HTTP {r.status_code}: {r.text}")
        except Exception as e:
            results.append(f"❌ {member['first_name']} ({member['email']}) -> Exception: {e}")
            
    print(f"[{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}] ✉️ Weekly Sales Testimonials Reminder (Individual Delivery): {sent_count}/{len(SALES_TEAM)} sent successfully.")
    for res in results:
        print(f"  {res}")

if __name__ == "__main__":
    send_all_reminders()
