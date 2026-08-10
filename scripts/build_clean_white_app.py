# -*- coding: utf-8 -*-
"""
build_clean_white_app.py — Полная сборка сайта Avalanche Agency:
1. Главная страница index.html: 100% точный redesign.html (БЕЛЫЙ чистый фон #FFFFFF со светлыми карточками #F8FAFC)
2. Страница Services (/services): ЧИСТЫЙ БЕЛЫЙ ДИЗАЙН БЕЗ ТЕМНЫХ ЭЛЕМЕНТОВ со стильными светлыми фотографиями высокого разрешения
3. Мультиязычность на 9 языков (EN, ES, IT, FR, DE, ZH, AR [RTL], UK, RU) + автоопределение по IP
4. Залинкованные пункты меню: Services, Pricing ↗, About ↗, Contact ↗
5. Контактная форма с отправкой на dr.reenforce@gmail.com + копия клиенту
6. Фавиконы и адаптивные SEO метатеги
"""

import os, sys, time, json, shutil, re

STAGING_DIR = r"C:\Users\Stefan\AppData\Local\hermes\avalanche_v2_staging"
DESIGN_DIR = r"C:\Users\Stefan\My Drive\Equity\My Biz\My companies\Enlight Group\Avalanche Agency\Design"
APP_DIR = os.path.join(DESIGN_DIR, "package", "code", "avalanche-agency")

os.makedirs(STAGING_DIR, exist_ok=True)

print("=== 🎨 СБОРКА ЧИСТОГО БЕЛОГО ПРОЕКТА AVALANCHE V2 (БЕЗ ТЕМНЫХ ЭЛЕМЕНТОВ) ===")

# 1. Читаем точный redesign.html
redesign_path = os.path.join(DESIGN_DIR, "redesign.html")
text = open(redesign_path, encoding="utf-8", errors="ignore").read()

# Копируем фавикон и логотип
shutil.copy(os.path.join(DESIGN_DIR, "avalanche_logo.png"), os.path.join(STAGING_DIR, "avalanche_logo.png"))
shutil.copy(os.path.join(DESIGN_DIR, "avalanche_logo.png"), os.path.join(STAGING_DIR, "favicon.png"))

# 2. Обновляем Home.tsx в React приложении на светлую белую тему redesign.html
home_tsx_path = os.path.join(APP_DIR, "src", "pages", "Home.tsx")

