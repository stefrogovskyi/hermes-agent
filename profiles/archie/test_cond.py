from test_audit_fixes import body

cond1 = "expanding multi-carrier shipping API integration across ocean and air routes remains a core focus" not in body.lower()
cond2 = "multi-carrier shipping API integration" in body.lower()

print("cond1:", cond1)
print("cond2:", cond2)
print("cond1 and cond2:", cond1 and cond2)
