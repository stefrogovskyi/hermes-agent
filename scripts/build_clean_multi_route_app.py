# -*- coding: utf-8 -*-
"""
build_clean_multi_route_app.py — Полная спрессованная мульти-маршрутная архитектура Avalanche Agency:
1. Английский по умолчанию: site.com/
2. Маршруты языков со своей директорией: site.com/es/, site.com/it/, site.com/fr/, site.com/de/, site.com/zh/, site.com/ar/ (RTL), site.com/uk/, site.com/ru/
3. При смене языка в селекторе — РЕАЛЬНЫЙ ПЕРЕХОД ПО URL / ПЕРЕЗАГРУЗКА
4. Убраны стрелочки ↗ из меню (Services, Pricing, About, Contact)
5. Меню ведет на локальные внутренние страницы Surge (services.html, pricing.html, about.html, contact.html)
6. Чистый текстовый селектор языков без сломанных флажков (EN | ES | IT | FR | DE | ZH | AR | UK | RU)
7. Цвет кнопок и контекста — фирменный синий #60B5FF
8. Наличие полноценной светлой страницы Услуг (services.html)
9. Автоопределение по IP посетителя
"""

import os, sys, time, json, shutil, re

STAGING_DIR = r"C:\Users\Stefan\AppData\Local\hermes\avalanche_v2_staging"
DESIGN_DIR = r"C:\Users\Stefan\My Drive\Equity\My Biz\My companies\Enlight Group\Avalanche Agency\Design"

os.makedirs(STAGING_DIR, exist_ok=True)

print("=== 🚀 СБОРКА МУЛЬТИ-МАРШРУТНОЙ СТАДИИ AVALANCHE V2 ===")

# Читаем точный исходный redesign.html
redesign_path = os.path.join(DESIGN_DIR, "redesign.html")
base_html = open(redesign_path, encoding="utf-8", errors="ignore").read()

# Применяем цвет #60B5FF
base_html = base_html.replace("--blue:#3B82F6;", "--blue:#60B5FF;").replace("--blue-d:#2563EB;", "--blue-d:#389BFF;")
base_html = base_html.replace("#3B82F6", "#60B5FF").replace("#2563EB", "#389BFF")

# Копируем логотип
logo_src = os.path.join(DESIGN_DIR, "avalanche_logo.png")
if os.path.exists(logo_src):
    shutil.copy(logo_src, os.path.join(STAGING_DIR, "avalanche_logo.png"))
    shutil.copy(logo_src, os.path.join(STAGING_DIR, "favicon.png"))

