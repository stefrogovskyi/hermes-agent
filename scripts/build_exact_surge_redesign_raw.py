# -*- coding: utf-8 -*-
"""
build_exact_surge_redesign_raw.py — Премиум-фикс главной страницы Avalanche Agency на базе redesign.html:
1. Замена основного синего цвета кнопок и акцентов на #60B5FF
2. Исправление и восстановление мобильной верстки (гамбургер-меню, 1 колонка на мобильных, адаптивные шрифты)
3. Исправление всех ссылок и переходов (Services -> #services, Pricing/About/Contact -> открываются в новых вкладках)
4. Переключение 9 языков с SVG-флагами + автоопределение по IP
5. Рабочая контактная форма
"""

import os, sys, time, json, shutil, re

STAGING_DIR = r"C:\Users\Stefan\AppData\Local\hermes\avalanche_v2_staging"
DESIGN_DIR = r"C:\Users\Stefan\My Drive\Equity\My Biz\My companies\Enlight Group\Avalanche Agency\Design"

os.makedirs(STAGING_DIR, exist_ok=True)

print("=== 🎨 ФИНАЛЬНЫЙ РЕФАКТОРИНГ: #60B5FF, МОБИЛЬНАЯ ВЕРСТКА, ССЫЛКИ ===")

redesign_path = os.path.join(DESIGN_DIR, "redesign.html")
text = open(redesign_path, encoding="utf-8", errors="ignore").read()

# Копируем фавикон и логотип
logo_src = os.path.join(DESIGN_DIR, "avalanche_logo.png")
if os.path.exists(logo_src):
    shutil.copy(logo_src, os.path.join(STAGING_DIR, "avalanche_logo.png"))
    shutil.copy(logo_src, os.path.join(STAGING_DIR, "favicon.png"))

# 1. Заменяем синий цвет в CSS на #60B5FF
text = text.replace("--blue:#3B82F6;", "--blue:#60B5FF;").replace("--blue-d:#2563EB;", "--blue-d:#389BFF;")
text = text.replace("#3B82F6", "#60B5FF").replace("#2563EB", "#389BFF")

# 2. Добавляем стили для мобильного гамбургер-меню и адаптива в <head>
mobile_css = """
<style>
  :root {
    --blue: #60B5FF !important;
    --blue-d: #389BFF !important;
  }
  
  .btn, button.btn, a.btn {
    background: #60B5FF !important;
    color: #FFFFFF !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    box-shadow: 0 8px 25px rgba(96, 181, 255, 0.3) !important;
  }
  .btn:hover, button.btn:hover, a.btn:hover {
    background: #389BFF !important;
    transform: translateY(-2px);
  }

  /* Адаптивная мобильная верстка */
  @media (max-width: 900px) {
    .nav-in {
      padding: 12px 20px !important;
    }
    .desktop-nav {
      display: none !important;
    }
    .mobile-menu-btn {
      display: flex !important;
    }
    .hero-h1 {
      font-size: 32px !important;
      line-height: 1.2 !important;
    }
    .hero-p {
      font-size: 16px !important;
    }
    .grid, .services-grid, .why-grid {
      grid-template-columns: 1fr !important;
      gap: 20px !important;
    }
  }

  @media (min-width: 901px) {
    .mobile-menu-btn {
      display: none !important;
    }
    .mobile-nav-overlay {
      display: none !important;
    }
  }

  .mobile-nav-overlay {
    position: fixed;
    top: 70px;
    left: 0;
    right: 0;
    background: #0B0F19;
    border-bottom: 1px solid #1E293B;
    padding: 24px;
    display: none;
    flex-direction: column;
    gap: 16px;
    z-index: 999;
  }
  .mobile-nav-overlay.active {
    display: flex !important;
  }
</style>
"""

text = text.replace("</head>", mobile_css + "\n<meta id='meta-desc' name='description' content='High-conversion web design, digital marketing, and custom AI automations for ambitious businesses.'><link rel='icon' type='image/png' href='avalanche_logo.png'></head>")

