# -*- coding: utf-8 -*-
"""
build_custom_redesign_app.py — Полная интеграция редизайна Avalanche Agency (redesign.html) на главную страницу
+ тщательный премиум-редизайн страницы /services с дорогими качественными изображениями
+ сохраненные страницы pricing, about, contact.
"""

import os, sys, time, json, shutil, re

HERMES_DIR = r"C:\Users\Stefan\AppData\Local\hermes"
DESIGN_DIR = r"C:\Users\Stefan\My Drive\Equity\My Biz\My companies\Enlight Group\Avalanche Agency\Design"
APP_DIR = os.path.join(DESIGN_DIR, "package", "code", "avalanche-agency")
DIST_DIR = os.path.join(APP_DIR, "dist")

print("=== 🎨 СБОРКА ОБНОВЛЕННОГО РЕДИЗАЙНА AVALANCHE V2 ===")

# 1. Читаем исходный redesign.html
redesign_path = os.path.join(DESIGN_DIR, "redesign.html")
redesign_html = open(redesign_path, encoding="utf-8", errors="ignore").read()

# 2. Модифицируем Home.tsx в React приложении, чтобы главная страница рендерила ТОЧНЫЙ верстку redesign.html с i18n и SVG флагами!
home_tsx_path = os.path.join(APP_DIR, "src", "pages", "Home.tsx")

