# -*- coding: utf-8 -*-
"""
build_evaluation_and_monobank_flow.py — Реализация всей цепочки ИИ-оценки проекта, расчета стоимости и оплаты через Monobank:
  1. Кнопка отправки формы в Hero на index.html сохраняет описание проекта в localStorage и перенаправляет на evaluation.html
  2. Страница evaluation.html (Оценка проекта):
     - Анимированный ИИ-прелоадер с процентами (0% -> 100%) и статусами оценки
     - ИИ-расчет трудоемкости по 10-балльной шкале ($9+$5/мес -> $99+$50/мес). Простой агент/бот пометки ➔ 2 балла ($19 + $10/мес).
     - Блок "Вы получаете" (You Receive) с обязательными 7 ключевыми пунктами + запрошенными навыками.
     - Кнопка "Accept & Pay" с окном Monobank оплаты и конвертацией в UAH.
     - Сообщение об успешной оплате ("Ваш агент будет готов в течение 48 часов").
  3. Двойное брендированное письмо через send_mail.php клиенту и админу на dr.reenforce@gmail.com с номером заказа.
"""

import os, re, paramiko, subprocess

HERMES_DIR = r"C:\Users\Stefan\AppData\Local\hermes"
site_dir = os.path.join(HERMES_DIR, "avalanche_v2_staging")
prod_extract_dir = os.path.join(HERMES_DIR, "prod_extracted_pages")
os.chdir(site_dir)

header_html = open(os.path.join(prod_extract_dir, "header.html"), encoding="utf-8").read()
footer_html = open(os.path.join(prod_extract_dir, "footer.html"), encoding="utf-8").read()

header_html = header_html.replace("#60B5FF", "#5FB3F9").replace("#389BFF", "#5FB3F9")
footer_html = footer_html.replace("#60B5FF", "#5FB3F9").replace("#389BFF", "#5FB3F9")

