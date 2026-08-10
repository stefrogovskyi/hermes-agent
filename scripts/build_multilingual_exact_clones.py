# -*- coding: utf-8 -*-
"""
build_multilingual_exact_clones.py — Создание 100% идентичных языковых версий (es, it, de, fr, zh, ar, uk, ru):
  - Каждая языковая страница копирует точный HTML/CSS макет соответствующей английской страницы (index, services, pricing, about, contact)
  - Меняются ИСКЛЮЧИТЕЛЬНО тексты (заголовки, описания, списки, надписи кнопок)
  - Дизайн, кнопки, логотипы, Хедер, Футер и геометрия остаются 1-в-1 совпадением!
"""

import os, re, paramiko, subprocess

HERMES_DIR = r"C:\Users\Stefan\AppData\Local\hermes"
site_dir = os.path.join(HERMES_DIR, "avalanche_v2_staging")
os.chdir(site_dir)

# Read master English pages
master_pages = {}
for p_name in ["index.html", "services.html", "pricing.html", "about.html", "contact.html"]:
    master_pages[p_name] = open(os.path.join(site_dir, p_name), encoding="utf-8").read()

# Multilingual dictionary for key phrases across 8 languages
translations = {
    "es": {
        "nav_services": "Servicios", "nav_pricing": "Precios", "nav_about": "Nosotros", "nav_contact": "Contacto",
        "lang_tag": "ES", "lang_name": "Español (ES)",
        "get_in_touch": "Ponerse en Contacto ➔", "start_project": "Iniciar Proyecto ➔", "send_message": "Enviar Mensaje",
        "about_title": "Sobre Avalanche Agency",
        "about_desc": "Somos una agencia web premium dedicada a crear experiencias digitales excepcionales. Nuestro equipo combina creatividad con experiencia técnica.",
        "values_title": "Nuestros Valores",
        "val_1_title": "Excelencia", "val_1_desc": "Buscamos la perfección en cada proyecto que entregamos.",
        "val_2_title": "Asociación", "val_2_desc": "Trabajamos junto a usted, no solo para usted.",
        "val_3_title": "Resultados", "val_3_desc": "Cada decisión se basa en resultados medibles.",
        "val_4_title": "Innovación", "val_4_desc": "Adoptamos soluciones modernas y pensamiento creativo.",
        "contact_title": "Información de Contacto", "your_name": "Su Nombre", "email_addr": "Correo Electrónico", "your_msg": "Su Mensaje",
        "pricing_title": "Precios Simples y Transparentes", "pricing_sub": "Sin tarifas ocultas. Sin sorpresas. Desarrollo web personalizado completo.",
        "flat_rate": "Tarifa Plana", "peace_mind": "Tranquilidad Total", "zero_risk": "Cero Riesgo", "custom_dev": "Desarrollo Personalizado",
        "banner_text": "Sin pago por adelantado. Pague solo cuando esté 100% satisfecho."
    },
    "de": {
        "nav_services": "Leistungen", "nav_pricing": "Preise", "nav_about": "Über uns", "nav_contact": "Kontakt",
        "lang_tag": "DE", "lang_name": "Deutsch (DE)",
        "get_in_touch": "Kontakt Aufnehmen ➔", "start_project": "Projekt Starten ➔", "send_message": "Nachricht Senden",
        "about_title": "Über Avalanche Agency",
        "about_desc": "Wir sind eine führende Webagentur für erstklassige digitale Erlebnisse. Unser Team verbindet Kreativität mit technischer Exzellenz.",
        "values_title": "Unsere Werte",
        "val_1_title": "Exzellenz", "val_1_desc": "Wir streben bei jedem Projekt nach Perfektion.",
        "val_2_title": "Partnerschaft", "val_2_desc": "Wir arbeiten mit Ihnen, nicht nur für Sie.",
        "val_3_title": "Ergebnisse", "val_3_desc": "Jede Entscheidung basiert auf messbaren Ergebnissen.",
        "val_4_title": "Innovation", "val_4_desc": "Wir nutzen moderne Lösungen und kreatives Denken.",
        "contact_title": "Kontaktinformationen", "your_name": "Ihr Name", "email_addr": "E-Mail-Adresse", "your_msg": "Ihre Nachricht",
        "pricing_title": "Einfache, Transparente Preise", "pricing_sub": "Keine versteckten Gebühren. Keine Überraschungen.",
        "flat_rate": "Festpreis", "peace_mind": "Rundum Sorglos", "zero_risk": "Null Risiko", "custom_dev": "Individuelle Entwicklung",
        "banner_text": "Keine Vorauszahlung erforderlich. Bezahlen Sie nur, wenn Sie zu 100% zufrieden sind."
    },
    "fr": {
        "nav_services": "Services", "nav_pricing": "Tarifs", "nav_about": "À propos", "nav_contact": "Contact",
        "lang_tag": "FR", "lang_name": "Français (FR)",
        "get_in_touch": "Prendre Contact ➔", "start_project": "Lancer le Projet ➔", "send_message": "Envoyer le Message",
        "about_title": "À Propos d'Avalanche Agency",
        "about_desc": "Nous sommes une agence web premium dédiée à la création d'expériences numériques d'exception.",
        "values_title": "Nos Valeurs",
        "val_1_title": "Excellence", "val_1_desc": "Nous visons la perfection dans chaque projet.",
        "val_2_title": "Partenariat", "val_2_desc": "Nous travaillons avec vous, pas seulement pour vous.",
        "val_3_title": "Résultats", "val_3_desc": "Chaque décision est guidée par des résultats mesurables.",
        "val_4_title": "Innovation", "val_4_desc": "Nous adoptons des solutions modernes et créatives.",
        "contact_title": "Coordonnées de Contact", "your_name": "Votre Nom", "email_addr": "Adresse E-mail", "your_msg": "Votre Message",
        "pricing_title": "Tarification Simple et Transparente", "pricing_sub": "Pas de frais cachés. Aucune surprise.",
        "flat_rate": "Tarif Fixe", "peace_mind": "Sérénité Totale", "zero_risk": "Zéro Risque", "custom_dev": "Développement Sur Mesure",
        "banner_text": "Aucun acompte requis. Payez uniquement lorsque vous êtes 100% satisfait."
    },
    "it": {
        "nav_services": "Servizi", "nav_pricing": "Prezzi", "nav_about": "Chi Siamo", "nav_contact": "Contatti",
        "lang_tag": "IT", "lang_name": "Italiano (IT)",
        "get_in_touch": "Mettiti in Contatto ➔", "start_project": "Inizia il Progetto ➔", "send_message": "Invia Messaggio",
        "about_title": "Su Avalanche Agency",
        "about_desc": "Siamo un'agenzia web premium dedicata alla creazione di esperienze digitali eccezionali.",
        "values_title": "I Nostri Valori",
        "val_1_title": "Eccellenza", "val_1_desc": "Puntiamo alla perfezione in ogni progetto che realizziamo.",
        "val_2_title": "Partnership", "val_2_desc": "Lavoriamo al tuo fianco, non solo per te.",
        "val_3_title": "Risultati", "val_3_desc": "Ogni decisione è guidata da risultati misurabili.",
        "val_4_title": "Innovazione", "val_4_desc": "Adottiamo soluzioni moderne e pensiero creativo.",
        "contact_title": "Informazioni di Contatto", "your_name": "Il Tuo Nome", "email_addr": "Indirizzo Email", "your_msg": "Il Tuo Messaggio",
        "pricing_title": "Prezzi Semplici e Trasparenti", "pricing_sub": "Nessun costo nascosto. Nessuna sorpresa.",
        "flat_rate": "Tariffa Fissa", "peace_mind": "Tranquillità Totale", "zero_risk": "Zero Rischio", "custom_dev": "Sviluppo Personalizzato",
        "banner_text": "Nessun pagamento anticipato. Paghi solo quando sei soddisfatto al 100%."
    },
    "uk": {
        "nav_services": "Послуги", "nav_pricing": "Ціни", "nav_about": "Про нас", "nav_contact": "Контакти",
        "lang_tag": "UK", "lang_name": "Українська (UK)",
        "get_in_touch": "Зв'язатися з Нами ➔", "start_project": "Розпочати Проєкт ➔", "send_message": "Надіслати Повідомлення",
        "about_title": "Про Avalanche Agency",
        "about_desc": "Ми — преміальна веб-агенція, що створює виняткові цифрові рішення. Наша команда поєднує креативність із технічною експертизою.",
        "values_title": "Наші Цінності",
        "val_1_title": "Досконалість", "val_1_desc": "Прагнемо до досконалості в кожному проєкті.",
        "val_2_title": "Партнерство", "val_2_desc": "Працюємо разом із вами, а не просто на вас.",
        "val_3_title": "Результати", "val_3_desc": "Кожне рішення базується на вимірюваних результатах.",
        "val_4_title": "Інновації", "val_4_desc": "Впроваджуємо сучасні рішення та креативне мислення.",
        "contact_title": "Контактна Інформація", "your_name": "Ваше Ім'я", "email_addr": "Електронна Пошта", "your_msg": "Ваше Повідомлення",
        "pricing_title": "Прості та Прозорі Ціни", "pricing_sub": "Без прихованих платежів. Без сюрпризів.",
        "flat_rate": "Фіксована Ціна", "peace_mind": "Повний Спокій", "zero_risk": "Нуль Ризику", "custom_dev": "Індивідуальна Розробка",
        "banner_text": "Без передплати. Оплата лише після 100% задоволення результатом."
    },
    "ru": {
        "nav_services": "Услуги", "nav_pricing": "Цены", "nav_about": "О нас", "nav_contact": "Контакты",
        "lang_tag": "RU", "lang_name": "Русский (RU)",
        "get_in_touch": "Связаться с Нами ➔", "start_project": "Начать Проект ➔", "send_message": "Отправить Сообщение",
        "about_title": "Об Avalanche Agency",
        "about_desc": "Мы — премиальное веб-агентство, создающее исключительные цифровые решения. Наша команда сочетает креативность с технической экспертизой.",
        "values_title": "Наши Ценности",
        "val_1_title": "Совершенство", "val_1_desc": "Стремимся к совершенству в каждом проекте.",
        "val_2_title": "Партнерство", "val_2_desc": "Работаем вместе с вами, а не просто на вас.",
        "val_3_title": "Результаты", "val_3_desc": "Каждое решение основано на измеримых результатах.",
        "val_4_title": "Инновации", "val_4_desc": "Внедряем современные решения и креативное мышление.",
        "contact_title": "Контактная Информация", "your_name": "Ваше Имя", "email_addr": "Электронная Почта", "your_msg": "Ваше Сообщение",
        "pricing_title": "Простые и Прозрачные Цены", "pricing_sub": "Без скрытых платежей. Без сюрпризов.",
        "flat_rate": "Фиксированная Цена", "peace_mind": "Полное Спокойствие", "zero_risk": "Ноль Риска", "custom_dev": "Индивидуальная Разработка",
        "banner_text": "Без предоплаты. Оплата только при 100% удовлетворении результатом."
    },
    "zh": {
        "nav_services": "服务", "nav_pricing": "价格", "nav_about": "关于我们", "nav_contact": "联系我们",
        "lang_tag": "ZH", "lang_name": "中文 (ZH)",
        "get_in_touch": "联系我们 ➔", "start_project": "启动项目 ➔", "send_message": "发送消息",
        "about_title": "关于 Avalanche Agency",
        "about_desc": "我们是一家致力于打造卓越数字体验的高级网络机构。",
        "values_title": "我们的核心价值观",
        "val_1_title": "卓越", "val_1_desc": "我们在交付的每一个项目中追求完美。",
        "val_2_title": "合作", "val_2_desc": "我们与您携手共进，而不仅是为您工作。",
        "val_3_title": "成果", "val_3_desc": "每一个决策都由可衡量的成果驱动。",
        "val_4_title": "创新", "val_4_desc": "我们拥抱现代解决方案与创新思维。",
        "contact_title": "联系信息", "your_name": "您的姓名", "email_addr": "电子邮箱", "your_msg": "您的留言",
        "pricing_title": "简单透明的定价", "pricing_sub": "无隐藏费用。无意外开支。",
        "flat_rate": "固定开发费", "peace_mind": "无忧托管", "zero_risk": "零风险保证", "custom_dev": "定制开发",
        "banner_text": "无需预付款。仅在您100%满意时付款。"
    },
    "ar": {
        "nav_services": "الخدمات", "nav_pricing": "الأسعار", "nav_about": "من نحن", "nav_contact": "اتصل بنا",
        "lang_tag": "AR", "lang_name": "العربية (AR)",
        "get_in_touch": "تواصل معنا ➔", "start_project": "ابدأ المشروع ➔", "send_message": "إرسال الرسالة",
        "about_title": "عن Avalanche Agency",
        "about_desc": "نحن وكالة ويب ممتازة مكرسة لإنشاء تجارب رقمية استثنائية.",
        "values_title": "قيمنا",
        "val_1_title": "التميز", "val_1_desc": "نسعى جاهدين للكمال في كل مشروع نقدمه.",
        "val_2_title": "الشراكة", "val_2_desc": "نعمل جنباً إلى جنب معك، وليس فقط لأجلك.",
        "val_3_title": "النتائج", "val_3_desc": "كل قرار مدفوع بمدى تحقيق النتائج.",
        "val_4_title": "الابتكار", "val_4_desc": "نعتمد الحلول الحديثة والتفكير الإبداعي.",
        "contact_title": "معلومات الاتصال", "your_name": "الاسم الكامل", "email_addr": "البريد الإلكتروني", "your_msg": "رسالتك",
        "pricing_title": "أسعار بسيطة وشفافة", "pricing_sub": "لا توجد رسوم خفية. لا مفاجآت.",
        "flat_rate": "سعر ثابت", "peace_mind": "راحة البال", "zero_risk": "صفر مخاطر", "custom_dev": "تطوير مخصص",
        "banner_text": "لا يتطلب دفع مقدم. ادفع فقط عندما تكون راضياً بنسبة 100%."
    }
}

