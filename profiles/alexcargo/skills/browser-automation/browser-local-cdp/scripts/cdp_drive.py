#!/usr/bin/env python
# cdp_drive.py - minimal Chrome DevTools Protocol driver for the USER's real
# Chrome (or any CDP endpoint). Use when config.yaml browser.cdp_url can't be
# changed (agent is blocked from editing it). Requires `websockets` (in venv).
#
# Library:
#   from cdp_drive import CDP
#   async with CDP(9223) as c:
#       await c.open("https://silpo.ua/")      # attach or create tab
#       html = await c.snapshot()              # ARIA HTML (Page.captureSnapshot)
#       await c.click_text("Додати у кошик")   # click el whose text contains str
#       await c.type_text("380636222272")      # set active field value + input evt
#       await c.navigate("https://silpo.ua/category/x")
#
# CLI:
#   python cdp_drive.py --port 9223 --url https://silpo.ua/ --snapshot
#   python cdp_drive.py --port 9223 --click "Додати у кошик"
#   python cdp_drive.py --port 9223 --type "380636222272" --selector "#phone"
import asyncio, json, sys, urllib.request, argparse, websockets


class CDP:
    def __init__(self, port=9223):
        self.port = port
        self.browser = None
        self.ws = None
        self.tab = None
        self._id = 0

    async def __aenter__(self):
        self.browser = await websockets.connect(self._browser_ws(), max_size=None)
        return self

    async def __aexit__(self, *a):
        if self.ws:
            await self.ws.close()
        if self.browser:
            await self.browser.close()

    def _browser_ws(self):
        d = json.load(urllib.request.urlopen(
            f"http://127.0.0.1:{self.port}/json/version", timeout=10))
        return d["webSocketDebuggerUrl"]

    def _tabs(self):
        return json.load(urllib.request.urlopen(
            f"http://127.0.0.1:{self.port}/json", timeout=10))

    async def _send(self, ws, method, params=None):
        self._id += 1
        await ws.send(json.dumps({"id": self._id, "method": method, "params": params or {}}))
        while True:
            r = json.loads(await asyncio.wait_for(ws.recv(), timeout=15))
            if r.get("id") == self._id:
                return r

    async def open(self, url=None, url_substr="silpo"):
        """Attach to an existing matching tab, else create one from url."""
        for t in self._tabs():
            if t.get("type") == "page" and url_substr in t.get("url", ""):
                self.tab = t
                break
        if not self.tab and url:
            r = await self._send(self.browser, "Target.createTarget", {"url": url})
            tid = r["result"]["targetId"]
            for t in self._tabs():
                if t.get("targetId") == tid:
                    self.tab = t
                    break
        if not self.tab:
            raise RuntimeError("no tab (pass --url to create one)")
        self.ws = await websockets.connect(self.tab["webSocketDebuggerUrl"], max_size=None)
        await self._send(self.ws, "Page.enable", {})
        return self.tab

    async def snapshot(self):
        # Page.captureSnapshot (aria) — NOT Accessibility.getFullAXTree (v151 returns
        # no 'axTree' key → KeyError).
        r = await self._send(self.ws, "Page.captureSnapshot", {"format": "aria"})
        return r["result"]["data"]

    async def click_text(self, text, selector="button,a,div"):
        js = (
            "(() => {"
            "  const els = [...document.querySelectorAll(" + json.dumps(selector) + ")];"
            "  const e = els.find(x => (x.innerText||'').trim().includes(" + json.dumps(text) + "));"
            "  if (e) { e.click(); return 'clicked: ' + (e.innerText||'').slice(0,40); }"
            "  return 'NOT FOUND';"
            "})()"
        )
        r = await self._send(self.ws, "Runtime.evaluate",
                             {"expression": js, "returnByValue": True, "awaitPromise": True})
        return r["result"]["result"].get("value")

    async def type_text(self, text, selector=None):
        field = ("document.querySelector(" + json.dumps(selector) + ")") if selector else "document.activeElement"
        js = (
            "(() => {"
            "  const el = " + field + ";"
            "  if (!el) return 'NO FIELD';"
            "  el.focus();"
            "  el.value = " + json.dumps(text) + ";"
            "  el.dispatchEvent(new Event('input', {bubbles:true}));"
            "  el.dispatchEvent(new Event('change', {bubbles:true}));"
            "  return 'typed';"
            "})()"
        )
        r = await self._send(self.ws, "Runtime.evaluate",
                             {"expression": js, "returnByValue": True})
        return r["result"]["result"].get("value")

    async def navigate(self, url):
        await self._send(self.ws, "Page.navigate", {"url": url})


async def _cli():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=9223)
    ap.add_argument("--url")
    ap.add_argument("--substr", default="silpo")
    ap.add_argument("--snapshot", action="store_true")
    ap.add_argument("--click")
    ap.add_argument("--type")
    ap.add_argument("--selector")
    a = ap.parse_args()
    async with CDP(a.port) as c:
        await c.open(a.url, a.substr)
        if a.snapshot:
            print((await c.snapshot())[:8000])
        if a.click:
            print(await c.click_text(a.click))
        if a.type:
            print(await c.type_text(a.type, a.selector))


if __name__ == "__main__":
    asyncio.run(_cli())
