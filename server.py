import asyncio
from aiohttp import web

EMITTER = None
RECEIVER = None

async def websocket_handler(request):
    global EMITTER, RECEIVER

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    role = await ws.receive_str()

    if role == "EMITTER":
        EMITTER = ws
        print("Emisor conectado")

    elif role == "RECEIVER":
        RECEIVER = ws
        print("Receptor conectado")

    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            if ws == EMITTER and RECEIVER:
                await RECEIVER.send_str(msg.data)
            elif ws == RECEIVER and EMITTER:
                await EMITTER.send_str(msg.data)

    return ws

# 👇 HTTP normal para Render (health check)
async def health(request):
    return web.Response(text="OK")

app = web.Application()
app.router.add_get("/", health)
app.router.add_get("/ws", websocket_handler)

web.run_app(app, port=int(__import__("os").environ.get("PORT", 10000)))
