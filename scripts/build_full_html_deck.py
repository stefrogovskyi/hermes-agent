# -*- coding: utf-8 -*-
"""
build_full_html_deck.py — Сборщик полной 11-слайдовой HTML-презентации Navo24 с исправным JS-контроллером.
"""

import os

REPORTS_DIR = r"C:\Users\Stefan\AppData\Local\hermes\reports"
html_path = os.path.join(REPORTS_DIR, "navo24_team_presentation.html")

full_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>The Next Chapter: Our Path to Break Free and Win — Navo24</title>
  <style>
    :root {
      --bg-dark: #0B0F19;
      --card-bg: #111827;
      --card-border: rgba(255, 255, 255, 0.08);
      --accent-sky: #0284C7;
      --accent-cyan: #38BDF8;
      --accent-emerald: #10B981;
      --accent-amber: #F59E0B;
      --text-main: #F8FAFC;
      --text-muted: #94A3B8;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
      background-color: var(--bg-dark);
      color: var(--text-main);
      overflow-x: hidden;
      display: flex;
      flex-direction: column;
      align-items: center;
      min-height: 100vh;
      padding: 20px;
    }

    .deck-header {
      width: 100%;
      max-width: 1200px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 15px 25px;
      background: rgba(17, 24, 39, 0.85);
      backdrop-filter: blur(16px);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      margin-bottom: 25px;
      z-index: 100;
    }
    .brand-logo {
      display: flex;
      align-items: center;
      gap: 10px;
      font-weight: 800;
      font-size: 1.3rem;
      letter-spacing: -0.5px;
    }
    .brand-logo span { color: var(--accent-cyan); }
    .badge {
      background: rgba(2, 132, 199, 0.15);
      border: 1px solid var(--accent-sky);
      color: var(--accent-cyan);
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 0.8rem;
      font-weight: 600;
      text-transform: uppercase;
    }

    .deck-controls {
      display: flex;
      gap: 15px;
      align-items: center;
    }
    .btn-nav {
      background: var(--accent-sky);
      color: white;
      border: none;
      padding: 8px 18px;
      border-radius: 8px;
      font-weight: 600;
      font-size: 0.95rem;
      cursor: pointer;
      transition: all 0.2s;
    }
    .btn-nav:hover { background: var(--accent-cyan); color: #000; }

    .deck-container {
      width: 100%;
      max-width: 1200px;
      min-height: 680px;
      position: relative;
    }

    .slide {
      display: none;
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 24px;
      padding: 50px 60px;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
      position: relative;
      overflow: hidden;
    }
    .slide.active {
      display: block;
      animation: fadeIn 0.3s ease-out forwards;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(8px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .glow-bg {
      position: absolute;
      top: -100px;
      right: -100px;
      width: 350px;
      height: 350px;
      background: radial-gradient(circle, rgba(2, 132, 199, 0.2) 0%, rgba(0,0,0,0) 70%);
      pointer-events: none;
    }

    .slide-tag {
      color: var(--accent-cyan);
      font-size: 0.9rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1.5px;
      margin-bottom: 12px;
    }
    .slide-title {
      font-size: 2.4rem;
      font-weight: 800;
      line-height: 1.15;
      margin-bottom: 16px;
      color: #FFF;
    }
    .slide-subtitle {
      font-size: 1.2rem;
      color: var(--text-muted);
      line-height: 1.5;
      margin-bottom: 35px;
    }

    .hero-slide {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: flex-start;
      min-height: 560px;
      background: linear-gradient(135deg, rgba(17, 24, 39, 0.95) 0%, rgba(11, 15, 25, 0.98) 100%),
                  radial-gradient(circle at top right, rgba(2, 132, 199, 0.3), transparent 60%);
    }
    .hero-title {
      font-size: 3.5rem;
      font-weight: 900;
      line-height: 1.1;
      margin-bottom: 20px;
      color: #FFF;
    }
    .hero-subtitle {
      font-size: 1.4rem;
      color: var(--accent-cyan);
      max-width: 800px;
      line-height: 1.5;
    }

    .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }
    .grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 25px; }

    .feature-card {
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid var(--card-border);
      padding: 28px;
      border-radius: 16px;
      transition: all 0.3s;
    }
    .feature-card:hover {
      border-color: var(--accent-sky);
      transform: translateY(-4px);
    }
    .card-icon {
      font-size: 2rem;
      margin-bottom: 15px;
      color: var(--accent-cyan);
    }
    .card-title {
      font-size: 1.25rem;
      font-weight: 700;
      margin-bottom: 10px;
      color: #FFF;
    }
    .card-text {
      color: var(--text-muted);
      font-size: 0.95rem;
      line-height: 1.6;
    }

    .comp-table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 15px;
    }
    .comp-table th, .comp-table td {
      padding: 14px 20px;
      text-align: left;
      border-bottom: 1px solid var(--card-border);
    }
    .comp-table th {
      background: rgba(2, 132, 199, 0.1);
      color: var(--accent-cyan);
      font-weight: 700;
      font-size: 1rem;
    }
    .comp-table td {
      font-size: 0.95rem;
      color: var(--text-main);
    }
    .tag-us { color: var(--accent-emerald); font-weight: 700; }
    .tag-them { color: #EF4444; font-weight: 600; }

    .metric-hero {
      font-size: 3.5rem;
      font-weight: 900;
      color: var(--accent-emerald);
      margin-bottom: 8px;
    }

    .quote-box {
      border-left: 4px solid var(--accent-sky);
      padding: 20px 25px;
      background: rgba(2, 132, 199, 0.05);
      border-radius: 0 16px 16px 0;
      font-size: 1.2rem;
      font-style: italic;
      color: #F1F5F9;
      margin-bottom: 25px;
      line-height: 1.6;
    }

    .bullet-list { list-style: none; }
    .bullet-list li {
      position: relative;
      padding-left: 28px;
      margin-bottom: 16px;
      font-size: 1.1rem;
      color: var(--text-main);
      line-height: 1.5;
    }
    .bullet-list li::before {
      content: "➔";
      position: absolute;
      left: 0;
      color: var(--accent-cyan);
      font-weight: bold;
    }

    .slide-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 35px;
      padding-top: 15px;
      border-top: 1px solid var(--card-border);
      color: var(--text-muted);
      font-size: 0.85rem;
    }
  </style>