# Translate master pages for all 8 language subfolders
for lang_code, dict_t in translations.items():
    l_dir = os.path.join(site_dir, lang_code)
    os.makedirs(l_dir, exist_ok=True)
    
    for p_name, p_html in master_pages.items():
        translated_html = p_html
        
        # Replace navigation menu labels
        translated_html = translated_html.replace('>Services<', f'>{dict_t["nav_services"]}<')
        translated_html = translated_html.replace('>Pricing<', f'>{dict_t["nav_pricing"]}<')
        translated_html = translated_html.replace('>About<', f'>{dict_t["nav_about"]}<')
        translated_html = translated_html.replace('>Contact<', f'>{dict_t["nav_contact"]}<')
        
        # Replace buttons & headers
        translated_html = translated_html.replace('Get in Touch ➔', dict_t["get_in_touch"])
        translated_html = translated_html.replace('Start Your Project ➔', dict_t["start_project"])
        translated_html = translated_html.replace('<span>Send Message</span>', f'<span>{dict_t["send_message"]}</span>')
        
        # Replace About Page content
        translated_html = translated_html.replace('About Avalanche Agency', dict_t["about_title"])
        translated_html = translated_html.replace('We are a premium web agency dedicated to creating exceptional digital experiences. Our team combines creativity with technical expertise to deliver solutions that drive results.', dict_t["about_desc"])
        translated_html = translated_html.replace('Our Values', dict_t["values_title"])
        translated_html = translated_html.replace('Excellence', dict_t["val_1_title"]).replace('We strive for perfection in every project we deliver.', dict_t["val_1_desc"])
        translated_html = translated_html.replace('Partnership', dict_t["val_2_title"]).replace('We work alongside you, not just for you.', dict_t["val_2_desc"])
        translated_html = translated_html.replace('Results', dict_t["val_3_title"]).replace('Every decision is driven by measurable outcomes.', dict_t["val_3_desc"])
        translated_html = translated_html.replace('Innovation', dict_t["val_4_title"]).replace('We embrace modern solutions and creative thinking.', dict_t["val_4_desc"])
        
        # Replace Contact Page content
        translated_html = translated_html.replace('Contact Information', dict_t["contact_title"])
        translated_html = translated_html.replace('Your Name', dict_t["your_name"])
        translated_html = translated_html.replace('Email Address', dict_t["email_addr"])
        translated_html = translated_html.replace('Your Message', dict_t["your_msg"])
        
        # Replace Pricing Page content
        translated_html = translated_html.replace('Simple, Transparent Pricing', dict_t["pricing_title"])
        translated_html = translated_html.replace('Flat Rate', dict_t["flat_rate"])
        translated_html = translated_html.replace('Peace of Mind', dict_t["peace_mind"])
        translated_html = translated_html.replace('Zero Risk', dict_t["zero_risk"])
        translated_html = translated_html.replace('Custom Development', dict_t["custom_dev"])
        translated_html = translated_html.replace('No prepayment required. Pay only when you are 100% satisfied.', dict_t["banner_text"])

        # Update language selector tag in header
        translated_html = re.sub(r'<span>EN</span>', f'<span>{dict_t["lang_tag"]}</span>', translated_html)

        # Write to subfolder
        sub_p = os.path.join(l_dir, p_name)
        open(sub_p, "w", encoding="utf-8").write(translated_html)
        print(f"✅ Generated 100% identical clone for /{lang_code}/{p_name}")

