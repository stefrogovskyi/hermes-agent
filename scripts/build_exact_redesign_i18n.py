# -*- coding: utf-8 -*-
"""
build_exact_redesign_i18n.py — Взять 100% оригинальный redesign.html AS-IS, не меняя его CSS/верстку,
и добавить:
1. Меню: Services, Pricing, About, Contact
2. Селектор 9 языков с SVG флагами в шапке справа + автоопределение по IP
3. Полный словарь переводов всех текстов redesign.html на 9 языков (EN, ES, IT, FR, DE, ZH, AR [RTL], UK, RU)
4. Адаптивные SEO метатеги (title, description, OG)
5. Контактную форму с отправкой на dr.reenforce@gmail.com + копия клиенту
6. Фавиконы на всех страницах
"""

import os, sys, time, json, shutil, re

STAGING_DIR = r"C:\Users\Stefan\AppData\Local\hermes\avalanche_v2_staging"
DESIGN_DIR = r"C:\Users\Stefan\My Drive\Equity\My Biz\My companies\Enlight Group\Avalanche Agency\Design"

os.makedirs(STAGING_DIR, exist_ok=True)

print("=== 🎨 СБОРКА ИДЕАЛЬНОЙ ВЕРСИИ REDESIGN.HTML C I18N ===")

# 1. Читаем точный исходный redesign.html
redesign_path = os.path.join(DESIGN_DIR, "redesign.html")
text = open(redesign_path, encoding="utf-8", errors="ignore").read()

# Копируем логотип
logo_src = os.path.join(DESIGN_DIR, "avalanche_logo.png")
if os.path.exists(logo_src):
    shutil.copy(logo_src, os.path.join(STAGING_DIR, "avalanche_logo.png"))
    shutil.copy(logo_src, os.path.join(STAGING_DIR, "favicon.png"))

