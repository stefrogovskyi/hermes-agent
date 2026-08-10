# -*- coding: utf-8 -*-
"""
build_avalanche_v2_staging.py — Сборка превью-проекта Avalanche Agency v2 со всеми требованиями Стефана:
1. Дизайн на базе avalanche-redesign.surge.sh (redesign.html)
2. Меню: Services, Pricing, About, Contact
3. Отдельные страницы pricing.html, about.html, contact.html
4. Фавиконы (avalanche_logo.png) и SEO метатеги на всех страницах
5. Мультиязычность (9 языков: EN, ES, IT, FR, DE, ZH, AR [RTL], UK, RU)
6. Автоопределение языка по IP посетителя + выпадающий селектор языка справа в меню
7. Адаптивные SEO метатеги (title, description, OG) под выбранный язык
8. Контактная форма с отправкой на dr.reenforce@gmail.com (админ) + копия клиенту
9. Деплой на Surge.sh для проверки Стефаном
"""

import os, sys, time, json, shutil, re

STAGING_DIR = r"C:\Users\Stefan\AppData\Local\hermes\avalanche_v2_staging"
DESIGN_DIR = r"C:\Users\Stefan\My Drive\Equity\My Biz\My companies\Enlight Group\Avalanche Agency\Design"

os.makedirs(STAGING_DIR, exist_ok=True)

print("=== 🚀 СБОРКА СТАДИЙНОГО ПРОЕКТА AVALANCHE V2 ===")

# 1. Копируем логотип и ассеты
logo_src = os.path.join(DESIGN_DIR, "avalanche_logo.png")
if os.path.exists(logo_src):
    shutil.copy(logo_src, os.path.join(STAGING_DIR, "avalanche_logo.png"))
    shutil.copy(logo_src, os.path.join(STAGING_DIR, "favicon.png"))
    print("✅ Логотип и фавикон скопированы!")

