with open('/opt/hermes/profiles/archie/extracted_goal.txt', 'rb') as f:
    content = f.read()
print("Raw length:", len(content))
print(content.decode('utf-8', errors='ignore'))