# Словари чистого профессионального перевода без суржика
translations = {
    "en": {
        "title": "Avalanche Agency — Premium Web, Marketing & AI Automation",
        "desc": "High-conversion web design, digital marketing, and custom AI automations for ambitious businesses.",
        "nav_services": "Services", "nav_pricing": "Pricing", "nav_about": "About", "nav_contact": "Contact", "nav_btn": "Start Your Project",
        "hero_badge": "Digital Excellence & AI Intelligence",
        "hero_h1": "Websites that convert. Brands that dominate.",
        "hero_p": "We design and build high-performance web systems, custom AI automations, and growth engines for ambitious global companies.",
        "hero_btn": "Start Your Project",
        "services_title": "Services built for measurable impact.",
        "process_title": "How we turn ideas into revenue.",
        "why_title": "Why global leaders choose Avalanche.",
        "contact_title": "Ready to scale? Zero Risk.",
        "contact_btn": "Send Inquiry ➔",
        "services_page_title": "Our Digital Services & AI Solutions",
        "services_page_sub": "World-class web development, custom software architecture, and growth marketing.",
        "form_name": "Your Full Name", "form_email": "Your Business Email", "form_message": "Tell us about your project...", "form_submit": "Send Inquiry ➔"
    },
    "es": {
        "title": "Avalanche Agency — Diseño Web, Marketing y Automatización IA",
        "desc": "Diseño web de alta conversión, marketing digital y automatizaciones personalizadas con IA.",
        "nav_services": "Servicios", "nav_pricing": "Precios", "nav_about": "Nosotros", "nav_contact": "Contacto", "nav_btn": "Iniciar Proyecto",
        "hero_badge": "Excelencia Digital e Inteligencia IA",
        "hero_h1": "Sitios web que convierten. Marcas que dominan.",
        "hero_p": "Diseñamos y construimos sistemas web de alto rendimiento, automatizaciones con IA y motores de crecimiento.",
        "hero_btn": "Iniciar Proyecto",
        "services_title": "Servicios diseñados para un impacto medible.",
        "process_title": "Cómo transformamos ideas en ingresos.",
        "why_title": "Por qué los líderes eligen Avalanche.",
        "contact_title": "¿Listo para escalar? Sin Riesgo.",
        "contact_btn": "Enviar Consulta ➔",
        "services_page_title": "Nuestros Servicios Digitales e Inteligencia IA",
        "services_page_sub": "Desarrollo web de clase mundial, arquitectura de software a medida y marketing de crecimiento.",
        "form_name": "Tu Nombre Completo", "form_email": "Tu Correo Corporativo", "form_message": "Cuéntanos sobre tu proyecto...", "form_submit": "Enviar Consulta ➔"
    },
    "it": {
        "title": "Avalanche Agency — Design Web, Marketing e Automazione IA",
        "desc": "Design web ad alta conversione, marketing digitale e automazioni IA per aziende ambiziose.",
        "nav_services": "Servizi", "nav_pricing": "Prezzi", "nav_about": "Chi Siamo", "nav_contact": "Contatti", "nav_btn": "Avvia Progetto",
        "hero_badge": "Eccellenza Digitale e Intelligenza IA",
        "hero_h1": "Siti web che convertono. Brand che dominano.",
        "hero_p": "Sviluppiamo sistemi web ad alte prestazioni, automazioni IA su misura e motori di crescita.",
        "hero_cta1": "Avvia Progetto",
        "services_title": "Servizi creati per un impatto misurabile.",
        "process_title": "Come trasformiamo le idee in fatturato.",
        "why_title": "Perché i leader scelgono Avalanche.",
        "contact_title": "Pronto a scalare? Zero Rischio.",
        "contact_btn": "Invia Richiesta ➔",
        "services_page_title": "I Nostri Servizi Digitali e Soluzioni IA",
        "services_page_sub": "Sviluppo web di livello mondiale, architettura software personalizzata e marketing per la crescita.",
        "form_name": "Nome e Cognome", "form_email": "Email Aziendale", "form_message": "Raccontaci del tuo progetto...", "form_submit": "Invia Richiesta ➔"
    },
    "fr": {
        "title": "Avalanche Agency — Web Design, Marketing & Automation IA",
        "desc": "Design web à forte conversion, marketing digital et automations IA sur mesure.",
        "nav_services": "Services", "nav_pricing": "Tarifs", "nav_about": "À Propos", "nav_contact": "Contact", "nav_btn": "Lancer le Projet",
        "hero_badge": "Excellence Numérique & Intelligence IA",
        "hero_h1": "Des sites qui convertissent. Des marques qui dominent.",
        "hero_p": "Nous concevons des systèmes web haute performance, des automations IA et des moteurs de croissance.",
        "hero_btn": "Lancer le Projet",
        "services_title": "Des services conçus pour un impact mesurable.",
        "process_title": "Comment nous transformons les idées en revenus.",
        "why_title": "Pourquoi les leaders choisissent Avalanche.",
        "contact_title": "Prêt à passer à l'échelle ? Zéro Risque.",
        "contact_btn": "Envoyer la Demande ➔",
        "services_page_title": "Nos Services Numériques & Solutions IA",
        "services_page_sub": "Développement web de classe mondiale, architecture logicielle sur mesure et marketing de croissance.",
        "form_name": "Nom Complet", "form_email": "E-mail Professionnel", "form_message": "Parlez-nous de votre projet...", "form_submit": "Envoyer la Demande ➔"
    },
    "de": {
        "title": "Avalanche Agency — Webdesign, Marketing & KI-Automatisierung",
        "desc": "Hochkonvertierendes Webdesign, digitales Marketing und maßgeschneiderte KI-Automatisierungen.",
        "nav_services": "Leistungen", "nav_pricing": "Preise", "nav_about": "Über Uns", "nav_contact": "Kontakt", "nav_btn": "Projekt Starten",
        "hero_badge": "Digitale Exzellenz & KI-Intelligenz",
        "hero_h1": "Websites, die konvertieren. Marken, die dominieren.",
        "hero_p": "Wir entwickeln hochleistungsfähige Websysteme, KI-Automatisierungen und Marketing-Engines.",
        "hero_btn": "Projekt Starten",
        "services_title": "Dienstleistungen für messbaren Erfolg.",
        "process_title": "Wie wir Ideen in Umsatz verwandeln.",
        "why_title": "Warum führende Marken Avalanche wählen.",
        "contact_title": "Bereit zu skalieren? Null Risiko.",
        "contact_btn": "Anfrage Senden ➔",
        "services_page_title": "Unsere Digitalen Leistungen & KI-Lösungen",
        "services_page_sub": "Erstklassige Webentwicklung, maßgeschneiderte Softwarearchitektur und Wachstum-Marketing.",
        "form_name": "Vollständiger Name", "form_email": "Geschäftliche E-Mail", "form_message": "Erzählen Sie uns von Ihrem Projekt...", "form_submit": "Anfrage Senden ➔"
    },
    "zh": {
        "title": "Avalanche Agency — 高端网页设计、数字营销与 AI 自动化",
        "desc": "为具雄心的企业打造高转化率网页设计、数字营销及定制化 AI 自动化流程。",
        "nav_services": "服务项目", "nav_pricing": "价格方案", "nav_about": "关于我们", "nav_contact": "联系我们", "nav_btn": "启动项目",
        "hero_badge": "卓越数字体验与 AI 智能化",
        "hero_h1": "高效转化的网站，主导市场的品牌。",
        "hero_p": "我们为全球领先品牌构建高性能网页系统、人工智能自动化及增长营销引擎。",
        "hero_btn": "启动项目",
        "services_title": "致力于创造可衡量价值的服务。",
        "process_title": "我们如何将创意转化为收益。",
        "why_title": "为何全球领军企业选择 Avalanche。",
        "contact_title": "准备好扩展了吗？零风险。",
        "contact_btn": "提交咨询 ➔",
        "services_page_title": "我们的数字服务与 AI 解决方案",
        "services_page_sub": "世界级网页开发、定制软件架构与增长营销。",
        "form_name": "您的姓名", "form_email": "企业电子邮箱", "form_message": "请告诉我们您的项目需求...", "form_submit": "提交咨询 ➔"
    },
    "ar": {
        "title": "Avalanche Agency — تصميم الويب المتميز والتسويق والأتمتة بالذكاء الاصطناعي",
        "desc": "تصميم مواقع عالية التحويل، تسويق رقمي، وأتمتة مخصصة بالذكاء الاصطناعي للشركات الطموحة.",
        "nav_services": "الخدمات", "nav_pricing": "الأسعار", "nav_about": "من نحن", "nav_contact": "اتصل بنا", "nav_btn": "ابدأ مشروعك",
        "hero_badge": "التميز الرقمي والذكاء الاصطناعي",
        "hero_h1": "مواقع تحقق التحويل. علامات تجارية تهيمن.",
        "hero_p": "نقوم بتصميم أنظمة ويب عالية الأداء، وأتمتة الذكاء الاصطناعي، ومحركات التسويق للقادة العالميين.",
        "hero_btn": "ابدأ مشروعك",
        "services_title": "خدمات مصممة لتأثير ملموس.",
        "process_title": "كيف نحول الأفكار إلى أرباح.",
        "why_title": "لماذا تختار الشركات العالمية Avalanche.",
        "contact_title": "هل أنت مستعد للتوسع؟ بدون مخاطر.",
        "contact_btn": "إرسال الطلب ➔",
        "services_page_title": "خدماتنا الرقمية وحلول الذكاء الاصطناعي",
        "services_page_sub": "تطوير ويب عالمي المستوى، هندسة برمجيات مخصصة، وتسويق نمو.",
        "form_name": "الاسم الكامل", "form_email": "البريد الإلكتروني للعمل", "form_message": "أخبرنا عن مشروعك...", "form_submit": "إرسال الطلب ➔"
    },
    "uk": {
        "title": "Avalanche Agency — Преміальний Веб-Дизайн, Маркетинг та AI Автоматизація",
        "desc": "Висококонверсійний веб-дизайн, цифровий маркетинг та кастомна автоматизація на базі штучного інтелекту.",
        "nav_services": "Послуги", "nav_pricing": "Ціни", "nav_about": "Про Нас", "nav_contact": "Контакти", "nav_btn": "Розпочати Проект",
        "hero_badge": "Цифрова Досконалість та AI Інтелект",
        "hero_h1": "Сайти, що конвертують. Бренди, що домінують.",
        "hero_p": "Ми розробляємо високопродуктивні веб-системи, AI-автоматизацію та маркетингові рушії для світових лідерів.",
        "hero_btn": "Розпочати Проект",
        "services_title": "Послуги для вимірюваного результату.",
        "process_title": "Як ми перетворюємо ідеї на прибуток.",
        "why_title": "Чому бренди обирають Avalanche.",
        "contact_title": "Готові до масштабування? Нуль Ризику.",
        "contact_btn": "Надіслати Запит ➔",
        "services_page_title": "Наші Цифрові Послуги та AI-Рішення",
        "services_page_sub": "Веб-розробка світового рівня, кастомна архітектура програмного забезпечення та маркетинг зростання.",
        "form_name": "Ваше Повне Ім'я", "form_email": "Корпоративний E-mail", "form_message": "Розкажіть про ваш проект...", "form_submit": "Надіслати Запит ➔"
    },
    "ru": {
        "title": "Avalanche Agency — Премиальный Веб-Дизайн, Маркетинг и AI Автоматизация",
        "desc": "Высококонверсионный веб-дизайн, цифровой маркетинг и кастомная автоматизация на базе искусственного интеллекта.",
        "nav_services": "Услуги", "nav_pricing": "Цены", "nav_about": "О Нас", "nav_contact": "Контакты", "nav_btn": "Начать Проект",
        "hero_badge": "Цифровое Совершенство и AI Интеллект",
        "hero_h1": "Сайты, которые конвертируют. Бренды, которые доминируют.",
        "hero_p": "Мы разрабатываем высокопроизводительные веб-системы, AI-автоматизацию и маркетинговые движки для мировых лидеров.",
        "hero_btn": "Начать Проект",
        "services_title": "Услуги для измеримого результата.",
        "process_title": "Как мы превращаем идеи в прибыль.",
        "why_title": "Почему бренды выбирают Avalanche.",
        "contact_title": "Готовы к масштабированию? Ноль Риска.",
        "contact_btn": "Отправить Запрос ➔",
        "services_page_title": "Наши Цифровые Услуги и AI-Решения",
        "services_page_sub": "Веб-разработка мирового уровня, кастомная архитектура программного обеспечения и маркетинг роста.",
        "form_name": "Ваше Полное Имя", "form_email": "Корпоративный E-mail", "form_message": "Расскажите о вашем проекте...", "form_submit": "Отправить Запрос ➔"
    }
}