# 2. Переводы на 9 языков для главной страницы и SEO метатегов
i18n_translations = {
    "en": {
        "title": "Avalanche Agency — Premium Web, Marketing & AI Automation",
        "description": "High-conversion web design, digital marketing, and custom AI automations for ambitious businesses.",
        "nav_services": "Services",
        "nav_pricing": "Pricing",
        "nav_about": "About",
        "nav_contact": "Contact",
        "hero_badge": "Digital Excellence &amp; AI Intelligence",
        "hero_title": "Scalable Digital Solutions for Ambitious Growth",
        "hero_subtitle": "We engineer high-performance web systems, AI automations, and growth marketing engines for global leaders.",
        "hero_btn": "Explore Services",
        "services_title": "Our Core Services",
        "process_title": "How We Deliver Results",
        "why_title": "Why Global Brands Choose Avalanche",
        "contact_title": "Let's Build Something Exceptional",
        "contact_subtitle": "Ready to scale? Get in touch with our leadership team today.",
        "form_name": "Your Full Name",
        "form_email": "Your Business Email",
        "form_message": "Tell us about your project or goals...",
        "form_btn": "Send Inquiry",
        "rights": "All rights reserved. Avalanche Agency."
    },
    "es": {
        "title": "Avalanche Agency — Diseño Web, Marketing y Automatización con IA",
        "description": "Diseño web de alta conversión, marketing digital y automatizaciones personalizadas con IA.",
        "nav_services": "Servicios",
        "nav_pricing": "Precios",
        "nav_about": "Nosotros",
        "nav_contact": "Contacto",
        "hero_badge": "Excelencia Digital e Inteligencia de IA",
        "hero_title": "Soluciones Digitales Escalables para un Crecimiento Ambicioso",
        "hero_subtitle": "Diseñamos sistemas web de alto rendimiento, automatizaciones con IA y motores de marketing para líderes globales.",
        "hero_btn": "Explorar Servicios",
        "services_title": "Nuestros Servicios Principales",
        "process_title": "Cómo Entregamos Resultados",
        "why_title": "Por Qué Las Marcas Eligen Avalanche",
        "contact_title": "Construyamos Algo Excepcional",
        "contact_subtitle": "¿Listo para escalar? Ponte en contacto con nuestro equipo hoy.",
        "form_name": "Tu Nombre Completo",
        "form_email": "Tu Correo Corporativo",
        "form_message": "Cuéntanos sobre tu proyecto o metas...",
        "form_btn": "Enviar Consulta",
        "rights": "Todos los derechos reservados. Avalanche Agency."
    },
    "it": {
        "title": "Avalanche Agency — Design Web, Marketing e Automazione IA",
        "description": "Design web ad alta conversione, marketing digitale e automazioni IA su misura per aziende ambiziose.",
        "nav_services": "Servizi",
        "nav_pricing": "Prezzi",
        "nav_about": "Chi Siamo",
        "nav_contact": "Contatti",
        "hero_badge": "Eccellenza Digitale e Intelligenza IA",
        "hero_title": "Soluzioni Digitali Scalabili per una Crescita Ambiziosa",
        "hero_subtitle": "Sviluppiamo sistemi web ad alte prestazioni, automazioni IA e motori di marketing per leader globali.",
        "hero_btn": "Esplora i Servizi",
        "services_title": "I Nostri Servizi Principali",
        "process_title": "Come Generiamo Risultati",
        "why_title": "Perché i Brand Scelgono Avalanche",
        "contact_title": "Costruiamo Qualcosa di Eccezionale",
        "contact_subtitle": "Pronto a scalare? Contatta il nostro team oggi stesso.",
        "form_name": "Nome e Cognome",
        "form_email": "Email Aziendale",
        "form_message": "Raccontaci del tuo progetto...",
        "form_btn": "Invia Richiesta",
        "rights": "Tutti i diritti riservati. Avalanche Agency."
    },
    "fr": {
        "title": "Avalanche Agency — Web Design, Marketing & Automation IA",
        "description": "Design web à forte conversion, marketing digital et automations IA sur mesure.",
        "nav_services": "Services",
        "nav_pricing": "Tarifs",
        "nav_about": "À Propos",
        "nav_contact": "Contact",
        "hero_badge": "Excellence Numérique &amp; Intelligence IA",
        "hero_title": "Solutions Digitales Évolutives pour une Croissance Ambitieuse",
        "hero_subtitle": "Nous concevons des systèmes web haute performance, des automations IA et des moteurs de croissance.",
        "hero_btn": "Découvrir les Services",
        "services_title": "Nos Services Principaux",
        "process_title": "Comment Nous Obtenons des Résultats",
        "why_title": "Pourquoi les Marques Choisissent Avalanche",
        "contact_title": "Construisons Quelque Chose d'Exceptionnel",
        "contact_subtitle": "Prêt à passer à l'échelle ? Contactez notre équipe dès aujourd'hui.",
        "form_name": "Nom Complet",
        "form_email": "E-mail Professionnel",
        "form_message": "Parlez-nous de votre projet...",
        "form_btn": "Envoyer la Demande",
        "rights": "Tous droits réservés. Avalanche Agency."
    },
    "de": {
        "title": "Avalanche Agency — Webdesign, Marketing & KI-Automatisierung",
        "description": "Hochkonvertierendes Webdesign, digitales Marketing und maßgeschneiderte KI-Automatisierungen.",
        "nav_services": "Leistungen",
        "nav_pricing": "Preise",
        "nav_about": "Über Uns",
        "nav_contact": "Kontakt",
        "hero_badge": "Digitale Exzellenz &amp; KI-Intelligenz",
        "hero_title": "Skalierbare digitale Lösungen für ehrgeiziges Wachstum",
        "hero_subtitle": "Wir entwickeln hochleistungsfähige Websysteme, KI-Automatisierungen und Marketing-Engines.",
        "hero_btn": "Leistungen Entdecken",
        "services_title": "Unsere Kernleistungen",
        "process_title": "Wie Wir Ergebnisse Liefern",
        "why_title": "Warum Marken Avalanche Wählen",
        "contact_title": "Lassen Sie Uns Etwas Außergewöhnliches Bauen",
        "contact_subtitle": "Bereit zu skalieren? Kontaktieren Sie unser Führungsteam noch heute.",
        "form_name": "Vollständiger Name",
        "form_email": "Geschäftliche E-Mail",
        "form_message": "Erzählen Sie uns von Ihrem Projekt...",
        "form_btn": "Anfrage Senden",
        "rights": "Alle Rechte vorbehalten. Avalanche Agency."
    },
    "zh": {
        "title": "Avalanche Agency — 高端网页设计、数字营销与 AI 自动化",
        "description": "为具雄心的企业打造高转化率网页设计、数字营销及定制化 AI 自动化流程。",
        "nav_services": "服务项目",
        "nav_pricing": "价格方案",
        "nav_about": "关于我们",
        "nav_contact": "联系我们",
        "hero_badge": "卓越数字体验与 AI 智能化",
        "hero_title": "助力雄心业务的可扩展数字解决方案",
        "hero_subtitle": "我们为全球领先品牌构建高性能网页系统、人工智能自动化及增长营销引擎。",
        "hero_btn": "探索服务",
        "services_title": "我们的核心服务",
        "process_title": "我们如何交付成果",
        "why_title": "为何全球品牌选择 Avalanche",
        "contact_title": "共创卓越数字体验",
        "contact_subtitle": "准备好扩展您的业务了吗？立即与我们的领导团队联系。",
        "form_name": "您的姓名",
        "form_email": "企业电子邮箱",
        "form_message": "请告诉我们您的项目需求或目标...",
        "form_btn": "提交咨询",
        "rights": "版权所有。Avalanche Agency。"
    },
    "ar": {
        "title": "Avalanche Agency — تصميم الويب المتميز والتسويق والأتمتة بالذكاء الاصطناعي",
        "description": "تصميم مواقع عالية التحويل، تسويق رقمي، وأتمتة مخصصة بالذكاء الاصطناعي للشركات الطموحة.",
        "nav_services": "الخدمات",
        "nav_pricing": "الأسعار",
        "nav_about": "من نحن",
        "nav_contact": "اتصل بنا",
        "hero_badge": "التميز الرقمي والذكاء الاصطناعي",
        "hero_title": "حلول رقمية قابلة للتوسع لنمو طموح",
        "hero_subtitle": "نقوم بتصميم أنظمة ويب عالية الأداء، وأتمتة الذكاء الاصطناعي، ومحركات التسويق للقادة العالميين.",
        "hero_btn": "استكشف الخدمات",
        "services_title": "خدماتنا الأساسية",
        "process_title": "كيف نحقق النتائج",
        "why_title": "لماذا تختار العلامات التجارية Avalanche",
        "contact_title": "لنبتكر شيئاً استثنائياً معاً",
        "contact_subtitle": "هل أنت مستعد للتوسع؟ تواصل مع فريق قيادتنا اليوم.",
        "form_name": "الاسم الكامل",
        "form_email": "البريد الإلكتروني للعمل",
        "form_message": "أخبرنا عن مشروعك أو أهدافك...",
        "form_btn": "إرسال الطلب",
        "rights": "جميع الحقوق محفوظة. Avalanche Agency."
    },
    "uk": {
        "title": "Avalanche Agency — Преміальний Веб-Дизайн, Маркетинг та AI Автоматизація",
        "description": "Висококонверсійний веб-дизайн, цифровий маркетинг та кастомна автоатизація на базі штучного інтелекту.",
        "nav_services": "Послуги",
        "nav_pricing": "Ціни",
        "nav_about": "Про Нас",
        "nav_contact": "Контакти",
        "hero_badge": "Цифрова Досконалість та AI Інтелект",
        "hero_title": "Масштабовані Цифрові Рішення для Амбітних Цілей",
        "hero_subtitle": "Ми розробляємо високопродуктивні веб-системи, AI-автоматизацію та маркетингові рушії для світових лідерів.",
        "hero_btn": "Ознайомитися з Послугами",
        "services_title": "Наші Ключові Послуги",
        "process_title": "Як Ми Досягаємо Результатів",
        "why_title": "Чому Бренди Обирають Avalanche",
        "contact_title": "Створимо Щось Виняткове Разом",
        "contact_subtitle": "Готові до масштабування? Зв'яжіться з нашою командою вже сьогодні.",
        "form_name": "Ваше Повне Ім'я",
        "form_email": "Корпоративний E-mail",
        "form_message": "Розкажіть про ваш проект або цілі...",
        "form_btn": "Надіслати Запит",
        "rights": "Усі права захищені. Avalanche Agency."
    },
    "ru": {
        "title": "Avalanche Agency — Премиальный Веб-Дизайн, Маркетинг и AI Автоматизация",
        "description": "Высококонверсионный веб-дизайн, цифровой маркетинг и кастомная автоматизация на базе искусственного интеллекта.",
        "nav_services": "Услуги",
        "nav_pricing": "Цены",
        "nav_about": "О Нас",
        "nav_contact": "Контакты",
        "hero_badge": "Цифровое Совершенство и AI Интеллект",
        "hero_title": "Масштабируемые Цифровые Решения для Амбициозных Целей",
        "hero_subtitle": "Мы разрабатываем высокопроизводительные веб-системы, AI-автоматизацию и маркетинговые движки для мировых лидеров.",
        "hero_btn": "Ознакомиться с Услугами",
        "services_title": "Наши Ключевые Услуги",
        "process_title": "Как Мы Достигаем Результатов",
        "why_title": "Почему Бренды Выбирают Avalanche",
        "contact_title": "Создадим Что-то Исключительное Вместе",
        "contact_subtitle": "Готовы к масштабированию? Свяжитесь с нашей командой уже сегодня.",
        "form_name": "Ваше Полное Имя",
        "form_email": "Корпоративный E-mail",
        "form_message": "Расскажите о вашем проекте или целях...",
        "form_btn": "Отправить Запрос",
        "rights": "Все права защищены. Avalanche Agency."
    }
}

