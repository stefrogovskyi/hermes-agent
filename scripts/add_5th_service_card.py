# -*- coding: utf-8 -*-
"""
add_5th_service_card.py — Добавление 5-й карточки услуг "AI Agents & Assistants Development" / "Создание ИИ-агентов / ИИ-ассистентов"
на страницу services.html и в блок услуг на index.html.
Отзеркалено на все 8 языков (en, es, de, fr, it, uk, ru, zh, ar)!
"""

import os, re, paramiko, subprocess

HERMES_DIR = r"C:\Users\Stefan\AppData\Local\hermes"
site_dir = os.path.join(HERMES_DIR, "avalanche_v2_staging")
os.chdir(site_dir)

# 5th Card Translations per language
card_data = {
    "en": ("05 • AI AUTOMATION", "AI Agents & Assistants Development", "Build autonomous AI agents, intelligent customer assistants, and agentic workflow automations for enterprise operations.", "Autonomous AI Agent Architecture", "Custom AI Customer Support Assistants", "Agentic Workflow & API Integrations", "Get Started ➔"),
    "es": ("05 • AUTOMATIZACIÓN DE IA", "Desarrollo de Agentes y Asistentes de IA", "Construya agentes de IA autónomos, asistentes inteligentes de atención al cliente y automatizaciones de flujos de trabajo.", "Arquitectura de Agentes de IA Autónomos", "Asistentes Virtuales de Atención al Cliente", "Integración de Flujos de Trabajo y APIs de IA", "Comenzar Ahora ➔"),
    "de": ("05 • KI-AUTOMATISIERUNG", "Entwicklung von KI-Agenten & Assistenten", "Bauen Sie autonome KI-Agenten, intelligente Kundensupport-Assistenten und automatisierte Workflows.", "Autonome KI-Agenten-Architektur", "Individuelle KI-Kundensupport-Assistenten", "KI-Workflow- & API-Integrationen", "Dienste Anzeigen ➔"),
    "fr": ("05 • AUTOMATISATION IA", "Développement d'Agents et Assistants IA", "Créez des agents IA autonomes, des assistants client intelligents et des automatisations de flux de travail.", "Architecture d'Agents IA Autonomes", "Assistants IA Sur Mesure pour Support Client", "Intégrations d'APIs et Flux de Travail IA", "Voir les Services ➔"),
    "it": ("05 • AUTOMAZIONALI IA", "Sviluppo di Agenti e Assistenti IA", "Crea agenti IA autonomi, assistenti clienti intelligenti e automazioni di flusso di lavoro aziendali.", "Architettura di Agenti IA Autonomi", "Assistenti IA Personalizzati per il Supporto", "Integrazioni di Flussi di Lavoro e API IA", "Vedi Servizi ➔"),
    "uk": ("05 • АВТОМАТИЗАЦІЯ ІІ", "Розробка ШІ-Агентів та ШІ-Асистентів", "Створення автономних ШІ-агентів, інтелектуальних асистентів підтримки клієнтів та автоматизації бізнес-процесів.", "Архітектура автономних ШІ-агентів", "Персоналізовані ШІ-асистенти підтримки", "Інтеграція робочих процесів та ШІ-API", "Переглянути Послуги ➔"),
    "ru": ("05 • АВТОМАТИЗАЦИЯ ИИ", "Создание ИИ-агентов и ИИ-ассистентов", "Создание автономных ИИ-агентов, интеллектуальных ассистентов поддержки клиентов и автоматизации бизнес-процессов.", "Архитектура автономных ИИ-агентов", "Персонализированные ИИ-ассистенты поддержки", "Интеграция рабочих процессов и ИИ-API", "Посмотреть Услуги ➔"),
    "zh": ("05 • 人工智能自动化", "AI 代理与智能助手开发", "构建自主 AI 代理、智能客户服务助手以及企业级工作流自动化系统。", "自主 AI 代理架构设计", "定制化 AI 客户服务助手", "工作流与 AI API 系统集成", "查看服务 ➔"),
    "ar": ("05 • أتمتة الذكاء الاصطناعي", "تطوير وكلاء ومساعدين الذكاء الاصطناعي", "بناء وكلاء ذكاء اصطناعي مستقلين، ومساعدين ذكيين لخدمة العملاء، وأتمتة سير العمل للشركات.", "بنية وكلاء الذكاء الاصطناعي المستقلة", "مساعدو خدمة العملاء المخصصون بالذكاء الاصطناعي", "تكامل سير العمل وواجهات برمجة التطبيقات", "عرض الخدمات ➔")
}