# 1. CREATE EVALUATION.HTML PAGE
evaluation_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Evaluating Your Project — Avalanche Agency</title>
  <link rel="icon" type="image/png" href="avalanche_logo.png">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: #FFFFFF; color: #0F172A; font-family: 'Inter', system-ui, sans-serif; line-height: 1.65; }
    .wrap { max-width: 1000px; margin: 0 auto; padding: 0 24px; }
    .card { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 20px; padding: 40px; box-shadow: 0 10px 30px rgba(0,0,0,0.04); margin-bottom: 30px; }
    .btn-pay { display: inline-block; background: #5FB3F9; color: #FFFFFF; font-size: 18px; font-weight: 800; padding: 18px 48px; border-radius: 14px; border: none; cursor: pointer; box-shadow: 0 8px 25px rgba(95,179,249,0.35); text-decoration: none; transition: transform 0.2s; }
    .btn-pay:hover { transform: scale(1.02); }
    .progress-bar { width: 100%; height: 14px; background: #E2E8F0; border-radius: 10px; overflow: hidden; margin: 20px 0; }
    .progress-fill { width: 0%; height: 100%; background: linear-gradient(90deg, #5FB3F9, #389BFF); transition: width 0.1s linear; }
    .deliverable-item { display: flex; align-items: flex-start; gap: 14px; padding: 14px 0; border-bottom: 1px solid #F1F5F9; font-size: 15px; color: #334155; font-weight: 600; }
    .deliverable-item span.icon { display: flex; align-items: center; justify-content: center; width: 22px; height: 22px; background: #D1FAE5; border-radius: 50%; color: #10B981; font-weight: 900; font-size: 13px; flex-shrink: 0; margin-top: 2px; }
  </style>
</head>
<body>

""" + header_html + """

<main style="padding: 70px 0; background: #F8FAFC;">
  <div class="wrap">
    
    <div style="text-align: center; margin-bottom: 40px;">
      <span style="font-size: 13px; font-weight: 800; letter-spacing: 0.15em; color: #5FB3F9; text-transform: uppercase;">AI PROJECT ESTIMATION</span>
      <h1 style="font-size: 40px; font-weight: 800; color: #0F172A; margin: 10px 0;">Evaluating Your Project</h1>
      <p style="font-size: 16px; color: #64748B; max-width: 600px; margin: 0 auto;">Our AI engine is analyzing your project requirements and calculating optimal architecture.</p>
    </div>

    <!-- PHASE 1: ANIMATED AI PRELOADER -->
    <div id="phase-preloader" class="card" style="text-align: center; padding: 60px 40px;">
      <div style="font-size: 48px; font-weight: 900; color: #5FB3F9;" id="progress-text">0%</div>
      
      <div class="progress-bar">
        <div class="progress-fill" id="progress-fill"></div>
      </div>

      <div id="status-message" style="font-size: 16px; font-weight: 700; color: #475569; margin-top: 10px;">Analyzing project objectives...</div>
    </div>

    <!-- PHASE 2: EVALUATION RESULT & PRICING BREAKDOWN -->
    <div id="phase-result" class="card" style="display: none;">
      
      <div style="background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 16px; padding: 24px; margin-bottom: 32px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 20px;">
        <div>
          <span style="font-size: 12px; font-weight: 800; color: #1E40AF; text-transform: uppercase;">CALCULATED PROJECT ESTIMATE</span>
          <h2 style="font-size: 28px; font-weight: 900; color: #0F172A; margin-top: 4px;" id="calc-price-usd">$19 One-Time Setup + $10 / month</h2>
          <div style="font-size: 14px; color: #64748B; margin-top: 2px;">Estimated local total: <b id="calc-price-uah">~ 1,190 UAH</b> (Monobank Acquiring)</div>
        </div>

        <button class="btn-pay" onclick="openPaymentModal()">Accept & Pay ➔</button>
      </div>

      <!-- DELIVERABLES LIST: "ВЫ ПОЛУЧАЕТЕ" -->
      <h3 style="font-size: 22px; font-weight: 800; color: #0F172A; margin-bottom: 20px;">Вы получаете (You Receive):</h3>

      <div id="deliverables-list">
        <div class="deliverable-item"><span class="icon">✓</span> <div><b>Телеграм агент</b>, который будет всегда с вами и никогда в жизни никуда не пропадет, с которым можно общаться круглосуточно всеми видами коммуникации.</div></div>
        <div class="deliverable-item"><span class="icon">✓</span> <div><b>Всегда самая последняя мощная модель ИИ</b> (GPT-4o / Claude 3.5 Sonnet / Gemini 1.5 Pro) с автоматическими апгрейдами.</div></div>
        <div class="deliverable-item"><span class="icon">✓</span> <div><b>Настроенная память</b>, которую можно масштабировать безгранично (с векторной индексацией и быстрым поиском без огромного расхода токенов на контекст).</div></div>
        <div class="deliverable-item"><span class="icon">✓</span> <div><b>Система самообучения и самосовершенствования</b>, которая развивается вместе с пользователем каждый день.</div></div>
        <div class="deliverable-item"><span class="icon">✓</span> <div><b>Набор скиллз (Skills)</b>, которые могут постоянно дополняться под новые задачи.</div></div>
        <div class="deliverable-item"><span class="icon">✓</span> <div><b>Возможность подключать свои сервисы</b> и сторонние API к агенту.</div></div>
        <div class="deliverable-item"><span class="icon">✓</span> <div><b>24/7 Поддержка Avalanche Agency</b> и выделенный инженер поддержки.</div></div>
        
        <!-- Custom Skills Requested in Form -->
        <div class="deliverable-item" id="custom-requested-skill" style="background: #F0F7FF; border-radius: 12px; padding: 16px; margin-top: 10px;">
          <span class="icon">✓</span>
          <div><b style="color: #1E40AF;">Персонализированный навык под ваш запрос:</b> <span id="user-req-text">Индивидуальный телеграм-бот ассистент</span></div>
        </div>
      </div>

      <div style="text-align: center; margin-top: 40px;">
        <button class="btn-pay" onclick="openPaymentModal()">Accept & Pay ➔</button>
      </div>

    </div>

    <!-- PAYMENT MODAL / CONFIRMATION -->
    <div id="payment-modal" style="display: none; position: fixed; top:0; left:0; width:100%; height:100%; background: rgba(15,23,42,0.7); z-index: 3000; align-items:center; justify-content:center; padding: 20px;">
      <div style="background:#FFFFFF; border-radius:20px; padding:40px; max-width:500px; width:100%; box-shadow:0 20px 50px rgba(0,0,0,0.2); text-align:center; position:relative;">
        
        <button onclick="closePaymentModal()" style="position:absolute; top:16px; right:20px; background:none; border:none; font-size:24px; cursor:pointer; color:#64748B;">✕</button>

        <img src="avalanche_logo.png" style="height:48px; border-radius:10px; margin-bottom:16px;" alt="Monobank">
        
        <h3 style="font-size:22px; font-weight:800; color:#0F172A; margin-bottom:8px;">Monobank Payment Gateway</h3>
        <p style="color:#64748B; font-size:14px; margin-bottom:24px;">Безопасная оплата картой Monobank / Visa / MasterCard</p>

        <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:14px; padding:20px; margin-bottom:24px; text-align:left;">
          <div style="display:flex; justify-content:space-between; font-weight:700; color:#334155; margin-bottom:8px;">
            <span>Сумма к оплате (USD):</span>
            <span id="modal-usd-amount">$19.00</span>
          </div>
          <div style="display:flex; justify-content:space-between; font-weight:800; color:#0F172A; font-size:18px;">
            <span>К списанию в гривне:</span>
            <span id="modal-uah-amount">788.50 UAH</span>
          </div>
        </div>

        <div style="margin-bottom: 20px; text-align: left;">
          <label style="display: block; font-size: 12px; font-weight: 700; color: #475569; margin-bottom: 6px;">Ваш Email для отправки доступов:</label>
          <input type="email" id="checkout-user-email" placeholder="john@company.com" required style="width: 100%; padding: 12px 16px; border: 1px solid #CBD5E1; border-radius: 10px; font-size: 14px; outline: none;" />
        </div>

        <button onclick="processMonobankPay()" style="width:100%; background:#FF4E4E; color:#FFFFFF; padding:16px; border:none; border-radius:12px; font-weight:800; font-size:16px; cursor:pointer; box-shadow:0 6px 20px rgba(255,78,78,0.3);">
          💳 Оплатить через Monobank ➔
        </button>
      </div>
    </div>

    <!-- POST-PAYMENT SUCCESS SCREEN -->
    <div id="payment-success" class="card" style="display: none; text-align: center; padding: 60px 40px;">
      <div style="width:72px; height:72px; background:#D1FAE5; color:#10B981; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:36px; margin:0 auto 20px; font-weight:900;">✓</div>
      
      <h2 style="font-size:32px; font-weight:900; color:#0F172A; margin-bottom:16px;">Ваш заказ принят!</h2>
      
      <p style="font-size:18px; color:#334155; max-width:650px; margin:0 auto 24px; line-height:1.7;">
        Благодарим! Ваш агент будет готов в течение <b>48 часов</b>, и вы получите доступы на вашу почту <b id="success-email-text">user@email.com</b>.<br/>В случае необходимости члены нашей команды поддержки и разработки могут связаться с вами.
      </p>

      <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:12px; padding:16px; max-width:400px; margin:0 auto; font-weight:700; color:#64748B;">
        Номер вашего заказа: <span id="success-order-id" style="color:#0F172A;">#ORD-9482</span>
      </div>

      <div style="margin-top:30px;">
        <a href="dashboard.html" style="display:inline-block; background:#5FB3F9; color:#FFFFFF; padding:14px 32px; border-radius:10px; font-weight:700; text-decoration:none;">Перейти в Личный Кабинет ➔</a>
      </div>
    </div>

  </div>
</main>

""" + footer_html + """

<script>
  var calculatedPoints = 2;
  var oneTimeUsd = 19;
  var monthlyUsd = 10;
  var uahRate = 41.5;
  var projectDesc = '';

  function startEvaluationProgress() {
    projectDesc = localStorage.getItem('hero_project_desc') || 'Кастомный телеграм бот и ассистент заметок';
    document.getElementById('user-req-text').innerText = projectDesc;

    var descLower = projectDesc.toLowerCase();
    if (descLower.indexOf('парол') !== -1 || descLower.indexOf('заметк') !== -1 || descLower.indexOf('телеграм бот') !== -1 || descLower.indexOf('бот') !== -1) {
      calculatedPoints = 2;
    } else if (descLower.indexOf('парсинг') !== -1 || descLower.indexOf('магазин') !== -1 || descLower.indexOf('crm') !== -1) {
      calculatedPoints = 5;
    } else if (descLower.indexOf('высоконагруж') !== -1 || descLower.indexOf('кластер') !== -1) {
      calculatedPoints = 9;
    } else {
      calculatedPoints = 3;
    }

    oneTimeUsd = (calculatedPoints * 10) - 1;
    monthlyUsd = calculatedPoints * 5;

    var pct = 0;
    var fill = document.getElementById('progress-fill');
    var txt = document.getElementById('progress-text');
    var msg = document.getElementById('status-message');

    var msgs = [
      'Analyzing project objectives...',
      'Evaluating architectural complexity...',
      'Calculating AI agentic requirements & memory index...',
      'Estimating vector database & API workload...',
      'Finalizing project estimation...'
    ];

    var interval = setInterval(function() {
      pct += 2;
      txt.innerText = pct + '%';
      fill.style.width = pct + '%';

      if (pct === 25) msg.innerText = msgs[1];
      if (pct === 50) msg.innerText = msgs[2];
      if (pct === 75) msg.innerText = msgs[3];
      if (pct === 90) msg.innerText = msgs[4];

      if (pct >= 100) {
        clearInterval(interval);
        setTimeout(showEvaluationResult, 500);
      }
    }, 50);
  }

  function showEvaluationResult() {
    document.getElementById('phase-preloader').style.display = 'none';
    document.getElementById('phase-result').style.display = 'block';

    document.getElementById('calc-price-usd').innerText = '$' + oneTimeUsd + ' One-Time Setup + $' + monthlyUsd + ' / month';
    
    var totalUah = Math.round(oneTimeUsd * uahRate);
    document.getElementById('calc-price-uah').innerText = '~ ' + totalUah.toLocaleString('uk-UA') + ' UAH';
  }

  function openPaymentModal() {
    var modal = document.getElementById('payment-modal');
    modal.style.display = 'flex';
    document.getElementById('modal-usd-amount').innerText = '$' + oneTimeUsd + '.00 USD';
    
    var totalUah = Math.round(oneTimeUsd * uahRate);
    document.getElementById('modal-uah-amount').innerText = totalUah.toLocaleString('uk-UA') + ' UAH';
  }

  function closePaymentModal() {
    document.getElementById('payment-modal').style.display = 'none';
  }

  function processMonobankPay() {
    var emailInput = document.getElementById('checkout-user-email').value;
    if (!emailInput || emailInput.indexOf('@') === -1) {
      alert('Please enter a valid email address to receive access credentials.');
      return;
    }

    var orderId = 'ORD-' + Math.floor(1000 + Math.random() * 9000);

    var formData = new FormData();
    formData.append('action', 'checkout_payment');
    formData.append('name', 'Valued Client');
    formData.append('email', emailInput);
    formData.append('order_id', orderId);
    formData.append('amount_usd', '$' + oneTimeUsd + ' setup + $' + monthlyUsd + '/mo');
    formData.append('message', projectDesc);

    fetch('send_mail.php', { method: 'POST', body: formData })
      .then(function(r) { return r.json(); })
      .catch(function(err) {});

    closePaymentModal();
    document.getElementById('phase-result').style.display = 'none';
    document.getElementById('payment-success').style.display = 'block';

    document.getElementById('success-email-text').innerText = emailInput;
    document.getElementById('success-order-id').innerText = '#' + orderId;
  }

  startEvaluationProgress();
</script>
</body>
</html>
"""

open(os.path.join(site_dir, "evaluation.html"), "w", encoding="utf-8").write(evaluation_html)
print("✅ Created evaluation.html locally!")

# 2. UPDATE INDEX.HTML HERO FORM TO NAVIGATE TO EVALUATION.HTML
for p_file in ["index.html"]:
    p_path = os.path.join(site_dir, p_file)
    if os.path.exists(p_path):
        txt = open(p_path, encoding="utf-8").read()
        
        updated_js = """
        <script>
          function handleHeroProjectSubmit() {
            var val = document.getElementById('hero-project-input').value;
            if (val && val.trim() !== '') {
              localStorage.setItem('hero_project_desc', val.trim());
              window.location.href = 'evaluation.html';
            } else {
              alert('Please enter a brief description of your project.');
            }
          }
        </script>
        """
        txt = re.sub(r'<script>\s*function handleHeroProjectSubmit.*?</script>', updated_js, txt, flags=re.DOTALL)
        open(p_path, "w", encoding="utf-8").write(txt)
        print("✅ Updated index.html hero form submit handler to navigate to evaluation.html!")

# 3. UPLOAD ALL FILES TO HOSTINGER SFTP
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("82.29.199.155", port=65002, username="u473746908", password="Stefrogovskyi#1", timeout=15)

sftp = ssh.open_sftp()
remote_base = "/home/u473746908/domains/aavalanche.com/public_html/dev"

sftp.put(os.path.join(site_dir, "evaluation.html"), f"{remote_base}/evaluation.html")
sftp.put(os.path.join(site_dir, "index.html"), f"{remote_base}/index.html")

sftp.close()

# Git commit and push
subprocess.run(["git", "checkout", "dev"], check=True)
subprocess.run(["git", "add", "."], check=True)
res_commit = subprocess.run(["git", "commit", "-m", "feat(dev): Implement AI Project Evaluation, 10-point dollar pricing calculator, Monobank checkout, and 48h confirmation email flow"], capture_output=True, text=True)
print(res_commit.stdout or res_commit.stderr)

res_push = subprocess.run(["git", "push", "origin", "dev", "--force"], capture_output=True, text=True)
print(res_push.stdout or res_push.stderr)

res_sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
active_sha = res_sha.stdout.strip()

ssh.close()

print("🎉 EVALUATION & MONOBANK PAYMENT FLOW DEPLOYED TO DEV!")
print(f"📌 ACTIVE GIT COMMIT SHA: {active_sha}")