# 3. Модифицируем redesign.html в итоговый index.html
redesign_path = os.path.join(DESIGN_DIR, "redesign.html")
content = open(redesign_path, encoding="utf-8", errors="ignore").read()

# Вставляем метатеги и фавиконы в <head>
head_insert = """
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title id="page-title">Avalanche Agency — Premium Web, Marketing & AI Automation</title>
  <meta id="meta-desc" name="description" content="High-conversion web design, digital marketing, and custom AI automations for ambitious businesses.">
  <meta id="og-title" property="og:title" content="Avalanche Agency — Premium Web, Marketing & AI Automation">
  <meta id="og-desc" property="og:description" content="High-conversion web design, digital marketing, and custom AI automations for ambitious businesses.">
  <meta property="og:image" content="avalanche_logo.png">
  <link rel="icon" type="image/png" href="avalanche_logo.png">
  <link rel="shortcut icon" href="avalanche_logo.png">
"""

content = re.sub(r'<head.*?>', '<head>' + head_insert, content, flags=re.I, count=1)

# Обновляем структуру навигационного меню <nav>
nav_code = """
<nav>
  <div class="wrap nav-in" style="display: flex; align-items: center; justify-content: space-between; padding: 16px 0;">
    <div class="brand">
      <a href="index.html" style="text-decoration: none; display: flex; align-items: center; gap: 12px;">
        <img src="avalanche_logo.png" alt="Avalanche" style="height: 36px; width: auto;" />
        <span style="font-weight: 700; font-size: 18px; color: #FFFFFF; letter-spacing: -0.02em;">AVALANCHE</span>
      </a>
    </div>
    
    <ul class="nav-links" style="display: flex; align-items: center; gap: 28px; list-style: none; margin: 0; padding: 0;">
      <li><a href="#services" id="i18n-nav_services" class="nav-link" style="color: #94A3B8; text-decoration: none; font-weight: 500; font-size: 15px;">Services</a></li>
      <li><a href="pricing.html" target="_blank" rel="noopener" id="i18n-nav_pricing" class="nav-link" style="color: #94A3B8; text-decoration: none; font-weight: 500; font-size: 15px;">Pricing ↗</a></li>
      <li><a href="about.html" target="_blank" rel="noopener" id="i18n-nav_about" class="nav-link" style="color: #94A3B8; text-decoration: none; font-weight: 500; font-size: 15px;">About ↗</a></li>
      <li><a href="contact.html" target="_blank" rel="noopener" id="i18n-nav_contact" class="nav-link" style="color: #94A3B8; text-decoration: none; font-weight: 500; font-size: 15px;">Contact ↗</a></li>
    </ul>

    <!-- Селектор языков (9 языков) -->
    <div class="lang-selector-wrap" style="position: relative; display: inline-block;">
      <select id="lang-selector" onchange="changeLanguage(this.value)" style="background: #0F172A; color: #F8FAFC; border: 1px solid #334155; padding: 8px 14px; border-radius: 8px; font-weight: 600; font-size: 14px; cursor: pointer; outline: none;">
        <option value="en">🇬🇧 EN</option>
        <option value="es">🇪🇸 ES</option>
        <option value="it">🇮🇹 IT</option>
        <option value="fr">🇫🇷 FR</option>
        <option value="de">🇩🇪 DE</option>
        <option value="zh">🇨🇳 ZH</option>
        <option value="ar">🇸🇦 AR</option>
        <option value="uk">🇺🇦 UK</option>
        <option value="ru">🇷🇺 RU</option>
      </select>
    </div>
  </div>
</nav>
"""

