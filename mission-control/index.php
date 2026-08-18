<?php
// AgentOS Admin Gateway Auth Check
ini_set('session.cookie_path', '/');
if (session_status() == PHP_SESSION_NONE) {
    session_set_cookie_params([
        'lifetime' => 86400 * 30,
        'path' => '/',
        'samesite' => 'Lax'
    ]);
    session_start();
}

$is_admin = false;

if (isset($_SESSION['role']) && $_SESSION['role'] === 'admin') {
    $is_admin = true;
} elseif (isset($_SESSION['user']) && is_array($_SESSION['user']) && isset($_SESSION['user']['role']) && $_SESSION['user']['role'] === 'admin') {
    $is_admin = true;
} elseif (isset($_SESSION['user_id']) || (isset($_SESSION['user']['id']))) {
    $uid = $_SESSION['user_id'] ?? $_SESSION['user']['id'];
    try {
        $pdo = new PDO('sqlite:' . __DIR__ . '/../data/database.sqlite');
        $stmt = $pdo->prepare("SELECT role, name FROM users WHERE id = ?");
        $stmt->execute([$uid]);
        $r = $stmt->fetch(PDO::FETCH_ASSOC);
        if ($r && $r['role'] === 'admin') {
            $is_admin = true;
            $_SESSION['role'] = 'admin';
            $_SESSION['name'] = $r['name'];
        }
    } catch (Exception $e) {}
}

if (!$is_admin) {
    header('Location: /login.html?redirect=' . urlencode('/agentos/'));
    exit;
}

// Proxy API calls locally to VPS if requested
if (isset($_GET['api'])) {
    header('Content-Type: application/json; charset=utf-8');
    $api = $_GET['api'];
    $profile = $_GET['profile'] ?? 'hermes';
    $limit = $_GET['limit'] ?? '50';
    
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $post_data = file_get_contents('php://input');
        $opts = [
            'http' => [
                'method' => 'POST',
                'header' => 'Content-Type: application/json',
                'content' => $post_data,
                'timeout' => 8
            ]
        ];
        $ctx = stream_context_create($opts);
        $url = "http://38.49.219.217:8888/api/{$api}";
        $resp = @file_get_contents($url, false, $ctx);
        echo $resp ?: json_encode(['error' => 'API gateway offline']);
        exit;
    }

    $url = "http://38.49.219.217:8888/api/{$api}?profile=" . urlencode($profile) . "&limit=" . urlencode($limit);
    $ctx = stream_context_create(['http' => ['timeout' => 8]]);
    $resp = @file_get_contents($url, false, $ctx);
    if ($resp) {
        echo $resp;
    } else {
        echo json_encode(['error' => 'API gateway offline or unreachable']);
    }
    exit;
}
?>
<!DOCTYPE html>
<html lang="ru" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>⚡ AgentOS | Mission Control Enterprise</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/lucide@latest"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            brand: {
              50: '#f0fdf4',
              500: '#10b981',
              600: '#059669',
              900: '#064e3b',
            },
            dark: {
              950: '#05070a',
              900: '#090d14',
              850: '#0d131e',
              800: '#111927',
              750: '#162032',
              700: '#1e293b',
              650: '#27354a',
              600: '#334155',
            }
          }
        }
      }
    }
  </script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    body { font-family: 'Plus Jakarta Sans', sans-serif; }
    code, pre, .font-mono { font-family: 'JetBrains Mono', monospace; }
    .custom-scrollbar::-webkit-scrollbar { width: 5px; height: 5px; }
    .custom-scrollbar::-webkit-scrollbar-track { background: #090d14; }
    .custom-scrollbar::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 4px; }
    .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #334155; }
  </style>
