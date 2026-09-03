import json

with open('draft.json') as f:
    d = json.load(f)

body = d['body']
print("Target: 'API rate integration'")
print("In body exact:", 'API rate integration' in body)
print("In body lower:", 'api rate integration' in body.lower())