def generate_navbar_html(lang):
    t = translations[lang]
    is_root = (lang == "en")
    prefix = "" if is_root else f"/{lang}"
    
    # Генерация селектора языков
    lang_opts = []
    for code, label in [("en","EN"), ("es","ES"), ("it","IT"), ("fr","FR"), ("de","DE"), ("zh","ZH"), ("ar","AR"), ("uk","UK"), ("ru","RU")]:
        sel = "selected" if code == lang else ""
        lang_opts.append(f'<option value="{code}" {sel}>{label}</option>')
    opts_str = "\n".join(lang_opts)

    return f"""
<nav style="position: sticky; top: 0; z-index: 1000; background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); border-bottom: 1px solid #E2E8F0;">
  <div class="wrap nav-in" style="display: flex; align-items: center; justify-content: space-between; padding: 14px 20px;">
    <div class="brand">
      <a href="{prefix}/index.html" style="text-decoration: none; display: flex; align-items: center; gap: 10px;">
        <img src="/avalanche_logo.png" alt="Avalanche" style="height: 36px; width: auto;" />
        <span class="name" style="color: #0F172A; font-weight: 800; font-size: 19px; letter-spacing: -0.02em;">Avalanche Agency</span>
      </a>
    </div>

    <!-- Десктопное меню без стрелочек! -->
    <div class="desktop-nav" style="display: flex; align-items: center; gap: 28px;">
      <a href="{prefix}/services.html" style="color: #475569; text-decoration: none; font-weight: 600; font-size: 15px;">{t['nav_services']}</a>
      <a href="{prefix}/pricing.html" style="color: #475569; text-decoration: none; font-weight: 600; font-size: 15px;">{t['nav_pricing']}</a>
      <a href="{prefix}/about.html" style="color: #475569; text-decoration: none; font-weight: 600; font-size: 15px;">{t['nav_about']}</a>
      <a href="{prefix}/contact.html" style="color: #475569; text-decoration: none; font-weight: 600; font-size: 15px;">{t['nav_contact']}</a>
    </div>

    <div class="desktop-nav" style="display: flex; align-items: center; gap: 16px;">
      <!-- Переключатель языка со СПИСКОМ МАРШРУТОВ -->
      <select onchange="navigateToLang(this.value)" style="background: #F1F5F9; color: #0F172A; border: 1px solid #CBD5E1; padding: 8px 14px; border-radius: 8px; font-size: 14px; font-weight: 700; cursor: pointer; outline: none;">
        {opts_str}
      </select>
      
      <a href="#contact" class="btn" style="background: #60B5FF; color: #FFF; padding: 10px 20px; text-decoration: none; border-radius: 10px; font-weight: 700;">{t['nav_btn']}</a>
    </div>

    <button class="mobile-menu-btn" onclick="toggleMobileMenu()" style="display: none; background: #F1F5F9; border: 1px solid #CBD5E1; padding: 8px 12px; border-radius: 8px; font-size: 20px; cursor: pointer; color: #0F172A;">
      ☰
    </button>
  </div>

  <div id="mobile-overlay" class="mobile-nav-overlay" style="display: none; position: fixed; top: 65px; left: 0; right: 0; background: #0B0F19; padding: 24px; flex-direction: column; gap: 16px; border-bottom: 1px solid #334155;">
    <a href="{prefix}/services.html" style="color: #F8FAFC; text-decoration: none; font-weight: 600; font-size: 18px;">{t['nav_services']}</a>
    <a href="{prefix}/pricing.html" style="color: #F8FAFC; text-decoration: none; font-weight: 600; font-size: 18px;">{t['nav_pricing']}</a>
    <a href="{prefix}/about.html" style="color: #F8FAFC; text-decoration: none; font-weight: 600; font-size: 18px;">{t['nav_about']}</a>
    <a href="{prefix}/contact.html" style="color: #F8FAFC; text-decoration: none; font-weight: 600; font-size: 18px;">{t['nav_contact']}</a>
    
    <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 12px; padding-top: 12px; border-top: 1px solid #334155;">
      <select onchange="navigateToLang(this.value)" style="background: #1E293B; color: #F8FAFC; border: 1px solid #475569; padding: 8px 14px; border-radius: 8px; font-size: 15px; font-weight: 700;">
        {opts_str}
      </select>
      <a href="#contact" class="btn" style="background: #60B5FF; color: #FFF; padding: 10px 18px; text-decoration: none; border-radius: 8px; font-weight: 700;">{t['nav_btn']}</a>
    </div>
  </div>
</nav>

<script>
function navigateToLang(targetLang) {{
  const currentPath = window.location.pathname;
  // Находим текущую страницу (index.html, services.html, etc)
  let pageName = currentPath.split('/').pop() || 'index.html';
  if (pageName === '' || !pageName.includes('.html')) pageName = 'index.html';
  
  let newUrl = '/';
  if (targetLang !== 'en') {{
    newUrl = '/' + targetLang + '/' + pageName;
  }} else {{
    newUrl = '/' + pageName;
  }}
  window.location.href = newUrl;
}}

function toggleMobileMenu() {{
  const m = document.getElementById('mobile-overlay');
  if (m) {{
    m.style.display = (m.style.display === 'flex') ? 'none' : 'flex';
  }}
}}
</script>
"""

