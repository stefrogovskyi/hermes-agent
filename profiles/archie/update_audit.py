import re

with open('/opt/hermes/profiles/archie/audit.py') as f:
    code = f.read()

code = code.replace(
    'facts = [\n        "$50 per m³", "$250", "$170 per m³", "$200 per m³", "500 USD", "15 days", "30%", "50%", "3 days", "48 hours", "5 business days", "5 calendar days", "6000", "1000", "sales@searates.com"\n    ]',
    'facts = [\n        "USD 50 per m³", "USD 250", "USD 170 per m³", "USD 200 per m³", "500 USD", "15 days", "30%", "50%", "3 days", "48 hours", "5 business days", "5 calendar days", "6000", "1000", "sales@searates.com"\n    ]'
)

with open('/opt/hermes/profiles/archie/audit.py', 'w') as f:
    f.write(code)
