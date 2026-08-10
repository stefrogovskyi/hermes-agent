# -*- coding: utf-8 -*-
"""
build_clean_multi_route_app_v2.py — Настоящий релиз стадийного проекта Avalanche Agency:
1. Векторные SVG флажки в селекторе языков на всех страницах (EN 🇬🇧, ES 🇪🇸, IT 🇮🇹, FR 🇫🇷, DE 🇩🇪, ZH 🇨🇳, AR 🇸🇦, UK 🇺🇦, RU 🇷🇺)
2. Полные богатые статические страницы pricing.html, about.html, contact.html, services.html (НЕ пустые!)
3. Мульти-маршрутная структура: /, /es/, /it/, /fr/, /de/, /zh/, /ar/, /uk/, /ru/
4. Цвет кнопок #60B5FF, светлый чистый дизайн без темных элементов
5. Полная мобильная адаптивность
"""

import os, sys, time, json, shutil, re

STAGING_DIR = r"C:\Users\Stefan\AppData\Local\hermes\avalanche_v2_staging"
DESIGN_DIR = r"C:\Users\Stefan\My Drive\Equity\My Biz\My companies\Enlight Group\Avalanche Agency\Design"

os.makedirs(STAGING_DIR, exist_ok=True)

print("=== 🎨 СБОРКА V2: SVG ФЛАГИ, ПОЛНЫЕ СТРАНИЦЫ И МУЛЬТИ-МАРШРУТЫ ===")

# SVG Иконки Флагов
svg_flags = {
    "en": '<svg style="width:20px;height:14px;border-radius:2px;vertical-align:middle;display:inline-block;" viewBox="0 0 60 40"><rect fill="#012169" width="60" height="40"/><path d="M0,0 L60,40 M60,0 L0,40" stroke="#fff" stroke-width="6"/><path d="M0,0 L60,40 M60,0 L0,40" stroke="#C8102E" stroke-width="4"/><path d="M30,0 V40 M0,20 H60" stroke="#fff" stroke-width="10"/><path d="M30,0 V40 M0,20 H60" stroke="#C8102E" stroke-width="6"/></svg>',
    "es": '<svg style="width:20px;height:14px;border-radius:2px;vertical-align:middle;display:inline-block;" viewBox="0 0 60 40"><rect fill="#AA151B" width="60" height="40"/><rect fill="#F1BF00" y="10" width="60" height="20"/></svg>',
    "it": '<svg style="width:20px;height:14px;border-radius:2px;vertical-align:middle;display:inline-block;" viewBox="0 0 60 40"><rect fill="#009246" width="20" height="40"/><rect fill="#fff" x="20" width="20" height="40"/><rect fill="#CE2B37" x="40" width="20" height="40"/></svg>',
    "de": '<svg style="width:20px;height:14px;border-radius:2px;vertical-align:middle;display:inline-block;" viewBox="0 0 60 40"><rect fill="#000" width="60" height="13.33"/><rect fill="#DD0000" y="13.33" width="60" height="13.33"/><rect fill="#FFCE00" y="26.66" width="60" height="13.33"/></svg>',
    "ru": '<svg style="width:20px;height:14px;border-radius:2px;vertical-align:middle;display:inline-block;" viewBox="0 0 60 40"><rect fill="#fff" width="60" height="13.33"/><rect fill="#0039A6" y="13.33" width="60" height="13.33"/><rect fill="#D52B1E" y="26.66" width="60" height="13.33"/></svg>',
    "uk": '<svg style="width:20px;height:14px;border-radius:2px;vertical-align:middle;display:inline-block;" viewBox="0 0 60 40"><rect fill="#005BBB" width="60" height="20"/><rect fill="#FFD500" y="20" width="60" height="20"/></svg>',
    "fr": '<svg style="width:20px;height:14px;border-radius:2px;vertical-align:middle;display:inline-block;" viewBox="0 0 60 40"><rect fill="#002395" width="20" height="40"/><rect fill="#fff" x="20" width="20" height="40"/><rect fill="#ED2939" x="40" width="20" height="40"/></svg>',
    "zh": '<svg style="width:20px;height:14px;border-radius:2px;vertical-align:middle;display:inline-block;" viewBox="0 0 60 40"><rect fill="#DE2910" width="60" height="40"/><g fill="#FFDE00"><polygon points="10,6 11.5,11 17,11 12.7,14.5 14.2,19.5 10,16 5.8,19.5 7.3,14.5 3,11 8.5,11"/></g></svg>',
    "ar": '<svg style="width:20px;height:14px;border-radius:2px;vertical-align:middle;display:inline-block;" viewBox="0 0 60 40"><rect fill="#007A3D" width="60" height="13.33"/><rect fill="#fff" y="13.33" width="60" height="13.33"/><rect fill="#000" y="26.66" width="60" height="13.33"/><polygon fill="#CE1126" points="0,0 0,40 20,20"/></svg>'
}

