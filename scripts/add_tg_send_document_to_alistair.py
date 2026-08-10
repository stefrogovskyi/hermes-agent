import os, py_compile

path = r'C:\Users\Stefan\My Drive\Equity\My Biz\Partner companies\Navo\6. Departments\Alister Sterling\Alistair Hermes\alistair_bot.py'
code = open(path, encoding='utf-8', errors='ignore').read()

send_doc_func = '''def tg_send_document(token, chat_id, file_path, caption=None):
    """Отправляет файл (документ/HTML/PDF/Excel) напрямую в Telegram чат/группу."""
    import uuid
    boundary = uuid.uuid4().hex
    headers = {"Content-Type": f"multipart/form-data; boundary={boundary}", "User-Agent": "Mozilla/5.0/HermesAgent"}
    filename = os.path.basename(file_path)
    file_bytes = open(file_path, "rb").read()
    
    body = []
    body.append(f"--{boundary}\\r\\nContent-Disposition: form-data; name=\\"chat_id\\"\\r\\n\\r\\n{chat_id}\\r\\n".encode("utf-8"))
    if caption:
        body.append(f"--{boundary}\\r\\nContent-Disposition: form-data; name=\\"caption\\"\\r\\n\\r\\n{caption}\\r\\n".encode("utf-8"))
        body.append(f"--{boundary}\\r\\nContent-Disposition: form-data; name=\\"parse_mode\\"\\r\\n\\r\\nMarkdown\\r\\n".encode("utf-8"))
    body.append(f"--{boundary}\\r\\nContent-Disposition: form-data; name=\\"document\\"; filename=\\"{filename}\\"\\r\\nContent-Type: application/octet-stream\\r\\n\\r\\n".encode("utf-8"))
    body.append(file_bytes)
    body.append(f"\\r\\n--{boundary}--\\r\\n".encode("utf-8"))
    
    payload = b"".join(body)
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    req = urllib.request.Request(url, data=payload, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"[Alistair] sendDocument error: {e}")
        return None
'''

if 'def tg_send_document' not in code:
    code = code.replace('def tg_send_message(', send_doc_func + '\n\ndef tg_send_message(')

open(path, 'w', encoding='utf-8').write(code)
py_compile.compile(path, doraise=True)
print("Successfully added tg_send_document to alistair_bot.py!")
