with open('draft2.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace ### and #### with ##
text = text.replace('### ', '## ').replace('#### ', '## ')

with open('draft3.md', 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved draft3.md")