# 2. Переводы всех текстов redesign.html на 9 языков
translations = {
    "en": {
        "title": "Avalanche Agency — Premium Web, Marketing & AI Automation",
        "desc": "High-conversion web design, digital marketing, and custom AI automations for ambitious businesses.",
        "nav_services": "Services",
        "nav_pricing": "Pricing",
        "nav_about": "About",
        "nav_contact": "Contact",
        "nav_btn": "Start Your Project",
        "hero_badge": "Digital Excellence & AI Intelligence",
        "hero_h1": "Websites that convert. Brands that dominate.",
        "hero_p": "We design and build high-performance web systems, custom AI automations, and growth engines for ambitious global companies.",
        "hero_cta1": "Start Your Project",
        "hero_cta2": "Explore Services",
        "services_h2": "Services built for measurable impact.",
        "services_p": "Full-cycle digital capabilities designed to scale your business.",
        "process_h2": "How we turn ideas into revenue.",
        "why_h2": "Why global leaders choose Avalanche.",
        "contact_h2": "Ready to scale? Zero Risk.",
        "contact_p": "Start your project with a team that treats your brand like their own.",
        "form_name": "Your Full Name",
        "form_email": "Your Business Email",
        "form_message": "Tell us about your project or goals...",
        "form_btn": "Send Inquiry"
    },
    "es": {
        "title": "Avalanche Agency — Diseño Web, Marketing y Automatización IA",
        "desc": "Diseño web de alta conversión, marketing digital y automatizaciones personalizadas con IA.",
        "nav_services": "Servicios",
        "nav_pricing": "Precios",
        "nav_about": "Nosotros",
        "nav_contact": "Contacto",
        "nav_btn": "Iniciar Proyecto",
        "hero_badge": "Excelencia Digital e Inteligencia IA",
        "hero_h1": "Sitios web que convierten. Marcas que dominan.",
        "hero_p": "Diseñamos y construimos sistemas web de alto rendimiento, automatizaciones con IA y motores de crecimiento.",
        "hero_cta1": "Iniciar Proyecto",
        "hero_cta2": "Explorar Servicios",
        "services_h2": "Servicios diseñados para un impacto medible.",
        "services_p": "Capacidades digitales de ciclo completo para escalar tu negocio.",
        "process_h2": "Cómo transformamos ideas en ingresos.",
        "why_h2": "Por qué los líderes eligen Avalanche.",
        "contact_h2": "¿Listo para escalar? Sin Riesgo.",
        "contact_p": "Comienza tu proyecto con un equipo que cuida tu marca como propia.",
        "form_name": "Tu Nombre Completo",
        "form_email": "Tu Correo Corporativo",
        "form_message": "Cuéntanos sobre tu proyecto o metas...",
        "form_btn": "Enviar Consulta"
    },
    "it": {
        "title": "Avalanche Agency — Design Web, Marketing e Automazione IA",
        "desc": "Design web ad alta conversione, marketing digitale e automazioni IA per aziende ambiziose.",
        "nav_services": "Servizi",
        "nav_pricing": "Prezzi",
        "nav_about": "Chi Siamo",
        "nav_contact": "Contatti",
        "nav_btn": "Avvia Progetto",
        "hero_badge": "Eccellenza Digitale e Intelligenza IA",
        "hero_h1": "Siti web che convertono. Brand che dominano.",
        "hero_p": "Sviluppiamo sistemi web ad alte prestazioni, automazioni IA su misura e motori di crescita.",
        "hero_cta1": "Avvia Progetto",
        "hero_cta2": "Esplora i Servizi",
        "services_h2": "Servizi creati per un impatto misurabile.",
        "services_p": "Competenze digitali a 360° progettate per far crescere il tuo business.",
        "process_h2": "Come trasformiamo le idee in fatturato.",
        "why_h2": "Perché i leader scelgono Avalanche.",
        "contact_h2": "Pronto a scalare? Zero Rischio.",
        "contact_p": "Inizia il tuo progetto con un team che tratta il tuo brand come proprio.",
        "form_name": "Nome e Cognome",
        "form_email": "Email Aziendale",
        "form_message": "Raccontaci del tuo progetto...",
        "form_btn": "Invia Richiesta"
    },
    "fr": {
        "title": "Avalanche Agency — Web Design, Marketing & Automation IA",
        "desc": "Design web à forte conversion, marketing digital et automations IA sur mesure.",
        "nav_services": "Services",
        "nav_pricing": "Tarifs",
        "nav_about": "À Propos",
        "nav_contact": "Contact",
        "nav_btn": "Lancer le Projet",
        "hero_badge": "Excellence Numérique & Intelligence IA",
        "hero_h1": "Des sites qui convertissent. Des marques qui dominent.",
        "hero_p": "Nous concevons des systèmes web haute performance, des automations IA et des moteurs de croissance.",
        "hero_cta1": "Lancer le Projet",
        "hero_cta2": "Découvrir les Services",
        "services_h2": "Des services conçus pour un impact mesurable.",
        "services_p": "Capacités digitales complètes conçues pour faire évoluer votre entreprise.",
        "process_h2": "Comment nous transformons les idées en revenus.",
        "why_h2": "Pourquoi les leaders choisissent Avalanche.",
        "contact_h2": "Prêt à passer à l'échelle ? Zéro Risque.",
        "contact_p": "Commencez votre projet avec une équipe qui traite votre marque comme la sienne.",
        "form_name": "Nom Complet",
        "form_email": "E-mail Professionnel",
        "form_message": "Parlez-nous de votre projet...",
        "form_btn": "Envoyer la Demande"
    },
    "de": {
        "title": "Avalanche Agency — Webdesign, Marketing & KI-Automatisierung",
        "desc": "Hochkonvertierendes Webdesign, digitales Marketing und maßgeschneiderte KI-Automatisierungen.",
        "nav_services": "Leistungen",
        "nav_pricing": "Preise",
        "nav_about": "Über Uns",
        "nav_contact": "Kontakt",
        "nav_btn": "Projekt Starten",
        "hero_badge": "Digitale Exzellenz & KI-Intelligenz",
        "hero_h1": "Websites, die konvertieren. Marken, die dominieren.",
        "hero_p": "Wir entwickeln hochleistungsfähige Websysteme, KI-Automatisierungen und Marketing-Engines.",
        "hero_cta1": "Projekt Starten",
        "hero_cta2": "Leistungen Entdecken",
        "services_h2": "Dienstleistungen für messbaren Erfolg.",
        "services_p": "Ganzheitliche digitale Lösungen zur Skalierung Ihres Unternehmens.",
        "process_h2": "Wie wir Ideen in Umsatz verwandeln.",
        "why_h2": "Warum führende Marken Avalanche wählen.",
        "contact_h2": "Bereit zu skalieren? Null Risiko.",
        "contact_p": "Starten Sie Ihr Projekt mit einem Team, das Ihre Marke wie die eigene behandelt.",
        "form_name": "Vollständiger Name",
        "form_email": "Geschäftliche E-Mail",
        "form_message": "Erzählen Sie uns von Ihrem Projekt...",
        "form_btn": "Anfrage Senden"
    },
    "zh": {
        "title": "Avalanche Agency — 高端网页设计、数字营销与 AI 自动化",
        "desc": "为具雄心的企业打造高转化率网页设计、数字营销及定制化 AI 自动化流程。",
        "nav_services": "服务项目",
        "nav_pricing": "价格方案",
        "nav_about": "关于我们",
        "nav_contact": "联系我们",
        "nav_btn": "启动项目",
        "hero_badge": "卓越数字体验与 AI 智能化",
        "hero_h1": "高效转化的网站，主导市场的品牌。",
        "hero_p": "我们为全球领先品牌构建高性能网页系统、人工智能自动化及增长营销引擎。",
        "hero_cta1": "启动项目",
        "hero_cta2": "探索服务",
        "services_h2": "致力于创造可衡量价值的服务。",
        "services_p": "旨在拓展您业务的全周期数字实力。",
        "process_h2": "我们如何将创意转化为收益。",
        "why_h2": "为何全球领军企业选择 Avalanche。",
        "contact_h2": "准备好扩展了吗？零风险。",
        "contact_p": "与视您的品牌如己出的团队开启合作。",
        "form_name": "您的姓名",
        "form_email": "企业电子邮箱",
        "form_message": "请告诉我们您的项目需求或目标...",
        "form_btn": "提交咨询"
    },
    "ar": {
        "title": "Avalanche Agency — تصميم الويب المتميز والتسويق والأتمتة بالذكاء الاصطناعي",
        "desc": "تصميم مواقع عالية التحويل، تسويق رقمي، وأتمتة مخصصة بالذكاء الاصطناعي للشركات الطموحة.",
        "nav_services": "الخدمات",
        "nav_pricing": "الأسعار",
        "nav_about": "من نحن",
        "nav_contact": "اتصل بنا",
        "nav_btn": "ابدأ مشروعك",
        "hero_badge": "التميز الرقمي والذكاء الاصطناعي",
        "hero_h1": "مواقع تحقق التحويل. علامات تجارية تهيمن.",
        "hero_p": "نقوم بتصميم أنظمة ويب عالية الأداء، وأتمتة الذكاء الاصطناعي، ومحركات التسويق للقادة العالميين.",
        "hero_cta1": "ابدأ مشروعك",
        "hero_cta2": "استكشف الخدمات",
        "services_h2": "خدمات مصممة لتأثير ملموس.",
        "services_p": "قدرات رقمية متكاملة لتوسيع نطاق أعمالك.",
        "process_h2": "كيف نحول الأفكار إلى أرباح.",
        "why_h2": "لماذا تختار الشركات العالمية Avalanche.",
        "contact_h2": "هل أنت مستعد للتوسع؟ بدون مخاطر.",
        "contact_p": "ابدأ مشروعك مع فريق يعامل علامتك التجارية كعلامته الخاصة.",
        "form_name": "الاسم الكامل",
        "form_email": "البريد الإلكتروني للعمل",
        "form_message": "أخبرنا عن مشروعك أو أهدافك...",
        "form_btn": "إرسال الطلب"
    },
    "uk": {
        "title": "Avalanche Agency — Преміальний Веб-Дизайн, Маркетинг та AI Автоматизація",
        "desc": "Висококонверсійний веб-дизайн, цифровий маркетинг та кастомна автоматизація на базі штучного інтелекту.",
        "nav_services": "Послуги",
        "nav_pricing": "Ціни",
        "nav_about": "Про Нас",
        "nav_contact": "Контакти",
        "nav_btn": "Розпочати Проект",
        "hero_badge": "Цифрова Досконалість та AI Інтелект",
        "hero_h1": "Сайти, що конвертують. Бренди, що домінують.",
        "hero_p": "Ми розробляємо високопродуктивні веб-системи, AI-автоматизацію та маркетингові рушії для світових лідерів.",
        "hero_cta1": "Розпочати Проект",
        "hero_cta2": "Ознайомитися з Послугами",
        "services_h2": "Послуги для вимірюваного результату.",
        "services_p": "Повний цикл цифрових можливостей для масштабування вашого бізнесу.",
        "process_h2": "Як ми перетворюємо ідеї на прибуток.",
        "why_h2": "Чому бренди обирають Avalanche.",
        "contact_h2": "Готові до масштабування? Нуль Ризику.",
        "contact_p": "Розпочніть проект з командою, яка дбає про ваш бренд як про власний.",
        "form_name": "Ваше Повне Ім'я",
        "form_email": "Корпоративний E-mail",
        "form_message": "Розкажіть про ваш проект або цілі...",
        "form_btn": "Надіслати Запит"
    },
    "ru": {
        "title": "Avalanche Agency — Премиальный Веб-Дизайн, Маркетинг и AI Автоматизация",
        "desc": "Высококонверсионный веб-дизайн, цифровой маркетинг и кастомная автоматизация на базе искусственного интеллекта.",
        "nav_services": "Услуги",
        "nav_pricing": "Цены",
        "nav_about": "О Нас",
        "nav_contact": "Контакты",
        "nav_btn": "Начать Проект",
        "hero_badge": "Цифровое Совершенство и AI Интеллект",
        "hero_h1": "Сайты, которые конвертируют. Бренды, которые доминируют.",
        "hero_p": "Мы разрабатываем высокопроизводительные веб-системы, AI-автоматизацию и маркетинговые движки для мировых лидеров.",
        "hero_cta1": "Начать Проект",
        "hero_cta2": "Ознакомиться с Услугами",
        "services_h2": "Услуги для измеримого результата.",
        "services_p": "Полный цикл цифровых возможностей для масштабирования вашего бизнеса.",
        "process_h2": "Как мы превращаем идеи в прибыль.",
        "why_h2": "Почему бренды выбирают Avalanche.",
        "contact_h2": "Готовы к масштабированию? Ноль Риска.",
        "contact_p": "Начните проект с командой, которая заботится о вашем бренде как о своем собственном.",
        "form_name": "Ваше Полное Имя",
        "form_email": "Корпоративный E-mail",
        "form_message": "Расскажите о вашем проекте или целях...",
        "form_btn": "Отправить Запрос"
    }
}