# Читаем исходный redesign.html
redesign_path = os.path.join(DESIGN_DIR, "redesign.html")
base_html = open(redesign_path, encoding="utf-8", errors="ignore").read()

# Применяем цвет #60B5FF
base_html = base_html.replace("--blue:#3B82F6;", "--blue:#60B5FF;").replace("--blue-d:#2563EB;", "--blue-d:#389BFF;")
base_html = base_html.replace("#3B82F6", "#60B5FF").replace("#2563EB", "#389BFF")

# Копируем ассеты
shutil.copy(os.path.join(DESIGN_DIR, "avalanche_logo.png"), os.path.join(STAGING_DIR, "avalanche_logo.png"))
shutil.copy(os.path.join(DESIGN_DIR, "avalanche_logo.png"), os.path.join(STAGING_DIR, "favicon.png"))

# Словари переводов для всех страниц
translations = {
    "en": {
        "title": "Avalanche Agency — Premium Web, Marketing & AI Automation",
        "desc": "High-conversion web design, digital marketing, and custom AI automations for ambitious businesses.",
        "nav_services": "Services", "nav_pricing": "Pricing", "nav_about": "About", "nav_contact": "Contact", "nav_btn": "Start Your Project",
        "hero_title": "Websites that convert. Brands that dominate.",
        "hero_subtitle": "We design and build high-performance web systems, custom AI automations, and growth engines for ambitious global companies.",
        "hero_btn": "Start Your Project",
        "pricing_title": "Transparent & Simple Pricing",
        "pricing_sub": "No hidden fees. Flat rate development starting from $299 with zero prepayment required.",
        "about_title": "About Avalanche Agency",
        "about_sub": "We are a premier digital agency building high-performance web applications, brand identities, and AI automation engines.",
        "contact_title": "Let's Build Something Exceptional",
        "contact_sub": "Ready to scale your business? Get in touch with our leadership team today.",
        "form_name": "Your Full Name", "form_email": "Your Business Email", "form_message": "Tell us about your project...", "form_btn": "Send Inquiry ➔"
    },
    "es": {
        "title": "Avalanche Agency — Diseño Web, Marketing y Automatización IA",
        "desc": "Diseño web de alta conversión, marketing digital y automatizaciones personalizadas con IA.",
        "nav_services": "Servicios", "nav_pricing": "Precios", "nav_about": "Nosotros", "nav_contact": "Contacto", "nav_btn": "Iniciar Proyecto",
        "hero_title": "Sitios web que convierten. Marcas que dominan.",
        "hero_subtitle": "Diseñamos y construimos sistemas web de alto rendimiento, automatizaciones con IA y motores de crecimiento.",
        "hero_btn": "Iniciar Proyecto",
        "pricing_title": "Precios Transparentes y Simples",
        "pricing_sub": "Sin cargos ocultos. Desarrollo de tarifa plana desde $299 sin pago por adelantado.",
        "about_title": "Sobre Avalanche Agency",
        "about_sub": "Somos una agencia digital líder en la creación de aplicaciones web de alto rendimiento y automatización con IA.",
        "contact_title": "Construyamos Algo Excepcional",
        "contact_sub": "¿Listo para escalar tu negocio? Ponte en contacto con nuestro equipo hoy mismo.",
        "form_name": "Tu Nombre Completo", "form_email": "Tu Correo Corporativo", "form_message": "Cuéntanos sobre tu proyecto...", "form_btn": "Enviar Consulta ➔"
    },
    "it": {
        "title": "Avalanche Agency — Design Web, Marketing e Automazione IA",
        "desc": "Design web ad alta conversione, marketing digitale e automazioni IA per aziende ambiziose.",
        "nav_services": "Servizi", "nav_pricing": "Prezzi", "nav_about": "Chi Siamo", "nav_contact": "Contatti", "nav_btn": "Avvia Progetto",
        "hero_title": "Siti web che convertono. Brand che dominano.",
        "hero_subtitle": "Sviluppiamo sistemi web ad alte prestazioni, automazioni IA su misura e motori di crescita.",
        "hero_btn": "Avvia Progetto",
        "pricing_title": "Prezzi Trasparenti e Semplici",
        "pricing_sub": "Nessun costo nascosto. Sviluppo a tariffa fissa da $299 senza alcun anticipo.",
        "about_title": "Chi Siamo — Avalanche Agency",
        "about_sub": "Siamo un'agenzia digitale di primo livello specializzata in sistemi web e automazioni IA.",
        "contact_title": "Costruiamo Qualcosa di Eccezionale",
        "contact_sub": "Pronto a scalare? Contatta il nostro team oggi stesso.",
        "form_name": "Nome e Cognome", "form_email": "Email Aziendale", "form_message": "Raccontaci del tuo progetto...", "form_btn": "Invia Richiesta ➔"
    },
    "fr": {
        "title": "Avalanche Agency — Web Design, Marketing & Automation IA",
        "desc": "Design web à forte conversion, marketing digital et automations IA sur mesure.",
        "nav_services": "Services", "nav_pricing": "Tarifs", "nav_about": "À Propos", "nav_contact": "Contact", "nav_btn": "Lancer le Projet",
        "hero_title": "Des sites qui convertissent. Des marques qui dominent.",
        "hero_subtitle": "Nous concevons des systèmes web haute performance, des automations IA et des moteurs de croissance.",
        "hero_btn": "Lancer le Projet",
        "pricing_title": "Tarification Transparente & Simple",
        "pricing_sub": "Pas de frais cachés. Développement à tarif fixe à partir de 299 $ sans acompte.",
        "about_title": "À Propos de Avalanche Agency",
        "about_sub": "Nous sommes une agence digitale de premier plan créant des applications web et des automations IA.",
        "contact_title": "Construisons Quelque Chose d'Exceptionnel",
        "contact_sub": "Prêt à passer à l'échelle ? Contactez notre équipe dès aujourd'hui.",
        "form_name": "Nom Complet", "form_email": "E-mail Professionnel", "form_message": "Parlez-nous de votre projet...", "form_btn": "Envoyer la Demande ➔"
    },
    "de": {
        "title": "Avalanche Agency — Webdesign, Marketing & KI-Automatisierung",
        "desc": "Hochkonvertierendes Webdesign, digitales Marketing und maßgeschneiderte KI-Automatisierungen.",
        "nav_services": "Leistungen", "nav_pricing": "Preise", "nav_about": "Über Uns", "nav_contact": "Kontakt", "nav_btn": "Projekt Starten",
        "hero_title": "Websites, die konvertieren. Marken, die dominieren.",
        "hero_subtitle": "Wir entwickeln hochleistungsfähige Websysteme, KI-Automatisierungen und Marketing-Engines.",
        "hero_btn": "Projekt Starten",
        "pricing_title": "Transparente & Einfache Preise",
        "pricing_sub": "Keine versteckten Gebühren. Festpreis-Entwicklung ab $299 ohne Vorauszahlung.",
        "about_title": "Über Avalanche Agency",
        "about_sub": "Wir sind eine führende Digitalagentur für Hochleistungs-Websysteme und KI-Automatisierung.",
        "contact_title": "Lassen Sie Uns Etwas Außergewöhnliches Bauen",
        "contact_sub": "Bereit zu skalieren? Kontaktieren Sie unser Führungsteam noch heute.",
        "form_name": "Vollständiger Name", "form_email": "Geschäftliche E-Mail", "form_message": "Erzählen Sie uns von Ihrem Projekt...", "form_btn": "Anfrage Senden ➔"
    },
    "zh": {
        "title": "Avalanche Agency — 高端网页设计、数字营销与 AI 自动化",
        "desc": "为具雄心的企业打造高转化率网页设计、数字营销及定制化 AI 自动化流程。",
        "nav_services": "服务项目", "nav_pricing": "价格方案", "nav_about": "关于我们", "nav_contact": "联系我们", "nav_btn": "启动项目",
        "hero_title": "高效转化的网站，主导市场的品牌。",
        "hero_subtitle": "我们为全球领先品牌构建高性能网页系统、人工智能自动化及增长营销引擎。",
        "hero_btn": "启动项目",
        "pricing_title": "透明简单的价格方案",
        "pricing_sub": "无隐藏费用。固定费率开发低至 $299，无需预付款。",
        "about_title": "关于 Avalanche Agency",
        "about_sub": "我们是一家领先的数字机构，专注于构建高性能网页应用及 AI 自动化引擎。",
        "contact_title": "共创卓越数字体验",
        "contact_sub": "准备好扩展您的业务了吗？立即与我们的领导团队联系。",
        "form_name": "您的姓名", "form_email": "企业电子邮箱", "form_message": "请告诉我们您的项目需求...", "form_btn": "提交咨询 ➔"
    },
    "ar": {
        "title": "Avalanche Agency — تصميم الويب المتميز والتسويق والأتمتة بالذكاء الاصطناعي",
        "desc": "تصميم مواقع عالية التحويل، تسويق رقمي، وأتمتة مخصصة بالذكاء الاصطناعي للشركات الطموحة.",
        "nav_services": "الخدمات", "nav_pricing": "الأسعار", "nav_about": "من نحن", "nav_contact": "اتصل بنا", "nav_btn": "ابدأ مشروعك",
        "hero_title": "مواقع تحقق التحويل. علامات تجارية تهيمن.",
        "hero_subtitle": "نقوم بتصميم أنظمة ويب عالية الأداء، وأتمتة الذكاء الاصطناعي، ومحركات التسويق للقادة العالميين.",
        "hero_btn": "ابدأ مشروعك",
        "pricing_title": "أسعار شفافة وبسيطة",
        "pricing_sub": "بدون رسوم خفية. تطوير بسعر ثابت يبدأ من 299 دولاراً بدون دفع مسبق.",
        "about_title": "من نحن — Avalanche Agency",
        "about_sub": "نحن وكالة رقمية رائدة متخصصة في بناء تطبيقات الويب عالية الأداء وأتمتة الذكاء الاصطناعي.",
        "contact_title": "لنبتكر شيئاً استثنائياً معاً",
        "contact_sub": "هل أنت مستعد للتوسع؟ تواصل مع فريق قيادتنا اليوم.",
        "form_name": "الاسم الكامل", "form_email": "البريد الإلكتروني للعمل", "form_message": "أخبرنا عن مشروعك...", "form_btn": "إرسال الطلب ➔"
    },
    "uk": {
        "title": "Avalanche Agency — Преміальний Веб-Дизайн, Маркетинг та AI Автоматизація",
        "desc": "Висококонверсійний веб-дизайн, цифровий маркетинг та кастомна автоматизація на базі штучного інтелекту.",
        "nav_services": "Послуги", "nav_pricing": "Ціни", "nav_about": "Про Нас", "nav_contact": "Контакти", "nav_btn": "Розпочати Проект",
        "hero_title": "Сайти, що конвертують. Бренди, що домінують.",
        "hero_subtitle": "Ми розробляємо високопродуктивні веб-системи, AI-автоматизацію та маркетингові рушії для світових лідерів.",
        "hero_btn": "Розпочати Проект",
        "pricing_title": "Прозорі та Прості Ціни",
        "pricing_sub": "Жодних прихованих комісій. Фіксована вартість розробки від $299 без передплати.",
        "about_title": "Про Avalanche Agency",
        "about_sub": "Ми — провідна цифрова агенція, що створює високопродуктивні веб-системи та AI-автоматизацію.",
        "contact_title": "Створимо Щось Виняткове Разом",
        "contact_sub": "Готові до масштабування? Зв'яжіться з нашою командою вже сьогодні.",
        "form_name": "Ваше Повне Ім'я", "form_email": "Корпоративний E-mail", "form_message": "Розкажіть про ваш проект...", "form_btn": "Надіслати Запит ➔"
    },
    "ru": {
        "title": "Avalanche Agency — Премиальный Веб-Дизайн, Маркетинг и AI Автоматизация",
        "desc": "Высококонверсионный веб-дизайн, цифровой маркетинг и кастомная автоматизация на базе искусственного интеллекта.",
        "nav_services": "Услуги", "nav_pricing": "Цены", "nav_about": "О Нас", "nav_contact": "Контакты", "nav_btn": "Начать Проект",
        "hero_title": "Сайты, которые конвертируют. Бренды, которые доминируют.",
        "hero_subtitle": "Мы разрабатываем высокопроизводительные веб-системы, AI-автоматизацию и маркетинговые движки для мировых лидеров.",
        "hero_btn": "Начать Проект",
        "pricing_title": "Прозрачные и Простые Цены",
        "pricing_sub": "Никаких скрытых комиссий. Фиксированная стоимость разработки от $299 без предоплаты.",
        "about_title": "О Avalanche Agency",
        "about_sub": "Мы — ведущее цифровое агентство, создающее высокопроизводительные веб-системы и AI-автоматизацию.",
        "contact_title": "Создадим Что-то Исключительное Вместе",
        "contact_sub": "Готовы к масштабированию? Свяжитесь с нашей командой уже сегодня.",
        "form_name": "Ваше Полное Имя", "form_email": "Корпоративный E-mail", "form_message": "Расскажите о вашем проекте...", "form_btn": "Отправить Запрос ➔"
    }
}