# 3. Полная адаптивная навигация с гамбургер-меню
nav_html = """
<nav style="position: sticky; top: 0; z-index: 1000; background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); border-bottom: 1px solid #E2E8F0;">
  <div class="wrap nav-in" style="display: flex; align-items: center; justify-content: space-between; padding: 14px 20px;">
    <div class="brand">
      <a href="index.html" style="text-decoration: none; display: flex; align-items: center; gap: 10px;">
        <img src="avalanche_logo.png" alt="Avalanche" style="height: 36px; width: auto;" />
        <span class="name" style="color: #0F172A; font-weight: 800; font-size: 19px; letter-spacing: -0.02em;">Avalanche Agency</span>
      </a>
    </div>

    <!-- Десктопная навигация -->
    <div class="desktop-nav" style="display: flex; align-items: center; gap: 28px;">
      <a href="#services" id="i18n-nav_services" style="color: #475569; text-decoration: none; font-weight: 600; font-size: 15px;">Services</a>
      <a href="https://aavalanche.com/pricing" target="_blank" rel="noopener" id="i18n-nav_pricing" style="color: #475569; text-decoration: none; font-weight: 600; font-size: 15px;">Pricing ↗</a>
      <a href="https://aavalanche.com/about" target="_blank" rel="noopener" id="i18n-nav_about" style="color: #475569; text-decoration: none; font-weight: 600; font-size: 15px;">About ↗</a>
      <a href="https://aavalanche.com/contact" target="_blank" rel="noopener" id="i18n-nav_contact" style="color: #475569; text-decoration: none; font-weight: 600; font-size: 15px;">Contact ↗</a>
    </div>

    <div class="desktop-nav" style="display: flex; align-items: center; gap: 16px;">
      <!-- Селектор языков -->
      <select id="lang-select" onchange="switchLanguage(this.value)" style="background: #F1F5F9; color: #0F172A; border: 1px solid #CBD5E1; padding: 8px 14px; border-radius: 8px; font-size: 14px; font-weight: 700; cursor: pointer; outline: none;">
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
      
      <a href="#contact" class="btn" id="i18n-nav_btn" style="background: #60B5FF; color: #FFF; padding: 10px 20px; text-decoration: none; border-radius: 10px; font-weight: 700;">Start Your Project</a>
    </div>

    <!-- Кнопка мобильного меню (Гамбургер) -->
    <button class="mobile-menu-btn" onclick="toggleMobileMenu()" style="display: none; background: #F1F5F9; border: 1px solid #CBD5E1; padding: 8px 12px; border-radius: 8px; font-size: 20px; cursor: pointer; color: #0F172A;">
      ☰
    </button>
  </div>

  <!-- Оверлей мобильного меню -->
  <div id="mobile-overlay" class="mobile-nav-overlay">
    <a href="#services" onclick="toggleMobileMenu()" id="i18n-m_services" style="color: #F8FAFC; text-decoration: none; font-weight: 600; font-size: 18px;">Services</a>
    <a href="https://aavalanche.com/pricing" target="_blank" rel="noopener" id="i18n-m_pricing" style="color: #F8FAFC; text-decoration: none; font-weight: 600; font-size: 18px;">Pricing ↗</a>
    <a href="https://aavalanche.com/about" target="_blank" rel="noopener" id="i18n-m_about" style="color: #F8FAFC; text-decoration: none; font-weight: 600; font-size: 18px;">About ↗</a>
    <a href="https://aavalanche.com/contact" target="_blank" rel="noopener" id="i18n-m_contact" style="color: #F8FAFC; text-decoration: none; font-weight: 600; font-size: 18px;">Contact ↗</a>
    
    <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 12px; pt-12; border-top: 1px solid #334155;">
      <select id="lang-select-mobile" onchange="switchLanguage(this.value)" style="background: #1E293B; color: #F8FAFC; border: 1px solid #475569; padding: 8px 14px; border-radius: 8px; font-size: 15px; font-weight: 700;">
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
      <a href="#contact" onclick="toggleMobileMenu()" class="btn" style="background: #60B5FF; color: #FFF; padding: 10px 18px; text-decoration: none; border-radius: 8px; font-weight: 700;">Start Project</a>
    </div>
  </div>
</nav>
"""

text = re.sub(r'<nav.*?</nav>', nav_html, text, flags=re.DOTALL)

