# Mission Control & OpenClaw Agentic OS Setup

## Architecture
- **Mission Control Web Dashboard**: Port `8888` (systemd: `mission-control.service`, path: `/opt/hermes/mission-control/`).
- **OpenClaw Control Gateway**: Port `18789` (systemd: `openclaw.service`, path: `/opt/openclaw/app/`).
- **Tailscale Access**: `http://100.99.146.42:8888` for Mission Control, `http://100.99.146.42:18789` for OpenClaw.

## Installation & Build Recipe for OpenClaw
```bash
# Node.js 22 + pnpm
curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
apt-get install -y nodejs
npm install -g pnpm

# Clone & Build
mkdir -p /opt/openclaw && cd /opt/openclaw
git clone https://github.com/openclaw/openclaw.git app
cd app
pnpm install
pnpm build
pnpm ui:build

# Symlink CLI
ln -sf /opt/openclaw/app/dist/entry.js /usr/local/bin/openclaw
chmod +x /opt/openclaw/app/dist/entry.js
```

## Configuration & Daemon
```bash
openclaw config set gateway.mode local
openclaw config set gateway.port 18789
openclaw config set gateway.bind loopback
openclaw config set gateway.auth.mode none
```

Systemd unit `/etc/systemd/system/openclaw.service`:
```ini
[Unit]
Description=OpenClaw Gateway Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/openclaw/app
Environment=PATH=/usr/local/bin:/usr/bin:/bin:/root/.local/bin
Environment=NODE_ENV=production
ExecStart=/usr/bin/node /opt/openclaw/app/dist/entry.js gateway run --port 18789 --bind loopback
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```