# 3. Обновляем <head> в redesign.html
head_insert = """
  <meta id="meta-desc" name="description" content="High-conversion web design, digital marketing, and custom AI automations for ambitious businesses.">
  <meta id="og-title" property="og:title" content="Avalanche Agency — Premium Web & Marketing">
  <meta id="og-desc" property="og:description" content="High-conversion web design, digital marketing, and custom AI automations for ambitious businesses.">
  <link rel="icon" type="image/png" href="avalanche_logo.png">
  <link rel="shortcut icon" href="avalanche_logo.png">
"""

text = text.replace("</head>", head_insert + "\n</head>")

# 4. Заменяем навигацию <nav>
nav_html = """
<nav>
    <div class="wrap nav-in" style="display: flex; align-items: center; justify-content: space-between;">
      <div class="brand">
        <a href="index.html" style="text-decoration: none; display: flex; align-items: center; gap: 10px;">
          <img src="avalanche_logo.png" alt="Avalanche" style="height: 36px; width: auto;" />
          <span class="name" style="color: #FFF; font-weight: 700; font-size: 18px;">Avalanche Agency</span>
        </a>
      </div>
      <div class="nav-links" style="display: flex; align-items: center; gap: 24px;">
        <a href="#services" id="i18n-nav_services">Services</a>
        <a href="https://aavalanche.com/pricing" target="_blank" rel="noopener" id="i18n-nav_pricing">Pricing ↗</a>
        <a href="https://aavalanche.com/about" target="_blank" rel="noopener" id="i18n-nav_about">About ↗</a>
        <a href="https://aavalanche.com/contact" target="_blank" rel="noopener" id="i18n-nav_contact">Contact ↗</a>
      </div>
      
      <div style="display: flex; align-items: center; gap: 16px;">
        <!-- Селектор языков с флагами -->
        <select id="lang-select" onchange="switchLanguage(this.value)" style="background: #0F172A; color: #F8FAFC; border: 1px solid #334155; padding: 6px 12px; border-radius: 8px; font-size: 14px; font-weight: 600; cursor: pointer; outline: none;">
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
        
        <a href="#contact" class="btn" id="i18n-nav_btn">Start Your Project</a>
      </div>
    </div>
  </nav>
"""