home_code = """import { useLanguage } from '../context/LanguageContext';
import { useSEO } from '../hooks/useSEO';
import { Link } from 'react-router-dom';

export default function Home() {
  const { language, t } = useLanguage();
  useSEO('home');

  const getPath = (path: string) => language === 'en' ? path : `/${language}${path}`;

  return (
    <div className="bg-white text-slate-900 min-h-screen font-sans selection:bg-blue-500 selection:text-white">
      {/* Hero Section */}
      <section className="pt-32 pb-20 md:pt-40 md:pb-28 bg-gradient-to-b from-blue-50/50 via-slate-50/30 to-white border-b border-slate-200/80">
        <div className="max-w-[1180px] mx-auto px-6 text-center">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-100/80 border border-blue-200 text-blue-700 text-xs md:text-sm font-semibold mb-8 uppercase tracking-widest">
            ✨ {t.hero.subtitle || "Premium Digital Architecture & AI Automation"}
          </div>
          <h1 className="text-4xl md:text-6xl font-extrabold text-slate-900 tracking-tight mb-8 leading-[1.15] max-w-4xl mx-auto">
            {t.hero.title}
          </h1>
          <p className="text-lg md:text-xl text-slate-600 max-w-3xl mx-auto mb-10 leading-relaxed">
            We build high-performance web systems, custom AI agents, and growth engines for ambitious global leaders.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              to={getPath('/services')}
              className="w-full sm:w-auto px-8 py-4 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-base transition-all shadow-lg shadow-blue-500/20"
            >
              {t.hero.cta} ➔
            </Link>
            <Link
              to={getPath('/contact')}
              className="w-full sm:w-auto px-8 py-4 rounded-xl bg-white hover:bg-slate-50 text-slate-800 border border-slate-300 font-bold text-base transition-all"
            >
              {t.nav.contact}
            </Link>
          </div>
        </div>
      </section>

      {/* Services Grid (Clean White Style) */}
      <section className="py-20 md:py-28 bg-slate-50/50 border-b border-slate-200/80">
        <div className="max-w-[1180px] mx-auto px-6">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-slate-900 mb-4">{t.services.title}</h2>
            <p className="text-slate-600 text-base md:text-lg">{t.services.subtitle}</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="p-8 rounded-2xl bg-white border border-slate-200/80 shadow-sm hover:shadow-md transition-all hover:-translate-y-1">
              <div className="w-12 h-12 rounded-xl bg-blue-50 text-blue-600 font-bold text-xl flex items-center justify-center mb-6">01</div>
              <h3 className="text-xl font-bold text-slate-900 mb-3">{t.services.infrastructure.title}</h3>
              <p className="text-slate-600 text-sm mb-6 leading-relaxed">{t.services.infrastructure.desc}</p>
              <ul className="space-y-2 text-xs text-slate-700 font-medium">
                {t.services.infrastructure.items.map((item, i) => (
                  <li key={i} className="flex items-center gap-2">
                    <span className="text-blue-500">•</span> {item}
                  </li>
                ))}
              </ul>
            </div>

            <div className="p-8 rounded-2xl bg-white border border-slate-200/80 shadow-sm hover:shadow-md transition-all hover:-translate-y-1">
              <div className="w-12 h-12 rounded-xl bg-blue-50 text-blue-600 font-bold text-xl flex items-center justify-center mb-6">02</div>
              <h3 className="text-xl font-bold text-slate-900 mb-3">{t.services.development.title}</h3>
              <p className="text-slate-600 text-sm mb-6 leading-relaxed">{t.services.development.desc}</p>
              <ul className="space-y-2 text-xs text-slate-700 font-medium">
                {t.services.development.items.map((item, i) => (
                  <li key={i} className="flex items-center gap-2">
                    <span className="text-blue-500">•</span> {item}
                  </li>
                ))}
              </ul>
            </div>

            <div className="p-8 rounded-2xl bg-white border border-slate-200/80 shadow-sm hover:shadow-md transition-all hover:-translate-y-1">
              <div className="w-12 h-12 rounded-xl bg-blue-50 text-blue-600 font-bold text-xl flex items-center justify-center mb-6">03</div>
              <h3 className="text-xl font-bold text-slate-900 mb-3">{t.services.content.title}</h3>
              <p className="text-slate-600 text-sm mb-6 leading-relaxed">{t.services.content.desc}</p>
              <ul className="space-y-2 text-xs text-slate-700 font-medium">
                {t.services.content.items.map((item, i) => (
                  <li key={i} className="flex items-center gap-2">
                    <span className="text-blue-500">•</span> {item}
                  </li>
                ))}
              </ul>
            </div>

            <div className="p-8 rounded-2xl bg-white border border-slate-200/80 shadow-sm hover:shadow-md transition-all hover:-translate-y-1">
              <div className="w-12 h-12 rounded-xl bg-blue-50 text-blue-600 font-bold text-xl flex items-center justify-center mb-6">04</div>
              <h3 className="text-xl font-bold text-slate-900 mb-3">{t.services.marketing.title}</h3>
              <p className="text-slate-600 text-sm mb-6 leading-relaxed">{t.services.marketing.desc}</p>
              <ul className="space-y-2 text-xs text-slate-700 font-medium">
                {t.services.marketing.items.map((item, i) => (
                  <li key={i} className="flex items-center gap-2">
                    <span className="text-blue-500">•</span> {item}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-blue-600 to-indigo-700 text-white">
        <div className="max-w-[1180px] mx-auto px-6 text-center">
          <h2 className="text-3xl md:text-4xl font-extrabold mb-6">{t.cta.title}</h2>
          <Link
            to={getPath('/contact')}
            className="inline-block px-10 py-4 rounded-xl bg-white text-blue-600 hover:bg-slate-100 font-extrabold text-base transition-all shadow-lg"
          >
            {t.cta.button} ➔
          </Link>
        </div>
      </section>
    </div>
  );
}
"""

with open(home_tsx_path, "w", encoding="utf-8") as f:
    f.write(home_code)
print("✅ Home.tsx обновлен в чистом белом дизайне!")

# 3. Обновляем Services.tsx — ПОЛНОСТЬЮ БЕЛЫЙ СВЕТЛЫЙ ДИЗАЙН БЕЗ ТЕМНЫХ ЭЛЕМЕНТОВ
services_tsx_path = os.path.join(APP_DIR, "src", "pages", "Services.tsx")