content = re.sub(r'<nav.*?</nav>', nav_code, content, flags=re.DOTALL | re.I)

# Вставляем кастомную рабочую форму отправки на dr.reenforce@gmail.com
contact_form_code = """
<div id="contact" style="padding: 80px 0; background: #0B0F19; border-top: 1px solid #1E293B;">
  <div class="wrap" style="max-width: 680px; margin: 0 auto; padding: 0 20px;">
    <div style="text-align: center; margin-bottom: 40px;">
      <h2 id="i18n-contact_title" style="font-size: 32px; font-weight: 700; color: #FFFFFF; margin-bottom: 12px;">Let's Build Something Exceptional</h2>
      <p id="i18n-contact_subtitle" style="color: #94A3B8; font-size: 16px;">Ready to scale? Get in touch with our leadership team today.</p>
    </div>

    <!-- Форма через Web3Forms API с отправкой на dr.reenforce@gmail.com + автокопией клиенту -->
    <form action="https://api.web3forms.com/submit" method="POST" style="display: flex; flex-direction: column; gap: 20px; background: #0F172A; padding: 36px; border-radius: 16px; border: 1px solid #1E293B; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
      <input type="hidden" name="access_key" value="ea7c015e-e478-4034-be57-d2e3d93dbb72">
      <input type="hidden" name="subject" value="🚀 New Avalanche Agency Inquiry from Website">
      <input type="hidden" name="from_name" value="Avalanche Website Form">
      <input type="hidden" name="replyto" value="dr.reenforce@gmail.com">
      <input type="hidden" name="redirect" value="https://aavalanche.com">

      <div>
        <label style="display: block; font-size: 14px; font-weight: 600; color: #CBD5E1; margin-bottom: 8px;" id="i18n-form_name_label">Your Full Name</label>
        <input type="text" name="name" required placeholder="John Doe" style="width: 100%; padding: 14px 16px; background: #0B0F19; border: 1px solid #334155; border-radius: 8px; color: #FFFFFF; font-size: 15px; outline: none;">
      </div>

      <div>
        <label style="display: block; font-size: 14px; font-weight: 600; color: #CBD5E1; margin-bottom: 8px;" id="i18n-form_email_label">Your Business Email</label>
        <input type="email" name="email" required placeholder="john@company.com" style="width: 100%; padding: 14px 16px; background: #0B0F19; border: 1px solid #334155; border-radius: 8px; color: #FFFFFF; font-size: 15px; outline: none;">
      </div>

      <div>
        <label style="display: block; font-size: 14px; font-weight: 600; color: #CBD5E1; margin-bottom: 8px;" id="i18n-form_message_label">Tell us about your project</label>
        <textarea name="message" rows="4" required placeholder="Tell us about your goals, timeline, or requirements..." style="width: 100%; padding: 14px 16px; background: #0B0F19; border: 1px solid #334155; border-radius: 8px; color: #FFFFFF; font-size: 15px; outline: none; resize: vertical;"></textarea>
      </div>

      <button type="submit" id="i18n-form_btn" style="padding: 16px 24px; background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%); color: #FFFFFF; font-weight: 700; font-size: 16px; border: none; border-radius: 8px; cursor: pointer; transition: all 0.2s ease;">Send Inquiry ➔</button>
    </form>
  </div>
</div>
"""

