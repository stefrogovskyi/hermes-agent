from test_audit_fixes import body

s1 = "multi-carrier shipping API integration".lower()
print("s1:", [ord(c) for c in s1])

for line in body.split("\n"):
    if "multi-carrier" in line.lower():
        print("line:", line)
        print("line ords:", [ord(c) for c in line.lower() if "multi" in line.lower() or "carrier" in line.lower()])