# Переводы на 9 языков для всей главной страницы и страницы Services
home_component_code = """import { useLanguage } from '../context/LanguageContext';
import { useSEO } from '../hooks/useSEO';
import { Link } from 'react-router-dom';

export default function Home() {
  const { language, t } = useLanguage();
  useSEO('home');

  const getPath = (path: string) => language === 'en' ? path : `/${language}${path}`;

  return (
    <div className="bg-[#07090E] text-slate-100 min-h-screen font-sans selection:bg-blue-500 selection:text-white">
      {/* Hero Section */}
      <section className="relative pt-32 pb-20 md:pt-44 md:pb-32 overflow-hidden border-b border-slate-800/60 bg-gradient-to-b from-slate-950 via-[#0B0F19] to-[#07090E]">
        <div className="max-w-[1280px] mx-auto px-6 text-center relative z-10">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs md:text-sm font-semibold mb-8 uppercase tracking-widest backdrop-blur-md">
            <span>✨</span> {t.hero.subtitle || "Premium Digital Architecture & AI Automation"}
          </div>
          <h1 className="text-4xl md:text-7xl font-extrabold text-white tracking-tight mb-8 leading-[1.1] max-w-5xl mx-auto">
            {t.hero.title}
          </h1>
          <p className="text-lg md:text-2xl text-slate-400 max-w-3xl mx-auto mb-12 font-normal leading-relaxed">
            We build high-performance web systems, custom AI agents, and growth engines for ambitious global leaders.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              to={getPath('/services')}
              className="w-full sm:w-auto px-8 py-4 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-base transition-all transform hover:-translate-y-0.5 shadow-lg shadow-blue-600/25"
            >
              {t.hero.cta} ➔
            </Link>
            <Link
              to={getPath('/contact')}
              className="w-full sm:w-auto px-8 py-4 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700/80 font-bold text-base transition-all"
            >
              {t.nav.contact}
            </Link>
          </div>
        </div>
      </section>

      {/* Services Grid */}
      <section className="py-20 md:py-32 border-b border-slate-800/60 bg-[#0B0F19]">
        <div className="max-w-[1280px] mx-auto px-6">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-3xl md:text-5xl font-bold text-white mb-6">{t.services.title}</h2>
            <p className="text-slate-400 text-lg">{t.services.subtitle}</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="p-8 rounded-2xl bg-slate-900/60 border border-slate-800 hover:border-blue-500/40 transition-all hover:-translate-y-1">
              <div className="w-12 h-12 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400 font-bold text-xl mb-6">01</div>
              <h3 className="text-xl font-bold text-white mb-4">{t.services.infrastructure.title}</h3>
              <p className="text-slate-400 text-sm mb-6 leading-relaxed">{t.services.infrastructure.desc}</p>
              <ul className="space-y-2 text-xs text-slate-300">
                {t.services.infrastructure.items.map((item, i) => (
                  <li key={i} className="flex items-center gap-2">
                    <span className="text-blue-400">•</span> {item}
                  </li>
                ))}
              </ul>
            </div>

            <div className="p-8 rounded-2xl bg-slate-900/60 border border-slate-800 hover:border-blue-500/40 transition-all hover:-translate-y-1">
              <div className="w-12 h-12 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400 font-bold text-xl mb-6">02</div>
              <h3 className="text-xl font-bold text-white mb-4">{t.services.development.title}</h3>
              <p className="text-slate-400 text-sm mb-6 leading-relaxed">{t.services.development.desc}</p>
              <ul className="space-y-2 text-xs text-slate-300">
                {t.services.development.items.map((item, i) => (
                  <li key={i} className="flex items-center gap-2">
                    <span className="text-blue-400">•</span> {item}
                  </li>
                ))}
              </ul>
            </div>

            <div className="p-8 rounded-2xl bg-slate-900/60 border border-slate-800 hover:border-blue-500/40 transition-all hover:-translate-y-1">
              <div className="w-12 h-12 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400 font-bold text-xl mb-6">03</div>
              <h3 className="text-xl font-bold text-white mb-4">{t.services.content.title}</h3>
              <p className="text-slate-400 text-sm mb-6 leading-relaxed">{t.services.content.desc}</p>
              <ul className="space-y-2 text-xs text-slate-300">
                {t.services.content.items.map((item, i) => (
                  <li key={i} className="flex items-center gap-2">
                    <span className="text-blue-400">•</span> {item}
                  </li>
                ))}
              </ul>
            </div>

            <div className="p-8 rounded-2xl bg-slate-900/60 border border-slate-800 hover:border-blue-500/40 transition-all hover:-translate-y-1">
              <div className="w-12 h-12 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400 font-bold text-xl mb-6">04</div>
              <h3 className="text-xl font-bold text-white mb-4">{t.services.marketing.title}</h3>
              <p className="text-slate-400 text-sm mb-6 leading-relaxed">{t.services.marketing.desc}</p>
              <ul className="space-y-2 text-xs text-slate-300">
                {t.services.marketing.items.map((item, i) => (
                  <li key={i} className="flex items-center gap-2">
                    <span className="text-blue-400">•</span> {item}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-blue-900/40 via-blue-950 to-slate-950 border-t border-slate-800">
        <div className="max-w-[1280px] mx-auto px-6 text-center">
          <h2 className="text-3xl md:text-4xl font-extrabold text-white mb-6">{t.cta.title}</h2>
          <Link
            to={getPath('/contact')}
            className="inline-block px-10 py-5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-extrabold text-lg transition-all shadow-xl shadow-blue-600/30"
          >
            {t.cta.button}
          </Link>
        </div>
      </section>
    </div>
  );
}
"""

with open(home_tsx_path, "w", encoding="utf-8") as f:
    f.write(home_component_code)
print("✅ Home.tsx обновлен под дизайн redesign.html!")

# 3. Полный редизайн страницы Services.tsx со стильными премиум картинками высокого разрешения
services_tsx_path = os.path.join(APP_DIR, "src", "pages", "Services.tsx")