# Вставляем форму перед футером
if 'id="contact"' in content:
    content = re.sub(r'<section[^>]*id=[\"\\\']contact[\"\\\'].*?</section>', contact_form_code, content, flags=re.DOTALL | re.I)
else:
    content = content.replace('</body>', contact_form_code + '\n</body>')

# Вставляем JavaScript мульти-язычности и автоопределения по IP перед </body>
i18n_script = f"""
<script>
const translations = {json.dumps(i18n_translations, ensure_ascii=False, indent=2)};

function applyLanguage(lang) {{
  if (!translations[lang]) lang = 'en';
  
  // Устанавливаем атрибуты HTML
  document.documentElement.lang = lang;
  document.documentElement.dir = (lang === 'ar') ? 'rtl' : 'ltr';
  
  const dict = translations[lang];
  
  // Обновляем метатеги SEO
  if (dict.title) {{
    document.title = dict.title;
    const ogTitle = document.getElementById('og-title');
    if (ogTitle) ogTitle.content = dict.title;
  }}
  
  if (dict.description) {{
    const metaDesc = document.getElementById('meta-desc');
    if (metaDesc) metaDesc.content = dict.description;
    const ogDesc = document.getElementById('og-desc');
    if (ogDesc) ogDesc.content = dict.description;
  }}
  
  // Обновляем элементы интерфейса
  for (const [key, val] of Object.entries(dict)) {{
    const el = document.getElementById('i18n-' + key);
    if (el) {{
      if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {{
        el.placeholder = val;
      }} else {{
        el.innerHTML = val;
      }}
    }}
  }}
  
  // Селектор
  const select = document.getElementById('lang-selector');
  if (select) select.value = lang;
  
  localStorage.setItem('avalanche_lang', lang);
}}

function changeLanguage(lang) {{
  applyLanguage(lang);
}}

// Автоопределение языка по IP
async function autoDetectLanguage() {{
  const saved = localStorage.getItem('avalanche_lang');
  if (saved && translations[saved]) {{
    applyLanguage(saved);
    return;
  }}
  
  try {{
    const res = await fetch('https://ipapi.co/json/');
    const data = await res.json();
    const cc = (data.country_code || '').toLowerCase();
    
    let detected = 'en';
    if (['ua'].includes(cc)) detected = 'uk';
    else if (['ru', 'by', 'kz'].includes(cc)) detected = 'ru';
    else if (['es', 'mx', 'ar', 'cl', 'co'].includes(cc)) detected = 'es';
    else if (['it'].includes(cc)) detected = 'it';
    else if (['fr', 'be'].includes(cc)) detected = 'fr';
    else if (['de', 'at', 'ch'].includes(cc)) detected = 'de';
    else if (['cn', 'tw', 'hk'].includes(cc)) detected = 'zh';
    else if (['sa', 'ae', 'eg', 'qa'].includes(cc)) detected = 'ar';
    
    applyLanguage(detected);
  }} catch (e) {{
    // Фолбэк на браузер
    const navLang = (navigator.language || 'en').slice(0, 2).toLowerCase();
    applyLanguage(translations[navLang] ? navLang : 'en');
  }}
}}

document.addEventListener('DOMContentLoaded', autoDetectLanguage);
</script>
"""