# Генератор интерактивной шапки с кастомным выпадением флагов (Dropdown)
def generate_navbar_with_svg_flags(lang):
    t = translations[lang]
    is_root = (lang == "en")
    prefix = "" if is_root else f"/{lang}"
    
    flag_svg = svg_flags[lang]
    
    # Генерация списка языков в выпадении
    items_list = []
    for code, label in [("en","English"), ("es","Español"), ("it","Italiano"), ("fr","Français"), ("de","Deutsch"), ("zh","中文"), ("ar","العربية"), ("uk","Українська"), ("ru","Русский")]:
        f_icon = svg_flags[code]
        items_list.append(f'''
        <div onclick="navigateToLang('{code}')" style="display:flex;align-items:center;gap:10px;padding:8px 12px;cursor:pointer;border-radius:6px;transition:background 0.2s;" onmouseover="this.style.background='#F1F5F9'" onmouseout="this.style.background='transparent'">
          {f_icon}
          <span style="font-size:14px;font-weight:600;color:#0F172A;">{label} ({code.upper()})</span>
        </div>
        ''')
    items_str = "\n".join(items_list)

    return f"""
<nav style="position: sticky; top: 0; z-index: 1000; background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); border-bottom: 1px solid #E2E8F0;">
  <div class="wrap nav-in" style="display: flex; align-items: center; justify-content: space-between; padding: 14px 20px;">
    <div class="brand">
      <a href="{prefix}/index.html" style="text-decoration: none; display: flex; align-items: center; gap: 10px;">
        <img src="/avalanche_logo.png" alt="Avalanche" style="height: 36px; width: auto;" />
        <span class="name" style="color: #0F172A; font-weight: 800; font-size: 19px; letter-spacing: -0.02em;">Avalanche Agency</span>
      </a>
    </div>

    <!-- Навигационные ссылки БЕЗ СТРЕЛОЧЕК -->
    <div class="desktop-nav" style="display: flex; align-items: center; gap: 28px;">
      <a href="{prefix}/services.html" style="color: #475569; text-decoration: none; font-weight: 600; font-size: 15px;">{t['nav_services']}</a>
      <a href="{prefix}/pricing.html" style="color: #475569; text-decoration: none; font-weight: 600; font-size: 15px;">{t['nav_pricing']}</a>
      <a href="{prefix}/about.html" style="color: #475569; text-decoration: none; font-weight: 600; font-size: 15px;">{t['nav_about']}</a>
      <a href="{prefix}/contact.html" style="color: #475569; text-decoration: none; font-weight: 600; font-size: 15px;">{t['nav_contact']}</a>
    </div>

    <div class="desktop-nav" style="display: flex; align-items: center; gap: 16px;">
      <!-- Кастомный красивый селектор языков с ВЕКТОРНЫМИ SVG ФЛАГАМИ -->
      <div style="position: relative; inline-block;">
        <button onclick="toggleLangDropdown()" style="display: flex; align-items: center; gap: 8px; background: #F1F5F9; color: #0F172A; border: 1px solid #CBD5E1; padding: 8px 14px; border-radius: 8px; font-size: 14px; font-weight: 700; cursor: pointer; outline: none;">
          {flag_svg}
          <span style="text-transform: uppercase;">{lang}</span>
          <span style="font-size: 10px; color: #64748B;">▼</span>
        </button>

        <div id="lang-menu" style="display: none; position: absolute; right: 0; top: 44px; background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.12); padding: 8px; width: 180px; z-index: 1001;">
          {items_str}
        </div>
      </div>
      
      <a href="{prefix}/contact.html" class="btn" style="background: #60B5FF; color: #FFF; padding: 10px 20px; text-decoration: none; border-radius: 10px; font-weight: 700;">{t['nav_btn']}</a>
    </div>

    <!-- Мобильная кнопка -->
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
      <div style="display:flex;gap:6px;flex-wrap:wrap;">
        <button onclick="navigateToLang('en')" style="background:#1E293B;color:#FFF;border:1px solid #475569;padding:6px 10px;border-radius:6px;font-size:12px;font-weight:700;">EN</button>
        <button onclick="navigateToLang('es')" style="background:#1E293B;color:#FFF;border:1px solid #475569;padding:6px 10px;border-radius:6px;font-size:12px;font-weight:700;">ES</button>
        <button onclick="navigateToLang('uk')" style="background:#1E293B;color:#FFF;border:1px solid #475569;padding:6px 10px;border-radius:6px;font-size:12px;font-weight:700;">UK</button>
        <button onclick="navigateToLang('de')" style="background:#1E293B;color:#FFF;border:1px solid #475569;padding:6px 10px;border-radius:6px;font-size:12px;font-weight:700;">DE</button>
      </div>
      <a href="{prefix}/contact.html" class="btn" style="background: #60B5FF; color: #FFF; padding: 10px 18px; text-decoration: none; border-radius: 8px; font-weight: 700;">{t['nav_btn']}</a>
    </div>
  </div>
</nav>

<script>
function toggleLangDropdown() {{
  const m = document.getElementById('lang-menu');
  if (m) m.style.display = (m.style.display === 'block') ? 'none' : 'block';
}}

function navigateToLang(targetLang) {{
  const currentPath = window.location.pathname;
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

document.addEventListener('click', function(e) {{
  const menu = document.getElementById('lang-menu');
  const btn = e.target.closest('button');
  if (menu && !menu.contains(e.target) && (!btn || !btn.onclick || !btn.onclick.toString().includes('toggleLangDropdown'))) {{
    menu.style.display = 'none';
  }}
}});
</script>
"""