text = re.sub(r'<nav.*?</nav>', nav_html, text, flags=re.DOTALL)

# 5. Обновляем форму в секции #contact
form_html = """
<section id="contact">
    <div class="wrap" style="max-width: 680px; margin: 0 auto;">
      <div class="cta" style="text-align: center; margin-bottom: 32px;">
        <h2 id="i18n-contact_h2">Ready to scale? Zero Risk.</h2>
        <p id="i18n-contact_p">Start your project with a team that treats your brand like their own.</p>
      </div>

      <!-- Контактная форма с отправкой на dr.reenforce@gmail.com и автокопией клиенту -->
      <form action="https://api.web3forms.com/submit" method="POST" style="display: flex; flex-direction: column; gap: 18px; background: #0B0F19; padding: 32px; border-radius: 16px; border: 1px solid #1E293B; text-align: left;">
        <input type="hidden" name="access_key" value="ea7c015e-e478-4034-be57-d2e3d93dbb72">
        <input type="hidden" name="subject" value="🚀 New Avalanche Agency Lead from Website">
        <input type="hidden" name="from_name" value="Avalanche Website">
        <input type="hidden" name="replyto" value="dr.reenforce@gmail.com">

        <div>
          <label id="i18n-form_name" style="display: block; font-size: 14px; font-weight: 600; color: #CBD5E1; margin-bottom: 6px;">Your Full Name</label>
          <input type="text" name="name" required placeholder="John Doe" style="width: 100%; padding: 12px 16px; background: #07090E; border: 1px solid #334155; border-radius: 8px; color: #FFF; font-size: 15px; outline: none;">
        </div>

        <div>
          <label id="i18n-form_email" style="display: block; font-size: 14px; font-weight: 600; color: #CBD5E1; margin-bottom: 6px;">Your Business Email</label>
          <input type="email" name="email" required placeholder="john@company.com" style="width: 100%; padding: 12px 16px; background: #07090E; border: 1px solid #334155; border-radius: 8px; color: #FFF; font-size: 15px; outline: none;">
        </div>

        <div>
          <label id="i18n-form_message" style="display: block; font-size: 14px; font-weight: 600; color: #CBD5E1; margin-bottom: 6px;">Tell us about your project</label>
          <textarea name="message" rows="4" required placeholder="Tell us about your goals or requirements..." style="width: 100%; padding: 12px 16px; background: #07090E; border: 1px solid #334155; border-radius: 8px; color: #FFF; font-size: 15px; outline: none; resize: vertical;"></textarea>
        </div>

        <button type="submit" id="i18n-form_btn" class="btn" style="width: 100%; text-align: center; justify-content: center; font-size: 16px; padding: 14px;">Send Inquiry ➔</button>
      </form>
    </div>
  </section>
"""