def generate_5th_card_html(lang_code="en"):
    d = card_data.get(lang_code, card_data["en"])
    return f"""
      <!-- 05. AI Agents & Assistants Development -->
      <div style="background: #FFFFFF; border: 2px solid #8B5CF6; border-radius: 20px; padding: 40px; box-shadow: 0 10px 30px rgba(139,92,246,0.12); grid-column: span 2;">
        <div style="font-size: 14px; font-weight: 800; color: #8B5CF6; margin-bottom: 12px;">{d[0]}</div>
        <h2 style="font-size: 26px; font-weight: 800; color: #0F172A; margin-bottom: 16px;">{d[1]}</h2>
        <p style="color: #64748B; line-height: 1.6; margin-bottom: 24px;">{d[2]}</p>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 24px;">
          <div style="padding: 10px 14px; background: #F5F3FF; border-radius: 10px; color: #5B21B6; font-weight: 700; font-size: 14px;">✓ {d[3]}</div>
          <div style="padding: 10px 14px; background: #F5F3FF; border-radius: 10px; color: #5B21B6; font-weight: 700; font-size: 14px;">✓ {d[4]}</div>
          <div style="padding: 10px 14px; background: #F5F3FF; border-radius: 10px; color: #5B21B6; font-weight: 700; font-size: 14px;">✓ {d[5]}</div>
        </div>
        <a href="contact.html" style="display: inline-block; background: #8B5CF6; color: #FFFFFF; font-weight: 700; padding: 12px 28px; border-radius: 10px; text-decoration: none;">{d[6]}</a>
      </div>
    """

# Update English services.html
serv_en_path = os.path.join(site_dir, "services.html")
if os.path.exists(serv_en_path):
    txt = open(serv_en_path, encoding="utf-8").read()
    if "05 • AI AUTOMATION" not in txt:
        card_html = generate_5th_card_html("en")
        # Inject card before closing grid div
        txt = txt.replace("</div>\n    </div>\n  </div>\n</section>", f"{card_html}\n    </div>\n  </div>\n</section>")
        open(serv_en_path, "w", encoding="utf-8").write(txt)
        print("✅ Added 5th AI Agents card to root services.html!")

# Update English index.html (What we do grid)
index_en_path = os.path.join(site_dir, "index.html")
if os.path.exists(index_en_path):
    txt = open(index_en_path, encoding="utf-8").read()
    if "AI Agents &amp; Assistants" not in txt and "05 • AI AUTOMATION" not in txt:
        ai_svc_box = """
        <div class="svc" style="grid-column: span 2; border: 2px solid #8B5CF6; background: #F5F3FF;"><div class="ic" style="color: #8B5CF6;">🤖</div><h3 style="color: #5B21B6;">AI Agents &amp; Assistants Development</h3><p class="desc">Autonomous AI agents, custom customer support assistants, and workflow automations.</p><ul><li>Autonomous AI Agent Architecture</li><li>Custom AI Customer Assistants</li><li>Agentic Workflow &amp; API Integrations</li></ul></div>
        """
        txt = txt.replace('</div>\n\n      </div>\n\n    </div>\n\n  </section>', f'{ai_svc_box}\n\n      </div>\n\n    </div>\n\n  </section>')
        open(index_en_path, "w", encoding="utf-8").write(txt)
        print("✅ Added 5th AI Agents card to root index.html grid!")

# Update all 8 language subfolders (services.html and index.html)
langs = ["es", "de", "fr", "it", "uk", "ru", "zh", "ar"]

for lang_code in langs:
    l_dir = os.path.join(site_dir, lang_code)
    
    # 1. services.html
    l_serv = os.path.join(l_dir, "services.html")
    if os.path.exists(l_serv):
        txt = open(l_serv, encoding="utf-8").read()
        if "05 •" not in txt:
            card_html = generate_5th_card_html(lang_code)
            txt = txt.replace("</div>\n    </div>\n  </div>\n</section>", f"{card_html}\n    </div>\n  </div>\n</section>")
            open(l_serv, "w", encoding="utf-8").write(txt)
            print(f"✅ Added 5th AI Agents card to /{lang_code}/services.html!")

    # 2. index.html
    l_index = os.path.join(l_dir, "index.html")
    if os.path.exists(l_index):
        txt = open(l_index, encoding="utf-8").read()
        d = card_data.get(lang_code, card_data["en"])
        if "05 •" not in txt and "AI" not in txt.split("grid4")[1][:500]:
            ai_svc_box = f"""
            <div class="svc" style="grid-column: span 2; border: 2px solid #8B5CF6; background: #F5F3FF;"><div class="ic" style="color: #8B5CF6;">🤖</div><h3 style="color: #5B21B6;">{d[1]}</h3><p class="desc">{d[2]}</p><ul><li>{d[3]}</li><li>{d[4]}</li><li>{d[5]}</li></ul></div>
            """
            txt = txt.replace('</div>\n\n      </div>\n\n    </div>\n\n  </section>', f'{ai_svc_box}\n\n      </div>\n\n    </div>\n\n  </section>')
            open(l_index, "w", encoding="utf-8").write(txt)
            print(f"✅ Added 5th AI Agents card to /{lang_code}/index.html grid!")

# Upload to Hostinger SFTP
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

# Git Commit and Push
subprocess.run(["git", "checkout", "dev"], check=True)
subprocess.run(["git", "add", "."], check=True)
res_commit = subprocess.run(["git", "commit", "-m", "feat(dev): Add 5th service card (AI Agents & Assistants Development) across services.html and index.html for all 9 languages"], capture_output=True, text=True)
print(res_commit.stdout or res_commit.stderr)

res_push = subprocess.run(["git", "push", "origin", "dev", "--force"], capture_output=True, text=True)
print(res_push.stdout or res_push.stderr)

res_sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
active_sha = res_sha.stdout.strip()

ssh.close()

print(f"🎉 5TH SERVICE CARD & DUAL MAILER DEPLOYED! COMMIT: {active_sha}")
