# Self-Signed SSL Deployment Recipe for Tailscale/LAN WebRTC & MediaDevices

Modern browsers (Chrome, Edge, Firefox, Safari) enforce W3C Secure Context for media APIs:
- `navigator.mediaDevices.getDisplayMedia` (Screen capture)
- `navigator.mediaDevices.getUserMedia` (Microphone / Webcam)
- Web Speech API (`webkitSpeechRecognition`)

When accessed via plain `http://<ip>:<port>`, browsers strip `navigator.mediaDevices`, throwing:
`Cannot read properties of undefined (reading 'getDisplayMedia')`

## 1. Python Generation of SAN (Subject Alternative Name) SSL Certificate
To enable access over LAN / Tailscale IP (e.g., `100.79.157.46`), create a certificate with both IP SAN and DNS SAN:

```python
import datetime, ipaddress
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa

key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "UA"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Ecosystem"),
    x509.NameAttribute(NameOID.COMMON_NAME, "100.79.157.46"),
])

cert = x509.CertificateBuilder().subject_name(
    subject
).issuer_name(
    issuer
).public_key(
    key.public_key()
).serial_number(
    x509.random_serial_number()
).not_valid_before(
    datetime.datetime.now(datetime.timezone.utc)
).not_valid_after(
    datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=3650)
).add_extension(
    x509.SubjectAlternativeName([
        x509.IPAddress(ipaddress.IPv4Address("100.79.157.46")),
        x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
        x509.DNSName("localhost"),
    ]),
    critical=False,
).sign(key, hashes.SHA256())

with open("cert.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

with open("key.pem", "wb") as f:
    f.write(key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    ))
```

## 2. Aiohttp Server SSL Integration
```python
import ssl, os
from aiohttp import web

app = web.Application()
# routes setup...

cert_path = "cert.pem"
key_path = "key.pem"
ssl_context = None

if os.path.exists(cert_path) and os.path.exists(key_path):
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(cert_path, key_path)

web.run_app(app, host='0.0.0.0', port=8765, ssl_context=ssl_context)
```

## 3. Client Interaction Rule
1. User opens `https://<tailscale_ip>:<port>`.
2. Browser displays standard self-signed certificate warning ("Your connection is not private").
3. User clicks **Advanced** -> **Proceed to <ip> (unsafe)** once.
4. All media streams, screen capture, and secure WebSockets (`wss://`) function normally with full permissions.
