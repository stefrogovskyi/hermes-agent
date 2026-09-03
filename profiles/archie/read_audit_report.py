with open('/opt/hermes/profiles/archie/audit_report.md', 'r') as f:
    text = f.read()

print(text[:3000])