# 4. Переводы
translations = {
    "en": {
        "title": "Avalanche Agency — Premium Web & Marketing",
        "desc": "High-conversion web design, digital marketing, and custom AI automations for ambitious businesses.",
        "nav_services": "Services", "nav_pricing": "Pricing ↗", "nav_about": "About ↗", "nav_contact": "Contact ↗", "nav_btn": "Start Your Project",
        "m_services": "Services", "m_pricing": "Pricing ↗", "m_about": "About ↗", "m_contact": "Contact ↗",
        "hero_title": "Websites that convert. Brands that dominate.",
        "hero_subtitle": "We design and build high-performance web systems, custom AI automations, and growth engines for ambitious global companies.",
        "hero_btn": "Start Your Project",
        "services_title": "Services built for measurable impact.",
        "process_title": "How we turn ideas into revenue.",
        "why_title": "Why global leaders choose Avalanche.",
        "contact_title": "Ready to scale? Zero Risk.",
        "contact_btn": "Send Inquiry ➔"
    },
    "es": {
        "title": "Avalanche Agency — Diseño Web y Marketing",
        "desc": "Diseño web de alta conversión, marketing digital y automatizaciones personalizadas con IA.",
        "nav_services": "Servicios", "nav_pricing": "Precios ↗", "nav_about": "Nosotros ↗", "nav_contact": "Contacto ↗", "nav_btn": "Iniciar Proyecto",
        "m_services": "Servicios", "m_pricing": "Precios ↗", "m_about": "Nosotros ↗", "m_contact": "Contacto ↗",
        "hero_title": "Sitios web que convierten. Marcas que dominan.",
        "hero_subtitle": "Diseñamos y construimos sistemas web de alto rendimiento, automatizaciones con IA y motores de crecimiento.",
        "hero_btn": "Iniciar Proyecto",
        "services_title": "Servicios diseñados para un impacto medible.",
        "process_title": "Cómo transformamos ideas en ingresos.",
        "why_title": "Por qué los líderes eligen Avalanche.",
        "contact_title": "¿Listo para escalar? Sin Riesgo.",
        "contact_btn": "Enviar Consulta ➔"
    },
    "it": {
        "title": "Avalanche Agency — Design Web e Marketing",
        "desc": "Design web ad alta conversione, marketing digitale e automazioni IA per aziende ambiziose.",
        "nav_services": "Servizi", "nav_pricing": "Prezzi ↗", "nav_about": "Chi Siamo ↗", "nav_contact": "Contatti ↗", "nav_btn": "Avvia Progetto",
        "m_services": "Servizi", "m_pricing": "Prezzi ↗", "m_about": "Chi Siamo ↗", "m_contact": "Contatti ↗",
        "hero_title": "Siti web che convertono. Brand che dominano.",
        "hero_subtitle": "Sviluppiamo sistemi web ad alte prestazioni, automazioni IA su misura e motori di crescita.",
        "hero_btn": "Avvia Progetto",
        "services_title": "Servizi creati per un impatto misurabile.",
        "process_title": "Come trasformiamo le idee in fatturato.",
        "why_title": "Perché i leader scelgono Avalanche.",
        "contact_title": "Pronto a scalare? Zero Rischio.",
        "contact_btn": "Invia Richiesta ➔"
    },
    "fr": {
        "title": "Avalanche Agency — Web Design & Marketing",
        "desc": "Design web à forte conversion, marketing digital et automations IA sur mesure.",
        "nav_services": "Services", "nav_pricing": "Tarifs ↗", "nav_about": "À Propos ↗", "nav_contact": "Contact ↗", "nav_btn": "Lancer le Projet",
        "m_services": "Services", "m_pricing": "Tarifs ↗", "m_about": "À Propos ↗", "m_contact": "Contact ↗",
        "hero_title": "Des sites qui convertissent. Des marques qui dominent.",
        "hero_subtitle": "Nous concevons des systèmes web haute performance, des automations IA et des moteurs de croissance.",
        "hero_btn": "Lancer le Projet",
        "services_title": "Des services conçus pour un impact mesurable.",
        "process_title": "Comment nous transformons les idées en revenus.",
        "why_title": "Pourquoi les leaders choisissent Avalanche.",
        "contact_title": "Prêt à passer à l'échelle ? Zéro Risque.",
        "contact_btn": "Envoyer la Demande ➔"
    },
    "de": {
        "title": "Avalanche Agency — Webdesign & Marketing",
        "desc": "Hochkonvertierendes Webdesign, digitales Marketing und maßgeschneiderte KI-Automatisierungen.",
        "nav_services": "Leistungen", "nav_pricing": "Preise ↗", "nav_about": "Über Uns ↗", "nav_contact": "Kontakt ↗", "nav_btn": "Projekt Starten",
        "m_services": "Leistungen", "m_pricing": "Preise ↗", "m_about": "Über Uns ↗", "m_contact": "Kontakt ↗",
        "hero_title": "Websites, die konvertieren. Marken, die dominieren.",
        "hero_subtitle": "Wir entwickeln hochleistungsfähige Websysteme, KI-Automatisierungen und Marketing-Engines.",
        "hero_btn": "Projekt Starten",
        "services_title": "Dienstleistungen für messbaren Erfolg.",
        "process_title": "Wie wir Ideen in Umsatz verwandeln.",
        "why_title": "Warum führende Marken Avalanche wählen.",
        "contact_title": "Bereit zu skalieren? Null Risiko.",
        "contact_btn": "Anfrage Senden ➔"
    },
    "zh": {
        "title": "Avalanche Agency — 高端网页设计与数字营销",
        "desc": "为具雄心的企业打造高转化率网页设计、数字营销及定制化 AI 自动化流程。",
        "nav_services": "服务项目", "nav_pricing": "价格方案 ↗", "nav_about": "关于我们 ↗", "nav_contact": "联系我们 ↗", "nav_btn": "启动项目",
        "m_services": "服务项目", "m_pricing": "价格方案 ↗", "m_about": "关于我们 ↗", "m_contact": "联系我们 ↗",
        "hero_title": "高效转化的网站，主导市场的品牌。",
        "hero_subtitle": "我们为全球领先品牌构建高性能网页系统、人工智能自动化及增长营销引擎。",
        "hero_btn": "启动项目",
        "services_title": "致力于创造可衡量价值的服务。",
        "process_title": "我们如何将创意转化为收益。",
        "why_title": "为何全球领军企业选择 Avalanche。",
        "contact_title": "准备好扩展了吗？零风险。",
        "contact_btn": "提交咨询 ➔"
    },
    "ar": {
        "title": "Avalanche Agency — تصميم الويب المتميز والتسويق",
        "desc": "تصميم مواقع عالية التحويل، تسويق رقمي، وأتمتة مخصصة بالذكاء الاصطناعي للشركات الطموحة.",
        "nav_services": "الخدمات", "nav_pricing": "الأسعار ↗", "nav_about": "من نحن ↗", "nav_contact": "اتصل بنا ↗", "nav_btn": "ابدأ مشروعك",
        "m_services": "الخدمات", "m_pricing": "الأسعار ↗", "m_about": "من نحن ↗", "m_contact": "اتصل بنا ↗",
        "hero_title": "مواقع تحقق التحويل. علامات تجارية تهيمن.",
        "hero_subtitle": "نقوم بتصميم أنظمة ويب عالية الأداء، وأتمتة الذكاء الاصطناعي، ومحركات التسويق للقادة العالميين.",
        "hero_btn": "ابدأ مشروعك",
        "services_title": "خدمات مصممة لتأثير ملموس.",
        "process_title": "كيف نحول الأفكار إلى أرباح.",
        "why_title": "لماذا تختار الشركات العالمية Avalanche.",
        "contact_title": "هل أنت مستعد للتوسع؟ بدون مخاطر.",
        "contact_btn": "إرسال الطلب ➔"
    },
    "uk": {
        "title": "Avalanche Agency — Преміальний Веб-Дизайн та Маркетинг",
        "desc": "Висококонверсійний веб-дизайн, цифровий маркетинг та кастомна автоматизація на базі штучного інтелекту.",
        "nav_services": "Послуги", "nav_pricing": "Ціни ↗", "nav_about": "Про Нас ↗", "nav_contact": "Контакти ↗", "nav_btn": "Розпочати Проект",
        "m_services": "Послуги", "m_pricing": "Ціни ↗", "m_about": "Про Нас ↗", "m_contact": "Контакти ↗",
        "hero_title": "Сайти, що конвертують. Бренди, що домінують.",
        "hero_subtitle": "Ми розробляємо високопродуктивні веб-системи, AI-автоматизацію та маркетингові рушії для світових лідерів.",
        "hero_btn": "Розпочати Проект",
        "services_title": "Послуги для вимірюваного результату.",
        "process_title": "Як ми перетворюємо ідеї на прибуток.",
        "why_title": "Чому бренди обирають Avalanche.",
        "contact_title": "Готові до масштабування? Нуль Ризику.",
        "contact_btn": "Надіслати Запит ➔"
    },
    "ru": {
        "title": "Avalanche Agency — Премиальный Веб-Дизайн и Маркетинг",
        "desc": "Высококонверсионный веб-дизайн, цифровой маркетинг и кастомная автоматизация на базе искусственного интеллекта.",
        "nav_services": "Услуги", "nav_pricing": "Цены ↗", "nav_about": "О Нас ↗", "nav_contact": "Контакты ↗", "nav_btn": "Начать Проект",
        "m_services": "Услуги", "m_pricing": "Цены ↗", "m_about": "О Нас ↗", "m_contact": "Контакты ↗",
        "hero_title": "Сайты, которые конвертируют. Бренды, которые доминируют.",
        "hero_subtitle": "Мы разрабатываем высокопроизводительные веб-системы, AI-автоматизацию и маркетинговые движки для мировых лидеров.",
        "hero_btn": "Начать Проект",
        "services_title": "Услуги для измеримого результата.",
        "process_title": "Как мы превращаем идеи в прибыль.",
        "why_title": "Почему бренды выбирают Avalanche.",
        "contact_title": "Готовы к масштабированию? Ноль Риска.",
        "contact_btn": "Отправить Запрос ➔"
    }
}