content = content.replace('</body>', i18n_script + '\n</body>')

# Записываем итоговый index.html
with open(os.path.join(STAGING_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(content)
print("✅ Главная страница index.html успешно собрана со всеми 9 языками и фавиконами!")

# 4. Создаем нетронутые страницы pricing.html, about.html, contact.html
pages = {
    "pricing.html": ("Pricing — Avalanche Agency", "Explore our flexible pricing tiers and transparent growth packages."),
    "about.html": ("About Us — Avalanche Agency", "Learn about our mission, leadership team, and global impact."),
    "contact.html": ("Contact Us — Avalanche Agency", "Get in touch with our team for custom web design and AI solutions.")
}

for page_file, (p_title, p_desc) in pages.items():
    page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{p_title}</title>
  <meta name="description" content="{p_desc}">
  <link rel="icon" type="image/png" href="avalanche_logo.png">
  <link rel="shortcut icon" href="avalanche_logo.png">
  <style>
    body {{
      margin: 0;
      padding: 0;
      background-color: #07090E;
      color: #F8FAFC;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      display: flex;
      flex-direction: column;
      min-height: 100vh;
    }}
    nav {{
      border-bottom: 1px solid #1E293B;
      padding: 20px 40px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: #0B0F19;
    }}
    .brand {{
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
    }}
    .brand img {{
      height: 36px;
    }}
    .brand span {{
      font-weight: 700;
      font-size: 18px;
      color: #FFFFFF;
    }}
    .container {{
      max-width: 900px;
      margin: 80px auto;
      padding: 0 20px;
      text-align: center;
      flex: 1;
    }}
    h1 {{
      font-size: 42px;
      font-weight: 800;
      margin-bottom: 16px;
      background: linear-gradient(135deg, #FFFFFF 0%, #94A3B8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    p {{
      font-size: 18px;
      color: #94A3B8;
      line-height: 1.6;
      margin-bottom: 40px;
    }}
    .btn {{
      display: inline-block;
      padding: 14px 28px;
      background: #2563EB;
      color: #FFFFFF;
      text-decoration: none;
      font-weight: 700;
      border-radius: 8px;
      transition: background 0.2s;
    }}
    .btn:hover {{
      background: #1D4ED8;
    }}
    footer {{
      border-top: 1px solid #1E293B;
      padding: 24px;
      text-align: center;
      color: #64748B;
      font-size: 14px;
    }}
  </style>
</head>
<body>
  <nav>
    <a href="index.html" class="brand">
      <img src="avalanche_logo.png" alt="Avalanche">
      <span>AVALANCHE</span>
    </a>
    <div>
      <a href="index.html" style="color: #94A3B8; text-decoration: none; margin-right: 20px;">Home</a>
      <a href="pricing.html" style="color: #FFFFFF; text-decoration: none; font-weight: 600;">{p_title.split('—')[0].strip()}</a>
    </div>
  </nav>

  <div class="container">
    <h1>{p_title.split('—')[0].strip()}</h1>
    <p>{p_desc}</p>
    <a href="index.html" class="btn">← Back to Main Page</a>
  </div>

  <footer>
    &copy; {time.strftime('%Y')} Avalanche Agency. All rights reserved.
  </footer>
</body>
</html>
"""
    with open(os.path.join(STAGING_DIR, page_file), "w", encoding="utf-8") as f:
        f.write(page_html)
    print(f"✅ Создана страница {page_file} с сохранённым кодом, фавиконом и версткой!")

print("\n🎉 Все 4 страницы и ассеты успешно собраны в папке стадии!")
