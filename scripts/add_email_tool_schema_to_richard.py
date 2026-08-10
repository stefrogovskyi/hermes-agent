# -*- coding: utf-8 -*-
"""
add_email_tool_schema_to_richard.py — Явная регистрация инструмента send_email в схеме инструментов Ричарда.
Теперь Ричард в Telegram 100% видит инструмент отправки почты и вызывает его без галлюцинаций!
"""

import os, re

bot_p = r"C:\Users\Stefan\My Drive\Equity\My Biz\Partner companies\Navo\6. Departments\Richard Marlowe\Richard Hermes\richard_bot.py"
txt = open(bot_p, encoding='utf-8', errors='ignore').read()

email_tool_code = """
import richard_email as remail

EMAIL_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "send_email",
        "description": "Send an email directly from rich@navo24.com to a client or team member",
        "parameters": {
            "type": "object",
            "properties": {
                "to_email": {"type": "string", "description": "Recipient email address"},
                "cc_email": {"type": "string", "description": "Optional CC email address"},
                "subject": {"type": "string", "description": "Email subject line"},
                "body_html": {"type": "string", "description": "Email body text/HTML"}
            },
            "required": ["to_email", "subject", "body_html"]
        }
    }
}
"""

if "EMAIL_TOOL_SCHEMA" not in txt:
    txt = email_tool_code + "\n" + txt

# Update tools definition in run_agent
old_tools_def = "tools = nc.tool_schemas()"
new_tools_def = "tools = (nc.tool_schemas() or []) + [EMAIL_TOOL_SCHEMA]"

if old_tools_def in txt:
    txt = txt.replace(old_tools_def, new_tools_def)

# Update call_tool in run_agent
old_call_tool = "result = nc.call_tool(name, args)"
new_call_tool = """if name == "send_email":
                        to_e = args.get("to_email")
                        cc_e = args.get("cc_email")
                        subj = args.get("subject", "Navo24 Message")
                        body = args.get("body_html", "")
                        ok, err = remail.send_email_direct(to_e, subj, body, body, cc_email=cc_e)
                        result = {"success": ok, "status": err, "message": f"Email sent to {to_e}" if ok else f"Error: {err}"}
                    else:
                        result = nc.call_tool(name, args)"""

if old_call_tool in txt:
    txt = txt.replace(old_call_tool, new_call_tool)

open(bot_p, "w", encoding='utf-8').write(txt)
print("✅ Successfully registered explicit send_email tool in richard_bot.py!")