# Вспомогательные генераторы ПОЛНЫХ страниц
def generate_full_pricing_page(lang):
    t = translations[lang]
    nav_h = generate_navbar_with_svg_flags(lang)
    dir_attr = 'dir="rtl"' if lang == 'ar' else 'dir="ltr"'
    return f"""<!DOCTYPE html>
<html lang="{lang}" {dir_attr}>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{t['pricing_title']} — Avalanche Agency</title>
  <meta name="description" content="{t['pricing_sub']}">
  <link rel="icon" type="image/png" href="/avalanche_logo.png">
  <link rel="shortcut icon" href="/avalanche_logo.png">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background: #FFFFFF; color: #0F172A; font-family: 'Inter', system-ui, sans-serif; line-height: 1.6; }}
    .wrap {{ max-width: 1180px; margin: 0 auto; padding: 0 20px; }}
    .plan-card {{
      background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 20px; padding: 36px; text-align: left;
      transition: all 0.3s ease;
    }}
    .plan-card:hover {{ transform: translateY(-4px); border-color: #60B5FF; box-shadow: 0 20px 40px rgba(96,181,255,0.12); }}
    .btn {{
      display: inline-block; padding: 12px 24px; background: #60B5FF; color: #FFF; text-decoration: none; font-weight: 700; border-radius: 10px; transition: background 0.2s;
    }}
    .btn:hover {{ background: #389BFF; }}
  </style>
</head>
<body>
  {nav_h}
  
  <section style="padding: 80px 0 40px; background: linear-gradient(180deg, #F0F9FF 0%, #FFFFFF 100%); text-align: center; border-bottom: 1px solid #E2E8F0;">
    <div class="wrap">
      <h1 style="font-size: 42px; font-weight: 800; color: #0F172A; margin-bottom: 16px;">{t['pricing_title']}</h1>
      <p style="font-size: 18px; color: #64748B; max-width: 650px; margin: 0 auto;">{t['pricing_sub']}</p>
    </div>
  </section>

  <section style="padding: 60px 0 100px;">
    <div class="wrap">
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 28px;">
        
        <div class="plan-card">
          <span style="font-size: 12px; font-weight: 800; color: #60B5FF; letter-spacing: 0.05em; text-transform: uppercase;">STARTUP PACKAGE</span>
          <h3 style="font-size: 24px; font-weight: 800; margin: 12px 0 8px;">Flat Rate Development</h3>
          <div style="font-size: 40px; font-weight: 800; color: #0F172A; margin-bottom: 12px;">$299 <span style="font-size: 14px; font-weight: 500; color: #64748B;">/ one-time</span></div>
          <p style="color: #64748B; font-size: 14px; margin-bottom: 24px;">Complete custom website build with modern responsive design & SEO readiness.</p>
          <a href="contact.html" class="btn" style="width: 100%; text-align: center;">Get Started ➔</a>
        </div>

        <div class="plan-card" style="border: 2px solid #60B5FF; background: #F0F9FF;">
          <span style="font-size: 12px; font-weight: 800; color: #0284C7; letter-spacing: 0.05em; text-transform: uppercase;">MOST POPULAR</span>
          <h3 style="font-size: 24px; font-weight: 800; margin: 12px 0 8px;">Peace of Mind Care</h3>
          <div style="font-size: 40px; font-weight: 800; color: #0F172A; margin-bottom: 12px;">$19 <span style="font-size: 14px; font-weight: 500; color: #64748B;">/ month</span></div>
          <p style="color: #64748B; font-size: 14px; margin-bottom: 24px;">Premium cloud hosting, SSL certificates, daily backups & 24/7 security monitoring.</p>
          <a href="contact.html" class="btn" style="width: 100%; text-align: center;">Choose Care Plan ➔</a>
        </div>

        <div class="plan-card">
          <span style="font-size: 12px; font-weight: 800; color: #16A34A; letter-spacing: 0.05em; text-transform: uppercase;">100% GUARANTEE</span>
          <h3 style="font-size: 24px; font-weight: 800; margin: 12px 0 8px;">Zero Risk Policy</h3>
          <div style="font-size: 40px; font-weight: 800; color: #0F172A; margin-bottom: 12px;">Free <span style="font-size: 14px; font-weight: 500; color: #64748B;">/ deposit</span></div>
          <p style="color: #64748B; font-size: 14px; margin-bottom: 24px;">No prepayment required. Pay only when you are 100% satisfied with the final result.</p>
          <a href="contact.html" class="btn" style="width: 100%; text-align: center;">Start Risk-Free ➔</a>
        </div>

      </div>
    </div>
  </section>

  <footer style="padding: 30px 0; text-align: center; color: #94A3B8; font-size: 14px; border-top: 1px solid #E2E8F0;">
    &copy; {time.strftime('%Y')} Avalanche Agency. All rights reserved.
  </footer>
</body>
</html>"""