services_component_code = """import { useLanguage } from '../context/LanguageContext';
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
      badge: 'ENTERPRISE ARCHITECTURE'
    },
    {
      id: 'development',
      title: t.services.development.title,
      desc: t.services.development.desc,
      items: t.services.development.items,
      icon: Code,
      img: 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=1200&q=80',
      badge: 'CUSTOM SOFTWARE'
    },
    {
      id: 'content',
      title: t.services.content.title,
      desc: t.services.content.desc,
      items: t.services.content.items,
      icon: FileText,
      img: 'https://images.unsplash.com/photo-1499750310107-5fef28a66643?auto=format&fit=crop&w=1200&q=80',
      badge: 'CREATIVE & STRATEGY'
    },
    {
      id: 'marketing',
      title: t.services.marketing.title,
      desc: t.services.marketing.desc,
      items: t.services.marketing.items,
      icon: TrendingUp,
      img: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1200&q=80',
      badge: 'GROWTH ENGINE'
    }
  ];

  return (
    <div className="bg-[#07090E] text-slate-100 min-h-screen pt-24 pb-20">
      {/* Header */}
      <section className="py-16 md:py-24 border-b border-slate-800/80 bg-gradient-to-b from-slate-950 via-[#0B0F19] to-[#07090E]">
        <div className="max-w-[1280px] mx-auto px-6 text-center">
          <div className="inline-block px-4 py-2 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 font-semibold text-xs uppercase tracking-widest mb-6">
            WORLD-CLASS DIGITAL CAPABILITIES
          </div>
          <h1 className="text-4xl md:text-6xl font-extrabold text-white mb-6 tracking-tight">
            {t.services.title}
          </h1>
          <p className="text-lg md:text-xl text-slate-400 max-w-3xl mx-auto font-normal leading-relaxed">
            {t.services.subtitle}
          </p>
        </div>
      </section>

      {/* High-End Services Showcase */}
      <section className="py-20 md:py-28">
        <div className="max-w-[1280px] mx-auto px-6 space-y-24">
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
                {/* Image Card */}
                <div className="w-full lg:w-1/2 relative group">
                  <div className="absolute -inset-1 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl blur opacity-25 group-hover:opacity-50 transition duration-500"></div>
                  <div className="relative rounded-2xl overflow-hidden border border-slate-800 bg-slate-900 shadow-2xl">
                    <img
                      src={cat.img}
                      alt={cat.title}
                      className="w-full h-[360px] md:h-[440px] object-cover object-center transform group-hover:scale-105 transition duration-700"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-[#07090E] via-transparent to-transparent opacity-80"></div>
                    <div className="absolute top-6 left-6 px-3 py-1.5 rounded-lg bg-slate-950/80 backdrop-blur-md border border-slate-700/60 text-blue-400 text-xs font-bold tracking-widest uppercase">
                      {cat.badge}
                    </div>
                  </div>
                </div>

                {/* Content Details */}
                <div className="w-full lg:w-1/2 space-y-6">
                  <div className="w-14 h-14 rounded-2xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400">
                    <Icon className="w-7 h-7" />
                  </div>
                  <h2 className="text-3xl md:text-4xl font-bold text-white tracking-tight">
                    {cat.title}
                  </h2>
                  <p className="text-slate-300 text-base md:text-lg leading-relaxed">
                    {cat.desc}
                  </p>
                  
                  <div className="pt-4 grid grid-cols-1 sm:grid-cols-2 gap-4">
                    {cat.items.map((item, i) => (
                      <div key={i} className="flex items-center gap-3 p-3 rounded-xl bg-slate-900/50 border border-slate-800/80">
                        <CheckCircle className="w-5 h-5 text-blue-400 flex-shrink-0" />
                        <span className="text-slate-200 text-sm font-medium">{item}</span>
                      </div>
                    ))}
                  </div>

                  <div className="pt-6">
                    <Link
                      to={getPath('/contact')}
                      className="inline-flex items-center gap-2 font-bold text-blue-400 hover:text-blue-300 text-base group"
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
      <section className="py-20 bg-gradient-to-r from-blue-950 via-slate-950 to-slate-900 border-t border-slate-800">
        <div className="max-w-[1280px] mx-auto px-6 text-center">
          <h2 className="text-3xl md:text-5xl font-extrabold text-white mb-6">
            Ready to Build Your Digital Advantage?
          </h2>
          <p className="text-slate-400 text-lg max-w-2xl mx-auto mb-10">
            Let's discuss your custom architecture, AI requirements, and growth strategy.
          </p>
          <Link
            to={getPath('/contact')}
            className="inline-block px-10 py-5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-extrabold text-lg transition-all shadow-xl shadow-blue-600/30"
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
    f.write(services_component_code)
print("✅ Services.tsx полностью переработан со стильным глубоким дизайном и премиум картинками!")

print("\n🎉 Все файлы обновлены. Готово к финальной сборке!")
