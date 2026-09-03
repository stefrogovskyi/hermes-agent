import re

with open('check_revised_draft.py') as f:
    text = f.read()

start = text.find('revised_draft = """') + len('revised_draft = """')
end = text.find('"""', start)
final_text = text[start:end]

with open('final_article.txt', 'w', encoding='utf-8') as f:
    f.write(final_text)

print("Saved to final_article.txt")