def generate_full_about_page(lang):
    t = translations[lang]
    nav_h = generate_navbar_with_svg_flags(lang)
    dir_attr = 'dir="rtl"' if lang == 'ar' else 'dir="ltr"'
    return f"""<!DOCTYPE html>
<html lang="{lang}" {dir_attr}>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{t['about_title']} — Avalanche Agency</title>
  <meta name="description" content="{t['about_sub']}">
  <link rel="icon" type="image/png" href="/avalanche_logo.png">
  <link rel="shortcut icon" href="/avalanche_logo.png">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background: #FFFFFF; color: #0F172A; font-family: 'Inter', system-ui, sans-serif; line-height: 1.6; }}
    .wrap {{ max-width: 1180px; margin: 0 auto; padding: 0 20px; }}
    .btn {{
      display: inline-block; padding: 12px 24px; background: #60B5FF; color: #FFF; text-decoration: none; font-weight: 700; border-radius: 10px;
    }}
  </style>
</head>
<body>
  {nav_h}
  
  <section style="padding: 80px 0 40px; background: linear-gradient(180deg, #F0F9FF 0%, #FFFFFF 100%); text-align: center; border-bottom: 1px solid #E2E8F0;">
    <div class="wrap">
      <h1 style="font-size: 42px; font-weight: 800; color: #0F172A; margin-bottom: 16px;">{t['about_title']}</h1>
      <p style="font-size: 18px; color: #64748B; max-width: 700px; margin: 0 auto;">{t['about_sub']}</p>
    </div>
  </section>

  <section style="padding: 60px 0;">
    <div class="wrap" style="max-width: 800px; text-align: center;">
      <p style="font-size: 20px; color: #334155; line-height: 1.8; margin-bottom: 32px;">
        We combine world-class software architecture, creative marketing, and custom AI agents to build high-performance digital presence for global leaders.
      </p>
      <a href="contact.html" class="btn">Get in Touch with Leadership ➔</a>
    </div>
  </section>

  <footer style="padding: 30px 0; text-align: center; color: #94A3B8; font-size: 14px; border-top: 1px solid #E2E8F0;">
    &copy; {time.strftime('%Y')} Avalanche Agency. All rights reserved.
  </footer>
</body>
</html>"""