</head>
<body class="bg-dark-950 text-gray-100 flex h-screen overflow-hidden antialiased select-none">

  <!-- LEVEL 1: PRIMARY SIDEBAR (64px / 240px wide) -->
  <aside class="w-60 bg-dark-900 border-r border-dark-800 flex flex-col justify-between shrink-0 z-20">
    <!-- Header -->
    <div>
      <div class="p-3 border-b border-dark-800 flex items-center justify-between">
        <div class="flex items-center space-x-2.5">
          <div class="w-8 h-8 rounded-lg bg-gradient-to-tr from-emerald-500 via-teal-500 to-cyan-500 flex items-center justify-center font-black text-white shadow-lg shadow-emerald-500/20 text-sm">
            ⚡
          </div>
          <div>
            <div class="font-extrabold text-xs tracking-wider text-white flex items-center gap-1.5">
              <span>AGENTOS</span>
              <span class="text-[9px] px-1 py-0.2 rounded bg-emerald-500/20 text-emerald-300 font-mono">v3.2</span>
            </div>
            <div class="text-[10px] text-emerald-400 flex items-center gap-1 font-mono">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
              7 AGENTS LIVE
            </div>
          </div>
        </div>
      </div>

      <!-- Level 1 Items -->
      <div class="p-2 space-y-3.5 overflow-y-auto max-h-[calc(100vh-125px)] custom-scrollbar">
        
        <!-- MASTER CLUSTER -->
        <div>
          <div class="px-2 text-[9px] font-bold uppercase tracking-wider text-gray-300 mb-1">Master Core</div>
          <div class="space-y-0.5">
            <button onclick="selectAgent('hermes')" id="agent-hermes" class="agent-nav-btn w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg text-xs font-semibold transition bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <div class="flex items-center space-x-2">
                <i data-lucide="crown" class="w-3.5 h-3.5 text-emerald-400"></i>
                <span class="truncate">Hermes Stevenson</span>
              </div>
              <span class="text-[9px] bg-emerald-500/20 text-emerald-300 px-1 py-0.5 rounded font-mono">Lead</span>
            </button>

            <button onclick="selectAgent('openclaw')" id="agent-openclaw" class="agent-nav-btn w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg text-xs font-medium text-gray-400 hover:bg-dark-800 hover:text-white transition">
              <div class="flex items-center space-x-2">
                <span class="text-xs">🦞</span>
                <span class="truncate">OpenClaw Gateway</span>
              </div>
              <span class="text-[9px] bg-cyan-500/20 text-cyan-300 px-1 py-0.5 rounded font-mono">:18789</span>
            </button>
          </div>
        </div>

        <!-- SPECIALIZED AGENTS (6 KANBANS) -->
        <div>
          <div class="px-2 text-[9px] font-bold uppercase tracking-wider text-gray-300 mb-1">Autonomous Sub-Agents</div>
          <div class="space-y-0.5">
            <button onclick="selectAgent('richard')" id="agent-richard" class="agent-nav-btn w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg text-xs text-gray-400 hover:bg-dark-800 hover:text-white transition">
              <div class="flex items-center space-x-2">
                <i data-lucide="briefcase" class="w-3.5 h-3.5 text-blue-400"></i>
                <span class="truncate">Richard</span>
              </div>
              <span class="text-[9px] text-gray-400 font-mono">Sales</span>
            </button>

            <button onclick="selectAgent('callum')" id="agent-callum" class="agent-nav-btn w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg text-xs text-gray-400 hover:bg-dark-800 hover:text-white transition">
              <div class="flex items-center space-x-2">
                <i data-lucide="code-2" class="w-3.5 h-3.5 text-purple-400"></i>
                <span class="truncate">Callum Vance</span>
              </div>
              <span class="text-[9px] text-gray-400 font-mono">Full-Stack</span>
            </button>

            <button onclick="selectAgent('alistair')" id="agent-alistair" class="agent-nav-btn w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg text-xs text-gray-400 hover:bg-dark-800 hover:text-white transition">
              <div class="flex items-center space-x-2">
                <i data-lucide="line-chart" class="w-3.5 h-3.5 text-amber-400"></i>
                <span class="truncate">Alistair</span>
              </div>
              <span class="text-[9px] text-gray-400 font-mono">Benchmark</span>
            </button>

            <button onclick="selectAgent('archie')" id="agent-archie" class="agent-nav-btn w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg text-xs text-gray-400 hover:bg-dark-800 hover:text-white transition">
              <div class="flex items-center space-x-2">
                <i data-lucide="pen-tool" class="w-3.5 h-3.5 text-pink-400"></i>
                <span class="truncate">Archie Wright</span>
              </div>
              <span class="text-[9px] text-gray-400 font-mono">Content</span>
            </button>

            <button onclick="selectAgent('liz')" id="agent-liz" class="agent-nav-btn w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg text-xs text-gray-400 hover:bg-dark-800 hover:text-white transition">
              <div class="flex items-center space-x-2">
                <i data-lucide="sparkles" class="w-3.5 h-3.5 text-rose-400"></i>
                <span class="truncate">Liz Harper</span>
              </div>
              <span class="text-[9px] text-gray-400 font-mono">Executive</span>
            </button>

            <button onclick="selectAgent('ben')" id="agent-ben" class="agent-nav-btn w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg text-xs text-gray-400 hover:bg-dark-800 hover:text-white transition">
              <div class="flex items-center space-x-2">
                <i data-lucide="activity" class="w-3.5 h-3.5 text-teal-400"></i>
                <span class="truncate">Ben</span>
              </div>
              <span class="text-[9px] text-gray-400 font-mono">Ops</span>
            </button>
          </div>
        </div>

        <!-- WORKFLOWS & FEEDS -->
        <div>
          <div class="px-2 text-[9px] font-bold uppercase tracking-wider text-gray-300 mb-1">Feeds & Ingress</div>
          <div class="space-y-0.5">
            <button onclick="selectAgent('career_scanner')" id="agent-career_scanner" class="agent-nav-btn w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg text-xs text-gray-400 hover:bg-dark-800 hover:text-white transition">
              <div class="flex items-center space-x-2">
                <i data-lucide="target" class="w-3.5 h-3.5 text-emerald-400"></i>
                <span class="truncate">Career Scanner</span>
              </div>
              <span class="text-[9px] text-emerald-400 font-mono">11 APIs</span>
            </button>

            <button onclick="selectAgent('odessa_router')" id="agent-odessa_router" class="agent-nav-btn w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg text-xs text-gray-400 hover:bg-dark-800 hover:text-white transition">
              <div class="flex items-center space-x-2">
                <i data-lucide="shield-alert" class="w-3.5 h-3.5 text-amber-400"></i>
                <span class="truncate">Odessa Router</span>
              </div>
              <span class="text-[9px] text-amber-400 font-mono">Live</span>
            </button>
          </div>
        </div>

      </div>
    </div>

    <!-- Admin Footer -->
    <div class="p-2.5 border-t border-dark-800 bg-dark-950 flex items-center justify-between">
      <div class="flex items-center space-x-2">
        <div class="w-7 h-7 rounded-full bg-dark-800 border border-dark-700 flex items-center justify-center font-bold text-[10px] text-emerald-400">
          AD
        </div>
        <div>
          <div class="text-xs font-semibold text-white leading-tight">Stefan (COO)</div>
          <div class="text-[9px] text-gray-400 font-mono">dr.reenforce@gmail.com</div>
        </div>
      </div>
      <button onclick="openSettingsModal()" class="text-gray-400 hover:text-white p-1 rounded hover:bg-dark-800 transition" title="Hermes Desktop Settings">
        <i data-lucide="settings" class="w-4 h-4 text-gray-300 hover:text-emerald-400"></i>
      </button>
    </div>
  </aside>

  <!-- LEVEL 2: SECONDARY SUBMENU (Exact 6 tabs requested) -->
  <aside class="w-56 bg-dark-850 border-r border-dark-800 flex flex-col justify-between shrink-0 z-10">
    <div class="p-3">
      <!-- Active Agent Name/Info Header -->
      <div class="pb-2.5 mb-2.5 border-b border-dark-700/80">
        <div class="text-[9px] uppercase font-bold text-gray-300 tracking-wider" id="submenu-category">Master Core</div>
        <div class="text-sm font-bold text-white mt-0.5 truncate" id="submenu-agent-name">Hermes Stevenson</div>
        <div class="text-[10px] text-emerald-400 font-mono mt-0.5 truncate" id="submenu-agent-role">Deputy Director & Lead</div>
      </div>

      <!-- Level 2 Submenu Tabs (Dashboard, Chat, Kanban, Crons, Capabilities, Artifacts) -->
      <div class="space-y-1" id="submenu-items-container">
        <!-- Dynamically Populated with the 6 exact tabs -->
      </div>
    </div>

    <!-- Status & Sync Indicator -->
    <div class="p-2.5 border-t border-dark-800 bg-dark-900/50 text-[10px] text-gray-400 flex items-center justify-between">
      <div class="flex items-center gap-1.5">
        <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
        <span>Gateway Sync</span>
      </div>
      <span class="font-mono text-emerald-400">Live 100%</span>
    </div>
  </aside>

  <!-- MAIN WORKSPACE -->
  <main class="flex-1 flex flex-col h-screen overflow-hidden bg-dark-950">
    
    <!-- Top Bar -->
    <header class="h-12 border-b border-dark-800 bg-dark-900/90 backdrop-blur px-5 flex items-center justify-between shrink-0">
      <div class="flex items-center space-x-3">
        <h1 id="view-title" class="font-bold text-xs md:text-sm text-white flex items-center gap-2">
          <i data-lucide="crown" class="w-4 h-4 text-emerald-400"></i>
          <span>Hermes Stevenson / Dashboard</span>
        </h1>
        <span id="view-badge" class="text-[10px] px-2 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 font-mono">
          Model: gemini-3.7-flash
        </span>
      </div>

      <div class="flex items-center space-x-2">
        <button onclick="refreshCurrentView()" class="p-1.5 text-gray-400 hover:text-white bg-dark-800 hover:bg-dark-700 rounded border border-dark-700 transition" title="Refresh">
          <i data-lucide="refresh-cw" class="w-3.5 h-3.5"></i>
        </button>
        <button onclick="openSettingsModal()" class="p-1.5 text-gray-400 hover:text-white bg-dark-800 hover:bg-dark-700 rounded border border-dark-700 transition" title="Global Model & Settings">
          <i data-lucide="sliders" class="w-3.5 h-3.5"></i>
        </button>
      </div>
    </header>

    <!-- Subheader Filter Bar (For Capabilities & Artifacts) -->
    <div id="filter-bar" class="h-10 border-b border-dark-800 bg-dark-900 px-5 flex items-center justify-between shrink-0 hidden">
      <div class="flex items-center space-x-2" id="filter-buttons-container">
        <!-- Dynamically filled filter pills -->
      </div>
      <div class="text-[11px] text-gray-400 font-mono" id="filter-count">Total: 0</div>
    </div>

    <!-- Content Workspace -->
    <div class="flex-1 relative overflow-hidden bg-dark-950">
      
      <!-- 1. RESPONSIVE FULL-WIDTH KANBAN VIEW (Single screen width without scrollbars) -->
      <div id="kanban-view" class="w-full h-full p-3 overflow-hidden hidden bg-dark-950 flex flex-col">
        <!-- Live Kanban Columns Header & Board -->
        <div class="flex-1 grid grid-cols-4 gap-3 h-full min-h-0" id="kanban-columns-container">
          <!-- 4 Columns: To Do, In Progress, Recurring / Cron, Completed -->
        </div>
      </div>

      <!-- 2. LIVE TWO-WAY CHAT SYNC (Identical to Telegram + Instant Send) -->
      <div id="chat-view" class="w-full h-full flex flex-col hidden bg-dark-950">
        <!-- Message stream container -->
        <div id="chat-messages" class="flex-1 p-4 md:p-6 overflow-y-auto custom-scrollbar space-y-3.5 max-w-4xl mx-auto w-full">
          <!-- Populated by live SQLite Stream -->
        </div>

        <!-- Chat Input Form (Telegram-like instant submission) -->
        <div class="p-3 border-t border-dark-800 bg-dark-900 shrink-0">
          <div class="max-w-4xl mx-auto w-full flex items-center gap-2">
            <textarea id="chat-input" rows="1" placeholder="Отправить сообщение агенту (синхронизируется с Telegram & Gateway)..." class="flex-1 bg-dark-800 border border-dark-700 rounded-lg px-3.5 py-2.5 text-xs text-white placeholder-gray-400 focus:outline-none focus:border-emerald-500 resize-none font-sans custom-scrollbar" onkeydown="handleChatKey(event)"></textarea>
            <button onclick="sendChatMessage()" id="chat-send-btn" class="bg-emerald-600 hover:bg-emerald-500 text-white p-2.5 rounded-lg transition flex items-center justify-center shrink-0">
              <i data-lucide="send" class="w-4 h-4"></i>
            </button>
          </div>
          <div class="max-w-4xl mx-auto w-full flex items-center justify-between text-[10px] text-gray-400 mt-1.5 px-1 font-mono">
            <span>Нажмите <b>Enter</b> для отправки, <b>Shift+Enter</b> для новой строки</span>
            <span class="text-emerald-400">● Gateway SQLite Sync: Active</span>
          </div>
        </div>
      </div>

      <!-- 3. DASHBOARD / CRONS / CAPABILITIES / ARTIFACTS NATIVE VIEW -->
      <div id="native-view" class="w-full h-full p-4 md:p-6 overflow-y-auto custom-scrollbar">
        <div id="view-content" class="space-y-6 max-w-6xl mx-auto">
          <!-- Native Component Render -->
        </div>
      </div>

    </div>
  </main>

  <!-- HERMES DESKTOP SETTINGS MODAL (Gear Icon / All Models / Config) -->
  <div id="settings-modal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4 hidden">
    <div class="bg-dark-900 border border-dark-700 rounded-2xl w-full max-w-3xl max-h-[85vh] flex flex-col overflow-hidden shadow-2xl">
      <!-- Modal Header -->
      <div class="p-4 border-b border-dark-800 flex items-center justify-between">
        <div class="flex items-center space-x-2.5">
          <i data-lucide="settings" class="w-5 h-5 text-emerald-400"></i>
          <div>
            <div class="text-sm font-bold text-white">Hermes Settings & Model Engine</div>
            <div class="text-[10px] text-gray-400 font-mono">Global Parameters & Multi-Provider Registry</div>
          </div>
        </div>
        <button onclick="closeSettingsModal()" class="p-1 rounded-lg text-gray-400 hover:text-white hover:bg-dark-800">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>

      <!-- Modal Body -->
      <div class="p-5 overflow-y-auto custom-scrollbar space-y-6 flex-1 text-xs">
        
        <!-- Section 1: Active Primary Model & Parameters -->
        <div>
          <h3 class="font-bold text-white uppercase tracking-wider text-[11px] mb-3 flex items-center gap-1.5">
            <i data-lucide="cpu" class="w-3.5 h-3.5 text-emerald-400"></i>
            <span>Активная модель и окружение</span>
          </h3>
          <div class="grid grid-cols-3 gap-3">
            <div class="bg-dark-850 p-3 rounded-lg border border-dark-750">
              <div class="text-gray-400 text-[10px]">Primary Model</div>
              <div class="text-white font-bold font-mono mt-1 text-xs" id="cfg-primary-model">google/gemini-3.7-flash</div>
            </div>
            <div class="bg-dark-850 p-3 rounded-lg border border-dark-750">
              <div class="text-gray-400 text-[10px]">Timeout / Retries</div>
              <div class="text-emerald-400 font-bold font-mono mt-1 text-xs">30s / 2 retries</div>
            </div>
            <div class="bg-dark-850 p-3 rounded-lg border border-dark-750">
              <div class="text-gray-400 text-[10px]">Fallback Pipeline</div>
              <div class="text-cyan-400 font-bold font-mono mt-1 text-xs">20 Active Fallbacks</div>
            </div>
          </div>
        </div>

        <!-- Section 2: All Configured Models Catalog -->
        <div>
          <h3 class="font-bold text-white uppercase tracking-wider text-[11px] mb-3 flex items-center gap-1.5">
            <i data-lucide="layers" class="w-3.5 h-3.5 text-cyan-400"></i>
            <span>Каталог всех подключенных моделей</span>
          </h3>
          <div class="space-y-2" id="settings-models-list">
            <!-- Dynamically populated from /api/settings -->
          </div>
        </div>

      </div>

      <!-- Modal Footer -->
      <div class="p-3 border-t border-dark-800 bg-dark-950 flex justify-between items-center text-xs">
        <span class="text-gray-400 font-mono text-[10px]">Config synced with /opt/hermes/config.yaml</span>
        <button onclick="closeSettingsModal()" class="px-4 py-1.5 bg-dark-800 hover:bg-dark-700 text-white rounded-lg font-semibold transition">
          Закрыть
        </button>
      </div>
    </div>
  </div>

  <!-- SCRIPT ENGINE -->
  <script>
    let currentAgent = 'hermes';
    let currentTab = 'dashboard';
    let currentFilter = 'all';
    let chatPollInterval = null;

    const AGENTS_META = {
      hermes: { name: 'Hermes Stevenson', role: 'Deputy Director & System Lead', category: 'Master Core', badge: 'gemini-3.7-flash' },
      openclaw: { name: 'OpenClaw Gateway', role: 'Autonomous Coding Gateway :18789', category: 'AI Coding Agent', badge: 'OpenClaw 2026.8.1' },
      richard: { name: 'Richard Marlowe', role: 'B2B Sales CRM (@richnavobot)', category: 'Autonomous Agent', badge: 'Sales Lead' },
      callum: { name: 'Callum Vance', role: 'Full-Stack Engineer (@callumvancebot)', category: 'Autonomous Agent', badge: 'Engineer' },
      alistair: { name: 'Alistair', role: 'Benchmark Lead (@alistairkanbanbot)', category: 'Autonomous Agent', badge: 'SeaRates vs Navo' },
      archie: { name: 'Archie Wright', role: 'Content Strategist (@archiewrightbot)', category: 'Autonomous Agent', badge: 'Copywriter' },
      liz: { name: 'Liz Harper', role: 'Executive Assistant', category: 'Autonomous Agent', badge: 'Operations' },
      ben: { name: 'Ben', role: 'Operations Specialist', category: 'Autonomous Agent', badge: 'Logistics' },
      career_scanner: { name: 'Career Scanner v2', role: '11 Verified APIs + Workday + Oracle', category: 'Feeds & Ingress', badge: 'Daily 09:00 MSK' },
      odessa_router: { name: 'Odessa Safe Router', role: 'Telethon Closed TG Group Ingress', category: 'Safety Feeds', badge: 'Session Active' }
    };

    // Exactly the 6 standard Level 2 tabs for ALL agents
    const STANDARD_TABS = [
      { id: 'dashboard', label: 'Dashboard', icon: 'layout-dashboard' },
      { id: 'chat', label: 'Chat', icon: 'message-square' },
      { id: 'kanban', label: 'Kanban', icon: 'columns' },
      { id: 'crons', label: 'Crons', icon: 'clock' },
      { id: 'capabilities', label: 'Capabilities', icon: 'cpu' },
      { id: 'artifacts', label: 'Artifacts', icon: 'file-text' }
    ];

    function selectAgent(agentId) {
      currentAgent = agentId;
      document.querySelectorAll('.agent-nav-btn').forEach(b => {
        b.className = 'agent-nav-btn w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg text-xs text-gray-400 hover:bg-dark-800 hover:text-white transition';
      });
      const actBtn = document.getElementById('agent-' + agentId);
      if (actBtn) {
        actBtn.className = 'agent-nav-btn w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg text-xs font-semibold transition bg-emerald-500/10 text-emerald-400 border border-emerald-500/20';
      }

      renderSubMenu(agentId);
      selectSubTab(currentTab || 'dashboard');
    }

    function renderSubMenu(agentId) {
      const meta = AGENTS_META[agentId] || AGENTS_META['hermes'];
      document.getElementById('submenu-category').innerText = meta.category;
      document.getElementById('submenu-agent-name').innerText = meta.name;
      document.getElementById('submenu-agent-role').innerText = meta.role;

      const container = document.getElementById('submenu-items-container');
      container.innerHTML = '';

      STANDARD_TABS.forEach(tab => {
        const btn = document.createElement('button');
        btn.id = 'subtab-' + tab.id;
        btn.onclick = () => selectSubTab(tab.id);
        btn.className = 'subtab-btn w-full flex items-center space-x-2 px-2.5 py-1.5 rounded-md text-xs text-gray-400 hover:bg-dark-800 hover:text-white transition';
        btn.innerHTML = `<i data-lucide="${tab.icon}" class="w-3.5 h-3.5"></i><span>${tab.label}</span>`;
        container.appendChild(btn);
      });
      lucide.createIcons();
    }

    function selectSubTab(tabId) {
      currentTab = tabId;
      if (chatPollInterval) {
        clearInterval(chatPollInterval);
        chatPollInterval = null;
      }

      document.querySelectorAll('.subtab-btn').forEach(b => {
        b.className = 'subtab-btn w-full flex items-center space-x-2 px-2.5 py-1.5 rounded-md text-xs text-gray-400 hover:bg-dark-800 hover:text-white transition';
      });
      const subBtn = document.getElementById('subtab-' + tabId);
      if (subBtn) {
        subBtn.className = 'subtab-btn w-full flex items-center space-x-2 px-2.5 py-1.5 rounded-md text-xs font-semibold bg-dark-750 text-emerald-400 border border-dark-650 transition';
      }

      const kanbanView = document.getElementById('kanban-view');
      const chatView = document.getElementById('chat-view');
      const nativeView = document.getElementById('native-view');
      const filterBar = document.getElementById('filter-bar');
      const title = document.getElementById('view-title');
      const badge = document.getElementById('view-badge');

      const meta = AGENTS_META[currentAgent] || AGENTS_META['hermes'];
      const tabObj = STANDARD_TABS.find(t => t.id === tabId);

      title.innerHTML = `<span class="text-white">${meta.name}</span> <span class="text-gray-400">/</span> <span class="text-emerald-400">${tabObj.label}</span>`;
      badge.innerText = meta.badge;

      filterBar.classList.add('hidden');

      // 1. KANBAN TAB (Full Screen Width, 4 Responsive Columns, Zero Horizontal Scroll)
      if (tabId === 'kanban') {
        chatView.classList.add('hidden');
        nativeView.classList.add('hidden');
        kanbanView.classList.remove('hidden');
        loadKanbanBoard(currentAgent);
      }
      // 2. LIVE CHAT TAB
      else if (tabId === 'chat') {
        kanbanView.classList.add('hidden');
        nativeView.classList.add('hidden');
        chatView.classList.remove('hidden');
        loadLiveChat(currentAgent);
        chatPollInterval = setInterval(() => loadLiveChat(currentAgent), 3500);
      }
      // 3. CAPABILITIES TAB (With Filter Pills)
      else if (tabId === 'capabilities') {
        kanbanView.classList.add('hidden');
        chatView.classList.add('hidden');
        nativeView.classList.remove('hidden');
        setupFilterBar(['All', 'Skills', 'Tools', 'MCP', 'Browse Hub'], 'All');
        loadCapabilities();
      }
      // 4. ARTIFACTS TAB (With Filter Pills)
      else if (tabId === 'artifacts') {
        kanbanView.classList.add('hidden');
        chatView.classList.add('hidden');
        nativeView.classList.remove('hidden');
        setupFilterBar(['All', 'Images', 'Files', 'Links'], 'All');
        loadArtifacts();
      }
      // 5. DASHBOARD & CRONS NATIVE TABS
      else {
        kanbanView.classList.add('hidden');
        chatView.classList.add('hidden');
        nativeView.classList.remove('hidden');
        renderNativeTab(tabId);
      }
      lucide.createIcons();
    }

    // --- KANBAN RENDERER (Single screen width without wrapping or scrolling) ---
    async function loadKanbanBoard(agent) {
      const container = document.getElementById('kanban-columns-container');
      container.innerHTML = '<div class="col-span-4 text-center text-xs text-gray-400 py-10">Загрузка карточек канбана...</div>';
      try {
        const res = await fetch(`/agentos/?api=kanban&profile=${agent}`);
        const data = await res.json();
        const cards = data.cards || [];

        const columns = [
          { id: 'todo', title: 'To Do', color: 'border-blue-500/30 text-blue-400 bg-blue-500/10' },
          { id: 'in_progress', title: 'In Progress', color: 'border-amber-500/30 text-amber-400 bg-amber-500/10' },
          { id: 'recurring', title: 'Recurring / Cron', color: 'border-purple-500/30 text-purple-400 bg-purple-500/10' },
          { id: 'completed', title: 'Completed', color: 'border-emerald-500/30 text-emerald-400 bg-emerald-500/10' }
        ];

        container.innerHTML = '';
        columns.forEach(col => {
          const colCards = cards.filter(c => c.column_id === col.id || (col.id === 'todo' && !c.column_id));
          
          const colEl = document.createElement('div');
          colEl.className = 'bg-dark-900 border border-dark-800 rounded-xl p-2.5 flex flex-col h-full overflow-hidden';
          
          colEl.innerHTML = `
            <div class="flex items-center justify-between pb-2 mb-2 border-b border-dark-800 shrink-0">
              <div class="flex items-center gap-1.5">
                <span class="text-xs font-bold text-white">${col.title}</span>
                <span class="text-[10px] px-1.5 py-0.2 rounded-full font-mono ${col.color}">${colCards.length}</span>
              </div>
            </div>
            <div class="flex-1 overflow-y-auto custom-scrollbar space-y-2 pr-1" id="col-cards-${col.id}">
              <!-- Cards -->
            </div>
          `;

          const cardsContainer = colEl.querySelector(`#col-cards-${col.id}`);
          if (colCards.length === 0) {
            cardsContainer.innerHTML = '<div class="text-center text-[11px] text-gray-400 py-6">Нет активных задач</div>';
          } else {
            colCards.forEach(card => {
              const cardEl = document.createElement('div');
              cardEl.className = 'bg-dark-850 hover:bg-dark-800 border border-dark-750 hover:border-dark-650 rounded-lg p-2.5 transition shadow-sm cursor-pointer';
              cardEl.innerHTML = `
                <div class="flex items-start justify-between gap-1 mb-1.5">
                  <div class="text-xs font-semibold text-gray-100 leading-snug">${escapeHtml(card.title)}</div>
                  <span class="text-[9px] px-1 py-0.2 rounded bg-dark-700 text-gray-300 font-mono shrink-0">${card.tag || 'TASK'}</span>
                </div>
                <div class="text-[11px] text-gray-400 line-clamp-3 leading-relaxed mb-2">${escapeHtml(card.desc || '')}</div>
                <div class="flex items-center justify-between text-[10px] text-gray-400 pt-1.5 border-t border-dark-800/80 font-mono">
                  <span>${card.assignee || AGENTS_META[agent].name}</span>
                  <span class="text-emerald-400">● Synced</span>
                </div>
              `;
              cardsContainer.appendChild(cardEl);
            });
          }

          container.appendChild(colEl);
        });
      } catch (e) {
        container.innerHTML = `<div class="col-span-4 text-center text-xs text-red-400 py-10">Ошибка загрузки канбана: ${e}</div>`;
      }
    }

    // --- LIVE CHAT SYNC (Instant 2-way communication) ---
    async function loadLiveChat(profile) {
      const container = document.getElementById('chat-messages');
      try {
        const res = await fetch(`/agentos/?api=messages&profile=${profile}&limit=50`);
        const data = await res.json();
        if (data.messages) {
          const isAtBottom = container.scrollHeight - container.scrollTop <= container.clientHeight + 50;
          container.innerHTML = '';
          if (data.messages.length === 0) {
            container.innerHTML = '<div class="text-center text-gray-400 text-xs py-10">Нет сохраненных сообщений для этого агента. Напишите первое сообщение в поле ниже!</div>';
            return;
          }
          data.messages.forEach(msg => {
            const isUser = msg.role === 'user';
            const card = document.createElement('div');
            card.className = `flex flex-col ${isUser ? 'items-end' : 'items-start'} space-y-1`;
            
            const bubble = document.createElement('div');
            bubble.className = `max-w-[85%] rounded-xl p-3 text-xs leading-relaxed ${isUser ? 'bg-emerald-600 text-white rounded-br-none shadow-md' : 'bg-dark-850 text-gray-200 border border-dark-750 rounded-bl-none shadow-md'}`;
            
            bubble.innerHTML = `
              <div class="font-bold text-[10px] mb-1 ${isUser ? 'text-emerald-200' : 'text-emerald-400'} flex items-center justify-between gap-4">
                <span>${isUser ? 'Stefan (COO)' : AGENTS_META[profile].name}</span>
                <span class="text-[9px] font-normal opacity-70 font-mono">${msg.time || ''}</span>
              </div>
              <div class="whitespace-pre-wrap font-sans text-xs">${escapeHtml(msg.content)}</div>
            `;
            
            card.appendChild(bubble);
            container.appendChild(card);
          });
          if (isAtBottom) {
            container.scrollTop = container.scrollHeight;
          }
        }
      } catch (e) {
        console.error('Chat load error:', e);
      }
    }

    async function sendChatMessage() {
      const input = document.getElementById('chat-input');
      const text = input.value.trim();
      if (!text) return;

      input.value = '';
      const btn = document.getElementById('chat-send-btn');
      btn.disabled = true;

      try {
        await fetch('/agentos/?api=send_message', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ profile: currentAgent, message: text })
        });
        loadLiveChat(currentAgent);
      } catch (e) {
        alert('Ошибка отправки: ' + e);
      } finally {
        btn.disabled = false;
      }
    }

    function handleChatKey(e) {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendChatMessage();
      }
    }

    // --- SUBHEADER FILTER BAR ---
    function setupFilterBar(options, defaultOption) {
      const bar = document.getElementById('filter-bar');
      const container = document.getElementById('filter-buttons-container');
      container.innerHTML = '';
      currentFilter = defaultOption.toLowerCase();

      options.forEach(opt => {
        const optLower = opt.toLowerCase();
        const btn = document.createElement('button');
        btn.onclick = () => {
          document.querySelectorAll('.filter-btn').forEach(b => {
            b.className = 'filter-btn px-2.5 py-1 rounded-md text-[11px] font-medium text-gray-400 hover:text-white hover:bg-dark-800 transition';
          });
          btn.className = 'filter-btn px-2.5 py-1 rounded-md text-[11px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 transition';
          currentFilter = optLower;
          if (currentTab === 'capabilities') loadCapabilities();
          if (currentTab === 'artifacts') loadArtifacts();
        };
        btn.className = `filter-btn px-2.5 py-1 rounded-md text-[11px] font-medium ${optLower === currentFilter ? 'font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'text-gray-400 hover:text-white hover:bg-dark-800'} transition`;
        btn.innerText = opt;
        container.appendChild(btn);
      });

      bar.classList.remove('hidden');
    }

    // --- CAPABILITIES TAB (Skills, Tools, MCP, Browse Hub) ---
    async function loadCapabilities() {
      const container = document.getElementById('view-content');
      container.innerHTML = '<div class="text-xs text-gray-400 py-10 text-center">Загрузка возможностей и реестра скиллов...</div>';
      try {
        const res = await fetch('/agentos/?api=capabilities');
        const data = await res.json();
        
        let allItems = [];
        if (currentFilter === 'all' || currentFilter === 'skills') allItems = allItems.concat(data.skills || []);
        if (currentFilter === 'all' || currentFilter === 'tools') allItems = allItems.concat(data.tools || []);
        if (currentFilter === 'all' || currentFilter === 'mcp') allItems = allItems.concat(data.mcp || []);
        if (currentFilter === 'all' || currentFilter === 'browse hub' || currentFilter === 'browse_hub') allItems = allItems.concat(data.browse_hub || []);

        document.getElementById('filter-count').innerText = `Всего: ${allItems.length}`;

        let html = `<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">`;
        allItems.forEach(item => {
          const typeBadge = item.type === 'skill' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' :
                            item.type === 'tool' ? 'bg-cyan-500/10 text-cyan-400 border-cyan-500/20' :
                            item.type === 'mcp' ? 'bg-purple-500/10 text-purple-400 border-purple-500/20' :
                            'bg-amber-500/10 text-amber-400 border-amber-500/20';

          html += `
            <div class="bg-dark-900 border border-dark-800 rounded-xl p-3.5 hover:border-dark-700 transition flex flex-col justify-between">
              <div>
                <div class="flex items-start justify-between gap-2 mb-1.5">
                  <div class="font-bold text-xs text-white">${escapeHtml(item.name)}</div>
                  <span class="text-[9px] px-1.5 py-0.2 rounded border font-mono uppercase ${typeBadge}">${item.type}</span>
                </div>
                <div class="text-[11px] text-gray-400 leading-relaxed mb-2.5">${escapeHtml(item.description)}</div>
              </div>
              <div class="text-[10px] text-gray-300 uppercase font-mono pt-2 border-t border-dark-800">
                Категория: <span class="text-gray-300">${item.category}</span>
              </div>
            </div>
          `;
        });
        html += `</div>`;
        container.innerHTML = html;
      } catch (e) {
        container.innerHTML = `<div class="text-xs text-red-400 py-10 text-center">Ошибка: ${e}</div>`;
      }
    }

    // --- ARTIFACTS TAB (Images, Files, Links) ---
    async function loadArtifacts() {
      const container = document.getElementById('view-content');
      container.innerHTML = '<div class="text-xs text-gray-400 py-10 text-center">Загрузка артефактов...</div>';
      try {
        const res = await fetch('/agentos/?api=artifacts');
        const data = await res.json();
        
        let allItems = [];
        if (currentFilter === 'all' || currentFilter === 'images') allItems = allItems.concat(data.images || []);
        if (currentFilter === 'all' || currentFilter === 'files') allItems = allItems.concat(data.files || []);
        if (currentFilter === 'all' || currentFilter === 'links') allItems = allItems.concat(data.links || []);

        document.getElementById('filter-count').innerText = `Всего: ${allItems.length}`;

        let html = `<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">`;
        allItems.forEach(art => {
          const isLink = art.type === 'link';
          html += `
            <div class="bg-dark-900 border border-dark-800 rounded-xl p-3.5 hover:border-dark-700 transition flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between mb-2">
                  <span class="text-xs font-bold text-white truncate">${escapeHtml(art.name)}</span>
                  <span class="text-[9px] px-1.5 py-0.2 rounded font-mono uppercase bg-dark-800 text-gray-300">${art.type}</span>
                </div>
                <div class="text-[11px] text-gray-400 font-mono truncate mb-2">${art.url || art.path || ''}</div>
              </div>
              <div class="flex items-center justify-between text-[10px] text-gray-300 pt-2 border-t border-dark-800 font-mono">
                <span>${art.size || art.category || 'Asset'}</span>
                ${isLink ? `<a href="${art.url}" target="_blank" class="text-emerald-400 hover:underline flex items-center gap-1">Открыть <i data-lucide="external-link" class="w-3 h-3"></i></a>` : `<span class="text-gray-400">${art.time || ''}</span>`}
              </div>
            </div>
          `;
        });
        html += `</div>`;
        container.innerHTML = html;
        lucide.createIcons();
      } catch (e) {
        container.innerHTML = `<div class="text-xs text-red-400 py-10 text-center">Ошибка: ${e}</div>`;
      }
    }

    // --- NATIVE TAB (Dashboard / Crons) ---
    function renderNativeTab(tabId) {
      const container = document.getElementById('view-content');
      if (tabId === 'dashboard') {
        container.innerHTML = `
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div class="bg-dark-900 p-4 rounded-xl border border-dark-800">
              <div class="text-xs text-gray-400">Активных агентов</div>
              <div class="text-2xl font-bold text-white mt-1">7</div>
              <div class="text-[11px] text-emerald-400 mt-1 flex items-center gap-1 font-mono">
                <i data-lucide="check-circle" class="w-3 h-3"></i> 6 Канбанов активны
              </div>
            </div>
            <div class="bg-dark-900 p-4 rounded-xl border border-dark-800">
              <div class="text-xs text-gray-400">Мониторинг вакансий</div>
              <div class="text-2xl font-bold text-white mt-1">~4,800</div>
              <div class="text-[11px] text-cyan-400 mt-1 flex items-center gap-1 font-mono">
                <i data-lucide="zap" class="w-3 h-3"></i> 11 проверенных API
              </div>
            </div>
            <div class="bg-dark-900 p-4 rounded-xl border border-dark-800">
              <div class="text-xs text-gray-400">Cron расписание</div>
              <div class="text-2xl font-bold text-white mt-1">09:00 MSK</div>
              <div class="text-[11px] text-amber-400 mt-1 flex items-center gap-1 font-mono">
                <i data-lucide="clock" class="w-3 h-3"></i> Career Scanner Daily
              </div>
            </div>
            <div class="bg-dark-900 p-4 rounded-xl border border-dark-800">
              <div class="text-xs text-gray-400">Google Workspace</div>
              <div class="text-2xl font-bold text-emerald-400 mt-1">Connected</div>
              <div class="text-[11px] text-gray-400 mt-1 flex items-center gap-1 font-mono">
                <i data-lucide="shield-check" class="w-3 h-3"></i> 10 Production Scopes
              </div>
            </div>
          </div>
          <div class="bg-dark-900 p-5 rounded-xl border border-dark-800 space-y-3">
            <h3 class="font-bold text-sm text-white flex items-center gap-2">
              <i data-lucide="info" class="w-4 h-4 text-emerald-400"></i>
              <span>AgentOS Enterprise Command Architecture</span>
            </h3>
            <p class="text-xs text-gray-400 leading-relaxed">
              У каждого из 7 агентов развернуто полное 6-уровневое рабочее пространство: <b>Dashboard</b> (метрики), <b>Chat</b> (живая двухсторонняя синхронизация со шлюзом и Telegram), <b>Kanban</b> (адаптивная интерактивная доска на всю ширину экрана), <b>Crons</b> (фоновые расписания), <b>Capabilities</b> (Skills / Tools / MCP / Hub) и <b>Artifacts</b> (Images / Files / Links).
            </p>
          </div>
        `;
      } else if (tabId === 'crons') {
        container.innerHTML = '<div class="text-xs text-gray-400 py-10 text-center">Загрузка активных кронов...</div>';
        fetch('/agentos/?api=crons').then(r => r.json()).then(d => {
          let html = '<div class="space-y-3"><h3 class="text-sm font-bold text-white mb-2">Активные Cron-задачи</h3>';
          (d.crons || []).forEach(c => {
            html += `
              <div class="p-3.5 bg-dark-900 rounded-xl border border-dark-800 flex items-center justify-between">
                <div>
                  <div class="text-xs font-bold text-white">${escapeHtml(c.name || 'Cron #' + c.id)}</div>
                  <div class="text-[10px] text-gray-400 font-mono mt-0.5">${c.schedule || 'manual'} | ID: ${c.id}</div>
                  <div class="text-[11px] text-gray-400 mt-1">${escapeHtml(c.prompt || '')}</div>
                </div>
                <span class="text-[10px] bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2 py-0.5 rounded font-mono">active</span>
              </div>`;
          });
          html += '</div>';
          container.innerHTML = html;
        });
      }
      lucide.createIcons();
    }

    // --- SETTINGS MODAL ---
    async function openSettingsModal() {
      const modal = document.getElementById('settings-modal');
      const list = document.getElementById('settings-models-list');
      modal.classList.remove('hidden');
      list.innerHTML = '<div class="text-gray-400 text-xs py-4 text-center">Загрузка каталога моделей...</div>';

      try {
        const res = await fetch('/agentos/?api=settings');
        const data = await res.json();
        list.innerHTML = '';
        (data.models || []).forEach(m => {
          const tierColor = m.tier === 'Primary' ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30' :
                            m.tier.includes('NIM') ? 'bg-green-500/20 text-green-300 border-green-500/30' :
                            m.tier.includes('HF') ? 'bg-purple-500/20 text-purple-300 border-purple-500/30' :
                            'bg-dark-750 text-gray-300 border-dark-650';

          const item = document.createElement('div');
          item.className = 'p-2.5 bg-dark-850 rounded-lg border border-dark-750 flex items-center justify-between';
          item.innerHTML = `
            <div>
              <div class="text-xs font-bold text-white font-mono">${escapeHtml(m.id)}</div>
              <div class="text-[10px] text-gray-400 mt-0.5">${escapeHtml(m.desc)}</div>
            </div>
            <div class="flex items-center gap-2">
              <span class="text-[9px] px-2 py-0.5 rounded border font-mono ${tierColor}">${m.tier}</span>
              <span class="text-[9px] text-gray-400 uppercase font-mono">${m.provider}</span>
            </div>
          `;
          list.appendChild(item);
        });
      } catch (e) {
        list.innerHTML = `<div class="text-red-400 text-xs py-4 text-center">Ошибка: ${e}</div>`;
      }
    }

    function closeSettingsModal() {
      document.getElementById('settings-modal').classList.add('hidden');
    }

    function refreshCurrentView() {
      selectSubTab(currentTab);
    }

    function escapeHtml(text) {
      if (!text) return '';
      return String(text).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }

    // Boot AgentOS with Hermes
    selectAgent('hermes');
  </script>
</body>
</html>
