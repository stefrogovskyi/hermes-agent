const { default: makeWASocket, useMultiFileAuthState, DisconnectReason } = require("@whiskeysockets/baileys");
const QRCode = require('qrcode');
const express = require('express');
const cors = require('cors');
const pino = require('pino');
const fs = require('fs');
const path = require('path');

const app = express();
app.use(cors());
app.use(express.json());

const PORT = 3050;
let sock = null;
let qrCodeDataURL = null;
let connectionStatus = "disconnected"; // disconnected, qr_ready, connected, connecting

async function connectToWhatsApp() {
    const authPath = path.join(__dirname, 'auth_info_baileys');
    const { state, saveCreds } = await useMultiFileAuthState(authPath);

    sock = makeWASocket({
        logger: pino({ level: 'silent' }),
        printQRInTerminal: false,
        auth: state,
        browser: ["Avalanche Agency CRM", "Chrome", "1.0.0"]
    });

    sock.ev.on('creds.update', saveCreds);

    sock.ev.on('connection.update', async (update) => {
        const { connection, lastDisconnect, qr } = update;

        if (qr) {
            qrCodeDataURL = await QRCode.toDataURL(qr);
            connectionStatus = "qr_ready";
            console.log("⚡️ QR Code updated. Waiting for scan...");
        }

        if (connection === 'close') {
            const statusCode = lastDisconnect?.error?.output?.statusCode;
            const shouldReconnect = statusCode !== DisconnectReason.loggedOut;
            connectionStatus = "disconnected";
            console.log(`Connection closed (reason: ${statusCode}). Reconnecting: ${shouldReconnect}`);
            if (shouldReconnect) {
                setTimeout(connectToWhatsApp, 3000);
            }
        } else if (connection === 'open') {
            connectionStatus = "connected";
            qrCodeDataURL = null;
            console.log("✅ WhatsApp successfully connected!");
        }
    });

    sock.ev.on('messages.upsert', async m => {
        // Handle incoming messages if needed
    });
}

// API Routes
app.get('/status', (req, res) => {
    res.json({
        status: connectionStatus,
        hasQr: !!qrCodeDataURL,
        qr: qrCodeDataURL
    });
});

app.post('/send-message', async (req, res) => {
    try {
        const { phone, message } = req.body;
        if (!phone || !message) {
            return res.status(400).json({ error: 'Phone and message required' });
        }

        if (connectionStatus !== 'connected' || !sock) {
            return res.status(503).json({ error: 'WhatsApp not connected. Please scan QR code first.' });
        }

        let cleanPhone = phone.replace(/[^0-9]/g, '');
        if (cleanPhone.length === 10) cleanPhone = '1' + cleanPhone; // Default to US if 10 digits
        const jid = `${cleanPhone}@s.whatsapp.net`;

        const exists = await sock.onWhatsApp(jid);
        if (!exists || !exists[0]?.exists) {
            return res.status(404).json({ error: 'Number not registered on WhatsApp', phone: cleanPhone });
        }

        const sentMsg = await sock.sendMessage(exists[0].jid, { text: message });
        res.json({ success: true, messageId: sentMsg.key.id, to: cleanPhone });
    } catch (err) {
        console.error("Send error:", err);
        res.status(500).json({ error: err.message });
    }
});

app.listen(PORT, () => {
    console.log(`🚀 WhatsApp Gateway running on port ${PORT}`);
    connectToWhatsApp();
});