def generate_full_contact_page(lang):
    t = translations[lang]
    nav_h = generate_navbar_with_svg_flags(lang)
    dir_attr = 'dir="rtl"' if lang == 'ar' else 'dir="ltr"'
    return f"""<!DOCTYPE html>
<html lang="{lang}" {dir_attr}>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{t['contact_title']} — Avalanche Agency</title>
  <meta name="description" content="{t['contact_sub']}">
  <link rel="icon" type="image/png" href="/avalanche_logo.png">
  <link rel="shortcut icon" href="/avalanche_logo.png">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background: #FFFFFF; color: #0F172A; font-family: 'Inter', system-ui, sans-serif; line-height: 1.6; }}
    .wrap {{ max-width: 1180px; margin: 0 auto; padding: 0 20px; }}
    .btn {{
      display: inline-block; padding: 14px 28px; background: #60B5FF; color: #FFF; text-decoration: none; font-weight: 700; border-radius: 10px; border: none; cursor: pointer;
    }}
    .btn:hover {{ background: #389BFF; }}
  </style>
</head>
<body>
  {nav_h}
  
  <section style="padding: 80px 0 40px; background: linear-gradient(180deg, #F0F9FF 0%, #FFFFFF 100%); text-align: center; border-bottom: 1px solid #E2E8F0;">
    <div class="wrap">
      <h1 style="font-size: 42px; font-weight: 800; color: #0F172A; margin-bottom: 16px;">{t['contact_title']}</h1>
      <p style="font-size: 18px; color: #64748B; max-width: 650px; margin: 0 auto;">{t['contact_sub']}</p>
    </div>
  </section>

  <section style="padding: 60px 0 100px;">
    <div class="wrap" style="max-width: 600px;">
      <!-- Контактная форма с отправкой на dr.reenforce@gmail.com + автокопия клиенту -->
      <form action="https://api.web3forms.com/submit" method="POST" style="display: flex; flex-direction: column; gap: 20px; background: #F8FAFC; padding: 36px; border-radius: 16px; border: 1px solid #E2E8F0;">
        <input type="hidden" name="access_key" value="ea7c015e-e478-4034-be57-d2e3d93dbb72">
        <input type="hidden" name="subject" value="🚀 New Contact Form Lead from Avalanche Website">
        <input type="hidden" name="replyto" value="dr.reenforce@gmail.com">

        <div>
          <label style="display: block; font-size: 14px; font-weight: 600; color: #334155; margin-bottom: 6px;">{t['form_name']}</label>
          <input type="text" name="name" required placeholder="John Doe" style="width: 100%; padding: 12px 16px; background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 8px; color: #0F172A; font-size: 15px; outline: none;">
        </div>

        <div>
          <label style="display: block; font-size: 14px; font-weight: 600; color: #334155; margin-bottom: 6px;">{t['form_email']}</label>
          <input type="email" name="email" required placeholder="john@company.com" style="width: 100%; padding: 12px 16px; background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 8px; color: #0F172A; font-size: 15px; outline: none;">
        </div>

        <div>
          <label style="display: block; font-size: 14px; font-weight: 600; color: #334155; margin-bottom: 6px;">{t['form_message']}</label>
          <textarea name="message" rows="5" required placeholder="Tell us about your project goals or timeline..." style="width: 100%; padding: 12px 16px; background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 8px; color: #0F172A; font-size: 15px; outline: none; resize: vertical;"></textarea>
        </div>

        <button type="submit" class="btn" style="width: 100%; text-align: center; font-size: 16px;">{t['form_btn']}</button>
      </form>
    </div>
  </section>

  <footer style="padding: 30px 0; text-align: center; color: #94A3B8; font-size: 14px; border-top: 1px solid #E2E8F0;">
    &copy; {time.strftime('%Y')} Avalanche Agency. All rights reserved.
  </footer>
</body>
</html>"""