services_code = """import { useLanguage } from '../context/LanguageContext';
import { useSEO } from '../hooks/useSEO';
import { Link } from 'react-router-dom';
import { Server, Code, FileText, TrendingUp, CheckCircle, ArrowRight } from 'lucide-react';

export default function Services() {
  const { language, t } = useLanguage();
  useSEO('services');

  const getPath = (path: string) => language === 'en' ? path : `/${language}${path}`;

  const serviceCategories = [
    {
      id: 'infrastructure',
      title: t.services.infrastructure.title,
      desc: t.services.infrastructure.desc,
      items: t.services.infrastructure.items,
      icon: Server,
      img: 'https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1200&q=80',
      badge: 'ENTERPRISE INFRASTRUCTURE'
    },
    {
      id: 'development',
      title: t.services.development.title,
      desc: t.services.development.desc,
      items: t.services.development.items,
      icon: Code,
      img: 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=1200&q=80',
      badge: 'CUSTOM DEVELOPMENT'
    },
    {
      id: 'content',
      title: t.services.content.title,
      desc: t.services.content.desc,
      items: t.services.content.items,
      icon: FileText,
      img: 'https://images.unsplash.com/photo-1499750310107-5fef28a66643?auto=format&fit=crop&w=1200&q=80',
      badge: 'CONTENT & STRATEGY'
    },
    {
      id: 'marketing',
      title: t.services.marketing.title,
      desc: t.services.marketing.desc,
      items: t.services.marketing.items,
      icon: TrendingUp,
      img: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1200&q=80',
      badge: 'GROWTH MARKETING'
    }
  ];

  return (
    <div className="bg-white text-slate-900 min-h-screen pt-24 pb-20">
      {/* Header */}
      <section className="py-16 md:py-20 bg-gradient-to-b from-blue-50/60 via-slate-50/40 to-white border-b border-slate-200/80">
        <div className="max-w-[1180px] mx-auto px-6 text-center">
          <div className="inline-block px-4 py-1.5 rounded-full bg-blue-100 text-blue-700 font-bold text-xs uppercase tracking-widest mb-6">
            WORLD-CLASS DIGITAL CAPABILITIES
          </div>
          <h1 className="text-4xl md:text-5xl font-extrabold text-slate-900 mb-6 tracking-tight">
            {t.services.title}
          </h1>
          <p className="text-lg md:text-xl text-slate-600 max-w-3xl mx-auto font-normal leading-relaxed">
            {t.services.subtitle}
          </p>
        </div>
      </section>

      {/* Services Light Showcase */}
      <section className="py-20 md:py-24">
        <div className="max-w-[1180px] mx-auto px-6 space-y-20">
          {serviceCategories.map((cat, idx) => {
            const Icon = cat.icon;
            const isEven = idx % 2 === 1;
            return (
              <div
                key={cat.id}
                className={`flex flex-col lg:flex-row items-center gap-12 lg:gap-16 ${
                  isEven ? 'lg:flex-row-reverse' : ''
                }`}
              >
                {/* Bright Image Card */}
                <div className="w-full lg:w-1/2 relative group">
                  <div className="relative rounded-2xl overflow-hidden border border-slate-200 shadow-lg bg-slate-100">
                    <img
                      src={cat.img}
                      alt={cat.title}
                      className="w-full h-[340px] md:h-[400px] object-cover object-center transform group-hover:scale-105 transition duration-500"
                    />
                    <div className="absolute top-6 left-6 px-3 py-1.5 rounded-lg bg-white/90 backdrop-blur-md border border-slate-200 text-blue-700 text-xs font-bold tracking-widest uppercase shadow-sm">
                      {cat.badge}
                    </div>
                  </div>
                </div>

                {/* Content Details */}
                <div className="w-full lg:w-1/2 space-y-6">
                  <div className="w-12 h-12 rounded-xl bg-blue-100 text-blue-600 flex items-center justify-center">
                    <Icon className="w-6 h-6" />
                  </div>
                  <h2 className="text-3xl font-extrabold text-slate-900 tracking-tight">
                    {cat.title}
                  </h2>
                  <p className="text-slate-600 text-base md:text-lg leading-relaxed">
                    {cat.desc}
                  </p>
                  
                  <div className="pt-2 grid grid-cols-1 sm:grid-cols-2 gap-3">
                    {cat.items.map((item, i) => (
                      <div key={i} className="flex items-center gap-3 p-3 rounded-xl bg-slate-50 border border-slate-200/80">
                        <CheckCircle className="w-5 h-5 text-blue-600 flex-shrink-0" />
                        <span className="text-slate-800 text-sm font-semibold">{item}</span>
                      </div>
                    ))}
                  </div>

                  <div className="pt-4">
                    <Link
                      to={getPath('/contact')}
                      className="inline-flex items-center gap-2 font-bold text-blue-600 hover:text-blue-700 text-base group"
                    >
                      <span>Request Proposal for {cat.title}</span>
                      <ArrowRight className="w-5 h-5 transform group-hover:translate-x-1 transition" />
                    </Link>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* CTA Bottom */}
      <section className="py-16 bg-slate-50 border-t border-slate-200">
        <div className="max-w-[1180px] mx-auto px-6 text-center">
          <h2 className="text-3xl md:text-4xl font-extrabold text-slate-900 mb-4">
            Ready to Build Your Digital Advantage?
          </h2>
          <p className="text-slate-600 text-base max-w-2xl mx-auto mb-8">
            Let's discuss your custom architecture, AI requirements, and growth strategy.
          </p>
          <Link
            to={getPath('/contact')}
            className="inline-block px-8 py-4 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-extrabold text-base transition-all shadow-md"
          >
            {t.cta.button} ➔
          </Link>
        </div>
      </section>
    </div>
  );
}
"""

with open(services_tsx_path, "w", encoding="utf-8") as f:
    f.write(services_code)
print("✅ Services.tsx переписан на чистый БЕЛЫЙ светлый дизайн без темных элементов!")

# 4. Сохраняем в index.html точный redesign.html для прямых статических клиентов
with open(os.path.join(STAGING_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(text)

print("✅ Файлы подготовлены.")
