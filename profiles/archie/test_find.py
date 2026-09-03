from test_audit_fixes import body

k = "multi-carrier shipping API integration"
print("k:", repr(k))
print("k.lower():", repr(k.lower()))
print("k.lower() in body.lower():", k.lower() in body.lower())