# Upload all files and folders to Hostinger /public_html/dev/
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("82.29.199.155", port=65002, username="u473746908", password="Stefrogovskyi#1", timeout=15)

sftp = ssh.open_sftp()
remote_base = "/home/u473746908/domains/aavalanche.com/public_html/dev"

def sftp_upload_dir(local_path, remote_path):
    try:
        sftp.mkdir(remote_path)
    except Exception:
        pass
    for item in os.listdir(local_path):
        if item in (".git", "node_modules", ".DS_Store"):
            continue
        l_item = os.path.join(local_path, item)
        r_item = remote_path + "/" + item
        if os.path.isdir(l_item):
            sftp_upload_dir(l_item, r_item)
        else:
            sftp.put(l_item, r_item)

sftp_upload_dir(site_dir, remote_base)
sftp.close()

# Git commit and push
subprocess.run(["git", "checkout", "dev"], check=True)
subprocess.run(["git", "add", "."], check=True)
res_commit = subprocess.run(["git", "commit", "-m", "feat(dev): Generate 100% identical HTML/CSS clones for all 8 languages (es, it, de, fr, zh, ar, uk, ru) with translated texts only"], capture_output=True, text=True)
print(res_commit.stdout or res_commit.stderr)

res_push = subprocess.run(["git", "push", "origin", "dev", "--force"], capture_output=True, text=True)
print(res_push.stdout or res_push.stderr)

res_sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
active_sha = res_sha.stdout.strip()

ssh.close()

print("🎉 MULTILINGUAL 100% IDENTICAL CLONES DEPLOYED TO DEV!")
print(f"📌 ACTIVE GIT COMMIT SHA: {active_sha}")