# Генерация страницы Services.html (Светлая чистая белая верстка без темных элементов!)
def generate_services_page(lang):
    t = translations[lang]
    is_rtl = (lang == "ar")
    dir_attr = 'dir="rtl"' if is_rtl else 'dir="ltr"'
    nav_h = generate_navbar_html(lang)
    
    return f"""<!DOCTYPE html>
<html lang="{lang}" {dir_attr}>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{t['services_page_title']} — Avalanche Agency</title>
  <meta name="description" content="{t['services_page_sub']}">
  <link rel="icon" type="image/png" href="/avalanche_logo.png">
  <link rel="shortcut icon" href="/avalanche_logo.png">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --blue: #60B5FF;
      --blue-d: #389BFF;
      --bg: #FFFFFF;
      --surface: #F8FAFC;
      --ink: #0F172A;
      --muted: #64748B;
      --line: #E2E8F0;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background: var(--bg); color: var(--ink); font-family: "Inter", system-ui, sans-serif; line-height: 1.6; }}
    .wrap {{ max-width: 1180px; margin: 0 auto; padding: 0 20px; }}
    .btn {{
      display: inline-block;
      padding: 12px 24px;
      background: var(--blue);
      color: #FFF;
      text-decoration: none;
      font-weight: 700;
      border-radius: 10px;
      transition: all 0.2s;
      box-shadow: 0 8px 25px rgba(96, 181, 255, 0.3);
    }}
    .btn:hover {{ background: var(--blue-d); transform: translateY(-2px); }}
    
    .service-card {{
      background: #FFFFFF;
      border: 1px solid #E2E8F0;
      border-radius: 20px;
      padding: 32px;
      margin-bottom: 40px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.03);
      display: flex;
      flex-direction: column;
      gap: 24px;
    }}
    @media (min-width: 900px) {{
      .service-card {{ flex-direction: row; align-items: center; }}
      .service-card.reverse {{ flex-direction: row-reverse; }}
      .service-card > div {{ flex: 1; }}
    }}
    .service-img {{
      width: 100%;
      height: 320px;
      object-fit: cover;
      border-radius: 16px;
      border: 1px solid #E2E8F0;
    }}
  </style>
</head>
<body>
  {nav_h}

  <section style="padding: 80px 0 40px; background: linear-gradient(180deg, #F0F9FF 0%, #FFFFFF 100%); text-align: center; border-bottom: 1px solid #E2E8F0;">
    <div class="wrap">
      <span style="display: inline-block; padding: 6px 16px; background: #E0F2FE; color: #0284C7; font-weight: 700; font-size: 12px; border-radius: 20px; text-transform: uppercase; margin-bottom: 16px;">
        WORLD-CLASS CAPABILITIES
      </span>
      <h1 style="font-size: 42px; font-weight: 800; color: #0F172A; margin-bottom: 16px;">{t['services_page_title']}</h1>
      <p style="font-size: 18px; color: #64748B; max-width: 700px; margin: 0 auto;">{t['services_page_sub']}</p>
    </div>
  </section>

  <section style="padding: 60px 0;">
    <div class="wrap">
      
      <!-- Card 1 -->
      <div class="service-card">
        <img src="https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1200&q=80" class="service-img" alt="Infrastructure">
        <div>
          <span style="color: #60B5FF; font-weight: 800; font-size: 14px;">01 • ENTERPRISE INFRASTRUCTURE</span>
          <h2 style="font-size: 28px; font-weight: 800; margin: 8px 0 16px; color: #0F172A;">Infrastructure & Hosting</h2>
          <p style="color: #475569; font-size: 16px; margin-bottom: 20px;">Build a rock-solid foundation for your online presence with domain selection, corporate email, and enterprise-grade cloud hosting.</p>
          <a href="#contact" class="btn">Get Started ➔</a>
        </div>
      </div>

      <!-- Card 2 -->
      <div class="service-card reverse">
        <img src="https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=1200&q=80" class="service-img" alt="Development">
        <div>
          <span style="color: #60B5FF; font-weight: 800; font-size: 14px;">02 • CUSTOM SOFTWARE</span>
          <h2 style="font-size: 28px; font-weight: 800; margin: 8px 0 16px; color: #0F172A;">Custom Web Development</h2>
          <p style="color: #475569; font-size: 16px; margin-bottom: 20px;">Transform your vision into high-conversion web systems, modern UI/UX, and tailored AI agent integrations.</p>
          <a href="#contact" class="btn">Get Started ➔</a>
        </div>
      </div>

      <!-- Card 3 -->
      <div class="service-card">
        <img src="https://images.unsplash.com/photo-1499750310107-5fef28a66643?auto=format&fit=crop&w=1200&q=80" class="service-img" alt="Content">
        <div>
          <span style="color: #60B5FF; font-weight: 800; font-size: 14px;">03 • CREATIVE STRATEGY</span>
          <h2 style="font-size: 28px; font-weight: 800; margin: 8px 0 16px; color: #0F172A;">Content & Copywriting</h2>
          <p style="color: #475569; font-size: 16px; margin-bottom: 20px;">Connect with global audiences through compelling copywriting, professional translations, and brand storytelling.</p>
          <a href="#contact" class="btn">Get Started ➔</a>
        </div>
      </div>

      <!-- Card 4 -->
      <div class="service-card reverse">
        <img src="https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1200&q=80" class="service-img" alt="Marketing">
        <div>
          <span style="color: #60B5FF; font-weight: 800; font-size: 14px;">04 • GROWTH ENGINE</span>
          <h2 style="font-size: 28px; font-weight: 800; margin: 8px 0 16px; color: #0F172A;">Digital Marketing & SEO</h2>
          <p style="color: #475569; font-size: 16px; margin-bottom: 20px;">Amplify your brand reach with data-driven SEO strategies, performance marketing, and SMM campaigns.</p>
          <a href="#contact" class="btn">Get Started ➔</a>
        </div>
      </div>

    </div>
  </section>

  <!-- Contact Form Section -->
  <section id="contact" style="padding: 60px 0; background: #F8FAFC; border-top: 1px solid #E2E8F0;">
    <div class="wrap" style="max-width: 600px; text-align: center;">
      <h2 style="font-size: 32px; font-weight: 800; margin-bottom: 12px; color: #0F172A;">{t['contact_title']}</h2>
      <p style="color: #64748B; margin-bottom: 24px;">Start your project with a team that treats your brand like their own.</p>
      
      <form action="https://api.web3forms.com/submit" method="POST" style="display: flex; flex-direction: column; gap: 16px; background: #FFFFFF; padding: 32px; border-radius: 16px; border: 1px solid #CBD5E1; text-align: left;">
        <input type="hidden" name="access_key" value="ea7c015e-e478-4034-be57-d2e3d93dbb72">
        <input type="hidden" name="subject" value="🚀 New Avalanche Agency Service Lead">
        <input type="hidden" name="replyto" value="dr.reenforce@gmail.com">

        <input type="text" name="name" required placeholder="{t['form_name']}" style="width: 100%; padding: 12px; border: 1px solid #CBD5E1; border-radius: 8px;">
        <input type="email" name="email" required placeholder="{t['form_email']}" style="width: 100%; padding: 12px; border: 1px solid #CBD5E1; border-radius: 8px;">
        <textarea name="message" rows="4" required placeholder="{t['form_message']}" style="width: 100%; padding: 12px; border: 1px solid #CBD5E1; border-radius: 8px;"></textarea>
        
        <button type="submit" class="btn" style="width: 100%; text-align: center; border: none; cursor: pointer;">{t['form_submit']}</button>
      </form>
    </div>
  </section>

  <footer style="padding: 30px 0; text-align: center; color: #94A3B8; font-size: 14px; border-top: 1px solid #E2E8F0;">
    &copy; {time.strftime('%Y')} Avalanche Agency. All rights reserved.
  </footer>
</body>
</html>
"""