</head>
<body>

  <header class="deck-header">
    <div class="brand-logo">
      <span>NAVO24</span> / Enterprise Team Deck
    </div>
    <div class="badge">Team Briefing 2026</div>
    <div class="deck-controls">
      <button class="btn-nav" onclick="prevSlide()">◀ Prev</button>
      <span id="slide-num" style="font-weight: bold; color: var(--accent-cyan); font-size: 1rem;">Slide 1 / 11</span>
      <button class="btn-nav" onclick="nextSlide()">Next ▶</button>
    </div>
  </header>

  <main class="deck-container">

    <!-- Slide 1 -->
    <section class="slide active hero-slide">
      <div class="glow-bg"></div>
      <div class="slide-tag">Executive Strategy Briefing</div>
      <h1 class="hero-title">The Next Chapter:<br>Our Path to Break Free and Win</h1>
      <p class="hero-subtitle">A candid message on transition, ownership, and our limitless future.</p>
      <div class="slide-footer" style="width: 100%; margin-top: 60px;">
        <span>Navo24 Leadership Team</span>
        <span>Slide 1 / 11</span>
      </div>
    </section>

    <!-- Slide 2 -->
    <section class="slide">
      <div class="glow-bg"></div>
      <div class="slide-tag">Slide 02 / The Core Mindset</div>
      <h2 class="slide-title">Obsession with Customer Success</h2>
      <p class="slide-subtitle">Shift Your Focus: From Transactions to Lifelong Relationships</p>
      <div class="grid-2">
        <div class="feature-card">
          <div class="card-icon">🤝</div>
          <h3 class="card-title">Customers for Life</h3>
          <p class="card-text">We aren't just selling tools or subscriptions; we are obsessively committed to solving real-world customer problems every single day.</p>
        </div>
        <div class="feature-card">
          <div class="card-icon">🚀</div>
          <h3 class="card-title">Service as Growth Engine</h3>
          <p class="card-text">Exceptional, proactive customer service is our primary growth driver. When customers win, our expansion becomes unstoppable.</p>
        </div>
      </div>
      <div class="slide-footer">
        <span>Navo24 Operating Philosophy</span>
        <span>Slide 2 / 11</span>
      </div>
    </section>

    <!-- Slide 3 -->
    <section class="slide">
      <div class="glow-bg"></div>
      <div class="slide-tag">Slide 03 / Potential & Earning Power</div>
      <h2 class="slide-title">$10,000+ Monthly Earnings</h2>
      <p class="slide-subtitle">A Realistic Target Built on Ownership, Not a Dream</p>
      <div class="grid-3">
        <div class="feature-card">
          <div class="metric-hero">$10k+</div>
          <h3 class="card-title">Absolute Reality</h3>
          <p class="card-text">We are 100% independent, AI & tech-empowered, and completely free from corporate red tape.</p>
        </div>
        <div class="feature-card">
          <div class="card-icon">🔥</div>
          <h3 class="card-title">Step Out of Comfort</h3>
          <p class="card-text">Leave the comfortable routine behind. Your income and trajectory now depend entirely on your drive and ownership.</p>
        </div>
        <div class="feature-card">
          <div class="card-icon">🛡️</div>
          <h3 class="card-title">Unshakeable Grit</h3>
          <p class="card-text">Early rejections will happen. Never give up—every setback is just valuable data to refine our execution.</p>
        </div>
      </div>
      <div class="slide-footer">
        <span>Personal Growth & Financial Freedom</span>
        <span>Slide 3 / 11</span>
      </div>
    </section>

    <!-- Slide 4 -->
    <section class="slide">
      <div class="glow-bg"></div>
      <div class="slide-tag">Slide 04 / Competitive Advantage</div>
      <h2 class="slide-title">Why We Break Through the Ceiling</h2>
      <p class="slide-subtitle">Speed, Agility, and Total Control vs. Corporate Giants</p>
      <table class="comp-table">
        <thead>
          <tr>
            <th>Operational Dimension</th>
            <th>Navo24 Agile Engine</th>
            <th>Corporate Giant</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Product Updates</strong></td>
            <td class="tag-us">Deployed instantly in real-time</td>
            <td class="tag-them">Months of bureaucratic review</td>
          </tr>
          <tr>
            <td><strong>Error Fixes</strong></td>
            <td class="tag-us">Automated, zero delays</td>
            <td class="tag-them">Endless ticket queues</td>
          </tr>
          <tr>
            <td><strong>Marketing & Outreach</strong></td>
            <td class="tag-us">Targeted, agile, hyper-fast</td>
            <td class="tag-them">Slow, generic campaigns</td>
          </tr>
          <tr>
            <td><strong>Customization</strong></td>
            <td class="tag-us">100% tailored per customer</td>
            <td class="tag-them">Rigid "one size fits all"</td>
          </tr>
        </tbody>
      </table>
      <div class="slide-footer">
        <span>Agility = Victory</span>
        <span>Slide 4 / 11</span>
      </div>
    </section>

    <!-- Slide 5 -->
    <section class="slide">
      <div class="glow-bg"></div>
      <div class="slide-tag">Slide 05 / Leadership Commitment</div>
      <h2 class="slide-title">True Loyalty & Skin in the Game</h2>
      <div class="quote-box">
        "A captain stays with his ship. My commitment to this vision and to our people has always been 100% absolute. Brand is important, but PEOPLE are paramount."
      </div>
      <ul class="bullet-list">
        <li><strong>Shared Lifeline:</strong> This business is my primary focus and lifeline too—we rise and win together.</li>
        <li><strong>Reflecting on Transition:</strong> Many doubted during the corporate transition, but my dedication to our team was never in question.</li>
        <li><strong>Total Investment:</strong> I am fully invested because I genuinely believe in our collective mastery and inevitable success.</li>
      </ul>
      <div class="slide-footer">
        <span>Leadership & Loyalty</span>
        <span>Slide 5 / 11</span>
      </div>
    </section>

    <!-- Slide 6 -->
    <section class="slide">
      <div class="glow-bg"></div>
      <div class="slide-tag">Slide 06 / Crucial Context</div>
      <h2 class="slide-title">Taking Ownership of Our Future</h2>
      <p class="slide-subtitle">The DP World Reality: Our Unstoppable Catalyst</p>
      <ul class="bullet-list" style="margin-bottom: 30px;">
        <li><strong>Official Corporate Reality:</strong> DP World is shutting down service extensions and client renewals (August sales blocked, July/August/September bonuses impacted).</li>
        <li><strong>Formal Steps Underway:</strong> We are confirming notice terms to notify clients transparently and protect their interests.</li>
        <li><strong>The Unstoppable Takeaway:</strong> We no longer depend on external corporate decisions or red tape. We own our destiny starting right now.</li>
      </ul>
      <div class="slide-footer">
        <span>Total Independence</span>
        <span>Slide 6 / 11</span>
      </div>
    </section>

    <!-- Slide 7 -->
    <section class="slide">
      <div class="glow-bg"></div>
      <div class="slide-tag">Slide 07 / Mobilization</div>
      <h2 class="slide-title">Time to Mobilize: The 60-Day Push</h2>
      <p class="slide-subtitle">Bite the Bullet: The 2-Month High-Intensity Sprint</p>
      <div class="grid-2">
        <div class="feature-card" style="border-color: var(--accent-amber);">
          <div class="card-icon" style="color: var(--accent-amber);">⚡</div>
          <h3 class="card-title">Intense Mobilization</h3>
          <p class="card-text">The next 2 months require extraordinary focus and going beyond standard 8-hour workdays. Every hour counts.</p>
        </div>
        <div class="feature-card" style="border-color: var(--accent-emerald);">
          <div class="card-icon" style="color: var(--accent-emerald);">🎯</div>
          <h3 class="card-title">Unstoppable Momentum</h3>
          <p class="card-text">This sprint is mandatory to put us firmly on our feet and establish market momentum that no competitor can stop.</p>
        </div>
      </div>
      <div class="slide-footer">
        <span>60-Day Sprint Mode</span>
        <span>Slide 7 / 11</span>
      </div>
    </section>

    <!-- Slide 8 -->
    <section class="slide">
      <div class="glow-bg"></div>
      <div class="slide-tag">Slide 08 / Execution Standards</div>
      <h2 class="slide-title">The Three Pillars of Execution</h2>
      <p class="slide-subtitle">Our Non-Negotiable Standards for the Sprint</p>
      <div class="grid-3">
        <div class="feature-card">
          <div class="card-icon">1️⃣</div>
          <h3 class="card-title">Discipline</h3>
          <p class="card-text">Zero excuses, no "I forgot" moments, total operational precision and punctuality in every detail.</p>
        </div>
        <div class="feature-card">
          <div class="card-icon">2️⃣</div>
          <h3 class="card-title">Responsibility</h3>
          <p class="card-text">End-to-end ownership of every lead, client, and issue until 100% resolved.</p>
        </div>
        <div class="feature-card">
          <div class="card-icon">3️⃣</div>
          <h3 class="card-title">Marketing Drive</h3>
          <p class="card-text">Aggressive outreach, loud market presence, and precise targeted growth across all channels.</p>
        </div>
      </div>
      <div class="slide-footer">
        <span>Operating Standards</span>
        <span>Slide 8 / 11</span>
      </div>
    </section>

    <!-- Slide 9 -->
    <section class="slide">
      <div class="glow-bg"></div>
      <div class="slide-tag">Slide 09 / Culture</div>
      <h2 class="slide-title">Spartan Mode Activation</h2>
      <p class="slide-subtitle">High Intensity, Zero Friction, Total Accountability</p>
      <div class="quote-box" style="border-color: var(--accent-amber); background: rgba(245, 158, 11, 0.05);">
        "We embrace a spartan, high-performance culture where speed, grit, and accountability drive daily wins. Zero drama, zero friction, maximum focus."
      </div>
      <div class="grid-2">
        <div class="feature-card">
          <h3 class="card-title">Grit & Speed</h3>
          <p class="card-text">Executing ideas in hours, not weeks. Solving issues live on calls with customers.</p>
        </div>
        <div class="feature-card">
          <h3 class="card-title">Daily Victories</h3>
          <p class="card-text">Tracking progress daily, holding ourselves accountable, and celebrating every closed deal.</p>
        </div>
      </div>
      <div class="slide-footer">
        <span>High-Performance Culture</span>
        <span>Slide 9 / 11</span>
      </div>
    </section>

    <!-- Slide 10 -->
    <section class="slide hero-slide">
      <div class="glow-bg"></div>
      <div class="slide-tag">Slide 10 / Closing</div>
      <h1 class="hero-title" style="font-size: 3rem;">We Have Everything We Need to Win</h1>
      <p class="hero-subtitle" style="color: #F8FAFC; margin-bottom: 30px;">
        This is not just about company survival—it's about personal growth, financial mastery, and reaching a whole new level together.
      </p>
      <div style="font-size: 1.8rem; font-weight: 800; color: var(--accent-cyan);">
        Let's build this future NOW.
      </div>
      <div class="slide-footer" style="width: 100%; margin-top: 60px;">
        <span>Navo24 Leadership & Team</span>
        <span>Slide 10 / 11</span>
      </div>
    </section>

    <!-- Slide 11: Financial Audit -->
    <section class="slide">
      <div class="glow-bg"></div>
      <div class="slide-tag">Slide 11 / Financial Audit & Baseline</div>
      <h2 class="slide-title">Current Sales Revenue & Team Portfolio</h2>
      <p class="slide-subtitle">A Solid $345,000+ Monthly Revenue Foundation Managed by 8 B2B Consultants</p>

      <div class="grid-3" style="margin-bottom: 20px;">
        <div class="feature-card" style="padding: 16px 20px;">
          <div style="font-size: 0.8rem; font-weight: 700; color: var(--accent-cyan); text-transform: uppercase;">Monthly Cash-Flow</div>
          <div style="font-size: 2rem; font-weight: 900; color: var(--accent-emerald); margin: 4px 0;">$167,122 / mo</div>
          <div style="font-size: 0.75rem; color: var(--text-muted);">Factual active monthly recurring stream</div>
        </div>
        <div class="feature-card" style="padding: 16px 20px;">
          <div style="font-size: 0.8rem; font-weight: 700; color: var(--accent-cyan); text-transform: uppercase;">Annual Portfolio (ARR)</div>
          <div style="font-size: 2rem; font-weight: 900; color: var(--accent-sky); margin: 4px 0;">$2,034,223 / yr</div>
          <div style="font-size: 0.75rem; color: var(--text-muted);">$198,685 / mo amortized equivalent</div>
        </div>
        <div class="feature-card" style="padding: 16px 20px;">
          <div style="font-size: 0.8rem; font-weight: 700; color: var(--accent-cyan); text-transform: uppercase;">Total Gross Stream</div>
          <div style="font-size: 2rem; font-weight: 900; color: #FFF; margin: 4px 0;">$345,807 / mo</div>
          <div style="font-size: 0.75rem; color: var(--text-muted);">Combined monthly business volume (8 Consultants)</div>
        </div>
      </div>

      <table class="comp-table" style="font-size: 0.9rem;">
        <thead>
          <tr>
            <th>Sales Consultant</th>
            <th>Monthly Stream (PAYG/Mo)</th>
            <th>Annual Portfolio (ARR)</th>
            <th>Monthly Amortization</th>
            <th>Key Accounts & Status</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Katya Komarova</strong></td>
            <td>$50,000 / mo</td>
            <td>$600,000 / yr</td>
            <td>$50,000 / mo</td>
            <td>Top 3 PAYG ($50k/mo, contract to Sept 2026/2027)</td>
          </tr>
          <tr>
            <td><strong>Sasha Grabarchuk</strong></td>
            <td>$58,844 / mo</td>
            <td>$700,000 / yr</td>
            <td>$58,333 / mo</td>
            <td>$38.9k/mo + $15.1k/mo (Renewal due Oct 2026)</td>
          </tr>
          <tr>
            <td><strong>Lilya Khovrak</strong></td>
            <td>$30,000 / mo</td>
            <td>$150,000 / yr</td>
            <td>$41,667 / mo</td>
            <td>Strong recurring base ($10k-$30k/mo)</td>
          </tr>
          <tr>
            <td><strong>Lera Guliy</strong></td>
            <td>$13,500 / mo</td>
            <td>$300,000 / yr</td>
            <td>$25,000 / mo</td>
            <td>$12k-$15k/mo (Renewal due Oct 3 2026 - $300k ARR)</td>
          </tr>
          <tr>
            <td><strong>Andrey Gorodinsky</strong></td>
            <td>$11,000 / mo</td>
            <td>$92,000 / yr</td>
            <td>$7,667 / mo</td>
            <td>Nauta ($6.5k), First ($2.2k), Herpot ($15k/qtr Sept 2026)</td>
          </tr>
          <tr>
            <td><strong>Oleg Chervinsky</strong></td>
            <td>$1,478 / mo</td>
            <td>$39,433 / yr</td>
            <td>$3,286 / mo</td>
            <td>Tradewind ($4.4k trial ends Aug 2026), Perdue, Nauffar</td>
          </tr>
          <tr>
            <td><strong>Katya Kernesh</strong></td>
            <td>$1,300 / mo</td>
            <td>$100,790 / yr</td>
            <td>$8,399 / mo</td>
            <td>1 recurring client ($1.3k/mo, $57.6k ARR due Nov 2026)</td>
          </tr>
          <tr>
            <td><strong>Katya Kapustyan</strong></td>
            <td>$1,000 / mo</td>
            <td>$52,000 / yr</td>
            <td>$4,333 / mo</td>
            <td>Small tier accounts (&lt;$1k/mo, $52k ARR due April/June 2027)</td>
          </tr>
          <tr style="background: rgba(2, 132, 199, 0.15); font-weight: bold;">
            <td><strong>TOTAL TEAM (8)</strong></td>
            <td style="color: var(--accent-emerald);">$167,122 / mo</td>
            <td style="color: var(--accent-cyan);">$2,034,223 / yr</td>
            <td>$345,807 / mo</td>
            <td>8 B2B Sales Consultants Portfolio</td>
          </tr>
        </tbody>
      </table>

      <div class="slide-footer">
        <span>Financial Audit & Baseline</span>
        <span>Slide 11 / 11</span>
      </div>
    </section>

  </main>

  <script>
    let currentSlide = 0;
    const slides = document.querySelectorAll('.slide');
    const slideNum = document.getElementById('slide-num');

    function showSlide(index) {
      if (index < 0) index = 0;
      if (index >= slides.length) index = slides.length - 1;
      
      currentSlide = index;
      
      slides.forEach((slide, i) => {
        if (i === currentSlide) {
          slide.classList.add('active');
        } else {
          slide.classList.remove('active');
        }
      });
      
      if (slideNum) {
        slideNum.textContent = `Slide ${currentSlide + 1} / ${slides.length}`;
      }
      
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function nextSlide() {
      if (currentSlide < slides.length - 1) {
        showSlide(currentSlide + 1);
      }
    }

    function prevSlide() {
      if (currentSlide > 0) {
        showSlide(currentSlide - 1);
      }
    }

    document.addEventListener('keydown', function(e) {
      if (e.key === 'ArrowRight' || e.key === 'Space') {
        nextSlide();
      } else if (e.key === 'ArrowLeft') {
        prevSlide();
      }
    });

    showSlide(0);
  </script>
</body>
</html>
"""

open(html_path, 'w', encoding='utf-8').write(full_html)
print('✅ Successfully built full_html deck with active slide controller!')