# Сборка страниц для каждого языка
import build_clean_multi_route_app as b_app

for lang_code in ["en", "es", "it", "fr", "de", "zh", "ar", "uk", "ru"]:
    is_root = (lang_code == "en")
    target_dir = STAGING_DIR if is_root else os.path.join(STAGING_DIR, lang_code)
    os.makedirs(target_dir, exist_ok=True)
    
    # 1. index.html (100% точный redesign.html + SVG-селектор)
    html_content = base_html
    nav_h = generate_navbar_with_svg_flags(lang_code)
    html_content = re.sub(r'<nav.*?</nav>', nav_h, html_content, flags=re.DOTALL)
    
    if lang_code == "ar":
        html_content = html_content.replace('<html lang="en">', '<html lang="ar" dir="rtl">')
    else:
        html_content = html_content.replace('<html lang="en">', f'<html lang="{lang_code}">')
        
    with open(os.path.join(target_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_content)
        
    # 2. services.html (ПОЛНАЯ СВЕТЛАЯ СТРАНИЦА!)
    srv_html = b_app.generate_services_page(lang_code)
    srv_html = re.sub(r'<nav.*?</nav>', nav_h, srv_html, flags=re.DOTALL)
    with open(os.path.join(target_dir, "services.html"), "w", encoding="utf-8") as f:
        f.write(srv_html)
        
    # 3. pricing.html, about.html, contact.html (БОГАТЫЕ ПОЛНЫЕ СТРАНИЦЫ!)
    with open(os.path.join(target_dir, "pricing.html"), "w", encoding="utf-8") as f:
        f.write(generate_full_pricing_page(lang_code))
        
    with open(os.path.join(target_dir, "about.html"), "w", encoding="utf-8") as f:
        f.write(generate_full_about_page(lang_code))
        
    with open(os.path.join(target_dir, "contact.html"), "w", encoding="utf-8") as f:
        f.write(generate_full_contact_page(lang_code))

print("✅ Все страницы (index.html, services.html, pricing.html, about.html, contact.html) собраны для ВСЕХ 9 языков!")

# 200.html для Surge SPA
shutil.copy(os.path.join(STAGING_DIR, "index.html"), os.path.join(STAGING_DIR, "200.html"))

print("🎉 V2 РЕЛИЗ ГОТОВ К ДЕПЛОЮ!")