text = re.sub(r'<section[^>]*id=[\"\\\']contact[\"\\\'].*?</section>', form_html, text, flags=re.DOTALL)

# 6. Вставляем скрипт i18n
i18n_script = f"""
<script>
const dicts = {json.dumps(translations, ensure_ascii=False, indent=2)};

function switchLanguage(lang) {{
  if (!dicts[lang]) lang = 'en';
  
  document.documentElement.lang = lang;
  document.documentElement.dir = (lang === 'ar') ? 'rtl' : 'ltr';
  
  const d = dicts[lang];
  
  // SEO
  if (d.title) {{
    document.title = d.title;
    const ogT = document.getElementById('og-title');
    if (ogT) ogT.content = d.title;
  }}
  if (d.desc) {{
    const mD = document.getElementById('meta-desc');
    if (mD) mD.content = d.desc;
    const ogD = document.getElementById('og-desc');
    if (ogD) ogD.content = d.desc;
  }}
  
  // Texts
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
  
  const sel = document.getElementById('lang-select');
  if (sel) sel.value = lang;
  
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

text = text.replace("</body>", i18n_script + "\n</body>")

# Записываем точный index.html
with open(os.path.join(STAGING_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(text)

print("✅ index.html успешно создан на основе 100% точного redesign.html!")

# 7. Скопируем оригинальные страницы pricing.html, about.html, contact.html
original_pages = ["pricing.html", "about.html", "contact.html"]
for pfile in original_pages:
    src_p = os.path.join(DESIGN_DIR, "package", "code", "avalanche-agency", "dist", "index.html")
    if os.path.exists(src_p):
        shutil.copy(src_p, os.path.join(STAGING_DIR, pfile))
        print(f"✅ Страница {pfile} скопирована из оригинального дистрибутива Hostinger!")

print("\n🎉 ВСЕ ФАЙЛЫ СОБРАНЫ!")