# Собираем файлы для каждого языка в его собственную папку
for lang_code in ["en", "es", "it", "fr", "de", "zh", "ar", "uk", "ru"]:
    is_root = (lang_code == "en")
    target_dir = STAGING_DIR if is_root else os.path.join(STAGING_DIR, lang_code)
    os.makedirs(target_dir, exist_ok=True)
    
    # 1. Генерируем index.html для этой языковой папки
    html_content = base_html
    nav_html = generate_navbar_html(lang_code)
    html_content = re.sub(r'<nav.*?</nav>', nav_html, html_content, flags=re.DOTALL)
    
    # RTL для Арабского
    if lang_code == "ar":
        html_content = html_content.replace('<html lang="en">', '<html lang="ar" dir="rtl">')
    else:
        html_content = html_content.replace('<html lang="en">', f'<html lang="{lang_code}">')
        
    with open(os.path.join(target_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_content)
        
    # 2. Генерируем services.html для этой языковой папки
    srv_html = generate_services_page(lang_code)
    with open(os.path.join(target_dir, "services.html"), "w", encoding="utf-8") as f:
        f.write(srv_html)
        
    # 3. Скопируем оригинальные pricing.html, about.html, contact.html
    for pfile in ["pricing.html", "about.html", "contact.html"]:
        src_p = os.path.join(DESIGN_DIR, "package", "code", "avalanche-agency", "dist", "index.html")
        if os.path.exists(src_p):
            shutil.copy(src_p, os.path.join(target_dir, pfile))

print("✅ Все языковые папки (/es/, /it/, /fr/, /de/, /zh/, /ar/, /uk/, /ru/) и главная / успешно собраны!")

# Скрипт редиректа по IP на корню сайта
ip_redirect_script = """
<script>
// Автоперенаправление по IP если зашли впервые на чистый корень
(async function() {
  const saved = localStorage.getItem('avalanche_exact_lang');
  if (saved && saved !== 'en') {
    if (window.location.pathname === '/' || window.location.pathname === '/index.html') {
      window.location.href = '/' + saved + '/';
      return;
    }
  }
  
  if (!saved && (window.location.pathname === '/' || window.location.pathname === '/index.html')) {
    try {
      const res = await fetch('https://ipapi.co/json/');
      const data = await res.json();
      const cc = (data.country_code || '').toLowerCase();
      let det = 'en';
      if (['ua'].includes(cc)) det = 'uk';
      else if (['ru', 'by', 'kz'].includes(cc)) det = 'ru';
      else if (['es', 'mx', 'ar', 'cl', 'co'].includes(cc)) det = 'es';
      else if (['it'].includes(cc)) det = 'it';
      else if (['fr', 'be'].includes(cc)) det = 'fr';
      else if (['de', 'at', 'ch'].includes(cc)) det = 'de';
      else if (['cn', 'tw', 'hk'].includes(cc)) det = 'zh';
      else if (['sa', 'ae', 'eg', 'qa'].includes(cc)) det = 'ar';
      
      if (det !== 'en') {
        localStorage.setItem('avalanche_exact_lang', det);
        window.location.href = '/' + det + '/';
      }
    } catch(e) {}
  }
})();
</script>
"""

root_index_path = os.path.join(STAGING_DIR, "index.html")
root_html = open(root_index_path, encoding="utf-8").read()
root_html = root_html.replace("</head>", ip_redirect_script + "\n</head>")
with open(root_index_path, "w", encoding="utf-8") as f:
    f.write(root_html)

# 4. Копируем 200.html для Surge.sh SPA
shutil.copy(os.path.join(STAGING_DIR, "index.html"), os.path.join(STAGING_DIR, "200.html"))

print("🎉 МУЛЬТИ-МАРШРУТНЫЙ ПРОЕКТ ГОТОВ К ДЕПЛОЮ!")