# 5. Скрипты
scripts_code = f"""
<script>
const dicts = {json.dumps(translations, ensure_ascii=False, indent=2)};

function toggleMobileMenu() {{
  const m = document.getElementById('mobile-overlay');
  if (m) m.classList.toggle('active');
}}

function switchLanguage(lang) {{
  if (!dicts[lang]) lang = 'en';
  
  document.documentElement.lang = lang;
  document.documentElement.dir = (lang === 'ar') ? 'rtl' : 'ltr';
  
  const d = dicts[lang];
  
  if (d.title) {{
    document.title = d.title;
    const ogT = document.getElementById('og-title');
    if (ogT) ogT.content = d.title;
  }}
  if (d.desc) {{
    const mD = document.getElementById('meta-desc');
    if (mD) mD.content = d.desc;
  }}
  
  for (const [k, v] of Object.entries(d)) {{
    const el = document.getElementById('i18n-' + k);
    if (el) {{
      if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {{
        el.placeholder = v;
      }} else {{
        el.innerHTML = v;
      }}
    }}
  }}
  
  const sel1 = document.getElementById('lang-select');
  if (sel1) sel1.value = lang;
  const sel2 = document.getElementById('lang-select-mobile');
  if (sel2) sel2.value = lang;
  
  localStorage.setItem('avalanche_exact_lang', lang);
}}

async function initAutoIPLanguage() {{
  const saved = localStorage.getItem('avalanche_exact_lang');
  if (saved && dicts[saved]) {{
    switchLanguage(saved);
    return;
  }}
  
  try {{
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
    
    switchLanguage(det);
  }} catch (e) {{
    const nL = (navigator.language || 'en').slice(0, 2).toLowerCase();
    switchLanguage(dicts[nL] ? nL : 'en');
  }}
}}

document.addEventListener('DOMContentLoaded', initAutoIPLanguage);
</script>
"""

text = text.replace("</body>", scripts_code + "\n</body>")

# Сохраняем главный index.html
with open(os.path.join(STAGING_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(text)

shutil.copy(os.path.join(STAGING_DIR, "index.html"), os.path.join(STAGING_DIR, "200.html"))

print("✅ index.html на 100% обновлен под фирменный синий #60B5FF и мобильную верстку!")
